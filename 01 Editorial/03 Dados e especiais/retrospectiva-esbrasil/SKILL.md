---
name: "retrospectiva-esbrasil"
description: "Produz capítulos da Retrospectiva 2026 da revista ES Brasil (ESB 238) para qualquer editoria, da ficha às páginas de 20,5 x 27,5 cm com texto encaixado e dados sempre na divulgação mais recente, e, depois da aprovação, pergunta se gera o pacote do InDesign (IDML com vínculos e pasta para o time)."
---

# Retrospectiva 2026 da revista ES Brasil

Um único fluxo para **todas as editorias** da Retrospectiva (setores econômicos, infraestrutura, economia geral, política, políticas públicas, municípios, turismo e cultura, meio ambiente e inovação). Baseado no prompt universal v10 (13/10/2026). O que é próprio de cada tema (números, fotos, marcos, aspas) entra no dossiê e nas páginas, nunca nesta skill.

**Edição:** ESB 238 · fechamento comercial 29/11 · envio de material 03/12 · circulação 09/12/2026.

O trabalho tem três momentos:
1. **Gerar o capítulo** (etapas 0 a 9): ficha, apuração, banco de aspas, páginas no formato da revista.
2. **Aprovação do editor** das páginas.
3. **Pacote do InDesign** (etapa 10): só depois da aprovação, e só depois de perguntar.

## Kit da skill (modelo das páginas e scripts)

O kit (modelo das páginas, base da revista e scripts) vai junto com a skill, na pasta `kit/` ao lado deste SKILL.md, quando ela é instalada pelo pacote .zip ou pelo GitHub (https://github.com/mfernandus/skills_nexteditorial, pasta `retrospectiva-esbrasil`). Antes da etapa 7b (montagem das páginas) e da etapa 10, copie essa pasta `kit/` para a pasta de trabalho. Ela traz `scripts/` (exportar_indesign.py, idml.py, extrair.js, embutir_imagens.py, nxtab_grafico.py), `assets/` (modelo-capitulo.html, grade-esb2026.css, base-materia-esb2026-inter.idml, selo-retrospectiva.png, logo-es-em-numeros.png) e `nxtab.html`, uma cópia do NXtab. O NXtab mais recente fica no artefato público “NXtab” (https://claude.ai/artifact/G5Zau8SX9BaWydqLmndR7Z): se a ferramenta de artefatos estiver disponível, baixe o `index.html` dele para `kit/nxtab.html`; senão, use a cópia do kit.

Se a skill estiver instalada sem a pasta `kit/`, baixe o kit do artefato **“Retrospectiva 2026 · kit do exportador InDesign”**, slug `2662af95-77ba-43d3-8205-463326509342`:

1. Chame a ferramenta de artefatos `read_file` com esse slug e `paths`: `scripts/exportar_indesign.py.txt`, `scripts/extrair.js`, `scripts/idml.py.txt`, `scripts/embutir_imagens.py.txt`, `scripts/nxtab_grafico.py.txt`, `assets/modelo-capitulo.html`, `assets/grade-esb2026.css`, `assets/base-materia-esb2026-inter.idml.b64.txt`, `assets/selo-retrospectiva.png`, `assets/logo-es-em-numeros.png`. A base da revista vai em base64 porque o artefato não serve `.idml`; o exportador a restaura sozinho em `kit/assets/base-materia-esb2026-inter.idml`.
2. Copie cada arquivo salvo para `kit/` na pasta de trabalho, com o mesmo caminho, tirando o `.txt` final dos `.py` (`kit/scripts/exportar_indesign.py`, `kit/scripts/idml.py`, `kit/scripts/embutir_imagens.py`, `kit/scripts/nxtab_grafico.py`, `kit/scripts/extrair.js`, `kit/assets/...`). Para os gráficos, baixe também o NXtab, o construtor de gráficos da Next: `read_file` no artefato “NXtab”, slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`, com `paths: ["index.html"]`, e copie para `kit/nxtab.html`.
3. Dependências: `pip install --break-system-packages playwright pymupdf pillow openpyxl python-docx segno` e um Chrome ou Chromium (`python3 -m playwright install chromium` se não houver Chrome no sistema).
4. Se nada disso estiver disponível, peça ao Mário o .zip da skill (`retrospectiva-esbrasil.zip`), que já traz o kit.

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
- Cartola da editoria no alto, à esquerda, com barra rosa, em caixa alta e com tracking de 0,5 px (a única exceção à regra de caixa baixa); selo oficial “Retrospectiva” no alto, à direita, 15% maior que o original (27,6 px de altura na prova).
- Abertura com foto grande (cerca de metade da página), QR Code no canto superior esquerdo (“Acesse o QR Code e leia a matéria em esbrasil.com.br”) e crédito da foto.
- Título em branco sobre a foto; linha fina em azul logo abaixo.
- Gráfico do NXtab que pode sobrepor a foto, aplicado direto sobre ela, sem moldura branca e sem sombra.
- Texto em 3 colunas com capitular; intertítulos em azul, em caixa alta e baixa (regra da casa: nada em caixa alta); **aspas sempre dentro do texto corrido**, sem olhos destacados.
- Rodapé no padrão do paginador da revista: na página par, número e redes (revistaesbrasil • esbrasil • @esbrasil) do lado de fora; na ímpar, radio.esbrasil.com.br e o número. No InDesign ele vem da página-mestre.

**Da Retrospectiva 2024 (edição 225)** — https://esbrasil.com.br/edicao-225-retrospectiva-2024/
- Gráficos de 2024 podem entrar quando forem relevantes e bonitos, refeitos no NXtab. Registrar no dossiê qual gráfico foi aproveitado e de que página.
- A **tabela padrão do tema** no mesmo formato de 2023, 2024 e 2025 (ex.: Rochas — exportações capixabas por produto, US$ e toneladas, com variação).
- Páginas internas com foto lateral e legenda, e intertítulos que separam os blocos.

**Modelos de página** (estão prontos em `kit/assets/modelo-capitulo.html`)
1. Abertura: foto grande com título, QR Code, painel de dados sobreposto, linha fina e texto em 3 colunas.
2. Dados: tabela padrão no alto, texto em 2 colunas e coluna lateral com foto e gráfico.
3. Contexto: foto em faixa, texto em 2 colunas, gráfico lateral e linha do tempo acima do rodapé.
4. Eventos: foto, tabela de feiras, eventos ou marcos do ano (conforme o perfil), texto em 2 colunas e gráficos na lateral.
5. Fechamento: foto, fim do texto e box “2026 em Números” na lateral.
- A quantidade de modelos segue o número de páginas da ficha. Capítulos menores juntam modelos (2 páginas = abertura + fechamento com tabela padrão; 1 página = abertura compacta com tabela ou gráfico, box e linha do tempo compactos). A linha do tempo e o box nunca saem.
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

## Etapa 3d · Dados quentes (sempre a referência mais recente)

Toda tabela, gráfico, box, linha fina e número do texto usa a **divulgação mais recente** da fonte: na apuração, de novo na montagem das páginas e de novo no fechamento (envio em 03/12). O leitor recebe a revista em dezembro; dado de agosto quando já saiu outubro é dado velho.

**Como buscar**
1. Para cada número do dossiê, ver no calendário abaixo se a fonte já soltou edição ou mês mais novo. Procurar primeiro no site ou boletim oficial da fonte (WebSearch com o nome da pesquisa e o ano; WebFetch na página de divulgação), depois na base NEIA e em esbrasil.com.br (a **ES Brasil** costuma noticiar no dia), depois na plataforma ES em Números.
2. Registrar de cada número: fonte, edição ou período de referência, data de divulgação e link. A nota da tabela ou do gráfico diz isso (ex.: “Fonte: Sinduscon-ES, 47º Censo Imobiliário (1º sem./2026), divulgado em out/2026”).
3. Número novo confirmado depois da prova: trocar na tabela, no gráfico (refeito no NXtab com `nxtab_grafico.py`, mesmo modelo e mesma vaga), no box, na linha fina e no texto, marcado com a classe `novo` (verde-claro na prova) até o editor conferir. Conferir se título, linha fina, linha do tempo e frases de tendência (cresce/cai) dependem do número trocado.
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
- **Onde entram:** sempre no texto corrido, com nome, cargo e verbo de atribuição (“afirma”, “explica”, “avalia”), no parágrafo do assunto. Sem olhos e sem aspas soltas em box.
- Aspa sem origem localizada sai do texto até confirmação.
- Entregar a tabela “Banco de aspas” (situação, quem, aspa, origem, uso no capítulo) junto com as páginas.

## Etapa 4 · Pauta de entrevistas e participações

- Lista de quem ouvir, com 3 perguntas por fonte e prazo de retorno até 25/11.
- **Artigo assinado** de uma liderança da editoria, como em 2025 (presidente de sindicato ou associação nos setores; gestor, pesquisador ou liderança da sociedade civil nos demais; em Política, só especialista sem mandato nem candidatura), com tema sugerido e tamanho. Não conta no texto corrido; trechos podem virar aspas verificadas.
- Empresas e entidades com potencial de **publieditorial** ou cota, para a área comercial (fechamento comercial 29/11), **só nos perfis que permitem**. Anúncio nunca encosta em matéria sobre o próprio anunciante sem a etiqueta de publicidade.

## Etapa 5 · Estrutura editorial

- Título curto e afirmativo (até 8 palavras) e linha fina com o número-chave do ano.
- Abertura com o saldo do ano e a comparação com 2025.
- Intertítulos a cada 1.200–1.800 caracteres.
- Aspas na quantidade da ficha, distribuídas pelas seções.
- Fecho com perspectivas para 2027 (metas do setor, agenda do governo eleito, projetos e calendário, conforme o perfil).
- Tom informativo e analítico, sem opinião da revista; adjetivos só atribuídos a fontes.
- Nada em caixa alta (título, intertítulo, título de gráfico, etiquetas): caixa alta e baixa sempre, exceto siglas e a cartola da editoria, que vai em caixa alta (escrita já em maiúsculas no HTML, para chegar assim ao InDesign).

## Etapa 6 · Elementos fixos de todo capítulo

**Box “2026 em Números”** (assinado pela plataforma ES em Números)
- Logomarca **ES em Números** no topo, numa faixa clara (a marca não entra vazada sobre fundo escuro); corpo do box em navy.
- 5 indicadores, cada um com etiqueta ES ou BR; sempre que existir, o dado vem da plataforma ES em Números.
- QR Code para esemnumeros.esbrasil.com.br e linha de fontes.
- Se a plataforma ainda não tiver o indicador do tema, registrar em “Para o fechamento” como pauta para alimentá-la.

**Linha do tempo do ano**
- Faixa horizontal de cerca de 4 a 5 cm de altura, em largura total, logo acima do rodapé da página com mais respiro.
- De 6 a 9 marcos em ordem cronológica: mês, título curto (até 6 palavras) e uma linha de detalhe; outubro e novembro em rosa até o fechamento.
- Prioridade: 1º fatos da editoria no **Espírito Santo**; 2º no **Brasil**; 3º do exterior que afetaram o tema. Pelo menos metade dos marcos é do ES.
- Etiqueta de escopo em cada marco — ES (navy), BR (ciano) ou Mundo/país (cinza) —, fontes no pé da faixa.

**Gráficos: sempre no NXtab** (construtor de gráficos da Next, artefato “NXtab”, slug `7a1c22c8-3982-455a-ab9a-cac69d588c8c`)
- Todo gráfico do capítulo (colunas, barras, rosca, faixa ou painel de números) sai do NXtab, num modelo da biblioteca da revista: `c-percentual` (uma série com destaque), `c-colunas` (séries por ano), `c-barras` (barras horizontais), `c-rosca` (participação), `c-faixa` e `c-lista` (números), `v-fita` e `v-leque`. Não desenhar gráfico à mão.
- Como gerar: descreva as peças num `graficos.json` (id, modelo, vaga, título, subtítulo, fonte, csv e, se houver, destaque) e rode `python3 kit/scripts/nxtab_grafico.py kit/nxtab.html graficos.json graficos/`. O script roda o próprio NXtab, aplica o modelo, troca os dados e entrega, por peça, o SVG que vai para a página, o projeto `.nxtab.json` (abre no NXtab para ajustes), a prévia em PNG e o `<figure>` pronto para colar no capítulo.
- Vagas: `abertura` (painel sobre a foto de abertura, 320 px), `lateral` (coluna lateral das internas, 270 px) e `larga` (largura total, 828 px). A escala de cada vaga faz os dados saírem perto de 6,5 pt no impresso.
- O título do gráfico sai em caixa alta e baixa (o script desliga a caixa alta do NXtab). A peça vai direto sobre a foto ou a página: sem o cerco branco do NXtab, sem sombra e sem drop shadow. Ajuste fino fica com o diagramador.
- Na coluna lateral, use rótulos curtos (até 12 caracteres, como “EUA”), para não quebrarem em duas linhas.
- **Escala quebrada quando um valor domina** (modelo de referência: “Para onde vão as cargas”, capítulo de Portos, versão 3.6). Em barras e colunas de uma série, quando o maior valor passa de 2 vezes o segundo, o eixo vai só até o segundo valor; a barra do maior encosta no fim do eixo com a marca de quebra (//), o número dela continua escrito por inteiro e a fonte ganha a nota “[item]: barra fora de escala.”. Assim os valores menores ficam visíveis e continuam proporcionais entre si. O `nxtab_grafico.py` faz isso sozinho (campo `quebra`: `auto`, o padrão; `true` força no maior; `false` desliga; `nota_quebra` troca o texto da nota) e informa no relatório qual barra quebrou.
- Nunca esticar ou encolher barras fora de proporção sem a marca de quebra, e não usar escala logarítmica: o leitor lê o tamanho errado. Se dois valores dominarem juntos, pôr os dois em números de destaque no alto do box e as barras só para os demais.
- Cores e hierarquia são as do NXtab na marca **ES Brasil**: barras azuis em degradê, destaque em magenta, título em Inter 900, subtítulo em Inter 300 e fonte colada no box.
- **Mapas e outras construções ilustradas** (mapa de portos, rotas, localização de projetos): não desenhar. Reservar o espaço com `figure.manual` e a etiqueta rosa “Criação manual”, descrevendo o que a peça deve mostrar (pontos, legenda, fonte). O espaço vai para a camada “Prova (não imprime)” do InDesign e o diagramador cria a peça. Registrar também em “Para o fechamento”.
- Tabelas (tabela padrão, de eventos ou de projetos) continuam como tabelas no HTML, que viram tabelas nativas no InDesign: cabeçalho navy, linhas alternadas, total em azul-claro, variação em verde ou vermelho.

**Escala tipográfica dos boxes, gráficos e tabelas** (px na prova de 900 px · pt no impresso)
- Título do box: 12 px · 7,7 pt, Inter Black. Subtítulo: 10,5 px · 6,8 pt. Dados (rótulos, valores, células das tabelas, legendas dos números): 10 px · 6,5 pt. Número em destaque: 18 px · 11,6 pt, Inter Black. Miúdos (fonte, eixos, notas, etiquetas ES/BR, detalhe da linha do tempo): 9 px · 5,8 pt.
- O modelo do kit já traz essa escala. Os gráficos do NXtab seguem a hierarquia do próprio NXtab, com os dados na mesma faixa de 6,5 pt.

**Regras de página**
- **Toda página tem, no mínimo, uma foto e um elemento de dados** (gráfico, tabela, infográfico ou linha do tempo).
- Paleta **ES Brasil**: azul #00427B e navy dos infográficos #0F2D5C, ciano #18A6E6, rosa #E01E70 (destaques e pendências), azul-pastel #A2D2FF.
- Tipografia: a da base da revista (“MATÉRIA 1 - BASE - ESB2026”, versão com Inter). Texto corrido em **Minion Pro Cond 11/12** (estilo “Texto geral 2026”; na prova, Crimson Pro em 15,79 px, calibrada para ocupar a mesma largura); abertura com capitular de 3 linhas; intertítulo em Inter Black 11/12, azul, em caixa alta e baixa; título sobre a foto em Inter Black 36 pt; linha fina em Inter Bold 16/16; assinatura em Inter Black 11; legendas em Inter 9,5/11; créditos em Inter Light 7, na vertical, à direita da foto; retranca (editoria) em Inter Black 12, em caixa alta. Tabelas, boxes, linha do tempo e gráficos seguem a escala tipográfica dos boxes, em **Inter**.
- Formato e grade: 20,5 × 27,5 cm, páginas espelhadas, sangria de 3 mm; margens de 22 mm em cima, 15 mm embaixo, 17 mm na lombada e 12 mm do lado de fora; 3 colunas de 55,8 mm com 4 mm entre elas. Abertura com texto em 3 colunas; internas com texto em 2 colunas e a coluna lateral de 55,8 mm. O modelo traz tudo isso em `kit/assets/grade-esb2026.css`. A primeira página do capítulo é par (esquerda); se o espelho abrir em página ímpar, troque as classes `esq`/`dir`.
- Sempre em destaque: **ES Brasil**, **revista ES Brasil**, **Café com Moqueca**.

## Etapa 7 · Fotos

- **Ordem de busca:** (1) originais das edições da **ES Brasil** (pasta de links do InDesign da edição especial e da 231) e banco NX Fotos; (2) fotos oficiais de entidades e assessorias; (3) organizadoras das feiras; (4) Adobe Stock licenciado.
- **Resolução mínima:** 300 dpi no tamanho de uso (abertura de página inteira: cerca de 2.500 px de largura). Nunca ampliar foto de site.
- Foto provisória é permitida com a etiqueta rosa **“Buscar original”** dizendo onde está a certa: “ES Brasil [nº], p. [x] — pedir original a [fonte]” ou “esbrasil.com.br, matéria de [data]”.
- Crédito no padrão “Foto: [autor]/[veículo ou Divulgação]”; conferir licença antes de reusar imagem de banco.

## Etapa 7b · Diagramação e encaixe do texto

- Montar as páginas **a partir de `kit/assets/modelo-capitulo.html`**, no tamanho fixo da revista (20,5 × 27,5 cm, 900 × 1207 px na tela). O modelo já traz o fluxo do texto entre as caixas, a medição de ocupação e as classes que o exportador do InDesign lê (ver “Contrato das páginas”). Não renomear classes nem trocar a estrutura.
- Trabalhar com as fotos em arquivos ao lado do HTML (caminhos relativos). Antes de publicar a prova, rodar `python3 kit/scripts/embutir_imagens.py capitulo.html capitulo-prova.html --qr-materia URL_DA_MATERIA`, que embute as imagens e gera os QR Codes; publicar o arquivo resultante como artefato.
- Corpo do texto corrido: 11 pt com entrelinha de 12 pt (Minion Pro Cond), como na base da revista.
- O texto corrido flui de página em página e o aviso de ocupação no alto da prova diz se cabe ou quantos caracteres sobram. Nunca preencher sobra com espaço em branco: página com buraco recebe foto maior, gráfico ou painel de números.

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
- O texto termina na última página, com a última coluna cheia: sem buraco e sem sobra. Tolerância: cerca de 5 linhas vazias (≈ 250 caracteres).
- Sobrou espaço: primeiro ajustar elementos (foto maior, gráfico relevante, painel de números); se ainda faltar mais de 1/4 de página, escrever mais com apuração já feita.
- Faltou espaço: primeiro editar o texto (enxugar, tirar número repetido de tabela ou gráfico); só depois reduzir foto. Se exceder mais de meia página, ir para a faixa seguinte, se o nível e o espelho permitirem.
- Ordem de corte: detalhes de outros estados e do exterior, listas de nomes, números repetidos. Guardar a versão integral para o site.
- Só entregar com o texto encaixado.

## Etapa 8 · Entregáveis para aprovação

1. Página HTML com as N páginas da ficha, publicada como artefato (arquivo único, saído de `embutir_imagens.py`), com o texto encaixado.
2. PDF das páginas.
3. Texto corrido separado, com contagem de caracteres com espaços.
4. Lista de fotos com etiqueta “Buscar original” (origem, página, contato).
5. Pauta de entrevistas, artigo assinado e lista para o comercial (etapa 4).
6. “Para o fechamento” com as pendências em rosa e lista de fontes com links (bloco `section.apur` da página).
7. **Banco de aspas** (bloco `section.banco` da página).
8. Versão para o site (esbrasil.com.br): título para busca, linha fina, texto integral e o link do QR Code da abertura.

Texto em .docx, tabelas em .xlsx e gráficos em SVG não são feitos à mão: saem no pacote do InDesign (etapa 10).

## Etapa 9 · Checagem final

- Conferir cada número contra a fonte e refazer as contas em código.
- Conferir recorte (ES ou Brasil), período e unidade de cada número.
- Conferir se toda página tem foto e elemento de dados, box e linha do tempo.
- Conferir caracteres (dentro da faixa do nível), número de páginas (igual à ficha ou ao espelho) e encaixe (aviso de ocupação “cabe”).
- Conferir nomes e cargos (presidentes de entidades mudam).
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
   O script imprime um resumo em JSON (páginas, fotos, gráficos, caracteres, ocupação na prova e avisos). Ele monta o pacote **sobre a base da revista** (`kit/assets/base-materia-esb2026-inter.idml`): mantém estilos, amostras CMYK, camadas, preferências e páginas-mestre da casa, tira as páginas de exemplo e cria a página-mestre “R-Retrospectiva 2026” (cópia da mestre de 3 colunas só com o paginador). Use `--pagina N` com o número da primeira página no espelho do NX Pages; `--sem-base` gera o arquivo antigo, do zero.
3. Conferência, quando o conector da Adobe estiver disponível: envie o .idml ao Creative Cloud (`asset_initialize_file_upload`, PUT do arquivo, `asset_finalize_file_upload`) e renderize com `document_render_layout` em PDF. Compare com `Referencia/` da pasta: páginas, texto encadeado, tabelas, box e linha do tempo devem estar no lugar. O servidor da Adobe não tem a Inter nem a Minion e não recebe os Links, então fontes trocadas e fotos em branco nessa prévia são esperadas. Se a renderização falhar, corrija o script antes de entregar.
4. Entregue o .zip com SendUserFile e um resumo curto: páginas, fotos provisórias que ainda precisam do original, avisos do script. Oferecer salvar no Drive só se ele pedir.

**O que vai no pacote** (pasta `Retrospectiva2026_[Editoria]`, também compactada em .zip)
- `.idml`: abre no InDesign 2018 ou mais novo. Páginas espelhadas de 20,5 × 27,5 cm com sangria de 3 mm, grade e páginas-mestre da revista; texto corrido numa história só, encadeada por todas as páginas, nos estilos da casa (“Texto geral 2026”, “Texto fatual cap 3 linhas 2026”, “Intertexto 2026 - caixa alta e baixa”); título, linha fina, assinatura, retranca, legendas e créditos nos estilos da casa (“Título 36pt 2026 - sobre foto”, “Lead 2026”, “Assinatura 2026”, “Retranca 2026 - Retrospectiva”, “Legenda 2026”, “Legenda dentro foto 2026”, “Créditos 2026”); tabelas, box e linha do tempo em estilos “Retro 2026 - …”; tabelas nativas; azul, rosa, preto e branco nas amostras CMYK da casa; camadas TEXTOS, FUNDOS E IMAGENS e “Prova (não imprime)”. O rodapé do HTML não vai: o paginador vem da página-mestre.
- `Links/`: fotos, selo, QR Codes e gráficos (PDF vetorial + SVG).
- Fontes: Inter e Minion Pro vêm do Adobe Fonts, com ativação pelo próprio documento (a pasta `Document fonts/` só existe no modo `--sem-base`).
- `Referencia/`: a prova aprovada em PDF e JPG.
- `Textos/`: texto corrido (.docx e .txt), tabelas (.xlsx), banco de aspas (.xlsx), fotos a buscar e pendências do fechamento.
- `Leia-me.txt`: como abrir, revincular, trocar fontes e limpar as marcações de prova.

## Contrato das páginas (o que o exportador lê)

O exportador mede o HTML no Chromium e converte o que vê. Para o pacote sair certo:
- Cada página é um `article.page` dentro de `.pagebox`, com 900 × 1207 px, a classe do lado (`esq` ou `dir`) e `data-lado` igual; as páginas alternam a partir da primeira, que é par (`esq`) salvo indicação do espelho.
- O texto corrido inteiro fica num `<template id="texto">`: `p.cap` (abertura com capitular), `p`, `h4` (intertítulo), `span.aspa-v` (aspa verificada), `span.mont` (aspa montada), `span.tbd` (pendência) e `span.fim` no último parágrafo. As caixas que recebem o texto são `div.flow.c3` ou `div.flow.c2` com `data-flow="1, 2, 3..."`, na ordem de leitura.
- Fotos: `figure.ph` com `img` (alt descritivo), `.cr` (crédito, na vertical à direita da foto; o exportador gira a moldura), `.busca` (Buscar original), `.leg` (legenda sobre a foto) e, na abertura, `h1` e `.qr`.
- Dados: `figure.panel` com `figcaption` (h3 + p), `table` (tabela, `tr.tot` para total, `td.up` e `td.dn` para variação) ou `.kpis`, e `p.src` para a fonte.
- Gráficos: `figure.nxtab` (e `figure.nxtab.sobre` na abertura) com o `svg` gerado pelo `nxtab_grafico.py`, que leva `aria-label` com o título.
- Peça de criação manual (mapa): `figure.manual` com altura fixa e `.busca` (“Criação manual: …”); o exportador manda tudo para a camada de prova.
- Linha do tempo: `figure.tempo` com `li.esc-es`, `li.esc-br` ou `li.esc-mundo` (mais `.tbd` para marco pendente), contendo `.e`, `.m`, `b` e `.x`.
- Box: `section.esn` com `.esn-top`, `.esn-body`, `.n` (i, b, span), `.esn-qr` e `.esn-src`.
- Dado atualizado: classe `novo` (em `span` no texto, na linha fina e no box; em `td` na tabela); no texto corrido, o exportador o converte no estilo de caractere “Prova - dado atualizado”.
- Outros: `header.top` (`.tag` do lado de fora e `img.selo` do lado da lombada), `p.fina`, `p.by`, `p.legenda`, `footer.foot` (`.pn` e `.redes`, só na prova), `section.apur`, `section.banco` e `section.atual` (registro das atualizações de dados) fora das páginas.

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
| **3 · Editoria do caderno** | Relevante para o ES, sem vertical própria | Mineração e Siderurgia, Papel e Celulose, Comércio e Serviços, Turismo, Varejo automotivo, Política, Inovação e Tecnologia | 6.000 a 6.500 (ou 3.700 a 4.200) | 3 (ou 2) | Abertura, dados e fechamento; tabela padrão, 2 gráficos, box e linha do tempo |
| **4 · Tema curto** | Política pública ou panorama com um indicador central | Saúde, Educação, Segurança, Mobilidade e obras, Cultura, Esporte e Lazer | até 2.300 (ou 3.700 a 4.200) | 1 (ou 2) | Abertura compacta, 1 gráfico ou tabela, box e linha do tempo compactos |

- Nível 1 usa a edição especial do ano como base de dados, fotos e infográficos (etapa 2).
- Se as edições 230 e 237 tiverem tema confirmado, o tema correspondente sobe para o nível 1 ou 2. Nova vertical ou especial em outubro ou novembro: reclassificar antes de escrever.
- Candidatos a subir de nível (confirmar na etapa 0): Política (ano eleitoral: pode ir ao 2); Turismo (vertical **Destinos ES**: pode ir ao 2); Educação (ESEDUCA, se lançada: 2 ou 3); Municípios (Prócidade e ES Brasil Cidades).

## Capítulos já produzidos

| Tema | Nível | Páginas | Texto corrido | Aspas (verificadas + montadas) | Artefato (slug) |
|---|---|---|---|---|---|
| Rochas (piloto) | 1 | 5 | 14.321 | 16 + 2 | `3b2bf292-ec05-4374-9fc0-0c7feaca790b` |
| Portos e Logística | 1 | 6 | 12.960 (versão 4, grade da revista, 11/11; integral de 17.424 para o site) | 10 + 2 | `b0b7bc09-b799-4e69-bb03-519322f39235` |
| Energia, Petróleo e Gás | 1 | 5 | cerca de 13.600 | 18 no banco | `b033b5eb-ebb6-493f-ac41-04e8ae22ed95` |
| ESG e Meio Ambiente | 2 | 4 | cerca de 10.900 | 13 + 0 | `d6ed8533-1b39-4ce4-ab28-152126b27468` |

Ao terminar um capítulo novo, informe ao Mário a linha que ele pode acrescentar a esta tabela.