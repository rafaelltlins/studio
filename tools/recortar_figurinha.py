"""Recorta figurinhas (contorno branco de adesivo sobre fundo liso) para PNG transparente, com borda suave.

Uso:
    python tools/recortar_figurinha.py entrada.jpg saida.png [lado=1024]

Feito para as figurinhas geradas no Flow (ou em outra IA) com o prompt da biblioteca:
contorno branco grosso, fundo liso (cinza, por exemplo). Funciona melhor que um removedor genérico
(como o rembg) nesse caso porque aproveita duas certezas: o fundo é liso e a borda externa é branca.

1. Estima a cor do fundo pela moldura da imagem.
2. Marca como fundo as regiões neutras (cinza do fundo e as sombras dele) que tocam a moldura
   ou que são buracos grandes dentro da figura (o miolo de uma argola, o vão entre estrelas).
3. Na faixa da borda, a transparência vem da mistura entre o branco do contorno e o fundo,
   em vez de um corte seco: é isso que tira o serrilhado.
4. Tira a cor do fundo que vazou nos pixels semitransparentes e trabalha em 2x, reduzindo no fim.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def recortar(entrada: str, saida: str, lado: int = 1024) -> None:
    im = Image.open(entrada).convert('RGB')
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    rgb = np.asarray(im).astype(np.float32)
    lum = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    croma = rgb.max(axis=2) - rgb.min(axis=2)

    moldura = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    fundo = np.median(moldura, axis=0)
    lum_fundo = float(fundo @ np.array([0.299, 0.587, 0.114]))

    # fundo e sombras: neutros e não mais claros que o fundo (o contorno branco fica de fora)
    candidato = (croma < 28) & (lum < lum_fundo + 30)
    rotulos, n = ndimage.label(candidato)
    area_min = 0.0015 * lum.size
    borda = np.zeros_like(candidato)
    borda[:2], borda[-2:], borda[:, :2], borda[:, -2:] = True, True, True, True
    toca = set(np.unique(rotulos[borda & candidato])) - {0}
    areas = ndimage.sum(np.ones_like(lum), rotulos, index=np.arange(1, n + 1))
    eh_fundo = np.zeros(n + 1, dtype=bool)
    for i in range(1, n + 1):
        eh_fundo[i] = i in toca or areas[i - 1] >= area_min
    figura = ~eh_fundo[rotulos]
    figura = ndimage.binary_opening(figura, iterations=1)  # tira pontinhos soltos

    # faixa da borda: 4 px para cada lado (em 2x)
    dentro = ndimage.distance_transform_edt(figura)
    fora = ndimage.distance_transform_edt(~figura)
    faixa = (dentro <= 4) | (fora <= 4)

    branco = float(np.percentile(lum[figura & (dentro > 4) & (dentro < 14)], 90)) if (figura & (dentro > 4)).any() else 245.0
    branco = max(branco, lum_fundo + 40)
    mistura = np.clip((lum - lum_fundo) / (branco - lum_fundo), 0, 1)
    alfa = np.where(faixa, mistura, figura.astype(np.float32))
    alfa = ndimage.gaussian_filter(alfa, 0.8)
    alfa[(fora > 6)] = 0
    alfa[(dentro > 6)] = 1

    # tira o cinza do fundo que vazou na borda: C = (I - (1 - a) * fundo) / a
    a = alfa[..., None]
    limpo = np.where(a > 0.02, (rgb - (1 - a) * fundo) / np.maximum(a, 0.02), rgb)
    limpo = np.clip(limpo, 0, 255)

    rgba = np.dstack([limpo, alfa * 255]).astype(np.uint8)
    out = Image.fromarray(rgba, 'RGBA')
    caixa = out.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox()
    out = out.crop(caixa)
    w, h = out.size
    q = int(max(w, h) * 1.06)
    quadro = Image.new('RGBA', (q, q), (0, 0, 0, 0))
    quadro.paste(out, ((q - w) // 2, (q - h) // 2))
    quadro.resize((lado, lado), Image.LANCZOS).save(saida)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    recortar(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1024)
