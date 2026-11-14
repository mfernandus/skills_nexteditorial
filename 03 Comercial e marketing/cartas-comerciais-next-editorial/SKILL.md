---
name: cartas-comerciais-next-editorial
description: Gera cartas comerciais de propostas de veiculação no padrão Next Editorial — para ES Brasil, Comunhão, Destinos ES e Prócidade. Use esta skill sempre que o usuário pedir uma carta, proposta comercial, oferta publicitária, oferta de mídia, proposta de patrocínio, carta de prospecção, ou qualquer comunicação dirigida a um cliente/anunciante com proposta de presença editorial — mesmo quando ele não usar literalmente a palavra "carta". Também acione quando ele apenas der os insumos (destinatário + edição + investimento) sem explicitar o pedido. Esta é a skill canônica da casa para o padrão de cartas comerciais Next Editorial.
---

# Cartas Comerciais — Next Editorial

Skill para gerar cartas comerciais de propostas de veiculação nas plataformas da Next Editorial, reproduzindo com fidelidade o padrão editorial, o tom institucional e a identidade visual da casa.

## Quando usar

Aciona-se sempre que houver pedido de:
- Carta/proposta comercial para anunciante ou patrocinador
- Oferta de veiculação publicitária em ES Brasil, Comunhão, Destinos ES ou Prócidade
- Convite formal para participar de uma edição específica
- Carta de prospecção comercial vinculada a um produto editorial
- Resgate ou reapresentação de proposta a cliente existente

Não usar para: cartas institucionais (sem proposta comercial), cartas do editor (editoriais de revista), comunicação interna, comunicação com fornecedores.

## Input mínimo necessário

Antes de gerar a carta, garanta que estes campos estão definidos. Se faltar algum, pergunte de forma agrupada (uma só rodada de perguntas, nunca de uma em uma):

1. **Marca/produto editorial** — qual revista/edição (ex.: "ES Brasil ed. 234 — Especial Aniversário", "Comunhão ed. 326 — Jesus Vida Verão")
2. **Destinatário** — instituição, nome do contato, cargo
3. **Conexão estratégica** — 1-3 frases sobre por que o destinatário se conecta a esta edição (setor, papel na economia, histórico, relevância)
4. **Aproveitamento publicitário** — formatos da proposta (página simples, página dupla, banners com volume de impressões, publieditorial, etc.)
5. **Proposta comercial** — investimento (R$), condições de pagamento, data de fechamento, data de envio de material, número da edição, mês/ano de veiculação
6. **Data da carta** — se não informada, use a data corrente

## Anatomia da carta — 12 blocos fixos

Toda carta segue rigorosamente esta sequência. Não invente blocos novos, não suprima blocos existentes.

### 1. Cabeçalho visual
Logo da marca da publicação (ES Brasil, Comunhão, Destinos ES ou Prócidade) à esquerda + logotipo Next Editorial à direita. No template HTML, isso é resolvido pelo cabeçalho com a classe `brand-header`.

### 2. Local e data
Formato: `Vitória, ES, DD de [mês por extenso] de AAAA`
Exemplo: `Vitória, ES, 27 de março de 2026`

### 3. Bloco do destinatário
Três linhas, sem espaçamento extra entre elas:
- Linha 1: Nome da instituição (em negrito)
- Linha 2: Nome do contato (em negrito)
- Linha 3: Cargo

### 4. Linha de assunto
Destaque visual em vermelho institucional (#B11A27 para ES Brasil, ou cor proprietária da marca). Formato fixo:
`Assunto: [Instituição] na [Produto editorial específico]`

Exemplos reais:
- `Assunto: Prefeitura Municipal de Viana na ES Brasil Especial Aniversário e ES em Números 26`
- `Assunto: Cesan - Companhia Espirito Santense de Saneamento na Comunhão Especial Jesus Vida Verão 2026`
- `Assunto: Banco do Nordeste na Edição ES Brasil Retrospectiva 2026`

### 5. Saudação
Sempre curta: `Olá [Primeiro nome],`. Nunca "Prezado", "Estimado", "Caro" — fora do padrão.

### 6. Parágrafo 1 — Espelho de valor
Estrutura: posiciona o destinatário como pilar do setor + apresenta a edição/produto editorial conectando-o ao universo do destinatário. Frases curtas, com negrito em nomes próprios e nos produtos editoriais. Tamanho: 4-6 linhas.

Padrão do raciocínio: "A [Instituição] é [papel relevante no setor]. [Frase de impacto sobre a contribuição]. A [Edição] é [descrição da edição como produto de inteligência], [enumera o que entrega]."

### 7. Parágrafo 2 — Prova e convite
Estrutura: dados de alcance da plataforma (anos de mercado, impactos mensais, segmentação) + benefícios institucionais que o destinatário ganha + chamada para garantir presença antes do prazo. Tamanho: 4-6 linhas.

Padrões de prova por marca:
- **ES Brasil:** "mais de 20 anos", "quase 3 milhões de impactos mensais", "classes A e B", "impresso, portal, PDFs e streams"
- **Comunhão:** "quase 30 anos", "maior revista cristã em circulação", "mais de 6 milhões de impactos mensais", "15 mil exemplares impressos e 200 mil leitores digitais"

### 8. Linha de transição
Frase fixa de ligação para a tabela:
`A seguir, apresentamos proposta de veiculação na plataforma [Marca] em condições comerciais e técnicas diferenciadas e com excelente relação custo/benefício para [Destinatário]:`

### 9. Tabela APROVEITAMENTO
Cabeçalho colorido com o título `APROVEITAMENTO – PLATAFORMA [MARCA]` ou `APROVEITAMENTO PUBLICITÁRIO - REVISTA [MARCA]`. Lista os formatos contratados:
- ANÚNCIO PUBLICITÁRIO (página simples ou dupla, impresso ou digital, colocação indeterminada)
- BANNER (volume de impressões + formatos: 300x100, 300x250, 728x90, 970x250)
- PUBLIEDITORIAL (quando aplicável)
- Outros conforme aproveitamento contratado

Cada formato em uma linha, com o nome do formato em **negrito maiúsculo** seguido de hífen e descrição técnica.

### 10. Tabela PROPOSTA COMERCIAL
Cabeçalho colorido com `PROPOSTA COMERCIAL – REVISTA [MARCA] [edição específica]`. Cinco linhas:
- Edição/Período de veiculação
- Investimento (com `R$` antes do valor — se for valor líquido, indicar entre parênteses)
- Condições de pagamento
- Fechamento comercial
- Envio de Material

### 11. Bloco institucional da plataforma
Texto fixo descrevendo a plataforma. Use o texto padrão (em `references/voz-por-marca.md`) com substituições mínimas de edição/período.

### 12. Bloco de emissão + assinatura
- Cabeçalho: `Informações para emissão de autorização e pagamento`
- Razão social + CNPJ (ver regra de CNPJ por edição abaixo)
- Fechamento: `Sem mais, atenciosamente.`
- Assinatura: `Mário Fernando Souza` / `Diretor Executivo` / `(27) 98121-4222` / `(27) 2123-6506` / `mariof@nxte.com.br`

### 13. Rodapé
Endereço e canais: `Av. Paulino Muller, 795 • Vitória • ES • 29040-715` + Instagram `nexteditorial` + site `nexteditorial.com.br` + WhatsApp `27 98121-4442`.

## Regra de CNPJ por edição

A razão social emissora varia por produto:
- **ES Brasil Retrospectiva** (edição anual de dezembro, geralmente ed. 238): **Linea Editorial Ltda** — CNPJ **39.416.443/0001-01**
- **Todas as demais edições** (ES Brasil regulares, Comunhão, Destinos ES, Prócidade): **Next Editorial Ltda** — CNPJ **47.940.902/0001-71**

Se houver dúvida sobre o emissor, pergunte ao usuário antes de gerar a carta.

## Voz e tom por marca

Esta skill carrega instruções específicas de voz para cada marca em `references/voz-por-marca.md`. Antes de redigir o parágrafo 1 e o parágrafo 2, leia o arquivo para incorporar o léxico correto. Síntese rápida:

- **ES Brasil** — factual, contextualizado, analítico. Léxico: economia, decisão, inteligência, gestão estratégica, infraestrutura, indicadores, lideranças. Tom executivo, sem floreios.
- **Comunhão** — bíblico, pastoral, equilibrado. Léxico: fé, família, comunidade, impacto missionário, valores cristãos, juventude, igreja. Acolhedor sem ser pietista.
- **Destinos ES** — experiencial, útil, descritivo. Léxico: experiência, descoberta, território, lifestyle, percurso. Inspira antes de informar.
- **Prócidade** — técnico-urbanístico. Léxico: cidade, mobilidade, infraestrutura, desenvolvimento urbano, gestão pública.

## Regras absolutas (não negociáveis)

Estas regras vêm da memória global do usuário e nunca podem ser violadas em nenhuma carta:

1. **Nunca escrever "S Brasil"** — o nome correto é sempre **ES Brasil**.
2. **Nunca usar emojis** em nenhum bloco da carta.
3. **Nunca usar linguagem infantilizada.**
4. **Nunca usar bordões:** "indo direto ao ponto", "vamos mergulhar", "super incrível", "honestamente", "pra ser sincero".
5. **Nunca explicar que está sendo direto ou objetivo** — apenas seja.
6. **Comunicação institucional, estratégica, analítica e editorial.**
7. **Linguagem humana, premium e profissional** — sem exageros emocionais, sem genericidades.

## Identidade visual aplicada

O template HTML (em `assets/template-carta.html`) já tem as paletas oficiais aplicadas por marca. Síntese:

| Marca | Cor de cabeçalho | Cor de assunto | Cor de cabeçalho de tabela |
|---|---|---|---|
| ES Brasil | `#001C43` | `#B11A27` | `#B11A27` |
| Comunhão | `#001C43` | `#FFC220` (sobre `#001C43`) | `#FFC220` |
| Destinos ES | `#0D2B45` | `#E91E8C` | `#E91E8C` |
| Prócidade | `#1A1A1A` | `#F26522` | `#F26522` |

Tipografia: **Heebo 700–900** para títulos/cabeçalhos/labels; **Lato 300, 400, 700** para corpo. Fallback: Roboto, sans-serif.

## Como gerar a carta

Fluxo de execução:

1. **Confira o input** contra os 6 campos do "Input mínimo". Se faltar algo essencial, pergunte uma vez de forma agrupada.
2. **Identifique a marca** e leia `references/voz-por-marca.md` para incorporar o léxico correto.
3. **Resolva o CNPJ emissor** conforme a regra de CNPJ por edição.
4. **Escreva os parágrafos 1 e 2** seguindo a anatomia. Use negrito estratégico em: nome do destinatário, nome da edição, dados de alcance da plataforma, frases-âncora.
5. **Monte as duas tabelas** (Aproveitamento e Proposta Comercial) com os dados fornecidos.
6. **Gere o HTML final** a partir do template em `assets/template-carta.html`, substituindo os placeholders. Salve em `/mnt/user-data/outputs/carta-[destinatario]-[marca]-[data].html`.
7. **Apresente o arquivo** ao usuário com `present_files`.

## Antes de finalizar — checklist

Antes de entregar a carta, valide internamente:

- [ ] Local e data corretos
- [ ] Nome do destinatário em negrito no bloco de destinatário e nos parágrafos 1 e 2
- [ ] Linha de assunto no padrão "X na Y"
- [ ] Saudação como "Olá [primeiro nome]"
- [ ] Parágrafo 1 com espelho de valor (posiciona o destinatário + conecta à edição)
- [ ] Parágrafo 2 com prova de alcance + convite + senso de prazo
- [ ] Linha de transição literal antes da tabela
- [ ] Tabela APROVEITAMENTO com formato técnico correto (volume de impressões + dimensões dos banners)
- [ ] Tabela PROPOSTA COMERCIAL com R$ e datas
- [ ] Bloco institucional da plataforma
- [ ] CNPJ correto conforme regra
- [ ] Assinatura padrão do Mário Fernando Souza
- [ ] Nenhuma regra absoluta violada
- [ ] Nenhum emoji em lugar nenhum

## Referências da skill

- `references/voz-por-marca.md` — léxico, tom, blocos institucionais por marca
- `assets/template-carta.html` — template visual parametrizável por marca
- `examples/exemplos-comentados.md` — extratos dos modelos reais (Viana, CESAN, BNB) com análise dos padrões
