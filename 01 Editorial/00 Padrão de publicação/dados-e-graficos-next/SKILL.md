---
name: "dados-e-graficos-next"
description: "Apoio da padrao-publicacao-next (seções 12 e 13): gráficos, tabelas e infográficos no NXtab e dados atualizados na republicação. Carregar antes de montar qualquer peça e em toda republicação."
---

# Gráficos no NXtab e dados na republicação — apoio do padrão Next

Estas são as seções 12 e 13 da skill `padrao-publicacao-next`, separadas em 17/11/2026 para economizar o plano (decisão do Mário Fernando): só são carregadas quando a rodada vai montar tabela, gráfico ou infográfico, e sempre nas rotinas de republicação. Valem acima de qualquer rotina e de qualquer tarefa agendada, como se estivessem no padrão. Quando o texto abaixo cita "seção 4", "seção 5", "seção 9" ou "9.3", é da `padrao-publicacao-next`.

## 12. Gráficos, tabelas e infográficos: sempre no NXtab (decisão do Mário Fernando, 13/11/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada.** Toda tabela, gráfico ou infográfico que entra numa matéria dos sites sai do NXtab, o construtor de gráficos da Next (artefato "NXtab", slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`), na paleta do veículo. Nada de tabela HTML montada à mão, gráfico de matplotlib ou de outra biblioteca, imagem de IA com números ou print de outro site. Única exceção: o quadro da previsão do tempo, que sai do gerador da rotina `previsao-tempo-esbrasil`.

1. **Quando entra.** Sempre que a matéria tiver dados que se leem melhor numa peça: série no tempo, ranking, comparação entre itens, participação no todo ou três a seis números-chave do assunto. Um número solto fica só no texto. No máximo duas peças por matéria. Na republicação, todo dado atualizado que couber num modelo vira peça (seção 13).
2. **Modelo pela natureza do dado** (biblioteca da revista no NXtab):
   - evolução no tempo: `c-percentual` (uma série, o último ou o maior valor em destaque) ou `c-colunas` (duas ou mais séries);
   - ranking ou comparação entre itens (municípios, estados, países, empresas, denominações): `c-barras`;
   - participação no todo: `c-rosca` (uma fatia em destaque) ou `v-leque` (várias fatias);
   - três a seis números-chave: `c-faixa` (números grandes) ou `c-lista` (box "em números");
   - tabela: `t-indicadores` (indicador e resultado), `t-comparativo` (várias colunas numéricas), `t-panorama` (indicador e valor), `t-descritiva` (item e explicação), `t-tres` (três colunas) ou `t-abertura` (título em frase);
   - etapas ou lista ordenada: `v-numerada`.
3. **Paleta do veículo.** Campo `marca`: `"esb"` na **ES Brasil** (portal 1: azul em degradê e destaque magenta) e `"com"` na Comunhão (portal 4: azul com o amarelo e o laranja da marca). Destinos ES usa `"des"` e Prócidade, `"pro"`. Matéria que vai aos dois portais leva uma peça para cada um, cada qual na sua marca. Nunca misture marcas numa peça.
4. **Regras da peça** (o script já aplica): Inter, título em peso 900 e subtítulo em 300, em caixa alta e baixa; sem cerco branco e sem sombra; fonte colada embaixo do box; escala quebrada (//) quando o maior valor passa de duas vezes o segundo, com a nota "[item]: barra fora de escala."; nunca barra esticada nem escala logarítmica. Campo `fundo`: `"none"` por padrão; `"auto"` só na **ES Brasil** e quando o assunto for um dos temas de foto do NXtab (construção, agro, portos, indústria, energia, rochas, turismo, cidade). Rótulos curtos; números com vírgula decimal e ponto de milhar, na unidade da fonte.
5. **Dado conferido.** A peça só leva número conferido na fonte oficial aberta com WebFetch (seção 5), igual ao do texto. Período no subtítulo ("em 2025, em US$ milhões") e fonte no campo `fonte` ("IBGE, Censo 2022."). Número não confirmado não entra.
6. **Como gerar.** O kit é baixado uma vez por execução, e só se alguma matéria levar peça.
   - Ferramenta de artefatos `read_file` com `paths`: no NXtab (slug acima), `["index.html"]`, copiado para `nxtab.html`; no kit da Retrospectiva (slug `2662af95-77ba-43d3-8205-463326509342`), `["scripts/nxtab_grafico.py.txt"]`, copiado para `nxtab_grafico.py`. Sem a ferramenta de artefatos, use a pasta `retrospectiva-esbrasil/kit` do GitHub mfernandus/skills_nexteditorial.
   - `pip install --break-system-packages playwright`. O script usa o Chrome do sistema (`/usr/bin/google-chrome`); se o navegador não abrir, rode `python3 -m playwright install chromium`.
   - `pecas.json`: lista de peças com `id`, `modelo`, `vaga` ("site"), `marca`, `titulo`, `subtitulo`, `fonte` e `csv` (separador `;`, primeira linha de cabeçalho, ex.: `"País;US$ milhões\nEUA;3.120,5\nChina;1.050,2"`) e, se precisar, `destaque`, `ordem` ("desc"), `fundo` e `quebra`.
   - Em cada peça do `pecas.json`, ponha também `"publicar": true`, para sair a versão para web (decisão do Mário Fernando, 21/11/2026). O script então sobe a peça animada e responsiva ao Cloudflare R2 da Next (bucket `nx-graficos`) em `https://nxtab.nxte.com.br/<marca>/<id>.html`, nas pastas esbrasil, comunhao, destinos, procidade e next, e grava `<id>.iframe.html` com o código para a matéria. Ele precisa de `pip install --break-system-packages boto3` e das variáveis de ambiente `NX_R2_ACCESS_KEY`, `NX_R2_SECRET` e `NX_R2_ENDPOINT`, que vêm do ambiente da rotina. Nunca escreva a chave na skill, no resumo, no texto da matéria nem no NX Feed. Sem as variáveis, tire o `publicar` e siga só com o PNG.
   - `python3 nxtab_site.py nxtab.html nxtab_grafico.py pecas.json pecas/` (script abaixo). Sai, por peça, `<id>.png` (1.520 px de largura), `<id>.svg`, `<id>.nxtab.json` (abre no NXtab para ajustes) e, com `publicar`, `<id>.web.html` e `<id>.iframe.html`. O relatório impresso pelo script traz o endereço público no campo `web`.
   - Olhe o PNG (Read) antes de subir. Número cortado, rótulo quebrado, cor de outra marca ou valor errado: corrija e gere de novo uma vez.
7. **Como entra na matéria.** Com a versão para web publicada, a peça entra no `texto_html` como iframe, logo depois do parágrafo que traz os dados: `<figure class="nxtab">` + o conteúdo de `<id>.iframe.html` + `</figure>`. No `style` do iframe, troque a altura de 480px pela `altura_na_pagina` do relatório mais 10 px, para a peça caber mesmo se o WordPress tirar o script que ajusta a altura sozinho. A mesma peça serve ao computador e ao celular, anima ao aparecer na tela e mostra o número ao toque. Depois de publicar, confira com `conferir_publicacao` ou `ver_materia` se o iframe continua no texto. Se o WordPress tiver tirado o iframe, edite a matéria e troque pela versão em imagem, abaixo. A versão em imagem também é a regra quando a peça não foi publicada na web: suba o PNG com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `titulo` = título da peça, `materia_id` quando houver) e `curl -T`, e ponha a URL do Studio que o envio devolve (como na 9.3) no `texto_html`, no mesmo lugar: `<figure class="nxtab"><img src="URL" alt="..." width="1520" height="ALTURA" /></figure>`. O PNG continua sendo gerado sempre, para o Instagram e para quando a peça precisar ir como imagem. O alt diz o dado principal numa frase ("Evangélicos são 26,9% da população brasileira no Censo 2022, segundo o IBGE"). Os números principais da peça também estão no texto, para a busca e para quem usa leitor de tela. A peça não substitui a imagem destacada (seção 9). O link de envio é de uso único: não mostre nem guarde.
8. **Se falhar** (artefato fora, Playwright ou navegador indisponível, envio recusado): a matéria vai ao ar sem a peça, com os números no texto, e o resumo registra em Pendências "peça do NXtab fora: [motivo]". Nunca troque por tabela ou gráfico feito de outro jeito.
9. **Resumo:** em "Publicadas", acrescente "com peça NXtab ([modelo])" e, se ela entrou na versão para web, o endereço em nxtab.nxte.com.br.

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

## 13. Republicação: dados sempre atualizados (decisão do Mário Fernando, 13/11/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada**, para toda matéria que volta ao ar: `acervo-esbrasil`, `acervo-comunhao`, `artigos-acervo-esbrasil`, `artigos-acervo-comunhao`, `artigos-acervo-next` e as que vierem.

1. **Procure a atualização de todo dado datado do texto**, não só dos que sustentam a conclusão: estatística, ranking, população, preço, valor em reais, percentual, número de igrejas, alunos ou empresas, cargo e situação das pessoas citadas. Fonte oficial mais recente, aberta com WebFetch (seção 5); mesma métrica e mesmo recorte; valor em reais com a observação de que a comparação é nominal. Dado histórico (data de fundação, ano de um fato) só se confere.
2. **Reportagem e matéria da redação** (rotinas de acervo): o número atual vai para o texto do repórter, com fonte e ano, e a mudança fica registrada na Nota da Redação, como a rotina já manda. Dentro de citação, a fala fica como foi dita e o número atual vai para a Nota.
3. **Texto assinado** (rotinas de artigos do acervo): o texto do autor continua intocado (decisão de 30/10/2026). O dado atualizado vai na Nota de contexto, com fonte e ano, sempre que o artigo citar número que tem versão mais nova, mesmo que o texto se entenda sem a nota. A regra de rejeição da rotina continua: se o número novo derruba o argumento, troque de artigo.
4. **Peça do NXtab.** Dado atualizado que cabe num modelo da seção 12 vira peça, na paleta do portal. Sempre que der, a peça mostra o antes e o depois (o número da época da publicação original e o atual, cada um com o ano). Na reportagem, ela entra logo depois do trecho atualizado; no texto assinado, junto da Nota de contexto, nunca no meio do texto do autor.
5. **Sem atualização possível** (a fonte parou de publicar, não há recorte equivalente): siga a regra da rotina (tirar do texto o que não pesa na conclusão ou deixar o ano bem claro) e registre no resumo.
6. **Resumo:** item "Dados atualizados", com antigo → atual (fonte e ano) e se virou peça.