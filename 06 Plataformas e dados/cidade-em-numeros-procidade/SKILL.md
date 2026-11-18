---
name: "cidade-em-numeros-procidade"
description: "Gera o site \"{Cidade} em Números\" (Prócidade, by NextLab) para um município do ES a partir do modelo de Conceição da Barra e Piúma, com as mesmas fontes, NX Fotos, mapa com relevo e ligação ao Destinos ES."
---

# Cidade em Números (Prócidade)

Use quando Mário pedir um site "{Cidade} em Números" ou disser "faz igual ao de Conceição da Barra / Piúma para {cidade}". O site é um produto Prócidade, conectado ao ES em Números, by NextLab, no Lovable (workspace Mario2). Responder sempre em pt-BR.

## Modelo

- Remixar o projeto mais novo: **Piúma em Números** (`ba2d01b2-9467-440e-8df4-2a6522e9e37c`). Ele já tem a camada de área urbanizada e a ligação com o Destinos ES. O original é **Conceição da Barra em Números** (`a03465d6-3b84-4138-946c-b21759b79baa`).
- A estrutura, o layout, os coletores e as fontes ficam iguais. Tudo o mais é da nova cidade: números, textos, fotos, vídeos, mapa, relevo, brasão, cores do brasão, créditos e testes.
- Logo depois do remix, reescrever o conhecimento do projeto (`set_project_knowledge`) com os dados da cidade e as regras da casa abaixo.

## 1. Identificação da cidade

Levantar e guardar num arquivo de trabalho:
- código IBGE (7 dígitos), código TSE do município e zona eleitoral;
- distritos oficiais e sede, gentílico, área (IBGE, divulgação mais recente), densidade (Censo 2022) e distância de Vitória em linha reta;
- prefeito e câmara atuais (conferir na web);
- **Destinos ES**: id e slug do município em `GET https://mapas.nx.tv.br/api/mapa/municipios` (leitura pública, CORS aberto, até 120 requisições por minuto).

## 2. Dados (mesmas fontes do modelo)

- **IBGE/SIDRA:** estimativa de população (6579), PIB dos municípios (5938), nascidos vivos (2609), óbitos (2683/2654), casamentos e divórcios do registro civil, Censo 2022 (cor ou raça 9605 e as demais tabelas que o modelo usa), religião (Censo 2010, tabela 137).
- **API servicodados do IBGE:** PIB per capita (pesquisa 38, indicador 47001) e mortalidade infantil (pesquisa 39, indicador 30279).
- **Tesouro Nacional, Siconfi:** RREO Anexo 01 com `id_ente` = código IBGE. Município pequeno pode só ter `co_tipo_demonstrativo=RREO Simplificado`.
- **Aequus, anuário Finanças dos Municípios Capixabas** (edição mais recente): receita, despesas, royalties, IPM e ranking entre os 78.
- **IJSN, Sumário de Informações Criminais** (ano mais recente): taxas e posição no ES.
- **Sesa, deliberações CIR/CIB** (`saude.es.gov.br/media/CIB/deliberacoes/cir_cib-NNN.pdf`): emendas para a saúde.
- **App de eleições da Next** (ES Eleicoes 26): totais (`unit_totals`, unit_key = código TSE), resultados e vereadores eleitos.
- **Economia em Números (dados do Portal da Transparência):** Bolsa Família.
- **Obras do Governo do Estado na cidade:** valores divulgados oficialmente. Se entrarem estimativas ou preço máximo de licitação, o texto diz "ordem de grandeza".
- **Notícias:** portal da prefeitura (muitos bloqueiam robô; aí o coletor fica pendente) e Google Notícias.

Sem dado oficial, o card fica pendente. Nunca inventar número.

## 3. Mídia

- **Fotos do NX Fotos:** Claude escolhe sozinho, por beleza, informação da foto e atualidade. São 5 para a capa e 15 para a galeria, com crédito "Foto: Autor / NX Fotos".
  - `link_do_original` aceita cerca de 4 chamadas por minuto e o link vale 15 minutos.
  - Baixar um arquivo por vez e conferir cada um abrindo com o PIL.
  - Tratar e exportar em webp nos tamanhos 2400 (capa), 1600 e 640.
- **Vídeos do NX Fotos:**
  - capa: 4 trechos com transição de 0,5 s, cerca de 16 s;
  - faixa da cidade: 1 trecho de 10 s.
  - Exportar em H.264 com CRF 28, faststart e sem áudio. A capa sai em 1080 e 720 e a faixa em 720, cada um com sua imagem de pôster.
- **Brasão:**
  - versão colorida com fundo transparente, removendo o branco fora do escudo;
  - versão em silhueta branca.
  - Citar a lei do brasão só se ela for localizada; senão, escrever "símbolos oficiais".
- Enviar tudo num zip por `get_file_upload_url` com PUT. O agente do Lovable registra cada arquivo com `lovable-assets create`.

## 4. Mapa

- **Limites:** usar o PDF de divisão administrativa do Geobases (`one.s3.es.gov.br/pr-geobases-public/DIVISAO_ADMINISTRATIVA_ES/{Municipio}.pdf`), vetorizado em contorno, limites distritais e águas.
- **Área urbanizada:** IJSN.
- **Coordenadas:** UTM 24S (EPSG:31984), com uma transformação afim para o viewBox do SVG.
- **Águas e área urbana** sempre com `fill-rule="evenodd"`.
- **Relevo:** gerar a partir de blocos terrarium (AWS Terrain Tiles, SRTM), com sombreamento, exagero vertical e legenda de altitude mínima e máxima. Fica recortado no contorno, com versões de 2000 e 1000 px e uma chave "relevo" no mapa.
- **Praias e atrações:**
  - posição pelo OpenStreetMap ou Nominatim, com user agent genérico (nunca e-mail) e no máximo 1 chamada por segundo;
  - nomes por guia confiável;
  - rótulos sem sobreposição em 390 px e em 1440 px.

## 5. Destinos ES no mapa

Todo destino do mapa liga à ficha do Destinos ES, o guia turístico da Next. Vale para praia, ilha, atração e o distrito que tenha ficha.

1. **Pontos da cidade:** `GET https://mapas.nx.tv.br/api/mapa/filtrar?pontoturistico=true&municipio_id={id}&per_page=100`. Para outros "O que fazer" do município, a mesma chamada sem `pontoturistico`.
2. **Casar cada item do mapa com uma ficha**, por nome e por posição. Converter latitude e longitude do Destinos ES para o SVG com a mesma transformação do território e comparar.
   - Na dúvida, não ligar.
   - Ponto do Destinos ES que falta no mapa pode entrar com a posição do Destinos ES.
3. **Slug:** vem do endereço público. `https://mapas.nx.tv.br/publico/destino/{id}` redireciona para `https://destinoses.com/destino/{id}/{slug}`.
4. **Configuração no projeto:** `src/config/destinos.ts`, com `municipioId`, `municipioSlug`, `municipioNome` e UTM `utm_source=procidade&utm_medium=cidade-em-numeros&utm_campaign={slug}`. Cada item do mapa leva `destino: { id, slug }`.
5. **Painel do item selecionado**, lido ao vivo de `GET /api/mapa/{id}`:
   - foto principal com crédito "Foto: Autor / Destinos ES" (nunca foto com autoria do Google Places) e o subtítulo;
   - os blocos o que fazer, onde comer e onde ficar: headline, texto curto e até 3 lugares vinculados mais próximos, com a distância;
   - botão "Ver {lugar} no Destinos ES".
   - Sem serviços, telefones ou avaliações. Se a API falhar, fica só o botão.
6. **Bloco "{Cidade} no Destinos ES":** chips com os pontos turísticos ao vivo e o link `https://destinoses.com/{slug}`.
7. **Fichas magras:** conferir quais fichas estão sem textos ou com poucos lugares vinculados e avisar Mário. A skill atualizacao-mapas-destinos-es enriquece essas fichas.

## 6. Banco e coletores

- **Trocar a carga da cidade anterior por SQL** (`query_database`) nas tabelas indicadores, series, ranking_es, obras, emendas, noticias, eleicoes_totais, eleicoes_resultados, vereadores e fotos.
  - O app lê `series` sem ordenação: inserir a composição da cidade e a do ES na mesma ordem.
  - Tabela `fotos`: as 20 linhas apontam para as URLs dos assets 1600 e 640, lidas dos `.asset.json` do projeto.
  - Tabela `coletores`: atualizar o campo `fonte` com o nome da nova cidade.
- **Coletores:** pedir ao agente que rode sync-ibge, sync-siconfi e sync-noticias e confira os agendamentos, que um remix pode perder. Comparar as séries antes e depois.

## 7. Conferência e entrega

- Busca sem resultado pelos nomes da cidade anterior, dos distritos, das praias, dos códigos e dos prefixos de asset. A única exceção é a cidade anterior quando aparece num ranking estadual.
- Build e testes passando.
- Prévia em 390 px e em 1440 px:
  - capa com vídeo, ticker e cartões;
  - galeria e filtros;
  - mapa com relevo ligado e desligado, rótulos sem sobreposição e painel do Destinos ES;
  - rodapé com o brasão.
- **Nunca publicar sem um "pode publicar" do Mário para aquela versão.** O ok vale só para a versão que ele viu.
- Relatório final curto: o que entrou, os pendentes (dado oficial que faltou, lei do brasão, fichas magras no Destinos ES) e o pedido de ok para publicar.

## Regras da casa

- Nunca caixa alta. Fonte Inter. Ícones Lucide.
- Paleta Prócidade, com o azul do brasão como cor da cidade.
- Todo número leva fonte, período e selo: real, ao vivo, referência ou pendente.
- Números e datas no padrão brasileiro.
- Marcas Prócidade, ES em Números e NextLab: usar as versões oficiais, como no rodapé do modelo, sem inventar versão.
- Negrito em **ES Brasil**, **revista ES Brasil** e **Café com Moqueca** quando aparecerem.