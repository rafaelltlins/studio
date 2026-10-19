#!/usr/bin/env python3
"""Verifica a configuração do Graphify numa máquina e num repositório.

Uso:  python verificar_setup.py [pasta-do-repositorio]

Só usa a biblioteca padrão. Não altera nada: apenas lê e relata.
Saída: uma linha por verificação, com OK / AVISO / FALHA, e um resumo final.
Código de saída 0 = sem falhas; 1 = alguma falha.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RESULTS: list[tuple[str, str, str]] = []

# Pastas privadas de apps empacotados (MSIX) no Windows. Um Python que resolve
# para cá só existe dentro do app que o instalou (ex.: app desktop do Claude).
ISOLATED_MARKERS = ("\\packages\\", "\\localcache\\")

GITIGNORE_EXPECTED = [
    "graphify-out/cost.json",
    "graphify-out/.graphify_python",
    "graphify-out/.graphify_root",
    "graphify-out/.graphify_analysis.json",
    "graphify-out/cache/stat-index.json",
    "graphify-out/cache/last_query_stamp",
    "graphify-out/obsidian/",
]
DATED_BACKUP = "graphify-out/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/"
VERSIONED_FILES = ["graph.json", "manifest.json", "GRAPH_REPORT.md", ".graphify_labels.json"]
HOOKS = ["post-commit", "post-checkout", "post-merge", "post-rewrite"]


def add(level: str, item: str, detail: str) -> None:
    RESULTS.append((level, item, detail))


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return 127, "comando não encontrado"
    except subprocess.TimeoutExpired:
        return 124, "tempo esgotado"


def is_isolated(path: str) -> bool:
    low = path.lower().replace("/", "\\")
    return all(m in low for m in ISOLATED_MARKERS)


def check_machine() -> str | None:
    if os.name == "nt" and os.environ.get("CLAUDE_CODE_ENTRYPOINT") == "claude-desktop":
        add("INFO", "app desktop do Claude",
            "instalar pacotes (uv, graphify, Obsidian) daqui iria para a pasta privada do app; peça à pessoa "
            "para instalar num terminal comum. Comandos do graphify no repositório podem rodar daqui se a "
            "linha 'local da instalação' estiver OK")
    exe = shutil.which("graphify")
    if not exe:
        add("FALHA", "graphify no PATH", "não encontrado; instale com `uv tool install graphifyy` num terminal comum")
        return None
    code, out = run(["graphify", "--version"])
    add("OK" if code == 0 else "FALHA", "graphify --version", out.splitlines()[-1] if out else f"saída {code}")

    py = None
    uv = shutil.which("uv")
    if uv:
        _, tool_dir = run(["uv", "tool", "dir"])
        cand = Path(tool_dir.strip()) / "graphifyy" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if cand.exists():
            py = str(cand)
    if py:
        _, real = run([py, "-c", "import sys, os; print(os.path.realpath(sys.executable))"])
        if is_isolated(real):
            add("FALHA", "instalação isolada",
                f"o Python do Graphify resolve para {real}. Ela só existe dentro do app que a criou; "
                "reinstale num terminal comum (`uv tool install graphifyy --force`) e rode `graphify hook install` de novo")
        else:
            add("OK", "local da instalação", real)
    else:
        add("AVISO", "local da instalação", "não localizei o ambiente do uv (instalado por pip/pipx?)")

    skill = Path.home() / ".claude" / "skills" / "graphify" / "SKILL.md"
    add("OK" if skill.exists() else "AVISO", "skill /graphify no Claude Code",
        "instalada" if skill.exists() else "ausente; rode `graphify install` (só necessário para o Claude Code)")
    return py


def check_repo(repo: Path) -> None:
    code, top = run(["git", "rev-parse", "--show-toplevel"], cwd=repo)
    if code != 0:
        add("FALHA", "repositório Git", f"{repo} não é um repositório Git")
        return
    repo = Path(top)
    out_dir = repo / "graphify-out"

    graph = out_dir / "graph.json"
    if not graph.exists():
        add("AVISO", "graphify-out/graph.json", "ainda não existe (repositório não adotado ou grafo não gerado)")
    else:
        try:
            data = json.loads(graph.read_text(encoding="utf-8"))
            add("OK", "graphify-out/graph.json", f"{len(data.get('nodes', []))} nós")
        except Exception as e:  # noqa: BLE001
            add("FALHA", "graphify-out/graph.json", f"não é JSON válido: {e}")
        code, _ = run(["git", "ls-files", "--error-unmatch", "graphify-out/graph.json"], cwd=repo)
        add("OK" if code == 0 else "AVISO", "grafo versionado",
            "graph.json está no Git" if code == 0 else "graph.json ainda não foi commitado")

    # Hooks: instalados e apontando para um Python que existe e não está isolado.
    _, git_dir = run(["git", "rev-parse", "--git-common-dir"], cwd=repo)
    hooks_dir = (repo / git_dir).resolve() if not Path(git_dir).is_absolute() else Path(git_dir)
    hooks_dir = hooks_dir / "hooks"
    for name in HOOKS:
        f = hooks_dir / name
        if not f.exists() or "graphify" not in f.read_text(encoding="utf-8", errors="replace"):
            add("FALHA", f"hook {name}", "não instalado; rode `graphify hook install`")
            continue
        m = re.search(r"_PINNED='([^']*)'", f.read_text(encoding="utf-8", errors="replace"))
        pinned = m.group(1) if m else ""
        if pinned and is_isolated(pinned):
            add("FALHA", f"hook {name}", f"aponta para instalação isolada ({pinned}); rode `graphify hook install` num terminal comum")
        elif pinned and not Path(pinned).exists():
            add("FALHA", f"hook {name}", f"aponta para Python inexistente ({pinned}); rode `graphify hook install`")
        else:
            add("OK", f"hook {name}", "instalado")

    code, hp = run(["git", "config", "--get", "core.hooksPath"], cwd=repo)
    if code == 0 and hp.strip():
        add("AVISO", "core.hooksPath", f"definido como '{hp.strip()}': o Git ignora .git/hooks e os hooks do "
            "graphify não rodam; integre-os nesse diretório ou remova a configuração")

    code, drv = run(["git", "config", "--get", "merge.graphify.driver"], cwd=repo)
    if code != 0:
        add("FALHA", "merge driver do graph.json", "não registrado; rode `graphify hook install`")
    elif is_isolated(drv):
        add("FALHA", "merge driver do graph.json", "aponta para instalação isolada; rode `graphify hook install` num terminal comum")
    else:
        add("OK", "merge driver do graph.json", "registrado")

    gi = repo / ".gitignore"
    text = gi.read_text(encoding="utf-8", errors="replace") if gi.exists() else ""
    missing = [p for p in GITIGNORE_EXPECTED if p not in text]
    if DATED_BACKUP not in text:
        missing.append(DATED_BACKUP)
    if re.search(r"^\s*graphify-out/?\s*$", text, re.M):
        add("AVISO", ".gitignore", "graphify-out/ inteiro está ignorado; a prática da equipe é versionar o grafo e o cache")
    elif missing:
        add("AVISO", ".gitignore", "faltam: " + ", ".join(missing))
    else:
        add("OK", ".gitignore", "arquivos de máquina e backups ignorados")

    # Arquivos versionados não podem carregar caminhos desta máquina.
    home = str(Path.home())
    needles = {home, home.replace("\\", "/"), home.replace("\\", "\\\\"), str(repo), str(repo).replace("\\", "/")}
    leaks = []
    for name in VERSIONED_FILES:
        f = out_dir / name
        if f.exists():
            body = f.read_text(encoding="utf-8", errors="replace")
            if any(n and n in body for n in needles):
                leaks.append(name)
    if leaks:
        add("AVISO", "caminhos absolutos", "encontrados em: " + ", ".join(leaks) + " (não devem ir para o Git)")
    elif out_dir.exists():
        add("OK", "caminhos absolutos", "nenhum nos arquivos versionados")

    settings = repo / ".claude" / "settings.json"
    if settings.exists():
        body = settings.read_text(encoding="utf-8", errors="replace")
        if "graphify hook-guard" in body:
            absolute = re.search(r'"command"\s*:\s*"[^"]*[\\/][^"]*graphify[^"]*hook-guard', body)
            add("AVISO" if absolute else "OK", "integração Claude Code",
                "hook-guard com caminho absoluto; use `graphify claude install --project`" if absolute
                else "hooks PreToolUse portáveis em .claude/settings.json")
        else:
            add("AVISO", "integração Claude Code", "sem hooks PreToolUse do graphify em .claude/settings.json")


def main() -> int:
    if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # saída lida por agentes/pipes
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(f"Verificando máquina e repositório: {repo}\n")
    check_machine()
    check_repo(repo)
    width = max(len(i) for _, i, _ in RESULTS)
    for level, item, detail in RESULTS:
        print(f"[{level:5}] {item:<{width}}  {detail}")
    fails = sum(1 for l, _, _ in RESULTS if l == "FALHA")
    warns = sum(1 for l, _, _ in RESULTS if l == "AVISO")
    print(f"\nResumo: {fails} falha(s), {warns} aviso(s).")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
