"""Visual dos Shorts da Comunhão (1080x1920, PNG) no padrão Comunhão play.

Uso:
  python3 gerar_visual_short.py moldura config.json saida.png   # camada do vídeo (janela transparente)
  python3 gerar_visual_short.py capa    config.json saida.png   # capa (miniatura) do Short

config.json:
  {"titulo": "Quem domina\\nsua linguagem?",   # até 30 caracteres, 2 linhas (\\n opcional; quebra automática)
   "nome": "Tassos Lycurgo",                    # 1 linha
   "foto": "quadro_convidado.png"}              # só para a capa

ESPECIFICAÇÃO (fornecida pelo Mário Fernando, out/2026)
  Tela: 1080x1920 px, PNG.
  Área livre para o vídeo de fundo: 1260 px de altura (y 344 a 1604), largura total.
  Título: 2 linhas, Inter (ExtraBold Italic), corpo 22, entrelinha 22, tracking -35, máx. 30 caracteres.
  Nome:   1 linha,  Inter (ExtraBold Italic), corpo 11, tracking -35.
  Tracking -35 = -35/1000 do corpo (-0,035 em).
  Escala: 1 unidade de corpo = 4 px na tela 1080 (prancheta 270x480 exportada em 4x):
  corpo 22 = 88 px; corpo 11 = 44 px. Conferido contra o modelo aprovado.
  Capa: mesma fonte, tracking -35 e entrelinha = corpo, mas maior, como no modelo aprovado
  da capa: título corpo 30 (120 px), nome corpo 14 (56 px).
"""
import base64, json, math, sys, pathlib
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
W, H = 1080, 1920
K = 4.0                       # px por unidade de corpo (prancheta 270x480 exportada em 4x)
ANG = -4.95                   # inclinação das faixas e do texto (sobe para a direita)
TAN = math.tan(math.radians(-ANG))
VID_Y0, VID_Y1 = 344, 1604    # área livre do vídeo: 1260 px
MAX_CHARS = 30
BASE_MOLDURA = 292            # linha de base da 2ª linha do título (centro x)
BASE_CAPA = 1440
LOGO_W = 494                  # largura do PNG do logo play (arte visível ~450 px)
CREME = "#fff6d8"
MAXW = 980                    # largura máxima de uma linha (com margem de 50 px por lado)

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def quebrar(titulo):
    """Respeita a quebra manual; sem ela, divide em 2 linhas de tamanho parecido."""
    if "\n" in titulo:
        linhas = [l.strip() for l in titulo.split("\n") if l.strip()]
    else:
        p = titulo.split()
        if len(p) < 2:
            return [titulo]
        cands = [(" ".join(p[:i]), " ".join(p[i:])) for i in range(1, len(p))]
        linhas = list(min(cands, key=lambda c: abs(len(c[0]) - len(c[1]))))
    return linhas

def validar(cfg):
    t = cfg["titulo"].replace("\n", " ")
    assert len(t) <= MAX_CHARS, f"título com {len(t)} caracteres (máx. {MAX_CHARS}): {t!r}"
    assert len(quebrar(cfg["titulo"])) <= 2, "título: no máximo 2 linhas"
    assert cfg.get("nome") and "\n" not in cfg["nome"], "nome: obrigatório, 1 linha"

def bloco_texto(linhas, nome, cx, base2, c1, c2, gap=0.87):
    """SVG do bloco título + nome, centralizado em cx, girado como as faixas."""
    t1, t2 = c1 * K, c2 * K
    lead = c1 * K                 # entrelinha 22 = 100% do corpo
    y_nome = base2 + gap * t1              # distância medida no modelo
    if len(linhas) == 1:                   # 1 linha só: recentraliza o bloco
        base2 += lead / 2; y_nome += lead / 2
    ys = [base2 - lead * (len(linhas) - 1 - i) for i in range(len(linhas))]
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
    txt = "".join(f'<text class="t1" x="{cx}" y="{y:.1f}">{esc(l)}</text>' for l, y in zip(linhas, ys))
    txt += f'<text class="t2" x="{cx}" y="{y_nome:.1f}">{esc(nome)}</text>'
    cy = (ys[0] - 0.73 * t1 + y_nome) / 2
    css = (f".t1{{font-size:{t1:.1f}px;letter-spacing:{-0.035 * t1:.2f}px}}"
           f".t2{{font-size:{t2:.1f}px;letter-spacing:{-0.035 * t2:.2f}px}}")
    return f'<g transform="rotate({ANG} {cx} {cy:.1f})">{txt}</g>', css

def faixa(y_esq_topo, y_esq_base, cor_borda=True):
    """Polígono inclinado (mesmo ângulo do texto) com o degradê amarelo -> laranja."""
    d = TAN * W
    pts = f"0,{y_esq_topo} {W},{y_esq_topo - d:.1f} {W},{y_esq_base - d:.1f} 0,{y_esq_base}"
    return (f'<polygon points="{pts}" fill="url(#gfaixa)" filter="url(#sombra)"/>')

DEFS = """<defs>
<linearGradient id="gfaixa" x1="0" y1="1" x2="1" y2="0">
  <stop offset="0" stop-color="#ffc800"/><stop offset=".55" stop-color="#ffa000"/>
  <stop offset="1" stop-color="#ff7400"/></linearGradient>
<filter id="sombra" x="-5%" y="-10%" width="110%" height="130%">
  <feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#3a0600" flood-opacity=".55"/></filter>
<filter id="sh" x="-5%" y="-20%" width="110%" height="160%">
  <feDropShadow dx="2" dy="5" stdDeviation="5" flood-color="#7a2300" flood-opacity=".5"/></filter>
</defs>"""

VERMELHO = ("background:radial-gradient(ellipse 75% 60% at 50% 70%,#f0463f 0%,#c4231d 45%,#7a0b08 85%,#3a0000 100%)")
VERMELHO_CAPA = ("background:radial-gradient(ellipse 80% 13% at 50% 11%,#ee433c 0%,rgba(238,67,60,0) 100%),"
                 "radial-gradient(ellipse 80% 16% at 50% 93%,#e2352f 0%,rgba(226,53,47,0) 100%),"
                 "linear-gradient(#7a0806,#9c120e 50%,#7a0806)")
RETICULA = ("background-image:radial-gradient(rgba(0,0,0,.22) 1.4px,transparent 1.9px);"
            "background-size:7px 7px;mix-blend-mode:multiply")

def html(modo, cfg):
    fb = b64(ASSETS / "fonts/Inter-ExtraBoldItalic.ttf")
    play = b64(ASSETS / "logo_play.png")
    linhas = quebrar(cfg["titulo"])
    if modo == "moldura":
        g, css = bloco_texto(linhas, cfg["nome"], W / 2, BASE_MOLDURA, 22, 11)
        corpo = f"""
<div style="position:absolute;left:0;top:{VID_Y1}px;width:{W}px;height:{H - VID_Y1}px;{VERMELHO}">
  <div style="position:absolute;inset:0;{RETICULA}"></div>
  <div style="position:absolute;left:0;top:0;width:100%;height:5px;background:#5c0504"></div></div>
<img src="data:image/png;base64,{play}" style="position:absolute;width:{LOGO_W}px;left:{(W - LOGO_W) // 2}px;top:{1697 - LOGO_W * 95 // 350 // 2}px">
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{DEFS}
 {faixa(-120, 455)}<g filter="url(#sh)">{g}</g></svg>"""
        fundo = "transparent"
    else:  # capa
        foto = b64(cfg["foto"])
        g, css = bloco_texto(linhas, cfg["nome"], W / 2, BASE_CAPA, 30, 14, gap=0.80)
        corpo = f"""
<div style="position:absolute;inset:0;{VERMELHO_CAPA}"></div>
<div style="position:absolute;inset:0;{RETICULA}"></div>
<div style="position:absolute;left:0;top:358px;width:{W}px;height:1000px;overflow:hidden">
  <img src="data:image/png;base64,{foto}" style="width:100%;height:100%;object-fit:cover;object-position:{cfg.get('foto_pos', '50% 25%')}"></div>
<img src="data:image/png;base64,{b64(ASSETS / 'logo_comunhao.png')}" style="position:absolute;width:302px;left:{(W - 302) // 2}px;top:207px">
<img src="data:image/png;base64,{play}" style="position:absolute;width:{LOGO_W}px;left:{(W - LOGO_W) // 2}px;top:{1697 - LOGO_W * 95 // 350 // 2}px">
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{DEFS}
 {faixa(1228, 1645)}<g filter="url(#sh)">{g}</g></svg>"""
        fundo = "#3a0000"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:IEB;src:url(data:font/ttf;base64,{fb})}}
*{{margin:0;padding:0}} body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;background:{fundo}}}
text{{font-family:IEB;fill:{CREME};text-anchor:middle}} {css}
</style></head><body>{corpo}</body></html>"""

def render(modo, cfg, out):
    validar(cfg)
    if modo == "capa":
        assert cfg.get("foto"), "capa: informe 'foto' (quadro do convidado, olhos abertos, sem tarja)"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html(modo, cfg), wait_until="load")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        largura = pg.evaluate("Math.max(...[...document.querySelectorAll('text')].map(e=>e.getComputedTextLength()))")
        lim = MAXW * (1 if modo == "moldura" else 1.0)
        if largura > lim:
            print(f"AVISO: linha com {largura:.0f} px passa da largura útil ({lim} px). "
                  "Reescreva o título mais curto ou quebre em outro ponto; o corpo não é reduzido.")
        pg.screenshot(path=out, type="png", omit_background=(modo == "moldura"))
        b.close()
    print(out)

if __name__ == "__main__":
    modo, cfg_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
    assert modo in ("moldura", "capa"), "modo: moldura ou capa"
    render(modo, json.load(open(cfg_p, encoding="utf-8")), out)
