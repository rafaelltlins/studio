<!--
Modelo da skill graphify-setup. Como preencher:
- Troque cada {{campo}} pelo valor real.
- Linhas que terminam com um comentário "SE <condição>": mantenha a linha (sem o comentário) só se a condição valer; senão apague a linha inteira.
- Apague este bloco de comentário.
-->
# Grafo de conhecimento (Graphify)

Este repositório tem um grafo de conhecimento em `graphify-out/`, gerado pelo [Graphify](https://github.com/Graphify-Labs/graphify). Os agentes de IA consultam o grafo (`graphify query`) em vez de varrer arquivos, o que economiza contexto e tokens.

## Como está configurado

| Item | Valor |
|---|---|
| Modo da primeira geração | {{sem LLM / completo}} |
| Gerado em | {{AAAA-MM-DD}}, Graphify {{versão}} |
| Fora do grafo (`.graphifyignore`) | {{pastas e motivo, ou "nada além do .gitignore"}} |
| Agentes integrados | {{ex.: Claude Code (`CLAUDE.md` + `.claude/settings.json`)}} |
| Versionado | `graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json`, rótulos e `cache/` |
| Ignorado | arquivos desta máquina, derivados locais, `graphify-out/obsidian/` e backups datados do `update` |

## Ao clonar (cada pessoa)

Num terminal comum (não dentro de apps da Microsoft Store, como o app desktop do Claude):

```bash
uv tool install graphifyy     # uma vez por máquina; requer o uv
graphify install              # uma vez por máquina; skill /graphify no Claude Code
graphify hook install         # uma vez por clone
graphify hook status          # 4 hooks "installed" + merge driver "registered"
```

Não gere o grafo de novo: ele vem no repositório.

## Atualização

Os hooks reconstroem a parte de código sozinhos, sem tokens, depois de commit, troca de branch, pull/merge e rebase. À mão:

- `graphify update .` → código alterado e ainda não commitado, ou na dúvida (zero tokens).
- `/graphify . --update` no agente → documentos alterados. <!-- SE modo completo -->
- Evite `graphify extract` e `graphify cluster-only` sem chave de API: eles chamam o `claude -p` e gastam tokens.

## Consultas úteis

```bash
graphify query "<pergunta>"
graphify path "<A>" "<B>"
graphify explain "<conceito>"
graphify affected "<símbolo>"
```

## Obsidian (opcional)

`graphify export obsidian`, depois, no Obsidian: **Abrir pasta como um cofre** → `graphify-out/obsidian` → Ctrl+G. O cofre é gerado: não escreva notas nele.

## Cuidados

- O grafo é um mapa: antes de renomear ou mudar uma assinatura, confirme os usos com busca no código. Build e testes antes de todo commit.
- Diff grande no `graph.json` em PR é normal.
- Projeto relacionado: {{nome}} em `{{caminho relativo}}`; consulte com `graphify query "..." --graph "{{caminho relativo}}/graphify-out/graph.json"`. <!-- SE houver projeto relacionado -->
