# Graph Report - VideoStudio  (2026-10-19)

## Corpus Check
- 36 files · ~27,394 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 5)

## Summary
- 329 nodes · 524 edges · 23 communities (20 shown, 3 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `12e2ee1a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Código Remotion e estilos
- Galeria de estilos
- Regras invioláveis e Nível 2
- Dependências npm
- Ferramentas Python
- Práticas do Graphify
- Nível 2 · Google Flow
- Skill graphify-setup
- Primeiros passos
- Modelo de guia do Graphify
- Registro dos vídeos
- Configuração TypeScript
- Nível 1: edição com Remotion
- Nível 2: Higgsfield
- Glossário rápido
- Validação de telas divididas
- Script de instalação
- Diretor de vídeo
- Guia Graphify e Obsidian
- Direção editorial
- 8-nivel-2-meta-ai.md
- Repertório de cenas (camera, aula, demo, cena, broll, transformacao...)

## God Nodes (most connected - your core abstractions)
1. `Nível 1: edição com Remotion` - 31 edges
2. `Nível 2: Higgsfield` - 24 edges
3. `Direção editorial` - 21 edges
4. `Galeria de estilos` - 20 edges
5. `Nível 2 · Google Flow` - 20 edges
6. `Primeiros passos` - 17 edges
7. `Práticas da equipe com Graphify (base de conhecimento)` - 15 edges
8. `Manual do Remotion para leigos` - 14 edges
9. `useEntrada()` - 13 edges
10. `Plano de edição 003. jev-nao-e-hype` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Papel creme em aula` --semantically_similar_to--> `AULA 70/30`  [INFERRED] [semantically similar]
  estilos/README.md → projetos/000. exemplo/plano.md
- `Dica: tirar prints do que é citado` --semantically_similar_to--> `Estrutura de pasta de projeto (video/ + prints/)`  [INFERRED] [semantically similar]
  README.md → projetos/LEIA-ME.md
- `Cardápio de opções de edição` --references--> `Galeria de estilos`  [EXTRACTED]
  CLAUDE.md → estilos/README.md
- `Repertório de cenas (CÂMERA, NOTÍCIA/DEMO, AULA 70/30, CENA, B-ROLL)` --conceptually_related_to--> `Direção editorial`  [INFERRED]
  projetos/000. exemplo/plano.md → guias/5-direcao-editorial.md
- `Pontos de aprovação obrigatórios` --conceptually_related_to--> `Plano de edição 003. jev-nao-e-hype`  [INFERRED]
  CLAUDE.md → projetos/000. exemplo/plano.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Montagem no Remotion (Nível 1, Higgsfield Caminho B, Google Flow)** — guias_2_nivel_1_remotion, guias_4_nivel_2_higgsfield_caminho_b_cloud_api, guias_6_nivel_2_google_flow, guias_3_manual_remotion_remotion [EXTRACTED 1.00]
- **Pipeline assistir → transcrever → planejar** — guias_1_primeiros_passos_skill_watch, tools_transcrever, guias_2_nivel_1_remotion_palavras_json, guias_2_nivel_1_remotion_plano_de_edicao [EXTRACTED 1.00]
- **Geração de B-roll papel recortado na Higgsfield** — projetos_000__exemplo_plano_assets_higgsfield, projetos_000__exemplo_plano_nano_banana_pro, projetos_000__exemplo_plano_kling3_0, projetos_000__exemplo_plano_seedance_2_0, estilos_readme_papel_recortado [EXTRACTED 1.00]
- **Três níveis de edição do Studio** — claude_nivel_1_remotion, claude_nivel_2_higgsfield, claude_nivel_2_google_flow, readme_remotion, readme_higgsfield, readme_google_flow [EXTRACTED 1.00]
- **Pipeline de transcrição por palavra até gatilhos da timeline** — tools_transcrever, readme_faster_whisper, claude_palavras_json, projetos_000__exemplo_plano_timeline [INFERRED 0.85]
- **Geração de assets IA com aprovação prévia de custo** — guias_4_nivel_2_higgsfield_custo_estimado_creditos, guias_6_nivel_2_google_flow_previa_de_custo, guias_2_nivel_1_remotion_plano_de_edicao, guias_4_nivel_2_higgsfield_imagens_antes_de_animar, guias_4_nivel_2_higgsfield_sem_texto_em_assets_gerados [INFERRED 0.85]

## Communities (23 total, 3 thin omitted)

### Community 0 - "Código Remotion e estilos"
Cohesion: 0.10
Nodes (37): npm run typecheck, react, remotion, CameraFalsa(), clamp, suave, useEntrada(), COR (+29 more)

### Community 1 - "Galeria de estilos"
Cohesion: 0.16
Nodes (17): Cinematográfico escuro, Dados leves, Dossiê claro-escuro, Dossiê com marca-texto, Editorial quente, Galeria de estilos, Legenda dinâmica, Lousa a giz (+9 more)

### Community 2 - "Regras invioláveis e Nível 2"
Cohesion: 0.10
Nodes (17): Flow automático (Claude in Chrome), Nível 2 · Higgsfield, Numeração NNN. slug, palavras.json, Papel recortado, Assets a gerar (B-rolls Higgsfield), Curva de energia, Dialeto papel recortado (creme/tinta/terracota) (+9 more)

### Community 3 - "Dependências npm"
Cohesion: 0.07
Nodes (25): dependencies, react, react-dom, remotion, @remotion/cli, @remotion/media, description, devDependencies (+17 more)

### Community 4 - "Ferramentas Python"
Cohesion: 0.13
Nodes (12): add(), check_machine(), check_repo(), is_isolated(), main(), run(), main(), urls() (+4 more)

### Community 5 - "Práticas do Graphify"
Cohesion: 0.12
Nodes (15): 10. Projetos relacionados (app + API), 11. Obsidian, 12. Ambiente: apps isolados no Windows, 13. Checklist individual, 1. O que é e por que economiza, 2. Custos, 3. Riscos de grafo desatualizado, 4. O que versionar (+7 more)

### Community 6 - "Nível 2 · Google Flow"
Cohesion: 0.19
Nodes (12): Plano de edição (plano.md), Remotion, Caminho B: Higgsfield Cloud API (HF_KEY), Imagens primeiro, prancha de conferência, depois animar, Nível 2 · Google Flow, Claude in Chrome, Flow automático (Claude in Chrome), Flow manual (prompts.md) (+4 more)

### Community 7 - "Skill graphify-setup"
Cohesion: 0.18
Nodes (10): 1. Descobrir o modo, 2. Verificar a máquina (todos os modos), 3. Adotar no repositório, 4. Integrar um membro (clone que já usa Graphify), 5. Verificação avulsa, 6. Ensinar as práticas, Decisões (antes de mudar arquivos), Encerramento (+2 more)

### Community 8 - "Primeiros passos"
Cohesion: 0.11
Nodes (22): CLAUDE.md, Primeiros passos, Escolha de nível (1, 2 Higgsfield, 2 Google), Estrutura de pastas do Studio, faster-whisper (transcrição local), Chave gratuita da Groq (GROQ_API_KEY), npm run instalar, Pasta edicoes/ (+14 more)

### Community 9 - "Modelo de guia do Graphify"
Cohesion: 0.25
Nodes (7): Ao clonar (cada pessoa), Atualização, Como está configurado, Consultas úteis, Cuidados, Grafo de conhecimento (Graphify), Obsidian (opcional)

### Community 11 - "Configuração TypeScript"
Cohesion: 0.17
Nodes (11): compilerOptions, esModuleInterop, jsx, lib, module, moduleResolution, noEmit, skipLibCheck (+3 more)

### Community 12 - "Nível 1: edição com Remotion"
Cohesion: 0.18
Nodes (8): Nível 1: edição com Remotion, Validação com ffprobe, Processo Nível 1 (organizar, assistir, planejar, programar, conferir, renderizar), <Sequence premountFor={fps}>, Stills de revisão, Entregável vídeo completo (MP4), Fluxo de edição (gravar → transcrever → plano → revisão → entrega), Studio

### Community 13 - "Nível 2: Higgsfield"
Cohesion: 0.16
Nodes (14): estilos/README.md, palavras.json (tempo por palavra), Nível 2: Higgsfield, Estilo cinematográfico escuro, edit.jsx (roteiro de montagem), Estilos e prompts base (papel recortado, cinematográfico escuro), Higgsedit, Higgsfield (+6 more)

### Community 14 - "Glossário rápido"
Cohesion: 0.22
Nodes (5): Gatilho (palavra falada), Glossário rápido, Master (vídeo gravado e cortado), MCP, Caminho A: conector MCP oficial (mcp.higgsfield.ai)

### Community 15 - "Validação de telas divididas"
Cohesion: 0.29
Nodes (4): allowed, collect(), sourceRoot, violations

### Community 19 - "Diretor de vídeo"
Cohesion: 0.21
Nodes (11): Cardápio de opções de edição, Diretor de vídeo, Flow manual (ficha de prompts), Nível 1: gratuito, com Remotion, Nível 2 · Google (Flow), faster-whisper, Google Flow (Veo 3.1, Omni Flash, Nano Banana), npm run instalar (+3 more)

### Community 20 - "Guia Graphify e Obsidian"
Cohesion: 0.18
Nodes (11): 7. Grafo de conhecimento (Graphify) e Obsidian, Atalho: a skill `/graphify-setup`, Atualizar ou remover, Comandos de consulta, Como está configurado neste projeto, Cuidados, Obsidian, Quando o grafo se atualiza sozinho (+3 more)

### Community 21 - "Direção editorial"
Cohesion: 0.25
Nodes (7): Prints do usuário, Direção editorial, Formatos (16:9, 9:16, quadrado/4:5), Identidade visual (permanente, dialeto, direção da cena), Movimento e transições, Prints e marca-texto semântico, Traduções fala → visual

### Community 23 - "8-nivel-2-meta-ai.md"
Cohesion: 0.15
Nodes (12): 1. Organizar, assistir e transcrever, 1. Os dois modos, 2. Planejar (ponto de aprovação), 2. Prévia de gerações (obrigatória nos dois modos), 3. Gerar os assets, 3. O processo, 4. Checklist, 4. Montar no Remotion (+4 more)

### Community 25 - "Repertório de cenas (camera, aula, demo, cena, broll, transformacao...)"
Cohesion: 0.40
Nodes (4): Cena aula (tela dividida 70/30), Cena broll, Cena demo, Repertório de cenas (camera, aula, demo, cena, broll, transformacao...)

## Knowledge Gaps
- **43 isolated node(s):** `@remotion/media`, `react-dom`, `@types/react`, `@types/react-dom`, `typescript` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 162 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Nível 1: edição com Remotion` connect `Nível 1: edição com Remotion` to `Código Remotion e estilos`, `Galeria de estilos`, `Regras invioláveis e Nível 2`, `Ferramentas Python`, `Nível 2 · Google Flow`, `Primeiros passos`, `Nível 2: Higgsfield`, `Glossário rápido`, `Diretor de vídeo`, `Direção editorial`, `8-nivel-2-meta-ai.md`?**
  _High betweenness centrality (0.311) - this node is a cross-community bridge._
- **What connects `@remotion/media`, `react-dom`, `@types/react` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Código Remotion e estilos` be split into smaller, more focused modules?**
  _Cohesion score 0.10434782608695652 - nodes in this community are weakly interconnected._
- **Why does `Nível 2: Higgsfield` connect `Nível 2: Higgsfield` to `Galeria de estilos`, `Regras invioláveis e Nível 2`, `Ferramentas Python`, `Nível 2 · Google Flow`, `Primeiros passos`, `Nível 1: edição com Remotion`, `Glossário rápido`, `Direção editorial`, `8-nivel-2-meta-ai.md`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Should `Regras invioláveis e Nível 2` be split into smaller, more focused modules?**
  _Cohesion score 0.10144927536231885 - nodes in this community are weakly interconnected._
- **Why does `Plano de edição 003. jev-nao-e-hype` connect `Regras invioláveis e Nível 2` to `Galeria de estilos`, `Nível 1: edição com Remotion`, `Nível 2: Higgsfield`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Should `Dependências npm` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._