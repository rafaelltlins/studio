# Studio

**Edite seus vídeos conversando com o Claude.** Você grava e corta; o Claude assiste, entende o que você fala e monta a edição: textos animados, prints com zoom e marca-texto, tela dividida, gráficos, legendas e, se quiser, B-rolls gerados por IA.

| | | |
|---|---|---|
| ![](estilos/imagens/MinimalSuico.jpg) | ![](estilos/imagens/papel-creme-aula.jpg) | ![](estilos/imagens/tecnico-neon.jpg) |

O arquivo [CLAUDE.md](CLAUDE.md) transforma o Claude num **diretor de vídeo**: ao abrir o projeto, ele pergunta em qual nível você quer editar, confere o que falta instalar, sugere estilos e conduz cada etapa, parando para você aprovar.

## Dois níveis, com três vertentes no Nível 2

| | **Nível 1: gratuito** | **Nível 2 · Higgsfield** | **Nível 2 · Google (Flow)** | **Nível 2 · Meta AI** |
|---|---|---|---|---|
| Motor | [Remotion](https://www.remotion.dev) (vídeo feito com código) | [Higgsfield](https://higgsfield.ai) (IA generativa + editor Higgsedit) | [Google Flow](https://labs.google/fx/tools/flow) (Veo 3.1, Omni Flash, Nano Banana) + montagem no Remotion | [Meta AI](https://www.meta.ai) (Imagine: imagem e animação) + montagem no Remotion |
| O que faz | textos, prints animados, marca-texto, tela dividida, gráficos, legendas, transições | tudo do Nível 1 + imagens e vídeos gerados por IA: B-roll, metáforas, cenas realistas | tudo do Nível 1 + imagens e vídeos gerados no Flow, em modo manual (ficha de prompts) ou automático (Claude in Chrome) | tudo do Nível 1 + imagens e vídeos gerados no meta.ai, em modo manual ou automático (Claude in Chrome) |
| Custo | zero, roda no seu computador | créditos da sua conta Higgsfield | créditos da assinatura Google AI Pro/Ultra, com prévia de custo antes de gerar | zero por enquanto (conta Meta); sem API oficial, limites podem surgir sem aviso, marca d'água nos arquivos |
| Melhor para | tutoriais, aulas, análises, notícias, Reels | vídeos que pedem imagem de cinema e ilustração | quem já assina o Google AI e quer B-roll sem pagar API | quem quer B-roll gerado sem gastar créditos e aceita os riscos |
| Guia | [guias/2-nivel-1-remotion.md](guias/2-nivel-1-remotion.md) | [guias/4-nivel-2-higgsfield.md](guias/4-nivel-2-higgsfield.md) | [guias/6-nivel-2-google-flow.md](guias/6-nivel-2-google-flow.md) | [guias/8-nivel-2-meta-ai.md](guias/8-nivel-2-meta-ai.md) |

Em todos os níveis, o fluxo é o mesmo:

```text
você grava e corta → salva o vídeo e os prints em projetos/
   → o Claude assiste e transcreve (com o tempo de cada palavra)
   → propõe um plano de edição → você aprova
   → ele produz, mostra quadros de revisão → você aprova
   → o vídeo final sai em edicoes/
```

## Instalar

O jeito mais fácil: abra uma sessão **Code** no Claude e cole:

```text
Instala o repositório https://github.com/mackswendhell/studio na pasta C:\dev (siga a seção "Instalação" do README).
```

O Claude clona o repositório e instala tudo, incluindo as skills gratuitas **remotion-best-practices** e **watch**. No fim, abra uma sessão nova dentro da pasta `studio`.

Pré-requisitos no computador: Node.js, Python 3.10+ e FFmpeg. Se faltar algum, o passo a passo para Windows e Mac está em **[guias/1-primeiros-passos.md](guias/1-primeiros-passos.md)**.

### Instalação (instruções para o agente)

Se você é um agente de IA instalando este repositório, faça exatamente isto:

1. Clone: `git clone https://github.com/mackswendhell/studio.git` na pasta indicada (padrão: `C:\dev` no Windows, `~/dev` no Mac/Linux; evite pastas do OneDrive/iCloud).
2. Entre na pasta e rode **`npm run instalar`**. Ele instala, nesta ordem:
   - dependências do Remotion (`npm install`);
   - transcrição local (`pip install faster-whisper`);
   - skill **remotion-best-practices** no projeto (`npx -y skills add remotion-dev/skills -s remotion-best-practices -a claude-code -y`);
   - skill **watch** (`claude plugin marketplace add bradautomates/claude-video` e `claude plugin install watch@claude-video`).
3. Se o comando `claude` não existir (usuário só com o Claude Desktop), a watch é oferecida automaticamente ao abrir a pasta, porque está declarada em `.claude/settings.json`. Oriente a pessoa a aceitar, ou a instalar em **Personalizar → Plugins → Adicionar marketplace** com `https://github.com/bradautomates/claude-video`.
4. Se `node`, `python` ou `ffmpeg` faltarem, instale-os com o gerenciador do sistema (`winget` no Windows, `brew` no Mac; comandos em [guias/1-primeiros-passos.md](guias/1-primeiros-passos.md)) e rode `npm run instalar` de novo.
5. Termine dizendo à pessoa para **abrir uma sessão nova do Claude dentro da pasta `studio`**. Skills instaladas só aparecem numa sessão nova, e é lá que o diretor de vídeo ([CLAUDE.md](CLAUDE.md)) assume.

Já clonou manualmente? Basta rodar `npm run instalar` dentro da pasta.

## Começo rápido

Depois de instalar:

1. Coloque seu vídeo em `projetos/001. meu-video/video/` e os prints em `projetos/001. meu-video/prints/`.
2. Abra a pasta `studio` no Claude (sessão **Code**).
3. Responda se quer o Nível 1, o Nível 2 · Higgsfield, o Nível 2 · Google (Flow) ou o Nível 2 · Meta AI e diga o que imagina. O diretor cuida do resto.

> **Dica que mais faz diferença:** tire print de tudo o que você cita no vídeo (sites, notícias, telas, gráficos) e salve em `prints/`. Animação feita sobre print real fica muito melhor que recriação.

## Estrutura

```text
studio/
├─ CLAUDE.md      o diretor de vídeo
├─ guias/         os manuais, do zero ao avançado
├─ estilos/       galeria de estilos de referência (horizontais e verticais)
├─ projetos/      ← você coloca o vídeo e os prints aqui
├─ edicoes/       ← o vídeo pronto sai aqui
├─ src/           código do Remotion (exemplos de estilo + seus vídeos)
└─ tools/         transcrição local e gerador da Higgsfield Cloud API
```

A explicação pasta por pasta está nos [primeiros passos](guias/1-primeiros-passos.md#7-entendendo-as-pastas).

## Guias

1. [Primeiros passos](guias/1-primeiros-passos.md): instalação, pastas e primeira edição.
2. [Nível 1: Remotion](guias/2-nivel-1-remotion.md): o processo gratuito, fase por fase.
3. [Manual do Remotion para leigos](guias/3-manual-remotion.md): o que é, como funciona e tudo o que dá para pedir.
4. [Nível 2 · Higgsfield](guias/4-nivel-2-higgsfield.md): como conectar (conta ou API key), processo, modelos, custos e prompts.
5. [Direção editorial](guias/5-direcao-editorial.md): o repertório de cenas, transições e cuidados que guia toda edição.
6. [Nível 2 · Google (Flow)](guias/6-nivel-2-google-flow.md): Flow manual ou automático pelo Claude in Chrome, prévia de custo em créditos, processo e montagem no Remotion.
7. [Grafo de conhecimento (Graphify) e Obsidian](guias/7-graphify-e-obsidian.md): para quem desenvolve o Studio; o Claude consulta um mapa do projeto em vez de varrer arquivos.

E a [galeria de estilos](estilos/README.md) para escolher o visual.

## Créditos e licenças

- Fork de [mackswendhell/studio](https://github.com/mackswendhell/studio), de Macks Wendhell. Este fork acrescenta o Nível 2 · Google (Flow), o Nível 2 · Meta AI, o registro automático dos vídeos (`src/videos/` fora do Git) e o grafo de conhecimento com [Graphify](https://github.com/Graphify-Labs/graphify), mais a skill `/graphify-setup`.
- Código e guias deste repositório: [MIT](LICENSE), © 2026 Macks Wendhell e © 2026 Rafaell Lins. Pode usar, modificar e distribuir, inclusive comercialmente, mantendo o aviso de licença.
- As imagens em `estilos/imagens/` que vêm de vídeos do canal **Macks Wendhell | Inteligência Aplicada** são referência visual; não as reutilize como material próprio.
- [Remotion](https://www.remotion.dev): gratuito para pessoas físicas, organizações sem fins lucrativos e empresas com até 3 pessoas; empresas maiores precisam de [licença](https://www.remotion.dev/license).
- Skill [watch](https://github.com/bradautomates/claude-video), de bradautomates (MIT).
- Skills do Remotion: [remotion-dev/skills](https://github.com/remotion-dev/skills).
- Transcrição: [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
- Higgsfield: serviço de terceiros, sujeito aos termos e preços da [Higgsfield](https://higgsfield.ai).
- Google Flow: serviço do Google, sujeito aos termos e aos créditos do seu plano [Google AI](https://one.google.com/about/google-ai-plans/).
- Meta AI: serviço da Meta, sujeito aos [termos da Meta AI](https://www.meta.ai); os arquivos gerados saem com marca d'água.
- [Graphify](https://github.com/Graphify-Labs/graphify) e [Obsidian](https://obsidian.md): ferramentas de terceiros, com licenças próprias, usadas para o grafo de conhecimento (veja [guias/7-graphify-e-obsidian.md](guias/7-graphify-e-obsidian.md)).
