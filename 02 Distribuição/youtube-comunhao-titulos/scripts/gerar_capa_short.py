"""Capa do Short (1080x1920) no modelo foto cheia — Passo 13, item 8 do SKILL.md.

Uso: python3 gerar_capa_short.py config.json saida.jpg

config (caminhos relativos à pasta da skill ou absolutos):
{
  "titulo": "Quem domina\\nsua linguagem?",   # até 30 caracteres, 2 linhas (\\n opcional: sem ele, quebra equilibrada)
  "nome": "Tassos Lycurgo",
  "cargo": "Professor e escritor",             # opcional (linha de apoio)
  "foto": "recorte.png",                       # recorte com fundo transparente (rembg/tratar_foto.py)
                                               # ou foto opaca do assunto (Short sem convidado: tela cheia)
  "programa": "assets/logo_entrevista.png",    # opcional: logo do programa (canto esquerdo); sem ele, só o quadradinho
  "selo_marca": "assets/selos/com_quadrado.png",  # padrão; o arquivo oficial tem de existir
  "cabeca_x": null,                            # opcional: centro da cabeça no recorte (0 a 1); padrão = medido
  "topo_cabeca": 262                           # opcional: y do topo da cabeça
}

Regras aplicadas (não altere sem mudar o SKILL.md junto):
- fundo azul #00427B; recorte assentado com o topo da cabeça em y=262, cabeça centrada em x=540, base na borda;
- véu só na base: 760 px, do transparente a 85% de rgb(0,25,60);
- selos: 132 px de altura, topo em y=272, a 56 px das bordas, sombra leve, quadradinho com raio 16;
- texto à esquerda, margens de 96 px, base do bloco em y=1652: filete 96x10 #FFC220, título, nome, cargo;
  espaço de 28 px entre filete, título e nome;
- título: Inter ExtraBold (sem itálico), entreletras -2%, entrelinha 1,08, sombra 0 2 16 px azul-marinho 55%;
- TRAVA DO TEXTO: maior corpo entre 56 e 92 px em que a linha mais longa x 1,08 caiba em 888 px;
  nome (48) e cargo (36) também travados, mínimo 30 px. Se não couber, o script PARA com AVISO:
  reescreva o título mais curto. Nunca 3 linhas, nunca margem menor, nunca texto fora da tela.
Requer Pillow e as fontes do kit em assets/fonts/.
"""
import json, pathlib, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTES = RAIZ / "assets" / "fonts"
W, H = 1080, 1920
AZUL = (0, 66, 123)
MARINHO = (0, 25, 60)
OURO = (255, 194, 32)
CREME = (255, 246, 216)
MARGEM = 96
LARGURA_UTIL = W - 2 * MARGEM          # 888
BASE_BLOCO = 1652
MAX_TITULO = 30


def aviso(msg, texto=True):
    sys.exit("AVISO — capa do Short não gerada: " + msg + (
        " Se o título veio do jornalista, devolva a ele com uma sugestão mais curta; não corte por conta própria."
        if texto else ""))


def caminho(p):
    p = pathlib.Path(p)
    return p if p.is_absolute() else (RAIZ / p if (RAIZ / p).exists() else pathlib.Path.cwd() / p)


def fonte(nome, corpo):
    return ImageFont.truetype(str(FONTES / nome), int(round(corpo)))


def largura(texto, f, corpo, track=-0.02):
    """Largura com o entreletras aplicado (track em fração do corpo por letra)."""
    return f.getlength(texto) + track * corpo * max(len(texto) - 1, 0)


def quebrar(titulo):
    if "\n" in titulo:
        return [l.strip() for l in titulo.split("\n")]
    pal = titulo.split()
    if len(pal) == 1:
        return [titulo]
    f = fonte("Inter-ExtraBold.otf", 80)
    melhor = min(range(1, len(pal)), key=lambda i: abs(f.getlength(" ".join(pal[:i])) - f.getlength(" ".join(pal[i:]))))
    return [" ".join(pal[:melhor]), " ".join(pal[melhor:])]


def maior_corpo(linhas, nome_fonte, cmax, cmin, track=-0.02, folga=1.08):
    for c in range(cmax, cmin - 1, -1):
        f = fonte(nome_fonte, c)
        if max(largura(l, f, c, track) for l in linhas) * folga <= LARGURA_UTIL:
            return c
    return None


def escrever(camada, xy, texto, f, corpo, cor, track=-0.02):
    d = ImageDraw.Draw(camada)
    x, y = xy
    for i, ch in enumerate(texto):   # preserva o kerning: posição = largura do prefixo + entreletras
        d.text((x + f.getlength(texto[:i]) + track * corpo * i, y), ch, font=f, fill=cor, anchor="ls")


def sombra(base, desenho, dx=0, dy=2, raio=8, alfa=0.55):
    """Aplica sombra (cor azul-marinho) a partir do canal alfa de 'desenho' e cola o desenho por cima."""
    a = desenho.getchannel("A").point(lambda v: int(v * alfa))
    s = Image.new("RGBA", desenho.size, MARINHO + (0,))
    s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(s, (dx, dy))
    base.alpha_composite(desenho)


def foto_recorte(capa, cfg):
    im = Image.open(caminho(cfg["foto"])).convert("RGBA")
    alfa = im.getchannel("A")
    bbox = alfa.point(lambda v: 255 if v > 40 else 0).getbbox()
    opaca = bbox is None or alfa.getextrema()[0] > 200
    if opaca:   # Short sem convidado: foto do assunto em tela cheia (cobre 1080x1920)
        esc = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
        capa.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
        return "tela cheia"
    im = im.crop(bbox)
    topo = cfg.get("topo_cabeca", 262)
    esc = (H - topo) / im.height                       # do topo da cabeça até a borda de baixo
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    if cfg.get("cabeca_x") is not None:
        cx = cfg["cabeca_x"] * im.width
    else:   # centro da cabeça = centro da massa do alfa nos 22% de cima do recorte
        faixa = im.getchannel("A").crop((0, 0, im.width, int(im.height * 0.22)))
        cols = [sum(faixa.crop((x, 0, x + 1, faixa.height)).histogram()[41:])
                for x in range(0, im.width, 4)]
        tot = sum(cols) or 1
        cx = sum(i * 4 * c for i, c in enumerate(cols)) / tot
    capa.alpha_composite(im, (round(W / 2 - cx), topo))
    return f"recorte: cabeça em x=540, topo em y={topo}"


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


def gerar(cfg, saida):
    linhas = quebrar(cfg["titulo"])
    n = len(" ".join(linhas))
    if n > MAX_TITULO:
        aviso(f"o título da capa tem {n} caracteres; o máximo é {MAX_TITULO}. Reduza {n - MAX_TITULO} ou mais.")
    if len(linhas) > 2:
        aviso(f"o título da capa está em {len(linhas)} linhas; o máximo é 2.")
    ct = maior_corpo(linhas, "Inter-ExtraBold.otf", 92, 56)
    if ct is None:
        aviso("o título não cabe em 2 linhas nem no corpo 56 dentro das margens de 96 px.")
    cn = maior_corpo([cfg["nome"]], "Inter-Bold.otf", 48, 30, track=0) if cfg.get("nome") else 0
    cc = maior_corpo([cfg["cargo"]], "Inter-Regular.otf", 36, 30, track=0) if cfg.get("cargo") else 0
    if cn is None:
        aviso("o nome não cabe na largura nem no corpo 30.")
    if cc is None:
        aviso("o cargo/linha de apoio não cabe na largura nem no corpo 30.")

    marca = caminho(cfg.get("selo_marca", "assets/selos/com_quadrado.png"))
    if not marca.exists():
        aviso(f"falta o selo oficial da marca ({marca.relative_to(RAIZ) if RAIZ in marca.parents else marca}). "
              "Envie a pasta assets/selos/ para a skill; nunca redesenhe o selo.", texto=False)

    capa = Image.new("RGBA", (W, H), AZUL + (255,))
    modo = foto_recorte(capa, cfg)

    veu = Image.new("RGBA", (W, 760))
    for y in range(760):
        ImageDraw.Draw(veu).line([(0, y), (W, y)], fill=MARINHO + (int(255 * 0.85 * y / 759),))
    capa.alpha_composite(veu, (0, H - 760))

    camada = Image.new("RGBA", (W, H))
    q = selo(marca, 132, raio=16)
    camada.alpha_composite(q, (W - 56 - q.width, 272))
    if cfg.get("programa"):
        p = selo(caminho(cfg["programa"]), 132)
        camada.alpha_composite(p, (56, 272))
        if 56 + p.width + 24 > W - 56 - q.width:
            aviso("os dois selos se encostam; confira o arquivo do logo do programa.", texto=False)
    sombra(capa, camada, 0, 2, 6, 0.45)

    # bloco de texto, de baixo para cima (base do bloco em y=1652)
    texto = Image.new("RGBA", (W, H))
    y = BASE_BLOCO
    if cc:
        escrever(texto, (MARGEM, y), cfg["cargo"], fonte("Inter-Regular.otf", cc), cc, CREME, 0)
        y -= round(cc * 1.3)
    if cn:
        escrever(texto, (MARGEM, y), cfg["nome"], fonte("Inter-Bold.otf", cn), cn, (255, 255, 255), 0)
        y -= round(cn * 0.73) + 28 + round(ct * 0.22)
    ft = fonte("Inter-ExtraBold.otf", ct)
    bases = [y - round(ct * 1.08) * (len(linhas) - 1 - i) for i in range(len(linhas))]
    tit = Image.new("RGBA", (W, H))
    for l, b in zip(linhas, bases):
        escrever(tit, (MARGEM, b), l, ft, ct, (255, 255, 255))
    topo_titulo = bases[0] - round(ct * 0.73)
    ImageDraw.Draw(texto).rectangle((MARGEM, topo_titulo - 28 - 10, MARGEM + 96, topo_titulo - 28), fill=OURO + (255,))
    sombra(capa, tit, 0, 2, 8, 0.55)
    capa.alpha_composite(texto)

    # conferência: nada passa da margem nem sai do miolo 3:4 (y 240 a 1680)
    caixa = Image.alpha_composite(tit, texto).getchannel("A").getbbox()
    if caixa and (caixa[0] < MARGEM - 2 or caixa[2] > W - MARGEM + 2 or caixa[1] < 240 or caixa[3] > 1680):
        aviso(f"o texto saiu da área segura (caixa {caixa}).")
    if caixa and caixa[1] < 272 + 132 + 40:
        aviso("o bloco de texto subiu até os selos; encurte o título ou o cargo.")

    rgb = capa.convert("RGB")
    for qual in (92, 88, 84, 80, 75):
        rgb.save(saida, "JPEG", quality=qual, optimize=True)
        if pathlib.Path(saida).stat().st_size < 2_000_000:
            break
    print(f"capa: {modo}; título {n} caracteres em {len(linhas)} linha(s), corpo {ct}; "
          f"nome {cn or '-'}; cargo {cc or '-'}; {pathlib.Path(saida).stat().st_size // 1024} KB")


if __name__ == "__main__":
    gerar(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
