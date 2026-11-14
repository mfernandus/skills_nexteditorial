"""Gera a capa 1600x900 no template ES Brasil Entrevista.
Uso: python3 gerar_thumb_esbrasil.py config.json saida.png

config.json:
{"linha1": "Linha A\\nLinha B\\nLinha C",  # manchete: até 3 linhas de ~15 caracteres (máx. 42 no total)
 "linha2": "Nome do Convidado",          # nome
 "linha3": "Cargo e empresa",            # opcional; só com manchete de até 2 linhas
 "foto": "recorte.png",              # PNG com fundo transparente (convidado já tratado)
 "foto_h": 870, "foto_right": -20}   # altura da foto e distância da borda direita (px)

Base: assets/base_clean.png = arte oficial com o texto e a pessoa de exemplo removidos.
Os selos (ES BRASIL ENTREVISTA, no alto, e ES BRASIL play, embaixo) fazem parte da base
e não são redesenhados.

Medidas tiradas da arte de referência (assets/template_referencia.jpg), em px na arte 1600x900:
  faixa inclinada a -5,35 graus; no eixo da faixa ela vai de v=267 a v=774 (centro 520)
  manchete: Inter ExtraBold Italic, corpo 40,5 (123,5 px), entreletras -2,1 (-6,4 px), entrelinha 0,886
  nome: Inter SemiBold Italic, corpo 20 (61 px), entreletras -0,5
  bloco (manchete + nome) centralizado na faixa; largura útil do texto: 900 px
  texto branco que vai ao lilás-rosado para a direita, com sombra azul-escura suave
  1 unidade de corpo = 3,05 px
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
K = 3.05
ANG = -5.35              # inclinação da faixa
V_CENTRO = 520           # centro da faixa no eixo inclinado
U_MANCHETE = 34          # margem esquerda da manchete (eixo inclinado)
U_NOME = 4.5             # margem esquerda do nome (eixo inclinado; na tela fica em x~70)
MAXW = 900               # largura máxima do texto: depois disso entra o convidado
CAP = 0.727              # altura das maiúsculas do Inter, em relação ao corpo

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def build(cfg):
    l1 = cfg["linha1"].split("\n")
    n = len(" ".join(l1))
    lim = cfg.get("max_chars", 42)
    assert n <= lim, f"manchete com {n} caracteres (máx. {lim})"
    assert len(l1) <= 3, "manchete: no máximo 3 linhas"
    u1 = max(38, cfg.get("corpo1", 40.5)); u2 = min(22, max(20, cfg.get("corpo2", 20)))
    u3 = cfg.get("corpo3", 14)
    t1, t2, t3 = u1 * K, u2 * K, u3 * K
    lh, gap = cfg.get("lh", 0.886), cfg.get("gap", 0.875)
    assert not (cfg.get("linha3") and len(l1) > 2), "linha de cargo só com manchete de até 2 linhas"
    # posições relativas à linha de base da 1ª linha da manchete
    ys = [i * lh * t1 for i in range(len(l1))]
    y2 = ys[-1] + gap * t1                     # linha de base do nome
    y3 = y2 + 0.30 * t2 + 0.95 * t3            # linha de base do cargo (opcional)
    bottom = y3 if cfg.get("linha3") else y2
    altura = CAP * t1 + bottom                 # do topo das maiúsculas à última linha de base
    v0 = cfg.get("v0", "auto")
    if v0 == "auto":                           # centraliza o bloco na faixa
        v0 = V_CENTRO - altura / 2 + CAP * t1
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
    texts = "".join(f'<text class="t1" x="{U_MANCHETE}" y="{v0 + dy:.1f}">{esc(t)}</text>'
                    for t, dy in zip(l1, ys))
    if cfg.get("linha2"):
        texts += f'<text class="t2" x="{U_NOME}" y="{v0 + y2:.1f}">{esc(cfg["linha2"])}</text>'
    if cfg.get("linha3"):
        texts += f'<text class="t3" x="{U_NOME}" y="{v0 + y3:.1f}">{esc(cfg["linha3"])}</text>'
    foto = ""
    if cfg.get("foto"):
        glow = '<div class="glow"></div>' if cfg.get("brilho") else ""   # brilho atrás do convidado: desligado por padrão
        foto = f'{glow}<img class="foto" src="data:image/png;base64,{b64(cfg["foto"])}">'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-ExtraBoldItalic.ttf')})}}
@font-face{{font-family:ISB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-SemiBoldItalic.ttf')})}}
*{{margin:0;padding:0}} body{{width:1600px;height:900px;overflow:hidden;position:relative;background:#000C3E}}
.base,.foto,svg{{position:absolute}} .base{{left:0;top:0;width:1600px;height:900px}}
.foto{{right:{cfg.get('foto_right', -20)}px;bottom:0;height:{cfg.get('foto_h', 870)}px}}
svg{{left:0;top:0}}
text{{fill:url(#tx);stroke:url(#tx);stroke-linejoin:round;paint-order:stroke;filter:url(#sh)}}
.t1{{stroke-width:1.6px;font-family:IEB;font-size:{t1:.1f}px;letter-spacing:{cfg.get('track', -2.1) * K:.2f}px}}
.t2{{stroke-width:1.2px;font-family:ISB;font-size:{t2:.1f}px;letter-spacing:{cfg.get('track2', -0.5) * K:.2f}px}}
.t3{{stroke-width:.6px;font-family:ISB;font-size:{t3:.1f}px;letter-spacing:{cfg.get('track3', -0.3) * K:.2f}px}}
.glow{{position:absolute;right:-140px;top:20px;width:1000px;height:900px;
 background:radial-gradient(closest-side,rgba(120,90,255,.20),rgba(224,30,112,.07) 60%,rgba(0,0,0,0) 100%);mix-blend-mode:screen}}
</style></head><body>
<img class="base" src="data:image/png;base64,{b64(ASSETS / 'base_clean.png')}">
{foto}
<svg width="1600" height="900"><defs>
<linearGradient id="tx" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="940" y2="0">
 <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#FBF0FF"/><stop offset="1" stop-color="#F8D4FF"/></linearGradient>
<filter id="sh" x="-5%" y="-20%" width="110%" height="160%">
<feDropShadow dx="3" dy="6" stdDeviation="6" flood-color="#00194F" flood-opacity=".45"/></filter></defs>
<g transform="rotate({ANG})">{texts}</g></svg>
</body></html>"""

def render(cfg, out):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        pg.set_content(build(cfg), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        larg = pg.evaluate("""()=>Object.fromEntries(['t1','t2','t3'].map(c=>[c,
            Math.max(0,...[...document.querySelectorAll('.'+c)].map(e=>e.getComputedTextLength()))]))""")
        for c, w in larg.items():
            if w > MAXW:
                print(f"AVISO: {c} com {w:.0f} px passa da largura útil ({MAXW} px). "
                      f"Reescreva o texto ou quebre em mais linhas; o corpo não é reduzido.")
        pg.screenshot(path=out, type="png")
        b.close()
    return larg

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    print(render(cfg, sys.argv[2]))
