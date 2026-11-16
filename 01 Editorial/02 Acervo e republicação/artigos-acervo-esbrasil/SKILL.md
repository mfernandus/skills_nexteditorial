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

1. **Foto da pessoa, com corpo.** No NX Fotos (pelo nome do articulista), escolha uma foto em que apareçam o peito e os ombros, e baixe a original (`link_do_original`) ou a versão de 1600 px do CDN. Retrato fechado, com a cabeça ocupando quase a foto toda, não serve: para a cabeça ficar com metade da altura, o corpo tem de descer até a base. Montagem antiga da rotina também serve de fonte, se tiver corpo. Foto com objeto ou outra pessoa encostada (carro, cadeira, parede pintada com sombra) dá recorte sujo: prefira outra.
2. **Fundo do tema, no NX Fotos** (`buscar`, `orientacao` "h", `tipo` "foto"): foto real, horizontal, ligada ao tema do artigo. Exemplos: gestão, carreira e liderança → escritório; ESG, sustentabilidade e meio ambiente → área verde; urbanismo e cidades → Centro de Vitória, orla ou Terceira Ponte; mobilidade → trânsito na cidade; economia, indústria e logística → porto ou fábrica; agro e mundo rural → lavouras capixabas; turismo → cartão-postal capixaba. Prefira a biblioteca dos fotógrafos da casa (Sidney Pagotto, Claudio Alves e demais). Nunca foto oculta (`visibilidade` "oculta", banco de imagem comprado), de outro veículo ou da Reuters, nem com texto, logotipo ou pessoa em primeiro plano. A versão de 1600 px do CDN basta, porque o fundo vai desfocado.
3. Grave o script abaixo como `padronizar_retrato.py` e rode `python3 padronizar_retrato.py foto.jpg fundo.jpg destacada.jpg --altura 0.45 --folha folha.jpg` (`--altura`, de 0 a 1, escolhe a faixa da foto do tema que fica atrás da pessoa). Ele recorta a pessoa (rembg; se faltar, `pip install --break-system-packages "rembg[cpu]" opencv-python-headless`), acha o rosto, iguala a cabeça e compõe sobre o tema desfocado.
4. Leia o JSON. Com `ok` true, siga. Com problema:
   - "corpo curto": a foto acaba antes da base. Troque por outra foto da pessoa, com mais corpo. Sem outra, rode de novo com `--aceitar-cabeca-maior` (a cabeça cresce só o necessário e o alto continua a 7%) e registre "cabeça maior que o padrão" em Pendências.
   - "corte lateral esfumado": a foto original corta o ombro ou o braço, e o script esfuma o corte. Se o degradê ficar estranho, troque a foto.
   - "sem rosto detectado" ou "ampliação alta": troque a foto. Sem outra, mantenha a destacada que houver e registre "foto fora do padrão" em Pendências.
5. Olhe com Read a saída e a folha (cortes 5:3, 70% e quadrado): cabeça inteira, alto do cabelo logo abaixo do topo, recorte limpo, sem halo, sem pedaço do fundo antigo ou de objeto grudado na pessoa, sem orelha, óculos ou ombro comidos. Com defeito, troque a foto ou o fundo.
6. Suba com `pedir_link_de_envio` (`tipo` "imagem", `tratamento` "nao", `materia_id`) e `curl -T`, e grave a URL que o envio devolve com `definir_imagem_destacada` (`tratamento` "nao"). O link de envio é de uso único: não mostre nem guarde. Campos: título "<Nome>, articulista da ES Brasil"; fonte, a da foto da pessoa; autor "<crédito da foto da pessoa>; fundo: <autor do fundo>/NX Fotos"; descrição "<Nome>, autor do artigo[, em <ano da foto>]; foto de arquivo, em montagem com fundo ilustrativo de <cena>"; legenda (alt) com o que se vê, terminando em "diante de <cena> desfocada".
7. Vale para toda foto de pessoa na destacada (articulista ou personagem do título). Foto de tema sem pessoa e imagem de IA (gerada em 16:9) não passam pelo script.

```python
#!/usr/bin/env python3
"""Padrão de foto dos artigos: recorta o articulista, troca SEMPRE o fundo e iguala a cabeça.

Decisão do Mário Fernando (16/11/2026): toda destacada de artigo sai no mesmo padrão,
seja qual for a foto de partida (estúdio, cena, montagem antiga):
  - a pessoa recortada (rembg) sobre uma foto do tema bem desfocada (o fundo é sempre trocado);
  - 1600x900 (16:9);
  - a cabeça sempre do mesmo tamanho e na mesma altura: do alto do cabelo ao queixo = 50%
    da altura; alto do cabelo a 7% do topo; rosto no centro; corte na altura dos braços.

Uso:
  python3 padronizar_retrato.py foto.jpg fundo.jpg saida.jpg [--altura 0.45] [--folha folha.jpg]
  fundo.jpg: foto do tema (NX Fotos, horizontal). Use "cinza" só para testar.
  --altura: de 0 (alto) a 1 (baixo), a faixa da foto do tema que fica atrás da pessoa.
  --aceitar-cabeca-maior: foto fechada demais e nenhuma outra do articulista: a cabeça cresce
    só o necessário para o corpo chegar à base (o alto da cabeça continua a 7%).
Imprime um JSON. "ok": false lista os problemas (corpo curto, corte lateral, ampliação alta,
sem rosto): nesse caso escolha outra foto do articulista em vez de subir esta.
Precisa de: pip install --break-system-packages "rembg[cpu]" opencv-python-headless
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

HAAR_BASE = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/"
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
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    w, h = im.size
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
    global AMPLIAR
    altura, folha_saida = 0.45, None
    if "--aceitar-cabeca-maior" in a:
        a.remove("--aceitar-cabeca-maior"); AMPLIAR = True
    if "--altura" in a:
        i = a.index("--altura"); altura = float(a[i + 1]); del a[i:i + 2]
    if "--folha" in a:
        i = a.index("--folha"); folha_saida = a[i + 1]; del a[i:i + 2]
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
    if toca_base and base_y < H - 2:
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