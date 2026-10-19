---
name: graphify-setup
description: Configura o Graphify (grafo de conhecimento para agentes de IA) e, opcionalmente, o Obsidian num repositório seguindo as práticas da equipe, ou integra uma pessoa a um clone que já usa Graphify, verificando a máquina, os hooks do Git e a IDE e explicando as práticas. Use sempre que alguém pedir para instalar, configurar, adotar ou "colocar o graphify" num projeto; para preparar a máquina ou um clone recém-feito de um repositório que tem graphify-out/; para conferir se hooks/merge driver/.gitignore do Graphify estão certos; para abrir o grafo no Obsidian; ou para explicar à equipe como trabalhar com o grafo (o que versionar, quando atualizar, custos, riscos). Não use para simples consultas ao grafo já pronto (isso é a skill graphify / graphify query).
---

# graphify-setup

Roteiro para levar um repositório (ou uma pessoa) ao estado que a equipe considera "Graphify bem configurado": grafo versionado e portátil, hooks do Git atualizando sozinhos, agente de IA consultando o grafo, e a pessoa entendendo o que fazer no dia a dia.

Responda no idioma da pessoa, em linguagem simples e só com o necessário. Os porquês e detalhes estão em `references/praticas.md`; leia a seção pertinente quando for explicar algo ou surgir dúvida.

## 1. Descobrir o modo

Rode `git status --short`, `git branch --show-current` e `git ls-files --error-unmatch graphify-out/graph.json` (código de saída 0 = versionado; sem `--error-unmatch` o comando sai 0 mesmo sem o arquivo).

| Situação | Modo |
|---|---|
| `graph.json` versionado | **Integrar membro** (seção 4) |
| Sem `graphify-out/` | **Adotar no repositório** (seção 3) |
| `graphify-out/` existe mas não versionado | Pergunte: terminar a adoção (seção 3 a partir de E2) ou só uso pessoal |
| Pedido só de verificar | Verificação (seção 5) |

Fora de um repositório Git os hooks não se aplicam: avise e pergunte se segue só com o grafo.

## 2. Verificar a máquina (todos os modos)

Rode o script, que só lê:

```bash
python -I <dir-desta-skill>/scripts/verificar_setup.py <pasta-do-repo>
```

Sem `python` no PATH, use o do Graphify: no PowerShell, `& "$(uv tool dir)\graphifyy\Scripts\python.exe" -I <script> <repo>`; no Linux/macOS, `"$(uv tool dir)/graphifyy/bin/python"`.

**Quem instala.** Instalar software (uv, Graphify, Obsidian) pede o "sim" da pessoa. No Windows, se o agente roda dentro de um app empacotado, tudo o que ele grava em `AppData` vai para a pasta privada do app (`AppData\Local\Packages\<app>\LocalCache\...`). O Graphify ficaria invisível para o terminal e as IDEs da pessoa, e os hooks apontariam para lá. Sinais: a variável `CLAUDE_CODE_ENTRYPOINT=claude-desktop` (o script avisa) ou caminhos de skills/sessão sob `AppData\Local\Packages\`. Nesse caso **não instale você mesmo**: passe os comandos para a pessoa rodar num terminal comum (PowerShell/Windows Terminal), um por bloco, espere a confirmação e verifique de novo:

```bash
winget install --id astral-sh.uv -e
uv tool install graphifyy --force
graphify install
cd <pasta-do-repo>
graphify hook install
```

A regra vale para **instalar pacotes**. Comandos do próprio Graphify no repositório (`graphify hook install`, `update`, `claude install --project`…) você pode rodar mesmo dentro do app, desde que o script mostre "local da instalação" OK (instalação real, fora de `Packages`): os hooks apontam para o Python que o script verificou.

Se você já tiver criado uma cópia isolada nesta sessão, remova-a depois que a instalação real funcionar: só as pastas `uv` dentro de `...\LocalCache\Roaming` e `...\LocalCache\Local` daquele app. Em terminal comum, Linux ou macOS, instalar diretamente é normal (`uv tool install graphifyy`, pacote com dois "y").

Skill do agente: `graphify install` (Claude Code) ou `graphify install --platform <codex|cursor|gemini|copilot|antigravity|…>`.

## 3. Adotar no repositório

### Decisões (antes de mudar arquivos)

Faça uma pergunta por decisão, juntando-as numa única chamada da ferramenta de perguntas quando ela existir, com a recomendação como primeira opção:

- **D1 Branch:** sugira `chore/graphify-setup`. Se houver alterações pendentes de outro trabalho, avise que vão junto e que convém commitá-las à parte.
- **D2 Modo:** mostre antes o corpus (arquivos por tipo).
  - *Sem LLM* (recomendado para começar, repositórios grandes e pilotos): código + estrutura dos Markdown (títulos, links), **zero tokens**.
  - *Completo*: além disso, leitura semântica de docs/PDFs/imagens pelo LLM do agente. Custa tokens uma vez por arquivo (referência: ~200 mil tokens para ~22 mil palavras de Markdown) e **cada imagem é uma chamada de visão**.
- **D3 Exclusões:** proponha um `.graphifyignore` (sintaxe do `.gitignore`) para imagens já descritas em texto, dados, código gerado, fixtures. O `.gitignore` já é respeitado.
- **D4 Obsidian:** se querem o cofre para navegação.

### Execução

**E1. Gerar o grafo.**
- *Sem LLM:* `graphify update .` — funciona como primeira geração, produz `graph.json`, `GRAPH_REPORT.md`, `graph.html`, sem tokens, e é o mesmo caminho que os hooks usam depois. Os nomes de comunidade saem só como sugestão heurística em `graphify-out/.graphify_labels.pending.json` (nome de arquivo ou título); o `.graphify_labels.json` fica vazio e o cofre do Obsidian mostraria "Community N". Para nomes legíveis, sem custo de API:
  1. leia o `.pending.json` e os nós de cada comunidade no `GRAPH_REPORT.md`;
  2. escreva `graphify-out/.graphify_labels.json` com `{"0": "Nome curto", …}` — 2 a 5 palavras, no idioma do projeto, mesmas chaves do `.pending.json`;
  3. `graphify cluster-only . --no-label` aplica os nomes ao grafo, ao relatório e ao cofre (zero tokens).

  **Não use** `graphify extract` sem chave nem `graphify cluster-only` sem `--no-label`: sem chave de API eles chamam o `claude -p` sozinho para nomear comunidades e gastam tokens (~38 mil num repositório de 4 arquivos). Se precisar deles, use `GRAPHIFY_BACKEND=none` / `--no-label`.
- *Completo:* invoque a skill `graphify` com `.` e siga-a (subagentes para os docs, sem chave de API; ela mesma nomeia as comunidades). Depois, os hooks preservam os nós semânticos ao atualizar o código.
- Extensões ambíguas (`.h`, `.inc`, `.m`) → `.graphifyrc` com `language.<ext>=<linguagem>`.

**E2. Integrar o agente, de forma portátil:** `graphify claude install --project` (outros agentes: `references/praticas.md` §9). O `--project` grava o comando `graphify` sem caminho absoluto. Depois arrume as sobras do install:
- apague `.claude/settings.json.graphify-bak`, se existir;
- apague só `.claude/skills/graphify/` (nunca a pasta `.claude/skills/` inteira, que pode ter outras skills; se ela ficar vazia e não existia antes, remova-a);
- apague o `.claude/CLAUDE.md` se foi criado agora; se já existia, remova só o bloco `# graphify` dele. Cada pessoa recebe a skill atualizada via `graphify install`; uma cópia versionada envelheceria a cada upgrade;
- confira a seção `## graphify` adicionada ao `CLAUDE.md`/`AGENTS.md` e que o conteúdo anterior foi preservado. Não traduza nem edite essa seção: ela é gerenciada pelo Graphify (o `uninstall` e upgrades a localizam pelo título).

**E3. Hooks:** `graphify hook install`, depois `graphify hook status` (4 hooks "installed" + merge driver "registered"; cria a linha `graphify-out/graph.json merge=graphify` no `.gitattributes`).

**E4. `.gitignore`:** acrescente o bloco de `references/praticas.md` §4, preservando o final de linha que o arquivo já usa (CRLF ou LF).

**E5. Guia no repositório:** crie `docs/graphify.md` (ou na pasta de documentação que o projeto já usa) a partir de `assets/guia-projeto.md`, seguindo os comentários do modelo. Se o `CLAUDE.md`/README tiver uma lista de pastas ou documentos do projeto, acrescente o guia nela. O guia entra no grafo como estrutura de Markdown, o que é bom: o agente acha as regras.

**E6. Testar** (depois do guia, para ele entrar no grafo):
- `graphify update .` — deve rodar sem erro; se surgirem comunidades novas, nomeie-as como em E1 e rode `graphify cluster-only . --no-label`. O Graphify pode criar `graphify-out/AAAA-MM-DD/` como backup do grafo anterior (já ignorado);
- `graphify query "<pergunta que a pessoa sabe responder sobre o projeto>"` — confira se faz sentido;
- `scripts/verificar_setup.py` de novo. Resultado esperado antes do commit: **0 falhas e 1 aviso** ("ainda não foi commitado"); linhas INFO não contam. Resolva o resto.

**E7. Obsidian (se D4 = sim)**, por último, para o cofre refletir o grafo final: `graphify export obsidian`. Instalado? Windows: `%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe` (não fica no PATH); macOS: `/Applications/Obsidian.app`. Se faltar, peça o "sim" antes de instalar (`winget install --id Obsidian.Obsidian -e` / `brew install --cask obsidian`). Não tente registrar o cofre nem abri-lo por link (`obsidian://`): de dentro de apps isolados não persiste e abre em erro. Oriente: abrir o Obsidian pelo menu Iniciar/Launchpad → **Abrir pasta como um cofre** (Open folder as vault) → `graphify-out/obsidian` → Ctrl+G.

**E8. Projetos relacionados:** se a pessoa mencionar outro repositório que este consome ou serve (app ↔ API), proponha a seção "Projeto relacionado" no `CLAUDE.md` com caminho relativo (`references/praticas.md` §10). Não use `merge-graphs` para app ↔ API.

**E9. Não faça commit sem pedir.** Rode `git status --short --untracked-files=all` e confira se só aparecem arquivos previstos em `graphify-out/` (lista em `references/praticas.md` §4); algo inesperado (novo carimbo, arquivo de máquina) → ignore-o antes. Sugira o `git add` com a lista explícita: `graphify-out/`, `.graphifyignore`, `.graphifyrc`, `.gitattributes`, `.gitignore`, `CLAUDE.md`/`AGENTS.md`, `.claude/settings.json`, o guia.

## 4. Integrar um membro (clone que já usa Graphify)

1. Verificação da máquina (seção 2), respeitando a regra de quem instala.
2. `graphify install`, se a skill do agente não existir.
3. `graphify hook install` e `graphify hook status`.
4. **Não gere o grafo de novo**: ele veio no repositório. Se houver commits de código depois do último que tocou `graphify-out/` (`git log -1 --format=%h -- graphify-out/` vs `git log -1 --format=%h`), `graphify update .` deixa em dia sem tokens. Avise que o primeiro commit da pessoa pode trazer mudanças pequenas em `graphify-out/` (manifesto/cache, por exemplo por diferença de final de linha entre quem gerou e quem clonou): é normal, vai junto.
5. **Teste na IDE da pessoa — sem commit artificial.** Commit vazio ou que só mexe em `graphify-out/` não dispara reconstrução (falso negativo), e commits de teste sujam o histórico. Oriente: o **próximo commit real** dela, feito pela interface Git da IDE (Visual Studio, VS Code, Antigravity, Android Studio, IntelliJ…), deve mostrar no console Git da IDE a linha `[graphify hook] launching background rebuild` e acrescentar uma entrada em `~/.cache/graphify-rebuild.log`. Se não aparecer, a IDE usa um Git embutido ou um `core.hooksPath` próprio:
   - JetBrains (Android Studio, IntelliJ): Settings → Version Control → Git → *Path to Git executable* = o `git` do sistema;
   - VS Code / Antigravity: usam o Git do sistema por padrão (`git.path` nas configurações, se alterado);
   - Visual Studio: usa o Git do Git for Windows, que executa hooks;
   - em qualquer caso, `git config --get core.hooksPath` vazio (o script avisa se não estiver).
   Alternativa sempre válida: commit/pull pelo terminal.
6. **Obsidian, se a pessoa quiser:** `graphify export obsidian` (cofre em `graphify-out/obsidian/`, já ignorado). Se o Obsidian não estiver instalado, peça o "sim" antes de instalar (seção 2). Ela abre pelo menu Iniciar/Launchpad → **Abrir pasta como um cofre** → `graphify-out/obsidian` → Ctrl+G. O cofre não se atualiza sozinho: exportar de novo quando quiser.
7. `scripts/verificar_setup.py` de novo (esperado: 0 falhas, 0 avisos; linhas INFO não contam).
8. **Ensinar** (seção 6).

## 5. Verificação avulsa

Rode o script e traduza o resultado em ações: cada FALHA vira um comando, dizendo onde rodar (terminal comum, se envolver instalação ou hooks); cada AVISO vira uma explicação curta de se vale corrigir.

## 6. Ensinar as práticas

Ao final de uma adoção ou integração, entregue um resumo curto (não um tratado), com o checklist de `references/praticas.md` §13 e estes pontos:

- Os hooks atualizam o grafo de código sozinhos (commit, troca de branch, pull/merge, rebase), sem tokens, depois do evento. Hooks não vão no Git: cada clone instala.
- Na dúvida, `graphify update .` (zero tokens; se nada mudou, nada acontece). Docs alterados no modo completo: `/graphify . --update`.
- Evitar `graphify extract`/`cluster-only` sem chave: gastam tokens via `claude -p`.
- O grafo é um mapa: antes de renomear ou mudar assinatura, confirmar usos com busca; build e testes antes de todo commit (mais ainda em linguagens de script).
- Diff grande no `graph.json` em PR é normal.
- Instalar/atualizar o Graphify sempre num terminal comum (`uv tool upgrade graphifyy`).

Para perguntas além disso, use a seção correspondente de `references/praticas.md`.

## Encerramento

Termine com: o que foi feito, o resultado da verificação, o que a pessoa ainda precisa fazer (comandos em blocos separados, um por bloco), o que não foi commitado, e **todo** gasto de tokens que houve (leitura semântica, nomeação de comunidades, subagentes), mesmo se zero.
