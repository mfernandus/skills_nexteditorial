---
name: "validacao-diaria-datafe"
description: "Validação diária dos números do Datafé (datafe.com.br): confere o banco, uma amostra de municípios contra o IBGE (SIDRA) e o site publicado, e acusa igreja escondida, soma errada, dado vencido e erro de texto. Só lê."
---

# Validação diária do Datafé

Rodada diária de conferência do Datafé, o portal de dados sobre os evangélicos da Revista Comunhão (datafe.com.br). Nasceu em 17/11/2026, quando Mário viu que a Igreja Cristã Maranata não aparecia em Vitória: a estimativa de igrejas de 2022 só separava seis igrejas nacionais e escondia em "outras" as igrejas grandes de cada região.

Regras:
- A skill SÓ LÊ. Nunca grava no banco, nunca manda mensagem ao Lovable, nunca publica. Toda correção é proposta e só é feita com o ok de Mário Fernando, numa conversa.
- Não criar token, não contornar trava de permissão, não raspar sites que recusem leitura (g1, Veja, UOL).
- Responder em português do Brasil, sem caixa alta em títulos e rótulos.

## Onde estão os dados

- Projeto Lovable "Evangélicos BR em Números" (workspace Mario2), project_id `bd496ff6-6711-470b-aef0-fc1c2b6a611e`. Usar `mcp__Lovable__query_database` só com SELECT.
- Leitura pública pelo Supabase (o script usa): `https://mvxzozxjzbrzndaunlxj.supabase.co`, com a chave publicável que está no script.
- Site publicado: https://datafe.com.br. O HTML pré-renderizado de cada página traz no título e no texto o percentual e o número de evangélicos (é o que o script confere).
- IBGE: `https://apisidra.ibge.gov.br/values/...` (tabela 10183 para 2022, 10 anos ou mais, classificação c133 de religião; tabela 137 para 2010, igrejas, todas as idades). O terminal alcança o SIDRA; o servicodados.ibge.gov.br recusa leitura automática.
- Tabelas: `religiao_censo`, `denominacoes_2010`, `denominacoes_2022_estimativa` (13 grupos por território desde 17/11/2026), `modelo_parametros`, `templos`, `mv_templos_municipio`, `v_municipio_religiao`, `materias_home`, `municipios`, `ufs`.

## Passo 1: painel de checagens no banco

Rodar o SQL abaixo inteiro, numa chamada só, com `mcp__Lovable__query_database`. Ele devolve 15 linhas: checagem, status (ok, erro ou alerta) e detalhe.

```sql
with
rc as (select nivel, codigo_ibge, ano, base, populacao, evangelicos, pct_evangelicos from religiao_censo where faixa_idade = 'total'),
rc_m as (select (codigo_ibge / 100000) uf, ano, base, sum(populacao) pop, sum(evangelicos) ev from rc where nivel = 'municipio' group by 1, 2, 3),
rc_u as (select ano, base, sum(populacao) pop, sum(evangelicos) ev from rc where nivel = 'uf' group by 1, 2),
c1 as (select count(*) n, string_agg(u.codigo_ibge || ' ' || u.ano || ' ' || u.base, '; ') ex from rc u join rc_m m on m.uf = u.codigo_ibge and m.ano = u.ano and m.base = u.base
  where u.nivel = 'uf' and (abs(m.pop - u.populacao) > 0.0001 * u.populacao or abs(m.ev - u.evangelicos) > 0.0001 * u.evangelicos)),
c2 as (select count(*) n, string_agg(b.ano || ' ' || b.base, '; ') ex from rc b join rc_u u on u.ano = b.ano and u.base = b.base
  where b.nivel = 'brasil' and (abs(u.pop - b.populacao) > 0.0001 * b.populacao or abs(u.ev - b.evangelicos) > 0.0001 * b.evangelicos)),
c3 as (select count(*) n, string_agg(codigo_ibge || ' ' || ano, '; ') filter (where rn <= 5) ex from (select *, row_number() over () rn from rc where populacao > 0 and abs(pct_evangelicos - 100.0 * evangelicos / populacao) > 0.01) x),
c3b as (select count(*) n, string_agg(codigo_ibge::text, ', ') ex from rc where nivel = 'municipio' and ano = 2022 and coalesce(populacao, 0) = 0),
c4 as (select count(*) n, string_agg(p.codigo::text, '; ') filter (where rn <= 5) ex from (select p.*, row_number() over () rn from modelo_parametros p join rc r on r.nivel = p.tipo and r.codigo_ibge = p.codigo and r.ano = 2022 and r.base = '10_anos_ou_mais'
  where p.tipo = 'municipio' and abs(p.ev_2022 - 100.0 * r.evangelicos / nullif(r.populacao, 0)) > 0.01) p),
est as (select tipo, codigo, sum(central) soma, count(*) grupos, count(*) filter (where not (baixo <= central and central <= alto) or baixo < 0) faixa_ruim from denominacoes_2022_estimativa group by 1, 2),
c5 as (select count(*) n, string_agg(e.codigo || ' (' || e.soma || ' x ' || r.evangelicos || ')', '; ') filter (where rn <= 5) ex from (select e.*, row_number() over () rn from est e) e
  join rc r on r.nivel = e.tipo and r.codigo_ibge = e.codigo and r.ano = 2022 and r.base = '10_anos_ou_mais' where e.tipo = 'municipio' and abs(e.soma - r.evangelicos) > 15),
c6 as (select sum(faixa_ruim) n, count(*) filter (where grupos <> (select grupos from est where tipo = 'brasil')) grupos_diferentes, (select grupos from est where tipo = 'brasil') grupos_brasil from est),
c6b as (select count(*) n from municipios m where not exists (select 1 from denominacoes_2022_estimativa e where e.tipo = 'municipio' and e.codigo = m.codigo_ibge)),
c7 as (select count(*) n, string_agg(u.codigo || ' ' || u.denominacao, '; ') filter (where rn <= 5) ex from (select u.*, row_number() over () rn from denominacoes_2022_estimativa u
  join (select codigo / 100000 uf, denominacao, sum(central) s from denominacoes_2022_estimativa where tipo = 'municipio' group by 1, 2) m on m.uf = u.codigo and m.denominacao = u.denominacao where u.tipo = 'uf' and u.central <> m.s) u),
det as (select nivel, codigo_ibge, max(pessoas) filter (where slug = 'evangelicas') - coalesce(max(pessoas) filter (where slug = 'nao-determinada'), 0) det from denominacoes_2010 group by 1, 2),
esc as (select d.nivel, d.codigo_ibge, d.slug, round(100.0 * d.pessoas / t.det, 1) pct from denominacoes_2010 d join det t using (nivel, codigo_ibge)
  where d.grupo = 'igreja' and d.slug <> 'outras-pentecostais' and t.det > 0 and d.pessoas >= 500 and 100.0 * d.pessoas / t.det >= 10
  and exists (select 1 from denominacoes_2022_estimativa e where e.tipo = d.nivel and e.codigo = (case when d.nivel = 'brasil' then 0 else d.codigo_ibge end))
  and not exists (select 1 from denominacoes_2022_estimativa e where e.tipo = d.nivel and e.codigo = (case when d.nivel = 'brasil' then 0 else d.codigo_ibge end) and e.denominacao = d.slug)),
c8 as (select count(*) filter (where slug not in ('casa-da-bencao', 'nova-vida', 'comunidade-evangelica')) n, count(*) filter (where slug in ('casa-da-bencao', 'nova-vida', 'comunidade-evangelica')) conhecidos,
  string_agg(nivel || ' ' || codigo_ibge || ' ' || slug || ' ' || pct || '%', '; ') filter (where slug not in ('casa-da-bencao', 'nova-vida', 'comunidade-evangelica')) ex from esc),
e22 as (select codigo, denominacao, 100.0 * central / nullif(sum(central) over (partition by codigo), 0) p22 from denominacoes_2022_estimativa where tipo = 'municipio'),
e10 as (select d.codigo_ibge codigo, d.slug denominacao, 100.0 * d.pessoas / t.det p10 from denominacoes_2010 d join det t using (nivel, codigo_ibge) where d.nivel = 'municipio' and d.grupo = 'igreja' and t.det >= 1000),
dv as (select e22.codigo, e22.denominacao, round(e22.p22, 1) p22, round(e10.p10, 1) p10 from e22 join e10 using (codigo, denominacao) where abs(e22.p22 - e10.p10) > 20),
c9 as (select count(*) n, string_agg(m.nome || '-' || m.uf || ' ' || dv.denominacao || ' ' || dv.p10 || '→' || dv.p22, '; ') filter (where rn <= 5) ex
  from (select *, row_number() over (order by abs(p22 - p10) desc) rn from dv) dv join municipios m on m.codigo_ibge = dv.codigo),
c10 as (select count(*) n, string_agg(t.origem || ' tabela ' || t.n || ' x visão ' || coalesce(v.n, 0), '; ') ex from (select origem, count(*) n from templos where codigo_ibge is not null group by 1) t
  left join (select origem, sum(total) n from mv_templos_municipio group by 1) v using (origem) where t.n <> coalesce(v.n, 0)),
c11 as (select (select count(*) from templos where origem = 'cnefe') cnefe, (select max(referencia) from templos where origem = 'cnpj') base_cnpj),
c12 as (select count(*) n from (select rank_brasil, rank() over (order by pct_ev_2022 desc nulls last) r from v_municipio_religiao) x where rank_brasil <> r),
c13 as (select count(*) n, max(escolhida_em) ultima from materias_home)
select 1 ordem, 'Censo: estado = soma dos municípios (tolerância 0,01%)' checagem, case when n = 0 then 'ok' else 'erro' end status, coalesce(ex, '') detalhe from c1
union all select 2, 'Censo: Brasil = soma dos estados (tolerância 0,01%)', case when n = 0 then 'ok' else 'erro' end, coalesce(ex, '') from c2
union all select 3, 'Censo: percentual = evangélicos ÷ população', case when n = 0 then 'ok' else 'erro' end, n || ' linhas ' || coalesce(ex, '') from c3
union all select 4, 'Censo 2022: municípios sem divulgação do IBGE', case when n <= 2 then 'ok' else 'alerta' end, n || ' (linha de base: 2, Pacaraima-RR e Marcação-PB) ' || coalesce(ex, '') from c3b
union all select 5, 'Modelo: parâmetros = Censo 2022', case when n = 0 then 'ok' else 'erro' end, n || ' municípios ' || coalesce(ex, '') from c4
union all select 6, 'Igrejas 2022: soma = evangélicos do Censo', case when n = 0 then 'ok' else 'erro' end, n || ' municípios ' || coalesce(ex, '') from c5
union all select 7, 'Igrejas 2022: faixa e grupos', case when n = 0 and grupos_diferentes = 0 then 'ok' else 'erro' end, n || ' faixas fora de ordem ou negativas; ' || grupos_diferentes || ' territórios com grupos diferentes do Brasil (' || grupos_brasil || ' grupos)' from c6
union all select 8, 'Igrejas 2022: municípios sem estimativa', case when n <= 9 then 'ok' else 'alerta' end, n || ' (linha de base: 9, criados depois de 2010 ou sem dado)' from c6b
union all select 9, 'Igrejas 2022: estado = soma dos municípios', case when n = 0 then 'ok' else 'erro' end, n || ' linhas ' || coalesce(ex, '') from c7
union all select 10, 'Igreja com 10% ou mais escondida em "outras"', case when n = 0 and conhecidos <= 9 then 'ok' when n = 0 then 'alerta' else 'erro' end, n || ' casos novos ' || coalesce(ex, '') || ' · limite conhecido: ' || conhecidos || ' (linha de base 9: Casa da Bênção, Nova Vida e Comunidade Evangélica)' from c8
union all select 11, 'Estimativa a mais de 20 pontos do Censo 2010', case when n <= 52 then 'ok' else 'alerta' end, n || ' casos (linha de base 17/11/2026: 52) ' || coalesce(ex, '') from c9
union all select 12, 'Templos: visão em dia com a tabela', case when n = 0 then 'ok' else 'erro' end, coalesce(ex, '') from c10
union all select 13, 'Templos: CNEFE e base do CNPJ', case when cnefe = 579798 then 'ok' else 'erro' end, 'CNEFE ' || cnefe || ' (esperado 579.798); base CNPJ: ' || base_cnpj from c11
union all select 14, 'Ranking dos municípios = ordem do percentual', case when n = 0 then 'ok' else 'erro' end, n || ' municípios fora de ordem' from c12
union all select 15, 'Matérias da home renovadas', case when n = 3 and ultima > now() - interval '26 hours' then 'ok' else 'alerta' end, n || ' matérias; última escolha ' || ultima from c13
order by ordem;
```

O que cada checagem pega:
1–2. Censo: estado = soma dos municípios e Brasil = soma dos estados (tolerância de 0,01%, porque o próprio SIDRA tem diferenças de poucas pessoas entre níveis).
3. Percentual gravado = evangélicos ÷ população.
4. Municípios em que o IBGE não divulgou religião em 2022 (hoje 2: Pacaraima-RR e Marcação-PB; o site avisa "o Censo 2022 não permite calcular"). Mais que 2 é alerta.
5. Parâmetros do modelo de projeção = Censo 2022.
6–9. Estimativa de igrejas 2022: soma dos grupos = evangélicos do Censo; baixo ≤ central ≤ alto, sem negativos; todo território com os mesmos 13 grupos; estado = soma dos municípios; municípios sem estimativa (hoje 9, criados depois de 2010 ou sem dado).
10. Igreja escondida: igreja com 10% ou mais dos evangélicos (e 500 pessoas ou mais) em 2010 sem linha própria na estimativa. É o erro da Maranata. Limite conhecido: 9 cidades com Casa da Bênção, Nova Vida ou Comunidade Evangélica (não passam no teste de correlação; aparecem só nas barras de 2010).
11. Estimativa a mais de 20 pontos do Censo 2010 numa igreja (cidades com mil evangélicos ou mais em 2010). Linha de base: 52 casos em 17/11/2026. Os piores costumam ser cidades pequenas com poucos templos no CNEFE.
12–13. Templos: visão materializada em dia com a tabela; CNEFE com 579.798 endereços; base do CNPJ (a atualização mensal roda nos dias 16 e 26: se depois do dia 27 a base ainda for de dois meses antes, é alerta).
14. Ranking dos municípios = ordem do percentual (empates são normais).
15. Matérias da home renovadas nas últimas 26 horas (job das 6h05).

## Passo 2: amostra contra o IBGE e o site publicado

Gravar o script abaixo em `~/validacao-datafe/amostra.py` (sobrescrever) e rodar `cd ~/validacao-datafe && python3 -I amostra.py`. Ele usa a data de hoje para sortear 8 municípios (muda todo dia) e confere sempre Vitória, Santa Maria de Jetibá, São Paulo e Arroio do Padre, além do Brasil e de um estado por dia, em rodízio. Para cada município:
- Censo 2022 do banco = SIDRA 10183 (população de 10 anos ou mais, evangélicos, católicos e sem religião);
- igrejas de 2010 do banco = SIDRA 137 (todas as igrejas, inclusive Maranata e Luterana);
- o site publicado mostra o mesmo percentual e o mesmo número de evangélicos;
- na página do estado, o artigo certo ("no Espírito Santo", "na Bahia", e não "em Espírito Santo").

Se o SIDRA ou o site não responderem, o script tenta três vezes e marca alerta "não deu para conferir agora"; isso não é erro de dado.

```python
"""Validação diária do Datafé: amostra rotativa contra o IBGE (SIDRA) e contra o site publicado.
Só lê. Nunca grava nada.
Uso: python3 -I amostra.py [AAAA-MM-DD] [--n 8]
Imprime uma linha por conferência (ok, erro ou alerta) e, no fim, uma linha começando com RESUMO_JSON."""
import datetime, hashlib, html, json, re, sys, time, urllib.parse, urllib.request

SB = 'https://mvxzozxjzbrzndaunlxj.supabase.co/rest/v1/'
KEY = 'sb_publishable_ewekwTa4nrpdlXkhyfdYGg_IZkZskj2'  # chave publicável (leitura pública)
SIDRA = 'https://apisidra.ibge.gov.br/values/'
SITE = 'https://datafe.com.br'
# Sempre conferidos: Vitória, Santa Maria de Jetibá, São Paulo, Arroio do Padre
FIXOS = [3205309, 3204559, 3550308, 4301073]
# Estados que pedem artigo: "no Espírito Santo", "na Bahia"
COM_ARTIGO = {'AP': 'o', 'AM': 'o', 'BA': 'a', 'CE': 'o', 'DF': 'o', 'ES': 'o', 'MA': 'o', 'MT': 'o', 'MS': 'o',
              'PA': 'o', 'PB': 'a', 'PR': 'o', 'PI': 'o', 'RJ': 'o', 'RN': 'o', 'RS': 'o', 'TO': 'o', 'AC': 'o'}
# Rótulo do SIDRA 137 (trecho) -> slug do banco. A ordem importa: o primeiro que casar vale.
MAPA_137 = [
    ('assembl', 'assembleia-de-deus'), ('congregação cristã', 'congregacao-crista-do-brasil'),
    ('brasil para cristo', 'o-brasil-para-cristo'), ('quadrangular', 'evangelho-quadrangular'),
    ('universal do reino', 'universal-do-reino-de-deus'), ('casa da ben', 'casa-da-bencao'),
    ('deus é amor', 'deus-e-amor'), ('maranata', 'maranata'), ('nova vida', 'nova-vida'),
    ('comunidade evangélica', 'comunidade-evangelica'), ('pentecostal - outras', 'outras-pentecostais'),
    ('adventista', 'adventista'), ('luterana', 'luterana'), ('presbiteriana', 'presbiteriana'),
    ('metodista', 'metodista'), ('batista', 'batista'), ('evangélica não determinada', 'nao-determinada'),
]
achados = []

def registrar(status, onde, texto):
    achados.append({'status': status, 'onde': onde, 'texto': texto})
    print(f'[{status}] {onde}: {texto}')

def get(url, headers=None, tentativas=3):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=headers or {'User-Agent': 'Mozilla/5.0 (validacao-datafe)'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8', 'ignore')
        except Exception:
            if i == tentativas - 1:
                raise
            time.sleep(4 * (i + 1))

def banco(tabela, **params):
    q = urllib.parse.urlencode(params, safe=',.()*')
    return json.loads(get(SB + tabela + '?' + q, {'apikey': KEY, 'Authorization': 'Bearer ' + KEY}))

def sidra(caminho):
    d = json.loads(get(SIDRA + caminho))
    cab = d[0]
    dims = [k for k in cab if k.startswith('D') and k.endswith('N')]
    out = []
    for linha in d[1:]:
        v = linha['V']
        out.append((' | '.join(linha[k] for k in dims), None if v in ('-', '...', 'X', '..') else int(v)))
    return out

def num_br(n):
    return f'{n:,}'.replace(',', '.')

def pct_br(p):
    return f'{p:.1f}'.replace('.', ',')

def texto_pagina(caminho):
    t = get(SITE + caminho)
    titulo = (re.findall(r'<title>(.*?)</title>', t, re.S) or [''])[0]
    corpo = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    return html.unescape(titulo), re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', corpo)))

def conferir_2022(onde, nivel_sidra, codigo, db):
    """db: dict com pop, ev, cat, sr (Censo 2022, 10 anos ou mais)."""
    linhas = sidra(f't/10183/{nivel_sidra}/{codigo}/v/allxp/p/2022/c133/all')
    fonte = {}
    for rot, v in linhas:
        r = rot.split(' | ')[3].strip().lower()
        if r == 'total': fonte['pop'] = v
        elif r == 'evangélicas': fonte['ev'] = v
        elif r.startswith('católica apostólica'): fonte['cat'] = v
        elif r == 'sem religião': fonte['sr'] = v
    if fonte.get('pop') is None:
        if db.get('pop'):
            registrar('erro', onde, f'IBGE não divulga 2022 aqui, mas o banco tem {db.get("pop")} pessoas')
        else:
            registrar('ok', onde, 'sem dado de 2022 no IBGE e no banco (página deve avisar)')
        return
    dif = [f'{k}: banco {db.get(k)} x IBGE {fonte.get(k)}' for k in ('pop', 'ev', 'cat', 'sr') if fonte.get(k) is not None and db.get(k) is not None and db[k] != fonte[k]]
    if dif:
        registrar('erro', onde, 'Censo 2022 diferente do SIDRA 10183: ' + '; '.join(dif))
    else:
        registrar('ok', onde, f'Censo 2022 = SIDRA 10183 ({num_br(fonte["ev"])} evangélicos de {num_br(fonte["pop"])})')

def conferir_2010_igrejas(onde, codigo):
    linhas = sidra(f't/137/n6/{codigo}/v/allxp/p/2010/c133/all')
    fonte = {}
    exatos = {'evangélicas': 'evangelicas', 'evangélicas de missão': 'missao', 'evangélicas de origem pentecostal': 'pentecostal'}
    for rot, v in linhas:
        r = rot.split(' | ')[3].strip().lower()
        if r in exatos:
            fonte[exatos[r]] = v or 0
            continue
        if not r.startswith('evang'):
            continue
        for trecho, slug in MAPA_137:
            if trecho in r:
                fonte[slug] = fonte.get(slug, 0) + (v or 0)
                break
    db = {d['slug']: d['pessoas'] for d in banco('denominacoes_2010', select='slug,pessoas', nivel='eq.municipio', codigo_ibge=f'eq.{codigo}')}
    conferidos = {s for _, s in MAPA_137} | set(exatos.values())
    dif = [f'{s}: banco {v} x IBGE {fonte.get(s, 0)}' for s, v in db.items() if s in conferidos and v != fonte.get(s, 0)]
    if dif:
        registrar('erro', onde, 'igrejas 2010 diferentes do SIDRA 137: ' + '; '.join(dif[:6]))
    else:
        registrar('ok', onde, f'igrejas 2010 = SIDRA 137 ({len(db)} linhas)')

def conferir_pagina_municipio(onde, m):
    titulo, texto = texto_pagina(f'/municipio/{m["slug"]}')
    if m.get('pct_ev_2022') is None:
        ok = 'não permite calcular' in texto
        registrar('ok' if ok else 'erro', onde, 'página avisa que não há dado de 2022' if ok else 'página não avisa a falta de dado de 2022')
        return
    pct, ev = pct_br(float(m['pct_ev_2022'])), num_br(int(m['ev_2022']))
    falta = [x for x in (pct + '%', ev) if x not in titulo + ' ' + texto]
    if falta:
        registrar('erro', onde, f'site publicado não mostra {", ".join(falta)} (título: {titulo[:90]})')
    else:
        registrar('ok', onde, f'site publicado mostra {pct}% e {ev}')

def conferir_pagina_estado(onde, uf, db):
    titulo, texto = texto_pagina(f'/estado/{uf["slug"]}')
    pct, ev = pct_br(100.0 * db['ev'] / db['pop']), num_br(db['ev'])
    falta = [x for x in (pct + '%', ev) if x not in titulo + ' ' + texto]
    registrar('erro' if falta else 'ok', onde, f'site publicado não mostra {", ".join(falta)}' if falta else f'site publicado mostra {pct}% e {ev}')
    art = COM_ARTIGO.get(uf['sigla'])
    # Só no título e na primeira frase, para não confundir com frases como "nascido em Amazonas"
    if art and re.search(r'\bem ' + re.escape(uf['nome']) + r'\b', titulo + ' ' + texto[:400]):
        registrar('alerta', onde, f'texto diz "em {uf["nome"]}"; o certo é "{"no" if art == "o" else "na"} {uf["nome"]}"')

def censo_banco(nivel, codigo):
    r = banco('religiao_censo', select='populacao,evangelicos,catolicos,sem_religiao', nivel=f'eq.{nivel}',
              codigo_ibge=f'eq.{codigo}', ano='eq.2022', base='eq.10_anos_ou_mais', faixa_idade='eq.total')
    r = r[0] if r else {}
    return {'pop': r.get('populacao'), 'ev': r.get('evangelicos'), 'cat': r.get('catolicos'), 'sr': r.get('sem_religiao')}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 8
    dia = args[0] if args and re.match(r'\d{4}-\d{2}-\d{2}$', args[0]) else datetime.date.today().isoformat()
    total = 5570
    sorteio = []
    for i in range(n * 3):
        k = int(hashlib.sha256(f'{dia}-{i}'.encode()).hexdigest(), 16) % total
        if k not in sorteio:
            sorteio.append(k)
        if len(sorteio) == n:
            break
    cols = 'codigo_ibge,nome,uf,slug,pop10_2022,ev_2022,cat_2022,sr_2022,pct_ev_2022'
    municipios = [banco('v_municipio_religiao', select=cols, codigo_ibge=f'eq.{c}')[0] for c in FIXOS]
    for k in sorteio:
        municipios += banco('v_municipio_religiao', select=cols, order='codigo_ibge', offset=str(k), limit='1')
    print(f'Dia {dia}: {len(municipios)} municípios ({len(FIXOS)} fixos + {n} sorteados)')
    for m in municipios:
        onde = f'{m["nome"]} ({m["uf"]})'
        db = {'pop': m['pop10_2022'], 'ev': m['ev_2022'], 'cat': m['cat_2022'], 'sr': m['sr_2022']}
        for etapa in (lambda: conferir_2022(onde, 'n6', m['codigo_ibge'], db),
                      lambda: conferir_2010_igrejas(onde, m['codigo_ibge']),
                      lambda: conferir_pagina_municipio(onde, m)):
            try:
                etapa()
            except Exception as e:
                registrar('alerta', onde, f'não deu para conferir agora ({type(e).__name__}: {str(e)[:80]})')
    # Brasil e um estado por dia (rodízio)
    ufs = banco('ufs', select='codigo_ibge,sigla,nome,slug', order='codigo_ibge')
    uf = ufs[datetime.date.fromisoformat(dia).toordinal() % len(ufs)]
    for onde, nivel_sidra, nivel, cod in (('Brasil', 'n1', 'brasil', 'all'), (uf['nome'], 'n3', 'uf', uf['codigo_ibge'])):
        try:
            db = censo_banco(nivel, cod) if nivel == 'uf' else (censo_banco('brasil', 1) if censo_banco('brasil', 1).get('pop') else censo_banco('brasil', 0))
            conferir_2022(onde, nivel_sidra, cod, db)
            if nivel == 'uf':
                conferir_pagina_estado(onde, uf, db)
        except Exception as e:
            registrar('alerta', onde, f'não deu para conferir agora ({type(e).__name__}: {str(e)[:80]})')
    resumo = {s: sum(1 for a in achados if a['status'] == s) for s in ('ok', 'erro', 'alerta')}
    print('RESUMO_JSON ' + json.dumps({'dia': dia, **resumo, 'problemas': [a for a in achados if a['status'] != 'ok']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
```

A última linha da saída começa com `RESUMO_JSON` e traz os totais e os problemas.

## Como ler o resultado

- **erro:** número diferente da fonte, soma que não fecha, igreja escondida, site mostrando outro número. Vai no topo do relatório.
- **alerta:** passou de uma linha de base, dado vencido, texto errado, fonte fora do ar. Vai depois dos erros.
- **ok:** não listar um por um; só contar.

Para cada erro ou alerta, dizer: o que está errado, onde (município, estado, página), o valor no site ou no banco, o valor na fonte com o link do SIDRA, a causa provável e a correção proposta. A correção só é feita com o ok de Mário, numa conversa.

Linhas de base em 17/11/2026 (atualizar nesta skill quando Mário aprovar uma recarga do modelo que as mude): 2 municípios sem dado de 2022; 9 sem estimativa; 9 casos de igreja escondida conhecidos; 52 casos acima de 20 pontos; 579.798 endereços no CNEFE.

## Pendências conhecidas

Problema já achado e já corrigido no preview, esperando publicação, não volta como novidade: vai numa linha só, no fim ("pendente de publicação: …"). Hoje: o artigo dos estados ("em Espírito Santo", "em Amazonas"), corrigido nos commits 3704ce2 e efb4c16 do Lovable em 17/11/2026. Quando a checagem do artigo passar a dar ok, tirar daqui.

## Saída

- **Tudo ok:** uma linha só. Ex.: "Datafé, 18/11: 15 checagens no banco e N conferências contra o IBGE e o site, tudo certo." (N = linhas que o script imprimiu, sem contar a do RESUMO_JSON.)
- **Com problema:** mensagem curta. Primeiro os erros, depois os alertas, cada um com a correção proposta e a pergunta de ok. Depois, em uma linha, as pendências conhecidas. No fim, a contagem do que passou.
- O relatório é para Mário: não assinar.
- Se a ferramenta Projects estiver disponível e o projeto "Evangelicos em numeros 2026" estiver ligado, acrescentar no doc `claude/validacao-datafe.md` uma linha datada só quando houver erro ou alerta novo (não gravar rodada sem novidade).
- Nunca dizer que corrigiu algo. A rodada só confere.

## Histórico

- 17/11/2026: primeira rodada, feita à mão. Achou a Maranata escondida em Vitória (14,2% dos evangélicos em 2010, 3ª igreja da cidade) e a Luterana escondida em 320 municípios. A estimativa passou de 6 para 12 igrejas (Maranata, Luterana, Presbiteriana, Metodista, Deus é Amor e O Brasil para Cristo, todas com correlação de pelo menos 0,5 entre os templos do CNEFE e o Censo 2010), com regra própria para as paróquias luteranas registradas como "Comunidade Evangélica" nas 222 cidades de maioria luterana. Achou também "em Espírito Santo" e "em Amazonas" nas páginas de estado.

## Modelo recomendado
- Nível: Sonnet
- Nota: 4/12 (raciocínio 1, fontes 1, texto 0, números 1, fluxo 1, risco 0)
- Motivo: segue regras escritas e só compara números de fontes fixas, mas roda SQL e script com ramos de erro, o que pede mais que o Haiku.
- Teste: aprovado em 17/11/2026 no Sonnet (ensaio completo: 15 checagens no banco, 40 conferências contra o IBGE e o site, relatório no formato certo)
- Subir para Opus se: a rodada passar a propor correções de método (recálculo do modelo) ou a escrever código no app.