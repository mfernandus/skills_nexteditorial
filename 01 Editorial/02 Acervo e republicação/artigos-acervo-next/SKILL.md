---
name: "artigos-acervo-next"
description: "Rotina diária das 8h que republica um artigo assinado da editoria Artigos (revistas e sites) da ES Brasil e da Comunhão, com in memoriam, data original, nota de contexto, regras de rejeição e story automático. Não vale para colunas."
---

# Artigos do acervo — ES Brasil e Comunhão (8h)

Objetivo: todo dia às 8h, um artigo assinado por um dos articulistas mais importantes da casa, publicado originalmente na **editoria Artigos**, volta ao ar **em cada portal** (um na **ES Brasil**, um na Comunhão), com o texto do autor preservado, a data da publicação original no rodapé, "in memoriam" quando o autor já morreu, nota de contexto quando o texto pede e um story no Instagram da marca.

**Esta skill vale só para artigo assinado da editoria Artigos. Coluna não entra** (seção 1.1).

Responda sempre em português do Brasil. Execução agendada: não faça perguntas. Na dúvida, tome a decisão mais conservadora (trocar de artigo) e registre no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns: publicação direta (2), pautas proibidas (2.1, vale acima de tudo), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), SEO (8), imagem destacada (9) e avisos (10). Onde as duas divergirem, vale esta skill nestes pontos (pedido do Mário Fernando, 30/10/2026):

- **O texto do articulista não se reescreve** e nenhum número dele é atualizado: artigo assinado é opinião do autor. O que mudou desde então vai na Nota de contexto; se a mudança compromete o artigo, ele é rejeitado (seção 4).
- **Título original mantido** (seção 6).
- **Rodapé próprio** (in memoriam, minibio, origem e aviso de republicação) no lugar do "Com informações de".
- **Story publicado direto**, sem fila de aprovação (seção 8).

## 1. Fontes no NEIA

### 1.1 O que conta como artigo (decisão do Mário Fernando, 30/10/2026)

Só entra texto **assinado** que saiu na **editoria Artigos**. O resto não é artigo para esta rotina, mesmo assinado.

- **Revista:** o texto completo (`get-article-content`) começa com o cabeçalho da editoria antes do título. Contam: "ARTIGO", "Artigo", "ARTIGOS", "ARTIGO ESPECIAL", "Artigo | Cotidiano", "Artigo / Tecnologia", "ARTIGO / ESBRASIL" (nas edições recentes da **ES Brasil**; a digitalização grafa "ESPRASIL" ou "ESPERASIL") e erros evidentes de digitalização da palavra ("ÁRTICO", "ANTIQUO"). Exemplos: "ARTIGO / Hernandes Dias Lopes / QUANDO OS LOBOS…"; "Artigo / Cotidiano / por Eustáquio Palhares / Xô carro!".
- **Não entra:** cabeçalho de coluna (O Endereço da História, Modus Vivendi, Fim de Papo, Palavra de Pastor, Estudo Bíblico, Som & Cia, Mindset, Essas Mulheres, Zoom Marketing, Família S/A, Tira-Gosto, Pratos do Dia, Periscópio, Gente, O editor recomenda, Panorâmicas) ou de outra editoria, mesmo com texto de opinião assinado (ECONOMIA, GESTÃO, POLÍTICA, SEGURANÇA, TECNOLOGIA, INOVAÇÃO, AGRONEGÓCIO, OPINIÃO, ATUALIDADE, FAMÍLIA, CULTURA, VIDA CRISTÃ). Também ficam fora: "ARTIGO DO LEITOR" (não é articulista da casa), textos assinados da edição de Retrospectiva sem cabeçalho de Artigo, editorial, entrevista, reportagem e página sem cabeçalho legível.
- **Site:** só post da categoria **Artigos** (`wp_categories`). Post em qualquer outra categoria não entra.
- O tipo (`content_type` "article" ou "column") e a seção que a NEIA atribui são só pista: erram para os dois lados (na conferência de 30/10, um em cada quatro). Vale o cabeçalho da página (revista) e a categoria (site).

### 1.2 Onde buscar

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch. Uma chamada de cada vez; "Não foi possível conectar": repita a mesma chamada.

| Fonte | Id | O que tem |
|---|---|---|
| REVISTA COMUNHÃO | 019ca1b0-1295-72f0-baaf-31867a70431e | Edição 1 (mar/1997) à 325 (dez/2025) |
| REVISTA ESBRASIL | 019d1cf8-4fc8-72e4-ab29-5ef31d204e4d | Edição 1 (abr/2005) à 229 |
| COMUNHAO.COM.BR | 019ca1ae-c3a6-718c-b1f2-e577c04f3ed8 | Posts do site, categoria Artigos |
| ESBRASIL.COM.BR | 019d2231-a834-71ec-af78-1ad6fa55f69a | Posts do site, categoria Artigos |

- **Revista:** `search-content` com `source`, `author` = nome do articulista, `query` "artigo", `page_size` 200. O filtro de autor funciona na revista. Teste as grafias da seção 2 (com e sem "Pr.", "Rev.", "Pastor"; erros de digitalização).
- **Site:** o campo `author` é quem postou no WordPress (Erik Oakes, Nathanael Rodor, Mario Fernando Souza...), **não** o articulista; o filtro de autor não acha o articulista. Busque por tema na fonte do site e leia com `get-article-content`: o articulista está em "**Por Fulano**" no começo, na minibio do fim ("**Fulano** é...") e em `metadata.llm_author`. Só entram posts da categoria Artigos (`wp_categories`).
- No site, o nome do articulista costuma estar também nas tags do post (`wp_tags`), o que ajuda a achar os textos dele. O `published_at` de um post que já é republicação é a data nova; a original só aparece no texto ("Este artigo foi publicado originalmente em…").
- `get-article-content` traz o texto completo; no site, também `wp_post_id`, `wp_url`, `published_at` e `featured_image`.
- **Prefira a revista.** O post do site entra quando o artigo só existe lá.
- **Corte de tempo:** publicação original com pelo menos 12 meses no dia da execução.

### 1.3 Datas: conferir antes de usar

- `list-editions` (project_id = id da revista) dá a data de cada edição. Na revista, use **só mês e ano**.
- **ES Brasil:** as edições 185 a 229 vêm com 01/01/2000 (data vazia) e a 195 vem com nov/2020, fora da sequência. Deduza pela sequência das vizinhas (184 = dez/2020; 196 = dez/2021; 223 = jun/2024; 225B = dez/2024; 228B = ago/2025) e por marcas do texto. **Comunhão:** algumas edições (ex.: 17 a 32) vêm com a data de ingestão de 2026; deduza do mesmo jeito. Registre "data deduzida" no resumo.
- O mesmo artigo pode estar em mais de uma edição ou na revista e no site. O original é o **mais antigo**. Post do site que já é republicação traz "Este artigo foi publicado originalmente em…": use a data citada, conferida na revista quando possível.

## 2. Articulistas

Ordem de prioridade, por portal. Grafias que a NEIA usa entre parênteses. Status conferido em 30/10/2026; reconfira a cada uso (seção 5.1).

### Comunhão

**Nível A**
- Hernandes Dias Lopes (Rev. Hernandes Dias Lopes; digitalização: Hemandes, Hornandes). Vivo; pastor titular da Primeira Igreja Presbiteriana de Vitória. As colunas Palavra de Pastor e Estudo Bíblico dele não entram.
- Atilano Muradas (Atiliano Muradas, Pr. Atilano Muradas). Vivo.
- Gilson Bifano (Pr. Gilson Bifano). Vivo.
- Josué Campanhã (Pr. Josué Campanhã; a busca não acha "Campanha" sem til). Vivo. A coluna Palavra de Pastor não entra.
- José Ernesto Conti. Vivo. A coluna Fim de Papo não entra.
- Dinart Barradas (Pr. Dinart Barradas, Dinart e Norma Barradas; digitalização: DINARTI GARGADAS). Status não confirmado. A coluna de áudio Som & Cia não entra.
- João Carlos Marins. Status não confirmado.
- Russell Shedd (Russell P. Shedd). **In memoriam**: morreu em 26/11/2016, em São Paulo.

**Nível B:** Marcelo Aguiar · Lourenço Stelio Rega (no site há textos dele cedidos pela Cristianismo Hoje: fora) · Jr. Vargas (Rev. Haveraldo Ferreira Vargas Jr.; não confundir com o pai, Presb. Haveraldo Ferreira Vargas, que morreu em 2025) · Erni Walter Seibert · Erasmo Vieira · Jorge Linhares · Romney Cruz · Joarês Mendes de Freitas · Ivonildo Teixeira · Nelson Bomilcar · Simonton Araújo · Waldemar Rocha Junior · Devi Titus · Ariovaldo Ramos · Valdir Steuernagel · Jilton Moraes.

**Só coluna, fora:** Idálio Gomes da Silva (Administração) · Jesus Gonçalves (Pregador/Púlpito) · Evaldo Carlos e Gedimar de Araújo (Palavra de Pastor).

### ES Brasil

**Nível A:** Eustáquio Palhares · Lucas Izoton · Luiz Fernando Schettino · Orlando Caliman · Arilda Teixeira · José Antonio Bof Buffon · Sidemberg Rodrigues · Ronald Carvalho (só os da editoria Artigo; Zoom Marketing é coluna).

**Nível B:** Gilberto Sudré · Luciano Raizer · Ralph Chelotti (Ralph Chellotti) · Usiel Carneiro · Pablo Lira · Enio Bergoli (Énio Bergoli) · Robson Melo · Manoel Goes Neto · Adilson Neves · André Gomyde · João Luiz Vassalo Reis · Luiz Fernando Leitão (só os da editoria Artigo; Tira-Gosto é coluna).

**Fora da editoria Artigos na conferência de 30/10/2026:** Ivo Nogueira Dias (Modus Vivendi) · José Eugênio Vieira (O Endereço da História) · Andrea Monteiro, Fabricia Kirmse e Natache Barros (Essas Mulheres) · Leonardo Carraretto (Mindset) · Adriano Salvi (Família S/A) · Arlindo Villaschi, Diógenes Lucca, André Pereira César, Rodrigo Augusto Prando e Eduardo Araújo (chapéu de editoria, como ECONOMIA ou POLÍTICA). A rotina não os procura; se um texto deles com cabeçalho "Artigo" aparecer numa busca, ele entra pela regra 1.1.

**Políticos, fora:** Paulo Hartung, Renato Casagrande, Max Filho.

A lista completa, com contagem por articulista, edições, status e fontes, está na planilha "Lista de artigos do acervo — ES Brasil e Comunhão" (30/10/2026).

### Rotação

- Um artigo por portal por dia. Nível A em 4 a 5 dias da semana; nível B completa a semana.
- O mesmo articulista não repete no mesmo portal em menos de 5 dias.
- Dentro do articulista, comece pelos artigos mais antigos ainda não usados, salvo gancho de calendário.
- Articulista novo achado na base (assina 3 ou mais textos da editoria Artigos) pode entrar no nível B; registre no resumo para o Mário incluir na lista.

### Fora da lista, sempre

- Político com mandato, candidato ou pré-candidato (ex.: Paulo Hartung, Renato Casagrande) e artigo de autoridade sobre o próprio governo.
- Texto de terceiros reproduzido pela revista ou pelo site: crônica de outro veículo (ex.: Martha Medeiros), capítulo de livro, artigo traduzido de autor estrangeiro, texto cedido pela Cristianismo Hoje, poema ou letra de outro autor, coletânea de frases ou "lições" alheias, release.
- Autor que pediu para não ser republicado (lista de exclusão do Mário; vazia em 30/10/2026).

## 3. Escolha do artigo do dia

1. Veja o que a rotina já publicou (seção 9) e escolha o articulista do dia pela rotação.
2. Liste os artigos dele (seção 1) e descarte os já usados.
3. Leia os candidatos com `get-article-content` até achar um aprovado: primeiro confirme que é artigo (seção 1.1), depois aplique a seção 4. Até 8 leituras por portal; sem aprovado, passe ao próximo articulista da fila.

### Nota de escolha (0 a 5 cada, mínimo 14 de 20)

- **Atemporalidade:** o argumento vale hoje sem depender do fato da época.
- **Autonomia:** o texto se entende sozinho, sem nota de contexto ou com uma nota curta.
- **Qualidade do original:** texto completo, sem trechos quebrados pela digitalização.
- **Interesse:** tema procurado hoje ou com gancho de calendário próximo. Comunhão: Reforma (31/10), Ação de Graças (4ª quinta de novembro), Advento e Natal, Ano-Novo, Páscoa, Dia das Mães e dos Pais, Dia do Pastor (2º domingo de junho), Dia da Bíblia (2º domingo de dezembro), volta às aulas. **ES Brasil:** aniversário de Vitória (8/9), Dia do Espírito Santo (23/5), Dia da Indústria (25/5), Dia do Economista (13/8), Dia do Comerciante (16/7), Dia do Agricultor (28/7), Dia do Trabalho (1/5), virada do ano e planejamento.

Contam também como gancho: o aniversário de morte do articulista (5, 10, 20 anos), o aniversário de nascimento e uma data citada no próprio texto (criação de um município, posse, fundação).

Empate: o gancho de calendário, depois o articulista de nível A, depois a década menos usada nos últimos 30 dias.

## 4. Rejeição

Rejeite e troque de artigo quando:

### 4.1 O contexto compromete

O argumento central depende de um fato da época e, lido hoje, confunde ou engana o leitor. Exemplos:

- comenta como atual uma eleição, um governo, uma crise, uma CPI, um escândalo, a pandemia, uma Copa ou um evento, e não se sustenta sem eles;
- anuncia ou recomenda algo que acabou (evento, campanha, programa da igreja, produto, lei em tramitação, instituição);
- a premissa foi desmentida pelos fatos ("o Brasil nunca vai…" e foi);
- precisaria de mais de dois itens na Nota de contexto para ser entendido, ou a nota contradiria o autor.

Contexto leve fica, com Nota de contexto: um ano citado, um fato antigo usado como exemplo, uma expressão de tempo ("este ano", "hoje") que se resolve com a data.

### 4.2 Os números comprometem

O raciocínio se apoia em dados específicos que envelheceram e mudam a conclusão: estatísticas, preços, salários, câmbio, juros, inflação, PIB, população, rankings, percentuais de conjuntura, contas com valores da época. Regra prática: **valor em reais usado como referência atual, ou mais de um número de conjuntura no argumento central, rejeita.** Um número histórico datado pelo próprio autor ("em 1998 eram…") que não sustenta a conclusão pode ficar.

### 4.3 Outros motivos

- Pautas proibidas (padrão, 2.1), política partidária ou eleitoral.
- Texto incompleto, ilegível ou com menos de 350 palavras.
- Tema de saúde (inclusive saúde mental) com orientação que hoje seria inadequada.
- Tema sensível que pede tratamento atual e revisão humana: abuso sexual, suicídio, aborto, violência contra a mulher, chacina, linchamento. Fica fora da rotina automática.
- Publieditorial, conteúdo de marca ou artigo que promove empresa, produto ou evento.
- Artigo técnico de equipamento ou tecnologia superada.
- **Autoria em dúvida:** pesquise na web, entre aspas, uma ou duas frases características do texto. Se ele aparece antes, atribuído a outra pessoa, ou circula como texto sem autor, rejeite e marque "autoria a conferir".
- **Erro de fato do original:** confira uma vez as datas e os números históricos centrais do texto (nascimento, morte, posse de um personagem). Erro que não é de digitalização (ex.: "nasceu em 1927" para quem nasceu em 1870) rejeita: corrigir seria reescrever o autor.
- Já está no site há menos de 2 anos (seção 9).

Todo texto descartado vai para o resumo com o motivo: **não é artigo** (coluna ou outra editoria), **contexto**, **dados** ou **outro**.

## 5. Conferências

### 5.1 O articulista está vivo?

- Confira na web no dia (WebSearch e WebFetch). Morte só com **duas fontes independentes** (cobertura da própria Comunhão ou ES Brasil no site vale como uma).
- **Falecido:** "In memoriam" no rodapé, antes do nome (seção 6), com o mês e o ano da morte.
- **Vivo:** minibio com o cargo e a função **atuais**, conferidos na fonte oficial (igreja, instituição, empresa, currículo). Não deu para confirmar o cargo atual: minibio só com o que não muda ("pastor e escritor", "economista", "foi diretor do Sebrae/ES") e registro no resumo.
- **Sem rastro recente** (nem obituário, nem atividade): minibio neutra, que vale nos dois casos: "[Nome] assinou artigos na revista [ES Brasil] entre [ano] e [ano]." Registre "status não confirmado" no resumo.
- Pessoa citada no texto que mudou de cargo ou morreu: o texto do autor fica; a Nota de contexto avisa quando muda o sentido.

### 5.2 Texto

- **Não reescreva.** Mantenha palavras, ordem, citações e números do autor.
- Tire o cabeçalho da página (editoria, nome do autor solto, minibio da época, créditos de foto e olhos repetidos) e escreva a abertura e o rodapé desta skill.
- Pode: corrigir erro evidente de digitalização ("família toca" → "família toda", "capivaba" → "capixaba", hifenização quebrada, linhas partidas), erro evidente de grafia ou concordância ("a sociedade conspiram" → "conspira", "boas vindas" → "boas-vindas", nome oficial de cidade), padronizar aspas e paragrafação, transformar caixa alta em caixa normal. Registre cada correção no resumo.
- Link estranho no meio do texto (spam, como já apareceu em post antigo do site): retire e registre.
- Não pode: cortar trechos, atualizar dados, trocar termos, suavizar opinião. Se o artigo precisa disso, rejeite (seção 4).
- **Bíblia:** confira toda citação no NEIA (`get-bible-passage`, nas três versões quando a numeração não bater). Escreva os livros por extenso, no padrão da casa: "(Romanos 5.5)", "(2 João 10-11)". Numeração diferente entre versões não é erro (2 Coríntios 13.13 na NTLH é o 13.14 na ACF): fica a do autor. Corrija só a referência com erro evidente e registre no resumo. A versão que o autor usou fica.

## 6. Formato da matéria

- **Título:** o original, só com correção de caixa e digitação. O título SEO (até 60 caracteres) pode ser diferente.
- **Linha fina:** a original (na revista, a frase em destaque logo abaixo do título). Sem ela, uma frase de até 25 palavras com a ideia central do artigo, sem inventar. Se o texto tem marca de tempo que só se entende com a data ("este ano", "atualmente"), a linha fina termina com o ano: "…, em artigo de 2009".
- **Chapéu:** o nome do articulista, em caixa alta e baixa, na grafia principal da seção 2 (sem Pr., Rev. ou outro título), ex.: "Hernandes Dias Lopes", "Eustáquio Palhares". "In memoriam" não entra no chapéu: fica no rodapé. "Artigo" não é mais chapéu (decisão do Mário Fernando, 13/11/2026).
- **Assinatura no NX Feed:** "Redação" (o articulista não tem credencial). O autor aparece no texto.
- **Abertura do texto:** `<p><strong>Por [Nome do articulista]</strong></p>`.
- **Intertítulos:** só os do original, em `<h4>`.
- **Links:** um interno, para matéria ou artigo recente do portal sobre o tema ou o autor; até dois externos, só na Nota de contexto.

### Bloco final, nesta ordem

1. **Nota de contexto** (só quando precisa): uma a três frases, com fatos conferidos e fonte, sem opinar sobre o autor.
2. **Minibio:** vivo → `<strong>Nome</strong> é …` (cargo atual). Falecido → `<em>In memoriam</em> — <strong>Nome</strong> foi …, morreu em [mês] de [ano].`
3. **Origem:** revista → "Artigo publicado originalmente na edição nº [X] da Revista [Comunhão | ES Brasil], em [mês] de [ano]." Site → "Artigo publicado originalmente no portal [comunhao.com.br | esbrasil.com.br] em [dia] de [mês] de [ano]."
4. **Aviso:** "É uma republicação do acervo de artigos da [Comunhão | ES Brasil]. As pessoas citadas podem não estar mais nos cargos e situações da época, e as opiniões e os fatos referem-se ao contexto de então."

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

### Categorias e tags

- **Comunhão (portal 4):** só Artigos (2).
- **ES Brasil (portal 1):** só Artigos (11960).
- Nunca uma segunda categoria temática: com ela, o site mostrava o artigo na editoria do tema (decisão do Mário Fernando, 16/11/2026). O tema vai nas tags.
- Nunca Destaques, Edição Digital, Conteúdo de Marca, Institucional ou Eleições.
- Tags (5 a 10): sempre "Acervo de Artigos" e o nome do articulista, mais tema, instituição e denominação quando houver.

### SEO e imagem

- SEO pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo). O título fica o original; a palavra-chave e o título SEO trazem o termo mais buscado do tema. **O texto do autor nunca muda por causa de SEO:** quando o que falta para a nota 85 exige mexer nele (palavra-chave em intertítulo, por exemplo), publique com a nota que tiver e registre.
- Imagem destacada pelo padrão (seção 9), nesta ordem: personagem do título, quando o artigo é sobre uma pessoa (retrato de acervo público com crédito) → **foto do articulista** (NX Fotos, que tem a pasta "Articulistas Comunhão"; imagem destacada de posts antigos dele ou sobre ele no site, que a NEIA traz em `featured_image`; `buscar_imagens`; foto oficial da igreja ou instituição com crédito) → foto real do tema → imagem por IA (nunca o rosto do autor). Foto antiga: "foto de arquivo" na descrição; falecido: "(1929-2016), foto de arquivo".
- **Padrão da foto (decisão do Mário Fernando, 16/11/2026):** toda destacada com pessoa sai no padrão de artigos das rotinas `artigos-acervo-esbrasil` e `artigos-acervo-comunhao` (seção 8, "Foto destacada: padrão de artigos", com o script `padronizar_retrato.py`): pessoa recortada sobre foto do tema bem desfocada (o fundo é sempre trocado), 1600x900, cabeça do alto do cabelo ao queixo com metade da altura, alto do cabelo a 7% do topo e rosto no centro. A foto é a mais recente do articulista (acervo WordPress das revistas e NX Fotos, pela data) e passa pelo tratamento adaptativo do script, medido no rosto (foto escura clareia, pele avermelhada ou alaranjada volta ao tom natural; nunca o tratamento quente das matérias). Foto nova do acervo WordPress vai, tratada, para a pasta "Articulistas" do NX Fotos.

## 7. Publicação às 8h

1. Refaça a duplicidade (seção 9).
2. `criar_materia` → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar → `definir_imagem_destacada`.
3. `conferir_publicacao` (tipo publicar) → `publicar_no_wordpress` com `quando` "agora" e o `codigo_confirmacao` (decisão de publicação direta, padrão seção 2). **ES Brasil primeiro, depois Comunhão.** Uma chamada de cada vez; erro 429: espere e repita.
4. Guarde o link publicado e o `materia_id` para o story.

## 8. Story automático

Feito logo depois de cada publicação, na conta da marca: **ES Brasil = conta 7** (@revistaesbrasil), **Comunhão = conta 6** (@oficialcomunhao). Siga o guia de arte da casa (`regras_de_arte` com a conta), com estas regras desta rotina:

1. `criar_arte_de_noticia` com `materia_id`, `conta_id`, `formatos` ["story"] e `criar_post` false. Use `so_conferir` true antes, se precisar acertar as linhas.
   - **Título** (2 linhas, ~38 a 45 caracteres): o título do artigo, reduzido sem mudar o sentido. Título original em metáfora ("Quando os lobos atacam as ovelhas") vira o tema dito com clareza ("Os três perigos dos falsos mestres na igreja"), como pede o guia de arte.
   - **Subtítulo** (2 linhas, ~80 a 105 caracteres, termina com ponto): "Artigo de [Nome], publicado em [ano] na revista [Comunhão | ES Brasil]." Falecido: "Artigo de [Nome] (in memoriam), publicado em [ano]…" quando couber.
   - **Tag:** ES Brasil → a tag da lista do guia que corresponde ao assunto (Artigos não vira tag). Comunhão → a subcategoria temática do artigo como tag provisória, conforme o guia.
   - **Foto:** a destacada. O guia proíbe imagem de IA na arte: se a destacada for IA, use outra foto real do tema; sem foto real, não faça o story e registre.
2. `criar_post_instagram` com `tipo` "story", `etapa` "aprovado", `midias` [{arte_id}], `materia_id`, `gerada_por_ia` false, `pedido` e `guia` preenchidos. A pergunta "mando para aprovação ou posto direto?" já está respondida: **posta direto** (pedido do Mário Fernando, 30/10/2026).
3. `publicar_post_instagram` com `post_id`, `versao`, `quando` "agora" e `destinos` ["stories"]; repita com o `codigo_confirmacao`.
4. Comunhão: não faz story de artigo sobre tragédia, violência ou eleição (regra do Instagram da Comunhão).
5. Falha no story não desfaz a publicação: registre em Pendências.

## 9. Duplicidade e controle

A rotina se reconhece por três marcas: tag "Acervo de Artigos", chapéu com o nome do articulista (até 13/11/2026 era "ARTIGO") e a frase "É uma republicação do acervo de artigos" no pé.

Antes de escrever e de novo antes de publicar:

1. **O que a rotina já fez:** `listar_materias` com `busca` "Acervo de Artigos" e com `autor` "Redação", `portal` do dia, últimos 365 dias, formato compacto; confirme com `ver_materia`. Daí saem os artigos já usados e a data do último uso de cada articulista. O mesmo artigo original nunca é republicado duas vezes.
2. **Site, na NEIA:** `search-content` na fonte do site pelo título original e pelo tema com o nome do autor.
3. **Site, na web:** WebSearch `site:comunhao.com.br "<título>"` ou `site:esbrasil.com.br "<título>"`.

Como decidir:

- O mesmo artigo está no site há **menos de 2 anos**: troque de artigo.
- Está no site há **mais de 2 anos**: siga com a republicação e liste o post antigo no resumo, em "Para tirar do ar" (link, id do post e link da versão nova). Nada é apagado por esta rotina.
- Rascunho da equipe com o mesmo artigo: troque de artigo.

## 10. Resumo e notificação

**Não envie e-mail.** Siga o padrão (seção 10), com o título "Artigos do acervo 8h · DD/MM" e estas seções:

- **Publicados:** por portal, título com link, articulista (vivo ou in memoriam), origem (edição ou post e data original, "data deduzida" quando for), categoria, nota de escolha, nota SEO, imagem (real, arquivo ou IA), se teve Nota de contexto.
- **Stories:** post_id, link do Studio e situação (publicado ou falhou).
- **Rejeitados no dia:** título, articulista, edição e motivo (não é artigo, contexto, dados ou outro), uma linha cada.
- **Para tirar do ar:** versões antigas no site, quando houver.
- **Imagens de IA para validar**, quando houver.
- **Pendências:** cargo não confirmado, data deduzida, grafia em dúvida, referência bíblica corrigida, articulista novo para a lista, story que falhou.

Notificação do app Claude ao terminar.