"""Gera a capa 1600x900 do canal Revista ES Brasil em um dos três templates.
Uso: python3 gerar_thumb_esbrasil.py config.json saida.png

config.json:
{"template": "entrevista",                  # entrevista | destinos | cafe
 "linha1": "Linha A\\nLinha B",              # manchete (quebra de linha com \\n)
 "linha2": "Nome do Convidado",              # nome
 "linha3": "Cargo e empresa",                # só no template entrevista, com manchete de até 2 linhas
 "foto": "recorte.png",                      # PNG com fundo transparente (convidado já tratado)
 "foto_h": 860, "foto_right": -20,           # altura da foto e distância da borda direita (px)
 "apresentadora": "ludmila"}                 # só Destinos ES: ludmila | thamiris | leticia (padrão: Kamila)

Bases: assets/thumbs/<template>.png = arte oficial com o texto e o convidado de exemplo removidos.
Logos, selos e o apresentador (Destinos ES e Café com Moqueca) fazem parte da base e não são redesenhados.

Medidas (arte 1600x900; corpo em pontos a 300 dpi: 1 pt = 4,1667 px):
  ENTREVISTA  faixa a -5,35 graus; manchete Inter ExtraBold Italic 123,5 px (corpo ~30), entreletras -52,
              entrelinha 0,886; até 3 linhas de ~15 caracteres (máx. 42); nome Inter SemiBold Italic 61 px,
              alinhado à esquerda; bloco centralizado na faixa; texto branco -> lilás; largura útil 900 px.
  DESTINOS ES e CAFÉ COM MOQUECA
              texto a -4,9 graus; manchete Inter ExtraBold Italic corpo 28 (116,67 px), entreletras -30,
              entrelinha 1,05; 2 linhas de até ~17 caracteres (máx. 34); nome Inter SemiBold Italic corpo 15
              (62,5 px), entreletras -35, alinhado à DIREITA em x=990; texto branco; largura útil 945 px.
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
PT = 300 / 72            # 1 ponto = 4,1667 px (arte a 300 dpi)
CAP = 0.727              # altura das maiúsculas do Inter, em relação ao corpo

TEMPLATES = {
    "entrevista": dict(base="thumbs/entrevista.png", max_linhas=3, max_chars=42, maxw=900),
    "destinos":   dict(base="thumbs/destinos.png",   max_linhas=2, max_chars=34, maxw=945),
    "cafe":       dict(base="thumbs/cafe.png",       max_linhas=2, max_chars=34, maxw=945),
}

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def textos_entrevista(cfg, l1):
    K = 3.05
    ang, v_centro, u_manchete, u_nome = -5.35, 520, 34, 4.5
    u1 = max(38, cfg.get("corpo1", 40.5)); u2 = min(22, max(20, cfg.get("corpo2", 20))); u3 = cfg.get("corpo3", 14)
    t1, t2, t3 = u1 * K, u2 * K, u3 * K
    lh, gap = cfg.get("lh", 0.886), cfg.get("gap", 0.875)
    assert not (cfg.get("linha3") and len(l1) > 2), "linha de cargo só com manchete de até 2 linhas"
    ys = [i * lh * t1 for i in range(len(l1))]
    y2 = ys[-1] + gap * t1
    y3 = y2 + 0.30 * t2 + 0.95 * t3
    altura = CAP * t1 + (y3 if cfg.get("linha3") else y2)
    v0 = cfg.get("v0", "auto")
    if v0 == "auto":                               # centraliza o bloco na faixa
        v0 = v_centro - altura / 2 + CAP * t1
    tx = "".join(f'<text class="t1" x="{u_manchete}" y="{v0 + dy:.1f}">{esc(t)}</text>' for t, dy in zip(l1, ys))
    if cfg.get("linha2"):
        tx += f'<text class="t2" x="{u_nome}" y="{v0 + y2:.1f}">{esc(cfg["linha2"])}</text>'
    if cfg.get("linha3"):
        tx += f'<text class="t3" x="{u_nome}" y="{v0 + y3:.1f}">{esc(cfg["linha3"])}</text>'
    css = (f".t1{{stroke-width:1.6px;font-family:IEB;font-size:{t1:.1f}px;letter-spacing:{cfg.get('track', -2.1) * K:.2f}px}}"
           f".t2{{stroke-width:1.2px;font-family:ISB;font-size:{t2:.1f}px;letter-spacing:{cfg.get('track2', -0.5) * K:.2f}px}}"
           f".t3{{stroke-width:.6px;font-family:ISB;font-size:{t3:.1f}px;letter-spacing:{cfg.get('track3', -0.3) * K:.2f}px}}"
           "text{fill:url(#tx);stroke:url(#tx);stroke-linejoin:round;paint-order:stroke;filter:url(#sh)}")
    defs = ('<linearGradient id="tx" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="940" y2="0">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#FBF0FF"/><stop offset="1" stop-color="#F8D4FF"/></linearGradient>'
            '<filter id="sh" x="-5%" y="-20%" width="110%" height="160%">'
            '<feDropShadow dx="3" dy="6" stdDeviation="6" flood-color="#00194F" flood-opacity=".45"/></filter>')
    return css, defs, f'<g transform="rotate({ang})">{tx}</g>'

def textos_programa(cfg, l1):
    assert not cfg.get("linha3"), "os templates Destinos ES e Café com Moqueca não têm linha de cargo"
    ang = -4.9
    t1 = cfg.get("corpo1", 28) * PT; t2 = cfg.get("corpo2", 15) * PT
    pitch = cfg.get("lh", 1.05) * t1
    ax, ay = 72, 354                                 # linha de base da 1ª linha da manchete
    if len(l1) == 1:                                  # uma linha só: fica no meio das duas posições
        ay += pitch / 2
    tx = "".join(f'<text class="t1" x="0" y="{i * pitch:.1f}">{esc(t)}</text>' for i, t in enumerate(l1))
    g = f'<g transform="translate({ax},{ay:.1f}) rotate({ang})">{tx}</g>'
    if cfg.get("linha2"):
        g += f'<g transform="translate(990,505) rotate({ang})"><text class="t2" x="0" y="0">{esc(cfg["linha2"])}</text></g>'
    css = (f".t1{{font-family:IEB;font-size:{t1:.2f}px;letter-spacing:{cfg.get('track', -30) / 1000 * t1:.2f}px}}"
           f".t2{{font-family:ISB;font-size:{t2:.2f}px;letter-spacing:{cfg.get('track2', -35) / 1000 * t2:.2f}px;text-anchor:end}}"
           "text{fill:#fff;filter:url(#sh)}")
    defs = ('<filter id="sh" x="-5%" y="-20%" width="110%" height="160%">'
            '<feDropShadow dx="3" dy="6" stdDeviation="7" flood-color="#000" flood-opacity=".30"/></filter>')
    return css, defs, g

def build(cfg):
    nome = cfg.get("template", "entrevista")
    assert nome in TEMPLATES, f"template desconhecido: {nome} (use entrevista, destinos ou cafe)"
    T = dict(TEMPLATES[nome])
    if cfg.get("apresentadora"):                    # Destinos ES: base com outra apresentadora no círculo
        T["base"] = f"thumbs/destinos_{cfg['apresentadora']}.png"
    l1 = cfg["linha1"].split("\n")
    n = len(" ".join(l1)); lim = cfg.get("max_chars", T["max_chars"])
    assert n <= lim, f"manchete com {n} caracteres (máx. {lim} no template {nome})"
    assert len(l1) <= T["max_linhas"], f"manchete: no máximo {T['max_linhas']} linhas no template {nome}"
    css, defs, textos = (textos_entrevista if nome == "entrevista" else textos_programa)(cfg, l1)
    foto = ""
    if cfg.get("foto"):
        foto = f'<img class="foto" src="data:image/png;base64,{b64(cfg["foto"])}">'
    return T, f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-ExtraBoldItalic.ttf')})}}
@font-face{{font-family:ISB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-SemiBoldItalic.ttf')})}}
*{{margin:0;padding:0}} body{{width:1600px;height:900px;overflow:hidden;position:relative;background:#000C3E}}
.base,.foto,svg{{position:absolute}} .base{{left:0;top:0;width:1600px;height:900px}}
.foto{{right:{cfg.get('foto_right', -20)}px;bottom:0;height:{cfg.get('foto_h', 860)}px}}
svg{{left:0;top:0}}
{css}
</style></head><body>
<img class="base" src="data:image/png;base64,{b64(ASSETS / T['base'])}">
{foto}
<svg width="1600" height="900"><defs>{defs}</defs>{textos}</svg>
</body></html>"""

def render(cfg, out):
    T, html = build(cfg)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        pg.set_content(html, wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        larg = pg.evaluate("""()=>Object.fromEntries(['t1','t2','t3'].map(c=>[c,
            Math.max(0,...[...document.querySelectorAll('.'+c)].map(e=>e.getComputedTextLength()))]))""")
        for c, w in larg.items():
            if c == "t1" and w > T["maxw"]:
                print(f"AVISO: manchete com {w:.0f} px passa da largura útil ({T['maxw']} px). "
                      f"Reescreva ou quebre de outro jeito; o corpo não é reduzido.")
        pg.screenshot(path=out, type="png")
        b.close()
    return larg

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    print(render(cfg, sys.argv[2]))
