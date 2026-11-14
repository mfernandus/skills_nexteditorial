"""Gera a arte quadrada 1600x1600 (feed do Instagram/Facebook, capa de episódio) de Café com Moqueca ou Destinos ES.
Uso: python3 gerar_quadrado.py config.json saida.png

config.json:
{"template": "cafe",                    # cafe | destinos
 "manchete": "Linha 1\\nLinha 2",       # 2 linhas na faixa de baixo (até ~14 caracteres por linha)
 "nome": "Nome do Convidado",           # à esquerda, acima da faixa
 "episodio": "#68",                     # opcional; só com o número real do episódio (sem número, o canto fica vazio)
 "foto": "recorte.png",                 # PNG com fundo transparente (convidado tratado)
 "foto_h": 900, "foto_cx": 1100}        # altura da foto e centro horizontal (px)

Bases: assets/quadrado/<template>.png (arte de referência de 16/10/2026 com texto e pessoa de exemplo removidos).
Medidas tiradas da referência: texto a -4,9 graus; manchete Inter ExtraBold Italic ~164 px, entreletras -30,
entrelinha 1,05, alinhada à esquerda em x=88; nome Inter SemiBold Italic ~78 px (creme #FFF6DC);
episódio Inter ExtraBold 90 px, branco, alinhado à direita em x=1517. A foto fica acima da faixa.
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright
ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
ANG = -4.9
T = {
    "cafe":     dict(faixa=(990, 870), at=(86, 1216), an=(88, 818), t=190, n=97),
    "destinos": dict(faixa=(975, 865), at=(83, 1195), an=(82, 793), t=190, n=97),
}
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def html(cfg):
    L = T[cfg.get("template", "cafe")]
    linhas = cfg["manchete"].split("\n"); assert len(linhas) <= 2, "manchete: no máximo 2 linhas"
    t, n = cfg.get("t", L["t"]), cfg.get("n", L["n"])
    ax, ay = L["at"]
    if len(linhas) == 1: ay += 1.05 * t / 2
    tx = "".join(f'<text class="t" x="0" y="{i * 1.05 * t:.1f}">{esc(l)}</text>' for i, l in enumerate(linhas))
    g = f'<g transform="translate({ax},{ay:.1f}) rotate({ANG})">{tx}</g>'
    if cfg.get("nome"):
        g += f'<g transform="translate({L["an"][0]},{L["an"][1]}) rotate({ANG})"><text class="n" x="0" y="0">{esc(cfg["nome"])}</text></g>'
    if cfg.get("episodio"):
        g += f'<text class="e" x="1519" y="168">{esc(cfg["episodio"])}</text>'
    yl, yr = L["faixa"]
    foto = ""
    if cfg.get("foto"):
        h = cfg.get("foto_h", 900); cx = cfg.get("foto_cx", 1100)
        foto = (f'<img class="foto" style="height:{h}px;left:{cx}px;bottom:{1600 - max(yl, yr) - 40}px;transform:translateX(-50%);'
                f'clip-path:polygon(-2000px -2000px, 4000px -2000px, 4000px {yr + 3 - (1600 - (1600 - max(yl, yr) - 40) - h)}px, '
                f'-2000px {yl + 3 - (1600 - (1600 - max(yl, yr) - 40) - h)}px)" src="data:image/png;base64,{b64(cfg["foto"])}">')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-ExtraBoldItalic.ttf')})}}
@font-face{{font-family:ISB;src:url(data:font/ttf;base64,{b64(ASSETS / 'fonts/Inter-SemiBoldItalic.ttf')})}}
@font-face{{font-family:IE;src:url(data:font/otf;base64,{b64(ASSETS / 'fonts/Inter-ExtraBold.otf')})}}
*{{margin:0;padding:0}} body{{width:1600px;height:1600px;overflow:hidden;position:relative}}
.base,.foto,svg{{position:absolute}} .base{{left:0;top:0;width:1600px;height:1600px}} svg{{left:0;top:0}}
text{{filter:url(#sh)}}
.t{{fill:#fff;font-family:IEB;font-size:{t}px;letter-spacing:{-0.03 * t:.2f}px}}
.n{{fill:#FFF6DC;font-family:ISB;font-size:{n}px;letter-spacing:{-0.02 * n:.2f}px}}
.e{{fill:#fff;font-family:IE;font-size:84px;text-anchor:end;letter-spacing:-1px}}
</style></head><body>
<img class="base" src="data:image/png;base64,{b64(ASSETS / 'quadrado' / (cfg.get('template', 'cafe') + '.png'))}">
{foto}
<svg width="1600" height="1600"><defs><filter id="sh" x="-5%" y="-20%" width="110%" height="160%">
<feDropShadow dx="3" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".30"/></filter></defs>{g}</svg>
</body></html>"""
def render(cfg, out):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1600})
        pg.set_content(html(cfg), wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        w = pg.evaluate("()=>Math.max(...[...document.querySelectorAll('.t')].map(e=>e.getComputedTextLength()))")
        if w > 1420: print(f"AVISO: manchete com {w:.0f} px passa da largura útil (1420 px). Reescreva ou quebre de outro jeito.")
        pg.screenshot(path=out, type="png"); b.close()
if __name__ == "__main__":
    render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
