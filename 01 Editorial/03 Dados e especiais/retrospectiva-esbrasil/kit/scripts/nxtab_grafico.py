#!/usr/bin/env python3
"""Gráficos da Retrospectiva feitos no NXtab, o construtor de gráficos da Next.

Roda o próprio NXtab (artefato "NXtab", slug 7a1c22c8-3982-455a-ab9a-cac69d588c8c) num Chromium sem tela,
aplica um modelo da biblioteca da revista ES Brasil, troca os dados e devolve a peça pronta para a página:

    python3 nxtab_grafico.py NXTAB.html GRAFICOS.json PASTA_SAIDA

NXTAB.html   o index.html do artefato NXtab (baixe com read_file, paths=["index.html"]).
GRAFICOS.json  lista de peças, por exemplo:
    [{"id": "quarto-do-pais", "modelo": "c-percentual", "vaga": "abertura",
      "titulo": "Quarto do país",
      "subtitulo": "Estados com maior movimentação portuária em 2025, em milhões de toneladas",
      "fonte": "Atlas Portuário do ES (Findes), com dados da Antaq.",
      "csv": "Estado;Milhões de toneladas\\n1º RJ;326,9\\n2º SP;235,4\\n3º MA;223,7\\n4º ES;137,5",
      "destaque": "4º ES"}]
    Campos opcionais: larguras (tabela: pesos relativos das colunas, um por coluna, ex.: [5, 6, 6, 5, 6, 5]), notas, unidade, ordem (original, desc, asc), fundo (auto, none, portos, agro...),
    fundo também aceita a foto escolhida no NX Fotos para o assunto da peça (o NXtab passa para cinza a 5%):
        {"arquivo": "fundos/culto.jpg", "titulo": "Culto", "autor": "Fulano", "fonte": "NX Fotos"}
        Busque sempre a foto pelo assunto dos dados (o que o gráfico mostra, e onde), nunca só pela editoria;
        sem foto, "auto" usa a foto do tema que o NXtab reconhece no título e nos dados.
    caixa (grad, gray, sky, none...), filete (red, navy), variante (std, ribbon, half...), marca (esb, com, des, pro, next),
    coluna_valor (índice da coluna de valores; padrão 1),
    publicar (true sobe a versão para web a nxtab.nxte.com.br/<marca>/<id>.html, no R2 "nx-graficos", e grava
    <id>.iframe.html com o código para a matéria; pede as variáveis NX_R2_ACCESS_KEY, NX_R2_SECRET e NX_R2_ENDPOINT).
    Linhas do tempo: "fotos" (só em i-tempo-fotos) liga cada data da coluna Data a uma foto:
        {"mar/26": {"arquivo": "fotos/porto.jpg", "autor": "Fulano", "fonte": "Divulgação"}, ...}
        (arquivo local ou data:URL; o crédito sai numa linha só, junto da fonte). Sem foto, o marco fica sem imagem.
    "icones" (i-tempo-pictos, c-faixa e c-lista) troca o picto de um marco ou de um indicador, pelo texto da coluna Marco e o nome do ícone
        Lucide: {"Porto Central": "anchor", "Safra recorde": "sprout"}. Sem isso, o NXtab escolhe pelo assunto.

Modelos de gráfico da biblioteca do NXtab: c-colunas (colunas por série), c-percentual (uma série, destaque),
c-barras (barras horizontais), c-rosca (participação), c-faixa (faixa de números), c-lista (box "em números"),
p-destaque e p-capa (painéis), v-fita, v-leque, v-numerada, v-passos.
Tabela: t-retro ("Tabela da Retrospectiva": título na cor da marca, sem caixa alta, fundo cinza 5%, barrinha
rosa no topo, primeira coluna em destaque), na vaga "tabela".
Linhas do tempo: i-tempo-fotos (faixa de fotos, data sob cada foto, marcos alternados acima e abaixo) e
i-tempo-pictos (faixa em seta com datas, pictos e texto alternados), em CSV Data;Marco;Detalhe, na vaga "larga".
Datas em mmm/aa (o NXtab converte abr/2026 em abr/26). Até 12 marcos; com mais de 8 o NXtab passa para a vertical.

Vagas (largura de desenho no NXtab -> largura na página de 900 px), escolhidas para os dados saírem perto de 10 px (6,5 pt):
    abertura  420 -> 320 px   painel sobre a foto de abertura
    lateral   330 -> 246 px   uma coluna da grade da revista (55,8 mm)
    larga    1000 -> 773 px   largura toda da mancha (176 mm), na mesma escala da coluna e da tabela (22/11/2026)
    tabela   1000 -> 773 px   tabela t-retro na largura toda; letra do corpo perto de 7,3 pt (antes 1250 px, que deixava
                              a letra em 5,8 pt; o editor pediu, em 22/11/2026, que tabela e gráfico nunca encolham para caber)

Regras da casa aplicadas na saída:
- escala quebrada (modelo de referência: "Para onde vão as cargas", Portos, 11/11/2026): em barras e colunas de
  uma série, quando o maior valor passa de 2 vezes o segundo, a escala vai só até o segundo valor, a barra do
  maior sai inteira até o fim do eixo com a marca de quebra (//), o número dela fica escrito por inteiro e a fonte
  ganha "<item>: barra fora de escala." Campo "quebra": "auto" (padrão), true (força no maior) ou false (desliga);
  "nota_quebra" troca o texto da nota. Nunca se estica barra sem a quebra, e escala logarítmica não é usada;
- título em caixa alta (decisão do Mário Fernando, 22/11/2026; o NXtab aplica);
- sem o cerco branco do NXtab: a peça é recortada no box e vai direto sobre a foto ou a página, sem sombra;
- a fonte fica logo abaixo do box, dentro da peça.

Saída, por peça: <id>.svg (vai para a página), <id>.nxtab.json (projeto que abre no NXtab para ajustes),
<id>.png (prévia), <id>.html (o <figure> pronto para colar no capítulo), <id>.csv (os dados, para Textos/ do pacote)
e <id>.web.html (a versão para o site: uma peça só para computador e celular, animada, com os números ao passar
o dedo ou o mouse; publica-se num endereço público e entra na matéria por iframe).
"""
from __future__ import annotations

import asyncio
import base64
import os
import json
import mimetypes
import html
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

VAGAS = {"abertura": (420, 320), "lateral": (330, 246), "dupla": (660, 509), "larga": (1000, 773), "tabela": (1000, 773)}   # grade da revista: coluna de 55,8 mm e mancha de 176 mm

# Barrinha de cor no canto superior esquerdo de toda peça (filete da marca): tamanho padrão de 20 x 1 mm
# na página impressa (pedido de 26/11/2026). A página tem 205 mm em 900 px na prova.
ABA_MM = (20.0, 1.0)
PX_POR_MM = 900 / 205


def aba_padrao(svg: str, w: float, exibe: float) -> str:
    """Redimensiona a barrinha do topo (o <rect> encostado no canto do viewBox, com até 10 de altura)
    para 20 x 1 mm na página, mantendo a posição e a cor."""
    m = re.search(r'viewBox="([-\d.]+)[\s,]+([-\d.]+)', svg)
    if not m:
        return svg
    vx, vy = float(m.group(1)), float(m.group(2))
    u = PX_POR_MM * w / exibe          # unidades do SVG por milímetro na página

    def troca(r):
        tag = r.group(0)
        g = lambda k: float(re.search(k + r'="([-\d.]+)"', tag).group(1)) if re.search(k + r'="([-\d.]+)"', tag) else None  # noqa: E731
        x, y, hh = g("x"), g("y"), g("height")
        if x is None or y is None or hh is None or abs(x - vx) > 0.5 or abs(y - vy) > 0.5 or hh > 10:
            return tag
        tag = re.sub(r'width="[\d.]+"', f'width="{ABA_MM[0] * u:.2f}"', tag, count=1)
        return re.sub(r'height="[\d.]+"', f'height="{ABA_MM[1] * u:.2f}"', tag, count=1)

    return re.sub(r"<rect [^>]*>", troca, svg)


JS = r'''
async (g) => {
  const m = REV_MODELS.find(x => x.id === g.modelo);
  if (!m) throw new Error('Modelo desconhecido no NXtab: ' + g.modelo);
  revApply(m);
  $('brand').value = g.marca || 'esb'; applyPalette();
  setData(parseCSV(g.csv));
  const set = (id, v) => { if (v !== undefined && v !== null) $(id).value = v; };
  set('title', g.titulo); set('subtitle', g.subtitulo || ''); set('source', g.fonte || '');
  set('notes', g.notas || ''); set('unit', g.unidade || ''); set('sortOrder', g.ordem || 'original');
  set('bgImage', g.fundo); set('boxTone', g.caixa);
  if (g.fundo_dados) {                                    // foto de fundo escolhida no NX Fotos para o assunto da peça
    state.bgCustom = await revGray(g.fundo_dados.src);
    state.bgCustomInfo = { title: g.fundo_dados.titulo || 'Foto do NX Fotos', author: g.fundo_dados.autor || '', source: g.fundo_dados.fonte || 'NX Fotos' };
    $('bgImage').value = 'custom';
  } set('tabColor', g.filete); set('variant', g.variante);
  $('showValues').checked = g.valores !== false;
  $('labelColumn').value = '0'; $('valueColumn').value = String(g.coluna_valor ?? 1);
  if (m.format === 'timeline') {                          // fotos e pictos da peça (nunca os de exemplo do modelo)
    state.tlImgs = {};
    for (const [k, f] of Object.entries(g.fotos_dados || {})) state.tlImgs[k] = { src: f.src, info: { title: k, author: f.autor || '', source: f.fonte || '' } };
    state.iconPick = { ...(g.icones || {}) };
  } else if (g.icones) {                                  // painéis de números (c-faixa, c-lista): um ícone por indicador
    state.iconPick = { ...g.icones }; if ($('iconMode')) $('iconMode').value = 'auto';
  }
  if (g.larguras && !window.__nxColPatched) {           // pesos das colunas da tabela (ex.: coluna de produto mais estreita)
    const src = revTable.toString();
    const re = /wts=H\.map\(\(h,j\)=>Math\.max\(4,Math\.min\(48,Math\.max\(len\(h\)\*\.5,\.\.\.state\.rows\.map\(r=>len\(r\[j\]\)\)\)\)\)\)/;
    if (!re.test(src)) throw new Error('NXtab mudou: não achei o cálculo das colunas da tabela');
    revTable = eval('(' + src.replace(re, 'wts=(window.__nxColW&&window.__nxColW.length===H.length)?window.__nxColW:H.map((h,j)=>Math.max(4,Math.min(48,Math.max(len(h)*.5,...state.rows.map(r=>len(r[j]))))))') + ')');
    window.__nxColPatched = true;
  }
  window.__nxColW = g.larguras || null;
  updateHighlight(); $('highlight').value = g.destaque || '';
  render();
  const svg = svgPiece(settings(), g.largura);   // título em caixa alta (decisão de 22/11/2026), o NXtab já aplica
  const web = typeof nxWebExport === 'function' ? nxWebExport(settings(), g.id) : null;
  return { svg, project: project(), web };
}
'''


LIMIAR_QUEBRA = 2.0     # maior valor / segundo maior a partir do qual a barra do maior é quebrada
MODELOS_QUEBRA = {"c-barras", "c-colunas", "c-percentual"}


def _num(v: str) -> float | None:
    t = str(v).strip().replace("\u00a0", "")
    if not re.fullmatch(r"-?[\d.]*\d(,\d+)?", t):
        return None
    return float(t.replace(".", "").replace(",", "."))


def planejar_quebra(g: dict) -> dict | None:
    """Decide se a peça leva escala quebrada e qual linha do CSV é a barra fora de escala."""
    pedido = g.get("quebra", "auto")
    if pedido is False or g.get("modelo") not in MODELOS_QUEBRA:
        return None
    linhas = [l for l in g["csv"].strip().split("\n") if l.strip()]
    cab, dados = linhas[0].split(";"), [l.split(";") for l in linhas[1:]]
    numericas = [j for j in range(1, len(cab)) if all(len(r) > j and _num(r[j]) is not None for r in dados)]
    if len(numericas) != 1 or len(dados) < 3:      # só para uma série
        return None
    j = numericas[0]
    vals = sorted(((_num(r[j]), i) for i, r in enumerate(dados)), reverse=True)
    (v1, i1), (v2, _) = vals[0], vals[1]
    if v2 <= 0 or (pedido == "auto" and v1 / v2 < LIMIAR_QUEBRA):
        return None
    return {"linha": i1, "coluna": j, "rotulo": dados[i1][0].strip(), "serie": cab[j].strip(),
            "original": dados[i1][j].strip(), "segundo": v2, "cab": cab, "dados": dados}


def aplicar_quebra(svg: str, q: dict) -> str:
    """Devolve o número verdadeiro à barra quebrada e desenha a marca de quebra (//)."""
    tit_falso = f'{q["rotulo"]} · {q["serie"]}: {q["teto_txt"]}'
    k = svg.find(f"<title>{tit_falso}</title>")
    if k < 0:
        raise RuntimeError(f"Barra a quebrar não encontrada: {tit_falso}")
    ini = max(svg.rfind("<rect", 0, k), svg.rfind("<path", 0, k))
    tag = "rect" if svg.startswith("<rect", ini) else "path"
    fim = svg.find(f"</{tag}>", k) + len(f"</{tag}>")
    el = svg[ini:fim]
    fill = re.search(r'fill="([^"]+)"', el).group(1)
    cor = fill if fill.startswith("#") else "#" + re.search(r"nxg[hv]([0-9A-F]{6})", fill).group(1)
    if el.startswith("<rect"):                      # barra horizontal
        x, y, w, h = (float(re.search(rf'\b{a}="([\d.]+)"', el).group(1)) for a in ("x", "y", "width", "height"))
        bx = x + w * 0.75
        marca = (f'<g class="quebra"><polygon points="{bx:.2f},{y+h+2:.2f} {bx+7:.2f},{y-2:.2f} {bx+12:.2f},{y-2:.2f} {bx+5:.2f},{y+h+2:.2f}" fill="#FFFFFF"/>'
                 f'<line x1="{bx:.2f}" y1="{y+h+2:.2f}" x2="{bx+7:.2f}" y2="{y-2:.2f}" stroke="{cor}" stroke-width="1"/>'
                 f'<line x1="{bx+5:.2f}" y1="{y+h+2:.2f}" x2="{bx+12:.2f}" y2="{y-2:.2f}" stroke="{cor}" stroke-width="1"/></g>')
    else:                                           # coluna
        d = re.search(r'd="M([\d.]+) ([\d.]+)V([\d.]+)', el)
        x, base, topo = float(d.group(1)), float(d.group(2)), float(d.group(3))
        xs = [float(v) for v in re.findall(r"[HL]([\d.]+)", el)] + [float(v) for v in re.findall(r"Q[\d.]+ [\d.]+ ([\d.]+)", el)]
        bw = max(xs) - x if xs else 20
        by = base - (base - topo) * 0.75
        marca = (f'<g class="quebra"><polygon points="{x-2:.2f},{by+5:.2f} {x+bw+2:.2f},{by-2:.2f} {x+bw+2:.2f},{by+3:.2f} {x-2:.2f},{by+10:.2f}" fill="#FFFFFF"/>'
                 f'<line x1="{x-2:.2f}" y1="{by+5:.2f}" x2="{x+bw+2:.2f}" y2="{by-2:.2f}" stroke="{cor}" stroke-width="1"/>'
                 f'<line x1="{x-2:.2f}" y1="{by+10:.2f}" x2="{x+bw+2:.2f}" y2="{by+3:.2f}" stroke="{cor}" stroke-width="1"/></g>')
    novo = el.replace(f"<title>{tit_falso}</title>", f'<title>{q["rotulo"]} · {q["serie"]}: {q["original"]} (fora de escala)</title>')
    svg = svg[:ini] + novo + marca + svg[fim:]
    if svg.count(f'>{q["teto_txt"]}</text>') != 1:
        raise RuntimeError("Rótulo da barra quebrada não encontrado")
    return svg.replace(f'>{q["teto_txt"]}</text>', f'>{q["original"]}</text>')


# Ajustes de corpo aplicados sobre o NXtab na hora de gerar (pedidos do editor, 22/11/2026). Cada chave tem de existir
# no NXtab; se o NXtab mudar e a chave sumir, o script avisa em vez de seguir com o corpo antigo.
AJUSTES_NXTAB = {
    # linha do tempo com fotos (faixa): título do marco e detalhe maiores, o detalhe no corpo da linha de apoio das tabelas
    "ph=Math.round(colW*.46),tf=n>6?11:12,df=n>6?9.5:10,": "ph=Math.round(colW*.40),tf=n>6?13:14,df=n>6?13.8:15,",
    # linha do tempo com pictos (faixa): o mesmo
    "tf=n>6?11.5:12.5,df=n>6?9.5:10,": "tf=n>6?13:14,df=n>6?12.5:13.5,",
    # linha do tempo com fotos (faixa): o texto ocupa quase toda a largura da foto (o detalhe é em Myriad Condensed,
    # mais estreita que a conta do NXtab), para quebrar em menos linhas e a peça ficar mais baixa (pedido do editor, 22/11/2026)
    # detalhe dos marcos da linha do tempo em Myriad Condensed mais forte (peso 500 em vez de 300), pedido do editor, 22/11/2026
    "revTlCond(text(l,tx,ty,df,300,R.dark?R.ink:'#666666')": "revTlCond(text(l,tx,ty,df,600,R.dark?R.ink:'#3d3d3d')",
    # rosca: o item em destaque (o maior indicador) abre a legenda, em vez de fechá-la (pedido do editor, 22/11/2026)
    "const its=[...order.slice(1),hiI]": "const its=[hiI,...order.slice(1)]",
    "items=[...order.slice(1),hiI]": "items=[hiI,...order.slice(1)]",
    "t=vc>=0?wrap(String(r[vc]),w,tf):[],d=revTlDesc(r,oth)?wrap(revTlDesc(r,oth),w,df):[];return{t,d,": "t=vc>=0?wrap(String(r[vc]),w*1.1,tf):[],d=revTlDesc(r,oth)?wrap(revTlDesc(r,oth),w*1.38,df):[];return{t,d,",
    # linha de apoio (subtítulo) das peças em Arial Narrow Bold, num corpo maior que o texto da lista e das células
    # (pedido do editor, 22/11/2026): 15 px na lateral e 16 px nas peças largas, em vez de Myriad Condensed light de 12,5/13,5.
    # Na prova, sem a Arial Narrow instalada, sai a Roboto Condensed Bold; no InDesign, a Arial Narrow Bold.
    "ss=tlFx?(width<500?12:12.5):(width<500?12.5:13.5)": "ss=tlFx?(width<500?14:14.5):(width<500?15:16)",
    "y+=block(c.subtitle,p,y,ss,300,inner/.8,": "y+=block(c.subtitle,p,y,ss,700,inner/.92,",
    # entrelinha da linha de apoio mais aberta e respiro antes do corpo da peça (pedido do editor, 22/11/2026)
    "y+=block(c.subtitle,p,y,ss,700,inner/.92,R.subInk||R.ink,cmp?1.2:1.35)": "y+=block(c.subtitle,p,y,ss,700,inner/.92,R.subInk||R.ink,cmp?1.34:1.4)",
    "parts.push('</g>')}y+=cmp?(c.format==='table'?5:2):6;bodyStart=parts.length": "parts.push('</g>')}y+=cmp?(c.format==='table'?10:9):10;bodyStart=parts.length",
    'parts.splice(k2,0,`<g font-family="${NX_MYRIAD}" letter-spacing="0">`)': 'parts.splice(k2,0,`<g font-family="\'Arial Narrow\',\'Roboto Condensed\',\'Myriad Pro Condensed\',Arial,sans-serif" letter-spacing="0">`)',
}


def nxtab_ajustado(nxtab: Path) -> Path:
    txt = nxtab.read_text(encoding="utf-8")
    for a, b in AJUSTES_NXTAB.items():
        if a not in txt and b not in txt:
            print(f"AVISO: o NXtab mudou e o ajuste de corpo não foi aplicado: {a[:60]}...", file=sys.stderr)
        txt = txt.replace(a, b)
    saida = nxtab.resolve().with_name(nxtab.stem + ".ajustado.html")
    saida.write_text(txt, encoding="utf-8")
    return saida


def fotos_da_linha(g: dict, base: Path) -> dict:
    """Lê as fotos de uma linha do tempo (arquivo local ou data:URL) e devolve data:URLs com o crédito."""
    out = {}
    for data, f in (g.get("fotos") or {}).items():
        f = {"arquivo": f} if isinstance(f, str) else dict(f)
        src = f.get("arquivo", "")
        if not src.startswith("data:"):
            arq = Path(src) if Path(src).is_absolute() else base / src
            if not arq.exists():
                raise FileNotFoundError(f"Foto da linha do tempo não encontrada ({data}): {arq}")
            tipo = mimetypes.guess_type(arq.name)[0] or "image/jpeg"
            src = f"data:{tipo};base64," + base64.b64encode(arq.read_bytes()).decode()
        out[data] = {"src": src, "autor": f.get("autor", ""), "fonte": f.get("fonte", "")}
    return out


def fundo_da_peca(g: dict, base: Path) -> dict | None:
    """Foto de fundo da peça (campo "fundo" como objeto): arquivo local ou data:URL, com o crédito."""
    f = g.get("fundo")
    if not isinstance(f, dict):
        return None
    src = f.get("arquivo", "")
    if not src.startswith("data:"):
        arq = Path(src) if Path(src).is_absolute() else base / src
        if not arq.exists():
            raise FileNotFoundError(f"Foto de fundo não encontrada ({g['id']}): {arq}")
        tipo = mimetypes.guess_type(arq.name)[0] or "image/jpeg"
        src = f"data:{tipo};base64," + base64.b64encode(arq.read_bytes()).decode()
    return {"src": src, "titulo": f.get("titulo", ""), "autor": f.get("autor", ""), "fonte": f.get("fonte", "NX Fotos")}


def ids_unicos(svg: str, prefixo: str) -> str:
    """Prefixa os ids do SVG com o id da peça, para duas peças na mesma página não trocarem defs."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        n = f"{prefixo}-{i}"
        svg = svg.replace(f'id="{i}"', f'id="{n}"').replace(f"url(#{i})", f"url(#{n})").replace(f'href="#{i}"', f'href="#{n}"')
        svg = re.sub(r'(aria-labelledby="[^"]*)', lambda mm: re.sub(rf'(?<![\w-]){re.escape(i)}(?![\w-])', n, mm.group(1)), svg)
    return svg


R2_BUCKET = "nx-graficos"
R2_PUBLICO = "https://nxtab.nxte.com.br"
MARCAS = {"esb": "esbrasil", "com": "comunhao", "des": "destinos", "pro": "procidade", "next": "next"}


CORES_REALCE = {"rosa": "#E01E70", "azul": "#113E74"}


def aplicar_realces(texto: str, realces) -> str:
    """Números que gritam na tabela (pedido do editor, 22/11/2026): a célula com o texto exato sai em negrito
    (Inter Black) e na cor do projeto, no SVG (<text>) e na versão para web (<td>, <b> do celular)."""
    # linha de total em negrito (todas as células com a mesma linha de base do rótulo "Total")
    for y in set(re.findall(r'<text [^>]*?y="([\d.]+)"[^>]*>Total[^<]*</text>', texto)):
        texto = re.sub(r'(<text [^>]*?y="' + re.escape(y) + r'"[^>]*?)font-weight="[\d]+"', r'\1font-weight="800"', texto)
    texto = re.sub(r'<tr><td>(Total[^<]*)</td>', r'<tr style="font-weight:800"><td>\1</td>', texto)
    if not realces:
        return texto
    for valor, cor in realces.items():
        hexa = CORES_REALCE.get(cor, cor)
        v = re.escape(valor)
        texto = re.sub(r'(<text [^>]*?)font-weight="[\d]+"([^>]*?)fill="[^"]*"([^>]*>)' + v + '</text>',
                       lambda m: f'{m.group(1)}font-weight="900"{m.group(2)}fill="{hexa}"{m.group(3)}{valor}</text>', texto)
        texto = re.sub(r'(<text [^>]*?font-size=")14("[^>]*?font-weight="900"[^>]*?fill="' + re.escape(hexa) + '"[^>]*>)' + v + '</text>',
                       lambda m: f'{m.group(1)}16.8{m.group(2)}{valor}</text>', texto)   # corpo 20% maior
        texto = re.sub(r'<td>' + v + '</td>', f'<td style="color:{hexa};font-weight:900">{valor}</td>', texto)
        texto = re.sub(r'<b>' + v + '</b>', f'<b style="color:{hexa};font-weight:900">{valor}</b>', texto)
    return texto

def publicar_web(caminho: Path, marca: str, nome: str) -> dict:
    """Sobe a versão para web ao R2 (nxtab.nxte.com.br/<marca>/<nome>.html) e devolve o endereço e o iframe.
    Credenciais só por variáveis de ambiente: NX_R2_ACCESS_KEY, NX_R2_SECRET e NX_R2_ENDPOINT (nunca no código)."""
    import boto3
    s3 = boto3.client("s3", endpoint_url=os.environ["NX_R2_ENDPOINT"], region_name="auto",
                      aws_access_key_id=os.environ["NX_R2_ACCESS_KEY"], aws_secret_access_key=os.environ["NX_R2_SECRET"])
    chave = f"{MARCAS.get(marca, marca)}/{nome}.html"
    s3.upload_file(str(caminho), R2_BUCKET, chave,
                   ExtraArgs={"ContentType": "text/html; charset=utf-8", "CacheControl": "public, max-age=300"})
    url = f"{R2_PUBLICO}/{chave}"
    iframe = (f'<iframe src="{url}" title="{nome}" loading="lazy" style="width:100%;border:0;height:480px" data-nxtab="{nome}"></iframe>'
              "<script>addEventListener('message',function(e){var d=e.data||{};if(!d.nxtab)return;"
              "document.querySelectorAll('iframe[data-nxtab=\"'+d.nxtab+'\"]').forEach(function(f){f.style.height=d.altura+'px'})});</script>")
    return {"url": url, "iframe": iframe}


MYRIAD = "'Myriad Pro Condensed','Myriad Condensed','Roboto Condensed','Arial Narrow',Arial,sans-serif"
# Linha de apoio em Arial Narrow Bold, maior que o texto da lista (pedido do editor, 22/11/2026); na prova, Roboto Condensed Bold.
NARROW = "'Arial Narrow','Roboto Condensed','Myriad Pro Condensed',Arial,sans-serif"


def linha_de_apoio_myriad(svg: str, subtitulo: str) -> str:
    """Linha de apoio (descrição logo abaixo do título) em Arial Narrow Bold, em toda peça (regra do editor, 22/11/2026,
    que trocou a Myriad Condensed light: a linha de apoio tem de ser maior e mais forte que o texto da lista)."""
    alvo = html.unescape(subtitulo or "").replace("\u00a0", " ")
    if not alvo.strip():
        return svg

    def troca(m):
        abre, txt = m.group(1), m.group(2)
        limpo = html.unescape(re.sub(r"<[^>]+>", "", txt)).strip()
        if len(limpo) < 2 or limpo not in alvo or "font-family=" in abre:
            return m.group(0)
        return abre[:-1] + f' font-family="{NARROW}">' + txt + "</text>"

    return re.sub(r'(<text [^>]*font-weight="(?:300|700)"[^>]*>)((?:(?!</text>).)*)</text>', troca, svg, flags=re.S)


def afastar_fonte(svg: str, folga: float = 17.0) -> str:
    """A linha de fonte (e de créditos) fica sempre com a mesma folga abaixo do box: baseline 17 px abaixo da borda
    de baixo do cartão, como nos gráficos da lateral. Sem isso, com a fonte em 12 px, ela encostava no box da tabela e
    da linha do tempo (pedido do editor, 22/11/2026)."""
    card = re.search(r'<path d="M[\d.]+ [\d.]+H[\d.]+Q[\d.]+ [\d.]+ [\d.]+ [\d.]+V[\d.]+Q[\d.]+ ([\d.]+) ', svg)
    m = re.search(r'<text ([^>]*?)y="([\d.]+)"([^>]*)>((?:Fonte|Fotos):)', svg)
    if not card or not m:
        return svg
    fundo, y = float(card.group(1)), float(m.group(2))
    alvo = fundo + folga
    if y >= alvo - 0.5:
        return svg
    return svg.replace(m.group(0), f'<text {m.group(1)}y="{alvo:.2f}"{m.group(3)}>{m.group(4)}', 1)


def fonte_em_duas_linhas(svg: str, h: float) -> tuple[str, float]:
    """Se a linha de fonte (com os créditos das fotos) não couber no corpo de 12 px, quebra em duas linhas no " · ",
    em vez de apertar as letras (regra do editor, 22/11/2026)."""
    vb = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.]+) ([\d.]+)"', svg)
    m = re.search(r'<text x="([\d.]+)" y="([\d.]+)" font-size="12"([^>]*)>((?:Fotos|Fonte):[^<]*)</text>', svg)
    if not vb or not m:
        return svg, h
    vx, vy, vw, vh = map(float, vb.groups())
    x, y, resto, txt = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
    if len(html.unescape(txt)) * 12 * 0.43 <= vw - 2 * (x - vx) or " · " not in txt:
        return svg, h
    a, b = txt.split(" · ", 1)
    duas = (f'<text x="{m.group(1)}" y="{y:.2f}" font-size="12"{resto}>{a}</text>'
            f'<text x="{m.group(1)}" y="{y + 15:.2f}" font-size="12"{resto}>{b}</text>')
    svg = svg.replace(m.group(0), duas, 1)
    nh = vh + 15
    svg = svg.replace(vb.group(0), f'viewBox="{vb.group(1)} {vb.group(2)} {vb.group(3)} {nh:g}"', 1)
    svg = re.sub(r'(<svg[^>]*?) height="[\d.]+"', lambda k: f'{k.group(1)} height="{nh:g}"', svg, count=1)
    return svg, h * nh / vh


def sem_cerco(svg: str, largura: int) -> tuple[str, float, float]:
    """Tira o fundo branco e a margem externa do NXtab; devolve o SVG recortado no box + fonte."""
    pad = 12 if largura < 500 else 20
    svg = svg.replace('<rect width="100%" height="100%" fill="#FFFFFF"/>', '', 1)
    m = re.search(r'viewBox="0 0 (\d+) ([\d.]+)"', svg)
    alto = float(m.group(2))
    largura = int(m.group(1))  # a peça pode sair mais estreita que a vaga (linha do tempo vertical)
    ultimos = [float(y) for y in re.findall(r'<text [^>]*y="([\d.]+)"', svg)]
    base = (max(ultimos) + 5) if ultimos else alto - pad
    w, h = largura - 2 * pad, round(base - pad, 2)
    svg = re.sub(r'viewBox="0 0 \d+ [\d.]+" width="\d+" height="\d+"',
                 f'viewBox="{pad} {pad} {w} {h}" width="{w}" height="{h}"', svg, count=1)
    return svg, w, h


async def main(nxtab: Path, specs: Path, saida: Path) -> None:
    base = specs.resolve().parent
    saida.mkdir(parents=True, exist_ok=True)
    pecas = json.loads(specs.read_text(encoding="utf-8"))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1400, "height": 1000})
        await pg.goto(nxtab_ajustado(nxtab).as_uri(), wait_until="load")
        await pg.wait_for_timeout(2500)
        relatorio = []
        for g in pecas:
            vaga = g.get("vaga", "lateral")
            csv_original = g["csv"]
            larg, exibe = VAGAS[vaga]
            g = {**g, "largura": larg, "fotos_dados": fotos_da_linha(g, base), "fundo_dados": fundo_da_peca(g, base)}
            if g["fundo_dados"]:
                g["fundo"] = "custom"
            q = planejar_quebra(g)
            if q:   # o eixo vai até o segundo valor; a barra do maior encosta no fim do eixo e leva a quebra
                ticks = await pg.evaluate("v => revTicks(v)", q["segundo"] * 1.04)
                tmax = ticks[-1]
                q["teto_txt"] = f"{tmax * (1 - 1e-6):.7f}".replace(".", ",")
                dados = [list(r) for r in q["dados"]]; dados[q["linha"]][q["coluna"]] = q["teto_txt"]
                g["csv"] = "\n".join([";".join(q["cab"])] + [";".join(r) for r in dados])
                nota = g.get("nota_quebra") or f'{q["rotulo"]}: barra fora de escala.'
                g["fonte"] = (g.get("fonte", "").rstrip() + " " + nota).strip()
            r = await pg.evaluate(JS, {k: v for k, v in g.items() if k != "fotos"})
            svg_bruto = aplicar_quebra(r["svg"], q) if q else r["svg"]
            # linha de fonte no mesmo corpo em toda peça (12 px, que saem a 6,2 pt): nunca encolhida para caber (regra do editor, 22/11/2026)
            svg_bruto = re.sub(r'(<text [^>]*?)font-size="[\d.]+"([^>]*?)( textLength="[\d.]+" lengthAdjust="[a-zA-Z]+")?>(Fonte:|Fotos:)',
                               r'\1font-size="12"\2>\4', svg_bruto, count=1)
            svg_bruto = linha_de_apoio_myriad(svg_bruto, g.get("subtitulo", ""))
            svg_bruto = afastar_fonte(svg_bruto)
            svg_bruto = aplicar_realces(svg_bruto, g.get("realces"))
            svg, w, h = sem_cerco(svg_bruto, larg)
            svg, h = fonte_em_duas_linhas(svg, h)
            svg = aba_padrao(svg, w, exibe)
            svg = ids_unicos(svg, g["id"])
            svg = svg.replace('<svg xmlns="http://www.w3.org/2000/svg"',
                              f'<svg aria-label="{g["titulo"]}" xmlns="http://www.w3.org/2000/svg"', 1)
            gid = g["id"]
            (saida / f"{gid}.svg").write_text(svg, encoding="utf-8")
            (saida / f"{gid}.csv").write_text(csv_original.strip() + "\n", encoding="utf-8-sig")   # dados para o time (Textos/)
            web = None
            if r.get("web"):   # versão para o site: animada e responsiva, entra na matéria por iframe
                (saida / f"{gid}.web.html").write_text(aplicar_realces(r["web"], g.get("realces")), encoding="utf-8")
                if g.get("publicar") and os.environ.get("NX_R2_ENDPOINT"):   # sem as chaves, fica só o arquivo .web.html (a equipe usa o "Copiar HTML" do NXtab)
                    web = publicar_web(saida / f"{gid}.web.html", g.get("marca", "esb"), gid)
                    (saida / f"{gid}.iframe.html").write_text(web["iframe"], encoding="utf-8")
            (saida / f"{gid}.nxtab.json").write_text(json.dumps(r["project"], ensure_ascii=False, indent=1), encoding="utf-8")
            classe = "nxtab sobre" if vaga == "abertura" else "nxtab"
            figura = f'<figure class="{classe}" data-vaga="{vaga}" style="width:{exibe}px">{svg}</figure>'
            (saida / f"{gid}.html").write_text(figura, encoding="utf-8")
            relatorio.append({"id": gid, "vaga": vaga, "largura_na_pagina": exibe,
                              "altura_na_pagina": round(h * exibe / w), "escala": round(exibe / w, 3),
                              "web": web["url"] if web else None,
                              "quebra": (f'{q["rotulo"]} ({q["original"]}) fora de escala; eixo até {tmax:g}' if q else None)})
        # prévias com a Inter
        for g in pecas:
            svg = (saida / f'{g["id"]}.svg').read_text(encoding="utf-8")
            html = ('<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Inter+Tight:wght@100..900&family=Roboto+Condensed:wght@300..700&display=swap">'
                    '</head><body style="margin:0;background:#fff">' + svg + '</body></html>')
            tmp = saida / f'{g["id"]}.prev.html'; tmp.write_text(html, encoding="utf-8")
            await pg.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
            await (await pg.query_selector("svg")).screenshot(path=str(saida / f'{g["id"]}.png'))
            tmp.unlink()
        await b.close()
    print(json.dumps(relatorio, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    asyncio.run(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
