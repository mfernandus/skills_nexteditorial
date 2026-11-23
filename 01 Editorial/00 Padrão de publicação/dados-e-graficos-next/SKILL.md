---
name: "dados-e-graficos-next"
description: "Apoio da padrao-publicacao-next (seções 12 e 13): peça do NXtab decidida sozinha em toda matéria com dados, conferência reforçada dos números e dados atualizados na republicação."
---

# Gráficos no NXtab e dados na republicação — apoio do padrão Next

Estas são as seções 12 e 13 da skill `padrao-publicacao-next`, separadas em 17/11/2026 para economizar o plano (decisão do Mário Fernando): são carregadas sempre que a rotina identificar, sozinha, dados que pedem peça (gatilho na seção 12 do padrão, decisão de 23/11/2026), e sempre nas rotinas de republicação. Valem acima de qualquer rotina e de qualquer tarefa agendada, como se estivessem no padrão. Quando o texto abaixo cita "seção 4", "seção 5", "seção 9" ou "9.3", é da `padrao-publicacao-next`.

## 12. Gráficos, tabelas e infográficos: sempre no NXtab (decisão do Mário Fernando, 13/11/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada.** Toda tabela, gráfico ou infográfico que entra numa matéria dos sites sai do NXtab, o construtor de gráficos da Next (artefato "NXtab", slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`), na paleta do veículo. Nada de tabela HTML montada à mão, gráfico de matplotlib ou de outra biblioteca, imagem de IA com números ou print de outro site. Única exceção: o quadro da previsão do tempo, que sai do gerador da rotina `previsao-tempo-esbrasil`.

1. **Quando entra: decisão automática** (decisão do Mário Fernando, 23/11/2026). Vale para toda skill de notícias, atual ou futura. A rotina decide sozinha, sem perguntar e sem esperar que a pauta ou a própria rotina peça, e monta a peça no NXtab quando:
   - a fonte oficial publica o dado em tabela, gráfico ou infográfico: a peça é refeita no NXtab com os números da fonte, nunca como print nem cópia do desenho dela;
   - a matéria traz dados que se leem melhor numa peça: série no tempo, ranking, comparação entre itens, participação no todo, três a seis números-chave do assunto ou etapas em ordem;
   - a rotina pede "tabela" ou "tabela simples": ela sai do NXtab, num modelo `t-`.

   Não vira peça: número solto (fica só no texto), dado que muda no mesmo dia (horário de sessão, placar ao vivo, cotação do momento) e dado que não passou na conferência do item 5. No máximo duas peças por matéria. Na republicação, todo dado atualizado que couber num modelo vira peça (seção 13). Na dúvida entre peça e texto, faça a peça se os números passaram na conferência; se não passaram, fica o texto.
2. **Modelo pela natureza do dado** (biblioteca da revista no NXtab):
   - evolução no tempo: `c-percentual` (uma série, o último ou o maior valor em destaque) ou `c-colunas` (duas ou mais séries);
   - ranking ou comparação entre itens (municípios, estados, países, empresas, denominações): `c-barras`;
   - participação no todo: `c-rosca` (uma fatia em destaque) ou `v-leque` (várias fatias);
   - três a seis números-chave: `c-faixa` (números grandes) ou `c-lista` (box "em números");
   - tabela: `t-indicadores` (indicador e resultado), `t-comparativo` (várias colunas numéricas), `t-panorama` (indicador e valor), `t-descritiva` (item e explicação), `t-tres` (três colunas) ou `t-abertura` (título em frase);
   - etapas ou lista ordenada: `v-numerada`.
3. **Paleta do veículo.** Campo `marca`: `"esb"` na **ES Brasil** (portal 1: azul em degradê e destaque magenta) e `"com"` na Comunhão (portal 4: azul com o amarelo e o laranja da marca). Destinos ES usa `"des"` e Prócidade, `"pro"`. Matéria que vai aos dois portais leva uma peça para cada um, cada qual na sua marca. Nunca misture marcas numa peça.
4. **Regras da peça** (o NXtab e o script já aplicam; decisões do Mário Fernando de 20 a 22/11/2026):
   - título de todo infográfico (gráfico, tabela, linha do tempo) em **caixa alta**, no azul da marca e no peso mais forte (Inter Black);
   - linha de apoio logo abaixo do título em **Arial Narrow Bold**, num corpo maior que o texto da lista e das células (15 px nas peças estreitas e 16 px nas largas, contra 14 px da lista), sem quebra quando couber numa linha (decisão do Mário Fernando, 22/11/2026, que substituiu a Myriad Condensed light; o NXtab publicado já aplica, com Roboto Condensed Bold de reserva onde a Arial Narrow não estiver instalada), com entrelinha aberta para respirar (cerca de 1,34 do corpo; 1,4 na web) e um respiro de cerca de 10 px antes do corpo da peça (pedido do Mário Fernando, 22/11/2026; o NXtab publicado já aplica); o detalhe dos marcos da linha do tempo continua em Myriad Condensed;
   - linha de fonte e créditos em **Roboto Condensed**, sempre numa linha só; dados em Inter;
   - na **ES Brasil**, barrinha rosa no topo de toda peça;
   - peças um pouco achatadas e letras um pouco mais juntas; tabelas no desenho compacto aprovado na Retrospectiva (nem as linhas altas antigas, nem apertado demais); rosca compacta, com o percentual de todas as fatias na legenda; linha do tempo vertical estreita (até 560 px de desenho);
   - sem cerco branco e sem sombra; fonte colada embaixo do box; escala quebrada (//) quando o maior valor passa de duas vezes o segundo, com a nota "[item]: barra fora de escala."; nunca barra esticada nem escala logarítmica;
   - rótulos curtos; números com vírgula decimal e ponto de milhar, na unidade da fonte.
4.1. **Foto de fundo buscada a cada peça** (decisão do Mário Fernando, 22/11/2026). Toda peça com box leva no fundo, em cinza e a 5%, uma foto do NX Fotos que faça sentido com a informação do gráfico. Antes de gerar, busque no NX Fotos (`buscar`, `orientacao: "h"`) pelo assunto dos dados e pelo lugar (o que o gráfico mostra e onde; ex.: “culto igreja” para números de evangélicos, “navio porto de Vitória” para movimentação portuária), não só pela editoria. Escolha uma foto horizontal, com pelo menos 1.600 px, não oculta e sem marca de empresa em destaque; baixe a imagem de 1.600 px que a busca devolve (ou o original, com `link_do_original`) e passe no campo `fundo` da peça: `{"arquivo": "fundos/culto.jpg", "titulo": "Culto", "autor": "Fulano", "fonte": "NX Fotos"}`. Sem foto que faça sentido, use `"auto"` (o NXtab escolhe a foto do tema que reconhece: agro, portos, energia, indústria, rochas, construção, turismo, assistência rural, igreja e fé, educação, saúde, meio ambiente, política ou cidade). Vale para a **ES Brasil** e para as outras marcas. No NXtab aberto no Claude, o fundo “Automática” já busca no NX Fotos sozinho, pelo título.
5. **Conferência reforçada** (decisão do Mário Fernando, 23/11/2026). Como a peça nasce de decisão automática e vai ao ar sem revisão humana, nenhum número entra sem passar por estas seis etapas, nesta ordem. Elas não se pulam para economizar o plano.
   1. **Fonte aberta na rodada.** Todo valor vem da fonte oficial aberta com WebFetch (ou pela `raspagem-web-next`) nesta execução (seção 5): nunca de memória, de snippet de busca, de outro veículo ou da imagem de um gráfico. Quando a fonte oferece tabela, CSV ou API, copie os valores dali com código, sem redigitar.
   2. **Mesma régua.** Mesma métrica, mesma unidade, mesmo período e mesmo recorte em todas as linhas; série com fontes ou métodos diferentes não se mistura. Período no subtítulo ("em 2025, em US$ milhões") e fonte com o ano no campo `fonte` ("IBGE, Censo 2022."). Valor em reais de anos diferentes leva a nota de que a comparação é nominal.
   3. **Segunda leitura.** Abra a fonte de novo (a mesma página, sem refazer a busca) e anote o que ela diz, linha por linha, em `conferencia.json`, sem copiar do `pecas.json`: `{"<id da peça>": {"url": "https://...", "linhas": {"<rótulo>": ["<valor>", ...]}}}`, com os valores na ordem das colunas do csv.
   4. **Script de conferência.** `python3 conferir_pecas.py pecas.json conferencia.json texto.html` (script abaixo; `texto.html` é o `texto_html` da matéria salvo em arquivo, opcional). Ele barra valor da peça diferente da segunda leitura, número fora do padrão (vírgula decimal e ponto de milhar), fatias que não somam 100%, rótulo repetido, peça sem período, sem fonte, sem marca válida ou sem `"publicar": true`, e avisa ranking fora de ordem e valor da peça que não aparece no texto. Com ERRO, a peça não é gerada até ser corrigida.
   5. **Peça igual ao texto.** O número que está na peça e no texto é o mesmo, com o mesmo arredondamento e a mesma unidade. Título e linha de apoio não afirmam o que os números não mostram: "maior", "recorde", "dobrou", "primeiro lugar" só quando a conta prova.
   6. **Olho no PNG.** Depois de gerar, leia o PNG (Read) e compare cada valor desenhado com o `conferencia.json`, não com o csv: assim aparecem número cortado, rótulo trocado, vírgula lida como ponto e escala errada.

   Valor que não se confirma sai da peça; se a peça perde o sentido sem ele, ela não entra e a matéria vai ao ar com os números conferidos no texto. Nunca estime, nunca arredonde para fechar conta e nunca complete série com valor de outra fonte. Fontes oficiais que divergem: vale a primária, e a divergência vai para o resumo.
6. **Como gerar.** O kit é baixado uma vez por execução, e só se alguma matéria levar peça.
   - Ferramenta de artefatos `read_file` com `paths`: no NXtab (slug acima), `["index.html"]`, copiado para `nxtab.html`; no kit da Retrospectiva (slug `2662af95-77ba-43d3-8205-463326509342`), `["scripts/nxtab_grafico.py.txt"]`, copiado para `nxtab_grafico.py`. Sem a ferramenta de artefatos, use a pasta `retrospectiva-esbrasil/kit` do GitHub mfernandus/skills_nexteditorial.
   - `pip install --break-system-packages playwright`. O script usa o Chrome do sistema (`/usr/bin/google-chrome`); se o navegador não abrir, rode `python3 -m playwright install chromium`.
   - `pecas.json`: lista de peças com `id`, `modelo`, `vaga` ("site"), `marca`, `titulo`, `subtitulo`, `fonte`, `csv` (separador `;`, primeira linha de cabeçalho, ex.: `"País;US$ milhões\nEUA;3.120,5\nChina;1.050,2"`) e `fundo` (a foto do NX Fotos da 4.1) e, se precisar, `destaque`, `ordem` ("desc") e `quebra`.
   - Em cada peça do `pecas.json`, ponha também `"publicar": true`, para sair a versão para web (decisão do Mário Fernando, 21/11/2026). O script então sobe a peça animada e responsiva ao Cloudflare R2 da Next (bucket `nx-graficos`) em `https://nxtab.nxte.com.br/<marca>/<id>.html`, nas pastas esbrasil, comunhao, destinos, procidade e next, e grava `<id>.iframe.html` com o código para a matéria. A versão animada é obrigatória em toda peça, em todas as marcas (decisão do Mário Fernando, 22/11/2026). O script precisa de `pip install --break-system-packages boto3` e das variáveis `NX_R2_ACCESS_KEY`, `NX_R2_SECRET` e `NX_R2_ENDPOINT`. Se elas não estiverem no ambiente da rotina, leia a nota de memória `/areas/r2-graficos-nxtab.md` com `mcp__memory__memory_read` e passe os valores ao script só no comando que o roda, sem mostrar, ecoar nem gravar em arquivo: `NX_R2_ACCESS_KEY` = R2_ACCESS_KEY_ID, `NX_R2_SECRET` = R2_SECRET_ACCESS_KEY, `NX_R2_ENDPOINT` = o endpoint S3 da nota. Nunca pergunte ao Mário pelas chaves: elas estão sempre nessa nota. Nunca escreva a chave na skill, no resumo, no texto da matéria, no NX Feed, num artefato ou numa página (o repositório de skills é público e páginas e artefatos abrem para quem tem o link); artefato e matéria usam só o endereço público em nxtab.nxte.com.br, que não pede chave. Fique só com o PNG apenas se o envio falhar mesmo com as chaves da memória, e diga o erro no resumo.
   - Rode a conferência do item 5 (`conferir_pecas.py`) e só siga com 0 erro.
   - `python3 nxtab_site.py nxtab.html nxtab_grafico.py pecas.json pecas/` (script `nxtab_site.py` abaixo). Sai, por peça, `<id>.png` (1.520 px de largura), `<id>.svg`, `<id>.nxtab.json` (abre no NXtab para ajustes) e, com `publicar`, `<id>.web.html` e `<id>.iframe.html`. O relatório impresso pelo script traz o endereço público no campo `web`.
   - Olhe o PNG (Read) antes de subir, valor por valor contra o `conferencia.json` (item 5, etapa 6). Número cortado, rótulo quebrado, cor de outra marca ou valor errado: corrija e gere de novo uma vez, com o mesmo id; se o erro continuar, a peça não entra (item 8).
7. **Como entra na matéria.** Com a versão para web publicada, a peça entra no `texto_html` como iframe, logo depois do parágrafo que traz os dados: `<figure class="nxtab">` + o conteúdo de `<id>.iframe.html` + `</figure>`. No `style` do iframe, troque a altura de 480px pela `altura_na_pagina` do relatório mais 10 px, para a peça caber mesmo se o WordPress tirar o script que ajusta a altura sozinho. A mesma peça serve ao computador e ao celular, anima ao aparecer na tela e mostra o número ao toque. Depois de publicar, confira com `conferir_publicacao` ou `ver_materia` se o iframe continua no texto. Se o WordPress tiver tirado o iframe, edite a matéria e troque pela versão em imagem, abaixo. A versão em imagem também é a regra quando a peça não foi publicada na web: suba o PNG com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `titulo` = título da peça, `materia_id` quando houver) e `curl -T`, e ponha a URL do Studio que o envio devolve (como na 9.3) no `texto_html`, no mesmo lugar: `<figure class="nxtab"><img src="URL" alt="..." width="1520" height="ALTURA" /></figure>`. O PNG continua sendo gerado sempre, para o Instagram e para quando a peça precisar ir como imagem. O alt diz o dado principal numa frase ("Evangélicos são 26,9% da população brasileira no Censo 2022, segundo o IBGE"). Os números principais da peça também estão no texto, para a busca e para quem usa leitor de tela. A peça não substitui a imagem destacada (seção 9). O link de envio é de uso único: não mostre nem guarde.
8. **Se falhar** (artefato fora, Playwright ou navegador indisponível, envio recusado): a matéria vai ao ar sem a peça, com os números no texto, e o resumo registra em Pendências "peça do NXtab fora: [motivo]". Nunca troque por tabela ou gráfico feito de outro jeito.
9. **Resumo:** em "Publicadas", acrescente "com peça NXtab ([modelo]) · [N] valores conferidos em [fonte]" e, se ela entrou na versão para web, o endereço em nxtab.nxte.com.br. Peça que caiu na conferência vai em Pendências: "peça fora: dado não confirmado ([qual])".

Script (`nxtab_site.py`):

```python
"""Peças do NXtab para as matérias dos sites (padrão, seção 12).
python3 nxtab_site.py nxtab.html nxtab_grafico.py pecas.json pecas/"""
import asyncio, importlib.util, json, sys
from pathlib import Path
from playwright.async_api import async_playwright

nxtab, script, specs, saida = (Path(a) for a in sys.argv[1:5])
spec = importlib.util.spec_from_file_location("nxtab_grafico", script)
ng = importlib.util.module_from_spec(spec); spec.loader.exec_module(ng)
ng.VAGAS["site"] = (800, 760)          # coluna de texto dos sites

async def png():
    chrome = Path("/usr/bin/google-chrome")
    async with async_playwright() as p:
        b = await p.chromium.launch(**({"executable_path": str(chrome)} if chrome.exists() else {}))
        pg = await b.new_page(viewport={"width": 900, "height": 900}, device_scale_factor=2)
        for g in json.loads(specs.read_text(encoding="utf-8")):
            svg = (saida / f'{g["id"]}.svg').read_text(encoding="utf-8")
            await pg.set_content('<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap">'
                                 '</head><body style="margin:0;background:#fff"><div id="p" style="display:inline-block;background:#fff">'
                                 + svg + '</div></body></html>', wait_until="networkidle")
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await (await pg.query_selector("#p")).screenshot(path=str(saida / f'{g["id"]}.png'))
        await b.close()

asyncio.run(ng.main(nxtab, specs, saida))   # SVG e projeto, com as regras da casa
asyncio.run(png())                            # PNG de 1.520 px para a matéria
```

Script (`conferir_pecas.py`):

```python
"""Conferência automática das peças do NXtab antes de gerar (dados-e-graficos-next, 12.5).
python3 conferir_pecas.py pecas.json conferencia.json [texto.html]
Sai com código 1 se houver ERRO: corrija ou tire a linha/peça. AVISO: confira e decida."""
import json, re, sys
from pathlib import Path

NUM = re.compile(r"[-−]?\d[\d.]*(?:,\d+)?")
ANO = re.compile(r"\b(19|20)\d{2}\b")
MODELOS = {"c-percentual", "c-colunas", "c-barras", "c-rosca", "v-leque", "c-faixa", "c-lista",
           "t-indicadores", "t-comparativo", "t-panorama", "t-descritiva", "t-tres", "t-abertura",
           "v-numerada", "t-retro", "i-tempo", "i-tempo-pictos"}
MARCAS = {"esb", "com", "des", "pro"}
erros, avisos = [], []

def tokens(txt):
    return [t.replace("−", "-") for t in NUM.findall(str(txt))]

def formato_ok(t):
    """Vírgula decimal e ponto de milhar: 3.120,5 / 26,9 / 1.050 / 2025."""
    inteiro = t.lstrip("-").split(",")[0]
    return "." not in inteiro or re.fullmatch(r"\d{1,3}(\.\d{3})+", inteiro) is not None

def valor(t):
    return float(t.replace(".", "").replace(",", "."))

def ler_csv(txt):
    linhas = [l for l in str(txt).strip().split("\n") if l.strip()]
    return [c.strip() for c in linhas[0].split(";")], [[c.strip() for c in l.split(";")] for l in linhas[1:]]

pecas = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
conf = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 and Path(sys.argv[2]).exists() else {}
texto = set(tokens(re.sub(r"<[^>]+>", " ", Path(sys.argv[3]).read_text(encoding="utf-8")))) if len(sys.argv) > 3 else None

for p in pecas:
    pid = p.get("id", "?"); E = lambda m: erros.append(f"{pid}: {m}"); A = lambda m: avisos.append(f"{pid}: {m}")
    for campo in ("titulo", "subtitulo", "fonte", "csv"):
        if not str(p.get(campo, "")).strip(): E(f"campo '{campo}' vazio")
    if p.get("marca") not in MARCAS: E(f"marca '{p.get('marca')}' inválida (esb, com, des, pro)")
    if p.get("modelo") not in MODELOS: A(f"modelo '{p.get('modelo')}' fora da lista conhecida")
    if p.get("publicar") is not True: E("falta \"publicar\": true (versão animada é obrigatória)")
    if not ANO.search(f"{p.get('subtitulo', '')} {p.get('fonte', '')}"): E("período/ano não aparece no subtítulo nem na fonte")
    if not str(p.get("csv", "")).strip(): continue
    cab, linhas = ler_csv(p["csv"])
    if not linhas: E("csv sem linhas de dados"); continue
    for i, l in enumerate(linhas, 2):
        if len(l) != len(cab): E(f"linha {i} tem {len(l)} colunas, o cabeçalho tem {len(cab)}")
    rotulos = [l[0] for l in linhas]
    for r in {r for r in rotulos if rotulos.count(r) > 1}: E(f"rótulo repetido: '{r}'")
    for l in linhas:
        for t in tokens(";".join(l[1:])):
            if not formato_ok(t): E(f"'{t}' em '{l[0]}' fora do padrão (vírgula decimal, ponto de milhar)")
            elif re.fullmatch(r"-?\d{1,3},\d{3}", t): A(f"'{t}' em '{l[0]}': é decimal mesmo ou era milhar?")
    mod = p.get("modelo", "")
    primeiros = [tokens(";".join(l[1:])) for l in linhas]
    vals = [valor(t[0]) for t in primeiros if t and formato_ok(t[0])]
    if mod in ("c-rosca", "v-leque") and vals:
        pct = "%" in p["csv"] or all(v <= 100 for v in vals)
        if pct and not 99.5 <= sum(vals) <= 100.5:
            E(f"fatias somam {sum(vals):.1f}% (esperado 100%); se for arredondamento da fonte, diga na nota")
    if mod == "c-barras" and p.get("ordem") != "desc" and len(vals) == len(linhas) and vals != sorted(vals, reverse=True):
        A("ranking fora da ordem decrescente e sem \"ordem\": \"desc\"")
    if mod in ("c-faixa", "c-lista") and not 3 <= len(linhas) <= 6: A(f"{len(linhas)} números-chave (o modelo pede de 3 a 6)")
    # dupla conferência: cada linha da peça contra o que foi lido de novo na fonte
    c = conf.get(pid)
    if not c: E("sem registro em conferencia.json (url e valores relidos na fonte)"); continue
    if not str(c.get("url", "")).startswith("http"): E("conferencia.json sem url da fonte oficial")
    fonte_linhas = c.get("linhas", {})
    for l in linhas:
        peca_t = tokens(";".join(l[1:]))
        if not peca_t: continue
        if l[0] not in fonte_linhas: E(f"'{l[0]}' não foi relido na fonte"); continue
        fonte_t = tokens(";".join(map(str, fonte_linhas[l[0]])))
        try:
            iguais = [valor(a) for a in peca_t] == [valor(b) for b in fonte_t]
        except ValueError:
            iguais = peca_t == fonte_t
        if not iguais: E(f"'{l[0]}': peça {peca_t} ≠ fonte {fonte_t}")
    if texto is not None:
        fora = [t for l in linhas for t in tokens(";".join(l[1:])) if not ANO.fullmatch(t) and t not in texto]
        if fora: A(f"{len(fora)} valor(es) da peça não aparecem no texto (confira arredondamento): {', '.join(fora[:5])}")

for m in erros: print("ERRO  ", m)
for m in avisos: print("AVISO ", m)
print(f"{len(pecas)} peça(s) · {len(erros)} erro(s) · {len(avisos)} aviso(s)")
sys.exit(1 if erros else 0)
```

## 13. Republicação: dados sempre atualizados (decisão do Mário Fernando, 13/11/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada**, para toda matéria que volta ao ar: `acervo-esbrasil`, `acervo-comunhao`, `artigos-acervo-esbrasil`, `artigos-acervo-comunhao`, `artigos-acervo-next` e as que vierem.

1. **Procure a atualização de todo dado datado do texto**, não só dos que sustentam a conclusão: estatística, ranking, população, preço, valor em reais, percentual, número de igrejas, alunos ou empresas, cargo e situação das pessoas citadas. Fonte oficial mais recente, aberta com WebFetch (seção 5); mesma métrica e mesmo recorte; valor em reais com a observação de que a comparação é nominal. Dado histórico (data de fundação, ano de um fato) só se confere.
2. **Reportagem e matéria da redação** (rotinas de acervo): o número atual vai para o texto do repórter, com fonte e ano, e a mudança fica registrada na Nota da Redação, como a rotina já manda. Dentro de citação, a fala fica como foi dita e o número atual vai para a Nota.
3. **Texto assinado** (rotinas de artigos do acervo): o texto do autor continua intocado (decisão de 30/10/2026). O dado atualizado vai na Nota de contexto, com fonte e ano, sempre que o artigo citar número que tem versão mais nova, mesmo que o texto se entenda sem a nota. A regra de rejeição da rotina continua: se o número novo derruba o argumento, troque de artigo.
4. **Peça do NXtab.** Dado atualizado que cabe num modelo da seção 12 vira peça, na paleta do portal. Sempre que der, a peça mostra o antes e o depois (o número da época da publicação original e o atual, cada um com o ano). Os dois passam pela conferência reforçada (seção 12, item 5): o antigo, relido na matéria original ou na série histórica da mesma fonte; o atual, na fonte oficial mais recente. Na reportagem, ela entra logo depois do trecho atualizado; no texto assinado, junto da Nota de contexto, nunca no meio do texto do autor.
5. **Sem atualização possível** (a fonte parou de publicar, não há recorte equivalente): siga a regra da rotina (tirar do texto o que não pesa na conclusão ou deixar o ano bem claro) e registre no resumo.
6. **Resumo:** item "Dados atualizados", com antigo → atual (fonte e ano) e se virou peça.

## Modelo recomendado
- Nível: Sonnet
- Nota: 6/12 (raciocínio 1, fontes 1, texto 0, números 1, fluxo 2, risco 1)
- Motivo: decide a peça por critérios escritos e confere com script e segunda leitura; publica direto e roda código, o que barra o Haiku.
- Teste: não testado, primeira execução monitorada.
- Subir para Opus se: um número errado passar pela conferência e for ao ar, ou se a rotina passar a cruzar várias fontes para montar a mesma série.