"""Gera thumb 1600x900 sobre o template oficial Comunhão Entrevista.
Uso: python3 gerar_thumb.py config.json saida.png
config: {"linha1": "linha A\\nlinha B", "linha2": "...", "linha3": "...", "foto": "recorte.png",
         "foto_h": 840, "foto_right": -40}
Base: base_clean.png = template original com texto e pessoa de exemplo removidos
(fundo, faixa, retícula e selos são os pixels do próprio template).
Tipografia (Inter itálico; 1 unidade = 3.05 px na arte 1600x900, medido no template):
  linha1 (manchete): Inter ExtraBold Italic, corpo1 >= 38 (padrão 44), máx. 38 caracteres, 2 linhas
  linha2 (nome): Inter ExtraBold Italic, corpo2 22-24
  linha3 (apoio, opcional): Inter SemiBold Italic, corpo3 13-14
  track (entreletras) padrão recomendado -1.6; lh 0.88; gap 0.34; y0 "auto" centraliza na faixa
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent.parent / "assets"  # raiz da skill/assets
K = 3.05
ANG = -4.95          # inclinação da faixa no template
X0, Y0 = 70, 409     # baseline da 1ª linha do título no template
MAXW = 1010           # largura máxima do texto dentro da faixa

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def build(cfg):
    l1 = cfg["linha1"].split("\n")
    assert len(" ".join(l1)) <= 38, f"linha1 tem {len(' '.join(l1))} caracteres (máx. 38)"
    assert len(l1) <= 3, "linha1: no máximo 3 linhas"
    u1 = max(38, cfg.get("corpo1", 44)); u2 = max(18, cfg.get("corpo2", 21))
    t1, t2 = u1 * K, u2 * K
    lines = [(l, i * cfg.get("lh",0.86) * t1, "t1") for i, l in enumerate(l1)]
    y2 = (len(l1) - 1) * cfg.get("lh",0.86) * t1 + cfg.get("gap",0.42) * t1 + 0.95 * t2
    t3 = cfg.get("corpo3", 12) * K
    Y0 = cfg.get("y0", "auto")
    if Y0 == "auto":  # centraliza o bloco (manchete + nome [+ apoio]) na faixa amarela
        bottom = y2 + 0.22 * t2 + ((0.35 * t2 + t3 + 0.25 * t3) if cfg.get("linha3") else 0)
        Y0 = 503 - (bottom + 0.80 * t1) / 2 + 0.80 * t1
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
    texts = "".join(
        f'<text class="{c}" x="{X0}" y="{Y0 + dy:.1f}">{esc(t)}</text>' for t, dy, c in lines)
    if cfg.get("linha2"):
        texts += f'<text class="t2" x="{X0}" y="{Y0 + y2:.1f}">{esc(cfg["linha2"])}</text>'
    if cfg.get("linha3"):
        texts += f'<text class="t3" x="{X0}" y="{Y0 + y2 + 0.35*t2 + t3:.1f}">{esc(cfg["linha3"])}</text>'
    fb = b64(HERE / "fonts/Inter-ExtraBoldItalic.ttf")
    fm = b64(HERE / "fonts/Inter-SemiBoldItalic.ttf")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{fb})}}
@font-face{{font-family:IM;src:url(data:font/ttf;base64,{fm})}}
*{{margin:0;padding:0}} body{{width:1600px;height:900px;overflow:hidden;position:relative;background:#000}}
.base,.foto,svg{{position:absolute}} .base{{left:0;top:0;width:1600px;height:900px}}
.foto{{right:{cfg.get('foto_right',-40)}px;bottom:0;height:{cfg.get('foto_h',840)}px}}
svg{{left:0;top:0}}
text{{fill:#fff4dc;filter:url(#sh)}}
.t1{{font-family:IEB;font-size:{t1:.1f}px;letter-spacing:{cfg.get("track",-0.4)*K:.2f}px}}
.t2{{font-family:IEB;font-size:{t2:.1f}px;letter-spacing:{cfg.get("track",-0.4)*K:.2f}px}}
.glow{{position:absolute;right:-120px;top:40px;width:1000px;height:900px;
 background:radial-gradient(closest-side,rgba(255,150,40,.42),rgba(255,90,20,.18) 55%,rgba(0,0,0,0) 100%);mix-blend-mode:screen}}
.t3{{font-family:IM;font-size:{t3:.1f}px;letter-spacing:{cfg.get("track3",-0.6)*K:.2f}px}}
</style></head><body>
<img class="base" src="data:image/png;base64,{b64(HERE/'base_clean.png')}">
<div class="glow"></div><img class="foto" src="data:image/png;base64,{b64(cfg['foto'])}">
<svg width="1600" height="900"><defs><filter id="sh" x="-5%" y="-20%" width="110%" height="160%">
<feDropShadow dx="2" dy="5" stdDeviation="5" flood-color="#7a2300" flood-opacity=".45"/></filter></defs>
<g id="g" transform="rotate({ANG} {X0} {Y0:.1f})">{texts}</g></svg>
</body></html>"""

def render(cfg, out):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        pg.set_content(build(cfg), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        # se alguma linha passar da largura da faixa, reduz o corpo proporcionalmente
        pg.evaluate(f"""()=>{{for(const c of ['t1','t2']){{const els=[...document.querySelectorAll('.'+c)];
          const w=Math.max(0,...els.map(e=>e.getComputedTextLength())); if(w>{MAXW}){{console.log('AVISO: '+c+' largo demais');const f={MAXW}/w;
          els.forEach(e=>{{const fs=parseFloat(getComputedStyle(e).fontSize);e.style.fontSize=(fs*f)+'px'}})}}}}}}""")
        pg.wait_for_timeout(100)
        pg.screenshot(path=out, type="png")
        b.close()

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
