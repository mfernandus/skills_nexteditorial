#!/usr/bin/env python3
"""Monta a página do artigo assinado da Retrospectiva 2026 (revista ES Brasil) no modelo do artigo do
Sidemar Acosta (ES 238, p. 28) e gera a prova.

Uso:
    python3 montar_artigo.py artigo.json PASTA_SAIDA

artigo.json:
{
  "pagina": 111,                         # número no espelho; null = "00" em rosa (lado: par = esquerda, ímpar = direita)
  "cartola": "Artigo",
  "autor": "Lourenzo de Oliveira",
  "cargo": "é superintendente estadual do Banco do Nordeste no Espírito Santo",
  "titulo": ["Crédito que transforma", "e impulsiona o", "Espírito Santo"],   # 1 a 3 linhas
  "texto": "texto.txt",                   # um parágrafo por linha; o primeiro abre com capitular
  "foto": "foto/lourenzo-de-oliveira-rgb.jpg",
  "credito": "Foto: Divulgação/BNB", "credito_pendente": true,
  "qr": "qr-artigo-lourenzo-de-oliveira.png",
  "qr_url": "https://nx-t.me/ART-LOURENZOO-ESB238",
  "pendencias": ["texto da etiqueta rosa (camada de prova)", ...]
}

Saída: artigo.html (página no contrato do exportador do InDesign), pagina.pdf (vetorial, 205 x 275 mm, limpa),
prova.pdf (a mesma página com as etiquetas rosa de pendência),
prova.png e encaixe.json (cabe? sobra ou falta, linhas vazias no fim da 2ª coluna, caracteres).

Geometria (pt) medida no modelo par e espelhada para a ímpar: a vinheta (aba rosa + retranca), o selo
Retrospectiva e o paginador trocam de lado; o miolo (foto, título, QR, texto) acompanha a margem da lombada
(17 mm) e do lado de fora (12 mm).
"""
from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
PX = 900 / 581.1024          # px por pt na prova (página de 900 px)
W_PT, H_PT = 581.1024, 779.5276
DESLOC_IMPAR = (17 - 12) * 72 / 25.4      # o miolo anda 14,17 pt na página ímpar (lombada à esquerda)
SANGRIA = 8.5039
CORPO_PX = 15.79     # Crimson Pro na prova, calibrada para ocupar a mesma largura da Minion Pro Cond 11 pt
CORPO_LS = -0.038    # espacejamento da prova (em): calibrado no artigo do Sidemar (3.433 caracteres em 60 linhas, igual ao InDesign)

# Modelo PAR (pt) — artigo do Sidemar Acosta, ES 238, p. 28
PAR = {
    "aba": (0.0, 17.0, 5.3, 15.9), "cartola_x": 28.3, "cartola_base": 29.4,
    "selo": (445.9, 17.9, 89.5, 13.7),
    "autor_dir": 538.6, "autor_base": 56.7, "cargo_base": 69.6,
    "foto": (34.0, 122.6, 112.6, 155.4), "raio": 3.9, "credito_x": 22.4,
    "titulo_x": 156.9, "titulo_base": 222.0, "titulo_lead": 25.75, "titulo_corpo": 28.0,
    "qr_moldura": (34.3, 300.4, 53.3, 53.4), "qr": (38.1, 304.3, 45.6), "qr_txt_x": 95.7, "qr_txt_base": 323.8,
    "texto": (34.0, 500.6), "texto_base": 394.0, "linhas": 30, "entrelinha": 11.7, "medianiz": 9.1,
    "esb_paginador": (500.9, 756.9, 36.7, 14.8),
}


def geo(lado: str) -> dict:
    g = dict(PAR)
    if lado == "esq":
        return g
    d = DESLOC_IMPAR
    x, y, w, h = PAR["aba"]; g["aba"] = (W_PT - x - w, y, w, h)
    g["cartola_dir"] = W_PT - PAR["cartola_x"]
    x, y, w, h = PAR["selo"]; g["selo"] = (W_PT - x - w, y, w, h)
    g["autor_dir"] = PAR["autor_dir"] + d
    x, y, w, h = PAR["foto"]; g["foto"] = (x + d, y, w, h)
    g["credito_x"] = PAR["credito_x"] + d
    g["titulo_x"] = PAR["titulo_x"] + d
    x, y, w, h = PAR["qr_moldura"]; g["qr_moldura"] = (x + d, y, w, h)
    x, y, w = PAR["qr"]; g["qr"] = (x + d, y, w)
    g["qr_txt_x"] = PAR["qr_txt_x"] + d
    x, w = PAR["texto"]; g["texto"] = (x + d, w)
    g["esb_paginador"] = (42.5, 756.9, 36.7, 14.8)          # página-mestre B, lado direito
    return g


def p(v: float) -> str:
    return f"{v * PX:.2f}px"


FIM_SVG = ("data:image/svg+xml;utf8," +
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 5.67 5.67'%3E%3Cpath fill='%23ED1C24' fill-rule='evenodd' "
           "d='M5.669 2.478V0H0V5.67H1.965V2.478H3.049L4.794 4.674V2.478Z M2.837 5.668V3.409L4.644 5.668Z'/%3E%3C/svg%3E")


def montar_html(cfg: dict, base: Path) -> str:
    num = cfg.get("pagina")
    lado = "esq" if (num is not None and num % 2 == 0) else "dir"
    g = geo(lado)
    e = html.escape
    paras = [l.strip() for l in (base / cfg["texto"]).read_text(encoding="utf8").splitlines() if l.strip()]
    corpo = []
    for i, t in enumerate(paras):
        cls = ' class="cap"' if i == 0 else ""
        fim = '<span class="fim"></span>' if i == len(paras) - 1 else ""
        corpo.append(f"<p{cls}>{e(t)}{fim}</p>")
    titulo = cfg["titulo"] if isinstance(cfg["titulo"], list) else [cfg["titulo"]]
    pn = f'<span class="pn">{num}</span>' if num else '<span class="pn tbd">00</span>'
    if lado == "esq":
        rodape = f'{pn}<span class="redes">revistaesbrasil • esbrasil • @esbrasil</span>'
        topo = (f'<span class="tag" style="left:{p(g["cartola_x"])}">{e(cfg.get("cartola", "Artigo").upper())}</span>')
    else:
        rodape = f'<span class="redes">radio.esbrasil.com.br</span>{pn}'
        topo = (f'<span class="tag dir" style="right:{p(W_PT - g["cartola_dir"])}">{e(cfg.get("cartola", "Artigo").upper())}</span>')
    ax, ay, aw, ah = g["aba"]
    if lado == "esq":
        aba = f'left:{p(-SANGRIA)};width:{p(aw + SANGRIA)}'
    else:
        aba = f'left:{p(ax)};width:{p(aw + SANGRIA)}'
    sx, sy, sw, sh = g["selo"]
    fx, fy, fw, fh = g["foto"]
    mx, my, mw, mh = g["qr_moldura"]
    qx, qy, qw = g["qr"]
    tx, tw = g["texto"]
    lin = cfg.get("entrelinha_pt", g["entrelinha"]) * PX
    g["linhas"] = cfg.get("linhas", g["linhas"])
    corpo_px = cfg.get("corpo_px", CORPO_PX)
    corpo_ls = cfg.get("corpo_ls", CORPO_LS)
    ex, ey, ew, eh = g["esb_paginador"]
    cred_cls = "cr tbd" if cfg.get("credito_pendente") else "cr"
    pend = "".join(f'<span class="busca" style="left:{p(b.get("x", fx))};top:{p(b.get("y", 90))};max-width:{p(b.get("w", 200))}"><b>Pendência</b>{e(b["texto"])}</span>'
                   for b in cfg.get("etiquetas", []))
    autor = e(cfg["autor"].upper())
    css_fontes = (KIT / "assets" / "fontes" / "crimson-pro.css").read_text(encoding="utf8")
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Retrospectiva 2026 · Artigo · {e(cfg["autor"])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,700;1,400&display=swap">
<style>
{css_fontes}
:root{{--serif:"Crimson Pro","Minion Pro",Georgia,serif;--sans:"Inter",system-ui,sans-serif;--tinta:#404041;--azul:#00427B;--rosa:#E01E70}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:#E6E9EE;font-family:var(--sans)}}
.wrap{{padding:24px 0 48px;display:flex;flex-direction:column;align-items:center;gap:12px}}
.note{{width:900px;background:#FFF6DA;border:1px solid #E8C766;color:#4A3A06;border-radius:8px;padding:10px 14px;font-size:13px;line-height:1.5}}
.pagebox{{position:relative;width:900px;height:1207px;overflow:hidden;box-shadow:0 14px 40px rgba(0,28,67,.14)}}
.page{{position:absolute;left:0;top:0;width:900px;height:1207px;background:#fff;color:var(--tinta)}}
.page > *{{position:absolute;margin:0}}
.aba{{top:{p(ay)};height:{p(ah)};{aba};background:#EC018C}}
.tag{{top:{p(g["cartola_base"] - 12)};font-family:var(--sans);font-weight:900;font-size:{p(12)};line-height:{p(12)};letter-spacing:-.02em;color:var(--azul);white-space:nowrap}}
.tag.dir{{text-align:right}}
img.selo{{left:{p(sx)};top:{p(sy)};width:{p(sw)};height:{p(sh)}}}
.autor{{right:{p(W_PT - g["autor_dir"])};top:0;font-weight:900;font-size:{p(12)};line-height:{p(13)};letter-spacing:-.025em;text-align:right;white-space:nowrap}}
.cargo{{right:{p(W_PT - g["autor_dir"])};top:0;font-weight:300;font-size:{p(10)};line-height:{p(12)};letter-spacing:-.01em;text-align:right;white-space:nowrap}}
figure.ph{{left:{p(fx)};top:{p(fy)};width:{p(fw)};height:{p(fh)};overflow:visible}}
figure.ph > img{{display:block;width:100%;height:100%;object-fit:cover;border-radius:{p(g["raio"])}}}
.ph .cr{{position:absolute;left:{p(g["credito_x"] - fx)};top:0;writing-mode:vertical-rl;transform:rotate(180deg);font-weight:300;font-size:{p(7)};line-height:{p(9.3)};letter-spacing:-.01em;white-space:nowrap;color:var(--tinta)}}
.titulo-artigo{{left:{p(g["titulo_x"])};top:0;width:{p(tx + tw - g["titulo_x"])};font-weight:900;font-size:{p(g["titulo_corpo"])};line-height:{p(g["titulo_lead"])};letter-spacing:-.025em;color:var(--tinta)}}
.qrbox{{left:{p(mx)};top:{p(my)};width:{p(mw)};height:{p(mh)};border:{p(0.5)} solid #231F20}}
.qr{{left:{p(qx)};top:{p(qy)};width:{p(qw)};height:{p(qw)}}}
.qr img{{display:block;width:100%;height:100%}}
.qrtxt{{left:{p(g["qr_txt_x"])};top:0;font-weight:400;font-size:{p(9.5)};line-height:{p(10)};letter-spacing:-.025em;color:var(--tinta)}}
.flow{{left:{p(tx)};top:0;width:{p(tw)};height:{lin * g["linhas"] + 1:.2f}px;column-count:2;column-gap:{p(g["medianiz"])};column-fill:auto;
  font-family:var(--serif);font-size:{corpo_px}px;letter-spacing:{corpo_ls}em;line-height:{lin:.3f}px;color:var(--tinta);text-align:justify;hyphens:auto;overflow:hidden}}
.flow p{{margin:0;text-indent:13.17px}}
.flow p.cont,.flow p.cap{{text-indent:0}}
.flow p.cap::first-letter{{float:left;font-family:var(--sans);font-weight:900;font-size:66px;line-height:46px;color:var(--tinta);margin:5px 6px 0 -2px}}
.flow .fim{{display:inline-block;width:{p(5.67)};height:{p(5.67)};margin-left:{p(3)};background:url("{FIM_SVG}") no-repeat center/contain;vertical-align:baseline}}
.flow .tbd,.tbd{{color:var(--rosa)!important}}
.foot{{top:1170px;height:16px;display:flex;align-items:center;gap:7px;font-family:var(--sans);font-size:10.84px;font-weight:900;letter-spacing:-.025em;color:#58595B}}
.page.esq .foot{{left:42.9px;justify-content:flex-start}}
.page.dir .foot{{right:41.8px;justify-content:flex-end}}
.foot .pn{{font-size:12.39px;font-weight:700;color:#E3061E}}
.foot .redes{{display:inline-block;transform:scaleX(.85);transform-origin:right center}}
img.esb-pag{{left:{p(ex)};top:{p(ey)};width:{p(ew)};height:{p(eh)}}}
.busca{{z-index:5;background:#FFE3EF;border:1.5px solid var(--rosa);color:#7A0B3A;font-size:10.5px;line-height:1.3;padding:5px 7px;border-radius:5px}}
.busca b{{display:block;font-size:9.5px;color:var(--rosa);margin-bottom:2px}}
#ocupacao.excede{{color:#C0182F}} #ocupacao.cabe{{color:#0F7A3F}}
@media print{{@page{{size:205mm 275mm;margin:0}} html,body{{background:#fff}} .wrap{{display:block;padding:0}} .note{{display:none}} .pagebox{{box-shadow:none;margin:0}} body.limpa .busca{{display:none}} body.limpa .tbd{{color:var(--tinta)!important}}}}
</style></head><body>
<div class="wrap" lang="pt-BR"><div class="note"><b>Retrospectiva 2026 · artigo · {e(cfg["autor"])}</b> · página {num if num else "<span class='tbd'>00</span>"} ({"ímpar, vinheta à direita" if lado == "dir" else "par, vinheta à esquerda"}) · modelo: artigo do Sidemar Acosta (ES 238, p. 28). Texto corrido em Minion Pro Cond 11/12 no InDesign (na prova, Crimson Pro calibrada). Rosa = pendência. <b id="ocupacao">Calculando encaixe…</b></div>
<div class="pagebox"><article class="page {lado}" data-lado="{lado}">
  <div class="aba so-aba" aria-hidden="true"></div>
  {topo}
  <img class="selo" src="selo-retrospectiva-artigo.png" alt="Retrospectiva">
  <p class="autor by-artigo" data-base="{g["autor_base"] * PX:.2f}">{autor}</p>
  <p class="cargo" data-base="{g["cargo_base"] * PX:.2f}">{e(cfg["cargo"])}</p>
  <figure class="ph"><img src="{e(cfg["foto"])}" alt="Retrato de {e(cfg["autor"])}"><span class="{cred_cls}">{e(cfg["credito"])}</span></figure>
  <h2 class="titulo-artigo" data-base="{g["titulo_base"] * PX:.2f}">{"<br>".join(e(t) for t in titulo)}</h2>
  <div class="qrbox"></div>
  <div class="qr"><img src="{e(cfg["qr"])}" alt="QR Code para o artigo"></div>
  <p class="qrtxt" data-base="{g["qr_txt_base"] * PX:.2f}">Acesse o<br>QR Code e leia<br>a matéria em<br>esbrasil.com.br</p>
  <div class="flow c2" data-flow="1" data-base="{g["texto_base"] * PX:.2f}"></div>
  <img class="esb-pag so-prova" src="esb-paginador.png" alt="">
  <footer class="foot">{rodape}</footer>
  {pend}
</article></div></div>
<template id="texto">{"".join(corpo)}</template>
<script>
document.fonts.ready.then(() => {{
  // 1. texto corrido flui na caixa de 2 colunas
  const src = document.getElementById('texto');
  const boxes = [...document.querySelectorAll('.flow')].sort((a, b) => a.dataset.flow - b.dataset.flow);
  const blocks = [...src.content.children].map(n => n.cloneNode(true));
  const over = el => el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1;
  const toks = p => {{ const t = []; let prevSpace = true; p.childNodes.forEach(n => {{ if (n.classList && n.classList.contains('fim')) return;
    const txt = n.textContent || ''; const c = n.nodeType === 3 ? '' : (n.className || ''); txt.split(' ').forEach((w, k) => {{ if (w === '') return;
    t.push({{ w, c, g: (k === 0 && !prevSpace && t.length > 0) }}); }}); prevSpace = / $/.test(txt); }}); return t; }};
  const htm = ts => {{ let h = '', cur = null; for (const k of ts) {{ const e = k.w.replace(/&/g, '&amp;').replace(/</g, '&lt;'); const sp = (h && !k.g) ? ' ' : '';
    if (k.c !== cur) {{ if (cur) h += '</span>'; h += sp; if (k.c) h += '<span class="' + k.c + '">'; cur = k.c; h += e; }} else {{ h += sp + e; }} }} if (cur) h += '</span>'; return h; }};
  const fitWords = (box, p) => {{ const T = toks(p); let lo = 0, hi = T.length; const part = p.cloneNode(false); box.appendChild(part);
    while (lo < hi) {{ const mid = Math.ceil((lo + hi) / 2); part.innerHTML = htm(T.slice(0, mid)); if (over(box)) hi = mid - 1; else lo = mid; }}
    if (lo < 2) {{ box.removeChild(part); return null; }}
    part.innerHTML = htm(T.slice(0, lo)); const rest = p.cloneNode(false); rest.classList.add('cont'); rest.classList.remove('cap');
    rest.innerHTML = htm(T.slice(lo)); if (p.querySelector('.fim')) rest.insertAdjacentHTML('beforeend', '<span class="fim"></span>'); return rest; }};
  let i = 0;
  for (const box of boxes) {{
    box.innerHTML = '';
    while (i < blocks.length) {{ const b = blocks[i]; box.appendChild(b); if (!over(box)) {{ i++; continue; }} box.removeChild(b);
      if (b.tagName === 'P') {{ const rest = fitWords(box, b); if (rest) blocks[i] = rest; }} break; }}
  }}
  // 2. linhas de base nos lugares do modelo
  const probe = el => {{ const s = document.createElement('span'); s.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
    const alvo = el.querySelector('p') || el; alvo.insertBefore(s, alvo.firstChild); const y = s.getBoundingClientRect().top; s.remove(); return y; }};
  const pg = document.querySelector('article.page').getBoundingClientRect();
  for (const el of document.querySelectorAll('[data-base]')) {{
    const atual = probe(el) - pg.top; const alvo = parseFloat(el.dataset.base);
    el.style.top = (parseFloat(getComputedStyle(el).top) + alvo - atual) + 'px';
  }}
  // 3. encaixe: sobra de texto ou linhas vazias no fim da 2ª coluna
  const box = boxes[0]; const restante = blocks.slice(i).reduce((s, n) => s + n.textContent.length, 0);
  const r = box.getBoundingClientRect(); const lh = parseFloat(getComputedStyle(box).lineHeight);
  const rg = document.createRange(); const ult = box.lastElementChild; rg.selectNodeContents(ult);
  const rects = [...rg.getClientRects()].filter(q => q.width > 0); const fimL = rects[rects.length - 1];
  const vazias = fimL && fimL.left > r.left + r.width / 2 ? Math.floor((r.bottom - fimL.bottom) / lh + 0.05) : null;
  const chars = blocks.reduce((s, n) => s + n.textContent.length, 0) + blocks.length - 1;
  window.__encaixe = {{ cabe: restante === 0, sobra_caracteres: restante, linhas_vazias_no_fim: vazias, caracteres: chars,
                        linhas_por_coluna: Math.round(r.height / lh) }};
  const info = document.getElementById('ocupacao');
  info.textContent = restante > 0 ? `Texto excede a página em cerca de ${{restante.toLocaleString('pt-BR')}} caracteres.`
    : (vazias === null ? 'Texto não chega à 2ª coluna.' : `Texto cabe (${{chars.toLocaleString('pt-BR')}} caracteres); ${{vazias}} linha(s) vazia(s) no fim da 2ª coluna.`);
  info.className = restante > 0 ? 'excede' : 'cabe';
  document.body.dataset.pronto = '1';
}});
</script></body></html>"""


def main():
    cfg_path, saida = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf8"))
    base = cfg_path.parent
    saida.mkdir(parents=True, exist_ok=True)
    for f in ("selo-retrospectiva-artigo.png", "esb-paginador.png"):
        shutil.copy(KIT / "assets" / f, saida / f)
    (saida / "fontes").mkdir(exist_ok=True)
    for f in (KIT / "assets" / "fontes").glob("*.woff2"):
        shutil.copy(f, saida / "fontes" / f.name)
    for k in ("foto", "qr", "texto"):
        src = base / cfg[k]
        dst = saida / cfg[k]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dst.resolve():
            shutil.copy(src, dst)
    html_txt = montar_html(cfg, saida)
    (saida / "artigo.html").write_text(html_txt, encoding="utf8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 960, "height": 1400}, device_scale_factor=2)
        pg.goto((saida / "artigo.html").as_uri(), wait_until="networkidle")
        pg.wait_for_selector("body[data-pronto='1']", timeout=30000)
        enc = pg.evaluate("window.__encaixe")
        pg.locator("article.page").screenshot(path=str(saida / "prova.png"))
        pg.emulate_media(media="print")
        opts = dict(width="205mm", height="275mm", print_background=True, scale=774.8 / 900,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, page_ranges="1")
        pg.pdf(path=str(saida / "prova.pdf"), **opts)                     # com as etiquetas de pendência
        pg.evaluate("document.body.classList.add('limpa')")
        pg.pdf(path=str(saida / "pagina.pdf"), **opts)                    # página limpa

        br.close()
    (saida / "encaixe.json").write_text(json.dumps(enc, ensure_ascii=False, indent=1), encoding="utf8")
    print(json.dumps(enc, ensure_ascii=False))


if __name__ == "__main__":
    main()
