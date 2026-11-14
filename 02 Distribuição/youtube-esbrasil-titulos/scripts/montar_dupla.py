"""Junta os recortes de dois convidados numa única imagem para a capa (PNG com transparência).
Uso: python3 montar_dupla.py esquerda.png direita.png saida.png [sobreposicao=0.25] [frente=direita]

Regras (aprovadas pelo Mário Fernando em 17/10/2026):
- Cada recorte entra INTEIRO: nunca corte a lateral de um rosto para caber.
- Os dois na mesma altura; quem fica na frente cobre só cabelo/ombro do outro, nunca o rosto.
- Coloque cada um olhando para o centro (quem olha para a esquerda vai à direita, e vice-versa).
- As laterais são esfumadas só na metade de baixo (corpo), para não cortar cabelo.
Na capa: "foto_h" 530–540 e "foto_right" -20. Se o nome encostar nas cabeças, use nomes curtos
("Thiago e Thayná").
"""
import sys, numpy as np
from PIL import Image

def esfuma(im, F=70):
    a = np.array(im.convert("RGBA")).astype(float); h, w = a.shape[:2]
    r = np.ones(w); r[:F] = np.linspace(0, 1, F); r[-F:] = np.linspace(1, 0, F)
    baixo = np.clip((np.linspace(0, 1, h)[:, None] - 0.55) / 0.3, 0, 1)
    a[..., 3] *= 1 - (1 - r[None, :]) * baixo
    return Image.fromarray(a.astype(np.uint8))

def dupla(esq, dir_, out, ov=0.25, frente="direita", H=900):
    A, B = esfuma(Image.open(esq)), esfuma(Image.open(dir_))
    A = A.resize((int(A.width * H / A.height), H), Image.LANCZOS)
    B = B.resize((int(B.width * H / B.height), H), Image.LANCZOS)
    x = int(A.width * (1 - ov)); g = Image.new("RGBA", (x + B.width, H))
    if frente == "direita":
        g.alpha_composite(A, (0, 0)); g.alpha_composite(B, (x, 0))
    else:
        g.alpha_composite(B, (x, 0)); g.alpha_composite(A, (0, 0))
    g.save(out); print(out, g.size)

if __name__ == "__main__":
    a = sys.argv
    dupla(a[1], a[2], a[3], float(a[4]) if len(a) > 4 else 0.25, a[5] if len(a) > 5 else "direita")
