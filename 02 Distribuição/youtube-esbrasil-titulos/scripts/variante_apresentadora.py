"""Gera uma base do Destinos ES com outra apresentadora no círculo.
Uso: python3 variante_apresentadora.py quadro.jpg "Nome Sobrenome" cx cy diametro saida.png
  quadro.jpg  frame/foto da apresentadora (fundo de estúdio mantido)
  cx cy       centro do rosto no quadro (px); diametro = lado do recorte quadrado no quadro
A base oficial (assets/thumbs/destinos.png) traz a Kamila Rangel fixa: este script tira os fios que saem
do círculo e o nome, coloca a nova foto dentro do círculo (r=145, aro branco de 4 px) e reescreve o nome
em Inter Bold branco na mesma linha de base de "Kamila Rangel".
"""
import sys, pathlib, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
K = pathlib.Path(__file__).resolve().parent.parent
src, nome, cx, cy, dia, out = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6]), sys.argv[6]
base = cv2.imread(str(K / "assets/thumbs/destinos.png"))
H, W = base.shape[:2]
CX, CY, R = 221.5, 718.5, 145
yy, xx = np.mgrid[:H, :W]
dist = np.hypot(xx - CX, yy - CY)
m = np.zeros((H, W), np.uint8)
# fios de cabelo acima do aro
# (preenchidos abaixo por interpolação horizontal, linha a linha)
# nome "Kamila Rangel"
g = base[688:750, 382:722].min(axis=2) > 150
t = np.zeros((H, W), np.uint8); t[688:750, 382:722][g] = 255
t = cv2.dilate(t, np.ones((7, 7), np.uint8))
m = cv2.bitwise_or(m, t)
img = cv2.inpaint(base, m, 9, cv2.INPAINT_TELEA)
X0, X1 = 95, 355                               # fios de cabelo acima do aro: interpola entre as bordas
rng = np.random.default_rng(1)
for y in range(505, 640):
    a, b = img[y, X0 - 3:X0].mean(0), img[y, X1:X1 + 3].mean(0)
    for x in range(X0, X1):
        if np.hypot(x - CX, y - CY) > R + 3:
            t_ = (x - X0) / (X1 - X0)
            img[y, x] = np.clip(a * (1 - t_) + b * t_ + rng.normal(0, 1.5, 3), 0, 255)
img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# foto no círculo
q = Image.open(src).convert("RGB")
h = dia / 2
f = q.crop((int(cx - h), int(cy - h), int(cx + h), int(cy + h))).resize((2 * R + 8, 2 * R + 8), Image.LANCZOS)
f = ImageEnhance.Contrast(f).enhance(1.06); f = ImageEnhance.Color(f).enhance(1.05)
S = 4  # supersampling da máscara
mk = Image.new("L", ((2 * R + 8) * S,) * 2, 0)
ImageDraw.Draw(mk).ellipse((4 * S, 4 * S, (2 * R + 4) * S, (2 * R + 4) * S), 255)
mk = mk.resize((2 * R + 8,) * 2, Image.LANCZOS)
ox, oy = int(round(CX - R - 4)), int(round(CY - R - 4))
img.paste(f, (ox, oy), mk)
ring = Image.new("L", ((2 * R + 16) * S,) * 2, 0); d = ImageDraw.Draw(ring)
d.ellipse((4 * S, 4 * S, (2 * R + 12) * S, (2 * R + 12) * S), 255)
d.ellipse((8 * S, 8 * S, (2 * R + 8) * S, (2 * R + 8) * S), 0)
ring = ring.resize(((2 * R + 16),) * 2, Image.LANCZOS)
img.paste(Image.new("RGB", ring.size, "white"), (int(round(CX - R - 8)), int(round(CY - R - 8))), ring)
# nome
fonte = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 51)
d = ImageDraw.Draw(img)
TR = -2.7                                     # entreletras (px por caractere), calibrado em "Kamila Rangel"
x = 388.0
for i, ch in enumerate(nome):
    d.text((x, 731), ch, font=fonte, fill="white", anchor="ls")
    x += fonte.getlength(nome[:i + 1]) - fonte.getlength(nome[:i])
    x += TR
img.save(out)
print("ok", out)
