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

Toda destacada com pessoa sai no mesmo padrão, seja qual for a foto de partida (estúdio, cena ou montagem antiga): **a pessoa recortada sobre uma foto do tema desfocada e em tons neutros (o fundo é sempre trocado), em 1600x900 (16:9), com a cabeça sempre do mesmo tamanho e na mesma altura**: do alto do cabelo ao queixo, metade da altura da imagem; o alto do cabelo a 7% do topo; o rosto no centro; o corte na altura dos braços. Substitui as regras de enquadramento e de fundo neutro de 13 e 14/11/2026: o fundo agora é trocado sempre, não só quando é neutro. Em 16:9, com o rosto no centro e a cabeça logo abaixo do topo, os cortes do tema dos sites (destaque grande 5:3, blocos de 70% e miniaturas quadradas) nunca pegam a cabeça.

**Decisões do Mário Fernando de 25 e 26/11/2026 (valem acima de tudo nesta seção):**
- **O rosto não se estraga.** Nunca escurece, nunca fica manchado, acinzentado, rosado ou magenta, e o tratamento nunca endurece a pele: a foto tem de sair mais bonita do que entrou. O script trava isso (o rosto nunca sai mais escuro do que entrou), clareia rosto abaixo do tom saudável, deixa a pele dourada (um pouco de amarelo), suaviza manchas e tira o aspecto "HDR" de rugas marcadas.
- **A pessoa vai inteira e por cima de tudo.** Nada de esfumado, degradê ou fundo passando por cima do corpo. Faltou corpo (foto fechada no peito, ombro ou braço cortado), a pessoa é reconstruída com o preenchimento generativo da Adobe (item 4).
- **Fundo com cara de foto, nunca "plantado":** em tons neutros (sem cor gritando, pouco contraste, luz clara e calma), com o horizonte na altura dos olhos, desfoque de lente e a mesma luz da pessoa. Quem tem cor e contraste é a pessoa, não o fundo.
- **Fundo ligado à atividade da pessoa e ao tema do artigo, nunca doméstico (sala, quarto ou cozinha de casa) e nunca repetido:** cada destacada tem um fundo próprio, inclusive dois artigos do mesmo articulista.

1. **A foto mais recente da pessoa (decisão do Mário Fernando, 16/11/2026).** Procure em todas as fontes e fique com a mais recente que sirva, pela data: o acervo WordPress da revista (no navegador, com o site aberto: `/wp-json/wp/v2/media?search=<sobrenome>&orderby=date&order=desc&per_page=30&_fields=date,source_url`; sem navegador, `buscar_imagens` com `fonte` "editoriais" e o nome, que traz a mesma biblioteca; o ano e o mês estão no caminho `wp-content/uploads/AAAA/MM`), o NX Fotos (pasta "Articulistas" e `buscar` pelo nome; campo `data`) e a destacada de posts antigos dele. As fotos de cdn.esbrasil.com.br e cdn.comunhao.com.br baixam direto pelo terminal. Fora: montagem antiga da rotina (nome terminado em "-HHMMSS.webp", fundo já desfocado) quando houver o original, arte com texto, foto de evento (palco, microfone, grupo) e foto com objeto ou outra pessoa encostada (carro, cadeira, haste de microfone, parede com sombra). Confira que é a mesma pessoa das fotos antigas. Prefira a que mostra peito e ombros; foto fechada no peito ainda serve (o corpo é reconstruído, item 4). Foto com o rosto estragado (mancha, pele acinzentada ou escurecida, montagem antiga já danificada) não serve, por mais recente que seja: use a mais recente que esteja limpa, mesmo que mais antiga.
2. **Fundo: um lugar ligado à atividade da pessoa e ao tema do artigo (decisões do Mário Fernando, 25 e 26/11/2026)**, no NX Fotos (`buscar`, `orientacao` "h", `tipo` "foto"). Comece pela atividade e afine pelo tema: empresário, gestor ou executivo → escritório ou sala de reunião; publicitário ou comunicador → agência ou escritório; jornalista → redação; advogado → escritório com estantes; médico → consultório ou hospital; professor ou pesquisador → sala de aula, universidade ou biblioteca; engenheiro ou industrial → fábrica ou obra; produtor rural → lavoura; pastor ou líder religioso → igreja por dentro; palestrante → auditório. O tema afina: ESG e meio ambiente → área verde ou parque; urbanismo e cidades → Centro de Vitória ou orla; economia e logística → porto; turismo → cartão-postal capixaba; educação → escola ou biblioteca. **Nunca ambiente doméstico** (sala, quarto ou cozinha de casa). **Foto feita na altura dos olhos** (de pé, câmera reta), de um lugar com profundidade (corredor, salão, nave, auditório), claro e de cores calmas: foto escura, de cor forte (verde intenso, laranja, roxo) ou cheia de detalhe fica feia mesmo neutralizada. Fora: foto aérea ou de drone, feita de cima, só céu, parede lisa, com texto, logotipo ou pessoa em primeiro plano, foto oculta (`visibilidade` "oculta", banco de imagem comprado), de outro veículo ou da Reuters. **Nunca repita um fundo:** antes de escolher, leia com `ver_materia` (`formato_texto` "nenhum") as destacadas das 30 últimas matérias desta rotina e da rotina irmã (`artigos-acervo-comunhao`); o id do fundo fica no fim do título da imagem ("· fundo <id>", item 6) e nenhum desses ids volta, nem para o mesmo articulista. Prefira a biblioteca dos fotógrafos da casa (Sidney Pagotto, Claudio Alves, Renato Cabrini e demais). Baixe a versão de 1600 px do CDN.
3. Grave o script abaixo como `padronizar_retrato.py` e rode `python3 padronizar_retrato.py foto.jpg fundo.jpg destacada.jpg --folha folha.jpg`. Ele recorta a pessoa (rembg; se faltar, `pip install --break-system-packages "rembg[cpu]" opencv-python-headless`), acha o rosto (YuNet), trata a foto, iguala a cabeça e monta o fundo como uma lente de retrato veria: ampliado (`--zoom`, padrão 1.5), com a linha do horizonte da foto do fundo na altura dos olhos da pessoa (`--horizonte`, padrão 0.5, o meio da foto; mude se o horizonte do fundo estiver em outro ponto), desfoque de lente, tons neutros, luz no nível da do rosto, o mesmo grão da pessoa, borda sem halo e a luz e a cor do lugar no contorno e na roupa. `--altura` (0 a 1) só para escolher a faixa do fundo à mão. **Tratamento (decisões do Mário Fernando, 16, 25 e 26/11/2026):** é medido no rosto de cada foto: rosto abaixo do tom saudável clareia; pele rosada, magenta, avermelhada ou alaranjada vai para um tom dourado e natural; a pele é suavizada (manchas e textura dura) sem perder olhos, boca e barba; foto com aspecto "HDR" perde parte do microcontraste; terno preto ganha detalhe; pele morena ou negra não é clareada à força. **O rosto nunca sai mais escuro do que entrou** (o script devolve a luz se algum passo a baixar). Nunca aplique ao retrato o tratamento quente das matérias (`padrao-publicacao-next` 9.3) nem o do NX Feed: a destacada sobe com `tratamento` "nao". **Foto já tratada (decisão do Mário Fernando de 25/11/2026):** antes, rode `python3 tratar_foto_next.py --verificar foto.jpg` (skill `tratamento-fotos-next`, com `--origem site` para foto do acervo WordPress). Se a foto já tem a marca da casa (inclusive a invisível), a palavra-chave `tratada-nx-v1` no NX Fotos ou foi editada pelo fotógrafo (Lightroom, Photoshop), rode o `padronizar_retrato.py` com `--sem-tratamento`: só recorte, fundo e cabeça. A destacada nova sai do script; a foto inteira tratada que vai para o NX Fotos (item 8) recebe depois a marca com `tratar_foto_next.py --tipo pessoas --sufixo`.
4. Leia o JSON. Com `ok` true, siga. Com problema:
   - **"reconstruir"** (nada foi gravado): a foto acaba antes do quadro (fechada no peito, ombro ou braço cortado, cabelo encostado no alto). A pessoa é reconstruída, nunca esfumada. Converta a foto para JPEG e suba para a Adobe: `adobe_mandatory_init`; `asset_initialize_file_upload` (`path` "nx-artigos/<arquivo>.jpg", `file_size`, `media_type` "image/jpeg"); `curl -L -X PUT -H "Content-Type: image/jpeg" --data-binary @arquivo.jpg "<href de transfer>"`; `asset_finalize_file_upload` com o `transfer_document` inteiro, como veio. Com o `presignedAssetUrl`, `image_generative_expand` com `expandPixels` = os números de "reconstruir" e `sessionId` "-1"; baixe o `outputUrl` com `curl -L` e rode o script de novo na foto estendida. Se ele pedir mais um lado, estenda de novo a saída anterior (o `outputUrl` em `imageURIs` e o mesmo `sessionId`). Olhe a emenda: roupa contínua, sem mão, braço ou objeto inventado. A descrição da foto ganha "e o paletó (ou a camisa) completado digitalmente".
   - Reconstrução falhou (Adobe fora do ar ou emenda ruim): troque pela foto mais recente que tenha corpo. Sem outra, `--aceitar-cabeca-maior` (a cabeça cresce até o corpo chegar à base, sem esfumado) e registre "cabeça maior que o padrão" em Pendências.
   - "tratamento": a pele do rosto antes e depois (L, a, b). O L depois nunca é menor que o antes; o b (amarelo) fica perto ou acima do a (vermelho). Pele morena ou negra pode fechar com L menor ("claros_ja_certos"): está certo.
   - "sem rosto detectado" ou "ampliação alta": troque a foto. Sem outra, mantenha a destacada que houver e registre "foto fora do padrão" em Pendências.
5. Olhe com Read a saída e a folha (cortes 5:3, 70% e quadrado): cabeça inteira, alto do cabelo logo abaixo do topo, recorte limpo, sem halo, sem pedaço do fundo antigo ou de objeto grudado na pessoa, sem orelha, óculos ou ombro comidos, sem fio ou haste grudado no ombro; **rosto mais bonito que o da foto original, nunca pior** (ponha os dois lado a lado: nem mais escuro, nem manchado, nem acinzentado, nem rosado ou magenta, nem duro); terno com detalhe, não um bloco preto; corpo inteiro até a base, nada passando por cima dele; **a pessoa dentro do lugar e não colada nele** (mesma luz, mesmo ar); fundo neutro, que não grita nem apaga a pessoa, com o horizonte na altura dos olhos e o lugar reconhecível. Com defeito, troque a foto ou o fundo e rode de novo.
6. Suba com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `materia_id`) e `curl -T`, e grave a URL que o envio devolve com `definir_imagem_destacada` (`tratamento` "nao"). O link de envio é de uso único: não mostre nem guarde. Campos: título "<Nome>, articulista da ES Brasil · fundo <id do fundo no NX Fotos>" (o id é o controle para nunca repetir o fundo, item 2); fonte, a da foto da pessoa; autor "<crédito da foto da pessoa>; fundo: <autor do fundo>/NX Fotos" (fundo sem autor no NX Fotos: "fundo: NX Fotos"); descrição "<Nome>, autor do artigo[, em <ano da foto>]; foto de arquivo, em montagem com fundo ilustrativo de <cena>[ e o paletó completado digitalmente]"; legenda (alt) com o que se vê, terminando no lugar (ex.: "num escritório desfocado com divisórias de vidro").
7. Vale para toda foto de pessoa na destacada (articulista ou personagem do título). Foto de tema sem pessoa e imagem de IA (gerada em 16:9) não passam pelo script.
8. **Foto nova vai para o NX Fotos.** Quando a foto da pessoa veio do acervo WordPress e ainda não está no NX Fotos, rode o script também com `--retrato retrato.jpg` (a foto inteira, com o fundo original, tratada) e salve-a na pasta "Articulistas" do NX Fotos (id 1450): no navegador, Gerenciador de Mídia (nxfotos.com.br/admin/midia), arquivo no campo de envio (`file_upload`) e "Enviar"; depois `listar_biblioteca` (texto: o nome do arquivo) para achar o `mediaId`, `editar_midia` (título "<Nome>, articulista da ES Brasil (<ano>)", autor "Arquivo ES Brasil", descrição com roupa e ano, palavras-chave com nome, articulista, revista e retrato, e a URL de origem em notas) e `mover_para_pasta` com a pasta 1450. Sem navegador na sessão, registre em Pendências "foto nova de <Nome> para o NX Fotos: <URL>".

```python
#!/usr/bin/env python3
"""Padrão de foto dos artigos: recorta o articulista, troca sempre o fundo e iguala a cabeça.

Decisões do Mário Fernando (16/11/2026): toda destacada de artigo sai no mesmo padrão,
seja qual for a foto de partida (estúdio, cena, montagem antiga):
  - a foto mais recente do articulista que esteja boa (acervo WordPress das revistas, NX Fotos);
  - a pessoa recortada (rembg) sobre uma foto do tema desfocada (o fundo é sempre trocado);
  - 1600x900 (16:9);
  - a cabeça sempre do mesmo tamanho e na mesma altura: do alto do cabelo ao queixo = 50%
    da altura; alto do cabelo a 7% do topo; rosto no centro; corte na altura dos braços.

Decisões do Mário Fernando (25 e 26/11/2026):
  - a pessoa vai inteira e por cima de tudo. Nada de esfumado, degradê ou fundo passando por
    cima do tronco, dos ombros ou dos braços. O recorte sai sólido por dentro, só a borda macia.
    Quando a foto acaba antes da base ou corta um ombro ou braço dentro do quadro, a pessoa é
    reconstruída: o script não monta a imagem e devolve "reconstruir" com quantos pixels faltam
    em cada lado; a rotina estende a foto com o preenchimento generativo da Adobe
    (image_generative_expand) e roda o script de novo sobre a foto estendida;
  - o rosto não se estraga ("não pode matar a imagem do personagem"; "a foto tem que ser mais
    bonita e bem tratada"): nunca sai mais escuro do que entrou, nunca manchado, acinzentado,
    rosado ou magenta, nunca com a pele endurecida. O tratamento clareia rosto abaixo do tom
    saudável, deixa a pele dourada (um pouco de amarelo), suaviza manchas e textura dura e tira
    parte do aspecto "HDR" (rugas marcadas, luz dura);
  - o fundo não pode parecer "plantado" nem gritar: entra ampliado como numa lente de retrato,
    com o horizonte na altura dos olhos da pessoa, desfoque de lente (bokeh), em tons neutros
    (pouca cor, pouco contraste, luz clara e calma, no nível da luz do rosto), com o mesmo grão
    da pessoa, borda sem halo, a luz do lugar no contorno e a cor e o ar do lugar no corpo.
    Quem tem cor e contraste é a pessoa.

Uso:
  python3 padronizar_retrato.py foto.jpg fundo.jpg saida.jpg [--folha folha.jpg]
  fundo.jpg: foto do tema (NX Fotos, horizontal, feita na altura dos olhos). "cinza" só para testar.
  --horizonte f: onde está a linha do horizonte na foto do fundo (0 = topo, 1 = base; padrão
    0.5, o centro, que é onde fica numa foto feita em pé e reta). O script põe essa linha na
    altura dos olhos da pessoa.
  --zoom z: quanto o fundo entra ampliado (padrão 1.5): de perto, o ambiente aparece grande.
  --altura a: ignora o horizonte e escolhe à mão a faixa do fundo (0 alto, 1 baixo).
  --desfoque N: raio do desfoque de lente, em px. Sem ele: automático (foto do fundo já
    desfocada leva 16 px; nítida, 25 px): fora de foco, mas o lugar continua reconhecível.
  --aceitar-cabeca-maior: último recurso, só quando a reconstrução falhar: a cabeça cresce o
    necessário para o corpo chegar à base (o alto da cabeça continua a 7%). Nunca esfuma.
  --sem-tratamento: só para foto que já veio tratada.
  --retrato r.jpg: grava também a foto inteira, com o fundo original (para o NX Fotos).
Imprime um JSON. "reconstruir" ({"bottom", "left", "right"} em pixels da foto de entrada)
quer dizer que nada foi gravado: estenda a foto e rode de novo. "tratamento" traz a pele do
rosto antes e depois (L, a, b do Lab de 8 bits); o L depois nunca é menor que o antes.
"ok": false lista os problemas (ampliação alta, sem rosto, rosto ainda escuro, recorte com
buraco): confira a saída e, se ficar ruim, escolha outra foto do articulista.
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
TRATAR = True    # tratamento adaptativo do retrato (--sem-tratamento desliga)
DESFOQUE = None  # --desfoque N: raio do desfoque do fundo em px (padrão: automático)
MARGEM_EXPANSAO = 1.15  # pede 15% a mais de foto do que falta, para a emenda ficar fora do quadro
ZOOM_FUNDO = 1.5   # --zoom: o fundo entra ampliado (efeito de teleobjetiva: de perto, o ambiente é grande)
FUNDO_SAT = 0.40        # o fundo fica com 40% da saturação: tons neutros, a pessoa se destaca
FUNDO_CONTRASTE = 0.72  # contraste do fundo suavizado
FUNDO_LUZ = 150         # luz média do fundo (Lab): meio-tom claro e calmo, nem escuro nem estourado
HORIZONTE = 0.5    # --horizonte: onde fica a linha do horizonte na foto do fundo (0.5 = foto feita na altura dos olhos)


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


def solidificar(alfa, rgb):
    """A pessoa sai sólida: buracos de dentro do recorte (paletó escuro, gola, cabelo) são
    fechados e tudo o que fica a mais de 3 px da borda vai a 255. Só a borda externa continua
    macia, para não ficar serrilhada. Assim o fundo nunca aparece através do corpo nem por
    cima dele. Vão de verdade entre braço e corpo (da cor do fundo antigo e grande) fica vazio."""
    import cv2
    bin_ = (alfa > 128).astype(np.uint8)
    hh, ww = bin_.shape
    k = max(5, int(min(hh, ww) * 0.012)) | 1
    fechado = cv2.morphologyEx(bin_, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    inv = (1 - fechado).astype(np.uint8)
    n, lab = cv2.connectedComponents(inv, 4)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])).tolist())
    fundo_antigo = (alfa < 20)
    cor_fundo = np.median(rgb[fundo_antigo], axis=0) if fundo_antigo.sum() > 100 else None
    buracos = np.zeros_like(bin_, dtype=bool)
    for i in range(1, n):
        if i in borda:
            continue                       # liga-se à borda: é fundo de verdade
        comp = lab == i
        area = int(comp.sum())
        if area < 0.002 * hh * ww:
            buracos |= comp                # buraco pequeno: é a pessoa
        elif cor_fundo is not None and np.linalg.norm(rgb[comp].mean(axis=0) - cor_fundo) > 30:
            buracos |= comp                # buraco grande mas com cor de roupa: é a pessoa
    cheio = (fechado.astype(bool) | buracos).astype(np.uint8)
    dist = cv2.distanceTransform(cheio, cv2.DIST_L2, 3)
    out = alfa.astype(np.float32)
    out[cheio.astype(bool) & (dist > 3)] = 255
    out[buracos] = 255
    return out.clip(0, 255).astype(np.uint8), int(buracos.sum())


PELE_L = (158, 184)   # luminância do rosto (Lab 8 bits do OpenCV): abaixo é escuro, acima estoura
ROSTO_MIN, ROSTO_ALVO = 168, 174   # rosto abaixo de 168 clareia até 174 (tom saudável); nunca escurece
SUAVIZAR = 0.55   # quanto da pele é suavizada (manchas e textura dura); olhos, boca e barba ficam
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
    1) exposição: rosto abaixo de L 168 clareia até 174 (tom saudável); nunca escurece;
    2) sombras: terno preto 'empapado' ganha um pouco de detalhe (só o corpo, nunca o rosto);
    3) cor: dominante geral pelos brancos da roupa; pele avermelhada/alaranjada volta ao tom natural;
    4) sem contraste local e sem nitidez (marcam rugas e manchas);
    5) pele suavizada com filtro que respeita contornos: some mancha e textura dura, fica a pessoa.
    O tratamento quente e saturado das matérias (padrao-publicacao-next 9.3) não vale para rosto."""
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
    if lf < ROSTO_MIN:
        alvo = ROSTO_ALVO
    # rosto claro nunca é escurecido (decisão do Mário Fernando, 25/11/2026: escurecer o
    # rosto "mata" o personagem e deixa a pele acinzentada, com cara de doente)
    p98 = float(np.percentile(L[mask], 98)) if mask.any() else 255
    if alvo and alvo > lf and p98 >= 235:
        # os claros da foto já estão certos (camisa branca bem exposta): o rosto escuro é
        # sombra ou pele morena/negra; clareia com moderação, sem "embranquecer" a pele
        alvo = min(alvo, lf + 18)
        gmin = 0.75
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
        if preto > 0.30:
            lift = 8 + 6 * min(1.0, (preto - 0.30) / 0.4)
            x = np.clip(1 - L / 110, 0, 1) * corpo
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

    # 3b) pele: tom quente e natural, nunca magenta nem rosado (decisão do Mário Fernando,
    #     26/11/2026: "tem que ter um pouco de amarelo"). O b (amarelo) fica pelo menos no nível
    #     do a (vermelho) + 2; o a passa no máximo de 17. Só os tons parecidos com a pele mexem.
    agora = medir_pele(np.dstack([L, A, B]), rosto, mask)
    if agora:
        _, ca, cb = agora
        alvo_a = min(max(ca, 11.0), PELE_A + 3)
        alvo_b = max(PELE_B, min(22.0, ca + 2))
        sa = (alvo_a - ca) * 0.8 if ca > alvo_a else 0.0
        sb = (alvo_b - cb) * 0.75 if cb < alvo_b else ((24 - cb) * 0.8 if cb > 26 else 0.0)
        if abs(sa) > 0.4 or abs(sb) > 0.4:
            d2 = (A - 128 - ca) ** 2 + (B - 128 - cb) ** 2
            peso = np.exp(-d2 / (2 * 14.0 ** 2)) * mask
            A += sa * peso; B += sb * peso
            rel["passos"].append(f"pele a{sa:+.1f} b{sb:+.1f}")
        elif np.hypot(ca, cb) < 12:      # rosto acinzentado: devolve um pouco de cor
            f = min(1.25, 16 / max(np.hypot(ca, cb), 1))
            peso = mask.astype(np.float32)
            A[:] = 128 + (A - 128) * (1 + (f - 1) * peso); B[:] = 128 + (B - 128) * (1 + (f - 1) * peso)
            rel["passos"].append(f"cor da pele x{f:.2f}")

    # 4) nunca contraste local a mais (o CLAHE marcava rugas e deixava a pele dura, com aspecto
    #    de doente: pedido do Mário Fernando, 25/11/2026). Ao contrário: foto que veio com cara de
    #    "HDR" (rugas e manchas marcadas, luz dura) perde parte desse microcontraste, para a pessoa
    #    ficar macia e entrar na luz do lugar (26/11/2026). Contornos, olhos e cabelo ficam.
    if mask.any():
        base = cv2.GaussianBlur(L, (0, 0), max(2.0, fw * 0.035))
        det = L - base
        hdr = float(np.std(det[mask]))
        if hdr > 6:
            k_ = float(np.clip((hdr - 6) / 10, 0, 1)) * 0.35
            L[:] = np.where(mask, base + det * (1 - k_), L)
            rel["passos"].append(f"menos aspecto HDR ({k_:.0%})")

    # trava (decisão do Mário Fernando, 25 e 26/11/2026): o rosto nunca sai mais escuro do que
    # entrou (nem do que o alvo, quando foi clareado). Se algum passo baixou a luz, ela volta.
    piso = max(antes[0], alvo if alvo else 0)
    agora_l = medir_pele(np.dstack([L, A, B]), rosto, mask)
    if agora_l and agora_l[0] < piso - 0.5:
        g = float(np.clip(np.log(piso / 255) / np.log(max(agora_l[0], 20) / 255), 0.6, 1.0))
        L[:] = np.where(mask, 255 * (np.clip(L, 0, 255) / 255) ** g, L)
        rel["passos"].append(f"luz do rosto devolvida (gamma {g:.2f})")

    lab = np.dstack([np.clip(L, 0, 255), np.clip(A, 0, 255), np.clip(B, 0, 255)]).astype(np.uint8)
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # 5) pele mais bonita (decisão do Mário Fernando, 25/11/2026: "não pode manchar o rosto nem
    #    embrutecer o tratamento; a foto tem que ser mais bonita"): suaviza manchas e a textura
    #    dura só nos tons de pele do rosto e do pescoço, com filtro que respeita contornos.
    #    Olhos, sobrancelhas, boca, barba, cabelo e óculos ficam como estão.
    ref = medir_pele(lab.astype(np.float32), rosto, mask)
    if ref and SUAVIZAR > 0:
        Lr, ar, br = ref
        lab_f = lab.astype(np.float32)
        dcor = np.hypot(lab_f[..., 1] - 128 - ar, lab_f[..., 2] - 128 - br)
        hh, ww = mask.shape
        zona = np.zeros_like(mask)
        zona[max(0, int(fy - 0.5 * fh)):min(hh, int(fy + 1.9 * fh)),
             max(0, int(fx - 0.35 * fw)):min(ww, int(fx + 1.35 * fw))] = True
        pele = mask & zona & (dcor < 11) & (np.abs(lab_f[..., 0] - Lr) < 38)
        k = max(3, int(fw * 0.02)) | 1
        pele = cv2.morphologyEx(pele.astype(np.uint8), cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
        peso = cv2.GaussianBlur(pele.astype(np.float32), (0, 0), max(1.5, fw * 0.012)) * SUAVIZAR
        lisa = cv2.bilateralFilter(out, 0, 24, max(3.0, fw * 0.018))
        lisa = cv2.bilateralFilter(lisa, 0, 16, max(2.0, fw * 0.01))
        out = (out.astype(np.float32) * (1 - peso[..., None]) + lisa.astype(np.float32) * peso[..., None])
        out = np.clip(out + 0.5, 0, 255).astype(np.uint8)
        rel["passos"].append(f"pele suavizada ({int(pele.sum())} px)")
    # a mesma trava no fim: o rosto que sai nunca é mais escuro do que o que entrou
    lab_o = cv2.cvtColor(out, cv2.COLOR_RGB2LAB).astype(np.float32)
    fim_l = medir_pele(lab_o, rosto, mask)
    if fim_l and fim_l[0] < piso - 0.3:
        g = float(np.clip(np.log(piso / 255) / np.log(max(fim_l[0], 20) / 255), 0.6, 1.0))
        lab_o[..., 0] = np.where(mask, 255 * (lab_o[..., 0] / 255) ** g, lab_o[..., 0])
        out = cv2.cvtColor(np.clip(lab_o, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    depois = medir_pele(cv2.cvtColor(out, cv2.COLOR_RGB2LAB).astype(np.float32), rosto, mask)
    rel["depois"] = [round(v) for v in depois] if depois else None
    return out, rel


def desfoque_lente(arr, raio):
    """Desfoque de lente (bokeh), não gaussiano: disco feito em luz linear, como numa objetiva
    aberta. Luzes viram círculos, as bordas do ambiente continuam legíveis. O gaussiano deixa
    tudo "lavado" e é uma das coisas que entregam a montagem."""
    import cv2
    r = max(1, int(round(raio)))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    d = np.sqrt(xx ** 2 + yy ** 2)
    k = np.clip(r + 0.5 - d, 0, 1).astype(np.float32)
    k /= k.sum()
    lin = (arr.astype(np.float32) / 255) ** 2.2
    lin = cv2.filter2D(lin, -1, k, borderType=cv2.BORDER_REFLECT)
    return (np.clip(lin, 0, 1) ** (1 / 2.2) * 255).astype(np.float32)


def fundo_tema(caminho, altura, olho, luz=None):
    """Monta o fundo como uma lente veria atrás de um retrato de perto (decisão do Mário
    Fernando, 25/11/2026: o fundo não pode parecer "plantado"):
      - ampliado (ZOOM_FUNDO): de perto, o ambiente aparece grande e fechado, não a sala inteira;
      - o horizonte da foto do fundo na altura dos olhos da pessoa (câmera e fundo no mesmo nível);
      - desfoque de lente, não gaussiano."""
    import cv2
    if caminho == "cinza":
        return np.full((H, W, 3), (128, 132, 136), np.float32)
    t = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    bw, bh = t.size
    if bw / bh >= W / H:
        ch = bh; cw = bh * W / H
    else:
        cw = bw; ch = bw * H / W
    cw, ch = cw / ZOOM_FUNDO, ch / ZOOM_FUNDO
    x0 = (bw - cw) / 2
    if altura is not None:
        y0 = (bh - ch) * altura
    else:
        y0 = HORIZONTE * bh - olho * ch
    y0 = min(max(0.0, y0), bh - ch)
    t = t.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    arr = np.array(t)
    nitidez = float(cv2.Laplacian(cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var())
    raio = DESFOQUE if DESFOQUE is not None else (W / 100 if nitidez < 60 else W / 64)
    out = desfoque_lente(arr, raio)
    return neutralizar(out, luz)


def neutralizar(fundo, luz=None):
    """Fundo em tons neutros (decisão do Mário Fernando, 25/11/2026): o lugar continua
    reconhecível, mas não grita nem apaga a pessoa. Tira a dominante de cor (o verde forte, o
    laranja), baixa a saturação, suaviza o contraste e leva a luz para um meio-tom claro e
    calmo, com um leve calor. Quem tem cor e contraste é a pessoa, não o fundo."""
    import cv2
    lab = cv2.cvtColor(np.clip(fundo, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    ma, mb = float(A.mean() - 128), float(B.mean() - 128)
    A[:] = 128 + (A - 128 - 0.8 * ma) * FUNDO_SAT + 1.0
    B[:] = 128 + (B - 128 - 0.8 * mb) * FUNDO_SAT + 4.0
    Lm = float(L.mean())
    L[:] = Lm + (L - Lm) * FUNDO_CONTRASTE
    # a luz do lugar é a mesma que bate na pessoa (decisão de 26/11/2026: a pessoa não pode
    # parecer "fora do ambiente"): o fundo fica um pouco abaixo da luz do rosto
    alvo = FUNDO_LUZ if luz is None else float(np.clip(luz - 16, 138, 162))
    L[:] = L + float(np.clip(alvo - Lm, -20, 30)) * 0.85
    lab = np.dstack([np.clip(L, 0, 255), np.clip(A, 0, 255), np.clip(B, 0, 255)]).astype(np.uint8)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32)


def harmonizar(camada, fundo, info, rosto_out=None):
    """Casa a pessoa com o ambiente, como se as duas coisas estivessem na mesma foto:
      - borda limpa: a cor do fundo antigo que ficou presa no contorno é trocada pela cor da
        própria pessoa (é o "halo" que denuncia o recorte);
      - borda de lente: o contorno fica levemente macio, como o resto da foto;
      - cor do ambiente: só a roupa recebe um toque da cor do lugar; o rosto e o brilho da
        pessoa não mudam nunca;
      - luz que contorna: a claridade do fundo invade de leve a borda do corpo (light wrap)."""
    import cv2
    rgb = camada[:, :, :3].astype(np.float32)
    al = camada[:, :, 3].astype(np.float32) / 255
    dentro = (al > 0.98).astype(np.float32)
    if dentro.sum() < 100:
        return camada
    # 1) borda limpa
    k = max(5, int(H * 0.012)) | 1
    num = cv2.GaussianBlur(rgb * dentro[..., None], (k, k), 0)
    den = cv2.GaussianBlur(dentro, (k, k), 0)[..., None]
    estimado = num / np.maximum(den, 1e-4)
    borda = ((al > 0.01) & (al <= 0.98) & (den[..., 0] > 0.02))[..., None]
    rgb = np.where(borda, estimado, rgb)
    # 2) borda de lente
    al = cv2.GaussianBlur(al, (0, 0), 1.2)
    # 3) luz do ambiente (no Lab): leva a pessoa um pouco na direção da cor e do brilho do lugar
    amb = cv2.GaussianBlur(fundo, (0, 0), W / 10)
    lab_p = cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    lab_a = cv2.cvtColor(np.clip(amb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    m = al > 0.5
    media_p = lab_p[m].mean(axis=0)
    # o rosto não muda de brilho nem de cor aqui (decisão de 25/11/2026: nada de escurecer
    # nem tingir o rosto). Só a roupa recebe um toque da cor do lugar.
    fora_rosto = np.ones((H, W), np.float32)
    if rosto_out is not None:
        cx, cy, rx, ry = rosto_out
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        e = ((xx - cx) / (rx * 1.6)) ** 2 + ((yy - cy) / (ry * 1.5)) ** 2
        fora_rosto = np.clip((e - 1) / 0.8, 0, 1)
    lab_p[..., 1] += np.clip(0.10 * (lab_a[..., 1] - media_p[1]), -4, 4) * fora_rosto
    lab_p[..., 2] += np.clip(0.10 * (lab_a[..., 2] - media_p[2]), -4, 4) * fora_rosto
    rgb_novo = cv2.cvtColor(np.clip(lab_p, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    rgb = rgb + (rgb_novo - rgb) * fora_rosto[..., None]      # no rosto, nem o arredondamento do Lab
    # 3b) luz do ambiente no corpo (decisão de 26/11/2026: a pessoa não pode parecer "fora do
    #     ambiente"): o preto da roupa sobe até perto do preto do lugar (fundo claro e calmo não
    #     tem preto chapado) e as sombras do corpo pegam um pouco da cor do lugar. Rosto intacto.
    lab_r = cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    lab_f = cv2.cvtColor(np.clip(fundo, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    corpo = (al > 0.5) & (fora_rosto > 0.5)
    if corpo.sum() > 1000:
        p_f = float(np.percentile(lab_f[..., 0], 4)); p_c = float(np.percentile(lab_r[..., 0][corpo], 4))
        sombra = np.clip(1 - lab_r[..., 0] / 115, 0, 1) ** 1.5 * fora_rosto
        if p_f > p_c + 4:
            lab_r[..., 0] += (p_f - p_c) * 0.55 * sombra
        mf = lab_f.reshape(-1, 3).mean(axis=0)
        lab_r[..., 1] += (mf[1] - lab_r[..., 1]) * 0.25 * sombra
        lab_r[..., 2] += (mf[2] - lab_r[..., 2]) * 0.25 * sombra
        # roupa sem o "HDR" da foto de origem: menos microcontraste e um pouco menos de cor,
        # como tudo o que está no mesmo ar do lugar
        Lc = lab_r[..., 0]
        base = cv2.GaussianBlur(Lc, (0, 0), 6)
        lab_r[..., 0] = base + (Lc - base) * (1 - 0.25 * fora_rosto)
        lab_r[..., 1] = 128 + (lab_r[..., 1] - 128) * (1 - 0.15 * fora_rosto)
        lab_r[..., 2] = 128 + (lab_r[..., 2] - 128) * (1 - 0.15 * fora_rosto)
        # a luz do lugar vem de um lado: o corpo acompanha, de leve (só o corpo)
        faixa = lab_f[int(H * 0.45):int(H * 0.85), :, 0]
        esq, dir_ = float(faixa[:, :W // 3].mean()), float(faixa[:, -W // 3:].mean())
        g = float(np.clip((dir_ - esq) / 2.5, -8, 8))
        xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
        lab_r[..., 0] += g * xx * fora_rosto
        rgb_novo = cv2.cvtColor(np.clip(lab_r, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
        rgb = rgb + (rgb_novo - rgb) * fora_rosto[..., None]
        info["luz_do_lugar"] = f"preto do corpo +{max(0.0, (p_f - p_c) * 0.55):.0f}, luz lateral {g:+.1f}"
    dL = 0.0
    # 4) luz que contorna
    R = H * 0.022
    dist = cv2.distanceTransform((al > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    peso = np.clip(1 - dist / R, 0, 1) ** 1.6 * 0.30
    luz = cv2.GaussianBlur(fundo, (0, 0), R * 0.8)
    tela = 255 - (255 - rgb) * (255 - luz) / 255           # modo "tela": só clareia
    rgb = rgb * (1 - peso[..., None]) + (0.5 * tela + 0.5 * luz) * peso[..., None]
    info["harmonizacao"] = "rosto intacto; roupa com 10% da cor do lugar; contorno com luz do fundo"
    return np.dstack([np.clip(rgb, 0, 255), al * 255])


def acabamento(img, grao):
    """A foto inteira recebe o mesmo acabamento: o mesmo grão por cima de tudo (fundo desfocado
    sem grão parece plástico), um véu de ar leve, um toque de amarelo (calor) e uma vinheta
    leve de lente."""
    hh, ww = img.shape[:2]
    rng = np.random.default_rng(7)
    ruido = rng.normal(0, grao, (hh, ww)).astype(np.float32)
    import cv2
    ruido = cv2.GaussianBlur(ruido, (0, 0), 0.6) * 1.6
    img = img + ruido[..., None]
    # a mesma luz para tudo: um véu de ar bem leve (3%) e um toque de amarelo na foto inteira
    veu = cv2.GaussianBlur(img, (0, 0), ww / 60)
    img = img * 0.97 + veu * 0.03
    lab = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 1] -= 0.6; lab[..., 2] += 2.5
    img = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    r = np.sqrt(((xx - ww / 2) / (ww / 2)) ** 2 + ((yy - hh / 2) / (hh / 2)) ** 2) / np.sqrt(2)
    img = img * (1 - 0.06 * r ** 2.4)[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)


def grao_da_pessoa(rgb, mask):
    """Mede o grão da pessoa (ruído fino nas áreas lisas) para o fundo receber o mesmo."""
    import cv2
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    hp = g - cv2.GaussianBlur(g, (0, 0), 1.5)
    liso = mask & (np.abs(cv2.Laplacian(cv2.GaussianBlur(g, (0, 0), 3), cv2.CV_32F)) < 1.0)
    if liso.sum() < 500:
        return 1.4
    return float(np.clip(0.6 * np.std(hp[liso]), 0.8, 2.2))


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
    global AMPLIAR, TRATAR, DESFOQUE, ZOOM_FUNDO, HORIZONTE
    altura, folha_saida = None, None
    if "--zoom" in a:
        i = a.index("--zoom"); ZOOM_FUNDO = float(a[i + 1]); del a[i:i + 2]
    if "--horizonte" in a:
        i = a.index("--horizonte"); HORIZONTE = float(a[i + 1]); del a[i:i + 2]
    if "--desfoque" in a:
        i = a.index("--desfoque"); DESFOQUE = float(a[i + 1]); del a[i:i + 2]
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

    arr = np.array(pessoa)            # a pessoa sólida por dentro: o fundo nunca passa por ela
    arr[:, :, 3], buracos = solidificar(arr[:, :, 3], np.array(im))
    pessoa = Image.fromarray(arr)
    mask = arr[:, :, 3] > 128
    if buracos:
        info["recorte"] = f"{buracos} px de buracos fechados dentro da pessoa"

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

    # Conferências (decisão do Mário Fernando, 25/11/2026): a pessoa vai inteira e por cima.
    # Nada de esfumar tronco ou ombro: o que falta de corpo é reconstruído na foto original.
    base_y = oy + h * s
    toca_base = mask[-3:, :].any()
    if toca_base and H - 2 > base_y >= H * (1 - FOLGA):    # falta pouco: desce a pessoa
        oy += H - base_y; base_y = H
        info["ajuste"] = "pessoa descida para chegar à base"
    if toca_base and base_y < H - 2 and AMPLIAR:          # último recurso: a cabeça cresce
        b = h - queixo                                       # o mínimo para chegar à base
        c_min = (1 - TOPO) * cabeca / (b + cabeca) + 0.005
        s = c_min * H / cabeca
        ox = CENTRO_X * W - cx * s
        oy = TOPO * H - topo * s
        base_y = oy + h * s
        info["ajuste"] = f"reconstrução indisponível: cabeça em {c_min:.0%} da altura, acima do padrão de {CABECA:.0%}"
        info["problemas"].append("cabeça maior que o padrão (a reconstrução do corpo falhou)")
        info["escala"] = round(s, 2)
    if not toca_base:
        info["problemas"].append("a pessoa não chega à borda de baixo da foto original: confira se o corpo não termina dentro do quadro")
    faltas = {}
    if toca_base and base_y < H - 2:
        faltas["bottom"] = (H - base_y) / s
    col0, col1 = (max(0, int(cx - 0.6 * cabeca)), min(w, int(cx + 0.6 * cabeca)))
    if mask[:2, col0:col1].any() and topo <= 2:            # o cabelo encosta no alto da foto
        faltas["top"] = 0.10 * cabeca
    if mask[:, :3].mean() > 0.02 and ox > 2:
        faltas["left"] = ox / s
    if mask[:, -3:].mean() > 0.02 and ox + w * s < W - 2:
        faltas["right"] = (W - (ox + w * s)) / s
    if not AMPLIAR:
        faltas = {k: int(np.ceil(v * MARGEM_EXPANSAO)) + 8 for k, v in faltas.items() if v > 2}
        if faltas:
            info["reconstruir"] = faltas
            info["como"] = ("a foto acaba antes do quadro (corpo, ombro ou cabelo cortados): estenda a foto "
                            "original com image_generative_expand (Adobe), expandPixels = reconstruir, e rode "
                            "o script de novo na foto estendida. Nada foi gravado.")
            info["ok"] = False
            print(json.dumps(info, ensure_ascii=False))
            sys.exit(3)
    if s > 2.2:
        info["problemas"].append(f"ampliação alta ({s:.1f}x): a foto vai perder nitidez")

    olho = ((oy + s * (rosto[1] + 0.40 * rosto[3])) / H) if rosto else (TOPO + 0.22)
    luz_rosto = (info.get("tratamento") or {}).get("depois") or (info.get("tratamento") or {}).get("antes")
    fundo = fundo_tema(fundo_p, altura, olho, luz_rosto[0] if luz_rosto else None)
    p2 = pessoa.resize((max(1, int(w * s + .5)), max(1, int(h * s + .5))), Image.LANCZOS)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    camada.paste(p2, (int(round(ox)), int(round(oy))))
    camada = np.array(camada).astype(np.float32)
    grao = grao_da_pessoa(camada[:, :, :3].astype(np.uint8), camada[:, :, 3] > 250)
    rosto_out = None
    if rosto:
        rosto_out = (ox + s * (rosto[0] + rosto[2] / 2), oy + s * (rosto[1] + rosto[3] / 2),
                     s * rosto[2] / 2, s * rosto[3] / 2)
    if fundo_p != "cinza":
        camada = harmonizar(camada, fundo, info, rosto_out)
    al = camada[:, :, 3:4] / 255
    comp = camada[:, :, :3] * al + fundo * (1 - al)
    # o grão que falta no fundo (o desfoque tirou) entra só no fundo; o acabamento vale para tudo
    rng = np.random.default_rng(3)
    comp = comp + (rng.normal(0, grao, (H, W)).astype(np.float32) * (1 - al[..., 0]))[..., None]
    out = Image.fromarray(acabamento(comp, 0.5))
    info["grao"] = round(grao, 1)
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