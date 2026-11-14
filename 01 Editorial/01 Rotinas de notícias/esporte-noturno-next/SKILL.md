---
name: "esporte-noturno-next"
description: "Esporte da ES Brasil e da Comunhão em 5 rodadas por dia (7h, 12h, 16h, 21h50, 23h50): resultados, notícias e resumo do Brasileirão, publicados direto. O noticiário geral fica na panorama-next."
---

# Esporte — ES Brasil e Comunhão (5 rodadas por dia)

Rotina que mantém atualizada a editoria de esportes dos portais **ES Brasil** e **Comunhão**. O noticiário geral (Panorama: Brasil, Mundo, clima e ciência, gente) é de outra rotina, a **panorama-next**, que roda na mesma execução, logo depois desta.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, cuidados do NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem, avisos e economia do plano (seção 11) estão lá. Aqui fica só o que é do esporte. Se a skill-base não estiver disponível, não publique nada: deixe as matérias em rascunho e avise que a skill-base faltou.

**Junto com a panorama-next (mesma execução):** esta rotina roda primeiro e faz as listagens que servem às duas: a manutenção da Comunhão (passo 0, inclusive a categoria 1), as pendências (passo 0b) e o feed nacional (passo 1). Separe para a panorama-next o que é dela; ela usa essas listagens e não as repete (skill-base, seção 11).

**Por que o esporte saiu do Panorama (25/10/2026):** o bloco Panorama das duas homes estava tomado por esporte (ES Brasil: 29 dos últimos 30 posts; Comunhão: 25 de 25). O Mário decidiu: menos esporte, fora do Panorama (na Comunhão, só a principal do momento) e cada assunto com sua rotina e seu teto.

**Ajuste já feito no site (25/10/2026):** o bloco Panorama da home da ES Brasil (página "Home 2026", id 398596, bloco td_flex_block_1, category_id 63) usa category_ids "63,-21560,-21860,-21861,-21862,-21863,-83881,-22736,-22264,-22114", que excluem as subcategorias de esporte. Se for criada uma subcategoria nova de esporte dentro de Panorama, ela precisa entrar nessa lista.

## Rodadas do dia (Brasília)

Descubra a rodada pela hora atual. Cada rodada cobre o que aconteceu **desde a rodada anterior** e ainda não tem matéria da casa. Fora desses horários, use a janela "desde a última matéria de esporte da casa" e o teto de 2.

| Rodada | Janela | Foco | Teto |
|---|---|---|---|
| **7h** | desde a das 23h50 | Jogos que terminaram depois da meia-noite; NBA, NFL e jogos das Américas da noite; F1, MotoGP, tênis e eventos na Ásia/Oceania na madrugada; notícias das agências da madrugada. Resultado da noite que ficou pendente sai agora (ou vai ao resumo com o motivo). | 2 |
| **12h** | desde a das 7h | Jogos da manhã na Europa com brasileiros ou de grande apelo; tênis; convocações e coletivas; classificação de F1 já encerrada; esporte capixaba. | 2 |
| **16h** | desde a das 12h | Jogos da tarde na Europa (Champions, Liga Europa, ligas nacionais); tênis; classificação de F1 e MotoGP; notícias da tarde (técnico demitido, contratação, lesão, decisões de STJD/CBF); esporte capixaba. Pré-jogo da noite publica direto, antes do início da partida. | 2 |
| **21h50** | desde a das 16h | Rodada principal: jogos da tarde e do começo da noite (Brasileirão, Copa do Brasil, Libertadores, Sul-Americana, Série B, Europa) e a matéria-resumo da rodada do Brasileirão. | 4 (o resumo conta) |
| **23h50** | desde a das 21h50 | Jogos que começaram às 19h30 ou depois (Libertadores, Copa do Brasil, Brasileirão das 20h/21h30), NBA do início da noite e eventos que terminaram depois das 21h50; matéria-resumo do Brasileirão se a rodada foi à noite. | 2 |

Total: até 12 matérias de esporte por dia. Rodada sem nada relevante no esporte: cumpra o passo 0 e termine com "Sem movimentação nova no esporte nesta rodada".

## Regra de categorias e Destaques

- **ES Brasil:** esporte vai **só** na categoria do esporte (tabela do passo 6), uma só, **nunca 63** (Panorama). O esporte aparece no bloco Esportes da home. **Destaques (11966) não é desta rotina** (decisão do Mário Fernando, 30/10/2026, reafirmada em 02/11/2026): quem põe e tira esporte do Destaques é a rotina de Destaques, de hora em hora, que dá mais espaço ao esporte nos fins de semana, feriados e noites de jogo. Esta rotina nunca marca nem tira a 11966; publique só com a categoria do esporte.
- **Comunhão:** esporte vai em **Cotidiano › Brasil & Mundo › Esportes (116634)**. A **Cotidiano › Panorama (1)**, que alimenta o bloco Panorama da home, recebe NO MÁXIMO UMA matéria de esporte por vez: a principal do momento (resultado decisivo de um dos 12 clubes, Seleção, título, final). As outras ficam só em 116634. Esporte **nunca** em Destaques (44517). A antiga Notícias › Esporte (16424) não existe mais desde 18/10/2026: nunca use; se uma matéria antiga ainda a tiver, troque por 116634 ao editar.
- **O que vai para a Comunhão:** só jogos e fatos grandes dos 12 clubes, Seleção Brasileira (principal e base, masculina e feminina), finais e títulos. NBA, NFL, lutas, ligas europeias sem final ou título e os demais esportes vão só para a ES Brasil (sem categorias da Comunhão; ao publicar, `portais` só ["ES Brasil"]).
- **Teto diário da Comunhão:** 4 matérias de esporte por dia, somando todas as rodadas. Antes de pôr uma matéria na Comunhão, conte o que esta rotina já pôs hoje lá (`listar_materias` portal=4, estado publicado, data_de = hoje, categoria 116634). Atingido o teto, a matéria sai só na ES Brasil.

## 0. Manutenção (primeiro passo de toda rodada)

1. **Destaques da ES Brasil:** não mexa; é da rotina de Destaques.
2. **Comunhão:** `listar_materias` (portal=4, estado publicado, campo_data publicada, data_de 3 dias atrás, formato compacto), primeiro com a categoria 44517 e depois com a 1. Tire de 44517 qualquer matéria de esporte. Na 1, deixe no máximo UMA de esporte (a mais importante das últimas 24 horas); das outras, tire a 1 e deixe só 116634. Esporte com mais de 24 horas sai da 1. Antes de tirar a 1, confira com `ver_materia` que a matéria está na Comunhão (na ES Brasil, a 1 é "Sem categoria"). **Guarde a listagem da categoria 1:** a panorama-next conta nela o teto diário de Panorama da Comunhão, sem listar de novo.
3. Não mexa em matérias de outras editorias.

## 0b. Pendências das rodadas anteriores

`listar_materias` com estado=rascunho (sem filtro de portal) e depois estado=rascunho_no_wp, data_de = ontem, formato compacto. Uma listagem só, que serve também à panorama-next: separe para ela as pendências de Panorama. Mexa só nas matérias de esporte desta rotina (via Claude). Rascunho parado não conta como cobertura.
- Mesmo fato já publicado por outra matéria da casa → deixe quieta e cite no resumo.
- Pré-jogo de partida já encerrada ou fato superado → não publique; cite no resumo.
- O resto → resolva foto e SEO e publique já.
- Os itens de 0b contam no teto da rodada.

## 1. Varredura do NX Feed (sempre antes da web)

1. `listar_materias` com `lista` = feed_nacional, `data_de` = início da janela, formato compacto, `por_pagina` = 100; pagine enquanto `tem_mais` = true e os itens estiverem dentro da janela.
2. O `feed_internacional` só traz veículos cristãos: pule-o. NBA, NFL, F1, tênis e Europa chegam pelo Estadão Conteúdo – Esportes e pela Agência Brasil – Esportes, no feed nacional.
3. Separe os itens de esporte (fontes de Esportes e títulos claramente esportivos). Os itens gerais são da panorama-next: não mexa neles aqui, mas deixe a lista para ela (ela não lista o feed de novo).
4. Item de esporte: já tem matéria da casa PUBLICADA → ignore; só em rascunho → passo 0b; relevante → entra na pauta (aproveite o próprio item editando SEO, chapéu, categorias e imagem, com o crédito da agência, ou escreva matéria autoral "Redação" juntando fontes); pré-jogo de evento já acontecido, nota menor ou fora do perfil → ignore.
5. Anote quantos itens de esporte havia e quantos foram aproveitados.

## 2. Varredura da web (só o que o feed não trouxe)

1. **Jogos e resultados da janela:** uma página de jogos do dia com todos os placares (ge, Gazeta Esportiva ou Lance!) monta a lista de jogos e mostra o que falta cobrir. As demais (Trivela, DOL, ESPN, CBF, Conmebol, UEFA) só para conferir o dado de uma matéria que vai sair.
2. Notícias dos 12 clubes e de atletas brasileiros em alta (técnico, contratação, lesão, punição, convocação): primeiro o que veio no feed; na web, uma busca por rodada com o que o feed não trouxe.
3. ES: Federação de Futebol do ES; A Gazeta e Folha Vitória só como pista.
4. WebSearch no modo standard; o extended só quando o standard não trouxer um fato muito recente. Imprensa é pista e conferência; o texto é sempre próprio.

### Cobertura obrigatória (não pode faltar)

- **Os 12 clubes:** Flamengo, Vasco, Fluminense, Botafogo, Atlético Mineiro, Cruzeiro, Corinthians, Palmeiras, São Paulo, Santos, Grêmio e Internacional. Todo jogo oficial aparece, com matéria própria (passo 5) ou com placar e contexto na matéria-resumo. Fatos grandes fora de campo (troca de técnico, contratação de impacto, lesão grave de titular, punição) também.
- **Libertadores** (inclusive feminina): todo jogo de clube brasileiro, com matéria própria.
- **Copa do Brasil:** todo jogo dos 12 clubes e tudo das quartas em diante, com matéria própria.
- **Brasileirão Série A:** todos os placares na matéria-resumo, com líder, G-4/G-6 e Z-4.
- **Seleção Brasileira** (principal e base, masculina e feminina): todo jogo e toda convocação.
- **Futebol capixaba:** Rio Branco, Desportiva, Vitória-ES e o Capixabão.

### Demais esportes (por prioridade, só evento grande)

1. Sul-Americana com brasileiros; Mundial de Clubes; Champions e ligas europeias com brasileiro em destaque; Série B só G-4/Z-4 ou com um dos 12.
2. Fórmula 1 (classificação, sprint e corrida). 3. Vôlei. 4. Basquete e NBA. 5. NFL. 6. Tênis (Grand Slams, Masters, brasileiros). 7. Jogos Olímpicos e ciclo olímpico. 8. Competições sazonais. 9. Celebridades do esporte em fato grande.

## 3. Não duplicar

Trava da skill-base (seção 4), com `busca` pelos times, atletas ou fato e `data_de` = ontem, em todos os estados, inclusive as rodadas anteriores do dia. A redação também publica itens de agência de esporte: refaça a busca imediatamente antes de publicar.

## 4. Apurar

Fontes, nesta ordem: agências no NX Feed; fontes oficiais (CBF, clubes, Conmebol, Fifa, FIA/F1, CBV, CBB, NBA, NFL, ATP/WTA, COB/COI, Federação de Futebol do ES); imprensa esportiva só para conferir. Placar, autor e minuto de gol, expulsões e posição na tabela conferidos em **duas fontes**; dado divergente fica de fora. Nada de "curiosidades" sem fonte.

## 5. Pauta (respeite o teto da rodada)

- Libertadores e Copa do Brasil: matéria própria por jogo de clube brasileiro.
- Brasileirão: matéria própria SÓ para jogo que muda a liderança, mexe no G-4 ou no Z-4, ou clássico entre os 12 clubes. Os demais placares, inclusive dos 12 clubes, vão para a matéria-resumo da rodada (uma por dia de rodada, na rodada das 21h50 ou das 23h50).
- Troca de técnico dos 12 clubes e classificação/eliminação em mata-mata sempre viram título.
- Outros esportes: só evento grande (final, título, brasileiro em decisão ou pódio, classificação e corrida de F1). Nada de pauta de contexto, bastidor ou serviço para preencher rodada.
- Coberturas especiais (ex.: um GP de F1): no máximo 1 matéria por rodada e só com fato novo (sessão encerrada, punição, fala forte).
- Se a cobertura obrigatória passar do teto, junte jogos em matéria-resumo em vez de estourar o teto.
- Ordene a pauta por importância: essa ordem define a ordem de publicação (o resultado mais forte sai primeiro e é o que a rotina de Destaques tende a escolher).

## 6. Padrão da matéria de esporte

- Chapéu: BRASILEIRÃO, COPA DO BRASIL, LIBERTADORES, LIBERTADORES FEMININA, SELEÇÃO, FÓRMULA 1, VÔLEI, NBA, NFL, TÊNIS, OLIMPÍADAS, ESPORTE CAPIXABA etc.
- Texto: lide; desenvolvimento; contexto de tabela ou chave; próximo compromisso; intertítulos `<h3>`; "Ficha técnica" no jogo principal; um link para fonte oficial; rodapé "Com informações de [fontes]".
- **Categorias** (conferidas em 20/10/2026):

| Esporte | ES Brasil (uma só) |
|---|---|
| Futebol (inclui Libertadores, Copa do Brasil, Seleção) | 21860 |
| Fórmula 1 | 21861 |
| Vôlei | 21862 |
| Basquete / NBA | 21863 |
| NFL | 83881 |
| Tênis | 22736 |
| Lutas | 22264 |
| Surfe | 22114 |
| Olimpíadas, sazonais, celebridades e outros | 21560 |

Na Comunhão, toda matéria de esporte vai em 116634, mas só entra lá o que passa na regra "O que vai para a Comunhão" (acima) e cabe no teto diário.

Nenhuma matéria desta rotina recebe 11966 (Destaques é da rotina de Destaques); na Comunhão, só a principal do momento recebe também a 1. Nada de categorias de outras editorias em matéria de esporte.

## 7. Imagem do esporte

- Prefira **sempre foto do próprio jogo ou evento**. Além de `buscar_imagens` recomendadas, editoriais e NX Fotos, busque com `fonte=google` ("<time A> x <time B>" + competição) e com WebSearch nas matérias do jogo. Só vale foto do fotógrafo do clube, da federação ou da liga com crédito visível (ex.: "Matheus Lima/Vasco"), gravada com fonte = clube ou entidade, autor = crédito e legenda do que a foto mostra.
- Sem foto real com direito de uso: imagem por IA (skill-base, 9.1) e publique; não deixe matéria parada por foto. No esporte, a IA nunca recria o lance, o jogo ou o atleta: cena genérica (estádio vazio ao entardecer, bola na grama, quadra, pista).

## 8. Publicação

1. Toda matéria de esporte da rodada (resultado, notícia, matéria-resumo, outros esportes, pré-jogo de partida que ainda não começou) vai ao ar direto, pela regra da skill-base, uma por vez. Resultado: placar e gols conferidos em duas fontes antes de publicar. Publicar também dispara o post no X dos portais.
2. Pré-jogo de partida já encerrada não sai: cite no resumo como superado.
3. **Prévia superada:** se a casa tem pré-jogo publicado de partida que já terminou e o resultado já está no ar, acrescente no topo da prévia `<p><strong>Atualização (DD/MM):</strong> placar e consequência. <a href="LINK">Veja como foi o jogo</a>.</p>`, com link absoluto do resultado **no mesmo portal** (nunca começando com /): grave com o link da ES Brasil e rode `atualizar_no_wordpress` só na ES Brasil; troque pelo link da Comunhão e rode só na Comunhão. Não mude título nem status da prévia.
4. Quando a panorama-next rodar na mesma execução, intercale as publicações das duas, começando pela notícia mais importante, uma de cada vez.

## 9. Resumo

Avisos da skill-base. Título do resumo: **"Esporte – rodada das <hora>"**; quando a panorama-next rodar na mesma execução, um resumo só: **"Esporte e Panorama – rodada das <hora>"**.

Parte do esporte no resumo:
- publicadas (título, portal, link no ar, imagem real ou IA);
- não publicadas, com o motivo; prévias atualizadas; o que saiu da 44517 e da categoria 1 da Comunhão;
- itens de esporte nas agências e quantos foram aproveitados;
- conferência da cobertura obrigatória (12 clubes, Libertadores, Copa do Brasil), tabela do Brasileirão (líder, G-4, Z-4) e o que falta jogar.