# Prompt da Retrospectiva 2026 · revista ES Brasil (versão 13, 25/11/2026)

**Use de preferência a skill** `retrospectiva-esbrasil` (arquivo `02-skills/retrospectiva-esbrasil.zip`). Este prompt é o mesmo texto da skill, para quem não puder instalá-la: cole o documento inteiro numa conversa nova do Claude e peça o capítulo.

**O que mudou na versão 13:** o prompt deixou de ser um texto separado e passou a ser cópia fiel da skill. A versão 12 ainda trazia regras antigas, que a skill já tinha trocado: QR Code na abertura, intertítulos e títulos de peça com caixa alta errada, box do ES em Números com indicadores e QR, capacidades de página antigas, lateral de 55 mm, datas de 29/11, 03/12 e 09/12. Agora as duas fontes dizem a mesma coisa. Os kits (scripts, NXtab, modelo das páginas) estão na pasta `kit/` da skill; quem usar só o prompt baixa o kit do pacote da equipe.

---

# Retrospectiva 2026 da revista ES Brasil

Um único fluxo para **todas as editorias** da Retrospectiva (setores econômicos, infraestrutura, economia geral, política, políticas públicas, municípios, turismo e cultura, meio ambiente e inovação). Baseado no prompt universal v10 (13/10/2026). O que é próprio de cada tema (números, fotos, marcos, aspas) entra no dossiê e nas páginas, nunca nesta skill.

**Edição:** ESB 238 (204 páginas). As datas valem sempre pelo calendário executivo do NX Pages (`get_calendario_executivo`); em 25/11/2026 eram: entrega de textos 03/12 · diagramação 04/12 · fechamento da diagramação, fechamento comercial e entrega de material 10/12 · gráfica 11/12 · circulação impressa 14/12 · digital 16/12/2026. Confira no NX Pages antes de citar qualquer prazo.

**Quem decide (desde 23/11/2026):** a equipe toca os capítulos sem depender do Mário Fernando; a palavra final (aprovação, cortes, fotos, mudança de regra) é da Kamila, da produção. A versão animada dos gráficos para o site sai pelo NXtab publicado (Exportar → Senha da equipe → Publicar na web), sem chaves do R2 para a equipe.

O trabalho tem três momentos:
1. **Gerar o capítulo** (etapas 0 a 9): ficha, apuração, banco de aspas, páginas no formato da revista.
2. **Aprovação do editor** das páginas.
3. **Pacote do InDesign** (etapa 10): só depois da aprovação, e só depois de perguntar.

## Kit da skill (modelo das páginas e scripts)

O kit (modelo das páginas, base da revista e scripts) vai junto com a skill, na pasta `kit/` ao lado deste SKILL.md, quando ela é instalada pelo pacote .zip ou pelo GitHub (https://github.com/mfernandus/skills_nexteditorial, pasta `retrospectiva-esbrasil`). Antes da etapa 7b (montagem das páginas) e da etapa 10, copie essa pasta `kit/` para a pasta de trabalho. Ela traz `scripts/` (exportar_indesign.py, idml.py, extrair.js, embutir_imagens.py, nxtab_grafico.py), `assets/` (modelo-capitulo.html, grade-esb2026.css, base-retrospectiva-2026-v5.idml, selo-retrospectiva.png, logo-es-brasil.png, logo-es-em-numeros.png) e `nxtab.html`, uma cópia do NXtab. O NXtab mais recente fica no artefato público “NXtab” (https://claude.ai/artifact/G5Zau8SX9BaWydqLmndR7Z): se a ferramenta de artefatos estiver disponível, baixe o `index.html` dele para `kit/nxtab.html`; senão, use a cópia do kit. As regras visuais de 22/11/2026 (títulos em caixa alta e azul, Roboto Condensed, rosca compacta, linha do tempo vertical estreita, fundo buscado no NX Fotos) pedem as versões de 22/11/2026 do NXtab e do `nxtab_grafico.py` (campo `fundo` com foto): se `grep -q 'fundo_da_peca' kit/scripts/nxtab_grafico.py` falhar ou o `kit/nxtab.html` não tiver `revBgAutoFetch`, baixe os dois dos artefatos, como no passo 1 abaixo.

Se a skill estiver instalada sem a pasta `kit/`, baixe o kit do artefato **“Retrospectiva 2026 · kit do exportador InDesign”**, slug `2662af95-77ba-43d3-8205-463326509342`:

1. Chame a ferramenta de artefatos `read_file` com esse slug e `paths`: `scripts/exportar_indesign.py.txt`, `scripts/extrair.js`, `scripts/idml.py.txt`, `scripts/embutir_imagens.py.txt`, `scripts/nxtab_grafico.py.txt`, `assets/modelo-capitulo.html`, `assets/grade-esb2026.css`, `assets/base-retrospectiva-2026-v5.idml.b64.txt`, `assets/selo-retrospectiva.png`, `assets/logo-es-brasil.png`, `assets/logo-es-em-numeros.png`. A base da revista vai em base64 porque o artefato não serve `.idml`; o exportador a restaura sozinho em `kit/assets/base-retrospectiva-2026-v5.idml`. Se o kit ainda trouxer `base-materia-esb2026-inter.idml`, ele é anterior a 21/11/2026: baixe o kit de novo.
2. Copie cada arquivo salvo para `kit/` na pasta de trabalho, com o mesmo caminho, tirando o `.txt` final dos `.py` (`kit/scripts/exportar_indesign.py`, `kit/scripts/idml.py`, `kit/scripts/embutir_imagens.py`, `kit/scripts/nxtab_grafico.py`, `kit/scripts/extrair.js`, `kit/assets/...`). Para os gráficos, baixe também o NXtab, o construtor de gráficos da Next: `read_file` no artefato “NXtab”, slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`, com `paths: ["index.html"]`, e copie para `kit/nxtab.html`.
3. Dependências: `pip install --break-system-packages playwright pymupdf pillow openpyxl python-docx segno` e um Chrome ou Chromium (`python3 -m playwright install chromium` se não houver Chrome no sistema).
4. Se nada disso estiver disponível, use o .zip da skill (`retrospectiva-esbrasil.zip`) do pacote da equipe (pasta do Drive “Retrospectiva 2026 · pacote da equipe”), que já traz o kit.

**Fontes do texto (desde 23/11/2026):** a família Minion Pro (16 arquivos .otf, enviados pelo Mário Fernando em `Minion.rar`) fica em `kit/assets/fonts/` do .zip da skill. Se a pasta não vier, peça o `Minion.rar` ao Mário e extraia com `pip install --break-system-packages libarchive-c` e `libarchive.extract_file` (não há unrar no ambiente). A Minion é fonte licenciada da Adobe: nunca a publique em artefato, página, repositório público ou pasta compartilhada; ela vai só embutida no PDF de prova e no pacote do InDesign.

Ao melhorar um script, atualize o kit nos três lugares: o artefato do kit (os `.py` vão com `.txt` no fim e a base em base64, porque o artefato não serve `.py` nem `.idml`), a pasta `kit/` do GitHub e o .zip da skill.

## Etapa 0 · Perguntas iniciais (antes de qualquer pesquisa)

**1. Pergunte numa única mensagem**, de preferência com perguntas de múltipla escolha e espaço para resposta livre:
1. **Editoria e tema:** ofereça as editorias da tabela “Nível e tamanho por tema” que ainda não foram feitas, mais a resposta livre. Pela resposta, identifique o **perfil da editoria** (tabela “Perfis de editoria”, A a I) e mostre-o na ficha. Se o tema couber em dois perfis, use o principal e some as fontes do outro.
2. **Importância:** nível do tema (1 · vertical âncora; 2 · vertical de apoio; 3 · editoria do caderno; 4 · tema curto). Mostre o nível sugerido pela tabela e pergunte se o tema tem edição especial, série ou plataforma da Next Editorial em 2025–2026 (isso sobe o nível).
3. **Tamanho:** caracteres com espaços de texto corrido. Ofereça a faixa do nível como opção recomendada.
4. **Número de páginas:** ofereça o número calculado pelo tamanho e o do espelho do NX Pages, se houver.

Na mesma mensagem, peça (opcionais, com padrão): **repórter** (padrão: “Por [repórter]” em rosa), **corte de dados** (padrão: janeiro a outubro de 2026 × mesmo período de 2025) e **observações do editor** (fonte, personagem ou ângulo obrigatório).

**2. Regras para completar e conferir as respostas**
- Em branco ou “você decide”: usar o padrão da tabela “Nível e tamanho por tema” e dizer qual foi usado.
- Tema fora da tabela: classificar pelo critério de nível (vertical própria com especial → 1; série, anuário ou plataforma → 2; editoria relevante sem vertical → 3; panorama com um indicador central → 4) e propor nível e perfil.
- **Conferir páginas × tamanho** pela capacidade da etapa 7b (grade da revista, corpo 11/12, aspas no texto, sem olhos): 1 página ≈ 2.300; 2 ≈ 4.000; 3 ≈ 6.300; 4 ≈ 9.100; 5 ≈ 11.200; 6 ≈ 13.300 caracteres. Para 3 páginas ou mais: 2.000 (abertura) + 1.950 (linha do tempo) + 2.350 (fechamento) + 2.800 por página interna só com foto, ou cerca de 2.100 quando ela traz a tabela padrão ou a tabela de eventos.
- Se o tamanho couber nas páginas com tolerância de ±300 caracteres, seguir. Se não couber, **não escolher sozinho**: mostrar as duas saídas (ajustar o texto às páginas, com o novo tamanho; ou ajustar as páginas ao texto, com o novo número) e perguntar.
- Se só um dos dois vier informado, calcular o outro. Tamanho entre duas faixas: níveis 1 e 2 arredondam páginas para cima; 3 e 4, para baixo.
- Tamanho ou páginas fora da faixa do nível: avisar em uma linha e seguir com o que o editor pediu.
- Mais de 6 páginas: aceitar, repetindo os modelos 2 e 4, e avisar que o espelho precisa confirmar.

**3. Devolver a ficha do capítulo e esperar o “ok”.** Depois do “ok”, seguir todas as etapas sem novas perguntas; o que faltar vira pendência em rosa.

| Campo | Valor |
|---|---|
| Editoria e tema | |
| Perfil da editoria | (ex.: A · setor econômico) |
| Nível e critério | (ex.: 1 · vertical âncora, especial ed. 235) |
| Tamanho do texto corrido | (ex.: 12.500 caracteres com espaços, faixa do nível 11.000–13.500) |
| Páginas e modelos | (ex.: 5 · abertura, dados, contexto, eventos, fechamento) |
| Elementos obrigatórios do nível | (tabela padrão, nº de gráficos, tabela de eventos, artigo assinado, box, linha do tempo) |
| Aspas previstas | (nível 1: 10 a 16; níveis 2 e 3: pelo menos 6; nível 4: 2 a 4), com quem dá aspas segundo o perfil |
| Regras específicas do perfil | (ex.: Política: equilíbrio entre os campos; sem aspa montada; sem publieditorial) |
| Edição especial a usar | (nº e mês, ou “verificar na etapa 2”) |
| Repórter | |
| Corte de dados | |
| Observações do editor | |

**Parâmetros fixos**
- Números de página e anúncios vêm do espelho do NX Pages; sem espelho, numerar “00” em rosa.
- Corte de dados: se a fonte oficial ainda não tiver outubro, usar o último mês disponível, dizer o período no texto e marcar em rosa para atualizar.
- Pendências (dado não divulgado, entrevista, foto em alta) ficam em rosa.
- **Código de cores da prova** (sai na versão final): rosa = pendência; azul-claro = aspa publicada, a validar pela produção; laranja = aspa montada, a confirmar com a fonte; verde-claro = número trocado por divulgação mais recente (etapa 3d), a conferir pelo editor.
- Título, linha fina, legendas, tabelas e boxes não contam no tamanho do texto corrido.

## Etapa 1 · Referências visuais

**Prioridade:** (1) infográficos da **ES Brasil** em 2026 (especiais do ano, como o Especial Rochas, ed. 235); (2) Retrospectiva 2025; (3) Retrospectiva 2024, liberada para gráficos e tabelas relevantes que 2025 e 2026 não tenham; (4) 2023 só como série histórica (base NEIA).

**Estrutura de página: Retrospectiva 2025 (edição 231)** — https://esbrasil.com.br/edicao-231-retrospectiva/
- **Cabeçalho da página-mestre da base V5** (“A-Master” de “MATÉRIA 1 - RETROSPECTIVA 2026 - ESB V5”, enviada pelo Mário Fernando em 21/11/2026), em todas as páginas, sobre o fundo da Retrospectiva (“BG Retrospectiva 2025.psd”): na página esquerda, retranca da editoria (por exemplo “ROCHAS NATURAIS”, “PORTOS E LOGÍSTICA”, “AGRONEGÓCIO”; estilo “Retranca 2026”, Inter Black 12, azul, caixa alta, a 10 mm do refile e 6,8 mm do topo) e selo da Retrospectiva do lado da lombada (a 155 mm, 33,8 × 19,4 mm), alinhado na altura da retranca, a partir da palavra “RETROSPECTIVA” (regra do Mário Fernando, 22/11/2026; na prova, `.selo` a 23,6 px do topo e margem de cima da página de 84 px, com a foto e os elementos subidos junto); na direita, logo da **ES Brasil** do lado da lombada (a 14,8 mm), na versão negativa transparente enviada pelo Mário Fernando em 22/11/2026 (`kit/assets/logo-es-brasil.png`), alinhado à retranca, e retranca “RETROSPECTIVA 2026” em caixa alta, alinhada à direita, terminando a 10 mm do refile; nas duas, aba de cor de 5 × 5,6 mm na sangria, a 6 mm do topo. A retranca é a única exceção à regra de caixa baixa. O capítulo do setor de rochas se chama **Rochas Naturais** (decisão do Mário Fernando, 22/11/2026): retranca “ROCHAS NATURAIS”, título do arquivo “Retrospectiva 2026 · Rochas Naturais” e box “Quer saber mais sobre os números das Rochas Naturais?”; nunca só “Rochas”.
- **Cabeçalho alinhado à mancha** (pedido do Mário Fernando, 22/11/2026): em todas as páginas, o elemento da esquerda do cabeçalho (retranca da editoria na página par, logo da **ES Brasil** na ímpar) começa exatamente na borda esquerda da foto e da mancha. O elemento da direita (selo da Retrospectiva na par, retranca “RETROSPECTIVA 2026” na ímpar). **Alternância das retrancas** (regra do Mário Fernando, 22/11/2026): a primeira página do capítulo, e toda página esquerda, leva a categoria (a editoria); a página direita, ao lado do logo da **ES Brasil**, leva “RETROSPECTIVA 2026”; e assim alternando pelas páginas duplas. O lado vem da posição real da página no espelho do NX Pages (página par é esquerda, mesmo quando há anúncio entre duas páginas do capítulo) termina exatamente na borda direita da foto e da mancha, sem contar o crédito vertical. Na prova: par, retranca a 52,68 px da esquerda e selo terminando a 74,63 px da direita; ímpar, logo a 74,63 px da esquerda e retranca terminando a 52,68 px da direita. No pacote do InDesign, a página-mestre segue o mesmo alinhamento (margens de 12 mm por fora e 17 mm na lombada).
- Abertura com foto grande, ocupando **no máximo metade da página** (regra do Mário Fernando, 21/11/2026, que vale para toda foto do capítulo: nunca mais do que meia página), e crédito da foto. **Sem QR Code**: o quadro do QR Code saiu de todas as matérias (regra do Mário Fernando, 22/11/2026); a chamada para fora da revista fica com o box do ES em Números no fim do capítulo.
- Título em branco sobre a foto, centralizado na própria moldura (“Título 36pt 2026”); linha fina logo abaixo da foto.
- **Linha fina em no máximo três linhas** (regra do Mário Fernando, 22/11/2026): econômica, com o número-chave e o protagonista, sem enumerar todos os assuntos do capítulo (cerca de 130 caracteres na largura da mancha). Conferir no PDF antes de entregar; se passar de três linhas, enxugar.
- **Entrelinha do título apertada** (pedido do Mário Fernando, 22/11/2026, corrigindo a regra anterior): o título sobre a foto usa a entrelinha justa do “Título 36pt 2026” da base V5 (35,1/32,3 pt, cerca de 0,92 do corpo). Na prova, 45,6 px de entrelinha para 49,6 px de corpo. As linhas ficam bem juntas, como bloco, sem vão entre elas; só se afrouxa o mínimo se um acento ou uma descendente encostar de fato na linha vizinha. Conferir no PDF, em zoom, antes de entregar. Quando a foto pedir, o título leva contorno azul-navy **por fora** da letra branca, que continua chapada (regra do Mário Fernando, 22/11/2026): no InDesign, traço de cerca de 1 pt na cor “Azul ES Brasil 2026”, alinhado por fora, nunca centralizado; na prova, um anel de sombras navy de cerca de 2,2 px atrás do branco (`text-shadow`), nunca `-webkit-text-stroke`, que sai oco no PDF. Conferir no PDF renderizado.
- A foto de abertura pode receber uma tabela ou um gráfico do NXtab ligeiramente sobreposto a ela, alinhado à última coluna da direita (vaga `lateral`, uma coluna de largura), aplicado direto sobre a foto, sem moldura branca e sem sombra. O título fica nas colunas livres da foto, sem cruzar com a peça nem com o QR Code.
- Texto em 3 colunas com capitular; intertítulos em azul, em caixa alta e baixa (regra da casa: nada em caixa alta); **aspas sempre dentro do texto corrido**, sem olhos destacados.
- Rodapé no padrão do paginador da revista: na página par, número e redes (só “revistaesbrasil • @esbrasil”, sem o “esbrasil” do meio, regra do Mário Fernando, 22/11/2026) do lado de fora; na ímpar, radio.esbrasil.com.br e o número. No InDesign ele vem da página-mestre.

**Da Retrospectiva 2024 (edição 225)** — https://esbrasil.com.br/edicao-225-retrospectiva-2024/
- Gráficos de 2024 podem entrar quando forem relevantes e bonitos, refeitos no NXtab. Registrar no dossiê qual gráfico foi aproveitado e de que página.
- A **tabela padrão do tema** no mesmo formato de 2023, 2024 e 2025 (ex.: Rochas — exportações capixabas por produto, US$ e toneladas, com variação).
- Páginas internas com foto lateral e legenda, e intertítulos que separam os blocos.

**Modelos de página** (estão prontos em `kit/assets/modelo-capitulo.html`)
1. Abertura: foto de no máximo meia página com título, linha fina e texto em 3 colunas, sem QR Code (22/11/2026); pode levar uma tabela ou um gráfico do NXtab ligeiramente sobreposto à foto, alinhado à última coluna da direita. O título fica na parte livre da foto, sem se cruzar com a peça. Se o modelo do kit ainda trouxer o quadro do QR Code, apague-o. O box “ES em Números” não vai na abertura (ver etapa 6).
2. Dados: tabela padrão no alto, texto em 3 colunas (a terceira na lateral, acima das peças) e gráfico ou lista do NXtab no pé da lateral. Sem foto: a tabela padrão já é o elemento visual da página.
3. Contexto: foto em faixa, texto em 2 colunas, gráfico lateral e linha do tempo acima do rodapé.
4. Eventos: foto, tabela de feiras, eventos ou marcos do ano (conforme o perfil), texto em 2 colunas e gráficos na lateral.
5. Fechamento: foto (no máximo meia página), fim do texto e o box “ES em Números” no pé da coluna lateral, ocupando uma coluna, fora da foto, como último elemento da página. O texto termina encostado no box, com no máximo cerca de uma linha em branco entre a última linha e ele (pedido do Mário Fernando, 22/11/2026): acerte o encaixe pela altura das fotos das últimas páginas antes de mexer no texto. Acima do box, na lateral, sobe o fim do texto (caixa `.flow.c1` com o `data-flow` seguinte); nenhuma peça vai embaixo do box. O gráfico ou a tabela que ocuparia a lateral vai para a página do assunto.
- A quantidade de modelos segue o número de páginas da ficha. Capítulos menores juntam modelos (2 páginas = abertura + fechamento com tabela padrão; 1 página = abertura compacta com tabela ou gráfico e box). O box nunca sai. **A linha do tempo só entra em capítulos com mais de 3 páginas** (regra do Mário Fernando, 22/11/2026); nos de 1 a 3 páginas, o espaço dela vai para o texto, para uma tabela ou para um gráfico.
- Nível 1 com 6 páginas repete o modelo 2 ou 4.

## Etapa 2 · Edições especiais do tema (obrigatória)

Antes de qualquer outra fonte, verifique se a **ES Brasil** publicou edição especial do tema em 2025 ou 2026. Se houver, ela é a principal fonte de dados, entrevistas, infográficos e fotos.
- Onde procurar: https://esbrasil.com.br/multimidia/digital/ e a base NEIA (`list-editions`, `search-content` nas fontes “REVISTA ESBRASIL” e “ESBRASIL.COM.BR”).
- Incluir edições com letra (225B, 228B…) e séries (“ES Brasil Cidades”, “Anuário Verde”, “ES Brasil Energia”).
- Registrar no início do trabalho: edição, mês, tema e páginas usadas. Conferir também as edições de outubro e novembro de 2026.

## Etapa 3 · Ordem de apuração

1. **ES Brasil**: edição especial do tema, matérias de 2026 em esbrasil.com.br e base NEIA.
2. **Fontes institucionais da editoria**, conforme o perfil.
3. **Dados oficiais primários** do perfil, sempre com o Instituto Jones dos Santos Neves, o Observatório da Findes e a plataforma **ES em Números** quando tiverem o indicador.
4. **Feiras, eventos e marcos do ano**, conforme o perfil.
5. **Sites especializados**.
6. **Só depois, outras mídias**, sempre com crédito.

**Regras de dados**
- Nunca inventar número ou nome. Aspas só com fonte publicada ou entrevista da redação; a única exceção é a aspa montada da etapa 3c.
- Valor calculado (ex.: base de 2025 derivada de variação) leva asterisco e nota.
- Divergência entre fontes: o número da entidade oficial vai no título e no texto; a tabela padrão usa a base oficial primária, com nota de metodologia.
- Todo número diz o recorte: ES ou Brasil, período e unidade.
- **Dupla checagem:** todo número, nome, cargo e fato do texto, do box, das tabelas e dos gráficos é conferido na publicação da **ES Brasil** usada como base e em pelo menos um site oficial ou confiável (órgão público, entidade do setor, empresa, base estatística). O dossiê registra os dois links. Número que só aparece numa fonte vai para “Para o fechamento” como pendência rosa.
- **Sem crédito à ES Brasil no texto:** as publicações da **ES Brasil** são fonte de apuração, não personagem. O texto usa a informação sem dizer em que edição, especial ou matéria ela saiu (nada de “como registrou o Anuário Verde”, “afirmou à ES Brasil” ou “segundo a edição de agro”). A origem fica só no dossiê e no banco de aspas.
- **Boxes, tabelas e gráficos fiéis ao texto:** cada peça ilustra o que o texto diz ou o complementa com dado confiável, com os mesmos números, recortes e períodos. Número de peça que contradiz o texto é erro de checagem.

## Etapa 3d · Dados quentes (sempre a referência mais recente)

Toda tabela, gráfico, box, linha fina e número do texto usa a **divulgação mais recente** da fonte: na apuração, de novo na montagem das páginas e de novo no fechamento (envio em 03/12). O leitor recebe a revista em dezembro; dado de agosto quando já saiu outubro é dado velho.

**Como buscar**
1. Para cada número do dossiê, ver no calendário abaixo se a fonte já soltou edição ou mês mais novo. Procurar primeiro no site ou boletim oficial da fonte (WebSearch com o nome da pesquisa e o ano; WebFetch na página de divulgação), depois na base NEIA e em esbrasil.com.br (a **ES Brasil** costuma noticiar no dia), depois na plataforma ES em Números.
2. Registrar de cada número: fonte, edição ou período de referência, data de divulgação e link. A nota da tabela ou do gráfico diz isso (ex.: “Fonte: Sinduscon-ES, 47º Censo Imobiliário (1º sem./2026), divulgado em out/2026”).
3. Número novo confirmado depois da prova: trocar na tabela e no gráfico (refeitos no NXtab com `nxtab_grafico.py`, mesmo modelo e mesma vaga), no box, na linha fina e no texto, marcado com a classe `novo` (verde-claro na prova) até o editor conferir. Nas peças do NXtab, a marca é uma nota `p.src` com `span.novo` logo abaixo da peça, dizendo o que mudou. Conferir se título, linha fina, linha do tempo e frases de tendência (cresce/cai) dependem do número trocado.
4. Divulgação prevista que ainda não saiu: manter o último dado com o período escrito e marcar em rosa “atualizar com [pesquisa], prevista para [mês]”.
5. Site, painel ou API bloqueado ou recusado: **não contornar** (nada de API escondida, chave tirada do código da página, cache ou espelho). Usar boletim, release ou nota oficial com o mesmo número (Fecomércio-ES, IJSN, Findes, MDIC, Ministério de Portos e Aeroportos, a própria entidade) ou deixar pendência rosa dizendo o que falta.
6. Dado mais novo de outra fonte ou com outra metodologia não substitui a série da tabela padrão: entra no texto, com crédito, e a série fica coerente.

**Calendário de divulgação** (ponto de partida; confirmar a data na fonte)

| Fonte | Pesquisa ou indicador | Periodicidade e quando sai | Editorias |
|---|---|---|---|
| MDIC · Comex Stat | Exportação e importação por UF, produto e URF | Mensal, nos primeiros dias úteis do mês seguinte | Rochas, Portos, Agro e Café, Indústria, Mineração |
| Antaq | Estatístico Aquaviário (movimentação por porto e terminal) | Mensal, cerca de 30 a 45 dias depois do mês; consolidação trimestral | Portos e Logística |
| Ministério de Portos e Aeroportos, Vports, Portocel, terminais | Balanços, releases e resultados trimestrais | Conforme a empresa | Portos e Logística |
| Findes | Atlas Portuário, Observatório, sondagens, Anuário do Petróleo | Conforme publicação | Portos, Indústria, Energia |
| Sinduscon-ES | Censo Imobiliário da Grande Vitória (lançamentos, vendas, estoque, VGV) | Semestral; o 47º (1º sem./2026) saiu em out/2026 | Construção civil e Mercado imobiliário |
| Sinduscon-ES, Ademi-ES | Outras pesquisas de vendas e lançamentos, quando houver | Conforme a entidade | Construção civil e Mercado imobiliário |
| MTE · Caged | Empregos formais por setor e município | Mensal, cerca de 4 semanas depois do mês | Todas as editorias de setor |
| IBGE | PIM-PF, PMC e PMS regionais | Mensal, cerca de 40 a 45 dias depois do mês | Indústria, Comércio e Serviços |
| IBGE · Conab | LSPA e safras (mensal); PAM e PPM (anuais, set/out) | Mensal e anual | Agronegócios e Café |
| Cecafé, CCCV | Exportação de café | Mensal | Agronegócios e Café |
| ANP | Produção de petróleo e gás, royalties e participações | Mensal | Energia, Petróleo e Gás |
| IJSN | PIB trimestral do ES e boletins | Trimestral | Economia e todas |
| Fenabrave | Emplacamentos | Mensal, nos primeiros dias do mês | Varejo automotivo |
| Anac e aeroportos | Passageiros e carga | Mensal | Turismo, Logística |
| ES em Números | Indicadores do box “2026 em Números” | Conforme os coletores | Box de todos os capítulos |

**Rotina automática.** A tarefa agendada “Retrospectiva 2026 · dados quentes dos capítulos” (segunda, quarta e sexta, 6h47, até 03/12/2026) aplica esta etapa a todos os capítulos da tabela “Capítulos já produzidos”: busca as divulgações novas, troca os números com a classe `novo`, refaz os gráficos no NXtab, confere o encaixe, registra as trocas em `section.atual` e publica nova versão do artefato (“Dados de DD/MM: …”). Ela não gera o pacote do InDesign: depois de uma atualização, o pacote precisa ser refeito.

## Etapa 3b · Dossiê de apuração (entregar antes de escrever)

- Edição especial encontrada (nº, mês, páginas úteis) ou “não há especial”.
- Tabela padrão já preenchida com o recorte do ano e a fonte.
- 10 a 15 números-chave, cada um com recorte (ES/BR), período, unidade e link.
- 8 a 12 fatos do ano candidatos à linha do tempo, marcados ES, BR ou Mundo.
- Perfil usado e fontes consultadas, com o que cada uma trouxe.
- Fotos candidatas com a origem (“Buscar original”).
- Lacunas: o que não foi encontrado e quem procurar.

## Etapa 3c · Banco de aspas (antes de escrever)

- **Ordem de busca:** (1) protagonistas da editoria que falaram à **ES Brasil** (site e revista, base NEIA); (2) especialistas do casting da **ES Brasil** da área (Corecon-ES e Findes nos temas econômicos; cientistas políticos, médicos, educadores, especialistas em segurança etc. nos demais); (3) só depois, falas publicadas por entidades e outras mídias, com crédito.
- **Equilíbrio de vozes:** o capítulo não depende de uma fonte só; em temas de governo e de Política, ouvir também oposição, controle (TCE, MP) e sociedade civil.
- Toda aspa leva a origem: veículo, data e link (ou edição e página).
- **Aspa verificada:** texto literal, sem alterar palavras; pode ser cortada só entre frases inteiras. Na prova, entra marcada em azul-claro.
- **Aspa montada:** quando faltar fala, pode-se redigir a partir de declarações já publicadas da mesma pessoa. Entra marcada em laranja e só vira definitiva depois de confirmada com a pessoa. **Proibida** nos perfis que a vetam (Política; vítimas ou casos policiais em Políticas públicas).
- **Aspas das publicações-base:** usar as falas que estavam nos textos da **ES Brasil** que serviram de base, desde que não corram risco de ter perdido a atualidade (fala sobre previsão já vencida, número superado, cargo que a pessoa não ocupa mais ficam de fora).
- **Onde entram:** sempre no texto corrido, com nome, cargo e verbo de atribuição (“afirma”, “explica”, “avalia”). Sem olhos e sem aspas soltas em box.
- **Toda aspa abre parágrafo próprio.** Nunca como continuação do parágrafo anterior. O parágrafo começa pela fala ou pelo atribuidor (“Para o presidente da Findes, Paulo Baraona, “…””) e o contexto fica no parágrafo de antes.
- **Fontes a ouvir:** em cada capítulo, indicar até duas fontes para entrevista, entre as principais autoridades do setor. Para cada uma: nome, cargo, teor da aspa esperada e o ponto exato do texto onde ela entra, para manter coesão, coerência e fluidez. Na diagramação, o espaço já fica reservado: um parágrafo próprio `p.vaga-aspa` com `span.tbd` (“Aspa a colher: [nome, cargo], sobre [teor] · cerca de [n] linhas”), no lugar em que a fala vai entrar.
- Aspa sem origem localizada sai do texto até confirmação.
- Entregar a tabela “Banco de aspas” (situação, quem, aspa, origem, uso no capítulo) junto com as páginas.

## Etapa 4 · Pauta de entrevistas e participações

- Lista de quem ouvir, com 3 perguntas por fonte e prazo de retorno até 25/11.
- **Artigo assinado** de uma liderança da editoria, como em 2025 (presidente de sindicato ou associação nos setores; gestor, pesquisador ou liderança da sociedade civil nos demais; em Política, só especialista sem mandato nem candidatura), com tema sugerido e tamanho. Não conta no texto corrido; trechos podem virar aspas verificadas.
- Empresas e entidades com potencial de **publieditorial** ou cota, para a área comercial (fechamento comercial pelo NX Pages: 10/12/2026 na consulta de 25/11), **só nos perfis que permitem**. Anúncio nunca encosta em matéria sobre o próprio anunciante sem a etiqueta de publicidade.

## Etapa 5 · Estrutura editorial

- Título curto e afirmativo (até 8 palavras) e linha fina com o número-chave do ano, em no máximo três linhas.
- Abertura com o saldo do ano e a comparação com 2025.
- Intertítulos a cada 1.200–1.800 caracteres.
- Aspas na quantidade da ficha, distribuídas pelas seções.
- Fecho com perspectivas para 2027 (metas do setor, agenda do governo eleito, projetos e calendário, conforme o perfil).
- Tom informativo e analítico, sem opinião da revista; adjetivos só atribuídos a fontes.
- **Estilo da Retrospectiva** (referência: capítulos das Retrospectivas 2024 e 2025, eds. 225 e 231): o primeiro parágrafo dá o fato e o número do ano; a fala da liderança vem logo depois, em parágrafo próprio; frases diretas, na ordem sujeito-verbo-complemento; transições simples (“Mas”, “Entre os desafios”, “Para 2027”); intertítulos curtos e informativos.
- **Escrita humana:** evitar clichês, jargões e marcas de texto gerado por IA, como “em um cenário de”, “não apenas… mas também”, “vale destacar”, “é importante ressaltar”, “nesse contexto”, “cada vez mais”, “desafios e oportunidades”, “um marco”, “divisor de águas”, “virar a chave”, “jornada”, “ecossistema” (fora do sentido técnico), “robusto”, “alavancar”, “potencializar”, “sinergia”, trios de adjetivos, frases de efeito no fim do parágrafo, dois-pontos dramáticos e travessões em série. Antes de entregar, reler o texto inteiro procurando essas marcas (falas literais de fontes ficam como foram ditas).
- **Sem abreviaturas no texto corrido:** quilômetro, quilo, tonelada, hectare, metro cúbico, milhão, bilhão (“R$ 1,4 bilhão”, “12 mil hectares”). Abreviaturas e símbolos só em tópicos, tabelas, gráficos e boxes. Siglas de instituições seguem a regra da casa (nome por extenso na primeira menção, quando não forem consagradas).
- Nada em caixa alta (título, intertítulo, etiquetas): caixa alta e baixa sempre, exceto siglas, a cartola da editoria e o **título de todo infográfico** (gráfico, tabela e linha do tempo do NXtab), que vão em caixa alta (decisão do Mário Fernando, 22/11/2026). A cartola é escrita já em maiúsculas no HTML, para chegar assim ao InDesign; o título dos infográficos o NXtab já põe em caixa alta.

## Etapa 6 · Elementos fixos de todo capítulo

**Box “ES em Números”, sempre numa coluna, fora da foto, de preferência na última página** (decisão do Mário Fernando, 20/11/2026, revista por ele em 21/11/2026; desenho oficial enviado por ele em 22/11/2026)
- Todo capítulo traz o box de chamada para a plataforma ES em Números, com o nome do segmento na pergunta.
- O box ocupa sempre uma coluna da grade (a coluna lateral, 55,8 mm), nunca vai sobre a foto nem dentro de outra tabela, e fica de preferência na última página do capítulo (fechamento), no pé da lateral, como **última coisa da página** (regra do Mário Fernando, 21/11/2026). Em capítulo de uma página, vai no pé da lateral da própria página, fora da foto.
- **Desenho oficial** (siga exatamente, sem acrescentar nem tirar elementos): cartão com cantos arredondados, mais largo que alto, em duas faixas.
  - **Faixa de cima**, em navy: à esquerda, a pergunta “Quer saber mais sobre os números do [Segmento]?” (ex.: “do Agro?”, “das Rochas?”, “do Mercado Imobiliário?”), em Inter Black, branco, em caixa alta e baixa, com letras juntas, em até quatro linhas; à direita, a logomarca **ES em Números** numa plaquinha de navy um pouco mais claro.
  - **Filete rosa** da marca, de ponta a ponta, separando as faixas.
  - **Faixa de baixo**, em navy mais escuro: o endereço “esemnumeros.esbrasil.com.br” centralizado, em Inter Bold, branco.
- O box não traz indicadores, etiquetas ES/BR, QR Code nem linha de fontes. Os números do segmento vão no texto, nas tabelas e nos gráficos do capítulo.
- Layout padronizado para todos os capítulos, adaptado a cada segmento só no nome da pergunta. Se o modelo do kit ainda trouxer o box antigo com indicadores, troque pelo desenho oficial.
- Como gerar: `python3 kit/scripts/box_esnumeros.py "Agro" graficos/` (editoria com artigo vai com ele: `"dos Supermercados"`, `"das Rochas Naturais"`; nome longo vai em linhas prontas separadas por `|`: `"Quer saber mais|sobre os números|dos Serviços|Financeiros?"`; corrigido em 22/11/2026, quando o box de Rochas saiu com “números do Rochas Naturais”) grava `graficos/esn-box.svg` e `graficos/esn-box.html` (cartão de 330 × 178 px de desenho, 246 px de largura na prova, a mesma escala das peças da lateral); no corpo, use `{{esn-box}}` como último elemento da lateral da última página. No InDesign ele vai como peça vetorial vinculada; a marca do ES em Números do kit (`assets/logo-es-em-numeros-h.png`) foi recortada da referência do Mário: aplique a versão vetorial, horizontal e negativa, quando houver. Se o NXtab publicado ganhar o modelo do box, prefira o do NXtab.
- Se a plataforma ainda não tiver o indicador do tema, registrar em “Para o fechamento” como pauta para alimentá-la.

**Linha do tempo do ano** (sai do NXtab, como os gráficos e as tabelas)
- Faixa em largura total (vaga `larga`), logo acima do rodapé da página com mais respiro; com 6 marcos fica com cerca de 4,5 a 5 cm de altura.
- A linha do tempo vertical (modelo `i-tempo`, ou a faixa com mais de 8 marcos) sai estreita, com no máximo 560 px de largura de desenho, datas e textos compactos e o detalhe em Roboto Condensed (pedido do Mário Fernando, 22/11/2026; o NXtab já aplica). Na página, ela cabe em duas colunas da grade.
- De 6 a 8 marcos em ordem cronológica, num CSV `Data;Marco;Detalhe`: data em mmm/aa, minúscula (abr/26; o NXtab converte abr/2026), título curto (até 6 palavras) e uma linha de detalhe. Até 12 só em último caso: com mais de 8 o NXtab passa a peça para a vertical.
- Dois modelos, os dois com fundo cinza 5%, barrinha rosa no topo, título em caixa alta, marcos no azul da paleta **ES Brasil** em caixa alta e baixa e créditos das fotos numa linha só, junto da fonte:
  - `i-tempo-fotos` (“Linha do tempo com fotos”): uma foto por marco, a data sob a foto e os textos alternados acima e abaixo, quebrados na largura da foto. É o padrão quando houver foto boa para todos os marcos (do próprio capítulo, do NX Fotos ou do WordPress da **ES Brasil**, com crédito). As fotos vão no campo `fotos` do `graficos.json`, pela data da coluna Data: `{"abr/26": {"arquivo": "fotos/porto.jpg", "autor": "Fulano", "fonte": "Divulgação"}}`.
  - `i-tempo-pictos` (“Linha do tempo com pictos”): faixa em seta com as datas e um picto por marco, para quando faltar foto ou o ano for mais de decisões e números do que de imagens. Dê um ícone Lucide a cada marco no campo `icones`, pelo texto da coluna Marco (`{"Porto Central": "anchor"}`); marco sem ícone que o NXtab não reconheça sai com o número no lugar do picto.
- Prioridade: 1º fatos da editoria no **Espírito Santo**; 2º no **Brasil**; 3º do exterior que afetaram o tema. Pelo menos metade dos marcos é do ES. Sem etiqueta de escopo (ES, BR, Mundo) na peça: quando o marco não é do ES, o detalhe diz onde foi.
- **Marcos inteligentes e reais** (decisão do Mário Fernando, 22/11/2026). Cada marco é um fato do ano com efeito direto e mensurável na economia do tema no ES, e o detalhe traz o número que prova isso: safra e produção, preço recebido pelo produtor, exportação, investimento anunciado ou entregue, obra, lei ou programa estadual, crédito, recorde, ranking nacional. Exemplos bons no agro: safra de conilon com a variação da Conab, recorde do preço da saca, Plano Safra estadual com o valor, liderança nacional na pimenta-do-reino. Fato geopolítico, internacional ou nacional genérico (guerra, fechamento do Estreito de Hormuz, eleição em outro país, decisão do Fed) só entra se a fonte mostrar o efeito no setor capixaba, e o detalhe traz esse efeito com número; sem isso, fica de fora. Todo marco tem data e fonte conferidas (etapa 3d), e nenhum é tirado de memória.
- **Produção manual**: quando o capítulo for feito com o editor na conversa (e não por rotina automática), antes de montar a linha do tempo pergunte a ele quais marcos quer incluir. Mostre a sua lista de 6 a 8 marcos apurados como sugestão, com data, número e fonte, e monte a peça com os que ele escolher ou acrescentar. Em rotina automática, siga a regra acima e registre a lista em “Para o fechamento” para o editor revisar.
- **Fonte condensada da casa: Roboto Condensed** (correção do Mário Fernando, 23/11/2026: onde ele disse “Myriad”, a fonte certa é a Roboto Condensed). Em tudo que antes pedia Myriad Condensed (detalhe da linha do tempo, linha de apoio, legenda sobre a foto), use Roboto Condensed, no mesmo corpo e no mesmo peso já definidos. O NXtab, o `nxtab_grafico.py`, o `legendas.py` e o exportador do InDesign do kit já aplicam desde 23/11/2026; prova antiga com Myriad sai em Roboto Condensed no InDesign.
- O texto sob o título de cada marco (detalhe) sai em **Roboto Condensed**, no mesmo corpo de antes; o NXtab já aplica.
- **Linha do tempo com fotos mais baixa** (pedido do Mário Fernando, 22/11/2026): o título e o detalhe de cada marco ocupam quase toda a largura da foto (duas ou três linhas, no máximo), para a peça perder altura. O `nxtab_grafico.py` aplica isso em `AJUSTES_NXTAB` (quebra do título a 1,1 e do detalhe a 1,38 da largura da coluna, porque a Roboto Condensed é mais estreita que a conta do NXtab). Se o kit ainda não tiver esse ajuste, acrescente-o antes de gerar a peça. Detalhe com no máximo cerca de 60 caracteres. O detalhe sai em Roboto Condensed um pouco mais forte e maior que no NXtab original (peso 500 em vez de 300, corpo cerca de 5% maior), para ler bem no impresso (pedido do Mário Fernando, 22/11/2026); o `nxtab_grafico.py` aplica em `AJUSTES_NXTAB`.
- A linha do tempo com fotos é o padrão em todo capítulo que leva linha do tempo (mais de 3 páginas, como em Agro); a de pictos só entra quando faltar foto boa para os marcos, e mesmo assim sem deixar áreas vazias acima ou abaixo da faixa.
- Marco de outubro ou novembro ainda provisório: entra na peça e vai também em rosa logo abaixo dela, num `p.src` com `span.tbd` (“No fechamento: confirmar …”); no fechamento, refaça a peça.

**Gráficos, tabelas e linha do tempo: sempre no NXtab** (construtor de gráficos da Next, artefato “NXtab”, slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`)
- Todo gráfico do capítulo (colunas, barras, rosca, faixa ou painel de números) sai do NXtab, num modelo da biblioteca da revista: `c-percentual` (uma série com destaque), `c-colunas` (séries por ano), `c-barras` (barras horizontais), `c-rosca` (participação), `c-faixa` e `c-lista` (números), `v-fita` e `v-leque`; tabela em `t-retro`; linha do tempo em `i-tempo-fotos` ou `i-tempo-pictos`. Não desenhar gráfico, tabela nem linha do tempo à mão.
- Como gerar: descreva as peças num `graficos.json` (id, modelo, vaga, título, subtítulo, fonte, csv e, se houver, destaque) e rode `python3 kit/scripts/nxtab_grafico.py kit/nxtab.html graficos.json graficos/`. O script roda o próprio NXtab, aplica o modelo, troca os dados e entrega, por peça, o SVG que vai para a página, o projeto `.nxtab.json` (abre no NXtab para ajustes), a prévia em PNG e o `<figure>` pronto para colar no capítulo.
- Vagas (largura na prova de 900 px): `abertura` (painel de 320 px, de capítulos antigos; a peça sobre a foto de abertura agora usa a vaga `lateral`, alinhada à última coluna da direita), `lateral` (uma coluna da grade, 246 px), `larga` (largura toda da mancha, 773 px, desenhada a 1.000 px desde 22/11/2026; também a da linha do tempo) e `tabela` (773 px, desenhada a 1.000 px desde 22/11/2026, só para tabelas; antes, 1.250 px, o que deixava o corpo em 5,8 pt e a fonte em 3,9 pt). A escala de cada vaga faz os dados saírem perto de 7 pt no impresso.
- **Peça nunca encolhe para caber** (regra do Mário Fernando, 22/11/2026: “o gráfico é um dos elementos mais importantes da retrospectiva”). Não reduzir tabela, gráfico nem o corpo das letras para a peça caber na vaga: adaptar o desenho. Na tabela, estreitar a coluna de texto (produto, evento) e alargar as de números, com o campo `larguras` do `graficos.json` (pesos relativos das colunas, ex.: `[9,7,7,6,7,6]`); no gráfico, encurtar rótulos ou trocar de modelo. Medir no PDF: corpo da tabela perto de 7,3 pt e linha de fonte perto de 6,2 pt; abaixo de 7 pt no corpo, refazer. Se mesmo assim não couber, o texto cede espaço, nunca a peça.
- **Mesma escala em todas as peças** (padronização visual da revista, pedida pelo Mário Fernando em 22/11/2026). Tabela, gráfico da lateral e linha do tempo saem na mesma escala (cerca de 0,805 do desenho do NXtab), para que título, linha de apoio e fonte tenham o mesmo corpo em todo o capítulo; o `nxtab_grafico.py` já usa as vagas `lateral` 330, `larga` 1.000 e `tabela` 1.000. O script também põe a **linha de apoio** (o texto logo abaixo do título) em fonte condensada no SVG, fixa a linha de fonte em 12 px (cerca de 6,2 pt) e, quando a fonte com os créditos das fotos não cabe numa linha, quebra em duas em vez de apertar as letras. Confira no PDF: o mesmo corpo de título e de fonte em todas as peças.
- O título de todo infográfico sai em caixa alta, no azul da marca (navy da **ES Brasil**) e no peso mais forte (Inter Black), como em “QUEM PUXA A PAUTA” (decisões do Mário Fernando, 22/11/2026; vale também para tabelas e linhas do tempo, e o NXtab e o script já aplicam). A linha de apoio logo abaixo do título sai em **Arial Narrow Bold**, num corpo maior que o texto da lista e das células (15 px na lateral e 16 px nas peças largas, contra 14 px da lista), e não quebra quando o texto couber numa linha (decisão do Mário Fernando, 22/11/2026, que substituiu a Myriad Condensed light; o NXtab publicado e o `nxtab_grafico.py` do kit já aplicam, com Roboto Condensed Bold de reserva onde a Arial Narrow não estiver instalada). A linha de apoio tem **entrelinha aberta**, para respirar (cerca de 1,34 do corpo nas peças da revista e 1,4 nas da web, contra 1,2 antes), e um **respiro de cerca de 10 px** antes do corpo da peça, entre ela e o primeiro item da lista, a tabela ou o gráfico (pedido do Mário Fernando, 22/11/2026, no painel “O dinheiro do ano” de Serviços Financeiros; o NXtab publicado e o `nxtab_grafico.py` do kit já aplicam).
- **Rosca (`c-rosca`) compacta**: na coluna lateral, a rosca sai menor e quase quadrada, com a legenda numa coluna logo abaixo, para ocupar menos altura no impresso (cerca de 246 × 300 px na prova, contra 246 × 360 antes). O NXtab já aplica nas vagas estreitas; não aumente a rosca para preencher espaço. Todo item da legenda leva o percentual, inclusive a fatia em destaque (“59,5% · Café”), além do número grande no centro. **O indicador principal abre a legenda** (pedido do Mário Fernando, 22/11/2026): a fatia em destaque vem em primeiro, em negrito, e as demais seguem em ordem decrescente; o `nxtab_grafico.py` faz isso em `AJUSTES_NXTAB` (troca `[...order.slice(1),hiI]` por `[hiI,...order.slice(1)]`).
- **Barrinha rosa** no topo de toda tabela e de todo infográfico da **ES Brasil** (regra do Mário Fernando, 20/11/2026; o NXtab trava a cor na marca).
- **Número que grita nos gráficos** (pedido do Mário Fernando, 23/11/2026): em barras, colunas e percentual, o valor da linha marcada em `destaque` sai maior que os demais, dois pesos acima (Inter Black) e na cor de destaque da paleta da marca. Um destaque por peça, sempre o mesmo número que o texto destaca. O NXtab já aplica.
- **Peças achatadas**: as peças do NXtab saem um pouco mais baixas e com as letras um pouco mais juntas (padrão de 21/11/2026, já no NXtab). Não estique a peça para ocupar espaço, e também não a encolha para caber (regra de 22/11/2026, acima).
- **Foto de fundo pelo assunto da peça** (decisão do Mário Fernando, 22/11/2026). Toda peça com box leva no fundo, a 5% e em cinza, uma foto do NX Fotos que faça sentido com o que o gráfico mostra, buscada a cada gráfico gerado. Busque no NX Fotos (`buscar`, `orientacao: "h"`) pelo assunto dos dados e pelo lugar (ex.: “safra de café conilon”, “navio no porto de Vitória”, “culto igreja”), não só pela editoria; escolha uma foto horizontal, de pelo menos 1.600 px, sem marca de empresa em destaque e não oculta; baixe com `link_do_original` (ou a imagem de 1.600 px que a busca devolve) para `fundos/` e passe no campo `fundo` do `graficos.json`: `{"arquivo": "fundos/cafe.jpg", "titulo": "Lavoura de conilon", "autor": "Fulano", "fonte": "NX Fotos"}`. O NXtab passa a foto para cinza. Sem foto boa, deixe `"auto"`: o NXtab usa a foto do tema que reconhece no título e nos dados (agro, portos, energia, indústria, rochas, construção, turismo, assistência rural, igreja e fé, educação, saúde, meio ambiente, política e, por último, cidade). No NXtab aberto no Claude, o fundo “Automática” já faz essa busca sozinho a cada título. As linhas do tempo `i-tempo-fotos` e `i-tempo-pictos` não levam foto de fundo.
- A peça vai direto sobre a foto ou a página: sem o cerco branco do NXtab, sem sombra e sem drop shadow. Ajuste fino fica com o diagramador.
- Na coluna lateral, use rótulos curtos (até 12 caracteres, como “EUA”), para não quebrarem em duas linhas.
- **Painel de números (`c-faixa`, `c-lista`) com ícone em todos os indicadores** (pedido do Mário Fernando, 22/11/2026): nenhum número fica sem picto quando os vizinhos têm. Dê um ícone Lucide a cada linha no campo `icones` do `graficos.json`, pelo texto da coluna do indicador (ex.: `{"empresas": "briefcase", "empregos formais": "users", "dos empregos no beneficiamento": "factory", "das exportações do país": "globe"}`). O script aplica `icones` também nesses modelos (não só na linha do tempo com pictos); se o kit for anterior, acrescente no `nxtab_grafico.py` o ramo `else if (g.icones) { state.iconPick = {...g.icones}; $('iconMode').value = 'auto' }`.
- **Escala quebrada quando um valor domina** (modelo de referência: “Para onde vão as cargas”, capítulo de Portos, versão 3.6). Em barras e colunas de uma série, quando o maior valor passa de 2 vezes o segundo, o eixo vai só até o segundo valor; a barra do maior encosta no fim do eixo com a marca de quebra (//), o número dela continua escrito por inteiro e a fonte ganha a nota “[item]: barra fora de escala.”. Assim os valores menores ficam visíveis e continuam proporcionais entre si. O `nxtab_grafico.py` faz isso sozinho (campo `quebra`: `auto`, o padrão; `true` força no maior; `false` desliga; `nota_quebra` troca o texto da nota) e informa no relatório qual barra quebrou.
- Nunca esticar ou encolher barras fora de proporção sem a marca de quebra, e não usar escala logarítmica: o leitor lê o tamanho errado. Se dois valores dominarem juntos, pôr os dois em números de destaque no alto do box e as barras só para os demais.
- Cores e hierarquia são as do NXtab na marca **ES Brasil**: barras azuis em degradê, destaque em magenta, título em Inter 900, linha de apoio em Arial Narrow Bold e fonte colada no box, numa linha só, em Roboto Condensed.
- **Mapas e outras construções ilustradas** (mapa de portos, rotas, localização de projetos): não desenhar. Reservar o espaço com `figure.manual` e a etiqueta rosa “Criação manual”, descrevendo o que a peça deve mostrar (pontos, legenda, fonte). O espaço vai para a camada “Prova (não imprime)” do InDesign e o diagramador cria a peça. Registrar também em “Para o fechamento”.
- **Tabelas** (tabela padrão, de eventos ou de projetos) saem do NXtab no modelo `t-retro`, “Tabela da Retrospectiva” (aprovado no capítulo de ESG e Meio Ambiente em 20/11/2026): título na cor da marca, em caixa alta, linha de apoio em Arial Narrow Bold, fundo cinza 5%, barrinha rosa no topo, cabeçalho navy, linhas em azul-claro e primeira coluna em destaque. Desde 20/11/2026 a tabela tem o desenho do meio-termo aprovado por Mário: células em Inter com cabeçalho e primeira coluna em seminegrito, linhas mais baixas e filetes mais finos que o desenho antigo, sem chegar ao aperto da versão em Inter Tight (que ele achou apertada demais). Não volte a nenhum dos dois extremos. Vaga `tabela`, com `coluna_valor` apontando a coluna dos valores. Células curtas, para **cada célula caber numa linha só** (pedido do Mário Fernando, 22/11/2026: a tabela de feiras de Rochas saiu esticada na vertical). **Nem célula nem cabeçalho quebra linha** (reforçado em 23/11/2026, com o print da tabela de Supermercados): acerte os pesos das colunas no campo `larguras` do `t-retro` (ex.: `[46,13,14,13,14]` para uma tabela de 5 colunas com rótulos longos na primeira), encurte o rótulo se ainda quebrar, e confira cada linha na prova antes de entregar: com 4 colunas, até uns 28 caracteres por célula; com 5, até uns 22. Datas em mês abreviado (“ago · Cachoeiro”), números com “mi” e sem repetir a unidade do cabeçalho. A tabela fica achatada, como “O ano do agro em feiras e prêmios” de Agro, e a altura poupada vai para a foto da página (até meia página). Mantenha a mesma escala de Agro: não alargue nem estique a peça.
- Pendência de tabela (dado que só sai no fechamento) não entra na peça: vai em rosa logo abaixo dela, num `p.src` com `span.tbd`.
- **Números que gritam na tabela** (pedido do Mário Fernando, 22/11/2026): quando uma célula carrega a notícia da tabela (a alta que contraria a queda geral, o recorde, o primeiro lugar no país, a maior queda), ela sai em negrito (Inter Black) e na cor do projeto: rosa da marca (#E01E70) para o destaque positivo ou principal, azul navy (#113E74) para o contraponto. No máximo dois ou três valores por tabela, sempre os mesmos que o texto destaca. O número que grita sai também **um ou dois corpos maior** que o corpo da tabela, conforme a largura (dois corpos na tabela larga, um na estreita da lateral), **dois pesos acima** dos vizinhos, em negrito, para saltar da linha, sem marca-texto nem sublinhado (pedido do Mário Fernando, 23/11/2026). No NXtab publicado, basta marcar a linha no campo `destaque`: o número da `coluna_valor` dessa linha sai maior, mais pesado e na cor de destaque da paleta da marca (rosa na **ES Brasil**); os `realces` continuam valendo para outros números da tabela. A **linha de total** da tabela sai inteira em negrito. O `aplicar_realces` do `nxtab_grafico.py` faz as três coisas (cor, peso e corpo dos realces, e negrito da linha que começa com “Total”). Se nenhum número gritar, a tabela fica sem realce. No `graficos.json`, use o campo `realces`, que mapeia o texto exato da célula para a cor: `{"+10,3%": "rosa", "+15,1%": "rosa", "-24,7%": "azul"}`. O `nxtab_grafico.py` troca a cor e o peso dessas células no SVG; se o kit ainda não tiver o campo, aplique a mesma troca no SVG depois de gerar a peça.
- No pacote do InDesign, tabela e linha do tempo do NXtab vão como peças vetoriais vinculadas em `Links/`, como os gráficos, e não mais como tabelas nativas; os dados de cada peça saem no `<id>.csv` do `nxtab_grafico.py` e vão para `Textos/`.

**Escala tipográfica dos boxes, gráficos e tabelas** (px na prova de 900 px · pt no impresso)
- Peças do NXtab (gráficos, tabelas e linha do tempo): dados perto de 10 px · 6,5 pt; miúdos (fonte, eixos, notas) em 9 px · 5,8 pt; o detalhe dos marcos da linha do tempo sai maior, no corpo das legendas das peças, perto de 10,5 px · 6,8 pt (pedido do Mário Fernando, 22/11/2026; o `nxtab_grafico.py` do kit já aplica). A linha de fonte de toda peça fica afastada do box, com a mesma folga em todas, e quebra em duas linhas em vez de apertar.
- Box “ES em Números”: pergunta no estilo “Título de box 2026” (Inter Black 12 pt · 18,6 px), branca, em caixa alta e baixa; endereço em Inter Bold, branco, no corpo do texto de box (9,5 pt · 14,7 px).
- O modelo do kit já traz essa escala. Os gráficos do NXtab seguem a hierarquia do próprio NXtab, com os dados na mesma faixa de 6,5 pt; na tabela `t-retro`, as células saem perto de 5,8 pt.

**Regras de página**
- **Toda página tem, no mínimo, um elemento de dados** (gráfico, tabela, infográfico ou linha do tempo). Foto só onde ilustra o assunto da página; página sem foto é aceita (regra do Mário Fernando, 21/11/2026).
- **Manual de estilo:** toda a diagramação (texto, tabelas, boxes e gráficos) segue o manual de estilo da **ES Brasil**: os estilos de parágrafo, espaçamentos, fontes e páginas-mestre da base V5 do InDesign (já traduzidos em `kit/assets/grade-esb2026.css` e no modelo) e o Brand System 2026 (paleta da **ES Brasil**). Capítulo montado fora do modelo do kit não serve: refazer sobre ele.
- Paleta **ES Brasil**: azul #00427B e navy dos infográficos #0F2D5C, ciano #18A6E6, rosa #E01E70 (destaques e pendências), azul-pastel #A2D2FF.
- Tipografia: a da base da Retrospectiva (“MATÉRIA 1 - RETROSPECTIVA 2026 - ESB V5”, de 21/11/2026), pelos nomes dos estilos. Texto corrido em **Minion Pro Cond 11/12**, tracking -15, recuo de 8,5 pt (“Texto geral 2026”; na prova, a própria Minion Pro Cond, embutida como `@font-face` em base64 a partir de `kit/assets/fonts/` — MinionPro-Cn, CnIt, SemiboldCn e BoldCn —, em 17,04 px com tracking -0,015 em, para a prova já sair pronta para a diagramação, pedido do Mário Fernando, 23/11/2026; a Crimson Pro só entra de reserva se a pasta de fontes faltar); abertura com capitular de 3 linhas (“Texto fatual cap 3 linhas 2026”); intertítulo em Inter Black 11/12, azul, tracking -20, em caixa alta e baixa (“Intertexto 2026”, já sem caixa alta na V5); título sobre a foto em Inter Black 35,1/32,3 pt, branco, centralizado, tracking -25 (“Título 36pt 2026”); linha fina em Inter Bold 16/16 (“Lead 2026”); assinatura em Inter Black 11/11,5 (“Assinatura 2026”); legendas em **Roboto Condensed** 9,5/11, tracking -25, preto 90% (“Legenda 2026”); legenda sobre a foto no padrão da **ES Brasil** (regra do Mário Fernando, 22/11/2026): **Roboto Condensed** **8,5/10** (era Myriad Condensed até a correção de 23/11/2026), tracking -15, em até três linhas, **sem fundo, caixa ou tarja** cinza ou branca, em branco ou preto conforme a área da foto; Roboto Condensed Bold quando faltar peso; sombra (drop shadow leve) só quando o contraste continuar fraco mesmo assim. **Posição padrão para todas as fotos** (regra do Mário Fernando, 22/11/2026): sempre num dos quatro cantos (inferior direito, inferior esquerdo, superior esquerdo ou superior direito), onde a foto permitir, sempre com a mesma margem (22 px da lateral e 20 px da borda na prova, cerca de 5,8 × 5,3 mm) e o mesmo tamanho; nunca solta no meio da foto. O canto sai de `kit/scripts/legendas.py` (o mais liso e com mais contraste; `data-leg` na `figure` limita os cantos para não cobrir rosto nem o assunto); créditos em Roboto Condensed Light 7/7, tracking -10, na vertical, à direita da foto (“Créditos 2026”); retranca em Inter Black 12, tracking -20, em caixa alta (“Retranca 2026”, na página-mestre). Peças do NXtab seguem a escala tipográfica das peças, em **Inter**, com a linha de apoio em Arial Narrow Bold (Roboto Condensed Bold de reserva), o detalhe da linha do tempo em **Roboto Condensed** e a linha de fonte e créditos em **Roboto Condensed**, numa linha só.
- Formato e grade: 20,5 × 27,5 cm, páginas espelhadas, sangria de 3 mm; margens de 22 mm em cima, 15 mm embaixo, 17 mm na lombada e 12 mm do lado de fora; 3 colunas de 55,8 mm com 4 mm entre elas. Abertura com texto em 3 colunas; internas com texto em 2 colunas e a coluna lateral de 55,8 mm. O modelo traz tudo isso em `kit/assets/grade-esb2026.css`. A primeira página do capítulo é par (esquerda); se o espelho abrir em página ímpar, troque as classes `esq`/`dir`.
- Sempre em destaque: **ES Brasil**, **revista ES Brasil**, **Café com Moqueca**.

## Etapa 7 · Fotos

- **Ordem de busca** (reforçada pelo Mário Fernando em 22/11/2026, quando achou as fotos mal escolhidas): (1) **NX Feed** (`buscar_imagens` por assunto, com as recomendadas da casa); (2) banco **NX Fotos** (`buscar`, `link_do_original` para o arquivo em resolução cheia); (3) WordPress da **ES Brasil** (fotos do site esbrasil.com.br e das publicações que serviram de base ao capítulo; originais na pasta de links do InDesign da edição); (4) fotos oficiais de entidades, assessorias e organizadoras das feiras; (5) só se nada servir, uma referência de fora (Adobe Stock licenciado ou foto de entidade com crédito) que combine com a beleza gráfica da revista. Comparar várias candidatas por vaga antes de escolher: a foto tem de ser bonita, mostrar o assunto exato daquela parte do texto (a colheita, o produto, o lugar) e ser recente; foto genérica ou que só ilustra a editoria não serve.
- **Varredura de data em toda foto** (regra do Mário Fernando, 22/11/2026, depois que quase saiu na abertura de Serviços Financeiros uma fachada do Sicoob de 2011, de agência já fechada): antes de escolher, confira a data de cada candidata (campo `data` do NX Fotos; filtre a busca com `ano_de` do ano anterior em diante) e prefira as de 2025 e 2026. Foto de fachada, sede, agência, loja, obra ou paisagem urbana com mais de dois anos só entra depois de confirmar que o lugar ainda existe e está igual (site ou assessoria da empresa, matéria recente). Na falta de foto recente, use a mais nova disponível e marque em “Buscar original”. Registre data, autor e origem de cada foto em “Para o fechamento”.
- **Escolha por espaço:** cada vaga (abertura, faixa, lateral, fechamento) recebe a foto que conta aquela parte do texto, escolhida por beleza, informação contida na foto e atualidade. Tratar todas no padrão da Next com `kit/scripts/tratar_fotos.py` antes de aplicar: recorte para a proporção da vaga, níveis, eliminação de névoa, claridade, vibração, saturação e nitidez, com nitidez reforçada nas fotos moles, ampliadas ou fora de foco; nas fotos de lavoura, mata e pasto, `verde_citrico=True` (verde mais cítrico) e `quente` perto de 0,05, como o Mário Fernando pediu para a abertura do Agro em 22/11/2026. A foto segue o padrão gráfico da **ES Brasil** (reforçado pelo Mário Fernando em 22/11/2026, com a matéria de Rochas da ed. 237 como referência): foto que informa, com luz, cor e profundidade, sem cara de banco de imagem; prefira as fotos da casa em alta no NX Fotos (Next Editorial, fotógrafos da revista, drone) às de 1.200 px do site, e marque em “Buscar original” toda foto que ainda não está em alta. Nunca entregue foto sem tratamento.
- **Formatos variados** (liberado pelo Mário Fernando, 22/11/2026): as fotos não precisam ser todas faixas retangulares no alto da página. Podem ser vertical na coluna lateral, ocupar duas colunas ao lado do texto, ficar no pé ou abrir a página em meia altura, desde que desenhem a página de forma bonita, no estilo da **ES Brasil**, e sem tapar sobra de texto.
- **Fotos internas arredondadas e menos achatadas** (pedido do Mário Fernando, 23/11/2026): toda foto do capítulo, exceto a de abertura, leva cantos arredondados com o mesmo raio das tabelas do NXtab (9,66 px na prova, cerca de 2,2 mm no InDesign; na prova, `.ph:not(.opener)>img{border-radius:9.66px}`). As faixas e fotos internas saem cerca de 20% mais altas do que a faixa achatada usada até 22/11/2026 (ex.: faixa de 200 px passa a 240 px na prova), sem passar de meia página; o texto se encaixa pela nova altura.
- **Foto não tapa buraco.** Foto entra por função editorial, numa vaga do modelo; nunca para preencher sobra de página ou de coluna lateral, nem cresce para compensar falta de texto (reforçado pelo Mário Fernando em 21/11/2026). Quando uma foto sai, o texto sobe para o lugar dela. Sobra se resolve com texto (o texto cresce com apuração já feita) ou com peça de dados do NXtab.
- **Resolução mínima:** 300 dpi no tamanho de uso (abertura de página inteira: cerca de 2.500 px de largura). Nunca ampliar foto de site.
- Foto provisória é permitida com a etiqueta rosa **“Buscar original”** dizendo onde está a certa: “ES Brasil [nº], p. [x] — pedir original a [fonte]” ou “esbrasil.com.br, matéria de [data]”.
- Crédito no padrão “Foto: [autor]/[veículo ou Divulgação]”; conferir licença antes de reusar imagem de banco.

## Etapa 7b · Diagramação e encaixe do texto

- Montar as páginas **a partir de `kit/assets/modelo-capitulo.html`**, no tamanho fixo da revista (20,5 × 27,5 cm, 900 × 1207 px na tela). O modelo já traz o fluxo do texto entre as caixas, a medição de ocupação e as classes que o exportador do InDesign lê (ver “Contrato das páginas”). Não renomear classes nem trocar a estrutura.
- Trabalhar com as fotos em arquivos ao lado do HTML (caminhos relativos). Antes de publicar a prova, rodar `python3 kit/scripts/embutir_imagens.py capitulo.html capitulo-prova.html`, que embute as imagens (sem `--qr-materia`: a abertura não leva mais QR Code desde 22/11/2026); publicar o arquivo resultante como artefato.
- Corpo do texto corrido: 11 pt com entrelinha de 12 pt (Minion Pro Cond), como na base da revista.
- O texto corrido flui de página em página e o aviso de ocupação no alto da prova diz se cabe ou quantos caracteres sobram. Nunca preencher sobra com espaço em branco nem com foto: página com buraco recebe texto ou peça de dados do NXtab (gráfico, tabela, painel de números). A coluna lateral é conferida também: nenhuma lateral termina com buraco.
- **Grade alinhada e respiros** (pedidos da equipe e do Mário Fernando, 23/11/2026, no Agro e em Serviços Financeiros: “a revista está torta”, “tá ficando apertado”, “o texto ficaria melhor sempre caindo por baixo e alinhado corretamente”):
  - Todas as colunas da página e a lateral começam **na mesma altura** e terminam na mesma linha de base, no pé. A sobra menor que uma linha não vira recuo no alto das colunas: ela entra na foto de cima, que cresce alguns pixels, ou vira respiro acima da grade quando não há foto. Se as peças da lateral não couberem, a foto de cima encolhe linhas inteiras.
  - Na lateral, as **peças do NXtab vêm em cima**, alinhadas ao topo das colunas, e o **texto cai por baixo**, alinhado ao pé das outras colunas; a sobra fica entre a peça e o texto. Quando o texto abre a lateral, sem peça acima (fechamento com o box do ES em Números), ele começa alinhado ao topo das colunas e a sobra vai para o pé, antes do box.
  - **Respiro de cerca de 20 px (5 mm no impresso) abaixo de toda foto interna e da tabela do alto**, antes do texto e das peças.
  - **Intertítulo com respiro antes do texto:** ele continua ocupando duas linhas da grade (uma linha de espaço mais a linha do intertítulo), mas sobe cerca de um terço de linha, de modo que o espaço maior fique acima dele e um respiro visível fique entre ele e o texto; no alto da coluna, ele fica rente ao topo. No InDesign, o estilo “Intertexto 2026” leva espaço antes maior que o espaço depois, sem tirar o texto da grade de linhas de base.
  - Na prova, o script de encaixe faz isso sozinho; confira com a medição de topo e pé de cada coluna e da lateral (diferença de até 2 px) e com o respiro abaixo das fotos antes de entregar. Quando a regra empurrar texto para fora, corte frases curtas apuradas ou ajuste a foto em linhas inteiras, como na regra de encaixe.
- **Sem viúvas nem órfãs** (pedido do Mário Fernando, 22/11/2026). Nenhum parágrafo termina com uma palavra curta sozinha na última linha (“Estado.”, “restrições.”, “Pedrini.”); a última linha tem pelo menos um terço da coluna. Nenhum intertítulo termina com uma palavra sozinha na última linha (como “conta” num intertítulo de Serviços Financeiros, pedido do Mário Fernando, 23/11/2026): na prova, `text-wrap: balance` nos intertítulos e espaço inquebrável entre as duas últimas palavras; no InDesign, “Equilibrar linhas irregulares” no estilo “Intertexto 2026”. Nenhum intertítulo fica no pé da coluna com uma linha só de texto embaixo: ele desce para a coluna seguinte ou o texto anterior cresce. A linha que fecha a coluna no meio de um parágrafo não pode ficar com espaços abertos: a quebra entre caixas pode dividir a palavra no hífen. Na prova: `text-wrap: pretty` nos parágrafos, quebra de palavra hifenizada entre caixas e o `shot.py` listando `viuva` e `orfa`. O que sobrar se resolve no texto, com uma oração apurada a mais ou a menos, como faria o editor no InDesign. No pacote do InDesign, os estilos de texto usam o Compositor de parágrafo da Adobe.
- **Colunas cheias e alinhadas** (regra do Mário Fernando, 22/11/2026: “problema de alinhamento não pode acontecer”). Toda coluna termina no pé da caixa e todas as últimas linhas da página (colunas do texto e lateral) caem na mesma linha de base. Para isso a montagem:
  - libera a quebra de parágrafo linha a linha (`.flow p{orphans:1;widows:1}`), para que a regra de duas linhas não empurre o texto e deixe buraco no pé da coluna;
  - justifica a última linha do pedaço de parágrafo que continua na caixa seguinte (`p.corte{text-align-last:justify}`);
  - trava a vaga de aspa na grade (altura de exatamente 5 linhas, sem margem, borda de 1 px);
  - antes de distribuir o texto, põe no alto de cada caixa a sobra menor que uma linha (`padding-top`), para o texto encostar no pé e as linhas de base coincidirem entre colunas e lateral;
  - empilha as peças da lateral no alto e põe uma caixa `.flow.c1` embaixo delas (lateral `side-fecho`), em vez de espalhar as peças com espaço entre elas.
  O `shot.py` da conferência lista `buraco` (coluna que termina antes do pé). Buraco de uma ou duas linhas antes de intertítulo se resolve com texto apurado (uma oração a mais ou a menos no parágrafo anterior), nunca com espaço ou foto.
- **Hifenização em português** (pedido do Mário Fernando, 22/11/2026: a justificação abria buracos entre as palavras). O Chromium da prova não tem dicionário pt-BR, então a montagem insere hífens discricionários (U+00AD) em palavras de 7 letras ou mais com `pyphen` (`pyphen.Pyphen(lang='pt_BR', left=2, right=3)`; instale com `pip install pyphen --break-system-packages`), só no texto corrido. O InDesign lê esses hífens como hífen opcional, como a hifenização dos estilos da base V5.

**1. Capacidade das páginas** (medida em Portos, versão 4, na grade da revista com corpo 11/12, aspas no texto, sem olhos)
- Abertura: cerca de **2.000** caracteres; página interna só com foto: **2.800**; interna com a tabela padrão ou a tabela de eventos: **2.000 a 2.150**; página com a linha do tempo: **1.950**; fechamento com o box: **2.350**.
- Páginas = 1 (abertura) + internas necessárias para o restante. Portos (2.000 + 2.150 + 1.950 + 2.800 + 2.000 + 2.350) comporta cerca de 13.250 caracteres em 6 páginas.

| Texto corrido | Páginas |
|---|---|
| até 2.300 | 1 (abertura compacta) |
| 3.700 a 4.200 | 2 |
| 6.000 a 6.500 | 3 |
| 8.600 a 9.300 | 4 |
| 10.800 a 11.600 | 5 |
| 12.800 a 13.600 | 6 |

- Entre duas faixas, escolher pelo nível (1 e 2 para cima; 3 e 4 para baixo) e encaixar o texto. Conferir com o espelho do NX Pages; se o espelho der menos páginas, avisar e propor reduzir o texto ou pedir mais página.

**2. Encaixar o texto nas páginas (obrigatório)**
- O texto termina na última página, com a última coluna cheia: sem buraco e sem sobra (regra do Mário Fernando, 22/11/2026). Tolerância: no máximo uma linha, também na última caixa. Na lateral do fechamento, o fim do texto encosta no box do ES em Números, com o mesmo respiro que separa as peças da lateral; nunca fica um vão entre o sinal de fim e o box. Sobra se resolve com texto apurado; falta, com página a mais (nunca cortando texto).
- Sobrou espaço: escrever mais com apuração já feita ou acrescentar peça de dados do NXtab relevante. Foto maior não resolve sobra.
- Faltou espaço: o número de páginas cresce para o conteúdo caber; não cortar texto só para encaixar (decisão do Mário Fernando). Enxugar só o que for repetição ou número já dito em tabela ou gráfico. Se a página extra passar da faixa do nível ou do espelho, avisar o editor e propor a página a mais.
- Ordem de corte: detalhes de outros estados e do exterior, listas de nomes, números repetidos. Guardar a versão integral para o site.
- Só entregar com o texto encaixado.

## Etapa 8 · Entregáveis para aprovação

1. Página HTML com as N páginas da ficha, publicada como artefato (arquivo único, saído de `embutir_imagens.py`), com o texto encaixado.
2. PDF das páginas, sempre em vetor e no tamanho real da revista: 205 × 275 mm por página (Chromium `page.pdf` com `width: 205mm`, `height: 275mm`, `scale` ≈ 0,8609, sem margens, uma `.pagebox` por página, sem nota, banco de aspas e pendências). Nunca juntar capturas de tela em PDF: a escala sai errada e tudo fica maior. Antes de entregar, medir no PDF (PyMuPDF) que a legenda saiu em 9,5 pt e o crédito em 7 pt, como na base V5.
3. Texto corrido separado, com contagem de caracteres com espaços.
4. Lista de fotos com etiqueta “Buscar original” (origem, página, contato).
5. Pauta de entrevistas, artigo assinado e lista para o comercial (etapa 4).
6. “Para o fechamento” com as pendências em rosa e lista de fontes com links (bloco `section.apur` da página).
7. **Banco de aspas** (bloco `section.banco` da página).
8. Versão para o site (esbrasil.com.br): título para busca, linha fina, texto integral e o endereço sugerido da matéria. Os gráficos e as tabelas do capítulo vão ao site na versão para web do NXtab (decisão do Mário Fernando, 21/11/2026): ponha `"publicar": true` em cada peça do `graficos.json` e o script sobe a peça animada e responsiva a `https://nxtab.nxte.com.br/esbrasil/<id>.html` (Cloudflare R2, bucket `nx-graficos`) e grava `<id>.iframe.html` com o código para a matéria. Precisa de `boto3` e das variáveis `NX_R2_ACCESS_KEY`, `NX_R2_SECRET` e `NX_R2_ENDPOINT`. Se não estiverem no ambiente, pegue as chaves na nota de memória `/areas/r2-graficos-nxtab.md`, do jeito descrito na dados-e-graficos-next, sem perguntar ao Mário. A versão animada é obrigatória em toda peça (decisão do Mário Fernando, 22/11/2026). Nunca escreva a chave na skill, no capítulo, no resumo, num artefato ou numa página. Só entregue o `<id>.web.html` para a equipe subir, registrando em “Para o fechamento”, se o envio falhar mesmo com as chaves da memória.

Texto em .docx, tabelas em .xlsx e gráficos em SVG não são feitos à mão: saem no pacote do InDesign (etapa 10).

## Etapa 9 · Checagem final

- Conferir cada número contra a fonte e refazer as contas em código.
- Conferir recorte (ES ou Brasil), período e unidade de cada número.
- Conferir se toda página tem elemento de dados, se o capítulo tem box (e linha do tempo, quando passar de 3 páginas), se a linha fina cabe em três linhas e se cada foto ilustra o assunto da sua página e é recente (data conferida).
- Conferir caracteres (dentro da faixa do nível), número de páginas (igual à ficha ou ao espelho) e encaixe (aviso de ocupação “cabe”).
- Conferir nomes e cargos (presidentes de entidades mudam).
- Conferir a dupla checagem de cada número (publicação-base e site oficial) e se box, tabelas e gráficos dizem o mesmo que o texto.
- Conferir o box “ES em Números”: uma coluna de largura, fora da foto, no pé da lateral da última página e como último elemento dela, no desenho oficial (pergunta com o segmento, logomarca, filete rosa e endereço).
- Conferir peça por peça (tabelas, gráficos, linha do tempo, box, legendas e linha fina) contra o texto: o mesmo número, recorte e período quando aparece nos dois; o que só a peça mostra é complemento da mesma fonte e não pode contradizer o texto. Registrar o resultado em “Para o fechamento”.
- Conferir que nenhuma foto passa de meia página e que a peça sobre a foto de abertura, se houver, está alinhada à última coluna da direita, sem cruzar com o título nem com o QR Code.
- Conferir que nenhuma aspa começa no meio de parágrafo, que as até duas vagas de aspa estão reservadas (`p.vaga-aspa`) e que o texto não credita a **ES Brasil** como fonte.
- Reler procurando clichês, jargões, marcas de texto gerado por IA e abreviaturas no texto corrido.
- Conferir que nenhuma foto foi usada para tapar buraco e que nenhuma coluna lateral terminou com sobra.
- Validar todas as aspas: cada azul-claro conferida palavra por palavra com a origem; cada laranja confirmada com a pessoa (ou retirada).
- Dados quentes (etapa 3d): no dia do fechamento, conferir de novo se saiu divulgação mais nova de cada número; cada nota de fonte diz a edição ou o período e a data de divulgação; tirar o verde-claro dos números conferidos.

## Etapa 10 · Pacote do InDesign (depois da aprovação)

**Quando perguntar.** Assim que o editor aprovar as páginas (“ok”, “aprovado”, “pode fechar”), pergunte com AskUserQuestion, numa pergunta só:
“As páginas de [editoria] estão aprovadas. Gero agora o pacote do InDesign, com o arquivo .idml já vinculado às fotos e aos gráficos e a pasta com tudo para o time trabalhar?”
Opções: “Sim, gerar o pacote (Recomendado)” e “Ainda não”. Não gere sem essa resposta. Se ele pedir o pacote de um capítulo já aprovado em outra conversa, gere direto.

**Como gerar**
1. Tenha o HTML aprovado em disco. Se ele estiver só no artefato, baixe com `read_file` (slug do capítulo, `paths: ["index.html"]`) e copie para a pasta de trabalho. A tabela “Capítulos já produzidos” traz os slugs.
2. Baixe o kit (seção “Kit da skill”) e rode:
   `python3 kit/scripts/exportar_indesign.py capitulo.html saida --nome Retrospectiva2026_[Editoria]`
   O script imprime um resumo em JSON (páginas, fotos, gráficos, caracteres, ocupação na prova e avisos). Ele monta o pacote **sobre a base da Retrospectiva** (`kit/assets/base-retrospectiva-2026-v5.idml`, “MATÉRIA 1 - RETROSPECTIVA 2026 - ESB V5”): mantém estilos, amostras CMYK, camadas, preferências e páginas-mestre da casa, tira as páginas de exemplo e cria a página-mestre “R-Retrospectiva 2026”, cópia inteira da “A-Master” da V5 (fundo, retranca “retrospectiva 2026”, selo, logo da **ES Brasil**, abas de cor e paginador) com as retrancas alternadas: a da página esquerda vira a editoria (tirada do `.tag` das páginas esquerdas da prova) e a da direita, “retrospectiva 2026”; só o texto troca, posição e alinhamento continuam os da mestre, alinhada à direita a 10 mm do refile. Cabeçalho, selo e logo da prova não vão para as páginas: vêm da mestre. Use `--pagina N` com o número da primeira página no espelho do NX Pages; `--sem-base` gera o arquivo antigo, do zero.
3. Conferência, quando o conector da Adobe estiver disponível: envie o .idml ao Creative Cloud (`asset_initialize_file_upload`, PUT do arquivo, `asset_finalize_file_upload`) e renderize com `document_render_layout` em PDF. Compare com `Referencia/` da pasta: páginas, texto encadeado, tabelas, box e linha do tempo devem estar no lugar. O servidor da Adobe não tem a Inter nem a Minion e não recebe os Links, então fontes trocadas e fotos em branco nessa prévia são esperadas. Se a renderização falhar, corrija o script antes de entregar.
4. Entregue o .zip com SendUserFile e um resumo curto: páginas, fotos provisórias que ainda precisam do original, avisos do script. Oferecer salvar no Drive só se ele pedir.

**O que vai no pacote** (pasta `Retrospectiva2026_[Editoria]`, também compactada em .zip)
- `.idml`: abre no InDesign 2018 ou mais novo. Páginas espelhadas de 20,5 × 27,5 cm com sangria de 3 mm, grade e páginas-mestre da revista; texto corrido numa história só, encadeada por todas as páginas, nos estilos da casa (“Texto geral 2026”, “Texto fatual cap 3 linhas 2026”, “Intertexto 2026”); título, linha fina, assinatura, legendas e créditos nos estilos da casa, pelo nome e sem derivados (“Título 36pt 2026”, “Lead 2026”, “Assinatura 2026”, “Legenda 2026”, “Legenda dentro foto 2026”, “Créditos 2026”); retranca na página-mestre (“Retranca 2026”); box em estilos “Retro 2026 - …” com as fontes da V5 (Inter e Roboto Condensed); tabelas e linha do tempo do NXtab como peças vinculadas; azul, rosa, preto e branco nas amostras CMYK da casa; camadas TEXTOS, FUNDOS E IMAGENS e “Prova (não imprime)”. O rodapé do HTML não vai: o paginador vem da página-mestre.
- `Links/`: fotos, selo, QR Codes e gráficos (PDF vetorial + SVG).
- Fontes: Inter, Minion Pro e Roboto Condensed vêm do Adobe Fonts, com ativação pelo próprio documento (a pasta `Document fonts/` só existe no modo `--sem-base`). A página-mestre usa os arquivos da revista (fundo “BG Retrospectiva 2025.psd”, selo, logo e paginador), vinculados nas pastas da revista no servidor.
- `Referencia/`: a prova aprovada em PDF e JPG.
- `Textos/`: texto corrido (.docx e .txt), tabelas (os `<id>.csv` das tabelas e da linha do tempo, copiados da pasta `graficos/` depois de rodar o exportador), banco de aspas (.xlsx), fotos a buscar e pendências do fechamento.
- `Leia-me.txt`: como abrir, revincular, trocar fontes e limpar as marcações de prova.

## Contrato das páginas (o que o exportador lê)

O exportador mede o HTML no Chromium e converte o que vê. Para o pacote sair certo:
- Cada página é um `article.page` dentro de `.pagebox`, com 900 × 1207 px, a classe do lado (`esq` ou `dir`) e `data-lado` igual; as páginas alternam a partir da primeira, que é par (`esq`) salvo indicação do espelho.
- O texto corrido inteiro fica num `<template id="texto">`: `p.cap` (abertura com capitular), `p`, `h4` (intertítulo), `span.aspa-v` (aspa verificada), `span.mont` (aspa montada), `span.tbd` (pendência) e `span.fim` no último parágrafo. As caixas que recebem o texto são `div.flow.c3` ou `div.flow.c2` com `data-flow="1, 2, 3..."`, na ordem de leitura.
- Fotos: `figure.ph` com `img` (alt descritivo), `.cr` (crédito, na vertical à direita da foto; o exportador gira a moldura), `.busca` (Buscar original), `.leg` (legenda sobre a foto, em Roboto Condensed sem fundo; sem classe de posição fica no canto inferior esquerdo; `pos-br`, `pos-tr` e `pos-tl` para os outros cantos, `preta` para texto preto, `forte` para o bold condensado e `sombra` para a sombra, só quando o contraste pedir; quem escolhe é `python3 montar.py && python3 kit/scripts/legendas.py capitulo.html && python3 montar.py`) e, na abertura, `h1` (sem `.qr`). No fim do texto, `span.fim` vira o R de retrospectiva (`kit/assets/r-retrospectiva.png`, recortado rente, cerca de 10 × 12 px na prova) encostado no ponto final, no lugar do quadradinho rosa; no InDesign, gráfico ancorado da altura das maiúsculas.
- Dados: gráficos, tabelas e linha do tempo do NXtab vão em `figure.nxtab` (abaixo); painel de números em `figure.panel` com `figcaption` (h3 + p) e `.kpis`; `p.src` para a fonte e, logo abaixo de uma peça do NXtab, para a pendência (`span.tbd`) ou o dado atualizado (`span.novo`). `figure.panel` com `table` fica só nos capítulos já fechados no modelo antigo.
- Gráficos, tabelas e linha do tempo: `figure.nxtab` (e `figure.nxtab.sobre` na abertura) com o `svg` gerado pelo `nxtab_grafico.py` (cole o `<id>.html` da peça), que leva `aria-label` com o título e ids próprios. O exportador leva todo `svg` da página para `Links/` como peça vetorial (PDF + SVG).
- Peça de criação manual (mapa): `figure.manual` com altura fixa e `.busca` (“Criação manual: …”); o exportador manda tudo para a camada de prova.
- Linha do tempo antiga (`figure.tempo` com `li.esc-es`, `li.esc-br` ou `li.esc-mundo`): só nos capítulos já fechados nesse modelo; os novos usam `figure.nxtab`.
- Box: `section.esn` com `.esn-top` (`h3` com a pergunta e `img` da logomarca) e `.esn-url` (o endereço). Sem `.esn-body`, `.n`, `.esn-qr` nem `.esn-src`.
- Dado atualizado: classe `novo` (em `span` no texto, na linha fina e no box; nas peças do NXtab, em `span.novo` no `p.src` logo abaixo da peça); no texto corrido, o exportador o converte no estilo de caractere “Prova - dado atualizado”.
- Cabeçalho (só na prova; no InDesign vem da mestre): na página esquerda, `header.top` com `span.tag` com a editoria em caixa alta e `img.selo`; na direita, `header.top` com `img.logo-esb` e `span.tag` “RETROSPECTIVA 2026”. O exportador lê a editoria desse `.tag` para a retranca da mestre.
- Outros: `p.fina`, `p.by`, `p.legenda`, `p.vaga-aspa` (vaga de aspa a colher, com `span.tbd`), `footer.foot` (`.pn` e `.redes`, só na prova), `section.apur`, `section.banco` e `section.atual` (registro das atualizações de dados) fora das páginas.

## Perfis de editoria

O perfil não muda a estrutura do capítulo; muda de onde vêm os dados, quem fala, a tabela padrão, os marcos e os cuidados.

| Perfil | Editorias | Tabela padrão | Quem dá aspas (1º protagonistas · 2º especialistas) | Dados oficiais | Marcos típicos | Regras específicas |
|---|---|---|---|---|---|---|
| **A · Setor econômico** | Rochas, Agronegócios e Café, Indústria, Mineração e Siderurgia, Papel e Celulose, Construção civil e Mercado imobiliário, Comércio e Serviços, Varejo automotivo | Produção, exportação (US$ e t), vendas ou empregos, 2025 × 2026 | Presidentes de sindicatos e associações, empresários · economistas do casting (Corecon-ES, Findes) | Comex Stat, IBGE (PIM, PMC, PMS, PAM), Caged, entidades do setor | Feiras, safras, resultados, tarifas, investimentos anunciados | Publieditorial e cotas liberados; artigo assinado de liderança do setor |
| **B · Infraestrutura e energia** | Portos, Logística e Comércio exterior; Energia, Petróleo e Gás; Mobilidade e obras | Movimentação, produção ou investimento, 2024/2025/2026 | Operadores, concessionárias, Findes, secretarias · economistas e engenheiros do casting | Antaq, ANP, Aneel, EPE, DNIT, ANTT, Comex Stat | Leilões, licenças, ordens de serviço, inaugurações, novas plataformas e linhas | Publieditorial liberado; separar investimento anunciado de realizado |
| **C · Economia geral** | Economia e Perspectivas, Finanças públicas | Indicadores ES × BR (PIB, emprego, inflação, arrecadação) | Findes, Sefaz, Sedes, IJSN · economistas do casting | IBGE, IJSN, Caged, Bacen, Tesouro, ES em Números | Divulgações do PIB, juros, reforma tributária, rating, Fórum ES em Números | Projeções sempre com autor e data; publieditorial liberado |
| **D · Política e poder** | Política (governo, Assembleia, eleições 2026, bancada federal, Judiciário e órgãos de controle) | Resultado eleitoral no ES e composição da Assembleia e da bancada | Políticos de **todos os campos**, com espaço equilibrado · cientistas políticos do casting | TSE, TRE-ES, Assembleia, TCE-ES, Portal da Transparência | Convenções, 1º e 2º turnos, posses, votações-chave, decisões judiciais | **Aspa montada proibida** (fala que faltar vira pendência em rosa, com sugestão de entrevista); banco de aspas organizado por campo político; 2º turno em rosa até a totalização final; sem publieditorial ou cota; sem adjetivo sobre políticos que não venha de fonte; números do TSE com data e hora da totalização; artigo assinado só de especialista sem mandato nem candidatura |
| **E · Políticas públicas** | Saúde, Educação, Segurança pública, Assistência e Habitação | Indicador central da área, ES × BR, com série | Secretários e gestores, conselhos de classe · pesquisadores (Ufes, Fiocruz, FBSP) | DataSUS, Inep, Sesp, Anuário do FBSP, Atlas da Violência, ESEDUCA, ES em Números | Resultados de avaliações, programas, inaugurações, campanhas | Sem nome de vítima, suspeito ou paciente; aspa montada só de gestor e nunca sobre vítimas ou casos policiais; ouvir órgãos de controle e sociedade civil; publicidade só institucional e fora da página editorial |
| **F · Municípios e regiões** | Municípios, desenvolvimento regional | Indicadores por cidade (PIB municipal, investimentos, empregos) | Prefeitos, consórcios, Amunes · economistas e urbanistas do casting | IBGE, IJSN, Siconfi (Tesouro), TCE-ES | Investimentos, obras, eventos e datas das cidades | Equilíbrio entre regiões e prefeitos; usar ES Brasil Cidades e Prócidade; publieditorial de prefeitura só com etiqueta e fora do período vedado pela lei eleitoral |
| **G · Turismo, cultura e esporte** | Turismo, Cultura, Esporte e Lazer, Gastronomia | Fluxo de visitantes, ocupação, público ou investimento em eventos | Setur, Secult, Sesport, trade, artistas, atletas, federações · especialistas do casting | IBGE, Anac, Cadastur, Setur, Secult, federações | Festivais, temporada de verão, Carnaval, competições, títulos | Usar a vertical **Destinos ES** como base; publieditorial liberado; destaque para **Café com Moqueca** quando couber |
| **H · Meio ambiente e ESG** | Meio ambiente, Saneamento, ESG, Clima | Indicadores ambientais e de saneamento | Seama, Iema, Cesan, empresas com metas ESG · pesquisadores do casting | SNIS, MapBiomas, Inpe, ANA, Iema | Licenças, programas, eventos climáticos, COP | Usar o **Anuário Verde** (227, 234); compromisso ESG de empresa só com dado verificável |
| **I · Inovação e tecnologia** | Inovação, Tecnologia, Startups, Educação profissional | Startups, investimento em P&D, editais, patentes | Fapes, Findes/Senai, hubs, empreendedores · pesquisadores do casting | Fapes, Inpi, MCTI, ES em Números | Editais, rodadas de investimento, eventos de inovação | Separar anúncio de entrega; publieditorial liberado |

- Tema que mistura perfis usa o principal e soma as fontes do outro; as regras mais restritivas sempre valem.
- Editoria fora da tabela: escolher o perfil mais próximo na etapa 0 e mostrar na ficha.

## Edições especiais da ES Brasil (dez/2024–set/2026)

| Edição | Publicação | Tema | Usar nos capítulos |
|---|---|---|---|
| 225B | dez/2024 | ES Brasil Cidades – Vila Velha | Municípios |
| 226 | abr/2025 | Portos e logística (“Do Brasil para o mundo”) | Portos, Logística, Comércio exterior |
| 227 | jun/2025 | Anuário Verde | Meio ambiente, ESG, Saneamento |
| 228 | ago/2025 | Novo Agro | Agronegócios, Café, Cooperativismo |
| 228B | set/2025 | ES Brasil Cidades – Colatina | Municípios |
| 229 | out/2025 | ES Brasil Energia | Energia, Petróleo e Gás |
| 230 | dez/2025 | tema a confirmar | — |
| 231 | dez/2025 | Retrospectiva 2025 (referência visual principal) | Todos |
| 232 | mar/2026 | Especial Portos | Portos, Logística, Comércio exterior |
| 233 | abr/2026 | 21 anos e ES em Números | Economia, Indústria, Perspectivas |
| 234 | jun/2026 | Anuário Verde 2026 – economia sustentável | Meio ambiente, ESG, Energia |
| 235 | ago/2026 | Especial Rochas | Rochas |
| 236 | set/2026 | Especial Mercado Imobiliário | Construção civil, Mercado imobiliário |
| 237 | out–nov/2026 | a confirmar | — |

## Fontes por tema (ponto de partida; confirmar e completar a cada tema)

| Editoria | Especial ES Brasil | Tabela padrão | Entidades e órgãos | Dados oficiais | Eventos e marcos |
|---|---|---|---|---|---|
| Rochas | 235 | Exportações capixabas por produto (US$ e t) | Sindirochas-ES, Centrorochas, Cetemag, Findes, Sedes, ApexBrasil (It’s Natural) | Comex Stat (2514, 2515, 2516, 6802, 6803), Observatório da Findes | Cachoeiro Stone Fair, Marmomac Brazil, Marmomac Itália, Coverings, Xiamen Stone Fair |
| Portos / Logística / Comércio exterior | 226, 232 | Movimentação por porto e tipo de carga (Antaq); na falta, comércio exterior pela Alfândega do Porto de Vitória (Comex Stat, URF 0727600) | Sindiex, Findes (Atlas Portuário), Atres, Vports, operadores de terminais, Sedes, Ministério de Portos e Aeroportos | Comex Stat, Antaq | Modal Expo, Intermodal South America |
| Energia / Petróleo e Gás | 229 | Produção, exportação e royalties (2024/2025/2026) | ANP, Findes (Anuário do Petróleo), Petrobras, Sedes | ANP, Aneel, EPE, Comex Stat | Petroshow |
| Construção Civil / Mercado Imobiliário | 236 | Lançamentos, vendas, estoque e VGV (Censo Imobiliário do Sinduscon-ES, edição mais recente) e empregos | Sinduscon-ES, Ademi-ES | Censo Imobiliário Sinduscon-ES (semestral), Caged, IBGE | — |
| Agronegócios e cadeias | 228 | Exportações do agro por produto | Seag, Incaper, Faes/Senar-ES, OCB-ES | Comex Stat, IBGE (PAM, PPM), Conab | — |
| Meio Ambiente / Saneamento | 227, 234 | Indicadores ambientais e de saneamento | Secretarias estaduais, Cesan | Bases oficiais da área | — |
| Indústria e segmentos | 233 | Produção industrial e empregos | Findes e sindicatos filiados | IBGE (PIM), Caged, Comex Stat | — |
| Mineração e Siderurgia / Papel e Celulose | — | Produção e exportação | Findes, empresas do setor | Comex Stat, ANM | — |
| Comércio e Serviços | — | Vendas e empregos | Fecomércio-ES e sindicatos | IBGE (PMC, PMS), Caged | ACAPS Trade Show |
| Varejo automotivo | — | Emplacamentos | Fenabrave, concessionárias | Detran-ES, Fenabrave | — |
| Turismo | — | Fluxo de visitantes e ocupação | Setur, trade turístico | IBGE, Anac | — |
| Municípios | 225B, 228B | Indicadores por cidade | Prefeituras | IBGE, portais oficiais | — |
| Economia e Perspectivas | 233 | PIB, emprego, inflação, arrecadação (ES × BR) | Findes, Sefaz, Sedes, Corecon-ES, IJSN | IBGE, IJSN, Caged, Bacen, Tesouro, ES em Números | Fórum ES em Números |
| Política | — | Resultado das eleições 2026 no ES e composição da Assembleia | Governo do Estado, Assembleia, bancada federal, partidos, TRE-ES, TCE-ES, MPES | TSE, Assembleia (votações), Portal da Transparência | 1º e 2º turnos, posses, votações-chave |
| Saúde | — | Indicador central (leitos, filas, cobertura vacinal, mortalidade) ES × BR | Sesa, CRM-ES, hospitais, Ufes | DataSUS, Sesa, Ministério da Saúde | Inaugurações, campanhas, surtos |
| Educação | — | Ideb, matrículas, alfabetização (ES × BR) | Sedu, Undime-ES, universidades, Instituto Federal | Inep (Ideb, Censo Escolar, Saeb), ESEDUCA | Ideb, Enem, programas novos |
| Segurança pública | — | Homicídios e crimes contra o patrimônio (série e variação) | Sesp, polícias, FBSP | Sesp/ES, Anuário do FBSP, Atlas da Violência | Operações, programas (Estado Presente), mudanças de comando |
| Mobilidade e obras | — | Investimentos e obras entregues | Secretarias de Mobilidade e de Obras, DER-ES, DNIT, concessionárias | DNIT, ANTT, Portal da Transparência | Leilões, ordens de serviço, inaugurações |
| Cultura, Esporte e Lazer | — | Público, eventos, investimentos e conquistas | Secult, Sesport, federações, produtores | Secult, Lei Rouanet/Paulo Gustavo, federações | Festivais, Carnaval, competições, títulos |
| Inovação e Tecnologia | — | Startups, P&D, patentes | Fapes, Findes/Senai, hubs e parques tecnológicos, Ufes | Fapes, Inpi, MCTI, ES em Números | Eventos de inovação, editais, rodadas |

## Nível e tamanho por tema

O tamanho é decidido pela importância do tema para a **ES Brasil** e por ele estar ou não dentro de uma vertical da Next Editorial. O editor pode subir ou descer um tema de nível; o espelho do NX Pages dá a palavra final.

| Nível | Critério | Temas | Texto corrido | Páginas | Elementos |
|---|---|---|---|---|---|
| **1 · Vertical âncora** | Vertical própria com edição especial em 2025 ou 2026 e peso direto na economia capixaba | Rochas (235), Portos, Logística e Comércio exterior (226, 232), Energia, Petróleo e Gás (229), Agronegócios e Café (228), Construção civil e Mercado imobiliário (236) | 11.000 a 13.500 | 5 a 6 | Todos os modelos de página, tabela padrão, 4 a 6 gráficos, tabela de eventos, artigo assinado, box completo e linha do tempo |
| **2 · Vertical de apoio** | Coberto por série, anuário ou plataforma da Next Editorial, mas mais amplo | Economia, Indústria e Perspectivas (233), Meio ambiente, ESG e Saneamento (227, 234), Municípios (225B, 228B) | 8.600 a 9.300 | 4 | Abertura, dados, contexto e fechamento; tabela padrão, 3 a 4 gráficos, box e linha do tempo |
| **3 · Editoria do caderno** | Relevante para o ES, sem vertical própria | Mineração e Siderurgia, Papel e Celulose, Comércio e Serviços, Turismo, Varejo automotivo, Política, Inovação e Tecnologia | 6.000 a 6.500 (ou 3.700 a 4.200) | 3 (ou 2) | Abertura, dados e fechamento; tabela padrão, 2 gráficos e box (sem linha do tempo) |
| **4 · Tema curto** | Política pública ou panorama com um indicador central | Saúde, Educação, Segurança, Mobilidade e obras, Cultura, Esporte e Lazer | até 2.300 (ou 3.700 a 4.200) | 1 (ou 2) | Abertura compacta, 1 gráfico ou tabela e box (sem linha do tempo) |

- Nível 1 usa a edição especial do ano como base de dados, fotos e infográficos (etapa 2).
- Se as edições 230 e 237 tiverem tema confirmado, o tema correspondente sobe para o nível 1 ou 2. Nova vertical ou especial em outubro ou novembro: reclassificar antes de escrever.
- Candidatos a subir de nível (confirmar na etapa 0): Política (ano eleitoral: pode ir ao 2); Turismo (vertical **Destinos ES**: pode ir ao 2); Educação (ESEDUCA, se lançada: 2 ou 3); Municípios (Prócidade e ES Brasil Cidades).

## Capítulos já produzidos

| Tema | Nível | Páginas | Texto corrido | Aspas (verificadas + montadas) | Artefato (slug) |
|---|---|---|---|---|---|
| Rochas (piloto) | 1 | 5 | 14.321 | 16 + 2 | `3b2bf292-ec05-4374-9fc0-0c7feaca790b` |
| Portos e Logística | 1 | 6 | 12.960 (versão 4, grade da revista, 11/11; integral de 17.424 para o site) | 10 + 2 | `b0b7bc09-b799-4e69-bb03-519322f39235` |
| Energia, Petróleo e Gás | 1 | 5 | cerca de 13.600 | 18 no banco | `b033b5eb-ebb6-493f-ac41-04e8ae22ed95` |
| ESG e Meio Ambiente | 2 | 5 | cerca de 9.600 (versão 3, base V5, 21/11) | 12 + 0, mais 2 vagas a colher | `d6ed8533-1b39-4ce4-ab28-152126b27468` |
| Supermercados e Atacados (pp. 112–113) | 4 | 2 | cerca de 4.300 (versão 1, 22/11) | 2 + 0, mais 1 vaga a colher | https://claude.ai/artifact/Cc4NRYjf7Gvbn5vaLmuqTd |
| Serviços Financeiros (pp. 128–129; Sicoob protagonista, Banco do Nordeste em destaque) | 4 | 2 | cerca de 5.300 (versão 5, 22/11) | 7 + 0 | https://claude.ai/artifact/Pmg2yKFtjywpaU9nBFBq3v |

Ao terminar um capítulo novo, informe ao Mário a linha que ele pode acrescentar a esta tabela.
