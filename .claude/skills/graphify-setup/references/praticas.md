# Práticas da equipe com Graphify (base de conhecimento)

Leia este arquivo quando precisar explicar algo a quem está adotando ou entrando num repositório, ou quando surgir uma dúvida que o SKILL.md não responde. Explique em linguagem simples, no idioma da pessoa, só a parte que interessa à pergunta.

## Sumário
1. O que é e por que economiza
2. Custos: o que gasta tokens e o que não gasta
3. Riscos de grafo desatualizado
4. O que versionar e por quê
5. Cache e manifesto
6. Hooks do Git: o que dispara o quê
7. Quando atualizar à mão
8. Só código vs completo
9. IDEs e agentes
10. Projetos relacionados (app + API)
11. Obsidian
12. Ambiente: apps isolados no Windows
13. Checklist individual

## 1. O que é e por que economiza
- O Graphify transforma o repositório num grafo de conhecimento em `graphify-out/` (nós = arquivos, classes, funções, conceitos; ligações = imports, chamadas, referências).
- O agente consulta o grafo (`graphify query/path/explain/affected`) e recebe um subgrafo pequeno, em vez de ler dezenas de arquivos. Menos contexto = menos tokens e respostas mais rápidas.
- O grafo é um **mapa, não uma cópia do código**. O agente ainda lê o arquivo real antes de editar (no Claude Code, editar exige ler).
- Ferramenta instalada **uma vez por máquina**; **um grafo por repositório**. Não existe um "projeto Graphify" separado para manter.

## 2. Custos
| Ação | Tokens |
|---|---|
| Ler/atualizar código (tree-sitter, ~40 linguagens: C#, Kotlin, Java, TS/JS, Python, Go…) | Zero, sempre |
| Títulos/estrutura de `.md` num `graphify update` | Zero |
| `graphify update .` como primeira geração (nomes de comunidade heurísticos) | Zero |
| Leitura semântica de docs, PDFs, imagens (modo completo) | Uma vez por arquivo, e de novo só quando o conteúdo muda |
| `graphify extract` ou `graphify cluster-only` **sem chave de API** | Chamam `claude -p` sozinhos para nomear comunidades: ~38 mil tokens num repositório de 4 arquivos. Evitar, ou usar `GRAPHIFY_BACKEND=none` / `--no-label` |
| Consultar o grafo | Pequeno; é a troca que economiza |

Pior caso realista: custo de hoje + algumas consultas que não ajudaram. Gastar muito mais só acontece reprocessando documentos sem necessidade.

Referência real: 11 arquivos Markdown (~22 mil palavras) custaram ~200 mil tokens de subagentes na primeira leitura semântica. Imagens custam uma chamada de visão cada.

## 3. Riscos de grafo desatualizado
- **Benigno:** o grafo aponta algo que não existe mais → o agente abre o arquivo, não acha e volta à busca tradicional (custo igual ao de não ter Graphify).
- **Perigoso:** o grafo **omite** um chamador novo → análise de impacto incompleta feita com confiança. Mitigações: hooks instalados; antes de renomear/mudar assinatura, pedir ao agente que confirme usos com busca no código; build e testes antes de todo commit.
- Linguagens tipadas (C#, Kotlin, Java, TS estrito): o build pega a maioria das quebras. Linguagens de script (JS, Python, PHP): os testes são a única rede.
- Mudanças não commitadas não estão no grafo; em geral são as que o próprio agente acabou de fazer. `graphify update .` resolve, sem custo.
- Ligações `INFERRED` podem mudar entre reconstruções; `EXTRACTED` são determinísticas.

## 4. O que versionar
Versionar (é o que deve aparecer em `graphify-out/` num `git status`): `graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json`, `.graphify_labels.json` (+ `.sig`/`.pending.json` se existirem), `cache/ast/`, `cache/semantic/`. Fora da pasta: `.graphifyignore`, `.graphifyrc`, `.gitattributes` (linha do merge driver).

Ignorar (bloco padrão do `.gitignore`):
```gitignore
# Graphify: arquivos desta máquina, derivados locais, cofre gerado e backups do update
graphify-out/cost.json
graphify-out/.graphify_python
graphify-out/.graphify_root
graphify-out/.graphify_analysis.json
graphify-out/cache/stat-index.json
graphify-out/cache/last_query_stamp
graphify-out/obsidian/
graphify-out/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/
```
Por quê: com o grafo e o cache versionados, quem clona recebe tudo pronto e ninguém paga de novo a leitura dos documentos. `.graphify_python`/`.graphify_root` têm caminhos absolutos da máquina; `last_query_stamp` é um carimbo de hora local; `.graphify_analysis.json` é um derivado que o `update` não regenera (ficaria defasado). `graphify update`/`cluster-only` podem criar pastas datadas (`graphify-out/AAAA-MM-DD/`) com backup do grafo anterior, quando há nomes de comunidade curados.

Diff grande no `graph.json` em PR é normal (reescrito inteiro a cada build). Conflitos nele são resolvidos pelo merge driver (união) e o hook `post-merge` reconstrói em seguida.

## 5. Cache e manifesto
1. No `update`, data de modificação igual → inalterado, sem ler.
2. Data diferente (todo clone/checkout muda datas) → compara hash do conteúdo; bateu → nada é reprocessado.
3. Hash diferente → reprocessa só aquele arquivo. Em `.md`, mudar só o cabeçalho YAML não conta.
4. O cache semântico tem chave SHA-256 de conteúdo + caminho relativo (portável entre máquinas) e é separado pela versão do prompt de extração: upgrade que muda o prompt invalida o cache antigo.

## 6. Hooks do Git
| Evento | Hook | Observação |
|---|---|---|
| `git commit` | post-commit | roda **depois** do commit, em segundo plano; o grafo atualizado entra no commit seguinte |
| troca de branch | post-checkout | |
| `git pull`/`git merge` (inclui fast-forward) | post-merge | |
| `git pull --rebase`, rebase, cherry-pick | post-rewrite | |
| merge com conflito | post-commit | quando a resolução é commitada |

- Ficam em `.git/hooks/`: **não são versionados**; cada pessoa instala em cada clone (`graphify hook install`).
- Reconstroem só código, sem tokens. Log: `~/.cache/graphify-rebuild.log`.
- Commits que só tocam `graphify-out/` não disparam reconstrução (sem laço).
- Não há aviso de grafo defasado; o hook só imprime uma linha `[graphify] ... launching background rebuild`.
- A documentação oficial (README, team workflows) ainda diz para rodar `graphify update .` após `git pull`; isso ficou desatualizado na v0.9.92, que instala post-merge e post-rewrite.
- `GRAPHIFY_SKIP_HOOK=1` desliga os hooks pontualmente.

## 7. Quando atualizar à mão
| Situação | Comando | Custo |
|---|---|---|
| Código mudou e não foi commitado | `graphify update .` | zero |
| Dúvida se está atual (se nada mudou, nada acontece) | `graphify update .` | zero |
| Docs mudaram (modo completo) | `/graphify . --update` no agente | só docs alterados |
| Muito código apagado e o update recusa "encolher" | `graphify update . --force` | zero |
| Atualização contínua enquanto edita | `graphify watch .` | zero |

## 8. Só código vs completo
| | Sem LLM | Completo |
|---|---|---|
| Comando | `graphify update .` (serve como primeira geração) | `/graphify .` dentro do agente |
| Entra | código, configs e estrutura dos Markdown (títulos, links) | + leitura semântica de Markdown, PDFs, imagens |
| Tokens | zero | leitura dos docs uma vez |
| Docs | o agente lê o conteúdo direto quando precisar | conceitos, regras e decisões viram nós ligados ao código |

No modo sem LLM, os nomes de comunidade saem heurísticos em `.graphify_labels.pending.json`; o agente da sessão escreve nomes legíveis em `.graphify_labels.json` e aplica com `graphify cluster-only . --no-label` (zero tokens de API).

Recomendação: sem LLM em repositórios grandes ou no piloto; completo onde a documentação é rica e estável (ADRs, specs, guias). Excluir imagens que já têm descrição em texto (`.graphifyignore`). Evitar `graphify extract . --code-only`: apesar do nome, ele manda rodar `cluster-only`, que sem chave chama `claude -p` e gasta tokens; e o primeiro `update` dos hooks incluiria os Markdown de qualquer jeito. Dentro do agente não há chave de API; em CI, `graphify extract . --backend <provedor>` exige a chave do provedor.

## 9. IDEs e agentes
| Agente/IDE | Comando |
|---|---|
| Claude Code (terminal, VS Code, JetBrains, desktop) | `graphify claude install --project` |
| VS Code + Copilot Chat | `graphify vscode install` |
| Google Antigravity | `graphify antigravity install` |
| Cursor | `graphify cursor install` |
| Codex | `graphify codex install` |
| Gemini CLI | `graphify gemini install` |
| Visual Studio, Android Studio, IntelliJ | sem integração própria; vale a do agente usado nelas |

Um caminho principal por agente (não carregar dois blocos de instrução fixos). No Claude Code, os hooks PreToolUse só lembram de consultar o grafo; `--strict` bloqueia a primeira leitura até uma consulta.

Teste dos hooks na IDE: no próximo commit real feito pela interface Git da IDE (com mudança fora de `graphify-out/`; commit vazio não dispara), o console Git da IDE mostra `[graphify hook] launching background rebuild` e `~/.cache/graphify-rebuild.log` ganha uma entrada. Sem isso: a IDE usa um Git embutido ou há `core.hooksPath` definido. JetBrains (Android Studio, IntelliJ): Settings → Version Control → Git → Path to Git executable = Git do sistema. Alternativa: commitar/puxar pelo terminal.

Final de linha: arquivos gerados com LF e convertidos para CRLF no checkout (ou vice-versa) mudam o hash do conteúdo. O primeiro commit de quem clonou pode trazer pequenas mudanças em `manifest.json`/`cache/`; é normal. No modo completo, se documentos forem relidos pelo LLM entre máquinas sem terem mudado, padronize o final de linha dos `.md` no `.gitattributes` (ex.: `*.md text eol=lf`).

## 10. Projetos relacionados (app + API)
- Um grafo por repositório. No `CLAUDE.md`/`AGENTS.md` de cada lado, apontar o grafo do outro:
  ```markdown
  ## Projeto relacionado
  A API consumida por este app fica em ../minha-api.
  Para perguntas sobre ela: graphify query "<pergunta>" --graph "../minha-api/graphify-out/graph.json"
  ```
- `merge-graphs` só liga repositórios por chamadas a classes da **mesma linguagem**; app e API conversam por HTTP → duas ilhas. A ponte real é o contrato (OpenAPI/cliente gerado versionado do lado do app).
- A direção mais valiosa é API → consumidores ("se eu mudar este endpoint, quem quebra?").
- Visão agregada pessoal: `graphify global add graphify-out/graph.json --as <nome>` (fica em `~/.graphify/`, fora dos repositórios).

## 11. Obsidian
- Opcional; serve para pessoas navegarem. A economia de tokens vem só do Graphify.
- `graphify export obsidian` → vault em `graphify-out/obsidian/` (uma nota por nó + `graph.canvas`). No Obsidian: "Abrir pasta como um cofre" (Open folder as vault) → Ctrl+G para o grafo.
- O vault é gerado, não versionado e não é atualizado pelos hooks: exportar de novo quando quiser.
- Não escrever notas dentro do vault (são sobrescritas). Decisões e "por quês" vão em `.md` versionados (ADRs, docs) e entram no grafo com `/graphify . --update`. Comentários `# WHY:` / `# NOTE:` no código também viram nós.

## 12. Ambiente: apps isolados no Windows
Apps empacotados (Microsoft Store/MSIX, como o app desktop do Claude, identificável por `CLAUDE_CODE_ENTRYPOINT=claude-desktop`) gravam o que vai para `AppData` numa pasta privada (`AppData\Local\Packages\<app>\LocalCache\...`). Um `uv tool install` rodado de dentro deles fica invisível para o terminal e para as IDEs, e os hooks apontam para lá. Instalar e atualizar o Graphify sempre num terminal comum; depois, `graphify hook install` em cada clone. O `scripts/verificar_setup.py` detecta isso.

Da mesma forma, um Obsidian aberto de dentro desses apps grava sua lista de cofres na pasta privada: a pessoa deve abrir o Obsidian pelo menu Iniciar e escolher o cofre ela mesma.

## 13. Checklist individual
- [ ] uv e Graphify instalados num terminal comum; `graphify --version` responde
- [ ] `graphify install` (ou `--platform <agente>`) feito
- [ ] `graphify hook install` em cada clone; `graphify hook status` tudo instalado
- [ ] commit de teste pela IDE registrou no log de reconstrução
- [ ] build e testes antes de todo commit, com ou sem IA
- [ ] antes de renomear/mudar assinatura, confirmar usos com busca no código
- [ ] docs importantes mudaram (modo completo): `/graphify . --update`
