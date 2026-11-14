"""Gera as artes dos Shorts do canal Revista ES Brasil (1080x1920, PNG).
Uso:
  python3 gerar_short_esbrasil.py moldura config.json saida.png   # moldura com título e nome, para aplicar SOBRE o vídeo
  python3 gerar_short_esbrasil.py capa    config.json saida.png   # capa (thumb) do Short: foto + título + nome

config.json:
{"marca": "esbrasil",                 # esbrasil (azul) | destinos (rosa/roxo, só Destinos ES) | cafe (laranja, só Café com Moqueca)
 "titulo": "Linha 1\\nLinha 2",        # 2 linhas, máximo de 30 caracteres no total
 "nome": "Nome do Convidado",         # 1 linha
 "foto": "quadro.png",                # só na capa: quadro do vídeo ou foto do convidado
 "centro_x": 0.5, "centro_y": 0.42}   # só na capa: ponto da foto que fica no centro da janela (0 a 1)

Medidas enviadas pelo design (corpo em pontos a 300 dpi: 1 pt = 4,1667 px; entreletras em milésimos do corpo):
  MOLDURA  1080x1920 PNG; área livre para o vídeo: 1080x1260, de y=352 a y=1612
           título: 2 linhas, Inter ExtraBold Italic, corpo 22 (91,67 px), entrelinha 22, entreletras -35, máx. 30 caracteres
           nome: 1 linha, Inter SemiBold Italic, corpo 11 (45,83 px), entreletras -35
           texto centralizado, branco, inclinado a -4,85 graus
  CAPA     1080x1920; janela da foto de y=357 até a borda inclinada da faixa (y~1227 à esquerda, ~1118 à direita)
           título: corpo 29 (120 px), entrelinha 1,0, entreletras -35; nome: corpo 14 (58,3 px)  [medido na arte de referência]
"""
import base64, io, json, sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
PT = 300 / 72
ANG = -4.85
LAYOUT_PADRAO = {
    # âncoras = centro do texto na linha de base (1ª linha do título; linha do nome)
    "moldura": dict(base="shorts/moldura_{m}.png", t=22 * PT, n=11 * PT, at=(530, 209), an=(538, 371), maxw=900),
    "capa":    dict(base="shorts/capa_{m}.png",    t=120.0,   n=58.3,    at=(531.6, 1322.4), an=(538.8, 1538.4), maxw=980),
}
JANELA_PADRAO = (0, 357, 1080, 1230)      # retângulo onde entra a foto da capa (a faixa inclinada cobre a parte de baixo)
# Café com Moqueca (laranja/marrom, arte de 16/10/2026): faixa do título em cima na moldura; faixa marrom rasgada na capa
LAYOUT_CAFE = {
    "moldura": dict(base="shorts/moldura_{m}.png", t=88.0, n=46.0, at=(531, 203), an=(536, 366), maxw=860),
    "capa":    dict(base="shorts/capa_{m}.png",    t=122.0, n=58.3, at=(532, 1328), an=(538, 1559), maxw=930),
}
JANELA_CAFE = (0, 374, 1080, 1270)
# Destinos ES (rosa/roxo com mapa, arte de 16/10/2026): faixa reta inclinada na capa
LAYOUT_DESTINOS = {
    "moldura": dict(base="shorts/moldura_{m}.png", t=91.67, n=45.83, at=(531, 209), an=(537, 372), maxw=880),
    "capa":    dict(base="shorts/capa_{m}.png",    t=121.0, n=58.3, at=(533, 1322), an=(538, 1539), maxw=930),
}
JANELA_DESTINOS = (0, 358, 1080, 1240)
def layout(marca):
    return {"cafe": (LAYOUT_CAFE, JANELA_CAFE), "destinos": (LAYOUT_DESTINOS, JANELA_DESTINOS)}.get(marca, (LAYOUT_PADRAO, JANELA_PADRAO))
LAYOUT = LAYOUT_PADRAO

def b64(data):
    return base64.b64encode(data).decode()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def foto_na_janela(path, cx, cy, JANELA=JANELA_PADRAO):
    """Recorta/escala a foto para cobrir a janela, mantendo (cx, cy) o mais perto possível do centro."""
    x0, y0, x1, y1 = JANELA; w, h = x1 - x0, y1 - y0
    im = Image.open(path).convert("RGB")
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    left = min(max(0, round(im.width * cx - w / 2)), im.width - w)
    top = min(max(0, round(im.height * cy - h / 2)), im.height - h)
    buf = io.BytesIO(); im.crop((left, top, left + w, top + h)).save(buf, "PNG")
    return buf.getvalue()

def build(tipo, cfg):
    marca = cfg.get("marca", "esbrasil")
    assert marca in ("esbrasil", "destinos", "cafe"), "marca: esbrasil, destinos ou cafe"
    LAY, JANELA = layout(marca); L = LAY[tipo]
    linhas = cfg["titulo"].split("\n")
    n = len(" ".join(linhas)); lim = cfg.get("max_chars", 30)
    assert len(linhas) <= 2, "título: no máximo 2 linhas"
    assert n <= lim, f"título com {n} caracteres (máx. {lim})"
    t, nn = L["t"], L["n"]
    ax, ay = L["at"]
    if len(linhas) == 1:
        ay += t / 2
    tx = "".join(f'<text class="t" x="0" y="{i * t:.1f}">{esc(l)}</text>' for i, l in enumerate(linhas))
    g = f'<g transform="translate({ax},{ay:.1f}) rotate({ANG})">{tx}</g>'
    if cfg.get("nome"):
        g += f'<g transform="translate({L["an"][0]},{L["an"][1]}) rotate({ANG})"><text class="n" x="0" y="0">{esc(cfg["nome"])}</text></g>'
    foto = ""
    if tipo == "capa":
        png = foto_na_janela(cfg["foto"], cfg.get("centro_x", 0.5), cfg.get("centro_y", 0.42), JANELA)
        foto = (f'<img style="position:absolute;left:{JANELA[0]}px;top:{JANELA[1]}px" '
                f'src="data:image/png;base64,{b64(png)}">')
    base = (ASSETS / L["base"].format(m=marca)).read_bytes()
    fundo = "#000" if tipo == "capa" else "transparent"
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{b64((ASSETS / 'fonts/Inter-ExtraBoldItalic.ttf').read_bytes())})}}
@font-face{{font-family:ISB;src:url(data:font/ttf;base64,{b64((ASSETS / 'fonts/Inter-SemiBoldItalic.ttf').read_bytes())})}}
*{{margin:0;padding:0}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{fundo}}}
body{{position:relative}} .base,svg{{position:absolute;left:0;top:0}}
text{{fill:#fff;text-anchor:middle;filter:url(#sh)}}
.t{{font-family:IEB;font-size:{t:.2f}px;letter-spacing:{-0.035 * t:.2f}px}}
.n{{font-family:ISB;font-size:{nn:.2f}px;letter-spacing:{-0.035 * nn:.2f}px}}
</style></head><body>
{foto}
<img class="base" width="1080" height="1920" src="data:image/png;base64,{b64(base)}">
<svg width="1080" height="1920"><defs><filter id="sh" x="-5%" y="-20%" width="110%" height="160%">
<feDropShadow dx="3" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".30"/></filter></defs>{g}</svg>
</body></html>"""
    return L, html

def render(tipo, cfg, out):
    L, html = build(tipo, cfg)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(html, wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        larg = pg.evaluate("""()=>Object.fromEntries(['t','n'].map(c=>[c,
            Math.max(0,...[...document.querySelectorAll('.'+c)].map(e=>e.getComputedTextLength()))]))""")
        if larg["t"] > L["maxw"]:
            print(f"AVISO: título com {larg['t']:.0f} px passa da largura útil ({L['maxw']} px). Reescreva ou quebre de outro jeito.")
        pg.screenshot(path=out, type="png", omit_background=(tipo == "moldura"))
        b.close()
    return larg

if __name__ == "__main__":
    tipo = sys.argv[1]
    assert tipo in LAYOUT, "primeiro argumento: moldura ou capa"
    cfg = json.load(open(sys.argv[2], encoding="utf-8"))
    print(render(tipo, cfg, sys.argv[3]))
