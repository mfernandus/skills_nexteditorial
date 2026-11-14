---
name: "youtube-playlists-next"
description: "Organiza e mantém as playlists e a página inicial dos canais Revista ES Brasil e Revista Comunhão no YouTube, no modelo em camadas (programa, editoria, tema, especial, cortes): inventário, diagnóstico, plano para aprovação, aplicação no Studio depois do ok e manutenção semanal."
---

# Playlists dos canais da Next — **ES Brasil** e Comunhão

Esta skill organiza as playlists e a página inicial (guia Início) dos canais **Revista ES Brasil** (youtube.com/@RevistaESBrasil, ID `UCKhj3LkxBnIQ7oU6hZED_nA`) e **Revista Comunhão** (youtube.com/@revistacomunhaooficial). O objetivo é que todo vídeo tenha lugar certo no canal, que quem chega por um vídeo encontre o próximo e maratone o tema, e que as playlists apareçam na busca do YouTube e do Google.

Use SEMPRE que o Mário Fernando ou a equipe pedir para organizar, auditar, revisar, criar, renomear, unir ou arquivar playlists; montar ou mudar a página inicial/seções do canal; marcar série oficial ou podcast; achar vídeos sem playlist; ou rodar a "manutenção das playlists" — em qualquer um dos dois canais.

## Relação com as outras skills

- `youtube-esbrasil-titulos` e `youtube-comunhao-titulos` publicam vídeo a vídeo e, no **Passo 11**, conferem se o vídeo está nas playlists da regra. **A regra vem desta skill.** Enquanto um plano não for aplicado no canal, as skills de publicação continuam usando os nomes atuais das playlists. Depois de cada aplicação, esta skill entrega a tabela nova do Passo 11 para atualizar aquelas duas skills (ver Fase 4, item 11).
- `youtube-lote-noturno-next` usa a coluna "playlist categoria" da Central. Depois de aplicado o plano, a sugestão de playlist da Central passa a seguir o mapa desta skill.

## Regra de ouro

**Nunca invente** dados de playlist, números de vídeos, periodicidade de programa, nome de apresentador, desempenho ou links. O que não for confirmado no Studio ou pelo Mário fica marcado como pendência. **Nunca exclua** playlist ou vídeo.

## Regras do YouTube que esta skill respeita

- **Série oficial** (Configurações da playlist → "Definir como série oficial desta playlist"): exige conta verificada; cada vídeo só pode estar em **uma** série oficial; só entram vídeos enviados pelo próprio canal e com direitos. Em troca, o YouTube passa a recomendar os outros episódios a quem assiste um deles. Por isso **só playlists de programa** viram série oficial.
- **Podcast** (Studio → Conteúdo → Playlists → ⋮ → "Definir como podcast"): o podcast é uma playlist, e ela deve ter **só episódios completos**, na ordem de consumo. Playlists de cortes ou de temporadas não são marcadas como podcast. O título do podcast não leva a palavra "podcast" (a não ser que faça parte do nome do programa) nem nomes genéricos como "Episódios completos". Exige capa **quadrada**. Shorts não aparecem no YouTube Music. Uma playlist marcada como podcast não recebe também a marca de série oficial.
- **Página inicial:** até 12 seções personalizadas, além do trailer (para não inscritos) e do vídeo em destaque (para inscritos que voltam). A seção de **playlist única** mostra o título, a descrição e o botão "Reproduzir tudo"; por isso a descrição de toda playlist pública precisa estar escrita. Há também a seção **"Para você"**, que mostra conteúdo do canal conforme o histórico de cada espectador. A casa usa de 6 a 8 seções e não abre a página com "Envios recentes".
- **Excluir apaga o histórico:** quando uma playlist é excluída, o tempo de exibição dela deixa de ser atribuído a ela no Analytics. Unir e arquivar, nunca excluir.
- **Shorts:** uma playlist que só tem Shorts não pode ser reordenada.
- **Limite diário:** o YouTube limita quantas playlists públicas um canal cria por dia (o número não é publicado). Margem da casa: **até 10 criações por canal por dia**. Se o Studio recusar antes disso, pare as criações, siga com o resto e retome no dia seguinte.
- **Título** da playlist: até 150 caracteres no YouTube; a casa usa **até 60**, para aparecer inteiro na busca e na página do canal.

## O modelo em camadas

Cada playlist pertence a **uma** camada. Cada vídeo entra em playlists de camadas diferentes, conforme a matriz abaixo.

| Camada | O que é | Marca técnica | Ordem dos vídeos |
|---|---|---|---|
| **1. Programa / formato** | Uma playlist por programa ou formato fixo (entrevista, debate, podcast, reportagens) | Série oficial (programas com vídeos 100% do canal) ou podcast (episódios completos) | Mais recente no topo. Série fechada em capítulos (especial em partes): capítulo 1 no topo |
| **2. Editoria** | Espelho das editorias do portal | Nenhuma | Topo com 3 a 5 "portas de entrada" (os vídeos com melhor desempenho nos últimos 90 dias que ainda estão atuais); depois, mais recente primeiro |
| **3. Tema perene** (hub) | Assunto que as pessoas buscam o ano todo; nas verticais da **ES Brasil**, também ativo comercial (patrocínio por vertical) | Nenhuma | O vídeo mais básico ou mais completo primeiro, depois os melhores; curadoria manual |
| **4. Especial / temporada** | Evento, cobertura ou projeto com data (eleições, retrospectiva, feiras) | Nenhuma (série oficial só se for especial em capítulos, sem conflito com a camada 1) | Ordem do evento ou dos capítulos |
| **5. Cortes (Shorts)** | Shorts de cada programa, separados dos vídeos longos | Nenhuma | Não reordenável; novos entram por último |
| **Vitrine** | "Comece por aqui": 10 a 15 melhores vídeos do canal | Nenhuma | Melhor primeiro; revisada todo mês |

**Matriz por vídeo**

- **Vídeo longo:** 1 playlist de programa/formato (camada 1) **+** 1 editoria (camada 2) **+** até 1 tema (camada 3), se houver **+** o especial (camada 4), se for de um especial **+** a vitrine, se for escolhido para ela.
- **Short:** só a playlist de cortes do seu programa (camada 5). Shorts não entram nas playlists de vídeos longos, para não quebrar a sequência de quem maratona.
- **Programa que já é editoria** (Destinos ES; na Comunhão, Na Estrada, A Música do Dia e Devocional): uma playlist só cumpre as camadas 1 e 2.
- Nenhum vídeo público fica sem camada 1 e camada 2.

**Quando criar:** tema (camada 3) só vira playlist pública quando houver **pelo menos 5 vídeos** para ela; antes disso, fica anotado na Central como "tema em formação". Especial (camada 4) é criado quando o projeto começa e fica fora da página inicial quando termina.

## Nomes e descrições

**Nomes**

- **Programa:** o nome do programa, exatamente como na arte e sem nada antes: `ES Brasil Entrevista`, `Café com Moqueca`, `Comunhão Entrevista`. Vale também para podcast.
- **Editoria e tema:** **palavra-chave primeiro, marca no fim**, separadas por ` | `: `Economia do Espírito Santo | ES Brasil`, `Casamento e família cristã | Comunhão`. É a mesma lógica dos títulos de vídeo das skills de publicação (assunto primeiro, programa ou marca no fim).
- **Especial:** `[Evento] [ano] | [marca]`: `Eleições 2026 no ES | ES Brasil`.
- **Cortes:** `Cortes | [programa]`: `Cortes | Café com Moqueca`.
- **Vitrine:** `Comece por aqui | ES Brasil`, `Comece por aqui | Comunhão`.
- Até 60 caracteres, sem emoji, sem palavras inteiras em caixa alta, sem nomes duplicados no canal.
- **Especiais antigos** (temporadas e projetos encerrados) mantêm o nome atual; só saem da página inicial. Renomear o que já não recebe vídeo não traz ganho e confunde quem tem o link.

**Descrição** (obrigatória em toda playlist pública), 2 ou 3 frases e um link:

```
[Palavra-chave + o que a pessoa encontra, em uma frase].
[Programa, apresentador ou periodicidade — só se confirmados no Studio ou pelo Mário].
Leia mais no portal: https://[portal]/[editoria]/?utm_source=youtube&utm_medium=playlist&utm_campaign=[slug-da-playlist]
```

- Portal: `esbrasil.com.br` ou `comunhao.com.br`, sempre na editoria correspondente, nunca na home quando a editoria existir.
- Tom da marca: **ES Brasil** sóbria e econômica, para quem decide; Comunhão acolhedora, séria e fundamentada. Nada de sensacionalismo.
- Capa da playlist: a miniatura do primeiro vídeo serve. Podcast exige capa quadrada própria: se não houver arte, registre a pendência "capa quadrada do podcast [nome]" para o design e não improvise arte.

## Mapa-alvo — **ES Brasil**

Nas tabelas, `\|` é só o separador ` | ` escapado para não quebrar a tabela; no YouTube o nome leva a barra simples.

Nomes atuais conforme o retrato de outubro de 2026 registrado em `youtube-esbrasil-titulos`. Confirme tudo no inventário (Fase 1) antes de propor: se algo mudou, vale o que está no canal.

| Camada | Nome-alvo | Hoje | Marca | Portal |
|---|---|---|---|---|
| 1 | `ES Brasil Entrevista` | ES Brasil Entrevista | Série oficial | — |
| 1 | `Café com Moqueca` | Café com Moqueca | Série oficial | — |
| 1 | `ES Brasil Debate` | **Duas** playlists com esse nome (~140 e ~24 vídeos) | Série oficial | — |
| 1 + 2 | `Destinos ES` | Destinos ES | Série oficial | /destinos-es/ |
| 1 | `Direito ao Direito` | Direito ao Direito | Série oficial | — |
| 1 | `Diálogos ES Brasil` | Diálogos ES Brasil | Podcast (só episódios completos) | — |
| 1 | `Reportagens \| ES Brasil` | Matérias - Reportagens | Nenhuma (formato, não série) | — |
| 1 | `Eventos e feiras no ES \| ES Brasil` | Eventos | Nenhuma | — |
| 2 | `Economia do Espírito Santo \| ES Brasil` | ES Brasil Economia | — | /economia/ |
| 2 | `Política no Espírito Santo \| ES Brasil` | ES Brasil Política | — | /politica/ |
| 2 | `Vida capixaba \| ES Brasil` | ES Brasil Vida Capixaba | — | /vida-capixaba/ |
| 2 | `Cultura, gastronomia e lazer no ES \| ES Brasil` | ES Brasil Diversão e Arte | — | /diversao-e-arte/ |
| 2 | `Ciência, tecnologia e inovação no ES \| ES Brasil` | **Não existe** — criar | — | /ciencia-e-tecnologia/ |
| 3 | `Portos e logística no ES \| ES Brasil` | — | — | /economia/logistica-infraestrutura/ |
| 3 | `Rochas naturais no ES \| ES Brasil` | — | — | /economia/comercio-exterior/ |
| 3 | `Energia no Espírito Santo \| ES Brasil` | — | — | /economia/energia-saneamento/ |
| 3 | `Agro capixaba \| ES Brasil` | — | — | /economia/agro/ |
| 3 | `Mercado imobiliário no ES \| ES Brasil` | — | — | /economia/ |
| 3 | `ESG no Espírito Santo \| ES Brasil` | — | — | /ciencia-e-tecnologia/ |
| 4 | `Eleições 2026 no ES \| ES Brasil` | — | — | /politica/ |
| 4 | `Retrospectiva 2026 \| ES Brasil` | — | — | — |
| 4 | Especiais antigos, com o nome atual | Acaps Trade Show 2022/2023, ES Brasil Retrospectiva 2021/2022, Especial doação de órgãos - 2018, VipES, Prodfor, 140 Destinos, Os 50 destinos mais amados pelos capixabas, Roteiros Metropolitanos de Agroturismo, De olho na Cidade | — | — |
| 5 | `Cortes \| [programa]` para cada programa com Shorts | — | — | — |
| Vitrine | `Comece por aqui \| ES Brasil` | HOME - ESBRASIL | — | — |

- **ES Brasil Debate duplicada:** a maior fica com o nome; os vídeos da menor que não estiverem nela são adicionados; a menor vira **privada** com o nome `ES Brasil Debate (arquivo)`.
- **Temas da camada 3:** só os que tiverem 5 vídeos ou mais no inventário entram no plano como "criar"; os outros, como "tema em formação".
- **Institucional, Conteúdos complementares, ES Brasil em áudio:** classificar no inventário (camada, visibilidade, conteúdo) e propor um destino no plano.

## Mapa-alvo — Comunhão

Nomes atuais conforme o retrato registrado em `youtube-comunhao-titulos`. No portal, a antiga categoria Notícias foi levada para dentro de Cotidiano (out/2026); a playlist acompanha.

| Camada | Nome-alvo | Hoje | Marca | Portal |
|---|---|---|---|---|
| 1 | `Comunhão Entrevista` | Comunhão Entrevista | Série oficial **ou** podcast (decisão do Mário: ver abaixo) | — |
| 1 | `Comunhão Debate` | Comunhão Debate | Série oficial | — |
| 1 + 2 | `Comunhão Na Estrada` | Comunhão Na Estrada | Série oficial | /categoria/na-estrada/ |
| 1 + 2 | `A Música do Dia` | A Música do Dia | Série oficial só se todos os vídeos forem do canal | /categoria/mercado-gospel-cristao/ |
| 1 + 2 | `Devocional` | Devocional | Série oficial | /categoria/multimidia/devocional/ |
| 1 | `Reportagens \| Comunhão` | Matérias e Reportagens | Nenhuma | — |
| 2 | `Igreja, liderança e missões \| Comunhão` | Comunhão Igreja | — | /categoria/igreja/ |
| 2 | `Casamento, filhos e família cristã \| Comunhão` | Comunhão Vida e Família | — | /categoria/vida-e-familia/ |
| 2 | `Notícias e cotidiano \| Comunhão` | Comunhão Notícias | — | editoria Cotidiano do portal |
| 2 | `Testemunhos de fé e conversão \| Comunhão` | Entrevistas e testemunhos | — | /categoria/colunas/testemunho/ |
| 3 | `Casamento cristão \| Comunhão` | — | — | /categoria/vida-e-familia/ |
| 3 | `Educação de filhos \| Comunhão` | — | — | /categoria/vida-e-familia/ |
| 3 | `Liderança pastoral e ministério \| Comunhão` | — | — | /categoria/igreja/ |
| 3 | `Missões e igreja perseguida \| Comunhão` | — | — | editoria Igreja e Missões › Missões |
| 3 | `Ansiedade, emoções e fé \| Comunhão` | — | — | /categoria/vida-e-familia/ |
| 3 | `Bíblia e teologia \| Comunhão` | — | — | /categoria/igreja/ |
| 4 | `Natal [ano] \| Comunhão`, `Páscoa [ano] \| Comunhão`, eventos | — | — | — |
| 5 | `Cortes \| [programa]` para cada programa com Shorts | — | — | — |
| Vitrine | `Comece por aqui \| Comunhão` | HOME COMUNHÃO | — | — |

- **Podcast da Comunhão:** as entrevistas do canal costumam ser os mesmos episódios do podcast no Spotify. A recomendação é marcar `Comunhão Entrevista` como podcast (episódios completos) em vez de série oficial, e manter **privada** a playlist "Revista Comunhão" do podcast. É uma decisão do Mário: apresente no plano como decisão, com as duas opções.
- **Testemunho de fé** (vazia e fora da página do canal): confirmar no inventário que está vazia e propor deixá-la privada como `Testemunho de fé (arquivo)`.
- **Café da Comunhão** (não listada): classificar no inventário e propor um destino.

## Página inicial — layout-padrão

Aplicar nos dois canais, em Studio → Personalização → Guia Início:

- **Trailer para quem não é inscrito:** vídeo curto que apresenta o canal (até 2 minutos). Se não existir, pendência para o audiovisual; não use uma entrevista longa no lugar.
- **Vídeo em destaque para inscritos:** o episódio mais recente do programa principal (`ES Brasil Entrevista`; `Comunhão Entrevista`), atualizado na manutenção semanal.

| # | Seção | Tipo |
|---|---|---|
| 1 | Comece por aqui | Playlist única (mostra a descrição e o "Reproduzir tudo") |
| 2 | Para você | "Para você", com vídeos e Shorts |
| 3 | Programas | Várias playlists: todas as da camada 1 em uso |
| 4 | Editoria principal (**ES Brasil**: Economia; Comunhão: Igreja) | Playlist única |
| 5 | Segunda editoria (**ES Brasil**: Política; Comunhão: Família) | Playlist única |
| 6 | Especial do momento (ex.: Eleições 2026, depois Retrospectiva 2026; Natal) | Playlist única; some quando o especial acabar |
| 7 | Temas | Várias playlists: as da camada 3 já criadas |
| 8 | Envios recentes | Vídeos |

Sem especial ativo, a seção 6 sai e a página fica com 7 seções. Não passe de 8. Shorts aparecem em "Para você" e na aba Shorts; só ganham seção própria se o Mário pedir.

## Execução

Fases 0 a 4 e **uma parada obrigatória**: o ok do plano, antes de qualquer alteração no canal. Inventário, diagnóstico e plano rodam sem perguntar.

### Fase 0 — Ambiente

- Chrome com a extensão do Claude. Cada canal fica numa conta Google diferente (Comunhão em comunhao70@gmail.com; **ES Brasil** em conta própria). Troque de conta pelo menu do avatar e **confirme no Studio o nome do canal antes de cada ação**. Nunca digite senha: se a conta não estiver logada, avise e pare naquele canal.
- Planilha Google **"Central YouTube Next"** (a mesma do lote): use as abas **Playlists**, **Playlists × vídeos** e **Plano de playlists**. Se não existirem, crie-as com as colunas abaixo. Não mexa nas abas do lote (Fila, Resumo).

### Fase 1 — Inventário (só leitura)

Para cada canal pedido:

1. **Playlists:** Studio → Conteúdo → Playlists (e a aba Podcasts). Para cada uma, grave na aba **Playlists**: canal, playlist_id, nome atual, visibilidade, nº de vídeos, série oficial (sim/não), podcast (sim/não), tem descrição (sim/não), data do vídeo mais recente, está na página inicial (sim/não), camada atual (classificação sua), camada-alvo e nome-alvo (do mapa).
2. **Vídeos:** liste os vídeos longos pela aba `/videos` do canal e os Shorts pela aba `/shorts`, paginando pela API interna do YouTube no próprio navegador (`/youtubei/v1/browse` com o token de continuação), como no inventário do lote. Liste o conteúdo de cada playlist pela página `youtube.com/playlist?list=[ID]`, logado, do mesmo jeito.
3. **Cruzamento:** na aba **Playlists × vídeos**, uma linha por vídeo: canal, video_id, título, longo/Short, publicado, views, playlists atuais, camada 1 atual, camada 2 atual, camada 1 e 2 sugeridas (pelo mapa e pela regra de assunto do Passo 11 da skill de publicação do canal), tema sugerido, falta (o que precisa ser adicionado).
4. **Desempenho (se o Analytics abrir):** visualizações e tempo de exibição de cada playlist nos últimos 90 dias e o tráfego de "Páginas do canal". Sem acesso, siga sem isso e anote.

Inventário grande: grave na planilha à medida que avança, para poder retomar.

### Fase 2 — Diagnóstico e plano (sem perguntar)

**Diagnóstico** (números por canal):

- playlists por camada e por visibilidade; duplicadas; vazias; sem descrição; fora do padrão de nome;
- vídeos longos públicos sem camada 1, sem camada 2 e sem nenhuma playlist (número e %);
- Shorts misturados em playlists de vídeos longos;
- vídeos em duas séries oficiais (o YouTube não deixa; se aparecer, é erro de classificação);
- temas da camada 3 com 5 vídeos ou mais (prontos para criar);
- página inicial atual × layout-padrão.

**Plano** — aba **Plano de playlists**, uma linha por ação, na ordem de aplicação:

| Coluna | Conteúdo |
|---|---|
| canal | ES Brasil / Comunhão |
| ação | criar · renomear · descrever · unir · adicionar vídeos · retirar vídeos · marcar série · marcar podcast · mudar visibilidade · ordenar · página inicial |
| playlist (id e nome atual) | — |
| nome-alvo / camada | do mapa |
| detalhe | ex.: "adicionar 37 vídeos (lista na aba Playlists × vídeos)", descrição proposta completa |
| motivo | uma linha |
| aprovar | o Mário escreve "sim" ou "não"; vazio = não aplicar |
| status / aplicado em | preenchido na Fase 4 |

Decisões que só o Mário toma (ex.: podcast da Comunhão; destino de playlists sem classificação clara) entram como linhas com ação "decisão" e as opções no detalhe.

### Fase 3 — Mostrar o plano e pedir o ok (parada obrigatória)

Mostre no chat o resumo (formato abaixo) e o link da Central. O ok pode vir de duas formas:

- **"Aprovado"** (ou equivalente) no chat: aplica todas as linhas do plano, menos as de decisão sem resposta;
- **coluna "aprovar"** preenchida linha a linha na Central: aplica só as linhas com "sim".

Ajustes pedidos: refaça só as linhas afetadas e mostre de novo. Enquanto o ok não vem, nada muda no canal.

### Fase 4 — Aplicação (depois do ok)

Confirme o nome do canal no Studio antes de começar e a cada troca de canal. Ordem:

1. **Criar** as playlists novas, já com nome-alvo e descrição, como **privadas**; respeite a margem de 10 criações por canal por dia.
2. **Renomear e descrever** as que ficam.
3. **Adicionar vídeos**: Studio → Conteúdo → selecione os vídeos → Editar → Playlist (edição em massa). Confira a contagem de cada playlist depois.
4. **Unir**: adicione à playlist de destino os vídeos da de origem que faltam, confira a contagem e só então deixe a de origem **privada** com `(arquivo)` no fim do nome.
5. **Retirar vídeos** fora da regra (ex.: Shorts em playlists longas), pela página da playlist.
6. **Marcar** série oficial e podcast (podcast só com a capa quadrada pronta; sem ela, fica pendente).
7. **Visibilidade**: playlists das camadas 1 a 3 e a vitrine ficam **públicas** quando tiverem vídeos (temas, com 5 ou mais); arquivos ficam privados.
8. **Ordem** dos vídeos conforme a camada. Se as configurações da playlist oferecerem ordenação automática ("Data de publicação, mais recente" ou "Adicionar novos vídeos ao topo"), use nas playlists de programa; nas outras, ordene manualmente.
9. **Página inicial** no layout-padrão → Publicar.
10. **Conferência**: recarregue cada playlist alterada e compare nome, visibilidade, marca e contagem com o plano; abra a página do canal e a aba Playlists e confira seções e ordem. Grave status e data em cada linha da Central.
11. **Atualização das skills de publicação**: entregue, para cada canal, a tabela nova do Passo 11 (assunto → playlist de editoria; programa → playlist de programa; nomes exatos como ficaram no canal), pronta para atualizar `youtube-esbrasil-titulos` e `youtube-comunhao-titulos`. Se a vitrine foi renomeada, inclua também a troca de "HOME - ESBRASIL" / "HOME COMUNHÃO" pelo nome novo no Passo 10 dessas skills (playlist reserva do card 1).
12. **Aviso à equipe** (edineim@nxte.net, audiovisual@nxte.com.br, esdrase@nxte.net): prepare o e-mail com as playlists novas e renomeadas e a regra "todo vídeo em programa + editoria". Mostre e **só envie com um sim explícito**.

Se uma etapa falhar (Studio recusa, conta deslogada, limite diário), registre na linha da Central, siga com o resto e relate no fim. Não fique parado esperando resposta.

## Manutenção semanal ("manutenção das playlists")

Roda por comando do Mário ou por tarefa agendada criada por ele. Mesmo fluxo, mais curto:

1. Vídeos e Shorts publicados desde a última manutenção: estão na camada 1 e na 2 (Shorts: na de cortes)? Os que faltam viram linhas "adicionar vídeos" no plano.
2. Temas em formação que chegaram a 5 vídeos → linha "criar".
3. Especial encerrado → linha "página inicial: retirar seção".
4. Vídeo em destaque para inscritos → o episódio mais recente do programa principal.
5. **Uma vez por mês**: revisar a vitrine e as 3 a 5 portas de entrada de cada editoria pelo desempenho dos últimos 90 dias; comparar as visualizações das playlists e o tráfego de "Páginas do canal" com o mês anterior.

Mostre o plano curto e aplique depois do ok, como na Fase 3. Inclusão de vídeo em playlist também passa pelo ok: as skills de publicação mandam a equipe marcar a playlist, e a manutenção só corrige o que ficou para trás.

## Autorizações

- **Livre, sem perguntar:** ler o Studio e o Analytics, listar vídeos e playlists, escrever nas abas de playlists da Central, montar diagnóstico e plano.
- **Depois do ok do plano:** tudo o que muda o canal (criar, renomear, descrever, adicionar ou retirar vídeos, unir, marcar série ou podcast, mudar visibilidade, ordenar, página inicial).
- **Sempre com um sim explícito à parte:** enviar e-mail ou mensagem; tornar público um vídeo ou Short (fora do escopo desta skill).
- **Nunca:** excluir playlist ou vídeo. Se o Mário pedir uma exclusão com todas as letras, confirme a playlist pelo ID e pelo número de vídeos antes, e avise que o histórico dela some do Analytics.

## Formato da entrega

**Depois do inventário e do plano** (Fase 3), no chat, por canal:

1. **Retrato:** nº de playlists (públicas, não listadas, privadas); vídeos longos sem programa, sem editoria e sem nenhuma playlist (nº e %); duplicadas, vazias e sem descrição.
2. **Plano por camada:** criar / renomear / unir / arquivar, com os nomes-alvo; nº de vídeos a adicionar por playlist.
3. **Página inicial:** atual × proposta.
4. **Decisões do Mário:** cada uma com as opções e a recomendação.
5. Link da Central e o pedido de ok.

**Depois da aplicação:** o que foi feito (com contagens), o que ficou pendente e por quê, as tabelas novas do Passo 11 e o e-mail à equipe aguardando o sim.

## Checklist antes de dar por concluído

- Todo vídeo longo público está em uma playlist de programa e em uma de editoria
- Nenhum Short em playlist de vídeos longos; cada programa com Shorts tem sua playlist de cortes
- Nenhum nome duplicado; nomes no padrão (programa puro; editoria e tema com palavra-chave primeiro e ` | marca` no fim; até 60 caracteres)
- Toda playlist pública com descrição e link do portal com UTM `utm_medium=playlist`
- Série oficial só em playlists de programa; podcast só com episódios completos e capa quadrada
- Nenhuma playlist excluída; unidas e encerradas privadas com `(arquivo)`
- Página inicial com 6 a 8 seções, sem abrir com "Envios recentes", trailer e destaque definidos (ou pendência)
- Central atualizada linha a linha; tabelas do Passo 11 entregues; e-mail à equipe só enviado com sim