# Seleciona fotos do NX Fotos para pontos turísticos e "o que fazer" do mapas (Destinos ES).
# Entrada: buscas.json (resultados do NX Fotos), ../mapas/alvo.json e ../mapas/base.json.
# Saída: escolha.json (até 4 fotos por local, com crédito, legenda, alt e intensidade de tratamento).
import json, os, re, math, unicodedata, concurrent.futures as cf, urllib.request, io
from PIL import Image, ImageFilter, ImageStat
import numpy as np

CACHE = 'cache'; os.makedirs(CACHE, exist_ok=True)

def norm(s):
    s = unicodedata.normalize('NFKD', (s or '').lower())
    return ''.join(c for c in s if not unicodedata.combining(c))

# regras por local: qualquer um dos grupos "todos" (cada grupo exige todas as palavras), menos as exclusões
REGRAS = {
    2562: dict(todos=[['guriri']], nao=['tamar']),                                   # Guriri
    4956: dict(todos=[['barra nova']], nao=['petroleo', 'bomba', 'orelhao', 'restaurante', 'guriri']),  # Barra Nova
    931:  dict(todos=[['centro historico de porto'], ['porto', 'sao mateus', 'aerea'], ['casar', 'porto'], ['porto de sao mateus'], ['sitio historico']],
               nao=['ruina', 'pichac', 'vazia', 'rua larga']),                                   # Sítio Histórico
    913:  dict(todos=[['igreja velha']], nao=[]),                                     # Igreja Velha
    7877: dict(todos=[['rio cricare']], nao=['placa', 'capela']),                                           # Rio Cricaré
    3670: dict(todos=[['urussuquara']], nao=[]),                                      # Urussuquara
    4678: dict(todos=[['regencia', 'praia'], ['regencia', 'foz'], ['regencia', 'mar ']], nao=['tamar', 'farol', 'escultura', 'comboios']),  # Praia de Regência
    6066: dict(todos=[['regencia', 'vila'], ['regencia', 'rua'], ['regencia', 'igreja']], nao=['tamar', 'comboios']),  # Vila de Regência
    6785: dict(todos=[['regencia', 'surf']], nao=[]),                                 # Reserva Nacional de Surf
    814:  dict(todos=[['farol', 'regencia']], nao=[]),                                # Farol de Regência
    901:  dict(todos=[['projeto tamar', 'regencia']], nao=[]),                        # Projeto Tamar Regência
    2556: dict(todos=[['pontal do ipiranga']], nao=[]),                               # Pontal do Ipiranga
    3669: dict(todos=[['povoacao']], nao=[]),                                         # Praia de Povoação
    804:  dict(todos=[['degredo', 'comunidade'], ['degredo', 'quilomb'], ['degredo', 'casa'], ['degredo', 'vila']], nao=[]),
    803:  dict(todos=[['degredo', 'praia'], ['degredo', 'restinga'], ['degredo', 'litoral'], ['degredo', 'mar ']], nao=[]),
    896:  dict(todos=[['barra seca']], nao=[]),                                       # Barra Seca
    3667: dict(todos=[['juparan']], nao=[]),                                          # Lagoa Juparanã
    827:  dict(todos=[['lagoa nova'], ['lagoa_nova']], nao=[]),                       # Lagoa Nova
    805:  dict(todos=[['reserva natural vale'], ['reserva', 'vale', 'linhares']], nao=[]),  # Reserva Natural Vale
    903:  dict(todos=[['comboios']], nao=[]),                                         # Rebio Comboios
}
RAIO_KM = 8.0      # foto com GPS mais longe que isso do local não entra
MAX_NOVAS = 4

alvo = {a['id']: a for a in json.load(open('../mapas/alvo.json'))}
base = {b['id']: b for b in json.load(open('../mapas/base.json'))}
db = json.load(open('buscas.json'))

pool = {}
for lab, v in db.items():
    for i in v['itens']:
        pool.setdefault(i['id'], i)
print('candidatos únicos no NX Fotos:', len(pool))

def texto(i):
    t = ' '.join([i.get('title') or '', i.get('description') or '', ' '.join(i.get('tags') or [])])
    ed = i.get('editable') or {}
    t += ' ' + (ed.get('location') or '')
    return ' ' + norm(t).replace('-', ' ').replace('_', ' ') + ' '

def dist_km(a, b, c, d):
    r = 6371; p = math.pi / 180
    x = (c - a) * p; y = (d - b) * p
    h = math.sin(x / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin(y / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def thumb_url(i):
    s = i.get('src') or {}
    return s.get('small') or s.get('thumb') or (i.get('url') or '').replace('@w1600', '@w400')

def baixar(url, nome):
    p = os.path.join(CACHE, nome)
    if not os.path.exists(p):
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'nx-script'}), timeout=60) as r:
            open(p, 'wb').write(r.read())
    return p

def metricas(path):
    im = Image.open(path).convert('RGB'); im.thumbnail((400, 400))
    a = np.asarray(im).astype(np.float32) / 255.0
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    L = 0.299 * R + 0.587 * G + 0.114 * B
    rg = R - G; yb = 0.5 * (R + G) - B
    colorido = (np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)) * 100
    g = np.asarray(im.convert('L').filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    nitidez = float(g.var())
    clip = float(((L < 0.02) | (L > 0.98)).mean())
    mx = a.max(-1); mn = a.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    small = im.convert('L').resize((16, 16)); px = np.asarray(small).astype(np.float32)
    ahash = (px > px.mean()).flatten()
    return dict(colorido=float(colorido), contraste=float(L.std()), luz=float(L.mean()), nitidez=nitidez,
                clip=clip, sat=float(sat.mean()), ahash=ahash.astype(int).tolist())

def hamming(a, b):
    return int(np.sum(np.array(a) != np.array(b)))

# 1) candidatos por local
cand = {}
for tid, regra in REGRAS.items():
    t = alvo[tid]; lat, lng = float(t['lat']), float(t['lng'])
    lst = []
    for i in pool.values():
        if (i.get('type') or 'foto') != 'foto' or i.get('orient') != 'h': continue
        if (i.get('width') or 0) < 1600: continue
        if i.get('visibilidade') == 'oculta' or i.get('license') not in (None, 'rf'): continue
        tx = texto(i)
        if not any(all(w in tx for w in grupo) for grupo in regra['todos']): continue
        if any(w in tx for w in regra['nao']): continue
        ex = i.get('exif') or {}
        d = None
        if ex.get('lat') and ex.get('lng'):
            d = dist_km(lat, lng, ex['lat'], ex['lng'])
            if d > RAIO_KM: continue
        lst.append((i, d))
    cand[tid] = lst
    print(f"{tid} {t['title'][:40]}: {len(lst)} candidatas")

# 2) miniaturas e métricas
todas = {i['id']: i for lst in cand.values() for i, _ in lst}
def proc(i):
    try:
        p = baixar(thumb_url(i), i['id'] + '.img')
        return i['id'], metricas(p)
    except Exception as e:
        return i['id'], {'erro': str(e)}
with cf.ThreadPoolExecutor(12) as ex:
    M = dict(ex.map(proc, todas.values()))
json.dump(M, open('metricas.json', 'w'))

# 3) fotos que o local já tem (para não repetir)
def hashes_existentes(tid):
    hs = []
    for im in (base[tid].get('images_collection') or []):
        try:
            p = baixar(im['url'], f"ex_{tid}_{im['id']}.img")
            hs.append(metricas(p)['ahash'])
        except Exception:
            pass
    return hs

def nota(m, i):
    if 'erro' in m: return -1
    s = 0
    s += min(m['colorido'], 60) / 60 * 3.0          # cor viva (foto tratada)
    s += min(m['contraste'], 0.28) / 0.28 * 1.5      # contraste
    s += min(m['nitidez'], 2500) / 2500 * 2.0        # nitidez
    s -= abs(m['luz'] - 0.48) * 3.0                  # exposição
    s -= m['clip'] * 6                               # estouro / empastado
    s += 0.6 if (i.get('width') or 0) >= 4000 else 0
    s += 0.4 if i.get('author') else 0
    s += 0.3 if (i.get('description') or '').strip() else 0
    return round(s, 3)

def intensidade(m):
    # foto crua (pouca cor e pouco contraste) recebe o tratamento da casa; foto viva fica como está
    if m['colorido'] >= 34 and m['contraste'] >= 0.18: return 0
    if m['colorido'] < 22: return 0.8
    return 0.6

escolha = {}
for tid, lst in cand.items():
    if not lst: continue
    ex_h = hashes_existentes(tid)
    ranked = sorted(lst, key=lambda x: -nota(M[x[0]['id']], x[0]))
    sel = []
    for i, d in ranked:
        m = M[i['id']]
        if 'erro' in m or nota(m, i) < 2.0: continue
        if any(hamming(m['ahash'], h) <= 20 for h in ex_h): continue      # já existe no local
        if any(hamming(m['ahash'], M[s['id']]['ahash']) <= 60 for s in sel): continue  # parecida demais com outra escolhida
        sel.append(i)
        if len(sel) == MAX_NOVAS: break
    t = alvo[tid]
    mun = 'São Mateus' if t['mun'] == 'SM' else 'Linhares'
    escolha[tid] = dict(titulo=t['title'], municipio=mun, main_atual=t['main'], fotos=[dict(
        id=i['id'], url=(i.get('src') or {}).get('large') or i.get('url'), thumb=thumb_url(i),
        autoria=i.get('author') or 'Acervo NX Fotos', legenda=(i.get('description') or i.get('title') or '').split('\n')[0].strip()[:240],
        alt=f"{t['title']} — {mun} (ES)", largura=i.get('width'), altura=i.get('height'),
        nota=nota(M[i['id']], i), k=intensidade(M[i['id']]),
        colorido=round(M[i['id']]['colorido'], 1), contraste=round(M[i['id']]['contraste'], 3)) for i in sel])
json.dump(escolha, open('escolha.json', 'w'), ensure_ascii=False, indent=1)
for tid, e in escolha.items():
    print(tid, e['titulo'][:35], '→', len(e['fotos']), 'fotos |', [(f['autoria'][:14], f['nota'], f['k']) for f in e['fotos']])
