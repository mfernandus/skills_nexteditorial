---
name: "artigos-acervo-esbrasil"
description: "Rotina diária que republica às 8h, no site da ES Brasil, um texto autoral assinado do acervo (artigo, opinião ou gestão que não seja repercussão de factual), com in memoriam, data original, nota de contexto, regras de rejeição e story enviado para revisão da Joviana e do Mário."
---

# Artigos do acervo — ES Brasil (8h)

Objetivo: todo dia às 8h, um texto autoral assinado por um dos articulistas mais importantes da casa volta ao ar no site da **ES Brasil** (esbrasil.com.br), com o texto do autor preservado, a data da publicação original no rodapé, "in memoriam" quando o autor já morreu e nota de contexto quando o texto pede. O story do Instagram fica pronto **em revisão**, para a Joviana e o Mário aprovarem.

A Comunhão tem rotina irmã, `artigos-acervo-comunhao`, com as mesmas regras. Mudança de regra comum às duas se faz nas duas.

Responda sempre em português do Brasil. Execução agendada: não faça perguntas. Na dúvida, tome a decisão mais conservadora (trocar de texto) e registre no resumo. Escreva **ES Brasil** em negrito no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns: publicação direta (2), pautas proibidas (2.1, vale acima de tudo), matéria agendada (2.2, vale acima de tudo), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), SEO (8), imagem destacada (9) e avisos (10). Onde as duas divergirem, vale esta skill nestes pontos (decisões do Mário Fernando):

- **O texto do articulista não se reescreve** e nenhum número dele é atualizado: texto assinado é opinião do autor. O que mudou desde então vai na Nota de contexto, que traz sempre os dados atualizados, com fonte e ano, e a peça do NXtab quando o dado couber num modelo (padrão, seções 12 e 13); se a mudança compromete o texto, ele é rejeitado (seção 6). (30/10/2026; dados e NXtab em 13/11/2026)
- **Título original mantido** (seção 8). (30/10/2026)
- **Rodapé próprio** (in memoriam, minibio, origem e aviso de republicação) no lugar do "Com informações de". (30/10/2026)
- **Story só com revisão:** a rotina deixa o story em "Para revisar" e não aprova, não agenda e não publica story. A Joviana e o Mário revisam e decidem quando sai (seção 10). (02/11/2026)
- **Articulista vivo não é avisado** antes da republicação. (02/11/2026)

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

Entra texto **autoral e assinado**: o autor defende uma ideia, analisa um tema ou orienta o leitor com a própria voz. O texto chega por um destes dois caminhos.

### 2.1 Editoria Artigos (decisão de 30/10/2026)

- **Revista:** o texto completo (`get-article-content`) começa com o cabeçalho da editoria antes do título. Contam: "ARTIGO", "Artigo", "ARTIGOS", "ARTIGO ESPECIAL", "Artigo | Cotidiano", "Artigo / Tecnologia", "ARTIGO / ESBRASIL" (nas edições recentes; a digitalização grafa "ESPRASIL" ou "ESPERASIL") e erros evidentes de digitalização da palavra ("ÁRTICO", "ANTIQUO"). Exemplo: "Artigo / Cotidiano / por Eustáquio Palhares / Xô carro!".
- **Site:** post da categoria **Artigos** (`wp_categories`).

### 2.2 Opinião, análise e gestão de outras editorias (decisão de 02/11/2026)

Texto assinado que saiu com cabeçalho de outra editoria (ECONOMIA, GESTÃO, POLÍTICA, SEGURANÇA, TECNOLOGIA, INOVAÇÃO, AGRONEGÓCIO, OPINIÃO, ATUALIDADE, CULTURA, COMPORTAMENTO...), ou post de outra categoria do site, entra quando passa nos **três testes**:

1. **É autoral.** Assinado por articulista ou colaborador ("Por Fulano" no início ou minibio de colaborador no fim), com a tese do próprio autor. Citações de terceiros só apoiam o argumento. Reportagem (texto apoiado em entrevistados e apuração), entrevista, perfil, nota e matéria assinada pela redação ou por jornalista da casa **não** são autorais, mesmo assinados.
2. **É opinião, análise ou gestão.** Defende uma posição, interpreta um tema ou orienta o leitor: liderança, planejamento, pessoas, finanças, marketing, inovação, carreira, cidade, desenvolvimento, comportamento.
3. **Não é repercussão de factual.** O texto não nasceu para comentar um fato da época: decisão de governo, eleição, índice ou balanço do mês, crise, operação, julgamento, lançamento, evento, posse, morte, resultado de empresa. **Teste:** tire o fato da semana; se o argumento cai, é repercussão e não entra. Texto que usa um fato antigo só como exemplo de uma tese que continua de pé pode entrar.

Na dúvida em qualquer um dos três, fica fora.

### 2.3 Continua fora

- **Coluna**, mesmo assinada: O Endereço da História, Modus Vivendi, Fim de Papo, Palavra de Pastor, Estudo Bíblico, Som & Cia, Mindset, Essas Mulheres, Zoom Marketing, Família S/A, Tira-Gosto, Pratos do Dia, Periscópio, Gente, O editor recomenda, Panorâmicas.
- **"ARTIGO DO LEITOR"**: não é articulista da casa (confirmado em 02/11/2026).
- Editorial, reportagem, entrevista, página sem cabeçalho legível.
- Texto da edição de Retrospectiva ou balanço do ano: é repercussão por natureza.
- O tipo (`content_type` "article" ou "column") e a seção que a NEIA atribui são só pista: erram para os dois lados (na conferência de 30/10, um em cada quatro). Vale o cabeçalho da página (revista), a categoria e a assinatura (site) e a leitura do texto.

## 3. Fontes no NEIA

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch. Uma chamada de cada vez; "Não foi possível conectar": repita a mesma chamada.

| Fonte | Id | O que tem |
|---|---|---|
| REVISTA ESBRASIL | 019d1cf8-4fc8-72e4-ab29-5ef31d204e4d | Edição 1 (abr/2005) à 229 |
| ESBRASIL.COM.BR | 019d2231-a834-71ec-af78-1ad6fa55f69a | Posts do site |

- **Revista:** `search-content` com `source`, `author` = nome do articulista, `query` "artigo" (e, para a seção 2.2, `query` com o tema: "gestão", "liderança", "economia", "opinião"), `page_size` 200. O filtro de autor funciona na revista. Teste as grafias da seção 4.
- **Site:** o campo `author` é quem postou no WordPress (Erik Oakes, Nathanael Rodor, Mario Fernando Souza...), **não** o articulista; o filtro de autor não acha o articulista. Busque por tema e pelo nome do articulista na fonte do site e leia com `get-article-content`: o articulista está em "**Por Fulano**" no começo, na minibio do fim ("**Fulano** é...") e em `metadata.llm_author`. O nome dele costuma estar também nas tags (`wp_tags`).
- O `published_at` de um post que já é republicação é a data nova; a original só aparece no texto ("Este artigo foi publicado originalmente em…").
- `get-article-content` traz o texto completo; no site, também `wp_post_id`, `wp_url`, `published_at` e `featured_image`.
- **Prefira a revista.** O post do site entra quando o texto só existe lá.
- **Corte de tempo:** publicação original com pelo menos 12 meses no dia da execução.

### 3.1 Datas: conferir antes de usar

- `list-editions` (project_id = id da revista) dá a data de cada edição. Na revista, use **só mês e ano**.
- As edições 185 a 229 vêm com 01/01/2000 (data vazia) e a 195 vem com nov/2020, fora da sequência. Deduza pela sequência das vizinhas (184 = dez/2020; 196 = dez/2021; 223 = jun/2024; 225B = dez/2024; 228B = ago/2025) e por marcas do texto. Registre "data deduzida" no resumo.
- O mesmo texto pode estar em mais de uma edição ou na revista e no site. O original é o **mais antigo**. Post do site que já é republicação traz "Este artigo foi publicado originalmente em…": use a data citada, conferida na revista quando possível.

## 4. Articulistas

Ordem de prioridade. Grafias que a NEIA usa entre parênteses. Status conferido em 30/10/2026; reconfira a cada uso (seção 7.1).

**Nível A:** Eustáquio Palhares · Lucas Izoton · Luiz Fernando Schettino · Orlando Caliman · Arilda Teixeira · José Antonio Bof Buffon · Sidemberg Rodrigues · Ronald Carvalho (Zoom Marketing é coluna: não entra).

**Nível B:** Gilberto Sudré · Luciano Raizer · Ralph Chelotti (Ralph Chellotti) · Usiel Carneiro · Pablo Lira · Enio Bergoli (Énio Bergoli) · Robson Melo · Manoel Goes Neto · Adilson Neves · André Gomyde · João Luiz Vassalo Reis · Luiz Fernando Leitão (Tira-Gosto é coluna: não entra).

**Entram pela seção 2.2 (desde 02/11/2026), nível B:** Arlindo Villaschi · Diógenes Lucca · Eduardo Araújo. Os textos deles saíram com chapéu de editoria (ECONOMIA, SEGURANÇA etc.): cada um passa pelos três testes.

**Com cautela, nível B:** André Pereira César · Rodrigo Augusto Prando. Escrevem análise política, que quase sempre é repercussão de factual ou toca eleição e governo da época (seção 6.3). Só entra texto de tese atemporal (instituições, democracia, cultura política), sem governo, partido, candidato ou eleição.

**Coluna, fora:** Ivo Nogueira Dias (Modus Vivendi) · José Eugênio Vieira (O Endereço da História) · Andrea Monteiro, Fabricia Kirmse e Natache Barros (Essas Mulheres) · Leonardo Carraretto (Mindset) · Adriano Salvi (Família S/A). Se um texto deles sair fora da coluna e passar na seção 2, ele entra.

**Políticos, fora:** Paulo Hartung, Renato Casagrande, Max Filho.

A planilha "Lista de artigos do acervo — ES Brasil e Comunhão" (30/10/2026) traz a contagem por articulista, as edições, o status e as fontes. Ela foi feita pela regra antiga (só a editoria Artigos): os textos da seção 2.2 não estão nela.

### Rotação

- Um texto por dia neste portal (confirmado em 02/11/2026). Nível A em 4 a 5 dias da semana; nível B completa a semana.
- O mesmo articulista não repete em menos de 5 dias.
- Dentro do articulista, comece pelos textos mais antigos ainda não usados, salvo gancho de calendário.
- Articulista novo achado na base (assina 3 ou mais textos que passam na seção 2) pode entrar no nível B; registre no resumo para o Mário incluir na lista.

### Fora da lista, sempre

- Político com mandato, candidato ou pré-candidato e artigo de autoridade sobre o próprio governo.
- Texto de terceiros reproduzido pela revista ou pelo site: crônica de outro veículo, capítulo de livro, artigo traduzido de autor estrangeiro, poema ou letra de outro autor, coletânea de frases ou "lições" alheias, release.
- Autor que pediu para não ser republicado (lista de exclusão do Mário; vazia em 02/11/2026).

## 5. Escolha do texto do dia

1. Veja o que a rotina já publicou (seção 11) e escolha o articulista do dia pela rotação.
2. Liste os textos dele (seção 3) e descarte os já usados.
3. Leia os candidatos com `get-article-content` até achar um aprovado: primeiro confirme que entra (seção 2), depois aplique a seção 6. Até 8 leituras; sem aprovado, passe ao próximo articulista da fila.

### Nota de escolha (0 a 5 cada, mínimo 14 de 20)

- **Atemporalidade:** o argumento vale hoje sem depender do fato da época.
- **Autonomia:** o texto se entende sozinho, sem nota de contexto ou com uma nota curta.
- **Qualidade do original:** texto completo, sem trechos quebrados pela digitalização.
- **Interesse:** tema procurado hoje ou com gancho de calendário próximo: aniversário de Vitória (8/9), Dia do Espírito Santo (23/5), Dia da Indústria (25/5), Dia do Economista (13/8), Dia do Comerciante (16/7), Dia do Agricultor (28/7), Dia do Trabalho (1/5), virada do ano e planejamento.

Contam também como gancho: o aniversário de morte do articulista (5, 10, 20 anos), o aniversário de nascimento e uma data citada no próprio texto (criação de um município, posse, fundação).

Empate: o gancho de calendário, depois o articulista de nível A, depois a década menos usada nos últimos 30 dias.

## 6. Rejeição

Rejeite e troque de texto quando:

### 6.1 O contexto compromete

O argumento central depende de um fato da época e, lido hoje, confunde ou engana o leitor. Exemplos:

- comenta como atual uma eleição, um governo, uma crise, uma CPI, um escândalo, a pandemia, uma Copa ou um evento, e não se sustenta sem eles;
- anuncia ou recomenda algo que acabou (evento, campanha, programa, produto, lei em tramitação, instituição);
- a premissa foi desmentida pelos fatos ("o Brasil nunca vai…" e foi);
- precisaria de mais de dois itens na Nota de contexto para ser entendido, ou a nota contradiria o autor.

Contexto leve fica, com Nota de contexto: um ano citado, um fato antigo usado como exemplo, uma expressão de tempo ("este ano", "hoje") que se resolve com a data.

### 6.2 Os números comprometem

O raciocínio se apoia em dados específicos que envelheceram e mudam a conclusão: estatísticas, preços, salários, câmbio, juros, inflação, PIB, população, rankings, percentuais de conjuntura, contas com valores da época. Regra prática: **valor em reais usado como referência atual, ou mais de um número de conjuntura no argumento central, rejeita.** Um número histórico datado pelo próprio autor ("em 1998 eram…") que não sustenta a conclusão pode ficar.

### 6.3 Outros motivos

- Pautas proibidas (padrão, 2.1), política partidária ou eleitoral.
- Texto incompleto, ilegível ou com menos de 350 palavras.
- Tema de saúde (inclusive saúde mental) com orientação que hoje seria inadequada.
- Tema sensível que pede tratamento atual e revisão humana: abuso sexual, suicídio, aborto, violência contra a mulher, chacina, linchamento.
- Publieditorial, conteúdo de marca ou texto que promove empresa, produto ou evento.
- Texto técnico de equipamento ou tecnologia superada.
- **Autoria em dúvida:** pesquise na web, entre aspas, uma ou duas frases características do texto. Se ele aparece antes, atribuído a outra pessoa, ou circula como texto sem autor, rejeite e marque "autoria a conferir".
- **Erro de fato do original:** confira uma vez as datas e os números históricos centrais do texto (nascimento, morte, posse de um personagem). Erro que não é de digitalização rejeita: corrigir seria reescrever o autor.
- Já está no site há menos de 2 anos (seção 11).

Todo texto descartado vai para o resumo com o motivo: **não entra** (coluna, leitor, reportagem ou repercussão de factual), **contexto**, **dados** ou **outro**.

## 7. Conferências

### 7.1 O articulista está vivo?

- Confira na web no dia (WebSearch e WebFetch). Morte só com **duas fontes independentes** (cobertura da própria **ES Brasil** no site vale como uma).
- **Falecido:** "In memoriam" no rodapé, antes do nome (seção 8), com o mês e o ano da morte.
- **Vivo:** minibio com o cargo e a função **atuais**, conferidos na fonte oficial (instituição, empresa, currículo). Não deu para confirmar o cargo atual: minibio só com o que não muda ("economista", "foi diretor do Sebrae/ES") e registro no resumo. **Não avise o articulista** antes de republicar.
- **Sem rastro recente** (nem obituário, nem atividade): minibio neutra, que vale nos dois casos: "[Nome] assinou artigos na revista ES Brasil entre [ano] e [ano]." Registre "status não confirmado" no resumo.
- Pessoa citada no texto que mudou de cargo ou morreu: o texto do autor fica; a Nota de contexto avisa quando muda o sentido.

### 7.2 Texto

- **Não reescreva.** Mantenha palavras, ordem, citações e números do autor.
- Tire o cabeçalho da página (editoria, nome do autor solto, minibio da época, créditos de foto e olhos repetidos) e escreva a abertura e o rodapé desta skill.
- Pode: corrigir erro evidente de digitalização ("capivaba" → "capixaba", hifenização quebrada, linhas partidas), erro evidente de grafia ou concordância ("a sociedade conspiram" → "conspira", "boas vindas" → "boas-vindas", nome oficial de cidade), padronizar aspas e paragrafação, transformar caixa alta em caixa normal. Registre cada correção no resumo.
- Link estranho no meio do texto (spam, como já apareceu em post antigo do site): retire e registre.
- Não pode: cortar trechos, atualizar dados, trocar termos, suavizar opinião. Se o texto precisa disso, rejeite (seção 6).

## 8. Formato da matéria

- **Título:** o original, só com correção de caixa e digitação. O título SEO (até 60 caracteres) pode ser diferente.
- **Linha fina:** a original (na revista, a frase em destaque logo abaixo do título). Sem ela, uma frase de até 25 palavras com a ideia central do texto, sem inventar. Se o texto tem marca de tempo que só se entende com a data ("este ano", "atualmente"), a linha fina termina com o ano: "…, em artigo de 2009".
- **Chapéu:** o nome do articulista, em caixa alta e baixa, na grafia principal da seção 4 (sem cargo ou título), ex.: "Eustáquio Palhares". Vale também para os textos da seção 2.2. "In memoriam" não entra no chapéu: fica no rodapé. "Artigo" não é mais chapéu (decisão do Mário Fernando, 13/11/2026).
- **Assinatura no NX Feed:** "Redação" (o articulista não tem credencial). O autor aparece no texto.
- **Abertura do texto:** `<p><strong>Por [Nome do articulista]</strong></p>`.
- **Intertítulos:** só os do original, em `<h4>`.
- **Links:** um interno, para matéria ou artigo recente do portal sobre o tema ou o autor; até dois externos, só na Nota de contexto.

### Bloco final, nesta ordem

1. **Nota de contexto** (quando o texto pede contexto ou cita dado que tem versão mais nova): uma a três frases, com fatos conferidos e fonte, sem opinar sobre o autor. Cada dado atualizado entra numa frase própria, com fonte e ano, e não conta no limite de três frases nem no de itens da seção 6.1. Quando o dado couber num modelo do NXtab, a peça vem logo depois da nota, na paleta da **ES Brasil** (`marca` "esb"; padrão, seção 12).
2. **Minibio:** vivo → `<strong>Nome</strong> é …` (cargo atual). Falecido → `<em>In memoriam</em> — <strong>Nome</strong> foi …, morreu em [mês] de [ano].`
3. **Origem:** revista → "Artigo publicado originalmente na edição nº [X] da Revista ES Brasil, em [mês] de [ano]." Site → "Artigo publicado originalmente no portal esbrasil.com.br em [dia] de [mês] de [ano]."
4. **Aviso:** "É uma republicação do acervo de artigos da ES Brasil. As pessoas citadas podem não estar mais nos cargos e situações da época, e as opiniões e os fatos referem-se ao contexto de então."

Modelo HTML (articulista falecido):

```html
<p><strong>Por Fulano de Tal</strong></p>
<p>…texto do autor…</p>
<p><em><strong>Nota de contexto:</strong> o artigo foi escrito em 2009, quando…, segundo o <a href="https://…" target="_blank" rel="noopener">IBGE</a>.</em></p>
<p><em>In memoriam</em> — <strong>Fulano de Tal</strong> foi economista e professor da Ufes; morreu em março de 2019.</p>
<p><em>Artigo publicado originalmente na edição nº 120 da Revista ES Brasil, em maio de 2014.</em></p>
<p><em>É uma republicação do acervo de artigos da ES Brasil. As pessoas citadas podem não estar mais nos cargos e situações da época, e as opiniões e os fatos referem-se ao contexto de então.</em></p>
```

Articulista vivo: a mesma estrutura, com a minibio no presente e sem "In memoriam".

### Categorias e tags (portal ES Brasil = 1)

- **Só Artigos (11960)**, em todo texto da rotina, inclusive os da seção 2.2. Nunca uma segunda categoria temática: com ela, o site mostrava o artigo na editoria do tema (decisão do Mário Fernando, 16/11/2026). O tema vai nas tags.
- Nunca Destaques, Edição Digital, Conteúdo de Marca, Institucional ou Eleições.
- Tags (5 a 10): sempre "Acervo de Artigos" e o nome do articulista, mais tema, setor e instituição quando houver.

### SEO e imagem

- SEO pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo). O título fica o original; a palavra-chave e o título SEO trazem o termo mais buscado do tema. **O texto do autor nunca muda por causa de SEO:** quando o que falta para a nota 85 exige mexer nele (palavra-chave em intertítulo, por exemplo), publique com a nota que tiver e registre.
- Imagem destacada pelo padrão (seção 9), nesta ordem: personagem do título, quando o texto é sobre uma pessoa (retrato de acervo público com crédito) → **foto do articulista** (NX Fotos pelo nome; imagem destacada de posts antigos dele ou sobre ele no site, que a NEIA traz em `featured_image`; `buscar_imagens`; foto oficial da instituição ou empresa com crédito) → foto real do tema → imagem por IA (nunca o rosto do autor). Foto antiga: "foto de arquivo" na descrição; falecido: "(1929-2016), foto de arquivo".

### Foto destacada: padrão de artigos (decisão do Mário Fernando, 16/11/2026)

Toda destacada com pessoa sai no mesmo padrão, seja qual for a foto de partida (estúdio, cena ou montagem antiga): **a pessoa recortada sobre uma foto do tema bem desfocada (o fundo é sempre trocado), em 1600x900 (16:9), com a cabeça sempre do mesmo tamanho e na mesma altura**: do alto do cabelo ao queixo, metade da altura da imagem; o alto do cabelo a 7% do topo; o rosto no centro; o corte na altura dos braços. Substitui as regras de enquadramento e de fundo neutro de 13 e 14/11/2026: o fundo agora é trocado sempre, não só quando é neutro. Em 16:9, com o rosto no centro e a cabeça logo abaixo do topo, os cortes do tema dos sites (destaque grande 5:3, blocos de 70% e miniaturas quadradas) nunca pegam a cabeça.

1. **A foto mais recente da pessoa (decisão do Mário Fernando, 16/11/2026).** Procure em todas as fontes e fique com a mais recente que sirva, pela data: o acervo WordPress da revista (no navegador, com o site aberto: `/wp-json/wp/v2/media?search=<sobrenome>&orderby=date&order=desc&per_page=30&_fields=date,source_url`; sem navegador, `buscar_imagens` com `fonte` "editoriais" e o nome, que traz a mesma biblioteca; o ano e o mês estão no caminho `wp-content/uploads/AAAA/MM`), o NX Fotos (pasta "Articulistas" e `buscar` pelo nome; campo `data`) e a destacada de posts antigos dele. As fotos de cdn.esbrasil.com.br e cdn.comunhao.com.br baixam direto pelo terminal. Fora: montagem antiga da rotina (nome terminado em "-HHMMSS.webp", fundo já desfocado) quando houver o original, arte com texto, foto de evento (palco, microfone, grupo) e foto com objeto ou outra pessoa encostada (carro, cadeira, haste de microfone, parede com sombra). Confira que é a mesma pessoa das fotos antigas. Prefira a que mostra peito e ombros; foto recente fechada no peito ainda serve (o script resolve, item 4), mas, se o resultado ficar só cabeça e gola, use a mais recente que tenha corpo.
2. **Fundo do tema, no NX Fotos** (`buscar`, `orientacao` "h", `tipo` "foto"): foto real, horizontal, ligada ao tema do artigo. Exemplos: gestão, carreira e liderança → escritório; ESG, sustentabilidade e meio ambiente → área verde; urbanismo e cidades → Centro de Vitória, orla ou Terceira Ponte; mobilidade → trânsito na cidade; economia, indústria e logística → porto ou fábrica; agro e mundo rural → lavouras capixabas; turismo → cartão-postal capixaba. Prefira a biblioteca dos fotógrafos da casa (Sidney Pagotto, Claudio Alves e demais). Nunca foto oculta (`visibilidade` "oculta", banco de imagem comprado), de outro veículo ou da Reuters, nem com texto, logotipo ou pessoa em primeiro plano. A versão de 1600 px do CDN basta, porque o fundo vai desfocado.
3. Grave o script abaixo como `padronizar_retrato.py` e rode `python3 padronizar_retrato.py foto.jpg fundo.jpg destacada.jpg --altura 0.45 --folha folha.jpg` (`--altura`, de 0 a 1, escolhe a faixa da foto do tema que fica atrás da pessoa). Ele recorta a pessoa (rembg; se faltar, `pip install --break-system-packages "rembg[cpu]" opencv-python-headless`), acha o rosto (YuNet), trata a foto, iguala a cabeça e compõe sobre o tema desfocado. **Tratamento (decisão do Mário Fernando, 16/11/2026):** é medido no rosto de cada foto, não é filtro fixo: foto escura clareia, pele avermelhada ou alaranjada volta ao tom natural, terno preto ganha detalhe e pele morena ou negra não é clareada à força. Nunca aplique ao retrato o tratamento quente das matérias (`padrao-publicacao-next` 9.3) nem o do NX Feed: a destacada sobe com `tratamento` "nao". **Foto já tratada (decisão do Mário Fernando de 25/11/2026):** antes, rode `python3 tratar_foto_next.py --verificar foto.jpg` (skill `tratamento-fotos-next`, com `--origem site` para foto do acervo WordPress). Se a foto já tem a marca da casa (inclusive a invisível), a palavra-chave `tratada-nx-v1` no NX Fotos ou foi editada pelo fotógrafo (Lightroom, Photoshop), rode o `padronizar_retrato.py` com `--sem-tratamento`: só recorte, fundo e cabeça. A destacada nova sai do script; a foto inteira tratada que vai para o NX Fotos (item 8) recebe depois a marca com `tratar_foto_next.py --tipo pessoas --sufixo`.
4. Leia o JSON. Com `ok` true, siga. Com problema:
   - "tratamento": a pele do rosto antes e depois (L, a, b). Bom: L 158 a 184, a 14 a 18, b 12 a 22. Pele morena ou negra pode fechar com L menor (o JSON traz "claros_ja_certos"): está certo. "rosto ainda escuro": olhe; se continuar escuro, troque a foto.
   - "foto fechada" e "tronco esfumado" (em "ajuste" e "ajuste_base"): a foto acaba no peito; a cabeça cresceu até 56% e o tronco some num degradê para a base escurecida do fundo. Olhe a saída.
   - "corpo curto demais": falta mais de 16% da altura mesmo com a cabeça em 56%. Se o esfumado deixar só cabeça e gola, troque pela foto mais recente que tenha corpo. `--aceitar-cabeca-maior` (cabeça maior, sem esfumado) só quando não houver outra; registre "cabeça maior que o padrão" em Pendências.
   - "corte lateral esfumado": a foto original corta o ombro ou o braço, e o script esfuma o corte. Se o degradê ficar estranho, troque a foto.
   - "sem rosto detectado" ou "ampliação alta": troque a foto. Sem outra, mantenha a destacada que houver e registre "foto fora do padrão" em Pendências.
5. Olhe com Read a saída e a folha (cortes 5:3, 70% e quadrado): cabeça inteira, alto do cabelo logo abaixo do topo, recorte limpo, sem halo, sem pedaço do fundo antigo ou de objeto grudado na pessoa, sem orelha, óculos ou ombro comidos, sem fio ou haste grudado no ombro; pele com cor natural (nem escura, nem avermelhada, nem alaranjada) e terno com detalhe, não um bloco preto. Com defeito, troque a foto ou o fundo.
6. Suba com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `materia_id`) e `curl -T`, e grave a URL que o envio devolve com `definir_imagem_destacada` (`tratamento` "nao"). O link de envio é de uso único: não mostre nem guarde. Campos: título "<Nome>, articulista da ES Brasil"; fonte, a da foto da pessoa; autor "<crédito da foto da pessoa>; fundo: <autor do fundo>/NX Fotos"; descrição "<Nome>, autor do artigo[, em <ano da foto>]; foto de arquivo, em montagem com fundo ilustrativo de <cena>"; legenda (alt) com o que se vê, terminando em "diante de <cena> desfocada".
7. Vale para toda foto de pessoa na destacada (articulista ou personagem do título). Foto de tema sem pessoa e imagem de IA (gerada em 16:9) não passam pelo script.
8. **Foto nova vai para o NX Fotos.** Quando a foto da pessoa veio do acervo WordPress e ainda não está no NX Fotos, rode o script também com `--retrato retrato.jpg` (a foto inteira, com o fundo original, tratada) e salve-a na pasta "Articulistas" do NX Fotos (id 1450): no navegador, Gerenciador de Mídia (nxfotos.com.br/admin/midia), arquivo no campo de envio (`file_upload`) e "Enviar"; depois `listar_biblioteca` (texto: o nome do arquivo) para achar o `mediaId`, `editar_midia` (título "<Nome>, articulista da ES Brasil (<ano>)", autor "Arquivo ES Brasil", descrição com roupa e ano, palavras-chave com nome, articulista, revista e retrato, e a URL de origem em notas) e `mover_para_pasta` com a pasta 1450. Sem navegador na sessão, registre em Pendências "foto nova de <Nome> para o NX Fotos: <URL>".

```python
#!/usr/bin/env python3
"""Padrão de foto dos artigos: recorta o articulista, TRATA a foto, troca SEMPRE o fundo e iguala a cabeça.

Decisões do Mário Fernando (16/11/2026): toda destacada de artigo sai no mesmo padrão,
seja qual for a foto de partida (estúdio, cena, montagem antiga):
  - a foto mais recente do articulista (acervo WordPress das revistas, NX Fotos);
  - tratamento adaptativo, medido no rosto de cada foto: foto escura clareia, pele avermelhada
    ou alaranjada volta ao tom natural, terno preto "empapado" ganha detalhe; pele morena ou
    negra não é clareada à força (o tratamento quente das matérias não vale para retrato);
  - a pessoa recortada (rembg) sobre uma foto do tema bem desfocada (o fundo é sempre trocado);
  - 1600x900 (16:9);
  - a cabeça sempre do mesmo tamanho e na mesma altura: do alto do cabelo ao queixo = 50%
    da altura; alto do cabelo a 7% do topo; rosto no centro; corte na altura dos braços.
    Foto recente fechada no peito: a cabeça cresce até 56% e o que faltar vira esfumado do
    tronco para a base escurecida do fundo.

Uso:
  python3 padronizar_retrato.py foto.jpg fundo.jpg saida.jpg [--altura 0.45] [--folha folha.jpg]
  fundo.jpg: foto do tema (NX Fotos, horizontal). Use "cinza" só para testar.
  --altura: de 0 (alto) a 1 (baixo), a faixa da foto do tema que fica atrás da pessoa.
  --aceitar-cabeca-maior: foto fechada demais e nenhuma outra do articulista: a cabeça cresce
    o necessário para o corpo chegar à base (o alto da cabeça continua a 7%), sem esfumado.
  --sem-tratamento: só para foto que já veio tratada.
  --retrato r.jpg: grava também a foto inteira, com o fundo original, tratada (para o NX Fotos).
Imprime um JSON. "tratamento" traz a pele do rosto antes e depois (L, a, b do Lab de 8 bits):
rosto bom fica com L 158 a 184, a 14 a 18, b 12 a 22. "ok": false lista os problemas (corpo
curto demais, corte lateral, ampliação alta, sem rosto, rosto ainda escuro): confira a saída e,
se ficar ruim, escolha outra foto do articulista.
Precisa de: pip install --break-system-packages "rembg[cpu]" opencv-python-headless
(o detector de rosto YuNet é baixado na primeira vez para a pasta modelos/).
"""
import json, os, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

W, H = 1600, 900
TOPO = 0.07      # alto do cabelo, em fração da altura
CABECA = 0.50    # do alto do cabelo ao queixo, em fração da altura (metade da imagem)
AMPLIAR = False  # --aceitar-cabeca-maior: só quando não houver outra foto do articulista
FOLGA = 0.04     # se o corpo não chegar à base por até 4% da altura, a pessoa desce esse tanto
CENTRO_X = 0.50  # centro do rosto
CABECA_MAX = 0.56  # foto fechada: a cabeça pode crescer até aqui antes de esfumar o tronco
TRATAR = True    # tratamento adaptativo do retrato (--sem-tratamento desliga)


HAAR_BASE = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/"
YUNET_URL = ("https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/"
             "face_detection_yunet/face_detection_yunet_2023mar.onnx")
MODELOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos")


def cascata(nome):
    import cv2
    p = os.path.join(MODELOS, nome)
    if not os.path.exists(p):
        os.makedirs(MODELOS, exist_ok=True)
        urllib.request.urlretrieve(HAAR_BASE + nome, p)
    return cv2.CascadeClassifier(p)


def achar_rosto(im, mask):
    """Maior rosto dentro da pessoa e com largura de rosto (pelo menos 45% da largura da
    silhueta na altura dos olhos), para não pegar botão, óculos ou mão."""
    import cv2
    w, h = im.size
    # 1º YuNet (rede neural do OpenCV, bem mais confiável que o Haar em foto fechada)
    yn = os.path.join(MODELOS, "yunet.onnx")
    if not os.path.exists(yn):
        try:
            os.makedirs(MODELOS, exist_ok=True)
            urllib.request.urlretrieve(YUNET_URL, yn)
        except Exception:
            pass
    if os.path.exists(yn) and hasattr(cv2, "FaceDetectorYN"):
        bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        det = cv2.FaceDetectorYN.create(yn, "", (w, h), 0.7, 0.3, 5000)
        _, faces = det.detect(bgr)
        if faces is not None and len(faces):
            boas = [f for f in faces if mask[min(h - 1, int(f[1] + f[3] / 2)), min(w - 1, int(f[0] + f[2] / 2))]]
            if boas:
                f = max(boas, key=lambda f: f[2] * f[3] * f[14])
                x, y, fw, fh = (float(v) for v in f[:4])
                # caixa do YuNet vai da testa ao queixo; converte para a geometria do Haar
                # (queixo = y + 1,07 * altura), que o resto do script usa
                return int(x), int(y), int(fw), int(fh / 1.07)
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    for nome in ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"):
        cas = cascata(nome)
        for viz in (6, 4, 3):
            fs = cas.detectMultiScale(g, 1.06, viz, minSize=(int(min(w, h) * 0.06),) * 2)
            boas = []
            for (x, y, fw, fh) in fs:
                cx, cy = int(x + fw / 2), min(int(y + fh * 0.4), h - 1)
                linha = mask[cy, :].sum()
                if mask[cy, min(cx, w - 1)] and fw >= 0.45 * linha:
                    boas.append((int(x), int(y), int(fw), int(fh)))
            if boas:
                return max(boas, key=lambda r: r[2] * r[3])
    return None


def maior_componente(alfa):
    import cv2
    bin_ = (alfa > 128).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bin_, 8)
    if n <= 2:
        return alfa
    k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    keep = (lab == k).astype(np.uint8)
    keep = cv2.dilate(keep, np.ones((9, 9), np.uint8))       # mantém a borda suave
    return (alfa * keep).astype(np.uint8)


PELE_L = (158, 184)   # luminância do rosto (Lab 8 bits do OpenCV): abaixo é escuro, acima estoura
PELE_A, PELE_B = 14, 16   # tom de pele de referência (a*, b* a partir do neutro 128)
TOL_A, TOL_B = 4, 5       # dentro da tolerância, a cor da pele não é mexida


def medir_pele(lab, rosto, mask):
    """Mediana de L, a, b na pele do rosto (bochechas, nariz, testa baixa), só dentro do recorte."""
    fx, fy, fw, fh = rosto
    hh, ww = mask.shape
    x0, x1 = max(0, int(fx + .22 * fw)), min(ww, int(fx + .78 * fw))
    y0, y1 = max(0, int(fy + .30 * fh)), min(hh, int(fy + .85 * fh))
    reg = lab[y0:y1, x0:x1].reshape(-1, 3)
    m = mask[y0:y1, x0:x1].reshape(-1)
    reg = reg[m]
    if len(reg) < 50:
        return None
    L = reg[:, 0]
    reg = reg[(L > np.percentile(L, 15)) & (L < np.percentile(L, 95))]   # tira sombra e brilho
    med = np.median(reg, axis=0)
    return float(med[0]), float(med[1] - 128), float(med[2] - 128)


def tratar_pessoa(rgb, mask, rosto):
    """Tratamento adaptativo do retrato, medido no rosto de cada foto (não é filtro fixo):
    1) exposição: leva a luz do rosto para a faixa PELE_L (foto escura clareia, estourada escurece);
    2) sombras: terno preto 'empapado' ganha um pouco de detalhe;
    3) cor: dominante geral pelos brancos da roupa; pele avermelhada/alaranjada volta ao tom natural;
    4) contraste local suave (CLAHE) só na pessoa.
    O tratamento quente e saturado das matérias (padrao-publicacao-next 9.3) NÃO vale para rosto."""
    import cv2
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    antes = medir_pele(lab, rosto, mask) if rosto else None
    rel = {"antes": [round(v) for v in antes] if antes else None, "passos": []}
    if not antes:
        return rgb, rel
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]

    # 1) exposição pelo rosto (gamma no L)
    lf = antes[0]
    alvo = None
    if lf < PELE_L[0]:
        alvo = PELE_L[0] + 6
    elif lf > PELE_L[1]:
        alvo = PELE_L[1] - 4
    p98 = float(np.percentile(L[mask], 98)) if mask.any() else 255
    if alvo and alvo > lf and p98 >= 235:
        # os claros da foto já estão certos (camisa branca bem exposta): o rosto escuro é
        # sombra ou pele morena/negra; clareia com moderação, sem "embranquecer" a pele
        alvo = min(alvo, lf + 40)
        gmin = 0.70
        rel["claros_ja_certos"] = True
    else:
        gmin = 0.55
    if alvo:
        g = float(np.clip(np.log(alvo / 255) / np.log(max(lf, 20) / 255), gmin, 1.35))
        L[:] = 255 * (L / 255) ** g
        rel["passos"].append(f"exposição gamma {g:.2f}")

    # 2) sombras do corpo (abaixo do queixo)
    fx, fy, fw, fh = rosto
    corpo = mask.copy(); corpo[:int(fy + 1.1 * fh)] = False
    if corpo.sum() > 500:
        preto = float((L[corpo] < 45).mean())
        if preto > 0.18:
            lift = 16 + 14 * min(1.0, (preto - 0.18) / 0.4)
            x = np.clip(1 - L / 110, 0, 1)
            L[:] = L + lift * x ** 2
            rel["passos"].append(f"sombras +{lift:.0f} ({preto:.0%} do corpo quase preto)")

    # 3a) dominante geral: brancos e cinzas claros da pessoa (camisa) devem ser neutros
    C = np.hypot(A - 128, B - 128)
    neutro = mask & (L > 175) & (C < 10)
    if neutro.mean() > 0.004 and neutro.sum() > 400:
        da = float(np.median(A[neutro]) - 128); db = float(np.median(B[neutro]) - 128)
        # só corrige no sentido que também leva a pele ao tom natural (camisa azul-clara
        # não pode esquentar uma pele que já está quente)
        pele = medir_pele(np.dstack([L, A, B]), rosto, mask)
        sa = -np.clip(.7 * da, -6, 6) if abs(da) > 2.5 else 0.0
        sb = -np.clip(.7 * db, -6, 6) if abs(db) > 2.5 else 0.0
        if pele:
            if sa * (PELE_A - pele[1]) <= 0: sa = 0.0
            if sb * (PELE_B - pele[2]) <= 0: sb = 0.0
        if sa or sb:
            A += sa; B += sb
            rel["passos"].append(f"dominante geral a{sa:+.1f} b{sb:+.1f}")

    # 3b) pele: só os tons parecidos com a pele do rosto são puxados para o tom natural
    agora = medir_pele(np.dstack([L, A, B]), rosto, mask)
    if agora:
        _, ca, cb = agora
        ea, eb = ca - PELE_A, cb - PELE_B
        if abs(ea) > TOL_A or abs(eb) > TOL_B:
            # corrige o excesso além da tolerância (ex.: a+35 vira ~a+18); não zera a cor
            sa = -np.sign(ea) * max(0.0, abs(ea) - TOL_A) * 0.85
            sb = -np.sign(eb) * max(0.0, abs(eb) - TOL_B) * 0.85
            d2 = (A - 128 - ca) ** 2 + (B - 128 - cb) ** 2
            peso = np.exp(-d2 / (2 * 14.0 ** 2)) * mask
            A += sa * peso; B += sb * peso
            rel["passos"].append(f"pele a{sa:+.1f} b{sb:+.1f}")
        elif np.hypot(ca, cb) < 12:      # rosto acinzentado: devolve um pouco de cor
            f = min(1.25, 16 / max(np.hypot(ca, cb), 1))
            peso = mask.astype(np.float32)
            A[:] = 128 + (A - 128) * (1 + (f - 1) * peso); B[:] = 128 + (B - 128) * (1 + (f - 1) * peso)
            rel["passos"].append(f"cor da pele x{f:.2f}")

    # 4) contraste local suave
    l8 = np.clip(L, 0, 255).astype(np.uint8)
    cl = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(l8).astype(np.float32)
    L[:] = np.where(mask, .65 * L + .35 * cl, L)

    lab = np.dstack([np.clip(L, 0, 255), np.clip(A, 0, 255), np.clip(B, 0, 255)]).astype(np.uint8)
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    depois = medir_pele(cv2.cvtColor(out, cv2.COLOR_RGB2LAB).astype(np.float32), rosto, mask)
    rel["depois"] = [round(v) for v in depois] if depois else None
    return out, rel


def fundo_tema(caminho, altura):
    if caminho == "cinza":
        return Image.new("RGB", (W, H), (128, 132, 136))
    t = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    bw, bh = t.size
    if bw / bh >= W / H:
        cw = int(bh * W / H); x0 = (bw - cw) // 2
        t = t.crop((x0, 0, x0 + cw, bh))
    else:
        ch = int(bw * H / W); y0 = int((bh - ch) * altura)
        t = t.crop((0, y0, bw, y0 + ch))
    t = t.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(W / 55))
    t = ImageEnhance.Brightness(t).enhance(0.92)
    return ImageEnhance.Color(t).enhance(0.85)


def folha(img, saida):
    """Saída e os três cortes do site (5:3 foco 60%, 70% foco 60%, quadrado foco 20%)."""
    caixas = [(0.60, 0.60), (0.70, 0.60), (1.00, 0.20)]
    pecas = [img.copy()]; pecas[0].thumbnail((420, 420))
    for rh, fy in caixas:
        bw, bh = 300, int(300 * rh)
        esc = max(bw / img.size[0], bh / img.size[1])
        r = img.resize((int(img.size[0] * esc + .5), int(img.size[1] * esc + .5)), Image.LANCZOS)
        ox = (r.size[0] - bw) // 2; oy = int((r.size[1] - bh) * fy)
        pecas.append(r.crop((ox, oy, ox + bw, oy + bh)))
    Wf = sum(p.size[0] for p in pecas) + 10 * (len(pecas) + 1)
    Hf = max(p.size[1] for p in pecas) + 20
    out = Image.new("RGB", (Wf, Hf), "white"); x = 10
    for p in pecas:
        out.paste(p, (x, 10)); x += p.size[0] + 10
    out.save(saida, quality=85)


def main():
    a = sys.argv[1:]
    global AMPLIAR, TRATAR
    altura, folha_saida = 0.45, None
    if "--sem-tratamento" in a:
        a.remove("--sem-tratamento"); TRATAR = False
    if "--aceitar-cabeca-maior" in a:
        a.remove("--aceitar-cabeca-maior"); AMPLIAR = True
    if "--altura" in a:
        i = a.index("--altura"); altura = float(a[i + 1]); del a[i:i + 2]
    if "--folha" in a:
        i = a.index("--folha"); folha_saida = a[i + 1]; del a[i:i + 2]
    retrato_saida = None
    if "--retrato" in a:
        i = a.index("--retrato"); retrato_saida = a[i + 1]; del a[i:i + 2]
    ent, fundo_p, sai = a[0], a[1], a[2]

    im = ImageOps.exif_transpose(Image.open(ent)).convert("RGB")
    w, h = im.size
    cache = ent.rsplit(".", 1)[0] + "_recorte.png"     # o recorte é a parte lenta: guarda
    if os.path.exists(cache):
        pessoa = Image.open(cache).convert("RGBA")
        arr = np.array(pessoa)
    else:
        from rembg import new_session, remove
        sess = new_session("isnet-general-use")
        pessoa = remove(im, session=sess, alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=15,
                        alpha_matting_erode_size=8).convert("RGBA")
        arr = np.array(pessoa)
        arr[:, :, 3] = maior_componente(arr[:, :, 3])
        pessoa = Image.fromarray(arr)
        pessoa.save(cache)
    mask = arr[:, :, 3] > 128

    info = {"entrada": f"{w}x{h}", "problemas": []}
    rosto = achar_rosto(im, mask)
    if rosto:
        fx, fy, fw, fh = rosto
        c0, c1 = max(0, int(fx - 0.25 * fw)), min(w, int(fx + 1.25 * fw))
        linhas = np.where(mask[:, c0:c1].any(axis=1))[0]
        topo = int(linhas.min()) if len(linhas) else max(0, int(fy - 0.6 * fh))
        queixo = fy + 1.07 * fh
        cx = fx + fw / 2
    else:
        info["problemas"].append("sem rosto detectado: cabeça estimada pela silhueta")
        ys, xs = np.where(mask)
        topo = int(ys.min())
        cols = xs[ys < topo + h * 0.05]
        cx = float(cols.mean()) if len(cols) else w / 2
        queixo = topo + 0.30 * h
    cabeca = queixo - topo
    s = CABECA * H / cabeca
    ox = CENTRO_X * W - cx * s
    oy = TOPO * H - topo * s
    info.update(rosto=bool(rosto), escala=round(s, 2), cabeca_px_original=int(cabeca))

    if rosto:                       # tira fios, cabos e hastes presos ao corpo (abaixo do queixo)
        import cv2
        arr = np.array(pessoa)
        al = arr[:, :, 3]
        y0 = int(min(h - 1, queixo))
        k = max(7, int(w * 0.02)) | 1
        bin_ = (al[y0:] > 20).astype(np.uint8)
        aberto = cv2.morphologyEx(bin_, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        manter = cv2.dilate(aberto, np.ones((3, 3), np.uint8)) > 0
        fino = (bin_ > 0) & ~manter
        if fino.sum() > 0:
            sub = al[y0:]
            sub[~manter] = 0
            arr[:, :, 3] = al
            pessoa = Image.fromarray(arr)
            mask = arr[:, :, 3] > 128
            info["limpeza"] = f"{int(fino.sum())} px de detalhes finos removidos abaixo do queixo"

    if TRATAR and rosto:            # tratamento adaptativo da pessoa, antes de compor
        arr = np.array(pessoa)
        rgb, rel = tratar_pessoa(np.ascontiguousarray(arr[:, :, :3]), mask, rosto)
        arr[:, :, :3] = rgb
        pessoa = Image.fromarray(arr)
        info["tratamento"] = rel
        if retrato_saida:          # a foto inteira, com o fundo original, tratada (para o NX Fotos)
            al = arr[:, :, 3:4].astype(np.float32) / 255
            Image.fromarray((rgb * al + np.array(im) * (1 - al)).astype(np.uint8)).save(
                retrato_saida, "JPEG", quality=93)
            info["retrato"] = retrato_saida
        dep = rel.get("depois")
        if dep and not rel.get("claros_ja_certos") and not (PELE_L[0] - 8 <= dep[0] <= PELE_L[1] + 6):
            info["problemas"].append(f"rosto ainda {'escuro' if dep[0] < PELE_L[0] else 'claro'} (L {dep[0]}) depois do tratamento: confira")

    # Conferências: a pessoa tem de chegar à base, sem corte reto visível nas laterais
    base_y = oy + h * s
    toca_base = mask[-3:, :].any()
    if toca_base and H - 2 > base_y >= H * (1 - FOLGA):    # falta pouco: desce a pessoa
        oy += H - base_y; base_y = H
        info["ajuste"] = "pessoa descida para chegar à base"
    elif toca_base and base_y < H - 2 and AMPLIAR:          # foto fechada: a cabeça cresce
        b = h - queixo                                       # o mínimo para chegar à base
        c_min = (1 - TOPO) * cabeca / (b + cabeca) + 0.005
        s = c_min * H / cabeca
        ox = CENTRO_X * W - cx * s
        oy = TOPO * H - topo * s
        base_y = oy + h * s
        info["ajuste"] = f"foto fechada: cabeça em {c_min:.0%} da altura, acima do padrão de {CABECA:.0%}"
        info["problemas"].append("cabeça maior que o padrão (não há corpo para a cabeça de 50%)")
        info["escala"] = round(s, 2)
    esfumar_base = False
    if toca_base and base_y < H - 2 and not AMPLIAR:
        # foto recente fechada demais: a cabeça cresce no máximo até CABECA_MAX (diferença
        # quase imperceptível) e o que ainda faltar vira um esfumado do tronco para o fundo
        b = h - queixo
        c_min = (1 - TOPO) * cabeca / (b + cabeca) + 0.005
        c_use = min(c_min, CABECA_MAX)
        if c_use > CABECA:
            s = c_use * H / cabeca
            ox = CENTRO_X * W - cx * s
            oy = TOPO * H - topo * s
            base_y = oy + h * s
            info["escala"] = round(s, 2)
            info["ajuste"] = f"foto fechada: cabeça em {c_use:.0%} da altura"
        if H - 2 > base_y >= H * (1 - FOLGA):              # falta pouco: desce a pessoa
            oy += H - base_y; base_y = H
        if base_y < H - 2:
            esfumar_base = True
            info["ajuste_base"] = f"tronco esfumado para o fundo (a foto acaba {int(H - base_y)} px acima da base)"
            if H - base_y > 0.16 * H:
                info["problemas"].append(f"corpo curto demais: a foto acaba {int(H - base_y)} px acima da base mesmo com a cabeça em {c_use:.0%}; confira o esfumado ou troque a foto")
    elif toca_base and base_y < H - 2:
        info["problemas"].append(f"corpo curto: a foto acaba {int(H - base_y)} px acima da base")
    if not toca_base:
        info["problemas"].append("a pessoa não chega à borda de baixo da foto original")
    toca_esq = mask[:, :3].mean() > 0.02
    toca_dir = mask[:, -3:].mean() > 0.02
    esfuma = []
    if toca_esq and ox > 2:
        esfuma.append("esq")
        info["aviso_lateral_esq"] = f"ombro ou braço cortado pela foto original ({int(ox)} px da borda): esfumado"
    if toca_dir and ox + w * s < W - 2:
        esfuma.append("dir")
        info["aviso_lateral_dir"] = f"ombro ou braço cortado pela foto original ({int(W - (ox + w * s))} px da borda): esfumado"
    if esfuma:                       # o corte reto da foto vira um degradê para o fundo
        a_ = np.array(pessoa).astype(float)
        F = max(8, int(w * 0.10))
        rampa = np.linspace(0.0, 1.0, F)
        if "esq" in esfuma:
            a_[:, :F, 3] *= rampa[None, :]
        if "dir" in esfuma:
            a_[:, -F:, 3] *= rampa[::-1][None, :]
        pessoa = Image.fromarray(a_.clip(0, 255).astype(np.uint8))
        info["problemas"].append("corte lateral esfumado: confira se não ficou estranho; se ficar, troque a foto")
    if s > 2.2:
        info["problemas"].append(f"ampliação alta ({s:.1f}x): a foto vai perder nitidez")

    out = fundo_tema(fundo_p, altura).convert("RGBA")
    p2 = pessoa.resize((max(1, int(w * s + .5)), max(1, int(h * s + .5))), Image.LANCZOS)
    if esfumar_base:
        # o tronco some aos poucos e a base do fundo escurece em degradê: o corte da foto
        # original não aparece e a pessoa "assenta" na imagem
        a2 = np.array(p2).astype(np.float32)
        hh2 = a2.shape[0]
        qy = queixo * s                                  # queixo dentro da camada redimensionada
        ini = int(qy + 0.30 * (hh2 - qy))
        if hh2 - ini > 4:
            r = (1 - np.linspace(0.0, 1.0, hh2 - ini)) ** 1.4
            a2[ini:, :, 3] *= r[:, None]
        p2 = Image.fromarray(a2.clip(0, 255).astype(np.uint8))
        fa = np.array(out.convert("RGB")).astype(np.float32)
        y0 = int(max(0, oy + ini - 0.05 * H))
        g = np.ones(H, np.float32)
        g[y0:] = 1 - 0.55 * np.linspace(0, 1, H - y0) ** 1.2
        fa *= g[:, None, None]
        out = Image.fromarray(fa.clip(0, 255).astype(np.uint8)).convert("RGBA")
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    camada.paste(p2, (int(round(ox)), int(round(oy))))
    out.alpha_composite(camada)
    out = out.convert("RGB")
    out.save(sai, "JPEG", quality=92, optimize=True, progressive=True)
    info["saida"] = f"{W}x{H}"
    info["ok"] = not info["problemas"]
    if folha_saida:
        folha(out, folha_saida); info["folha"] = folha_saida
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

## 9. Publicação às 8h

1. Refaça a duplicidade (seção 11).
2. `criar_materia` → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar → foto no padrão de artigos (seção 8, "Foto destacada: padrão de artigos") → `definir_imagem_destacada` com a foto final.
3. `conferir_publicacao` (tipo agendar) → `publicar_no_wordpress` com `portais` ["1"], `quando` "DD/MM/AAAA 08:00" (hoje) e o `codigo_confirmacao` (decisão de publicação direta, padrão seção 2). Se a matéria só ficar pronta depois das 7h55, agende para o próximo horário de 15 em 15 minutos (8h15, 8h30…), sempre com pelo menos 5 minutos de folga: a folga é o tempo de barrar o story automático (seção 10.1). Erro 429: espere e repita.
4. Guarde o `materia_id` e o horário agendado.
5. Faça a seção 10.1 logo em seguida.
6. Espere até 2 minutos depois do horário agendado (`sleep` no Bash, em blocos de no máximo 9 minutos). Confirme que a matéria está no ar: `listar_publicacoes` com `portal` "1", `situacao` "publicado" e `busca` pelo título, e o link com o slug (não `?p=`). Guarde o link.
7. Se 10 minutos depois do horário ela ainda não estiver no ar, não faça o story: registre em Pendências com o que `listar_agendamentos` mostra.

## 10. Story para revisão (decisão de 02/11/2026)

O story precisa da revisão da Joviana e do Mário. **A rotina nunca aprova, agenda ou publica story:** não use `revisar_post_instagram` para aprovar nem `publicar_post_instagram`. Conta da marca: **ES Brasil = conta 7** (@revistaesbrasil).

### 10.1 Barrar o story automático (antes de a matéria ir ao ar)

Quando a matéria é agendada, o painel do NX Feed cria sozinho um story dela e o agenda para o horário da matéria. Ele sairia sem revisão.

1. Logo depois de agendar, `listar_posts_instagram` com `conta_id` 7, `tipo` "story", `filtro` "agendados", e depois `filtro` "aprovados". Fique só com os itens cujo `materia_id` é o da matéria do dia. O painel pode levar alguns minutos para criar o story: se não achar nada, espere 2 minutos e procure de novo, até 3 vezes.
2. Story automático agendado: `cancelar_agendamento_instagram` com o `post_id`. A rotina só pode cancelar o story automático **da matéria dela**; nunca mexa em outro conteúdo.
3. Story automático já publicado: não dá para desfazer. Registre em Pendências ("story automático saiu sem revisão") e não faça outro story.
4. Guarde o `post_id` do automático para a seção 10.2.

### 10.2 Montar o story e mandar para revisão (depois de a matéria ir ao ar)

Só depois da confirmação da seção 9 (padrão, seção 2.2). Siga o guia de arte da casa (`regras_de_arte` com a conta 7). Procure de novo o story automático, como em 10.1, e cancele o agendamento se ele tiver voltado a ter horário.

1. `criar_arte_de_noticia`, com `so_conferir` true antes, se precisar acertar as linhas:
   - **Com story automático** (cancelado ou parado em revisão): `post_id` do automático. A arte vira a versão seguinte dele e o conteúdo volta para "Para revisar". Assim fica um story só para a matéria.
   - **Sem story automático:** `materia_id`, `conta_id` 7, `formatos` ["story"], `criar_post` true e `etapa` "revisao".
   - **Título** (2 linhas, ~38 a 45 caracteres): o título do texto, reduzido sem mudar o sentido. Título em metáfora vira o tema dito com clareza, como pede o guia de arte.
   - **Subtítulo** (2 linhas, ~80 a 105 caracteres, termina com ponto): "Artigo de [Nome], publicado em [ano] na revista ES Brasil." Falecido: "Artigo de [Nome] (in memoriam), publicado em [ano]…" quando couber.
   - **Tag:** a tag da lista do guia que corresponde ao assunto (Artigos não vira tag).
   - **Foto:** a destacada (em 16:9, com o rosto no centro, o recorte vertical do story pega a pessoa). O guia proíbe imagem de IA na arte: se a destacada for IA, use outra foto real do tema; sem foto real, não faça o story e registre.
   - **Nota:** "Story do acervo de artigos para revisão da Joviana e do Mário Fernando. A matéria está no ar desde [DD/MM às HHh]. Ao aprovar, escolham o horário."
   - **Pedido:** "Story do artigo do acervo da ES Brasil, para revisão da Joviana e do Mário (rotina artigos-acervo-esbrasil)."
2. Confira com `ver_post_instagram` que o story está em revisão ("Para revisar"). O NX Feed avisa os revisores do Studio.
3. Se o `post_id` do automático recusar o ajuste, volte o automático para rascunho (`revisar_post_instagram` com `acao` "voltar_rascunho" e `nota` "Substituído pelo story do acervo de artigos, em revisão") e crie o story novo sem `post_id`.
4. Falha no story não desfaz a publicação: registre em Pendências.

## 11. Duplicidade e controle

A rotina se reconhece por três marcas: tag "Acervo de Artigos", chapéu com o nome do articulista (até 13/11/2026 era "ARTIGO") e a frase "É uma republicação do acervo de artigos da ES Brasil" no pé.

Antes de escrever e de novo antes de agendar:

1. **O que a rotina já fez:** `listar_materias` com `busca` "Acervo de Artigos" e com `autor` "Redação", `portal` 1, últimos 365 dias, formato compacto; confirme com `ver_materia`. Daí saem os textos já usados e a data do último uso de cada articulista. O mesmo texto original nunca é republicado duas vezes.
2. **Site, na NEIA:** `search-content` na fonte do site pelo título original e pelo tema com o nome do autor.
3. **Site, na web:** WebSearch `site:esbrasil.com.br "<título>"`.

Como decidir:

- O mesmo texto está no site há **menos de 2 anos**: troque de texto.
- Está no site há **mais de 2 anos**: siga com a republicação e liste o post antigo no resumo, em "Para tirar do ar" (link, id do post e link da versão nova). Nada é apagado por esta rotina.
- Rascunho ou matéria agendada da equipe com o mesmo texto: troque de texto.

## 12. Resumo e notificação

**Não envie e-mail.** Siga o padrão (seção 10), com o título "Artigos do acervo · **ES Brasil** · DD/MM" e estas seções:

- **Publicado:** título com link, articulista (vivo ou in memoriam), caminho (editoria Artigos ou seção 2.2, com o cabeçalho original), origem (edição ou post e data original, "data deduzida" quando for), categoria, nota de escolha, nota SEO, imagem (real, arquivo ou IA, e se ficou no padrão de artigos), se teve Nota de contexto, dados atualizados (antigo → atual, fonte e ano) e peça do NXtab.
- **Story para revisão (Joviana e Mário):** link do Studio, `post_id` e situação ("em revisão"); story automático cancelado ou não encontrado.
- **Rejeitados no dia:** título, articulista, edição e motivo (não entra, contexto, dados ou outro), uma linha cada.
- **Para tirar do ar:** versões antigas no site, quando houver.
- **Imagens de IA para validar**, quando houver.
- **Pendências:** cargo não confirmado, data deduzida, grafia em dúvida, articulista novo para a lista, story que falhou ou saiu sem revisão, cabeça maior que o padrão, foto fora do padrão.

Notificação do app Claude ao terminar.