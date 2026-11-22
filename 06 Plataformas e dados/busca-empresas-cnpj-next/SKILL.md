---
name: "busca-empresas-cnpj-next"
description: "Busca de empresas pela API do CNPJ Aberto (CNPJ, razão social, situação, CNAE, endereço, contato, sócios, empresas por cidade) em tudo da Next. Diz onde fica a chave: na memória, nunca na skill."
---

# Busca de empresas — API do CNPJ Aberto

Use sempre que uma conversa, rotina ou skill da Next precisar de dados de empresa: CNPJ, razão social,
nome fantasia, situação cadastral, atividade (CNAE), endereço, telefone, e-mail, sócios, filiais ou a
lista de empresas de uma cidade ou atividade. Vale para todas as frentes: ES Brasil, Comunhão, Destinos
ES, Prócidade, Datafé, comercial e Nextor. Decisão de Mário em 22/11/2026 (no ChatGPT, a mesma API
entra por uma ação de GPT configurada por ele).

Responder sempre em português do Brasil.

## 1. Chave

- **A chave não fica nesta skill.** As skills sobem para o repositório público do GitHub. A chave fica só
  na memória do Claude, no arquivo `/areas/cnpj-aberto-api.md` (no projeto Site Destinos ES (Novo), também
  em `areas/cnpj-aberto-api.md` da memória do projeto).
- Ler com `memory_read`. Sem o arquivo: não chamar a API; seguir com o Nextor (`lookup_cnpj`,
  `enrich_cnpj`) e com a web, e registrar a pendência "CNPJ Aberto: chave não salva na memória
  (/areas/cnpj-aberto-api.md)".
- No shell, guardar a chave numa variável de ambiente (`CNPJ_ABERTO_KEY`) e mandá-la só no cabeçalho.
  Nunca imprimir a chave nem escrevê-la em skill, doc, matéria, carta, resumo, notificação, commit,
  Google Drive ou registro da Ponte Next.
- Trocar a chave: Mário pede, numa conversa comum (fora de projeto), para atualizar
  `/areas/cnpj-aberto-api.md`. Nada muda nas skills.

## 2. Ordem da busca de empresa

1. Assunto comercial (carta, proposta, prospecção, cadastro): primeiro o Nextor (`search_internal` ou
   `search_clients`), para saber se a empresa já é cliente, lead ou contato da casa.
2. Dados cadastrais: CNPJ Aberto (seção 3).
3. O que a Receita não tem (marca, produtos, notícias, redes, site): web.

Busca de pessoa (não empresa) segue a regra própria de Mário: agenda de contatos, depois web, depois
Nextor.

## 3. Rotas (testadas em 19 e 22/11/2026)

Base `https://cnpjaberto.com.br`, chave no cabeçalho `X-API-Key`. Respostas em JSON.

| Rota | Para quê |
|---|---|
| `GET /api/cnpj/{cnpj}` (14 dígitos, só números) | ficha completa: razão social, natureza jurídica, capital, porte, Simples/MEI, sócios e, por estabelecimento, situação e data, início de atividade, CNAE principal e secundários, endereço, telefone, e-mail |
| `GET /api/cnpj/{cnpj}/filiais` | filiais |
| `GET /api/busca-avancada` | lista por filtros: `nome_empresa` (4 ou mais letras), `uf`, `municipio` (nome em maiúsculas e sem acento, ex.: SAO MATEUS), `cnae` (7 dígitos; filtra só a atividade principal), `situacao=ativa`, `page`, `per_page` (até 50). Exige ao menos nome, cidade, CNAE, CNPJ parcial ou CEP; não traz telefone nem endereço (para isso, a ficha de cada CNPJ) |

```bash
curl -sS -H "X-API-Key: $CNPJ_ABERTO_KEY" "https://cnpjaberto.com.br/api/cnpj/47940902000171"
curl -sS -H "X-API-Key: $CNPJ_ABERTO_KEY" \
  "https://cnpjaberto.com.br/api/busca-avancada?uf=ES&nome_empresa=next%20editorial&per_page=20"
```

A documentação lista outras rotas gratuitas (`/api/socio/empresas`, `/api/socios/busca`,
`/api/cnae/{codigo}/stats`, `/api/municipios-por-uf`, `/api/municipios/search`, `/api/intelligence/rede`)
com parâmetros ainda não testados: conferir em https://cnpjaberto.com.br/api-docs antes de usar.

## 4. Limites do plano (gratuito, conferido em 22/11/2026)

- **200 requisições por dia para a conta inteira**, somando todas as rotinas e conversas do Claude e do
  ChatGPT. Cada consulta conta; não repetir consulta já feita.
- Busca avançada: só os 20 primeiros resultados. Busca por telefone ou e-mail e as rotas por cidade,
  endereço e contato (`/api/empresas-cidade`, `/api/endereco/empresas`, `/api/contato/empresas`) são do
  plano Pro (R$ 47/mês: 10.000 por dia e 50.000 por mês).
- Em 429 (cota do dia): parar o CNPJ Aberto naquele dia, seguir com o Nextor e a web, e avisar na nota da
  rodada.
- Cache: a base muda uma vez por mês. Guardar as respostas em arquivo na pasta de trabalho e reaproveitar
  no mês.
- Na nota ou no relatório da rodada, uma linha: "CNPJ Aberto: N consultas nesta rodada". Nunca a chave.

## 5. Cuidados

- Sócios: CPF parcial e faixa etária nunca vão para matéria, carta, documento público, Nextor ou
  registro. Nome e qualificação de sócio só quando a pauta pedir.
- MEI antigo traz CPF na razão social: retirar antes de gravar em qualquer lugar.
- "Ativa" na Receita não prova que o negócio funciona: para uso público (ex.: Destinos ES), confirmar no
  Google.
- Citar a fonte com a data da base: "Receita Federal via CNPJ Aberto (base mm/aaaa)".
- Antes de cadastrar empresa nova no Nextor (`create_client`), conferir aqui razão social, CNPJ e
  endereço.

## 6. Onde já se usa com regras próprias

- `atualizacao-mapas-destinos-es`: modelos cidade e lista externa e curadoria do mapas (casamento de
  cadastro com CNPJ, linha da Receita na observação).