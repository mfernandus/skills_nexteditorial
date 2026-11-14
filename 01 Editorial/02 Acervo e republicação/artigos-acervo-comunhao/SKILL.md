---
name: "artigos-acervo-comunhao"
description: "Rotina diária que republica às 8h, no site da Comunhão, um texto autoral assinado do acervo (artigo, opinião ou gestão que não seja repercussão de factual), com in memoriam, data original, nota de contexto, regras de rejeição e story enviado para revisão da Joviana e do Mário."
---

# Artigos do acervo — Comunhão (8h)

Objetivo: todo dia às 8h, um texto autoral assinado por um dos articulistas mais importantes da casa volta ao ar no site da Comunhão (comunhao.com.br), com o texto do autor preservado, a data da publicação original no rodapé, "in memoriam" quando o autor já morreu e nota de contexto quando o texto pede. O story do Instagram fica pronto **em revisão**, para a Joviana e o Mário aprovarem.

A **ES Brasil** tem rotina irmã, `artigos-acervo-esbrasil`, com as mesmas regras. Mudança de regra comum às duas se faz nas duas.

Responda sempre em português do Brasil. Execução agendada: não faça perguntas. Na dúvida, tome a decisão mais conservadora (trocar de texto) e registre no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns: publicação direta (2), pautas proibidas (2.1, vale acima de tudo), matéria agendada (2.2, vale acima de tudo), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), SEO (8), imagem destacada (9) e avisos (10). Onde as duas divergirem, vale esta skill nestes pontos (decisões do Mário Fernando):

- **O texto do articulista não se reescreve** e nenhum número dele é atualizado: texto assinado é opinião do autor. O que mudou desde então vai na Nota de contexto, que traz sempre os dados atualizados, com fonte e ano, e a peça do NXtab quando o dado couber num modelo (padrão, seções 12 e 13); se a mudança compromete o texto, ele é rejeitado (seção 6). (30/10/2026; dados e NXtab em 13/11/2026)
- **Título original mantido** (seção 8). (30/10/2026)
- **Rodapé próprio** (in memoriam, minibio, origem e aviso de republicação) no lugar do "Com informações de". (30/10/2026)
- **Story só com revisão:** a rotina deixa o story em "Para revisar" e não aprova, não agenda e não publica story. A Joviana e o Mário revisam e decidem quando sai (seção 10). (02/11/2026)
- **Articulista vivo não é avisado** antes da republicação. (02/11/2026)

### Quem é dono de quê no acervo da Comunhão

- **Esta rotina (8h):** texto autoral assinado por articulista (seção 2), publicado sem mudar o texto do autor.
- **Rotina `acervo-comunhao` (produção às 19h59, no ar às 22h):** reportagem, entrevista e matéria da redação, adaptadas e atualizadas, publicadas direto e agendadas para as 22h, com Destaques até o meio-dia seguinte (decisão de 02/11/2026).
- Um texto original nunca é usado pelas duas (seção 11).

## 1. Roteiro da execução

A tarefa agendada começa por volta das 7h30. Hora certa: `TZ=America/Sao_Paulo date`.

1. Carregue `padrao-publicacao-next` e as ferramentas do NEIA e do NX Feed (ToolSearch).
2. Veja o que a rotina já fez e o que está no site (seção 11).
3. Escolha o articulista do dia e o texto (seções 2 a 7).
4. Monte a matéria no NX Feed (seção 8).
5. **Agende** a matéria para as 8h00 de hoje (seção 9).
6. Logo depois, **barre o story automático** que o painel cria para a matéria agendada (seção 10.1).
7. Espere a matéria ir ao ar e confirme que está no ar (seção 9).
8. Faça o story **para revisão** (seção 10.2).
9. Mande o resumo (seção 12).

## 2. O que entra

Entra texto **autoral e assinado**: o autor defende uma ideia, analisa um tema, ensina ou orienta o leitor com a própria voz. O texto chega por um destes dois caminhos.

### 2.1 Editoria Artigos (decisão de 30/10/2026)

- **Revista:** o texto completo (`get-article-content`) começa com o cabeçalho da editoria antes do título. Contam: "ARTIGO", "Artigo", "ARTIGOS", "ARTIGO ESPECIAL", "Artigo | Cotidiano" e erros evidentes de digitalização da palavra ("ÁRTICO", "ANTIQUO"). Exemplo: "ARTIGO / Hernandes Dias Lopes / QUANDO OS LOBOS…".
- **Site:** post da categoria **Artigos** (id 2, em `wp_categories`).

### 2.2 Opinião, análise e gestão de outras editorias (decisão de 02/11/2026)

Texto assinado que saiu com cabeçalho de outra editoria (VIDA CRISTÃ, FAMÍLIA, IGREJA, MISSÕES, LIDERANÇA, GESTÃO, COMPORTAMENTO, CULTURA, OPINIÃO, ATUALIDADE...), ou post de outra categoria do site, entra quando passa nos **três testes**:

1. **É autoral.** Assinado por articulista ou colaborador ("Por Fulano" no início ou minibio de colaborador no fim), com a tese do próprio autor. Citações de terceiros e versículos só apoiam o argumento. Reportagem (texto apoiado em entrevistados e apuração), entrevista, perfil, testemunho contado pela redação, nota e matéria assinada pela redação ou por jornalista da casa **não** são autorais, mesmo assinados: são da rotina `acervo-comunhao`.
2. **É opinião, análise, ensino ou gestão.** Defende uma posição, interpreta um tema ou orienta o leitor: vida cristã, família, igreja, liderança e gestão da igreja, missões, ética, sociedade, comportamento.
3. **Não é repercussão de factual.** O texto não nasceu para comentar um fato da época: eleição, decisão de governo, lei votada, escândalo, tragédia, crise, evento, congresso, campanha do ano, posse, morte. **Teste:** tire o fato da semana; se o argumento cai, é repercussão e não entra. Texto que usa um fato antigo só como exemplo de uma tese que continua de pé pode entrar.

Na dúvida em qualquer um dos três, fica fora.

### 2.3 Continua fora

- **Coluna**, mesmo assinada: Palavra de Pastor, Estudo Bíblico, Fim de Papo, Som & Cia, Administração, Pregador/Púlpito, O Endereço da História, Modus Vivendi, Mindset, Essas Mulheres, Zoom Marketing, Família S/A, Tira-Gosto, Pratos do Dia, Periscópio, Gente, O editor recomenda, Panorâmicas.
- **"ARTIGO DO LEITOR"** e carta de leitor: não é articulista da casa (confirmado em 02/11/2026).
- Editorial, reportagem, entrevista, página sem cabeçalho legível.
- Texto de retrospectiva ou balanço do ano: é repercussão por natureza.
- O tipo (`content_type` "article" ou "column") e a seção que a NEIA atribui são só pista: erram para os dois lados (na conferência de 30/10, um em cada quatro; quase tudo vem como "Cultura"). Vale o cabeçalho da página (revista), a categoria e a assinatura (site) e a leitura do texto.

## 3. Fontes no NEIA

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch. Uma chamada de cada vez; "Não foi possível conectar": repita a mesma chamada.

| Fonte | Id | O que tem |
|---|---|---|
| REVISTA COMUNHÃO | 019ca1b0-1295-72f0-baaf-31867a70431e | Edição 1 (mar/1997) à 325 (dez/2025) |
| COMUNHAO.COM.BR | 019ca1ae-c3a6-718c-b1f2-e577c04f3ed8 | Posts do site |

- **Revista:** `search-content` com `source`, `author` = nome do articulista, `query` "artigo" (e, para a seção 2.2, `query` com o tema: "vida cristã", "família", "liderança", "igreja"), `page_size` 200. O filtro de autor funciona na revista. Teste as grafias da seção 4: erros de digitalização somem da busca por autor. Quando a grafia não aparecer, busque sem `author` e leia o texto.
- **Site:** o campo `author` é quem postou no WordPress (Fabio Barbosa, Mario Fernando Souza...), **não** o articulista; o filtro de autor não acha o articulista. Busque por tema e pelo nome do articulista na fonte do site e leia com `get-article-content`: o articulista está em "**Por Fulano**" no começo, na minibio do fim ("**Fulano** é...") e em `metadata.llm_author`. O nome dele costuma estar também nas tags (`wp_tags`).
- O `published_at` de um post que já é republicação é a data nova; a original só aparece no texto ("Este artigo foi publicado originalmente em…").
- `get-article-content` traz o texto completo; no site, também `wp_post_id`, `wp_url`, `published_at` e `featured_image`.
- **Prefira a revista.** O post do site entra quando o texto só existe lá.
- **Corte de tempo:** publicação original com pelo menos 12 meses no dia da execução.

### 3.1 Datas: conferir antes de usar

- `list-editions` (project_id = id da revista) dá a data de cada edição. Na revista, use **só mês e ano**.
- Algumas edições (16 a 32, por exemplo) vêm com a data de ingestão de 2026, não a de publicação. Deduza pela sequência mensal das edições vizinhas e por marcas do texto (Natal, Páscoa, "Campanha 2012", o Censo, Copa). Registre "data deduzida" no resumo.
- O mesmo texto pode estar em mais de uma edição ou na revista e no site. O original é o **mais antigo**. Post do site que já é republicação traz "Este artigo foi publicado originalmente em…": use a data citada, conferida na revista quando possível.

## 4. Articulistas

Ordem de prioridade. Grafias que a NEIA usa entre parênteses. Status conferido em 30/10/2026; reconfira a cada uso (seção 7.1).

**Nível A**
- Hernandes Dias Lopes (Rev. Hernandes Dias Lopes; digitalização: Hernandez, Hemandes, Hornandes, Horeandes). Vivo; pastor titular da Primeira Igreja Presbiteriana de Vitória. As colunas Palavra de Pastor e Estudo Bíblico dele não entram. Os textos dele com tema político ou eleitoral também não (seção 6.3).
- Atilano Muradas (Atiliano Muradas, Pr. Atilano Muradas). Vivo.
- Gilson Bifano (Pr. Gilson Bifano). Vivo.
- Josué Campanhã (Pr. Josué Campanhã; a busca não acha "Campanha" sem til). Vivo. A coluna Palavra de Pastor não entra.
- José Ernesto Conti. Vivo. A coluna Fim de Papo não entra.
- Dinart Barradas (Pr. Dinart Barradas, Dinart e Norma Barradas; digitalização: DINARTI GARGADAS). Status não confirmado. A coluna de áudio Som & Cia não entra.
- João Carlos Marins. Status não confirmado.
- Russell Shedd (Russell P. Shedd). **In memoriam**: morreu em 26/11/2016, em São Paulo. Em 26/11/2026 a morte completa 10 anos, no dia de Ação de Graças: data reservada para um texto dele.

**Nível B:** Marcelo Aguiar · Lourenço Stelio Rega (no site há textos dele cedidos pela Cristianismo Hoje: fora) · Jr. Vargas (Rev. Haveraldo Ferreira Vargas Jr.; não confundir com o pai, Presb. Haveraldo Ferreira Vargas, que morreu em 2025) · Erni Walter Seibert · Erasmo Vieira · Jorge Linhares · Romney Cruz · Joarês Mendes de Freitas · Ivonildo Teixeira · Nelson Bomilcar · Simonton Araújo · Waldemar Rocha Junior · Devi Titus · Ariovaldo Ramos · Valdir Steuernagel · Jilton Moraes.

**Só coluna, fora:** Idálio Gomes da Silva (Administração) · Jesus Gonçalves (Pregador/Púlpito) · Evaldo Carlos e Gedimar de Araújo (Palavra de Pastor). Se um texto deles sair fora da coluna e passar na seção 2, ele entra.

A planilha "Lista de artigos do acervo — ES Brasil e Comunhão" (30/10/2026) traz a contagem por articulista, as edições, o status e as fontes. Ela foi feita pela regra antiga (só a editoria Artigos): os textos da seção 2.2 não estão nela.

### Rotação

- Um texto por dia neste portal (confirmado em 02/11/2026). Nível A em 4 a 5 dias da semana; nível B completa a semana.
- O mesmo articulista não repete em menos de 5 dias.
- Dentro do articulista, comece pelos textos mais antigos ainda não usados, salvo gancho de calendário.
- Articulista novo achado na base (assina 3 ou mais textos que passam na seção 2) pode entrar no nível B; registre no resumo para o Mário incluir na lista.

### Fora da lista, sempre

- Político com mandato, candidato ou pré-candidato e artigo de autoridade sobre o próprio governo.
- Texto de terceiros reproduzido pela revista ou pelo site: crônica de outro veículo, capítulo de livro, artigo traduzido de autor estrangeiro, texto cedido pela Cristianismo Hoje, poema ou letra de outro autor, coletânea de frases ou "lições" alheias, release.
- Autor que pediu para não ser republicado (lista de exclusão do Mário; vazia em 02/11/2026).

## 5. Escolha do texto do dia

1. Veja o que a rotina já publicou (seção 11) e escolha o articulista do dia pela rotação.
2. Liste os textos dele (seção 3) e descarte os já usados, por esta rotina ou pela `acervo-comunhao`.
3. Leia os candidatos com `get-article-content` até achar um aprovado: primeiro confirme que entra (seção 2), depois aplique a seção 6. Até 8 leituras; sem aprovado, passe ao próximo articulista da fila.

### Nota de escolha (0 a 5 cada, mínimo 14 de 20)

- **Atemporalidade:** o argumento vale hoje sem depender do fato da época.
- **Autonomia:** o texto se entende sozinho, sem nota de contexto ou com uma nota curta.
- **Qualidade do original:** texto completo, sem trechos quebrados pela digitalização.
- **Interesse:** tema procurado hoje ou com gancho de calendário próximo: Reforma (31/10), Ação de Graças (4ª quinta de novembro), Advento e Natal, Ano-Novo, Páscoa, Dia das Mães e dos Pais, Dia do Pastor (2º domingo de junho), Dia da Bíblia (2º domingo de dezembro), volta às aulas.

Contam também como gancho: o aniversário de morte do articulista (5, 10, 20 anos), o aniversário de nascimento e uma data citada no próprio texto (fundação de uma igreja, posse, centenário).

Empate: o gancho de calendário, depois o articulista de nível A, depois a década menos usada nos últimos 30 dias.

## 6. Rejeição

Rejeite e troque de texto quando:

### 6.1 O contexto compromete

O argumento central depende de um fato da época e, lido hoje, confunde ou engana o leitor. Exemplos:

- comenta como atual uma eleição, um governo, uma crise, um escândalo, a pandemia, uma Copa, um congresso ou um evento, e não se sustenta sem eles;
- anuncia ou recomenda algo que acabou (evento, campanha, programa da igreja, produto, lei em tramitação, instituição);
- a premissa foi desmentida pelos fatos ("o Brasil nunca vai…" e foi);
- precisaria de mais de dois itens na Nota de contexto para ser entendido, ou a nota contradiria o autor.

Contexto leve fica, com Nota de contexto: um ano citado, um fato antigo usado como exemplo, uma expressão de tempo ("este ano", "hoje") que se resolve com a data.

### 6.2 Os números comprometem

O raciocínio se apoia em dados específicos que envelheceram e mudam a conclusão: estatísticas (inclusive de religião e do Censo), preços, salários, câmbio, inflação, população, rankings, percentuais de conjuntura, contas com valores da época. Regra prática: **valor em reais usado como referência atual, ou mais de um número de conjuntura no argumento central, rejeita.** Um número histórico datado pelo próprio autor ("em 1998 eram…") que não sustenta a conclusão pode ficar.

### 6.3 Outros motivos

- Pautas proibidas (padrão, 2.1), política partidária ou eleitoral, texto que orienta voto ou trata de candidato, partido ou governo.
- Texto incompleto, ilegível ou com menos de 350 palavras.
- Tema de saúde (inclusive saúde mental) com orientação que hoje seria inadequada.
- Tema sensível que pede tratamento atual e revisão humana: abuso sexual, suicídio, aborto, violência contra a mulher, chacina, linchamento.
- Publieditorial, conteúdo de marca ou texto que promove empresa, produto, evento ou igreja específica.
- **Autoria em dúvida:** pesquise na web, entre aspas, uma ou duas frases características do texto. Se ele aparece antes, atribuído a outra pessoa, ou circula como texto sem autor, rejeite e marque "autoria a conferir".
- **Erro de fato do original:** confira uma vez as datas e os números históricos centrais do texto (nascimento, morte, posse de um personagem). Erro que não é de digitalização (ex.: "nasceu em 1927" para quem nasceu em 1870) rejeita: corrigir seria reescrever o autor.
- Já está no site há menos de 2 anos (seção 11).

Todo texto descartado vai para o resumo com o motivo: **não entra** (coluna, leitor, reportagem ou repercussão de factual), **contexto**, **dados** ou **outro**.

## 7. Conferências

### 7.1 O articulista está vivo?

- Confira na web no dia (WebSearch e WebFetch). Morte só com **duas fontes independentes** (cobertura da própria Comunhão no site vale como uma).
- **Falecido:** "In memoriam" no rodapé, antes do nome (seção 8), com o mês e o ano da morte.
- **Vivo:** minibio com o cargo e a função **atuais**, conferidos na fonte oficial (igreja, instituição, currículo). Não deu para confirmar o cargo atual: minibio só com o que não muda ("pastor e escritor", "foi pastor da Igreja X") e registro no resumo. **Não avise o articulista** antes de republicar.
- **Sem rastro recente** (nem obituário, nem atividade): minibio neutra, que vale nos dois casos: "[Nome] assinou artigos na revista Comunhão entre [ano] e [ano]." Registre "status não confirmado" no resumo.
- Pessoa citada no texto que mudou de cargo ou morreu: o texto do autor fica; a Nota de contexto avisa quando muda o sentido.

### 7.2 Texto

- **Não reescreva.** Mantenha palavras, ordem, citações e números do autor.
- Tire o cabeçalho da página (editoria, nome do autor solto, minibio da época, créditos de foto e olhos repetidos) e escreva a abertura e o rodapé desta skill.
- Pode: corrigir erro evidente de digitalização ("família toca" → "família toda", hifenização quebrada, linhas partidas), erro evidente de grafia ou concordância ("boas vindas" → "boas-vindas", nome oficial de cidade), padronizar aspas e paragrafação, transformar caixa alta em caixa normal. Registre cada correção no resumo.
- Link estranho no meio do texto (spam, como já apareceu em post antigo do site): retire e registre.
- Não pode: cortar trechos, atualizar dados, trocar termos, suavizar opinião. Se o texto precisa disso, rejeite (seção 6).
- **Bíblia:** confira toda citação no NEIA (`get-bible-passage`, nas três versões quando a numeração não bater). Escreva os livros por extenso, no padrão da casa: "(Romanos 5.5)", "(2 João 10-11)". Numeração diferente entre versões não é erro (2 Coríntios 13.13 na NTLH é o 13.14 na ACF): fica a do autor. Corrija só a referência com erro evidente e registre no resumo. A versão que o autor usou fica: o artigo é citação da pessoa (decisão de Mário Fernando, 2/11/2026). Já o que a redação escreve (nota de contexto, linha fina, legenda, texto do story) cita a Bíblia **sempre na NTLH**, conferida no NEIA com `bible_code` "NTLH".

## 8. Formato da matéria

- **Título:** o original, só com correção de caixa e digitação. O título SEO (até 60 caracteres) pode ser diferente.
- **Linha fina:** a original (na revista, a frase em destaque logo abaixo do título). Sem ela, uma frase de até 25 palavras com a ideia central do texto, sem inventar. Se o texto tem marca de tempo que só se entende com a data ("este ano", "atualmente"), a linha fina termina com o ano: "…, em artigo de 2009".
- **Chapéu:** o nome do articulista, em caixa alta e baixa, na grafia principal da seção 4 (sem Pr., Rev. ou outro título), ex.: "Hernandes Dias Lopes". Vale também para os textos da seção 2.2. "In memoriam" não entra no chapéu: fica no rodapé. "Artigo" não é mais chapéu (decisão do Mário Fernando, 13/11/2026).
- **Assinatura no NX Feed:** "Redação" (o articulista não tem credencial). O autor aparece no texto.
- **Abertura do texto:** `<p><strong>Por [Nome do articulista]</strong></p>`.
- **Intertítulos:** só os do original, em `<h4>`.
- **Links:** um interno, para matéria ou artigo recente do portal sobre o tema ou o autor; até dois externos, só na Nota de contexto.

### Bloco final, nesta ordem

1. **Nota de contexto** (quando o texto pede contexto ou cita dado que tem versão mais nova): uma a três frases, com fatos conferidos e fonte, sem opinar sobre o autor. Cada dado atualizado entra numa frase própria, com fonte e ano, e não conta no limite de três frases nem no de itens da seção 6.1. Quando o dado couber num modelo do NXtab, a peça vem logo depois da nota, na paleta da Comunhão (`marca` "com"; padrão, seção 12).
2. **Minibio:** vivo → `<strong>Nome</strong> é …` (cargo atual). Falecido → `<em>In memoriam</em> — <strong>Nome</strong> foi …, morreu em [mês] de [ano].`
3. **Origem:** revista → "Artigo publicado originalmente na edição nº [X] da Revista Comunhão, em [mês] de [ano]." Site → "Artigo publicado originalmente no portal comunhao.com.br em [dia] de [mês] de [ano]."
4. **Aviso:** "É uma republicação do acervo de artigos da Comunhão. As pessoas citadas podem não estar mais nos cargos e situações da época, e as opiniões e os fatos referem-se ao contexto de então."

Modelo HTML (articulista falecido):

```html
<p><strong>Por Fulano de Tal</strong></p>
<p>…texto do autor…</p>
<p><em><strong>Nota de contexto:</strong> o artigo foi escrito em 2009, quando…, segundo o <a href="https://…" target="_blank" rel="noopener">IBGE</a>.</em></p>
<p><em>In memoriam</em> — <strong>Fulano de Tal</strong> foi pastor da Igreja X e escritor; morreu em março de 2019.</p>
<p><em>Artigo publicado originalmente na edição nº 120 da Revista Comunhão, em maio de 2006.</em></p>
<p><em>É uma republicação do acervo de artigos da Comunhão. As pessoas citadas podem não estar mais nos cargos e situações da época, e as opiniões e os fatos referem-se ao contexto de então.</em></p>
```

Articulista vivo: a mesma estrutura, com a minibio no presente e sem "In memoriam".

### Categorias e tags (portal Comunhão = 4)

- Artigos (2) + uma subcategoria temática da tabela da skill `acervo-comunhao` (seção 7), pela leitura do texto.
- Nunca as categorias-mãe Vida e Família 13, Igreja e Missões 116618, Cotidiano 16425 e Plugue-se 6062, nem Destaques 44517, Panorama 1, Edição Digital 54, Eleições 2026 117421, Conteúdo de Marca 108675 ou Institucional 114186.
- Tags (5 a 10): sempre "Acervo de Artigos" e o nome do articulista, mais tema, instituição e denominação quando houver.

### SEO e imagem

- SEO pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo). O título fica o original; a palavra-chave e o título SEO trazem o termo mais buscado do tema. **O texto do autor nunca muda por causa de SEO:** quando o que falta para a nota 85 exige mexer nele (palavra-chave em intertítulo, por exemplo), publique com a nota que tiver e registre.
- Imagem destacada pelo padrão (seção 9), nesta ordem: personagem do título, quando o texto é sobre uma pessoa (retrato de acervo público com crédito) → **foto do articulista** (NX Fotos, que tem a pasta "Articulistas Comunhão"; imagem destacada de posts antigos dele ou sobre ele no site, que a NEIA traz em `featured_image`; `buscar_imagens`; foto oficial da igreja ou instituição com crédito) → foto real do tema → imagem por IA (nunca o rosto do autor nem símbolo de denominação específica). Foto antiga: "foto de arquivo" na descrição; falecido: "(1929-2016), foto de arquivo".

### Enquadramento da foto destacada (decisão do Mário Fernando, 13/11/2026)

O tema dos sites mostra a destacada recortada em caixas mais altas que 16:9: o destaque grande da categoria Artigos é 5:3, com o foco um pouco abaixo do meio, e há blocos de 70% e miniaturas quadradas. Retrato vertical, quadrado ou 3:2 com a cabeça no alto perde a cabeça do autor quando aparece grande (aconteceu com Hernandes Dias Lopes, Gilson Bifano e Sidemberg Rodrigues em novembro de 2026). Em 16:9 a imagem preenche essas caixas pela altura e o site só corta as laterais. Por isso, **toda destacada com pessoa vai em 16:9, com o rosto no centro e a cabeça inteira**:

1. Baixe a foto escolhida em resolução cheia (NX Fotos: `link_do_original`; nas outras, o link da foto). Se ela precisar de tratamento de cor (padrão, 9.3), trate antes de enquadrar.
2. Grave o script abaixo como `enquadrar_retrato.py` e rode `python3 enquadrar_retrato.py foto.jpg destacada.jpg --folha folha.jpg`. Ele acha o rosto e escolhe um de três caminhos: foto já larga, corta só as laterais com o rosto no centro; foto mais alta com folga acima da cabeça, corta em 16:9 com a cabeça inteira; senão, mantém a foto inteira no centro (a vertical fica da cabeça à cintura) e completa as laterais com o próprio fundo (fundo liso: a cor da borda; fundo com cena: a própria foto desfocada). Saída em JPEG 1600x900 (menor só quando a original é pequena).
3. Olhe a `folha.jpg` com Read: nos três cortes do site (5:3, 70% e quadrado), a cabeça aparece inteira e o rosto fica perto do centro. Emenda visível, faixa estranha ou objeto esticado na lateral: escolha outra foto do articulista e repita.
4. Suba com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `materia_id`) e `curl -T`, e grave a URL que o envio devolve com `definir_imagem_destacada` (`tratamento` "nao"), com título, fonte, autor, descrição e legenda de sempre. O link de envio é de uso único: não mostre nem guarde.
5. Sem OpenCV ou sem o modelo de rosto, o script segue sem rosto e mantém a foto inteira, o que também protege a cabeça. Se nem o script rodar, prefira uma foto horizontal com a cabeça longe do alto e registre "foto sem enquadramento" em Pendências.
6. Vale para toda foto de pessoa na destacada (articulista ou personagem do título). Foto de tema sem pessoa e imagem de IA (gerada em 16:9) não precisam.

```python
#!/usr/bin/env python3
"""Enquadra a foto do articulista para a imagem destacada (16:9), sem cortar a cabeça.

Por que existe: o tema dos sites (Newspaper/tagDiv) mostra a destacada como fundo
"cover" em caixas mais altas que 16:9 (destaque grande 5:3 com foco vertical em 60%,
blocos de 70%, miniaturas quadradas). Foto vertical, quadrada ou 3:2 com a cabeça no
alto perde o alto da cabeça. Em 16:9 a imagem preenche essas caixas pela altura: o
site só corta as laterais, nunca o alto.

O que faz:
  - acha o rosto (OpenCV Haar; baixa o modelo do GitHub se faltar);
  - foto já 16:9 ou mais larga: corta só as laterais, com o rosto no centro;
  - foto mais alta que 16:9 com folga acima da cabeça: corta em 16:9 com a cabeça
    inteira e margem no alto;
  - senão (vertical, quadrada, cabeça encostada no alto): mantém a foto inteira no
    centro e completa as laterais com o próprio fundo (fundo liso: cor da borda,
    linha a linha; fundo com cena: a própria foto ampliada e desfocada).
Saída em JPEG 1600x900 (menor só se a original for pequena; nunca abaixo de 1200x675).

Uso:
  python3 enquadrar_retrato.py entrada.jpg saida.jpg [--folha folha.jpg]
Imprime um JSON com o modo usado e as medidas; a --folha mostra como o site cortaria
a saída (5:3 foco 60%, 70% foco 60%, quadrado foco 20%) para conferir antes de subir.
"""
import json, os, sys, urllib.request
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw

HAAR_URL = ("https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/"
            "haarcascade_frontalface_default.xml")
HAAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos",
                    "haarcascade_frontalface_default.xml")
RATIO = 16 / 9

# Caixas do tema medidas na Comunhão em 13/11/2026 (fundo "cover"): altura/largura e foco vertical
CAIXAS = [("5:3 foco 60%", 0.60, 0.60), ("70% foco 60%", 0.70, 0.60), ("quadrado foco 20%", 1.00, 0.20)]

def corte(im, ratio_h, foco_y, foco_x=0.5, larg=420):
    w, h = im.size
    box_w, box_h = larg, int(larg * ratio_h)
    esc = max(box_w / w, box_h / h)
    nw, nh = int(w * esc + 0.5), int(h * esc + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ox = int((nw - box_w) * foco_x); oy = int((nh - box_h) * foco_y)
    return r.crop((ox, oy, ox + box_w, oy + box_h))

def folha(paths, saida):
    """Folha de conferência: original e os três cortes do site, uma linha por imagem."""
    linhas = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        orig = im.copy(); orig.thumbnail((300, 300))
        pecas = [orig] + [corte(im, rh, fy) for _, rh, fy in CAIXAS]
        lw = sum(x.size[0] for x in pecas) + 10 * (len(pecas) + 1)
        lh = max(x.size[1] for x in pecas) + 34
        lin = Image.new("RGB", (lw, lh), "white"); d = ImageDraw.Draw(lin)
        x = 10
        for i, pc in enumerate(pecas):
            lin.paste(pc, (x, 28))
            d.text((x, 8), ("original %dx%d" % im.size) if i == 0 else CAIXAS[i - 1][0], fill="black")
            x += pc.size[0] + 10
        d.text((lw - 200, 8), p.split("/")[-1][:30], fill="red")
        linhas.append(lin)
    W = max(l.size[0] for l in linhas); H = sum(l.size[1] for l in linhas)
    out = Image.new("RGB", (W, H), "white"); y = 0
    for l in linhas: out.paste(l, (0, y)); y += l.size[1]
    out.save(saida, quality=85)



def achar_rosto(im):
    try:
        import cv2
    except ImportError:
        return None
    if not os.path.exists(HAAR):
        os.makedirs(os.path.dirname(HAAR), exist_ok=True)
        try:
            urllib.request.urlretrieve(HAAR_URL, HAAR)
        except Exception:
            return None
    cas = cv2.CascadeClassifier(HAAR)
    if cas.empty():
        return None
    w, h = im.size
    g = cv2.cvtColor(np.array(im)[:, :, ::-1], cv2.COLOR_BGR2GRAY)
    g = cv2.equalizeHist(g)
    for viz in (6, 4):
        fs = cas.detectMultiScale(g, 1.08, viz, minSize=(int(min(w, h) * 0.07),) * 2)
        if len(fs):
            x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3])
            return int(x), int(y), int(fw), int(fh)
    return None


def _suave(v, jan):
    """Média móvel ao longo das linhas (v: linhas x 3)."""
    jan = max(3, int(jan) | 1)
    pad = np.pad(v, ((jan // 2, jan // 2), (0, 0)), mode="edge")
    k = np.ones(jan) / jan
    return np.stack([np.convolve(pad[:, c], k, mode="valid") for c in range(3)], axis=1)


def fundo_liso(arr):
    """Fundo de estúdio? As faixas laterais (3% de cada lado) têm de ser uniformes em
    cada linha e sem objeto no caminho (cadeira, mesa, planta): a cor de cada linha não
    pode fugir da média móvel vertical."""
    h, w, _ = arr.shape
    b = max(4, int(w * 0.03))
    pior = 0.0
    for faixa in (arr[:, :b].astype(float), arr[:, -b:].astype(float)):
        na_linha = faixa.std(axis=1).mean()
        medias = faixa.mean(axis=1)
        salto = np.abs(medias - _suave(medias, h * 0.15)).max()
        pior = max(pior, na_linha, salto * 0.8)
    return pior < 12, round(float(pior), 1)


def preencher(im, W, H, x0, y0, liso):
    """Põe im (já na escala) em (x0, y0) de uma tela WxH e completa o resto."""
    iw, ih = im.size
    arr = np.array(im)
    if liso:
        b = max(3, int(iw * 0.02))
        cor_e = _suave(arr[:, :b].astype(float).mean(axis=1), ih * 0.15)   # cor da borda,
        cor_d = _suave(arr[:, -b:].astype(float).mean(axis=1), ih * 0.15)  # linha a linha
        tela = np.zeros((H, W, 3), float)
        linhas = np.clip(np.arange(H) - y0, 0, ih - 1)
        ce, cd = cor_e[linhas], cor_d[linhas]
        meio = x0 + iw // 2
        tela[:, :meio] = ce[:, None, :]
        tela[:, meio:] = cd[:, None, :]
        fundo = Image.fromarray(np.clip(tela, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
        borda = max(16, int(iw * 0.06))
    else:
        esc = max(W / iw, H / ih)
        fundo = im.resize((int(iw * esc) + 1, int(ih * esc) + 1), Image.LANCZOS)
        fx, fy = (fundo.size[0] - W) // 2, (fundo.size[1] - H) // 2
        fundo = fundo.crop((fx, fy, fx + W, fy + H)).filter(ImageFilter.GaussianBlur(28))
        fundo = Image.eval(fundo, lambda v: int(v * 0.78))
        borda = max(10, int(iw * 0.025))
    # máscara com bordas suaves para não ficar emenda
    m = Image.new("L", (iw, ih), 255)
    d = ImageDraw.Draw(m)
    for i in range(borda):
        a = int(255 * (i + 1) / (borda + 1))
        if x0 > 0:
            d.line([(i, 0), (i, ih)], fill=a)
        if x0 + iw < W:
            d.line([(iw - 1 - i, 0), (iw - 1 - i, ih)], fill=a)
        if y0 > 0:
            d.line([(0, i), (iw, i)], fill=min(a, 255))
    fundo.paste(im, (x0, y0), m)
    return fundo


def tamanho_tela(lado_ref):
    """Altura da tela: até 900, nunca abaixo de 675 (largura 1200)."""
    H = int(min(900, max(675, lado_ref)))
    return int(round(H * RATIO)), H


def enquadrar(ent, sai):
    im = ImageOps.exif_transpose(Image.open(ent)).convert("RGB")
    w, h = im.size
    r = w / h
    rosto = achar_rosto(im)
    info = {"entrada": f"{w}x{h}", "proporcao": round(r, 2), "rosto": bool(rosto)}
    if rosto:
        x, y, fw, fh = rosto
        cx = x + fw / 2
        topo = max(0.0, y - 0.6 * fh)           # alto do cabelo, com folga
        queixo = y + fh
    else:
        cx, topo, queixo, fh = w / 2, 0.0, h * 0.5, h * 0.25

    if r >= RATIO - 0.01:                        # já horizontal o bastante
        W, H = tamanho_tela(h)
        esc = H / h
        r_im = im.resize((int(w * esc + 0.5), H), Image.LANCZOS)
        cxs = cx * esc
        x0 = int(min(max(cxs - W / 2, 0), r_im.size[0] - W))
        out = r_im.crop((x0, 0, x0 + W, H))
        info["modo"] = "corte lateral"
    else:
        ch = w / RATIO                           # janela 16:9 na largura toda
        y_top = min(max(topo - 0.10 * ch, 0), h - ch)
        folga = topo - y_top
        cabe = (rosto is not None and folga >= 0.06 * ch
                and y_top + ch >= queixo + 0.6 * fh and ch >= 0.62 * h and w >= 1200)
        if cabe:
            W, H = tamanho_tela(ch)
            out = im.crop((0, int(y_top), w, int(y_top + ch))).resize((W, H), Image.LANCZOS)
            info["modo"] = "corte 16:9 com a cabeça inteira"
        else:
            if h > w:                            # vertical: fica da cabeça à cintura
                y_c = int(min(max(topo - 0.08 * w, 0), h - w))
                im = im.crop((0, y_c, w, y_c + w))
                topo -= y_c
                h = w
                info["recorte_vertical"] = f"{w}x{w} a partir de y={y_c}"
            liso, desvio = fundo_liso(np.array(im))
            W, H = tamanho_tela(h)
            margem = 0                           # sem faixa no alto: o site não corta o alto do 16:9
            ih = H - margem
            esc = ih / h
            iw = int(w * esc + 0.5)
            if iw > W:                           # não deveria acontecer (r < 16:9)
                iw, ih = W, int(h * W / w)
            r_im = im.resize((iw, ih), Image.LANCZOS)
            x0 = int(min(max(W / 2 - cx * esc, 0), W - iw))
            out = preencher(r_im, W, H, x0, margem, liso)
            info["modo"] = "foto inteira no centro, laterais completadas"
            info["fundo"] = "liso (cor da borda)" if liso else "cena (foto desfocada)"
            info["desvio_borda"] = desvio
    out.save(sai, "JPEG", quality=92, optimize=True, progressive=True)
    info["saida"] = f"{out.size[0]}x{out.size[1]}"
    return info


if __name__ == "__main__":
    args = sys.argv[1:]
    folha_saida = None
    if "--folha" in args:
        i = args.index("--folha"); folha_saida = args[i + 1]; del args[i:i + 2]
    res = enquadrar(args[0], args[1])
    if folha_saida:
        globals()["folha"]([args[1]], folha_saida)
        res["folha"] = folha_saida
    print(json.dumps(res, ensure_ascii=False))
```

## 9. Publicação às 8h

1. Refaça a duplicidade (seção 11).
2. `criar_materia` → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar → enquadramento da foto (seção 8, "Enquadramento da foto destacada") → `definir_imagem_destacada` com a foto enquadrada.
3. `conferir_publicacao` (tipo agendar) → `publicar_no_wordpress` com `portais` ["4"], `quando` "DD/MM/AAAA 08:00" (hoje) e o `codigo_confirmacao` (decisão de publicação direta, padrão seção 2). Se a matéria só ficar pronta depois das 7h55, agende para o próximo horário de 15 em 15 minutos (8h15, 8h30…), sempre com pelo menos 5 minutos de folga: a folga é o tempo de barrar o story automático (seção 10.1). Erro 429: espere e repita.
4. Guarde o `materia_id` e o horário agendado.
5. Faça a seção 10.1 logo em seguida.
6. Espere até 2 minutos depois do horário agendado (`sleep` no Bash, em blocos de no máximo 9 minutos). Confirme que a matéria está no ar: `listar_publicacoes` com `portal` "4", `situacao` "publicado" e `busca` pelo título, e o link com o slug (não `?p=`). Guarde o link.
7. Se 10 minutos depois do horário ela ainda não estiver no ar, não faça o story: registre em Pendências com o que `listar_agendamentos` mostra.

## 10. Story para revisão (decisão de 02/11/2026)

O story precisa da revisão da Joviana e do Mário. **A rotina nunca aprova, agenda ou publica story:** não use `revisar_post_instagram` para aprovar nem `publicar_post_instagram`. Conta da marca: **Comunhão = conta 6** (@oficialcomunhao). Não faça story de texto sobre tragédia, violência ou eleição (regra do Instagram da Comunhão).

### 10.1 Barrar o story automático (antes de a matéria ir ao ar)

Quando a matéria é agendada, o painel do NX Feed cria sozinho um story dela e o agenda para o horário da matéria. Ele sairia sem revisão.

1. Logo depois de agendar, `listar_posts_instagram` com `conta_id` 6, `tipo` "story", `filtro` "agendados", e depois `filtro` "aprovados". Fique só com os itens cujo `materia_id` é o da matéria do dia. O painel pode levar alguns minutos para criar o story: se não achar nada, espere 2 minutos e procure de novo, até 3 vezes.
2. Story automático agendado: `cancelar_agendamento_instagram` com o `post_id`. A rotina só pode cancelar o story automático **da matéria dela**; nunca mexa em outro conteúdo.
3. Story automático já publicado: não dá para desfazer. Registre em Pendências ("story automático saiu sem revisão") e não faça outro story.
4. Guarde o `post_id` do automático para a seção 10.2.

### 10.2 Montar o story e mandar para revisão (depois de a matéria ir ao ar)

Só depois da confirmação da seção 9 (padrão, seção 2.2). Siga o guia de arte da casa (`regras_de_arte` com a conta 6). Procure de novo o story automático, como em 10.1, e cancele o agendamento se ele tiver voltado a ter horário.

1. `criar_arte_de_noticia`, com `so_conferir` true antes, se precisar acertar as linhas:
   - **Com story automático** (cancelado ou parado em revisão): `post_id` do automático. A arte vira a versão seguinte dele e o conteúdo volta para "Para revisar". Assim fica um story só para a matéria.
   - **Sem story automático:** `materia_id`, `conta_id` 6, `formatos` ["story"], `criar_post` true e `etapa` "revisao".
   - **Título** (2 linhas, ~38 a 45 caracteres): o título do texto, reduzido sem mudar o sentido. Título em metáfora ("Quando os lobos atacam as ovelhas") vira o tema dito com clareza ("Os três perigos dos falsos mestres na igreja"), como pede o guia de arte.
   - **Subtítulo** (2 linhas, ~80 a 105 caracteres, termina com ponto): "Artigo de [Nome], publicado em [ano] na revista Comunhão." Falecido: "Artigo de [Nome] (in memoriam), publicado em [ano]…" quando couber.
   - **Tag:** a subcategoria temática do texto, como tag provisória, conforme o guia. O tema de cor (azul ou laranja) o NX Feed escolhe pela seção da matéria.
   - **Foto:** a destacada (em 16:9, com o rosto no centro, o recorte vertical do story pega a pessoa). O guia proíbe imagem de IA na arte: se a destacada for IA, use outra foto real do tema; sem foto real, não faça o story e registre.
   - **Nota:** "Story do acervo de artigos para revisão da Joviana e do Mário Fernando. A matéria está no ar desde [DD/MM às HHh]. Ao aprovar, escolham o horário."
   - **Pedido:** "Story do artigo do acervo da Comunhão, para revisão da Joviana e do Mário (rotina artigos-acervo-comunhao)."
2. Confira com `ver_post_instagram` que o story está em revisão ("Para revisar"). O NX Feed avisa os revisores do Studio.
3. Se o `post_id` do automático recusar o ajuste, volte o automático para rascunho (`revisar_post_instagram` com `acao` "voltar_rascunho" e `nota` "Substituído pelo story do acervo de artigos, em revisão") e crie o story novo sem `post_id`.
4. Falha no story não desfaz a publicação: registre em Pendências.

## 11. Duplicidade e controle

A rotina se reconhece por três marcas: tag "Acervo de Artigos", chapéu com o nome do articulista (até 13/11/2026 era "ARTIGO") e a frase "É uma republicação do acervo de artigos da Comunhão" no pé. A rotina `acervo-comunhao` usa outras: tag "Acervo Comunhão" e a frase "É uma republicação do acervo Comunhão."

Antes de escrever e de novo antes de agendar:

1. **O que esta rotina já fez:** `listar_materias` com `busca` "Acervo de Artigos" e com `autor` "Redação", `portal` 4, últimos 365 dias, formato compacto; confirme com `ver_materia`. Daí saem os textos já usados e a data do último uso de cada articulista. O mesmo texto original nunca é republicado duas vezes.
2. **O que a `acervo-comunhao` fez:** `listar_materias` com `busca` pelo título original, todos os estados, últimos 365 dias, formato compacto; rascunhos sem filtro de portal. Texto já adaptado por ela não entra aqui.
3. **Site, na NEIA:** `search-content` na fonte do site pelo título original e pelo tema com o nome do autor.
4. **Site, na web:** WebSearch `site:comunhao.com.br "<título>"`.

Como decidir:

- O mesmo texto está no site há **menos de 2 anos**: troque de texto.
- Está no site há **mais de 2 anos**: siga com a republicação e liste o post antigo no resumo, em "Para tirar do ar" (link, id do post e link da versão nova). Nada é apagado por esta rotina.
- Rascunho ou matéria agendada da equipe (ou da `acervo-comunhao`) com o mesmo texto: troque de texto.

## 12. Resumo e notificação

**Não envie e-mail.** Siga o padrão (seção 10), com o título "Artigos do acervo · Comunhão · DD/MM" e estas seções:

- **Publicado:** título com link, articulista (vivo ou in memoriam), caminho (editoria Artigos ou seção 2.2, com o cabeçalho original), origem (edição ou post e data original, "data deduzida" quando for), categoria, nota de escolha, nota SEO, imagem (real, arquivo ou IA, e o modo do enquadramento), se teve Nota de contexto, dados atualizados (antigo → atual, fonte e ano) e peça do NXtab.
- **Story para revisão (Joviana e Mário):** link do Studio, `post_id` e situação ("em revisão"); story automático cancelado ou não encontrado.
- **Rejeitados no dia:** título, articulista, edição e motivo (não entra, contexto, dados ou outro), uma linha cada.
- **Para tirar do ar:** versões antigas no site, quando houver.
- **Imagens de IA para validar**, quando houver.
- **Pendências:** cargo não confirmado, data deduzida, grafia em dúvida, referência bíblica corrigida, articulista novo para a lista, story que falhou ou saiu sem revisão, foto sem enquadramento.

Notificação do app Claude ao terminar.