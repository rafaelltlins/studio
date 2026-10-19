# Nível 2 · Meta AI: edição avançada com o meta.ai

Esta é a terceira vertente do Nível 2. Ela tem tudo do [Nível 1](2-nivel-1-remotion.md), mais imagens e vídeos gerados por IA no **[Meta AI](https://www.meta.ai)** (Imagine: imagem a partir de texto, e animação de imagem em vídeo curto), usando a sua **conta Meta** (Facebook ou Instagram). Hoje não há créditos nem cobrança: a Meta não publica limites fixos de uso.

A **montagem é sempre no Remotion**, igual ao Nível 1 e ao Nível 2 · Google. O Meta AI só gera os assets: B-rolls, ilustrações, metáforas e cenas de produto.

**Custo:** zero em dinheiro, por enquanto. A Meta pode passar a limitar ou cobrar a qualquer momento, sem aviso.
**Quando vale a pena:** quando você quer B-roll gerado sem gastar créditos da Higgsfield ou do Flow e aceita um resultado mais simples e menos controlável.

> **Riscos que você aceitou ao escolher esta vertente:**
> - O Meta AI **não tem API oficial** para gerar imagem e vídeo. No modo automático, o Claude opera o site no seu navegador, com a extensão Claude in Chrome, logado na sua conta Meta. Automação de site pode contrariar os termos de uso e, no pior caso, levar a bloqueio da conta. Use uma conta que você aceite arriscar.
> - Os limites mudam sem aviso. Um vídeo pode parar no meio da geração dos assets; o plano sempre tem um caminho B (Nível 1 ou outra vertente) para cada cena.
> - Os arquivos baixados saem com a marca d'água **"Imagined with Meta AI"** (canto inferior esquerdo). O Claude **não remove nem esconde** a marca d'água: ela fica visível na montagem.
> - Antes de usar em vídeo comercial (publi, afiliado), confira os termos de uso da Meta para conteúdo gerado.

---

## 1. Os dois modos

Depois que você escolhe o Nível 2 · Meta AI, o Claude pergunta o modo:

| | **Meta AI manual (recomendado)** | **Meta AI automático (Claude in Chrome)** |
|---|---|---|
| Quem clica em "gerar" | você, no meta.ai | o Claude, no seu navegador, enquanto você vê a tela |
| O que o Claude entrega | `meta/prompts.md`: uma ficha por asset, com o prompt pronto, a proporção e o nome do arquivo para salvar | os arquivos já baixados e renomeados em `meta/` |
| Precisa de quê | conta Meta logada no meta.ai | o mesmo, mais a extensão **Claude in Chrome** conectada |
| Vantagem | nada quebra se o site mudar e o risco para a conta é menor | rápido e sem trabalho braçal |
| Cuidado | dá trabalho copiar e colar os prompts | mais lento que uma API, pode quebrar se a Meta mudar o site e é o modo com mais risco para a conta |

### Preparar o modo automático

1. Instale a extensão **Claude in Chrome** (Chrome ou outro navegador Chromium) e entre com a mesma conta do Claude.
2. No mesmo navegador, entre na sua conta Meta e abra o [meta.ai](https://www.meta.ai) uma vez, para aceitar os termos e ver onde fica o Imagine.
3. Peça ao Claude: "confere se você enxerga o meu Chrome". Ele lista os navegadores conectados.

Regras do modo automático:

- O Claude **nunca** digita a sua senha nem faz login por você. Se o meta.ai pedir login ou verificação (inclusive CAPTCHA), ele para e pede que você resolva.
- Ele trabalha numa **aba nova** e não mexe nas suas outras abas, conversas ou perfis.
- Ele **não publica nada**: nada vai para o feed, Stories, Vibes ou qualquer lugar público. Se o site oferecer "compartilhar" ou "publicar", ele não clica.
- **Antes de cada lote** de gerações, ele mostra no chat o que vai gerar e quantas gerações isso dá, e só começa depois do seu "sim". Uma refação fora do plano pede um novo "sim".
- Os downloads também precisam do seu "sim". Os arquivos caem na pasta de Downloads do navegador, e o Claude os move para `projetos/<NNN. nome>/meta/` com nomes descritivos.
- Ritmo humano: uma geração por vez, sem disparar dezenas de pedidos seguidos. Se o site mostrar aviso de limite, ele para e avisa.

---

## O que se aprendeu no 1º teste (projeto 001, outubro de 2026)

- **Figurinhas transparentes saem prontas.** Pedindo "glossy 3D icon sticker ..., thick white die-cut outline, transparent background, 1:1, no text", o Meta AI gera sobre magenta e entrega um **PNG 1600×1600 com transparência real**. Basta limpar um eventual resto de magenta nas bordas. Ótimo para destaques em overlay (ícones, selos, objetos) animados no Remotion. As genéricas vão para a [biblioteca comum](../projetos/_biblioteca/figurinhas/LEIA-ME.md), para servir a qualquer vídeo; veja lá primeiro se a figurinha já existe. O `rembg` (`pip install rembg pillow`) fica só como reserva para imagens que vierem com fundo.
- **Vídeo depende da conta.** Na conta testada, o site respondeu "Video generation isn't available to you", tanto pelo chat quanto pela Mídia e pelo Vibes. Antes de planejar vídeos, peça um teste rápido; se não houver, use o plano B (imagem com zoom lento e deriva de câmera no Remotion).
- **Comparação A/B.** Às vezes o site mostra duas respostas ("Qual resposta você prefere?"); as duas contam como geração. Escolha uma antes de seguir.
- **Moderação.** Cenas de criança perto de algo perigoso podem ser recusadas no pedido de vídeo; a imagem passou.
- **Download:** o botão "Baixar" fica na resposta (ou em Mídia → abrir a imagem). Os arquivos chegam com nomes em inglês (`orange_cart_cutout.png`); o Claude renomeia ao mover para `meta/`.
- **Mídia** (`meta.ai/create`) é o melhor ponto de partida: abre a conversa de criação e guarda tudo em "Criações".

---

## 2. Prévia de gerações (obrigatória nos dois modos)

Como não há créditos, a prévia conta **gerações** em vez de custo. O `plano.md` ganha a seção **Assets a gerar (Meta AI)**, aprovada junto com o plano:

| asset | cena | modo | proporção | gerações | plano B se falhar |
|---|---|---|---|---|---|
| M1-img | sala bagunçada | texto → imagem | 9:16 | 1 | print do produto com zoom (Nível 1) |
| M1 | B-roll da sala bagunçada | animar M1-img | 9:16 | 1 | M1-img com zoom lento |
| M2-img | produto em fundo neutro | texto → imagem | 9:16 | 1 | foto do produto em `prints/` |
| **total** | | | | **3** | |
| margem de refação | ~1 em cada 2 | | | 2 | |

Também entram:

- o lembrete de que **não há saldo para mostrar** e que os limites podem aparecer no meio do caminho;
- o **plano B** de cada cena, para que o vídeo fique pronto mesmo se o Meta AI travar;
- a regra dos 20%: se o número real de gerações passar ~20% do estimado, o Claude para e avisa antes de continuar.

---

## 3. O processo

### 1. Organizar, assistir e transcrever
Igual ao Nível 1: `ffprobe`, quadros com a skill `watch` em `frames/` (sempre com `--engine local`) e tempo por palavra com `tools/transcrever.py`.

### 2. Planejar (ponto de aprovação)
O `plano.md` segue a [direção editorial](5-direcao-editorial.md) e acrescenta a **prévia de gerações** da seção 2. Nada é gerado antes da aprovação.

### 3. Gerar os assets

**Comum aos dois modos:**
- **Primeiro as imagens.** Elas servem de base para os vídeos (animar imagem) e garantem o mesmo estilo em todas as cenas. O Claude monta uma prancha de conferência com as imagens antes de animar.
- **Depois os vídeos**, animando as imagens aprovadas. O Meta AI dá pouco controle sobre câmera, duração e proporção: o Claude confere a proporção de cada arquivo e, se vier diferente do vídeo final, encaixa numa janela da montagem em vez de recortar.
- **Sem texto dentro das imagens e dos vídeos gerados.** Todo texto entra na montagem.
- Prompts em inglês. Os prompts base estão na seção 6 do [guia da Higgsfield](4-nivel-2-higgsfield.md#6-estilos-e-prompts-base) e valem aqui também.
- **Produto real** (afiliado, review): o Meta AI inventa um produto parecido, não o seu. Para mostrar o produto de verdade, prefira o print ou o próprio vídeo (Nível 1) e use a IA para cenário e metáfora.
- Nomes descritivos em `meta/`: `M1_broll_sala-bagunçada.mp4`, `M1-img_sala-bagunçada.jpg`.

**Modo manual:** o Claude escreve `meta/prompts.md` com uma ficha por asset:

```markdown
### M1 · sala bagunçada (animar imagem)
- Base: `meta/M1-img_sala-bagunçada.jpg` (gere antes com o prompt da M1-img)
- Proporção: 9:16
- Salvar como: `meta/M1_broll_sala-bagunçada.mp4`
- Prompt:
  > Slow handheld push-in through a messy living room with toys on the floor, soft morning light, ...
```

Você gera, baixa e salva com o nome indicado. Depois avise o Claude. Ele confere cada arquivo (duração, proporção, quadro do meio e do fim) e pede refação só do que não ficou bom.

**Modo automático:** o Claude segue a skill do Claude in Chrome. Ele abre o meta.ai numa aba nova, pede a imagem com o prompt da ficha, espera, confere o resultado na tela e, quando a imagem é aprovada, pede a animação. Por fim, baixa com o seu "sim" e move para `meta/`. A cada geração, ele anota no `plano.md` quantas gerações realmente usou. Na primeira vez, ele descreve no chat onde ficam os controles do site (proporção, animar, baixar) e atualiza este guia se algo mudou.

### 4. Montar no Remotion
Igual ao Nível 1, usando os arquivos de `meta/` como B-roll e ilustração:
- **Os vídeos gerados entram sempre sem som** (`muted`): o áudio original do seu vídeo aparece uma única vez;
- a marca d'água do Meta AI fica visível: posicione o clipe de modo que ela não fique em cima do rosto nem das legendas, mas sem cortá-la;
- confira o fps do clipe com `ffprobe`; a composição herda o fps do master e o Remotion converte sozinho, mas confira se o movimento ficou suave no still;
- clipe curto demais para a fala: use dois clipes ou um zoom lento no último quadro, nunca câmera lenta forçada.

### 5. Conferir, renderizar e entregar
Igual ao Nível 1: stills de revisão para a sua aprovação, render, validação com `ffprobe` e `volumedetect`. No resumo final entra o **número de gerações usadas** e qualquer aviso de limite que o site tenha mostrado.

---

## 4. Checklist

- [ ] riscos da vertente lembrados (sem API oficial, limites sem aviso, marca d'água, termos)
- [ ] modo escolhido (manual ou automático) e, no automático, Chrome conectado e meta.ai logado
- [ ] `palavras.json` gerado e conferido
- [ ] prévia de gerações aprovada, com plano B por cena
- [ ] imagens aprovadas em prancha antes de animar; vídeos aprovados pelo quadro do meio e do fim
- [ ] nada de texto nos assets gerados; áudio dos clipes gerados mudo; marca d'água mantida
- [ ] nada publicado no Meta AI; gerações reais anotadas no plano; parou se passou ~20% do estimado
- [ ] render final validado (resolução, fps, duração, volume)
