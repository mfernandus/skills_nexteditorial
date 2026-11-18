"""Camada de selos dos Shorts (1080x1920, PNG transparente) — Passo 13, item 7 do SKILL.md.

Uso:
  python3 montar_selos.py saida.png                          # só a marca: quadradinho COM à direita
  python3 montar_selos.py saida.png assets/logo_entrevista.png  # programa à esquerda + quadradinho à direita

Gera as camadas prontas da pasta assets/selos/ (selos_so_marca.png, selos_[programa].png), usadas por cima do
vídeo no ffmpeg (references/montagem_shorts.md). Medidas: 120 px de altura, topo em y=220, a 48 px das bordas,
sombra leve; quadradinho com cantos de raio 14. Usa sempre os arquivos oficiais, nunca redesenha.
Se um selo encostar no rosto em algum Short, gere uma camada com --altura 100 (os dois juntos; nunca tire um só).
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFilter

RAIZ = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1920


def selo(arq, altura, raio=0):
    im = Image.open(arq).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb:
        im = im.crop(bb)
    im = im.resize((round(im.width * altura / im.height), altura), Image.LANCZOS)
    if raio:
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), raio, fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), m, m))
    return im


def main(argv):
    altura = 120
    if "--altura" in argv:
        i = argv.index("--altura"); altura = int(argv[i + 1]); del argv[i:i + 2]
    saida = argv[0]
    programa = argv[1] if len(argv) > 1 else None
    marca = RAIZ / "assets" / "selos" / "com_quadrado.png"
    if not marca.exists():
        sys.exit("AVISO — falta assets/selos/com_quadrado.png (selo oficial). Nunca redesenhe o selo.")
    topo, borda = 220, 48
    raio = round(14 * altura / 120)
    camada = Image.new("RGBA", (W, H))
    q = selo(marca, altura, raio)
    camada.alpha_composite(q, (W - borda - q.width, topo))
    if programa:
        p = selo(RAIZ / programa if not pathlib.Path(programa).is_absolute() else programa, altura)
        if borda + p.width + 24 > W - borda - q.width:
            sys.exit("AVISO — os dois selos se encostam; confira o arquivo do logo do programa.")
        camada.alpha_composite(p, (borda, topo))
    # sombra leve (azul-marinho, 45%) por baixo dos selos
    a = camada.getchannel("A").point(lambda v: int(v * 0.45))
    sombra = Image.new("RGBA", (W, H), (0, 25, 60, 0)); sombra.putalpha(a)
    sombra = sombra.filter(ImageFilter.GaussianBlur(6))
    final = Image.new("RGBA", (W, H)); final.alpha_composite(sombra, (0, 2)); final.alpha_composite(camada)
    final.save(saida)
    print(f"camada de selos: {saida} ({'programa + marca' if programa else 'só a marca'}, {altura} px)")


if __name__ == "__main__":
    main(sys.argv[1:])
