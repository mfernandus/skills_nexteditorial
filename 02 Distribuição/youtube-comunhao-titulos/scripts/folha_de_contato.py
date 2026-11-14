"""Monta uma folha de contato para escolher o quadro do convidado.
Uso: python3 folha_de_contato.py saida.jpg quadro1.jpg quadro2.jpg ...   (até 24 quadros)
Cada miniatura leva o nome do arquivo (ex.: o percentual do vídeo) no canto, em amarelo.
Critérios de escolha: rosto de frente ou 3/4 olhando para o centro da capa, olhos abertos, boca
fechada ou sorriso; sem tarja de nome, sem microfone na frente do rosto; cabeça inteira no quadro;
nunca o apresentador. Se nenhum servir, capture mais quadros em outros pontos do vídeo.
"""
import sys, pathlib
from PIL import Image, ImageDraw
out, fs = sys.argv[1], sys.argv[2:26]
cols = 6 if len(fs) > 12 else 4; w, h = (320, 180) if cols == 6 else (400, 225)
rows = (len(fs) + cols - 1) // cols
g = Image.new("RGB", (cols * w, rows * h)); d = ImageDraw.Draw(g)
for k, f in enumerate(fs):
    x, y = (k % cols) * w, (k // cols) * h
    g.paste(Image.open(f).convert("RGB").resize((w, h)), (x, y))
    d.text((x + 5, y + 5), pathlib.Path(f).stem.split("_")[-1], fill="yellow")
g.save(out, quality=85); print(out)
