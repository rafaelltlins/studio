# Nível 2 · Google: edição avançada com o Flow

Esta é a segunda vertente do Nível 2. Ela tem tudo do [Nível 1](2-nivel-1-remotion.md), mais imagens e vídeos gerados por IA no **[Google Flow](https://labs.google/fx/tools/flow)** (Veo 3.1, Gemini Omni Flash, Nano Banana), usando os **créditos da sua assinatura Google AI** (Pro ou Ultra). Não usa chave de API nem cobrança por uso: o gasto sai dos créditos mensais do seu plano.

A **montagem é sempre no Remotion**, igual ao Nível 1. O Flow só gera os assets: B-rolls, ilustrações, metáforas e cenas de produto.

**Custo:** créditos do Flow. No Google AI Pro, são 1.000 créditos por mês, que não acumulam (≈ US$ 0,02 por crédito, considerando US$ 19,99/mês). Nada é gerado sem você aprovar a **prévia de custo**.
**Quando vale a pena:** vídeos em que imagem gerada faz diferença. Se o vídeo é mais tutorial e print, o Nível 1 resolve sem gastar crédito.

> O Flow **não tem API oficial**. Por isso, esta vertente funciona de dois jeitos: você gera no site seguindo uma ficha pronta (manual) ou o Claude opera o site no seu Chrome, com você acompanhando (automático). O Claude **não** usa conectores não oficiais que pedem a sua sessão do Google.

---

## 1. Os dois modos

Depois que você escolhe o Nível 2 · Google, o Claude pergunta o modo:

| | **Flow manual (recomendado)** | **Flow automático (Claude in Chrome)** |
|---|---|---|
| Quem clica em "gerar" | você, no site do Flow | o Claude, no seu Chrome, enquanto você vê a tela |
| O que o Claude entrega | `flow/prompts.md`: uma ficha por asset, com o prompt pronto, o modelo, a proporção, a duração e o nome do arquivo para salvar | os arquivos já baixados e renomeados em `flow/` |
| Precisa de quê | conta Google com plano AI Pro/Ultra, logada no Flow | o mesmo, mais a extensão **Claude in Chrome** conectada |
| Vantagem | controle total e nada quebra se o site do Flow mudar | rápido e sem trabalho braçal |
| Cuidado | dá trabalho copiar e colar os prompts | mais lento que uma API e pode quebrar se o Google mudar o site |

### Preparar o modo automático

1. Instale a extensão **Claude in Chrome** (Chrome ou outro navegador Chromium) e entre com a mesma conta do Claude.
2. No mesmo navegador, entre na sua conta Google e abra o [Flow](https://labs.google/fx/tools/flow) uma vez, para aceitar os termos.
3. Peça ao Claude: "confere se você enxerga o meu Chrome". Ele lista os navegadores conectados.

Regras do modo automático:

- O Claude **nunca** digita a sua senha nem faz login por você. Se o Flow pedir login, ele para e pede que você entre.
- Ele trabalha numa **aba nova** e não mexe nas suas outras abas.
- **Antes de cada lote** de gerações, ele mostra no chat o que vai gerar e quantos créditos isso custa, e só começa depois do seu "sim". Uma refação fora do plano pede um novo "sim".
- Os downloads também precisam do seu "sim". Os arquivos caem na pasta de Downloads do navegador, e o Claude os move para `projetos/<NNN. nome>/flow/` com nomes descritivos.

---

## 2. Prévia de custo (obrigatória nos dois modos)

O `plano.md` ganha a seção **Assets a gerar (Flow)**, e ela é aprovada junto com o plano. Formato:

| asset | cena | modo do Flow | modelo | chamadas | créd./chamada | total |
|---|---|---|---|---|---|---|
| F1 | B-roll da sala bagunçada | texto → vídeo, 9:16, 8 s | Veo 3.1 Lite | 1 | 10 | 10 |
| F2 | produto girando no fundo neutro | frames → vídeo (imagem inicial) | Veo 3.1 Fast | 1 | 20 | 20 |
| F2-img | imagem inicial do F2 | imagem | Nano Banana Pro | 1 | 0 | 0 |
| **subtotal** | | | | **3** | | **30** |
| margem de refação | ~1 em cada 3 vídeos | | | 1 | 20 | 20 |
| **total estimado** | | | | | | **~50 créditos (5% do plano Pro; ≈ US$ 1,00)** |

Também entram:

- **saldo atual** (no modo automático, o Claude lê no Flow; no manual, pergunta a você) e o saldo depois do gasto;
- **"saídas por comando" = 1**: o Flow pode gerar 2 variações por pedido, e cada variação é cobrada. O padrão aqui é 1. Só use 2 se você pedir;
- a regra dos 20%: se o gasto real passar ~20% do estimado, o Claude para e avisa antes de continuar.

### Tabela de referência (outubro de 2026, plano Pro)

| Uso | Modelo no Flow | Créditos por geração | Observação |
|---|---|---|---|
| B-roll padrão, barato | Veo 3.1 **Lite** | 10 (5 no Ultra) | 8 s, até 1080p, sem referências |
| B-roll com imagem inicial/final ou referências | Veo 3.1 **Fast** | 20 (10 no Ultra) | "frames → vídeo" e "ingredientes → vídeo" |
| Cena "herói" | Veo 3.1 **Quality** | 100 | só para o momento principal do vídeo |
| Gerar e depois **ajustar conversando** | Gemini **Omni Flash** | ~4–15 (varia com a qualidade e a duração) | bom para "a mesma cena, mas mais lenta"; não existe no plano gratuito |
| Ilustração, objeto, imagem inicial | **Nano Banana** Pro / 2 / 2 Lite | 0 | imagens não gastam crédito |

**Os preços mudam.** Antes de fechar a prévia:
- **Modo automático:** o Claude confere o custo que o próprio Flow mostra ao lado do botão de gerar e o saldo da conta.
- **Modo manual:** o Claude avisa que os valores são da tabela e pede que você confirme no Flow o custo do primeiro item.
- Se a tabela estiver desatualizada, o Claude atualiza este guia.

---

## 3. O processo

### 1. Organizar, assistir e transcrever
Igual ao Nível 1: `ffprobe`, quadros com a skill `watch` em `frames/` (sempre com `--engine local`) e tempo por palavra com `tools/transcrever.py`.

### 2. Planejar (ponto de aprovação)
O `plano.md` segue a [direção editorial](5-direcao-editorial.md) e acrescenta a **prévia de custo** da seção 2. Nada é gerado antes da aprovação.

### 3. Gerar os assets

**Comum aos dois modos:**
- **Primeiro as imagens** (Nano Banana, 0 crédito). Elas servem de imagem inicial para os vídeos e garantem o mesmo estilo em todas as cenas. O Claude monta uma prancha de conferência com as imagens antes de animar.
- **Depois os vídeos**, já na proporção do vídeo final (9:16 para Reels/TikTok, 16:9 para YouTube). Nunca recorte um 16:9 para virar vertical.
- **Sem texto dentro das imagens e dos vídeos gerados.** Todo texto entra na montagem.
- Prompts em inglês, que é o idioma com melhor resultado nos modelos do Google. Os prompts base estão na seção 6 do [guia da Higgsfield](4-nivel-2-higgsfield.md#6-estilos-e-prompts-base) e valem aqui também.
- Para produto real (afiliado, review), use os **prints do produto** como imagem inicial ou como ingrediente. Assim o vídeo mostra o produto de verdade, e não um parecido.
- Nomes descritivos em `flow/`: `F1_broll_sala-bagunçada.mp4`, `F2-img_produto.png`.

**Modo manual:** o Claude escreve `flow/prompts.md` com uma ficha por asset:

```markdown
### F2 · produto girando (Veo 3.1 Fast · 20 créditos)
- Modo: Frames → vídeo · imagem inicial: `flow/F2-img_produto.png`
- Proporção: 9:16 · Duração: 8 s · Saídas por comando: 1
- Salvar como: `flow/F2_produto-girando.mp4`
- Prompt:
  > The white metal baby gate slowly rotates on a seamless light grey studio background, ...
```

Você gera, baixa e salva com o nome indicado. Depois avise o Claude. Ele confere cada arquivo (duração, proporção, quadro do meio e do fim) e pede refação só do que não ficou bom.

**Modo automático:** o Claude segue a skill do Claude in Chrome. Ele abre o Flow numa aba nova, cria um projeto com o nome do vídeo, configura modelo, proporção, duração e "saídas = 1", cola o prompt e gera. Depois espera terminar e confere o resultado pelo próprio Flow. Por fim, baixa com o seu "sim" e move para `flow/`. A cada geração, ele anota no `plano.md` os créditos realmente gastos.

**Interface com agente (outubro de 2026).** O projeto do Flow agora abre com um assistente em chat à direita. O modelo, a proporção e o número de saídas ficam em **Configurações do agente** (ícone de ajustes ao lado do campo de texto): escolha, por exemplo, Nano Banana Pro, 1:1, x1, e clique em **Salvar**. Em "Confirmar antes de gerar", mantenha **Sempre**. Um único pedido pode gerar várias imagens separadas ("generate 6 separate images..."). Para baixar, clique com o botão direito na imagem e escolha **Fazer o download → 1K (tamanho original)**; 2K e 4K são versões aprimoradas.

**Figurinhas e ícones transparentes:** o Flow não entrega PNG transparente. Gere com contorno branco sobre fundo cinza liso e recorte localmente com `python tools/recortar_figurinha.py entrada.jpg saida.png`. Ele aproveita o fundo liso e o contorno branco para fazer a borda suave, sem serrilhado e sem comer o contorno. Removedores genéricos como o `rembg` deixaram a borda serrilhada e apagaram parte do contorno em formas com vãos (como três estrelas juntas). Confira as bordas sobre fundo claro e escuro. As figurinhas genéricas vão para a [biblioteca comum](../projetos/_biblioteca/figurinhas/LEIA-ME.md).

### 4. Montar no Remotion
Igual ao Nível 1, usando os arquivos de `flow/` como B-roll e ilustração:
- **Os vídeos gerados entram sempre sem som** (`muted`): o Veo e o Omni geram áudio, e o áudio original do seu vídeo aparece uma única vez;
- o Veo entrega 24 fps e a composição herda o fps do master. O Remotion converte sozinho, mas confira se o movimento ficou suave no still;
- um clipe gerado tem de 4 a 10 s. Se a fala pede mais tempo, use dois clipes ou um zoom lento no último quadro, nunca câmera lenta forçada.

### 5. Conferir, renderizar e entregar
Igual ao Nível 1: stills de revisão para a sua aprovação, render, validação com `ffprobe` e `volumedetect`. No resumo final entram os **créditos gastos** e o saldo restante.

---

## 4. Checklist

- [ ] modo escolhido (manual ou automático) e, no automático, Chrome conectado e Flow logado
- [ ] `palavras.json` gerado e conferido
- [ ] prévia de custo aprovada (modelo, chamadas, créditos, % do plano, saldo)
- [ ] "saídas por comando" = 1
- [ ] imagens aprovadas em prancha antes de animar; vídeos aprovados pelo quadro do meio e do fim
- [ ] nada de texto nos assets gerados; áudio dos clipes gerados mudo
- [ ] gasto real anotado no plano; parou se passou ~20% do estimado
- [ ] render final validado (resolução, fps, duração, volume)
