---
name: "atualizacao-mapas-destinos-es"
description: "Atualiza e enriquece locais do mapas.nx.tv.br (Destinos ES) em qualquer modelo de lote, no padrão único: fotos tratadas e creditadas, curadoria automática e aviso de checagem ao fim."
---

# Atualização dos pontos turísticos — mapas.nx.tv.br (Destinos ES)

Use quando Mário pedir para atualizar, enriquecer ou revisar locais do mapas.nx.tv.br:
locais próximos novos (restaurantes, cafés, hotéis, pousadas, serviços, atrações), fotos
(NX Fotos e Google), tags de experiência, descrições e informações importantes.
Responder sempre em pt-BR.

**Padrão único (19/11/2026).** Esta skill é a cópia que roda do "Padrão de enriquecimento do
Destinos ES" (arquivo de leitura: `claude/padrao-enriquecimento-destinos-es.md` no projeto Site
Destinos ES (Novo)). Regra mudou num, muda no outro no mesmo dia. Vale para os seis modelos de
lote (Passo 1); o modelo muda só a fonte e o escopo — fases, critérios, fotos, curadoria e aviso
são sempre os mesmos:

escopo e custo → auditoria → plano (ok) → teste no primeiro local → execução → fotos tratadas →
textos e tags → curadoria automática → fila de curadoria → checagem de fechamento, aviso e registro.

**Todo lote termina com a curadoria (Passo 9) e o aviso de checagem (Passo 10)**, sem Mário
precisar pedir (regras de 19/11/2026).

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

Primeiro, dizer qual é o modelo do lote:

| Modelo | Quando | Escopo da curadoria |
|---|---|---|
| A · Ponto ou fila | completar pontos turísticos com lacunas | o ponto e os vinculados novos |
| B · Cidade | enriquecer um município inteiro (varredura por centros e por tipo) | todos os locais do município, antigos inclusive |
| C · Lista externa | associados de entidade, CNPJ da Receita, lista de parceiro | os locais da lista e as duplicatas achadas |
| D · Plataforma | notas do Booking/Hotels.com, WhatsApp oficial, Instagram | os locais tocados |
| E · Fonte editorial de fotos | livro (100 Praias), portal de prefeitura, programa de TV | os locais que receberam foto |
| F · Vínculos | pontos turísticos sem locais relacionados | o ponto e os vinculados |

Depois, a estimativa de custo do Google (tabela da API antiga: buscas, detalhes e fotos;
franquia mensal de 5.000 buscas e 5.000 detalhes — o custo real fica nas fotos) e do plano
Claude (lote grande = várias sessões). Vai no plano (Passo 7).

Entrada aceita no modelo A: um ponto (nome ou id), um município, uma região, ou "fila".
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
2. Buscar pelo servidor (rotas que funcionam desde 14/11/2026):
   `GET /api/google-api/place/nearby?latitude&longitude&radius&use_cache` (as 4 categorias de uma
   vez, até ~300 lugares por chamada) e `GET /api/google-api/place/textsearch?query&language&region`
   (20 por consulta: tipo + localidade); detalhe por `GET /api/google-api/place/details?place_id`.
   `/api/mapa/external-nearby-places*` devolveu zero em 14/11: não usar. Modelo B: varrer por
   centros (sede, bairros, orla, distritos, vilas) e por tipo em cada centro.
   O site mostra a distância de cada vinculado, então ela tem de ser real.
3. Filtrar:
   - aberto/operando; dentro do ES e no município certo (endereço do Google e coordenada;
     cuidado com homônimos: bairro São Mateus em SP, Mucuri-BA, Martins-RN); registrar a
     distância até o ponto;
   - **Onde comer**: 4,0+ com 10+ avaliações. Sede de cidade com mais de 100 mil habitantes:
     restaurante 4,2+ com 20+ (ou 4,0+ com 80+); bar, padaria, lanchonete, açaí e sorveteria
     4,2+ com 40+. Vila ou zona rural com menos de 3 opções que passem: 4,5+ com 5+;
   - **Onde ficar** (hotéis, pousadas, chalés, campings): aberta com 5+ avaliações, sem corte
     de nota; sem motel, salvo lista de associado (modelo C) ou pedido de Mário;
   - **Serviços**: o essencial por localidade. Sede: até 4 farmácias, 3 postos, 3
     supermercados, 4 bancos ou caixas 24h, hospital/UPA, delegacia ou polícia, rodoviária.
     Distrito ou vila: 1 a 2 de cada;
   - **O que fazer**: atrações que ainda não existem na base. Se parecer relevante como
     ponto turístico, só **sugerir** a promoção — não marcar `pontoturistico` sozinho.
     Lembrar que a promoção muda a contagem de atrações da cidade no site (ex.: o Grande Buda,
     id 6251, está no carrossel da home mas não é ponto turístico, e Ibiraçu aparece com zero).
4. Deduplicar contra a base: mesmo `cid`/place id, ou nome normalizado (sem acento, sem
   "restaurante/pousada/hotel/café") a até 250 m. Já existe → não cria: completa e vincula.
5. Todo local vinculado precisa de categoria com `tipo_categoria` (O que fazer · Onde comer ·
   Onde ficar · Serviços): sem isso o site o esconde. O site também esconde vinculado com o
   mesmo nome do ponto.
6. Vínculos (todo modelo): cada local vai para os pontos turísticos a até 10 km (15 km em serra
   e zona rural), no máximo 8 pontos por local, os mais próximos; ponto novo ou sem relacionados
   recebe todos os locais do raio. Só no modelo A valem as metas por ponto: até 5 comer, 3 ficar,
   4 serviços, 3 fazer.
7. Nunca inventar estabelecimento: só entra o que veio da busca, com endereço e coordenadas.
8. **Ficha mínima de todo local novo ou completado**: título do Google em português sem sufixo
   de SEO; endereço e coordenadas; categoria com tipo, a mais representativa primeiro; celular
   de 9 dígitos começando por 9 como WhatsApp (fixo só com link wa.me no site do lugar); site do
   próprio lugar; horário no formato do painel; faixa de preço pelo price_level; nota, total e
   link do Google no resumo de avaliações (Booking e Hotels.com em `breakdown_data`: nota,
   avaliacoes, link, coletado_em — só o que bate em nome e cidade); resumo de card e tags
   (Passos 5 e 6); fotos (Passo 4); vínculos (item 6); verificação desmarcada com a observação
   no formato do Passo 8.

## Passo 4 — Fotos (NX Fotos primeiro, Google depois, sempre com crédito e tratadas)

O site mostra legenda e crédito em cada foto e promete imagens "sempre creditadas".

Vale para **todo local e todo modelo de lote**, não só ponto turístico: restaurante, hospedagem,
serviço ou atração sempre passa primeiro pelo NX Fotos. Origem, nesta ordem (decisão de Mário,
19/11/2026): NX Fotos (Claude escolhe as melhores) → Google com autor → outros meios, quando os
dois não bastam: Instagram do próprio local, parceiro com cessão por escrito (prefeitura, livro,
programa) e guia cadastrado. Nunca busca de imagens da web nem imagem de IA em lugar real.
**Instagram do local**: só fotos publicadas pelo perfil oficial do estabelecimento ou da
atração, que mostrem o lugar (nada de repost de cliente ou de influenciador, nem foto de agência
ou banco de imagem); crédito "@perfil / Instagram". Escolha pontual, perfil a perfil, no Chrome
de Mário — sem varredura em massa, porque o Instagram bloqueia robôs. O instagram.com precisa
estar liberado na extensão (em 14/11 o acesso foi barrado pela permissão da sessão).
Toda foto que a rodada sobe passa pelo tratamento (item 7), ganha a marca no nome do arquivo
(item 3) e fica com cópia local (item 2). Mínimo de 5 fotos em ponto turístico (máximo 12) e 3
nos demais locais (do Google, até 3 por local).

1. **Escolher no NX Fotos** (MCP `NXFOTOS`): `buscar` com `q` = nome do ponto; depois nome +
   município; depois `sugestoes_de_filtro` para achar o `local` exato; olhar com
   `mostrar_imagens`. Aceitar só fotos que sejam do lugar (título, descrição, tags ou
   geolocalização batem). Preferir horizontal, largura ≥ 1600, licença `rf`. Até 4 novas por
   ponto; total do ponto até 12.
2. **Cópia local obrigatória** (toda foto fica em mapas.nx.tv.br; nunca anexar endereço do CDN
   do NX Fotos nem do Google direto — as 42 fotos de Conceição da Barra de 14/11 que apontam
   para o CDN vão para a fila de curadoria). As rotas de importação do painel
   (`/api/photoprism/*`) e a gravação de foto do Google pelo servidor estão quebradas (pedido
   ao Brendew): não usar até ele avisar.
   - **Google**: `GET /api/google-api/photo?photo_reference&maxwidth` → tratar no canvas →
     `POST /api/upload-image` (campo `image`) → `POST /api/mapa/{id}/images` (`source: upload`).
   - **NX Fotos (caminho que funciona desde 17/11/2026)**: o CDN do NX Fotos não libera leitura pelo
     mapas (sem CORS). Numa aba do mapas logada, `window.open` da imagem do CDN; na aba do
     CDN, `fetch('/pub/...@w1600.webp')` e `window.opener.postMessage({key, blob},
     'https://mapas.nx.tv.br')`; na aba do mapas, tratar o blob no canvas (item 7), subir por
     `POST /api/upload-image` (campo `image`) e anexar com `POST /api/mapa/{id}/images`
     (`source: upload`). Assim a foto fica tratada e com cópia local.
3. Campos de cada foto nova: `alt_text` "<título> — <município> (ES)", `legenda` = descrição
   da foto, **`autoria` obrigatória** (NX Fotos: `author`; Google: nome do colaborador que vem
   na própria foto, no formato "Nome / Google Maps"; Instagram do local: "@perfil / Instagram";
   parceiro ou guia: "Nome / instituição"),
   `is_main: false` e `file_name` com a **marca de tratamento**:
   `{id}-{slug}-{origem}-{n}-t{k×10}.jpg` (origem nx, google, instagram, parceiro ou guia; ex.:
   `3206-praia-da-bugia-nx-1-t8.jpg`; `t0` = analisada e dispensada). É a marca que a curadoria
   usa para saber que a foto foi tratada. Foto do NX Fotos sem autor: "Acervo Next Editorial" e
   pendência de crédito. Não repetir foto já existente.
4. **Google**: só quando o NX Fotos não tiver o lugar. Fotos do Google Places pelo caminho do
   item 2 (nunca pela importação automática do sistema, que sobe sem tratamento), com crédito.
   **Não usar** `/api/google-images` (busca de imagens da web, direitos desconhecidos).
5. **Fotos antigas sem crédito**: preencher `autoria` (`PUT /api/mapa/{id}/images/{imgId}`)
   só quando o autor for conhecido com certeza; senão, listar no relatório.
6. **Foto principal**: trocar só se não houver principal, ou se a atual for Google ou imprópria
   e houver NX Fotos do lugar horizontal ≥ 1600 (`POST /api/mapa/{id}/images/{imgId}/set-main`).
   Na rodada, a troca entra no plano; na curadoria (9.2), é feita direto.
7. **Tratamento (regra de Mário, 11/11/2026, todas as rotinas)**: analisar cada foto. Se
   estiver crua, tratar no padrão das revistas impressas: mais viva, um pouco mais cítrica e
   quente, azuis mais quentes. Se já estiver tratada e boa, não mexer. Receita usada em
   17/11/2026 (k = 1 para foto crua de câmera, 0,8 para celular, 0,6 para foto já viva):
   contraste ×(1+0,09k) em torno de 0,5; vivacidade 0,55k×(1−saturação); R ×(1+0,04k),
   G ×(1+0,022k), B ×(1−0,012k); nos azuis (d = B−R > 0) G +0,05k·d e B −0,01k·d;
   gama 1−0,05k; JPEG 0,9. Não tirar azul do céu: esquentar puxando para o turquesa.
   k = 0 quando a foto já está tratada e boa: sobe sem mexer, com `t0` no nome. Google entra
   com k = 0,8. Foto antiga já cadastrada sem marca, sem crédito ou fora da cópia local não é
   apagada pela rodada: vai para a fila com a proposta de troca pela versão tratada; com o
   "sim" de Mário, sobe a nova e apaga a antiga, conferindo depois.
8. **Não repetir foto** (nem no mesmo local, nem em locais diferentes): antes de anexar,
   comparar cada candidata com as fotos que o local já
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
2. Serviços ficam sem tag. Tags de comodidade (TV, wi-fi, ar-condicionado, estacionamento etc.) não aparecem no site:
   não gastar a rodada com elas nos pontos turísticos.
3. **Primeira categoria = selo do card**: a mais representativa vem primeiro (ex.: "Cachoeira"
   antes de "Estacionamento"). Propor a reordenação quando estiver errada.

## Passo 6 — Textos (prompts da casa)

**Resumo de card de local** (restaurante, hospedagem, serviço, atração simples): uma frase
escrita a partir do tipo, da localidade conferida pela coordenada e do que se repete nas
avaliações do Google; sem nota, sem preço, sem comodidade inventada; tom neutro quando as
avaliações são ruins. Pode sair do prompt da casa no servidor com as avaliações no conteúdo,
revisando uma amostra antes de gravar em massa.

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

O plano traz o modelo do lote (Passo 1) e a estimativa de custo, e avisa que o lote fecha com a
curadoria (Passo 9) e o aviso de checagem (Passo 10). O ok do lote vale também para as
correções seguras dela (9.2); as decisões da curadoria vão para a fila, não para este ok.

Execução agendada / sem Mário presente: fazer auditoria e plano, não gravar, entregar o plano.

## Passo 8 — Aplicar (após o ok)

Ordem: teste no primeiro local → novos locais → vínculos → fotos → tags e categorias → textos →
verificação → curadoria (Passo 9) → checagem de fechamento, aviso e registro (Passo 10).

**Retomada**: o progresso fica no localStorage da aba, numa chave por lote (`DET_<sigla>`), por
place_id. Se o computador dormir ou a aba recarregar, recriar as funções e rodar de novo: o que
já foi criado é pulado. Computador acordado, Chrome aberto e painel logado são pré-requisitos.

1. Novo local: `POST /api/mapa` com `title`, `address`, `latitude`, `longitude`,
   `municipio_id`, `categories` (com tipo), `pontoturistico:false`, `telefones`/`websites`/`emails`
   se vierem e `open_hours` no formato do painel quando o Google trouxer horário:
   `{"type":"simple","simple_text":…,"regular_hours":{"monday":{"enabled":true,"periods":[{"open":"08:00","close":"18:00"}]},…},"fechado_feriados":false,"agendamento_necessario":false,"notes":…}`.
2. Vincular ao ponto: `POST /api/admin/all-locations/{novoId}/local-secundario`
   `{local_primario_id: pontoId}`.
3. Conferir se entrou como **pendente** em `GET /api/revisao/estabelecimentos`. Se não entrou,
   marcar `PUT /api/mapa/{novoId}/verificacao` `{verificado:false, observacoes}`. Observação
   padrão, uma linha por assunto (a de curadoria sempre a última; limite ~1.000 caracteres):
   `Inserido pela rotina de atualização em dd/mm/aaaa (fonte; nota X com N avaliações) — revisar`;
   em hospedagem casada com a Receita, `Receita Federal (base mm/aaaa): CNPJ … · razão social …
   · nome fantasia … · CNAE principal/secundário · ativa, início em …` (nunca CPF);
   `Curadoria dd/mm/aaaa: <nível> · pendências: …` (9.4).
   **Nunca aprovar na fila de revisão sem Mário mandar.**
4. Fotos e créditos: Passo 4.
5. Tags, categorias e textos: `GET /api/mapa/{id}` → mesclar só o que foi aprovado →
   `PUT /api/mapa/{id}` com o objeto completo no formato do painel (nunca PUT parcial). No
   primeiro ponto da execução, reler a ficha e confirmar que nenhum outro campo mudou antes
   de seguir.
6. Rodar uma vez, sem retentativa cega: erro → registrar e seguir para o próximo ponto.

## Passo 9 — Curadoria (padrão ao fim de todo lote)

Regra de Mário (19/11/2026): todo enriquecimento em lote (cidade, região, lista ou fila) termina
com a curadoria, sem ele precisar pedir. Escopo: **todos os locais do escopo do lote**, não só os
que a rodada criou, conforme o modelo (tabela do Passo 1): A, o ponto e os vinculados novos;
B, a base inteira do município, antigos inclusive; C, os locais da lista e as duplicatas achadas;
D, os locais tocados; E, os locais que receberam foto; F, o ponto e os vinculados. Lotes
anteriores a 19/11 (Conceição da Barra, Sindihotéis-ES, CNPJs de hospedagem) passam pela
curadoria na próxima rodada de cada cidade. Foto bonita de lugar fechado, duplicado
ou na cidade errada é pior do que nenhuma: a curadoria cobre o lugar, os dados e as fotos.

### 9.1 Checagens

| Camada | O que conferir |
|---|---|
| Lugar | existe e está aberto (situação no Google; hospedagem também pelo CNPJ ativo da observação) |
| Lugar | está no município certo (município do endereço do Google × `municipio_id`; coordenada dentro do município) |
| Lugar | não é duplicata (mesmo cid/place id, ou nome normalizado a até 250 m) |
| Lugar | merece estar no site (critérios de nota do Passo 3; sobra de importação sem dados; tema que não é lugar) |
| Dados | coordenadas, endereço, categoria com tipo e primeira categoria representativa |
| Dados | telefone (celular de 9 dígitos começando por 9 = WhatsApp), horário, site que abre e é do próprio lugar |
| Dados | resumo do card (`ai_description` ou `about`) presente, sem nota e sem comodidade inventada; título sem sufixo de SEO |
| Dados | tags verdadeiras (nada de "Cachoeiras" em rio nem tag de comodidade em praia ou igreja) |
| Fotos | principal existe, é horizontal e mostra o lugar; sem logo, selfie, texto por cima ou paisagem que não é do lugar |
| Fotos | todas com `autoria`, `legenda` e `alt_text`; nenhuma repetida (hash 16×16, distância ≤ 20); todas com marca de tratamento no nome do arquivo e cópia local em mapas.nx.tv.br |
| Fotos | mínimo de 5 em ponto turístico e 3 nos demais locais |
| Fotos | origem da principal, nesta ordem: NX Fotos → Google com autor → outros meios (Instagram do próprio local, parceiro com cessão por escrito, guia); imagem de IA nunca em lugar real |

- **Folha de contato**: no ambiente de trabalho, montar grades de ~40 fotos principais (miniatura,
  id e nome) e olhar cada grade. É o jeito barato de achar logo, selfie e foto que não mostra o
  lugar.
- **Situação no Google**: os locais criados na rodada já vêm conferidos; os antigos pedem um
  detalhe cada (sem place id: busca por texto + detalhe, conferindo o cid, como no método de
  17/11). Cabe na franquia mensal de 5.000 detalhes. A curadoria não compra foto nova.

### 9.2 O que a curadoria corrige sozinha (coberto pelo ok do lote)

Só o que não apaga nada e se desfaz:
- crédito, legenda e alt de foto quando o autor é conhecido com certeza;
- foto principal: definir quando falta; trocar quando a atual é imprópria, ou é do Google e o
  NX Fotos tem foto do lugar horizontal ≥ 1600. A rodada escolhe sozinha, pela beleza, pela
  informação que a foto traz e pela atualidade (Mário não quer escolher foto), e lista a troca
  no relatório;
- ordem das categorias e título sem sufixo de SEO;
- celular marcado como WhatsApp pelo critério acima;
- situação "Fechado permanentemente" só quando os sinais concordam: Google fechado e nenhuma
  avaliação nos últimos 12 meses (hospedagem: também nenhum CNPJ ativo). Sinais em conflito
  (ex.: Google fechado e hóspede recente) → fila;
- o registro do nível (9.4).

Execução agendada ou sem Mário presente: checar e montar a fila, sem gravar (como no Passo 7).

### 9.3 Fila de curadoria (decisão de pessoa)

Vai para a fila o que apaga, junta ou é dúvida: duplicata, local fora do município, coordenada
suspeita, fechado com sinais em conflito, foto imprópria ou repetida a apagar, tag errada, sobra
de importação sem dados, local sem correspondência no Google, foto antiga a trocar pela versão
tratada (sem marca, sem crédito ou fora da cópia local), divergência de crédito entre fontes,
candidato a ponto turístico e candidato a destaque.

- **Onde**: planilha "Fila de curadoria — Destinos ES" (tipo Sheets do Artifact; se a sessão não
  oferecer, .xlsx enviado no chat), criada na primeira rodada, com uma aba por lote
  ("<cidade> — dd/mm"). Registrar o link em `claude/curadoria-destinos-es.md` no projeto
  Site Destinos ES (Novo).
- **Colunas**: id · local · painel (`/admin/locais/{id}/edicao`) · página pública · camada ·
  problema · proposta · decisão (sim / não / outra) · quem decidiu · observação. Pontos
  turísticos primeiro, depois o que mais aparece no site.
- **Aplicar**: quando Mário mandar ("aplica a curadoria de <cidade>") ou na próxima rodada da
  mesma cidade, ler a coluna decisão e executar só as linhas com "sim" decididas por Mário ou por
  quem ele designar. Duplicata decidida: completar o cadastro que fica (dados, fotos e vínculos
  que faltam nele) e listar o outro para Mário apagar no painel — a skill nunca apaga local.
  Apagar foto segue a regra de ordem expressa (Regras invioláveis).

### 9.4 Nível de cada local

| Nível | Quando |
|---|---|
| bruto | falha em alguma checagem do lugar, ou está sem categoria com tipo ou sem coordenadas |
| conferido | passou nas checagens do lugar e dos dados, tem foto principal adequada com crédito e resumo de card; pode faltar quantidade de fotos |
| curado | conferido e aprovado por pessoa na fila; só aí `verificado = true` |
| destaque | escolha editorial de Mário (livro 100 Praias, experiência assinada por guia, vitrine); a skill só propõe |

- **Onde gravar** (até o mapas ter campo próprio): uma linha no fim da observação da
  verificação, substituindo a linha de curadoria anterior, sem tirar o resto (CNPJ, "Inserido
  pela rotina…"): `Curadoria dd/mm/aaaa: conferido · pendências: fotos 2/3, horário`. Limite do
  campo: ~1.000 caracteres. O PUT da verificação regrava "verificado por" e a data: mandar
  `verificado` com o valor que já estava.
- A rodada nunca marca `verificado = true` por conta própria.
- **Pedido ao Brendew** (repetir no relatório até existir): campos de nível, curado por e curado
  em; marca de foto principal aprovada; tela de fila de curadoria no painel (a revisão de
  estabelecimentos pode servir de base); e o site usar o nível — destaque e curado primeiro na
  vitrine, bruto fora dos trilhos e do Guia com IA.

### 9.5 No relatório do lote

Quantos locais ficaram em cada nível (e a comparação com a curadoria anterior da cidade, se
houver), correções feitas pela curadoria, tamanho da fila com o link e as 5 decisões que Mário
deve olhar primeiro.

## Passo 10 — Conferir no site, checagem de fechamento, aviso e registro

1. Abrir `https://mapas.nx.tv.br/publico/destino/{id}` e confirmar: foto principal, crédito
   das fotos, blocos e informações importantes, vinculados com distância.
2. Conferir `?lang=en` e `?lang=es` (tradução pendente vai para o relatório).
3. Relatório por ponto: o que foi inserido, vinculado, fotografado, creditado, etiquetado e
   escrito; o que ficou pendente e por quê; em quais experiências do site o ponto passou a
   aparecer. Comparar os totais com a linha de base do Passo 2.
   Links: página pública, `https://mapas.nx.tv.br/admin/locais/{id}/edicao` e
   `https://mapas.nx.tv.br/admin/revisao-estabelecimentos` (pendentes para aprovar).
   O histórico de cada local fica em `/admin/locais/{id}/historico`.
4. Fechar o relatório com o bloco da curadoria (9.5) e o link da fila.
5. **Checagem de fechamento** (antes do aviso). O lote só é dado como concluído se passar tudo:
   1. 100% dos locais do escopo com a linha de curadoria do dia;
   2. nenhuma foto subida pela rodada sem autoria, legenda, alt ou marca de tratamento, nem
      fora da cópia local;
   3. nenhum local novo sem categoria com tipo ou sem coordenadas;
   4. fila gravada, com link que abre;
   5. amostra de 10 páginas públicas conferidas (3 pontos turísticos + 7 sorteados): foto
      principal, créditos, resumo, vinculados com distância;
   6. modelo B: total de lugares da página da cidade bate com a base.
   Se algo falhar, o aviso sai como "curadoria incompleta", com o que faltou e por quê.
6. **Aviso de checagem**: no chat (mensagem final; em sessão sem Mário, por SendUserMessage) e
   como notificação no celular pelo app Claude (PushNotification, quando a sessão tiver). Sem
   e-mail (regra de 27/10/2026). A notificação leva só a primeira linha, os níveis e o tamanho
   da fila. Sempre neste modelo:
   ```
   Curadoria concluída · <cidade ou lote> · modelo <A–F> · dd/mm/aaaa
   Escopo: N locais (N novos, N completados, N antigos)
   Níveis: N destaque · N curados · N conferidos · N brutos (antes: …)
   Correções automáticas: N créditos · N principais · N WhatsApp · N títulos · N fechados
   Fotos: N subidas, todas tratadas, creditadas e com cópia local · N locais abaixo do mínimo
   Fila: N decisões → <link>
   Olhe primeiro: 1) … 2) … 3) … 4) … 5) …
   Pendente com o Brendew: …
   Custo: Google US$ … de tabela · real ≈ US$ …
   ```
7. **Registro no projeto** Site Destinos ES (Novo): um doc por cidade ou lote,
   `claude/enriquecimento-<cidade-ou-lote>.md` (rodada nova da mesma cidade = seção nova), com
   as seções Pedido e aprovação · Execução · Números antes e depois · Curadoria · Custo ·
   Pendências · Decisões de Mário. Link da fila em `claude/curadoria-destinos-es.md`; pedidos
   ao Brendew em `claude/mapas-nx-estrutura-e-auditoria.md`.

## Regras invioláveis

- Nunca apagar locais, fotos ou vínculos (`DELETE` fora de questão) nem desmarcar ponto turístico.
  Única exceção, e só com ordem expressa de Mário na hora: apagar foto que a própria rodada
  criou (cópia repetida, versão sem tratamento trocada pela tratada, foto imprópria) com
  `DELETE /api/mapa/{id}/images/{imgId}`, conferindo depois que a original continua.
- Nunca subir foto sem tratamento e sem a marca no nome do arquivo (Passo 4, itens 3 e 7), nem
  anexar foto fora da cópia local (endereço do CDN do NX Fotos ou do Google direto).
- Nunca dar o lote por concluído sem a checagem de fechamento (Passo 10, item 5).
- Nunca sobrescrever texto preenchido sem pedido explícito.
- Nunca aprovar/recusar na fila de revisão sem ordem de Mário.
- A curadoria nunca apaga, desvincula nem marca `verificado = true` sozinha: verificado só com
  decisão de Mário (ou de quem ele designar) na fila de curadoria.
- Nunca criar, renomear nem desativar tag ou categoria sem decisão de Mário (selo novo, como o
  do Sindihotéis-ES, é decisão dele).
- Nunca gravar foto sem crédito, nem foto de busca de imagens da web.
- Nunca gravar tradução à mão.
- Nunca digitar senha nem criar conta; sem sessão, parar e pedir login.
- Respeitar 120 req/min.
- Nunca inventar dados de estabelecimento, telefone, horário ou preço.