# monta folhas com as 12 melhores candidatas (diversas) de cada local, para escolha visual
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
exec(open('selecionar.py').read().split('escolha = {}')[0])   # reaproveita filtros, métricas e notas
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
top = {}
for tid, lst in cand.items():
    ranked = sorted(lst, key=lambda x: -nota(M[x[0]['id']], x[0]))
    sel = []
    for i, d in ranked:
        m = M[i['id']]
        if 'erro' in m: continue
        if (i.get('width') or 1) / (i.get('height') or 1) > 2.3: continue
        if any(hamming(m['ahash'], M[s['id']]['ahash']) <= 70 for s in sel): continue
        sel.append(i)
        if len(sel) == 12: break
    top[tid] = [s['id'] for s in sel]
json.dump(top, open('top12.json', 'w'))
ids = [t for t in top if top[t]]
W, H = 200, 118
for s in range(0, len(ids), 2):
    g = ids[s:s+2]
    sheet = Image.new('RGB', (6 * W + 10, len(g) * (2 * H + 24) + 4), 'white'); dr = ImageDraw.Draw(sheet)
    for r, tid in enumerate(g):
        y0 = r * (2 * H + 24)
        dr.text((4, y0 + 2), f"{tid} {alvo[int(tid)]['title'][:70]}", fill='black', font=font)
        for k, pid in enumerate(top[tid]):
            im = Image.open('cache/' + pid + '.img').convert('RGB'); im.thumbnail((W - 4, H - 4))
            x = (k % 6) * W + 4; y = y0 + 18 + (k // 6) * H
            sheet.paste(im, (x, y)); dr.rectangle((x, y, x + 22, y + 14), fill='black'); dr.text((x + 3, y + 1), str(k + 1), fill='yellow', font=font)
    sheet.save(f'rev_{s//2+1}.jpg', quality=78)
    print(f'rev_{s//2+1}.jpg', g)
