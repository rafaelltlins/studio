# 7. Grafo de conhecimento (Graphify) e Obsidian

Guia para quem desenvolve o Studio. Para editar vídeos você não precisa de nada disto.

O [Graphify](https://github.com/Graphify-Labs/graphify) transforma o repositório num grafo de conhecimento em `graphify-out/`. Em vez de varrer arquivos com busca, o Claude consulta o grafo (`graphify query`) e lê só os trechos que importam. Isso economiza contexto e tokens. O [Obsidian](https://obsidian.md) serve para você navegar nesse grafo.

## Como está configurado neste projeto

| Item | Onde | Versionado? |
|---|---|---|
| Grafo, relatório e visualização | `graphify-out/graph.json`, `GRAPH_REPORT.md`, `graph.html` | Sim |
| Manifesto e cache | `graphify-out/manifest.json`, `graphify-out/cache/ast/`, `graphify-out/cache/semantic/` | Sim, para ninguém pagar de novo a leitura dos `.md` pelo LLM |
| Nomes das comunidades | `graphify-out/.graphify_labels.json` | Sim |
| Arquivos da sua máquina | `cost.json`, `.graphify_python`, `.graphify_root`, `.graphify_analysis.json`, `cache/stat-index.json`, `cache/last_query_stamp` | Não (`.gitignore`) |
| Cópias de segurança do `update` | `graphify-out/AAAA-MM-DD/` | Não (`.gitignore`) |
| Vault do Obsidian | `graphify-out/obsidian/` | Não. É gerado sob demanda |
| O que fica fora do grafo | `.graphifyignore` (hoje: `estilos/imagens/`) | Sim |
| Instruções para o Claude | seção `## graphify` no `CLAUDE.md` + hooks `PreToolUse` em `.claude/settings.json` | Sim |
| Hooks do Git | `.git/hooks/post-*` | **Não. Cada pessoa instala no próprio clone** |

O grafo foi gerado no modo completo: o código foi lido localmente e os `.md` (guias, README, CLAUDE.md, estilos) passaram pelo LLM. As miniaturas de `estilos/imagens/` ficaram de fora, porque o `estilos/README.md` já as descreve.

## Atalho: a skill `/graphify-setup`

O projeto traz a skill `.claude/skills/graphify-setup/`. No Claude Code, aberto nesta pasta, digite `/graphify-setup` (ou "configura o graphify pra mim"). Ela confere a sua máquina, instala os hooks no seu clone, testa e explica as práticas abaixo. Se você tiver uma cópia dessa skill no seu perfil (`~/.claude/skills/`), é a do perfil que roda.

## Setup na sua máquina (uma vez)

Rode num **terminal comum** (PowerShell ou Windows Terminal), não num terminal embutido em app empacotado. Veja o aviso no fim.

```powershell
winget install --id astral-sh.uv -e   # se ainda não tiver o uv
uv tool install graphifyy              # dois "y"; instala o comando graphify
graphify install                       # registra a skill /graphify no seu Claude Code
```

## Setup neste clone (uma vez por clone)

```powershell
cd <pasta do VideoStudio>
graphify hook install    # liga a atualização automática do grafo
graphify hook status     # tem que mostrar os 4 hooks "installed" e o merge driver "registered"
```

Não rode `/graphify .` para gerar do zero: o grafo já vem no repositório.

## Quando o grafo se atualiza sozinho

Os hooks reconstroem só a parte de **código**, em segundo plano, com zero tokens:

| Você faz | Hook | Atualiza? |
|---|---|---|
| `git commit` | `post-commit` | Sim, depois do commit. O grafo atualizado entra no **próximo** commit |
| troca de branch | `post-checkout` | Sim |
| `git pull` / `git merge` sem conflito | `post-merge` | Sim |
| `git pull --rebase` / rebase | `post-rewrite` | Sim |
| merge com conflito | `post-commit` ao concluir | Sim, quando você commita a resolução |

O log fica em `~/.cache/graphify-rebuild.log`.

## Quando rodar algo à mão

| Situação | Comando | Custo |
|---|---|---|
| Mudou código e ainda não commitou, e quer o grafo em dia | `graphify update .` | Zero tokens |
| Na dúvida se o grafo está atual (pode rodar sem medo: se nada mudou, nada acontece) | `graphify update .` | Zero tokens |
| Mudou guias, README ou CLAUDE.md | no Claude Code: `/graphify . --update` | Tokens só dos `.md` alterados |
| Apagou ou moveu muito código e o update recusou "encolher" o grafo | `graphify update . --force` | Zero tokens |

Evite `graphify extract` e `graphify cluster-only` sem chave de API: eles chamam o `claude -p` sozinhos para nomear comunidades e gastam tokens.

## Comandos de consulta

```powershell
graphify query "como a transcrição alimenta as animações"   # subgrafo para uma pergunta
graphify path "transcrever.py" "Root.tsx"                    # caminho entre dois pontos
graphify explain "synchronized-split"                        # um conceito e seus vizinhos
graphify affected "alphaMetadata"                            # o que é impactado se X mudar
graphify god-nodes                                           # os pontos mais conectados
```

O Claude Code já usa esses comandos sozinho, por causa da seção `## graphify` do `CLAUDE.md`.

## Obsidian

O Obsidian (já instalado) abre o grafo como um vault de notas ligadas:

1. Gere ou atualize o vault: `graphify export obsidian`. Os hooks **não** fazem isso; rode quando quiser navegar.
2. No Obsidian: **Open folder as vault**, e escolha `graphify-out/obsidian`.
3. Use o **Graph view** e abra o `graph.canvas`.

O vault é gerado: tudo nele é sobrescrito na próxima exportação. **Não escreva notas suas ali.** Anotações que devem virar contexto para o Claude (decisões, por quês) vão em arquivos `.md` versionados do projeto, como os guias. Depois rode `/graphify . --update` para que entrem no grafo.

## Cuidados

- **O grafo é um mapa, não o código.** Antes de renomear ou mudar uma assinatura, peça ao Claude para confirmar os usos com busca no código. Rode sempre `npm run typecheck` antes de commitar.
- **Diff grande no `graph.json` é normal.** O arquivo é reescrito inteiro a cada build.
- **Aviso sobre apps empacotados no Windows.** Apps instalados pela Microsoft Store (como o app do Claude) gravam o que fica em `AppData` numa pasta privada do app. Um `uv tool install` rodado de dentro deles fica invisível para o seu terminal e para a sua IDE. Instale e atualize o Graphify sempre num terminal comum.

## Atualizar ou remover

```powershell
uv tool upgrade graphifyy           # nova versão (a skill do Claude se atualiza no próximo comando graphify)
graphify uninstall                  # remove integrações (adicione --purge para apagar graphify-out/)
```
