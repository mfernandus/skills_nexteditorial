"""Gera thumb 1600x900 sobre o template oficial Comunhão Entrevista.
Uso: python3 gerar_thumb.py config.json saida.png
config: {"linha1": "linha A\\nlinha B", "linha2": "...", "linha3": "...", "foto": "recorte.png",
         "foto_h": 840, "foto_right": -40}
Base: base_clean.png = template original com texto e pessoa de exemplo removidos
(fundo, faixa, retícula e selos são os pixels do próprio template).
Tipografia (Inter itálico; 1 unidade = 3.05 px na arte 1600x900, medido no template):
  linha1 (manchete): Inter ExtraBold Italic, máx. 60 caracteres e 3 linhas (4 linhas nunca).
    até 38 caracteres: 2 linhas, corpo1 44 (mínimo 38)
    39 a 60 caracteres: 3 linhas, corpo1 entre 32 e 38 (o maior que couber; padrão 38)
    Se não couber (mais de 60 caracteres, 4 linhas ou corpo abaixo do mínimo), o script NÃO reduz:
    para com um AVISO pedindo manchete mais curta (regra de 18/11/2026).
  Conferência do rosto (foto recortada com fundo transparente): se alguma letra encostar no rosto ou no
    cabelo da cabeça, o script para com AVISO (capa não aprovada). Raspar um fio solto (< 150 px) é aceito.
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
MAXCHARS = 60         # manchete: até 60 caracteres com espaços (antes 38; mudou em 18/11/2026)

def piso(n):
    """Corpo mínimo da manchete: 38 até 38 caracteres; 32 nas manchetes longas (39 a 60)."""
    return 38 if n <= 38 else 32

def aviso(msg):
    sys.exit("AVISO — precisa reduzir o título da capa: " + msg +
             " Se o título veio do jornalista, devolva a ele com uma sugestão mais curta; não corte por conta própria.")

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def build(cfg):
    l1 = cfg["linha1"].split("\n")
    n = len(" ".join(l1))
    if n > MAXCHARS:
        aviso(f"a manchete tem {n} caracteres; o máximo é {MAXCHARS}. Reduza {n - MAXCHARS} caracteres ou mais.")
    if len(l1) > 3:
        aviso(f"a manchete está em {len(l1)} linhas; o máximo é 3 (4 linhas nunca).")
    cfg["_min1"] = piso(n)
    u1 = max(cfg["_min1"], cfg.get("corpo1", 44 if n <= 38 else 38)); u2 = max(18, cfg.get("corpo2", 21))
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
        # se alguma linha passar da largura da faixa, reduz o corpo proporcionalmente, mas nunca abaixo
        # do mínimo da manchete (38 ou 32): abaixo disso, para e pede manchete mais curta
        r = pg.evaluate(f"""()=>{{const out={{}};for(const c of ['t1','t2']){{const els=[...document.querySelectorAll('.'+c)];
          const w=Math.max(0,...els.map(e=>e.getComputedTextLength())); const fs=els.length?parseFloat(getComputedStyle(els[0]).fontSize):0;
          out[c]={{w:w,fs:fs}}; if(w>{MAXW}){{const f={MAXW}/w; els.forEach(e=>{{e.style.fontSize=(fs*f)+'px'}}); out[c].fs=fs*f}}}}return out}}""")
        corpo_final = r["t1"]["fs"] / K
        if corpo_final < cfg["_min1"] - 0.05:
            b.close()
            aviso(f"para caber na faixa, a manchete cairia para o corpo {corpo_final:.1f} (mínimo {cfg['_min1']}).")
        print(f"manchete: {len(' '.join(cfg['linha1'].split(chr(10))))} caracteres, "
              f"{len(cfg['linha1'].split(chr(10)))} linhas, corpo final {corpo_final:.1f}")
        pg.wait_for_timeout(100)
        pg.screenshot(path=out, type="png")
        # conferência: nenhuma letra pode encostar no rosto/cabelo (recorte com fundo transparente)
        so = lambda css: (pg.add_style_tag(content=css), pg.screenshot(type="png", omit_background=True))[1]
        pg.add_style_tag(content="body{background:transparent!important}.base,.glow{display:none!important}")
        img_texto = so(".foto{visibility:hidden!important}svg{visibility:visible}")
        img_foto = so(".foto{visibility:visible!important}svg{visibility:hidden!important}")
        b.close()
    encosta(img_texto, img_foto, cfg)


def encosta(png_texto, png_foto, cfg, folga=4):
    import io
    from PIL import Image, ImageChops, ImageFilter
    t = Image.open(io.BytesIO(png_texto)).getchannel("A").point(lambda v: 255 if v > 200 else 0)   # só a letra, sem a sombra
    f = Image.open(io.BytesIO(png_foto)).getchannel("A").point(lambda v: 255 if v > 128 else 0)   # sem o halo do recorte
    caixa = f.getbbox()
    if not caixa or f.getextrema()[0] == 255:   # foto opaca ou ausente: não há como medir
        print("conferência do rosto: foto sem fundo transparente, confira no olho")
        return
    alto = f.crop((0, 0, 1600, caixa[1] + int((caixa[3] - caixa[1]) * 0.45)))   # cabeça e cabelo
    cabeca = Image.new("L", f.size, 0); cabeca.paste(alto, (0, 0))
    perto = t.filter(ImageFilter.MaxFilter(2 * folga + 1))                    # letras + folga de ~4 px
    sobre = ImageChops.multiply(perto, cabeca)
    toque_cab = sobre.getbbox()
    px = sobre.histogram()[255]
    if toque_cab and px < 150:   # só raspa a ponta do cabelo (fio solto): aceito, como no modelo aprovado
        print(f"conferência do rosto: a letra só raspa o contorno do cabelo ({px} px); aceito")
        toque_cab = None
    corpo = ImageChops.subtract(f, cabeca)
    toque_corpo = ImageChops.multiply(t, corpo).histogram()[255] >= 150
    if toque_cab:
        sys.exit(f"AVISO — capa não aprovada, a manchete encosta no rosto/cabelo do convidado (região x "
                 f"{toque_cab[0]}–{toque_cab[2]}, y {toque_cab[1]}–{toque_cab[3]}; {px} px). Aumente o recuo da foto "
                 f"(foto_right mais negativo, hoje {cfg.get('foto_right', -40)}), troque as quebras ou, se não houver "
                 f"jeito, reduza a manchete. A imagem foi salva só para conferência: não publique.")
    print("conferência do rosto: ok, nenhuma letra encosta no rosto nem no cabelo")
    if toque_corpo:
        print("atenção: o texto passa sobre o cabelo comprido ou o ombro, abaixo do rosto (aceito, como no modelo aprovado); confira a leitura")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
