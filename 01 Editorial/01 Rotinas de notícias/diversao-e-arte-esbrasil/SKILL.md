---
name: "diversao-e-arte-esbrasil"
description: "Rotina diária de Diversão e Arte da ES Brasil: agenda cultural, estreias de cinema, shows, teatro, exposições e música capixaba, apuradas na base de fontes da editoria e publicadas direto. Use quando pedirem a rodada de Diversão e Arte."
---

# Rotina diária de Diversão e Arte — ES Brasil

> Ativada em 02/11/2026 com as decisões do Mário Fernando (celebridades, prioridade das agendas da Thamiris, horários, fontes e Comunhão). Ajustada em 04/11/2026 para economizar o plano sem mudar a régua editorial (seções 2, 3, 3.5, 3.7 e 8).

Objetivo: manter a editoria **Diversão e arte** do site da **ES Brasil** (esbrasil.com.br, portal 1 no NX Feed) viva todos os dias: a agenda cultural do dia seguinte, a programação semanal dos cinemas, os anúncios de shows, teatro, exposições e festivais, e a música feita no Espírito Santo. A meta da editoria é **5 matérias por dia, 7 dias por semana**.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, pautas proibidas, cuidados do NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem (inclusive por IA), avisos e economia do plano (seção 11) estão lá. Aqui fica só o que é de Diversão e arte. Se a skill-base não estiver disponível, não publique nada: deixe as matérias em rascunho e avise que a skill-base faltou.

**Princípio editorial:** a Diversão e arte da **ES Brasil** é local. Tudo começa pelo que acontece no Espírito Santo, com serviço completo para o leitor decidir e comprar. **Celebridades (decisão de 02/11/2026):** entram, com **prioridade para as celebridades locais** (capixabas ou radicadas no ES, artistas e personalidades com agenda ou fato no Estado). Celebridade nacional só entra depois que a pauta local da rodada estiver coberta, no máximo **1 por rodada**, aproveitada do feed de agências do NX Feed (Estadão Conteúdo – Variedades e as demais contratadas, com o crédito da agência) ou de fonte oficial da própria celebridade, e nunca fofoca, vida íntima, briga, separação ou especulação. Categoria: a subcategoria de Diversão e arte que corresponde (Famosos ou TV, filmes e séries), com o id conferido em `listar_categorias_wordpress` no portal 1; nunca categoria aproximada.

**As pautas da Thamiris têm prioridade (decisão de 02/11/2026):** a editoria tem produção humana (Thamiris Guidoni faz as agendas e matérias). O que a Thamiris pautou vale sobre o que a rotina faria: se ela fez, agendou, deixou em rascunho ou pautou assunto igual ou semelhante (mesmo evento, mesmo artista, mesmo espaço na mesma semana, mesma agenda do dia), a rotina não escreve sobre ele e usa a vaga em outro assunto. Se a agenda do dia já existe, a rotina faz matérias individuais. A rotina só complementa: cobre o que a Thamiris não cobriu e os dias e horários em que ela não produziu. Se a Thamiris publicar ou agendar depois um assunto semelhante a uma matéria da rotina ainda agendada (como a agenda das 6h), a rotina tira a dela do agendamento na rodada seguinte e registra no resumo.

## 1. Rodadas (Brasília)

Descubra a rodada pela hora atual.

| Rodada | O que faz | Teto |
|---|---|---|
| **8h** (manhã) | Anúncios novos: shows e espetáculos que abriram venda, line-ups de festivais, exposições que abrem na semana, lançamentos de artistas capixabas. **Às quintas**, também a matéria de estreias da semana nos cinemas (seção 4.2). | 3 |
| **14h** (tarde) | Agenda cultural de amanhã (seção 4.1), agendada para as 6h do dia seguinte. **Às sextas**, as agendas de sábado e de domingo. Mais 1 matéria de serviço (teatro, exposição, festival do interior, gastronomia) para completar a meta do dia. | 4 |

- Meta do dia: 5 matérias somando as duas rodadas, incluindo a agenda. Teto do dia: 7. Mais vale uma matéria forte que duas fracas.
- Domingo à tarde: agenda de segunda só se houver programação relevante; senão, registre "segunda sem agenda".
- Se a execução cair fora desses horários, use a janela "desde a última matéria da casa em Diversão e arte".
- Horários confirmados em 02/11/2026: rodadas das **8h** e das **14h**. A editoria é só desta rotina: o turno noturno (`noticias-noturnas-esbrasil`) não produz mais Diversão e arte.

## 2. O que a equipe já fez (trava de duplicidade)

A trava é a da skill-base (seção 4), com estas janelas. Os itens 1 e 2 são feitos uma vez por rodada e servem a todas as pautas; o item 3 é por pauta.

1. `listar_materias` portal 1, categoria 17028, últimos 7 dias, formato compacto (todas as páginas).
2. Rascunhos dos últimos 3 dias, sem filtro de portal, e `rascunho_no_wp` e `agendado` com portal 1 (as agendas da equipe costumam ficar agendadas para as 6h).
3. Para cada pauta: `listar_materias` com `busca` pelo artista, espaço, evento ou filme (últimos 30 dias) e WebSearch `site:esbrasil.com.br <tema>`. O esbrasil.com.br recusa leitura automática: a conferência é sempre pelo NX Feed.

Regras próprias:
- **Agenda:** antes de escrever a agenda de amanhã, procure no NX Feed por "agenda" (criadas hoje e ontem, todos os estados). Se a equipe já fez ou agendou, não faça outra: use a vaga em matéria individual.
- **Evento já citado em agenda da casa** pode ganhar matéria própria, desde que traga o que a agenda não trouxe (entrevista publicada pela produção, repertório, história do artista, serviço novo como lote extra ou sessão extra).
- Mesmo evento, uma matéria própria por semana. Exceção: fato novo real (data extra, cancelamento confirmado, mudança de local, ingressos esgotados).

## 3. Base de fontes (validada em 30/10/2026)

A base abaixo vem da planilha **Fontes_Diversao_e_Arte_ES_Brasil** (132 fontes, 115 validadas com evidência de atividade em 2025–2026, 4 descartadas e 13 a confirmar). **Siga-a rigorosamente, na ordem de relevância** (decisão de 02/11/2026):

1. **Parceiros** (Sesc ES e Senac);
2. **Agenda oficial e centros culturais** (3.1), que são a fonte de verdade;
3. **Bilheterias online** (3.2), para confirmar data, local e preço;
4. **Cinemas** (3.3);
5. **Casas de show, palcos, produtoras e festivais** (3.4);
6. **Perfis de música capixaba** (3.5).

Varra nessa ordem e, entre duas pautas de mesmo peso, fica a da fonte mais relevante. Fonte fora da lista não serve de fonte; a única exceção é a página oficial do próprio evento, artista ou espaço, usada para confirmar o que uma fonte da lista anunciou. As fontes "a confirmar", descartadas ou fechadas não entram. As pistas (3.6) nunca são fonte nem crédito.

**Raspagem (decisão do Mário Fernando, 17/11/2026):** carregue a skill `raspagem-web-next` uma vez por rodada, rode `creditos` e `teto 8`, e use-a como diz a seção 3.8. Sem créditos, siga como antes, com WebFetch e WebSearch.

**Varredura econômica (skill-base, seção 11):** em cada fonte, procure só o recorte da rodada (8h: anúncios novos; 14h: a programação do dia da agenda, ou de sábado e domingo às sextas) e leia a página de programação uma vez; abra a página de um evento só quando ele for virar pauta ou item da agenda. Site que esta skill diz que não abre por leitura automática não é tentado de novo.

**Parceiros primeiro (como no turno noturno):** Sesc ES e Senac (gastronomia). Se tiverem fato novo, ganham a vaga antes de qualquer outra pauta, com a mesma régua editorial.

### 3.1 Agenda oficial e centros culturais (fonte de verdade)

| Fonte | Onde olhar | O que buscar |
|---|---|---|
| Centro Cultural Sesc Glória (Teatro Glória, Teatro Virgínia Tamanini, Cinema Sesc Glória) | sesc-es.com.br/programacao/ · lets.events/organizer/sescgloria · @sesc.es.oficial | Grandes Espetáculos, Cena Local, Palco Giratório, cinema gratuito (qua a sáb), oficinas |
| Unidades do Sesc no interior (Guarapari, Cachoeiro, São Mateus e outras) | sesc-es.com.br/programacao/ | shows, cinema e exposições |
| Theatro Carlos Gomes (Secult; reaberto em nov/2025) | @theatrocarlosgomes.es · secult.es.gov.br/noticias | temporada e espetáculos; ingressos pela Sympla |
| Teatro Universitário (Teatro da Ufes) | teatro.ufes.br (não abre por leitura automática) · Meu Bilhete | stand-up, musicais, infantis, shows nacionais |
| Teatro e Centro Cultural Sesi (Jardim da Penha) | site / Instagram | espetáculos, shows, exposições |
| Cais das Artes (museu aberto desde abr/2026; teatro só em 2027) | caisdasartes.byinti.com (ingressos gratuitos) | exposições (36ª Bienal de SP até 17/01/2027) |
| Casa da Música Sônia Cabral, Maes, Galeria Homero Massena, Parque Cultural Casa do Governador | secult.es.gov.br/noticias | exposições, recitais, eventos |
| Museu Vale, Parque Botânico Vale e Parque Costeiro | site e Instagram do Museu Vale | exposições e atividades |
| Mucane – Museu Capixaba do Negro | Instagram (canal oficial a confirmar) | exposições |
| Gaeu – Galeria de Arte Espaço Universitário (Ufes) | site da Ufes | exposições |
| Orquestra Sinfônica do ES (Oses) | Secult / Instagram | temporada de concertos |
| Fenatevi – Festival Nacional de Teatro Cidade de Vitória | @festivaldeteatrodevitoria (realização Associação Cultural Uma Floresta) | programação de outubro |
| Prefeitura de Vitória (Semc) | vitoria.es.gov.br/semc · vitoria.es.gov.br/imprensa/todas_noticias/semc | shows gratuitos, Fafi, verão |
| Prefeituras da Serra e de Colatina | serra.es.gov.br/agendas · colatina.es.gov.br/agendas/ (abrem por leitura automática) | eventos municipais |
| Prefeitura de Vila Velha | @prefvilavelha · vilavelha.es.gov.br/noticias | Arte no Parque, Luau da Vila, Saidera de Cocal, Vila Kids (Prainha), verão |
| Prefeitura de Cariacica | Instagram oficial · cariacica.es.gov.br | aniversário (junho), verão na Nova Orla |
| Prefeituras de Guarapari, Cachoeiro e Linhares | Instagram oficial; os sites bloqueiam leitura automática (3.7) | Festival Guarapari de Inverno (julho), Festa de Cachoeiro (junho), aniversário de Linhares (agosto) e Cacau Fest |

`portal.sesc-es.com.br` abre vazio: não use.

### 3.2 Bilheterias online (confirmam data, local e preço)

- **Principais:** Zig.tickets, Meaple, Sympla, Blueticket, Let's Events (use a página do organizador, como lets.events/organizer/sescgloria) e Pensa no Evento.
- **Por espaço:** Meu Bilhete (Teatro da Ufes), Inti (Cais das Artes), TicketBolt (festivais como o Somos Rock).
- **Turnês grandes (checagem eventual, sem evento capixaba em 2026):** Eventim (páginas por cidade, como eventim.com.br/city/vitoria-1747/) e Ticketmaster. Le Billet não abre por leitura automática e não teve evento capixaba achado depois de 2024.
- **Fora:** Superticket (redireciona para a Zig.tickets).
- A lista por cidade da Sympla carrega por JavaScript e não aparece na leitura automática: procure o evento pelo nome.
- A página oficial de venda conta como fonte primária de data, horário, local, classificação e preço.

### 3.3 Cinemas

- **Grande Vitória (todos com sessões em 2026):** Cinemark Shopping Vitória e Shopping Vila Velha, Cinépolis Moxuara, Cine Araújo Mestre Álvaro, Cinesercla Montserrat, Cine A Norte Sul, Cinesystem Boulevard, Kinoplex Praia da Costa, Cinema Sesc Glória (gratuito) e Cine Metrópolis (Ufes). Os links de cada sala estão na planilha.
- **Interior (com sessões em 2026):** Cine Ritz Perim Center (Cachoeiro), Cine Ritz Conceição e Cinesercla Pátio Mix (Linhares), Cine Ritz Guarapari, Cine Gama (Colatina), Cine Ritz Piúma, Cine Ritz São Mateus e Cine Ritz Aracruz (Shopping Oriundi). Sem sinal de atividade: Cine Unimed Sul, Cine Via Sul (Marataízes) e Cine Teatro Castelo.
- **Como conferir as sessões:** site de cada rede. O AdoroCinema mostra as sessões das salas capixabas e serve de atalho de conferência (não cite como fonte). No Ingresso.com os horários carregam por JavaScript.
- **Festivais e mostras:** Festival de Cinema de Vitória (Galpão Produções e IBCA; julho, com itinerante no verão), Cine.Ema (Cachoeiro e Alegre, março), FestCine Pedra Azul, Mostra Sesc de Cinema, Cine Imetame (carreta itinerante, Aracruz), mostras do Movimento Cidade.
- **Produtoras e entidades** (pauta de cinema capixaba): Galpão Produções, IBCA, Pique-Bandeira Filmes (Acervo Capixaba), Fábulas Filmes (Rodrigo Aragão), Finordia Filmes (@finordiafilmes, sem sinal desde 2024), ABD Capixaba, OCCa (@occapixabas), editais de audiovisual da Secult/Funcultura.

### 3.4 Casas de show, palcos e festivais

- **Casas e bares com programação:** Espaço Patrick Ribeiro (Goiabeiras), Café La Musique (Vila Velha), Pub 426 (Praia do Canto, Vitória, @pub.426), Brizz (Vitória), Gran Park Itapuã (Vila Velha), Garden (Praia da Costa), Arena Evo (Curva da Jurema).
- **Fechadas, não usar:** Privilège (fechou em fev/2024), Ilha Shows, Teatro Galpão (demolido em 2021). Teatro Municipal Rubem Braga (Cachoeiro): fechou com a enchente de 2020 e não há prova de reabertura; só use com confirmação da prefeitura.
- **Grandes palcos:** Praça do Papa, Parque da Prainha, Estádio Kleber Andrade, Sambão do Povo.
- **Produtoras e festivais:** Fatto Entreter (megashows, como Guns N' Roses), Brava Entretenimento (Somos Rock), Movimento Cidade (@movimento.cidade), Vital, Formemus (formemus.com.br), Jazz Vix (Cais das Artes), Boom Rap Festival, ES Restaurant Week (restaurantweek.com.br), Prêmio da Música Capixaba (MM Projetos Culturais, premiodamusicacapixaba.com.br; também faz o Formemus e o Marien Calixte Jazz Festival), Teatro Campanelli (grupo de teatro infantil em turnê, não é sala), Panshow (feira de panificação, entra em Gastronomia) e os festivais municipais do interior.

### 3.5 Música capixaba (perfis a monitorar)

Ativos em 2025–2026: Roberto Carlos, Silva, Dead Fish, Budah, Cesar MC (@cesarmc027), Luiza Dutra, Dan Abranches, Dudu MC, Afronta MC, André Prando, Amaro Lima (Manimal), Maré Tardia, Sandrera, Ada Koffi, DJ Gegeo, Casaca (@bandacasaca), Pele Morena (@pelemorenaoficial), Edson Papo Furado (@edsonpapofurado) e Thaysa Pizzolato (@thaysa_pizzolato). A confirmar: Modão das Patroas. Os @ e as páginas de Spotify estão na planilha. Vale: lançamento de música ou álbum, clipe, turnê, show no ES, prêmio, festival nacional com artista capixaba.

**Como monitorar (economia do plano, 04/11/2026; raspagem em 17/11/2026):** na rodada das 8h, primeiro por busca (`search` da `raspagem-web-next` com `--dias 7`, juntando 4 ou 5 nomes por consulta com "lançamento", "clipe" ou "show"; sem créditos, WebSearch no modo standard com o mês e o ano) e pelas páginas oficiais que abrem por leitura automática (site, YouTube, release). Abra o perfil no navegador quando a busca trouxer pista de lançamento, ou para confirmar a data e o crédito de um lançamento já achado (3.7).

### 3.6 Só pista (nunca fonte, nunca crédito)

HZ / A Gazeta (agazeta.com.br/hz), Folha Vitória (folhavitoria.com.br/agenda-de-eventos/, não abre por leitura automática), A Tribuna (tribunaonline.com.br/entretenimento/agendacultural), ES Hoje (eshoje.com.br/noticias/entretenimento/, com os posts diários "Sábado/Domingo no ES tem…"). Perfis verificados: Guia Capixaba (@guiacapixaba, cerca de 176 mil seguidores) e Rolê com o Rapha (TikTok e grupo de WhatsApp). Do It Brazil e Vitória Online não foram encontrados: não use até a equipe confirmar. Achou um evento numa pista: confirme na fonte oficial (local, produtora, bilheteria, artista) antes de escrever. Sem confirmação oficial, fica fora.

### 3.7 Leitura de Instagram e sites fechados

Instagram, alguns sites de bilheteria e de prefeituras e o próprio esbrasil.com.br não abrem por WebFetch. Nesses casos, abra no navegador (Claude in Chrome, carregando antes a skill `chrome-browser`) só para LER; nunca curta, siga, comente nem preencha nada. Use o navegador para confirmar uma pauta ou um item de agenda já escolhido, não para varrer perfis e listas (skill-base, seção 11): cada tela custa muitas vezes uma leitura de página. Se nem assim abrir, troque a pauta.

### 3.8 Raspagem com Firecrawl e Apify (17/11/2026)

Skill `raspagem-web-next`, teto de **8 créditos por rodada**. Usos, nesta ordem:

1. **Descobrir eventos novos numa fonte da base:** `map` com `--busca` (ex.: `map https://sesc-es.com.br --busca evento`, `map` na página do organizador na Let's Events ou na Sympla, Secult com `--busca noticias`). Abra só a URL do evento que vai virar pauta ou item da agenda.
2. **Páginas que carregam por JavaScript:** `scrape` da lista da Sympla por cidade, das sessões no Ingresso.com e da página da Eventim por cidade, quando precisar delas.
3. **Casas e bares (3.4) e artistas capixabas (3.5):** `search` com `--dias 7`, pelo nome da casa ou do artista e "programação", "show", "lançamento" ou "clipe". Resultado de agregador (TocaOnde, Vamos e afins), de imprensa e de Instagram é só pista: confirme na fonte oficial da base (3.1 a 3.4) ou na página oficial do evento, do artista ou da casa antes de escrever.

**Nunca pela raspagem:** os sites que esta skill diz que não abrem por leitura automática (teatro.ufes.br, Folha Vitória, Le Billet, prefeituras de Guarapari, Cachoeiro e Linhares), o Instagram e o esbrasil.com.br. Continuam como na 3.7.

## 4. Tipos de matéria

### 4.1 Agenda cultural do dia

Formato que a equipe já usa, com ajuste de SEO:

- **Chapéu:** AGENDA CULTURAL. **Categorias:** 17028, 108.
- **Palavra-chave:** "agenda cultural" (ou "o que fazer no ES"), no início do título, no slug, no 1º parágrafo e em um intertítulo. As agendas da casa ficaram entre 64 e 74 de nota SEO por falta disso; a meta é 85.
- **Título:** até 60 caracteres, com o dia e as duas atrações mais fortes. Ex.: "Agenda cultural: Nando Reis e Zé Ibarra nesta sexta no ES".
- **Abertura** de 25 a 70 palavras com o resumo do dia.
- **Blocos**, nesta ordem, só os que tiverem itens: SHOWS E FESTAS · TEATRO E DANÇA · CINEMA · GASTRONOMIA · EXPOSIÇÕES · PARA AS CRIANÇAS · INTERIOR. Cada item com intertítulo `<h4>` e serviço completo (seção 5).
- Depois do 1º bloco: `[sc name="leia_mais" categoria="diversao-e-arte" num_posts="2" ][/sc]`.
- **Mínimo de 6 itens**, com pelo menos 2 gratuitos e, quando houver, 1 do interior. Com menos de 6 itens confirmados, não faça agenda: faça matérias individuais.
- **Exposições em cartaz:** texto completo só na primeira vez que entram na agenda da semana; nas outras, uma linha com nome, local e data de encerramento. Nunca liste exposição já encerrada (confira a data final).
- Nunca escreva o que não vai acontecer (ex.: "não há atividades do Sesc neste domingo").

### 4.2 Estreias da semana nos cinemas (toda quinta, rodada das 8h)

Fecha a lacuna da subcategoria Cinema, que hoje só recebe matéria de agência.

- **Chapéu:** CINEMA. **Categorias:** 17028, 74658, 42100.
- **Título:** "Estreias nos cinemas do ES: <filme mais forte> e mais" (até 60).
- Para cada estreia: título no Brasil, gênero, classificação indicativa, duração, sinopse curta própria (2 a 3 frases) e em quais cinemas da Grande Vitória e do interior entra. Fonte: sites das redes (AdoroCinema como atalho de conferência).
- Bloco **Sessões gratuitas** com o Cinema Sesc Glória e cineclubes da semana.
- Bloco **Filme capixaba em cartaz**, quando houver.
- Não publique tabela de horários: mudam todo dia. Escreva "os horários estão no site de cada rede" e cite a rede.
- Sinopse e dados vêm do material oficial da distribuidora ou da rede; nunca de crítica de outro veículo.

### 4.3 Anúncio de evento (show, espetáculo, festival, exposição)

- Uma matéria por evento, com o gancho no título (atração, local e cidade). Ex.: "Zé Ibarra faz 1º show no ES nesta sexta em Vitória".
- Entra quando: abriu venda, line-up confirmado, data extra, abertura de exposição, festival do interior com programação fechada, primeira vez no ES, aniversário redondo de carreira.
- **Categorias:** shows 17028, 108, 42102 · teatro 17028, 108, 42101 · eventos e feiras 17028, 108, 80 · lazer e entretenimento 17028, 108, 74657 · exposições 17028, 74658 · gastronomia 17028, 86.
- 350 a 550 palavras: o que é o evento, quem é o artista (trajetória com dado oficial), o que o público vai ver, serviço completo no fim.

### 4.4 Música capixaba

- Lançamento, clipe, turnê, prêmio ou show de artista do ES. **Categorias:** 17028, 74658, 16010. **Chapéu:** MÚSICA CAPIXABA.
- Fonte: perfil, site ou release oficial do artista, gravadora, distribuidora ou plataforma de streaming. Citação só se o artista a publicou.
- 350 a 500 palavras, com link para ouvir na página oficial (um link externo, conforme a skill-base).

### 4.5 Calendário de festivais (antecipar)

Abra pauta 30 dias antes e cubra lançamento de line-up, abertura de venda e semana do evento. Datas aproximadas, a confirmar todo ano:

| Mês | Evento |
|---|---|
| Janeiro | Festival de Cinema de Vitória Itinerante (litoral); shows de verão das prefeituras |
| Março | Cine.Ema (Cachoeiro e Alegre) |
| Junho | Panshow (Shopping Vila Velha); Festa de Cachoeiro (20 a 29/jun em 2026); aniversário de Cariacica (Nova Orla) |
| Julho | Festival de Cinema de Vitória; festivais de inverno (Domingos Martins, Guarapari de 17 a 26/jul em 2026, Guaçuí) |
| Agosto | Movimento Cidade (Parque da Prainha, Vila Velha; 14 a 16/ago em 2026); aniversário de Linhares |
| Setembro | Jazz Vix (Cais das Artes); Festa do Morango (Pedra Azul); Festival do Caranguejo (Conceição da Barra); Primavera Teresense (Santa Teresa); semifinal do Prêmio da Música Capixaba |
| Outubro | Vital (Sambão do Povo; 10 e 11/out em 2026); Fenatevi; Formemus (Parque Botânico Vale); Festival do Camarão (Conceição da Barra); início da ES Restaurant Week |
| Novembro | Somos Rock (Shopping Vila Velha); fim da ES Restaurant Week |
| Dezembro | Boom Rap Festival (Kleber Andrade; 12/dez em 2026) |

## 5. Serviço (obrigatório em todo evento)

- **Data** com o dia da semana conferido no calendário ("nesta sexta-feira (30)").
- **Horário** (abertura dos portões e início, quando a fonte der).
- **Local** com nome, endereço e cidade.
- **Preço** como a fonte publica ("a partir de R$ 90, meia, 1º lote") ou "entrada gratuita"; se a retirada é antecipada, diga onde.
- **Classificação indicativa**, quando houver.
- **Onde comprar:** nome da plataforma oficial no texto. O link externo único da matéria vai para a fonte oficial (página de venda ou do evento).
- Evento sem data, local e preço confirmados em fonte oficial não entra.
- Mudança, adiamento ou cancelamento só com comunicado oficial da produção ou do local.

## 6. Padrão da matéria

- **Tamanho:** agenda e estreias sem limite rígido (o que os itens pedirem); demais tipos conforme a seção 4. **8 a 10 tags.**
- Intertítulos em `<h4>`; listas em `<ul>`; destaques em `<strong>`.
- Depois do 2º parágrafo (nas matérias que não são agenda): `[sc name="leia_mais" categoria="<slug da subcategoria>" num_posts="2" ][/sc]`.
- Sem adjetivo de propaganda ("imperdível", "o maior show do ano"). Dado em vez de elogio.
- O resto do padrão (título, lide, link, rodapé, datas, SEO) está na skill-base.

## 7. Imagem

Regra da skill-base, com esta ordem de busca:

1. `buscar_imagens` recomendadas (materia_id);
2. NX Fotos (termo: artista, espaço, cidade);
3. editoriais (termo);
4. divulgação oficial com crédito: site do evento, do espaço, da produtora, da distribuidora do filme ou release do artista ("Divulgação/<dono>");
5. imagem por IA, só com cena genérica (palco com luzes, plateia de costas, sala de cinema vazia, mesa posta), nunca o artista.

- **Agenda:** foto da atração principal do dia (divulgação oficial) ou foto de acervo do espaço.
- **Estreias:** imagem oficial de divulgação do filme mais forte da semana, com crédito da distribuidora.
- Foto de perfil de Instagram do próprio artista ou evento: **não use** (a skill-base proíbe Instagram de terceiros). Use a divulgação oficial do site, do release ou da bilheteria.

## 8. Criar e publicar

1. Reconferência leve de duplicidade imediatamente antes de publicar (skill-base, seção 4): `listar_publicacoes` do portal 1 desde a primeira conferência e `listar_materias` com `busca` pelo evento, artista ou espaço (todos os estados). Na agenda, repita também a busca por "agenda" (criadas hoje, todos os estados), porque a equipe costuma agendar a dela. As listagens dos itens 1 e 2 da seção 2 e o WebSearch não se repetem.
2. `prompt_do_nxfeed` e depois `criar_materia` com todos os campos (título, linha fina, chapéu, autor "Redação", texto, palavra-chave, título SEO, meta, slug, tags, categorias da seção 4 e imagem). Nunca Destaques.
3. Nota SEO pela skill-base (meta 85).
4. Publique direto no portal ES Brasil, uma de cada vez. Matérias da rodada: a primeira "agora" e as seguintes de 15 em 15 minutos. **Agenda:** agendada para as 6h do dia a que se refere (campo `quando`, horário de Brasília).

## 9. Resumo

Avisos da skill-base. Título do resumo: **"Diversão e Arte ES Brasil · DD/MM – rodada das <hora>"**.

Parte própria do resumo:
- publicadas: tipo (agenda, estreias, anúncio, música capixaba), título, cidade, fonte oficial, parceiro (sim/não), nota SEO, imagem (real / divulgação / IA / sem imagem), horário e link no ar (ou agendado);
- meta do dia (na rodada das 14h): quantas das 5 saíram e o motivo do que faltou;
- agenda: feita pela rotina, feita pela equipe ou não feita (menos de 6 itens);
- eventos achados só em pista, sem confirmação oficial;
- fontes da base que não abriram ou parecem desativadas (para a equipe atualizar a planilha);
- raspagem: créditos gastos na rodada e saldo, pela seção 6 da `raspagem-web-next` (crédito esgotado: aviso da seção 5 dela).

Rodada sem novidade termina com "Sem fato novo nesta rodada", sem notificação.

## 10. Comunhão

Diversão e arte é só da **ES Brasil**: a rotina não publica nada no portal da Comunhão (decisão de 02/11/2026).