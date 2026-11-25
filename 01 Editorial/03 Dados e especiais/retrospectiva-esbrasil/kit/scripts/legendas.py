"""Legendas sobre foto no padrão ES Brasil (Roboto Condensed 8,5/10, corrigido em 23/11/2026: era Roboto, não Myriad; sem fundo, tracking levemente apertado), sempre
num dos quatro cantos da foto, com a margem padrão (22 px dos lados, 20 px de cima ou de baixo), no canto que a foto
permite: o mais liso e com mais contraste. Branco ou preto pelo fundo; bold e sombra só quando o contraste não basta.
data-leg="x0,y0,x1,y1" (frações) na <figure> limita os cantos permitidos, para não cobrir rosto nem o assunto.
A etiqueta "Buscar original", só da prova, sai do caminho.
Uso, na pasta do capítulo: python3 montar.py && python3 legendas.py [capitulo.html] && python3 montar.py (grava as classes no corpo.html)."""
import asyncio, re, io, sys, pathlib
import numpy as np
from playwright.async_api import async_playwright
from PIL import Image

POS = ["bl", "br", "tl", "tr"]
MX, MY = 22, 20

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 940, 'height': 1300})
        await pg.goto(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'capitulo.html').resolve().as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(1500)
        info = await pg.evaluate('''()=>[...document.querySelectorAll('.ph .leg')].map(l=>{const f=l.closest('.ph');l.removeAttribute('style');l.className='leg';
            const r=l.getBoundingClientRect(),fr=f.getBoundingClientRect();return {w:Math.ceil(r.width),h:Math.ceil(r.height),
            fx:fr.left+scrollX,fy:fr.top+scrollY,fw:fr.width,fh:fr.height,zona:f.dataset.leg||''}})''')
        await pg.evaluate("document.querySelectorAll('.ph .leg,.ph .busca,.ph .cr').forEach(e=>e.style.visibility='hidden')")
        res = []
        for it in info:
            shot = await pg.screenshot(full_page=True, clip={'x': it['fx'], 'y': it['fy'], 'width': it['fw'], 'height': it['fh']})
            g = np.asarray(Image.open(io.BytesIO(shot)).convert('L').resize((round(it['fw']), round(it['fh'])))).astype(np.float64) / 255
            W, H = g.shape[1], g.shape[0]; w, h = it['w'], it['h']
            z = tuple(map(float, it['zona'].split(','))) if it['zona'] else (0, 0, 1, 1)
            best = None
            for pos in POS:
                x = MX if pos[1] == 'l' else W - MX - w
                y = MY if pos[0] == 't' else H - MY - h
                if x < z[0] * W - 1 or x + w > z[2] * W + 1 or y < z[1] * H - 1 or y + h > z[3] * H + 1:
                    continue
                q = g[y - 4:y + h + 4, x - 4:x + w + 4]
                m, sd = q.mean(), q.std()
                for cor, c in (("branca", 1 - m), ("preta", m)):
                    sc = c - 1.6 * sd
                    if best is None or sc > best[0]:
                        best = (sc, pos, cor, m, sd, c)
            if best is None:   # nenhum canto cabe na zona pedida: usa os quatro cantos
                it['zona'] = ''
                z = (0, 0, 1, 1)
                for pos in POS:
                    x = MX if pos[1] == 'l' else W - MX - w; y = MY if pos[0] == 't' else H - MY - h
                    q = g[y - 4:y + h + 4, x - 4:x + w + 4]; m, sd = q.mean(), q.std()
                    for cor, c in (("branca", 1 - m), ("preta", m)):
                        sc = c - 1.6 * sd
                        if best is None or sc > best[0]: best = (sc, pos, cor, m, sd, c)
            sc, pos, cor, m, sd, c = best
            sombra = c < 0.62 or sd > 0.15
            res.append(dict(pos=pos, cor=cor, sombra=bool(sombra), forte=bool(sombra and sd > 0.17), m=round(float(m), 2), sd=round(float(sd), 2)))
        await b.close()
    s = open('corpo.html', encoding='utf-8').read(); k = iter(res)
    def troca(mm):
        r = next(k)
        cls = 'leg' + ('' if r['pos'] == 'bl' else ' pos-' + r['pos']) + (' preta' if r['cor'] == 'preta' else '') + (' forte' if r['forte'] else '') + (' sombra' if r['sombra'] else '')
        return f'<span class="{cls}">'
    s = re.sub(r'<span class="leg[^"]*"(?: style="[^"]*")?(?: data-busca="[^"]*")?>', troca, s)
    def busca(fig):
        f = fig.group(0).replace('<span class="busca esq">', '<span class="busca">')
        if re.search(r'<span class="leg[^"]*pos-tr', f):
            f = f.replace('<span class="busca">', '<span class="busca esq">')
        return f
    s = re.sub(r'<figure class="ph[^"]*"[^>]*>.*?</figure>', busca, s, flags=re.S)
    open('corpo.html', 'w', encoding='utf-8').write(s)
    for r in res: print(r)
asyncio.run(main())
