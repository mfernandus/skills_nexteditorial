---
name: "atualizacao-mapas-destinos-es"
description: "Atualiza pontos turísticos do mapas.nx.tv.br (Destinos ES): locais próximos novos (comer, ficar, serviços, fazer), fotos NX Fotos e Google com crédito, tags de experiência, textos e informações. Plano antes de gravar."
---

# Atualização dos pontos turísticos — mapas.nx.tv.br (Destinos ES)

Use quando Mário pedir para atualizar, enriquecer ou revisar locais do mapas.nx.tv.br:
locais próximos novos (restaurantes, cafés, hotéis, pousadas, serviços, atrações), fotos
(NX Fotos e Google), tags de experiência, descrições e informações importantes.
Responder sempre em pt-BR.

## O sistema

Dois apps no mesmo domínio, uma só base (Laravel, API em `https://mapas.nx.tv.br/api`):

- **Painel** (`/admin`, Vue): onde se edita. ~4.800 locais, 342 pontos turísticos
  (`pontoturistico=true`), 78 municípios, 10 regiões Setur-ES, 439 categorias, 245 tags ativas.
- **Site público** (`/publico`, React, novo UX de nov/2026): o que o visitante vê. Página do
  destino: `https://mapas.nx.tv.br/publico/destino/{id}` (`?lang=en` / `?lang=es`).

Cada ponto turístico tem: `title`, `subtitle`, `description_headline`, `ai_description`, `about`,
`status`, `o_que_fazer`/`onde_comer`/`onde_ficar`/`servicos` (+ `*_headline`),
`informacoes_importantes_{como_chegar,estrada,clima,hospedagem,gerais,ritmo}`, `tags`,
`categories`, `mapa_images` (+ `main_image`), `phones`/`websites`/`mapa_emails`, `open_hours`,
`review_summary`, `verificacao` e **locais vinculados** (`linked_places`, cada um com
`category_type` e `distance_km`). "Locais próximos" = locais secundários vinculados ao ponto.

O painel já tem a busca do Google pelo servidor, os **prompts de IA da casa** e a **fila de
revisão** de estabelecimentos (lotes comida/hospedagem). A skill usa essas peças.

### O que o site público mostra (é isso que a rodada precisa alimentar)

- **Card** (listas, mapa, experiências): foto principal (`main_image` → `is_main` → primeira),
  **primeira categoria** como selo colorido pelo tipo, município · região, e o resumo =
  `ai_description` (se vazio, `about`), cortado em 2 linhas.
- **Página do destino**: subtítulo; chamada (`description_headline`); descrição; sobre; situação
  (`status`); galeria (principal primeiro, depois `order`) com **legenda, crédito (`autoria`) e
  texto alternativo**; contatos; horários; as **6 informações importantes** (como chegar, estrada,
  clima, hospedagem, gerais, ritmo); os 4 blocos (O que fazer, Onde ficar, Onde comer,
  Serviços) com headline + texto; vinculados agrupados por tipo, **com a distância**; selo
  de verificado.
- **Experiências, coleções e filtros** ("Com quem? / Onde? / O que busca?"): saem das
  **tags**, casadas pelo **nome** (tabela no Passo 5). Ponto sem essas tags não aparece neles.
- **Guia com IA e Planejador** (`POST /api/publico/guia`, `/api/publico/planejador`): montam
  roteiros a partir da base; tags e vínculos alimentam as sugestões.
- **Inglês e espanhol**: a API devolve os textos traduzidos com `?lang=en|es`; a tradução é do
  servidor, não do painel.
- **Cidades**: o número de "atrações" de cada município e as cidades em destaque contam só
  pontos turísticos.

## Acesso

- **Leitura pública** (sem login, funciona até por `curl` no ambiente de trabalho):
  - todos os pontos com tags e categorias, em 4 chamadas:
    `GET /api/mapa/filtrar?pontoturistico=true&include_tags=1&per_page=100&page=N`
  - ficha completa: `GET /api/mapa/{id}` (e `?lang=en|es`)
  - base inteira para deduplicar: `GET /api/mapa?page=N` (100/pág.)
  - `/api/mapa/municipios`, `/api/mapa/regioes`, `/api/mapa/estatisticas-municipios`,
    `/api/categories`, `/api/tags?active=true`
- **Escrita, busca no Google e prompts** exigem **sessão logada** (Sanctum, cookie): rodar pelo
  **Claude in Chrome** numa aba de `https://mapas.nx.tv.br` com Mário logado. Checar com
  `GET /api/me`: 401 → pedir para Mário entrar no painel no Chrome dele. **Nunca digitar senha.**
- **Limite: 120 requisições/min.** Espaçar ~550 ms; em 429, esperar `Retry-After` (≈30 s).
  Varreduras longas: laço em segundo plano na página (`window.__job`) e consultar.
- O retorno do javascript_tool é bloqueado se contiver `?`, `&` ou `=` (URLs, query strings):
  devolver só os campos necessários e trocar esses caracteres antes de retornar.

Helper para usar na aba (javascript_tool):

```js
window.api = async function api(path, {method='GET', body}={}) {
  if (method !== 'GET' && !window.__csrf) { await fetch('/api/csrf-cookie',{credentials:'include'}); window.__csrf = true; }
  const xsrf = decodeURIComponent((document.cookie.match(/XSRF-TOKEN=([^;]+)/)||[])[1]||'');
  const r = await fetch('/api'+path, {method, credentials:'include', headers:{
    Accept:'application/json','Content-Type':'application/json','X-Requested-With':'XMLHttpRequest',
    ...(xsrf?{'X-XSRF-TOKEN':xsrf}:{})}, body: body?JSON.stringify(body):undefined});
  if (r.status === 429) { await new Promise(z=>setTimeout(z,(+(r.headers.get('retry-after')||30))*1000+500)); return api(path,{method,body}); }
  const j = await r.json().catch(()=>null);
  if (!r.ok) throw new Error(r.status+' '+((j&&j.message)||''));
  return j;
};
```

## Passo 1 — Escopo

Entrada aceita: um ponto (nome ou id), um município, uma região, ou "fila".
Sem escopo → **fila**: os 10 pontos com maior pontuação de lacuna:

| Lacuna | Pontos |
|---|---|
| 8+ dos 14 campos de texto vazios (ou < 20 caracteres) | 3 |
| Menos de 5 fotos | 2 |
| Sem foto principal | 2 |
| Sem nenhuma tag de experiência (some de Experiências) | 2 |
| Onde comer < 5 vinculados | 2 |
| Onde ficar < 3 vinculados | 2 |
| Serviços < 3 vinculados | 1 |
| Sem tag de ambiente, de companhia ou de intenção | 1 |
| Alguma foto sem crédito | 1 |
| Todas as fotos vindas do Google (nenhuma autoral) | 1 |
| `updated_at` com mais de 9 meses | 1 |
| Não verificado | 1 |

Empate: priorizar região/município que Mário estiver trabalhando no momento.

## Passo 2 — Auditoria de cada ponto

`GET /api/mapa/{id}` e montar a ficha de lacunas:
- os 14 campos de texto (`subtitle`, `description_headline`, `ai_description`, `about`, os 4
  blocos e as 6 informações importantes): vazio, < 20 caracteres, rótulo genérico no lugar do
  texto (ex.: "Descrição") ou headline/subtítulo entre aspas;
- fotos: total, quantas do Google, principal, quais sem `autoria`, `legenda` ou `alt_text`;
- tags nos 4 eixos do site (Passo 5) e qual é a **primeira categoria**;
- vinculados por tipo, e se algum vinculado está sem tipo de categoria (não aparece no site);
- verificação, coordenadas, data da última edição;
- tradução: campos que em `?lang=en` ou `?lang=es` ainda saem em português.

Sem coordenadas → não buscar próximos; apontar no relatório.
Eventos e festivais marcados como ponto (ex.: concurso, festival) não têm endereço fixo:
buscar próximos a partir do local onde o evento acontece, se conhecido; senão, só textos e fotos,
e sinalizar no relatório.

**Linha de base (07/11/2026, 342 pontos)** — a base não mudou desde 25/10; só 2 pontos foram
editados à mão (Pedra do Elefante e Bacia das Turcas):

| Lacuna | Pontos |
|---|---|
| 8+ campos de texto vazios | 102 |
| "Estrada" e "Ritmo" vazios | 102 |
| Menos de 5 fotos (sem nenhuma) | 119 (29) |
| Sem foto principal | 37 |
| Só fotos do Google | 118 |
| Fotos sem crédito | 373 de 2.166, em 85 pontos |
| Headline ou subtítulo entre aspas | 12 |
| Sem tag de experiência | 37 |
| Sem tag de ambiente / companhia / intenção | 64 / 65 / 84 |
| Sem nenhuma tag | 36 |
| Menos de 5 "Onde comer" / 3 "Onde ficar" / 3 "Serviços" | 69 / 54 / 59 |
| Não verificados | 54 |
| Sem coordenadas | 8 |

Regiões mais carentes: Caparaó (fotos e textos), Costa e Imigração e Doce Pontões (Onde comer
e textos). Municípios com zero atrações no site: Ibiraçu e Pinheiros. Comparar cada rodada com
esta linha de base no relatório.

## Passo 3 — Locais próximos novos

1. Carregar uma vez por execução a base inteira (`/api/mapa?page=1..N`) para deduplicar.
2. Buscar pelo servidor:
   `GET /api/mapa/external-nearby-places-by-category` com
   `lat`, `lng`, `radius_km`, `category` (`onde_comer` | `onde_ficar` | `servicos` | `o_que_fazer`),
   `limit` (50), `offset`. Raio: 5 km; se não atingir a meta, 10 km; em serra/rural, até 15 km.
   O site mostra a distância de cada vinculado, então ela tem de ser real.
3. Filtrar:
   - aberto/operando; dentro do ES; registrar a distância até o ponto;
   - **Onde comer** (restaurantes, cafés, padarias, bares com comida): nota ≥ 4,0 com ≥ 15
     avaliações (cidade pequena: ≥ 4,5 com ≥ 5);
   - **Onde ficar** (hotéis, pousadas, chalés, campings): nota ≥ 4,0 com ≥ 10 avaliações;
     sem motel, salvo pedido;
   - **Serviços**: o essencial mais próximo de cada tipo — farmácia, posto, caixa 24h,
     hospital/UPA, supermercado, estacionamento, delegacia;
   - **O que fazer**: atrações que ainda não existem na base. Se parecer relevante como
     ponto turístico, só **sugerir** a promoção — não marcar `pontoturistico` sozinho.
     Lembrar que a promoção muda a contagem de atrações da cidade no site (ex.: o Grande Buda,
     id 6251, está no carrossel da home mas não é ponto turístico, e Ibiraçu aparece com zero).
4. Deduplicar contra a base: mesmo `cid`/place id, ou nome normalizado (sem acento, sem
   "restaurante/pousada/hotel/café") a menos de 150 m. Já existe mas não vinculado → só vincular.
5. Todo local vinculado precisa de categoria com `tipo_categoria` (O que fazer · Onde comer ·
   Onde ficar · Serviços): sem isso o site o esconde. O site também esconde vinculado com o
   mesmo nome do ponto.
6. Metas por execução e por ponto: até 5 comer, 3 ficar, 4 serviços, 3 fazer.
7. Nunca inventar estabelecimento: só entra o que veio da busca, com endereço e coordenadas.

## Passo 4 — Fotos (NX Fotos primeiro, Google depois, sempre com crédito e tratadas)

O site mostra legenda e crédito em cada foto e promete imagens "sempre creditadas".

Vale para **todo local**, não só ponto turístico: restaurante, hospedagem, serviço ou atração
sempre passa primeiro pelo NX Fotos; Google só quando o NX Fotos não tiver o lugar.
Toda foto, do NX Fotos ou do Google, passa pelo tratamento (item 7) antes de subir.

1. **Escolher no NX Fotos** (MCP `NXFOTOS`): `buscar` com `q` = nome do ponto; depois nome +
   município; depois `sugestoes_de_filtro` para achar o `local` exato; olhar com
   `mostrar_imagens`. Aceitar só fotos que sejam do lugar (título, descrição, tags ou
   geolocalização batem). Preferir horizontal, largura ≥ 1600, licença `rf`. Até 4 novas por
   ponto; total do ponto até 12.
2. **Gravar cópia local** (padrão da casa: todas as fotos dos pontos ficam em mapas.nx.tv.br):
   - caminho preferido, a importação do próprio painel:
     `POST /api/photoprism/search` `{query, count, offset}` →
     `POST /api/photoprism/save-images-optimized`
     `{images:[{uid, hash, url, name, width, height}], optimization_level:"cache_full"}` →
     URL local. Em 07/11 essas rotas responderam erro sem login: testar logado no primeiro
     ponto da rodada;
   - se a importação falhar: `POST /api/mapa/{id}/images` com a URL `src.large` do CDN do
     NX Fotos e conferir em `GET /api/mapa/{id}/images` se virou URL local; se continuar no
     CDN, registrar no relatório.
   - **caminho que funciona (17/11/2026)**: o CDN do NX Fotos não libera leitura pelo
     mapas (sem CORS). Numa aba do mapas logada, `window.open` da imagem do CDN; na aba do
     CDN, `fetch('/pub/...@w1600.webp')` e `window.opener.postMessage({key, blob},
     'https://mapas.nx.tv.br')`; na aba do mapas, tratar o blob no canvas (item 7), subir por
     `POST /api/upload-image` (campo `image`) e anexar com `POST /api/mapa/{id}/images`
     (`source: upload`). Assim a foto fica tratada e com cópia local.
3. Campos de cada foto nova: `alt_text` "<título> — <município> (ES)", `legenda` = descrição
   da foto, **`autoria` obrigatória** (NX Fotos: `author`; Google: nome do colaborador que vem
   na própria foto), `is_main: false`, `file_name`. Não repetir foto já existente.
4. **Google**: estabelecimentos novos chegam com as fotos do Google pelo próprio sistema.
   Para ponto com < 5 fotos e sem NX Fotos, usar as fotos do Google Places da busca do
   servidor, com crédito. **Não usar** `/api/google-images` (busca de imagens da web, direitos
   desconhecidos).
5. **Fotos antigas sem crédito**: preencher `autoria` (`PUT /api/mapa/{id}/images/{imgId}`)
   só quando o autor for conhecido com certeza; senão, listar no relatório.
6. **Foto principal**: propor trocar só se não houver principal, ou se a atual for Google e
   houver NX Fotos horizontal ≥ 1600 (`POST /api/mapa/{id}/images/{imgId}/set-main`).
7. **Tratamento (regra de Mário, 11/11/2026, todas as rotinas)**: analisar cada foto. Se
   estiver crua, tratar no padrão das revistas impressas: mais viva, um pouco mais cítrica e
   quente, azuis mais quentes. Se já estiver tratada e boa, não mexer. Receita usada em
   17/11/2026 (k = 1 para foto crua de câmera, 0,8 para celular, 0,6 para foto já viva):
   contraste ×(1+0,09k) em torno de 0,5; vivacidade 0,55k×(1−saturação); R ×(1+0,04k),
   G ×(1+0,022k), B ×(1−0,012k); nos azuis (d = B−R > 0) G +0,05k·d e B −0,01k·d;
   gama 1−0,05k; JPEG 0,9. Não tirar azul do céu: esquentar puxando para o turquesa.
8. **Não repetir foto**: antes de anexar, comparar cada candidata com as fotos que o local já
   tem (miniatura 16×16 em tons de cinza, hash médio; distância ≤ 20 = mesma foto). As
   fotos do Google já usadas numa rodada anterior voltam primeiro na busca.
9. **A foto tem de mostrar o lugar**: nada de logotipo, selfie ou paisagem que não mostre o
   estabelecimento. Foto do NX Fotos sem GPS e com título genérico ("praça central",
   "calçadão") só entra depois de comparar com as fotos que o local já tem.

## Passo 5 — Tags e categorias (o que põe o ponto nas experiências do site)

O site casa experiências, coleções e filtros pelo **nome exato** destas tags. Usar só tags que
já existem (ids de `/api/tags?active=true`); **nunca criar nem renomear tag** (os slugs da base
não batem com os nomes, ex.: "Eventos" tem slug `elevadores`).

| Eixo | Opção | Tags (basta uma) |
|---|---|---|
| Experiência | Praia & Mar | Praia Urbana, Praia Selvagem, Frutos do Mar, Mergulho, Areia Monazítica, Praia com Falésias, Praia de Tombo, Tartaruga Marinha, Águas Calmas |
| Experiência | Gastronomia & Sabores | Culinária Regional, Cafés Especiais, Culinária Italiana, Cervejas Artesanais, Doces e Sobremesas, Alta Gastronomia, Adega de Vinhos, Comida de Boteco, Restaurante com Vista |
| Experiência | Aventura | Turismo de Aventura, Esporte de Aventura, Trilhas e Trekking, Rapel, Asa Delta, Caminhadas |
| Experiência | Festas & Eventos | Eventos, Música ao Vivo, Sala de eventos |
| Experiência | A Dois | Pôr do Sol, Restaurante com Vista, Vista Panorâmica, Clima de Montanha, Adega de Vinhos, Alta Gastronomia |
| Experiência | Natureza & Ecoturismo | Natureza, Cachoeiras, Biodiversidade, Mirantes Naturais, Zona Rural, Agroturismo, Vista para as Montanhas |
| Experiência | Cultura & História | Cultura, Patrimônio Histórico e Cultural, Arquitetura Colonial, Centro Histórico, Museus, Artesanato, Arquitetura Eclética, Aldeia Indígena, Igrejas e Santuários, Arte sacra |
| Com quem? | A dois | Pôr do Sol, Restaurante com Vista, Vista Panorâmica, Adega de Vinhos, Alta Gastronomia |
| Com quem? | Família | Ideal para Crianças, Espaço Kids, Bom para Terceira Idade, Águas Calmas, Piscina ao ar livre |
| Com quem? | Amigos | Música ao Vivo, Comida de Boteco, Cervejas Artesanais, Eventos, Esporte de Aventura |
| Com quem? | Crianças | Ideal para Crianças, Espaço Kids |
| Com quem? | Solo | Trilhas e Trekking, Mirantes Naturais, Caminhadas, Museus, Religiosidade, Biodiversidade |
| Onde? | Praia | Praia Urbana, Praia Selvagem, Praia com Falésias, Praia de Tombo, Areia Monazítica |
| Onde? | Montanha | Clima de Montanha, Vista para as Montanhas, pico de montanhas, Mirantes Naturais |
| Onde? | Campo | Zona Rural, Agroturismo |
| Onde? | Cidade | Centro Histórico, Patrimônio Histórico e Cultural, Museus, Arquitetura Colonial |
| Onde? | Cachoeira | Cachoeiras |
| Onde? | Rio & Lagoa | Águas Calmas, Água Cristalina |
| O que busca? | Relaxar | Spa, Águas Calmas, Piscina ao ar livre, Pôr do Sol, Clima de Montanha |
| O que busca? | Passear | Caminhadas, Mirantes Naturais, Centro Histórico, Vista Panorâmica |
| O que busca? | Explorar | Trilhas e Trekking, Cachoeiras, Biodiversidade, Museus, Aldeia Indígena |
| O que busca? | Aventura | Turismo de Aventura, Esporte de Aventura, Rapel |
| O que busca? | Radical | Asa Delta, Esporte de Aventura, Rapel |

Coleções da home: Praias, Montanhas, Sabores, Raízes, Festas e Cachoeiras usam subconjuntos
das mesmas tags.

1. Propor, para cada ponto, ao menos uma tag de experiência, uma de ambiente, uma de
   companhia e uma de intenção — **só as que forem verdade para o lugar** (fonte: textos da
   ficha, fotos, categoria, avaliações). Pode partir do prompt da casa
   (`/prompts/tipo/tags` + `POST /api/ai/generate-tags`) e filtrar pelo vocabulário acima.
2. Tags de comodidade (TV, wi-fi, ar-condicionado, estacionamento etc.) não aparecem no site:
   não gastar a rodada com elas nos pontos turísticos.
3. **Primeira categoria = selo do card**: a mais representativa vem primeiro (ex.: "Cachoeira"
   antes de "Estacionamento"). Propor a reordenação quando estiver errada.

## Passo 6 — Textos (prompts da casa)

Preencher **só campos vazios, com menos de 20 caracteres ou com rótulo genérico**. Reescrever
texto existente apenas se Mário pedir "reescrever".

| Campo(s) | `tipo` do prompt |
|---|---|
| `subtitle` | `subtitulo` |
| `ai_description`, `description_headline` | `descrição` |
| `about` | `sobre_local` |
| `o_que_fazer` + headline | `o-que-fazer` |
| `onde_comer` + headline | `onde-comer` |
| `onde_ficar` + headline | `onde-ficar` |
| `servicos` + headline | `servicos` |
| `informacoes_importantes_*` (as 6, incluindo **estrada** e **ritmo**) | `informacoes-importantes` |
| categorias | `categorias` |

Fluxo do painel: `GET /api/prompts/tipo/{tipo}` → `POST /api/prompts/{id}/processar`
`{variaveis:{title, address, categories, tags}}` → `POST /api/ai/execute-prompt`
`{content, prompt_id}` → texto em `result`/`response`.

Revisar cada saída antes de propor:
- nada de nomes, preços, horários ou distâncias que não estejam nos dados;
- Onde comer / Onde ficar citam só estabelecimentos já vinculados (ou aprovados nesta rodada);
- `ai_description` é o resumo do card: a primeira frase tem de funcionar sozinha;
- headline e subtítulo **sem aspas**; headline ≤ 70 caracteres; subtítulo ≤ 80; nunca deixar
  rótulo no lugar do texto;
- pt-BR correto, sem superlativo vazio; coerente com município e região (nome oficial Setur-ES).

Tradução: só gravar em português. O servidor gera o inglês e o espanhol; a skill não grava
tradução. Depois de salvar, conferir `?lang=en` e `?lang=es` e listar no relatório os campos
que ainda saem em português (em 07/11, os campos editados hoje na Bacia das Turcas saíam em
português nas três línguas).

## Passo 7 — Plano para aprovação (obrigatório antes de gravar)

Por ponto: lacunas encontradas → locais novos (nome, categoria, nota/avaliações, distância),
vínculos de locais já existentes, fotos candidatas (miniatura, autor, origem), tags a
acrescentar (com o eixo de cada uma), ordem de categorias, textos propostos (campo + texto),
créditos a preencher e troca de foto principal. Fechar com totais e pedir **ok**
("aplicar tudo", "aplicar só X", "pular Y").

Execução agendada / sem Mário presente: fazer auditoria e plano, não gravar, entregar o plano.

## Passo 8 — Aplicar (após o ok)

Ordem: novos locais → vínculos → fotos → tags e categorias → textos → verificação.

1. Novo local: `POST /api/mapa` com `title`, `address`, `latitude`, `longitude`,
   `municipio_id`, `categories` (com tipo), `pontoturistico:false`, `telefones`/`websites`/`emails`
   se vierem e `open_hours` no formato do painel quando o Google trouxer horário:
   `{"type":"simple","simple_text":…,"regular_hours":{"monday":{"enabled":true,"periods":[{"open":"08:00","close":"18:00"}]},…},"fechado_feriados":false,"agendamento_necessario":false,"notes":…}`.
2. Vincular ao ponto: `POST /api/admin/all-locations/{novoId}/local-secundario`
   `{local_primario_id: pontoId}`.
3. Conferir se entrou como **pendente** em `GET /api/revisao/estabelecimentos`. Se não entrou,
   marcar `PUT /api/mapa/{novoId}/verificacao` `{verificado:false, observacoes:"Inserido pela
   rotina em <data> — revisar"}`. **Nunca aprovar na fila de revisão sem Mário mandar.**
4. Fotos e créditos: Passo 4.
5. Tags, categorias e textos: `GET /api/mapa/{id}` → mesclar só o que foi aprovado →
   `PUT /api/mapa/{id}` com o objeto completo no formato do painel (nunca PUT parcial). No
   primeiro ponto da execução, reler a ficha e confirmar que nenhum outro campo mudou antes
   de seguir.
6. Rodar uma vez, sem retentativa cega: erro → registrar e seguir para o próximo ponto.

## Passo 9 — Conferir no site e relatar

1. Abrir `https://mapas.nx.tv.br/publico/destino/{id}` e confirmar: foto principal, crédito
   das fotos, blocos e informações importantes, vinculados com distância.
2. Conferir `?lang=en` e `?lang=es` (tradução pendente vai para o relatório).
3. Relatório por ponto: o que foi inserido, vinculado, fotografado, creditado, etiquetado e
   escrito; o que ficou pendente e por quê; em quais experiências do site o ponto passou a
   aparecer. Comparar os totais com a linha de base do Passo 2.
   Links: página pública, `https://mapas.nx.tv.br/admin/locais/{id}/edicao` e
   `https://mapas.nx.tv.br/admin/revisao-estabelecimentos` (pendentes para aprovar).
   O histórico de cada local fica em `/admin/locais/{id}/historico`.

## Regras invioláveis

- Nunca apagar locais, fotos ou vínculos (`DELETE` fora de questão) nem desmarcar ponto turístico.
  Única exceção, e só com ordem expressa de Mário na hora: apagar foto que a própria rodada
  criou (cópia repetida, versão sem tratamento trocada pela tratada, foto imprópria) com
  `DELETE /api/mapa/{id}/images/{imgId}`, conferindo depois que a original continua.
- Nunca subir foto sem tratamento (Passo 4, item 7).
- Nunca sobrescrever texto preenchido sem pedido explícito.
- Nunca aprovar/recusar na fila de revisão sem ordem de Mário.
- Nunca criar, renomear nem desativar tag ou categoria.
- Nunca gravar foto sem crédito, nem foto de busca de imagens da web.
- Nunca gravar tradução à mão.
- Nunca digitar senha nem criar conta; sem sessão, parar e pedir login.
- Respeitar 120 req/min.
- Nunca inventar dados de estabelecimento, telefone, horário ou preço.