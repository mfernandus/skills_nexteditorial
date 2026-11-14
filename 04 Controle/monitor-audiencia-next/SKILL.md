---
name: monitor-audiencia-next
description: "Gera a análise de audiência dos sites da Next — ES Brasil e Comunhão — lendo o audiencia-latest.json do coletor. Entrega painel HTML no padrão Next e resumo curto de WhatsApp, sempre lendo o dia contra a base de sete dias e com selos REAL/REFERENCIA/SIMULADO/PENDENTE."
---

# Monitor de Audiência Next

Skill canônica da análise de audiência de **ES Brasil** e Comunhão.

Acione quando o usuário pedir "análise de audiência", "como foi a audiência", "o que bombou hoje", "monitor de audiência", "resumo de tráfego", "painel de audiência", ou quando a tarefa agendada disparar.

---

## 1. Entrada

O dado vem pronto. Esta skill **não autentica em nada** e não chama API alguma.

- Arquivo: `audiencia-latest.json`
- Pasta do Drive: **Monitor Audiencia Next** (id `1jPQ94DLrl80RQ3RUB7od_wILsJ9xixjm`), na conta `mariof@nxte.com.br`
- Id do arquivo estável: `1hzAqqOA88oXpH4Lj7io4LIVDJMIVNcNG`
- Produzido pelo Apps Script "Monitor de Audiencia Next - Coletor", de hora em hora, e consolidado às 6h

Procure o arquivo pelo conector do Google Drive. O conector costuma estar ligado em outra conta do usuário — se der "não encontrado", tente abrir o arquivo pelo id acima no navegador com `authuser=2`. Se ainda assim não abrir, **peça o arquivo ao usuário e pare**. Nunca invente números para preencher.

A mesma pasta guarda o histórico horário (`audiencia-AAAA-MM-DD_HH.json`). Leia dois ou três arquivos anteriores quando quiser comparar; sem eles, não afirme tendência.

### Validação obrigatória, antes de qualquer análise

1. `schema_version` precisa ser da família **1.x** (`1.0`, `1.1`, …). Campos novos dentro da família 1 são aditivos e opcionais — aceite. Uma versão **2.x** quebra o contrato: **recuse** e diga que o contrato mudou, não tente adivinhar campos.
2. Leia o array `erros`. Se houver entradas, elas entram no relatório como fonte que falhou, com o código (`PERMISSION_DENIED`, `AUTENTICACAO`, `COTA_EXCEDIDA`…).
3. Confira `janela`. O Search Console vem de D-4 a D-2 por causa da defasagem de publicação; GA4 vem de hoje ou de ontem conforme `granularidade`. **Nunca compare os dois como se fossem o mesmo período.**

---

## 2. A regra da amostra — leia antes de escrever qualquer número

Esta seção existe porque a análise já errou duas vezes pelo mesmo motivo, nas duas direções.

Quando `janela.granularidade` for `"hora"`, o bloco `resumo`, `canais`, `dispositivos` e `top_materias` descrevem **um dia ainda em curso**, muitas vezes com poucas centenas de sessões. Nessa amostra, qualquer anomalia — um robô, um pré-carregamento, um pico de crawler — domina o percentual.

**Nenhuma afirmação sobre o site pode sair do dia parcial.** Isso inclui:

- participação de canal ("metade do tráfego é Unassigned")
- páginas por sessão e encadeamento interno
- tempo médio e taxa de engajamento
- comparação entre as duas marcas

Para tudo isso use o bloco `semana` (schema 1.1 em diante): sete dias fechados, com `resumo` (incluindo `paginas_por_sessao`), `canais` e `busca`. É o denominador.

O bloco `comparacao_semana` já traz o dia contra a média diária da semana. Em coleta horária a `variacao_sessoes` é **sempre** negativa porque o dia não terminou — não chame isso de queda.

Se `semana` vier com selo `PENDENTE`, diga que a base de comparação faltou e **limite a análise a descrever o dia**, sem concluir nada sobre o site.

O dia parcial serve para uma coisa só: **detectar anomalia**. Pico de visualizações com um único usuário e zero segundos, matéria que aparece do nada, canal que some. Isso sim é leitura de dia.

---

## 3. Selos — a regra que não se negocia

Todo bloco do JSON traz um `selo`. A distinção é o motivo de o sistema existir.

| Selo | Significado | Como apresentar |
|---|---|---|
| `REAL` | Medido na fonte | Número puro, sem ressalva |
| `REFERENCIA` | Benchmark externo ou estimativa | Sempre etiquetado, com fonte e data |
| `SIMULADO` | Gerado por regra de negócio da casa | Sempre etiquetado |
| `PENDENTE` | Fonte não respondeu, ou módulo desligado | **Declare como ausência de dado. Nunca como zero, nunca como queda.** |

Nunca coloque dois selos diferentes na mesma frase sem etiquetar cada um. Um `PENDENTE` lido como queda de audiência é o pior erro possível aqui.

---

## 4. Como analisar

Número sem leitura não serve. O painel existe para responder o que fazer amanhã.

**Separe alcance de conversão.** Impressões no Search Console medem quanto o site aparece; CTR mede quanto ele convence. Antes de atribuir CTR baixo a título e snippet, **confira a posição média das duas marcas na mesma janela de sete dias**. Se a posição não for equivalente, parte do gap é distância no ranking, e a recomendação editorial vale menos do que parece. Diga qual parte é qual.

**Leia a cauda longa.** As posições 11–20 do ranking são o material que já tem tração e não recebeu esforço. Aponte de uma a três matérias dessa faixa que merecem republicação, atualização ou reforço em social.

**Cruze tempo médio com visualizações.** Matéria que atrai não é a mesma que prende. Uma com muitas visualizações e tempo baixo entregou menos do que parece; uma com poucas visualizações e tempo alto encontrou o leitor certo — e provavelmente não foi distribuída direito.

**Olhe a concentração de canais, sempre na base de sete dias.** Um canal acima de ~50% das sessões é dependência, não força. Registre quando acontecer.

**Compare as duas marcas com cuidado.** Elas têm tamanho e público diferentes. O que interessa é a taxa, não o volume: CTR de busca, taxa de engajamento, tempo médio, páginas por sessão — e todas na janela semanal.

**Quando houver GAM**, confronte entrega publicitária com audiência editorial. Viewability baixa com impressão alta significa anúncio servido e não visto — informação comercial, não editorial, mas que o time comercial precisa.

Seja direto sobre incerteza. Uma leitura de um dia não é tendência; diga isso quando for o caso.

**Se uma leitura anterior for contrariada pelo dado novo, corrija de forma explícita.** Não edite em silêncio: diga o que foi afirmado, o que o dado mostra e o que cai da recomendação. Uma correção declarada vale mais que um painel limpo.

---

## 5. Saída 1 — Painel HTML

Documento HTML autocontido, no **padrão Next Editorial** (assunto institucional, consolidando as duas marcas — nunca a paleta de uma marca só).

- Fonte **Inter** exclusivamente; títulos 800, corpo 400/500; tracking negativo
- Vermelho `#B20B27` predominante: fundos escuros e headers de tabela
- Secundárias `#00427B` e `#FFC220`; tinta `#1B2430`; linhas `#E6EAF0`
- Ícones Lucide outline, stroke 2px — nunca filled, nunca emoji
- `border-radius` de tabela: `0.5rem`
- Tabelas largas em contêiner com `overflow-x: auto`
- Tokens de cor definidos em `:root` puro e redefinidos em `@media (prefers-color-scheme: dark)` e `:root[data-theme="dark"]`; header de tabela usa um token sólido próprio, nunca `var(--red)`, que clareia no escuro

Estrutura:

1. Cabeçalho com data, janela de cada fonte e selo dominante
2. Resumo executivo — três a cinco frases, o que aconteceu e o que fazer
3. Blocos por marca: **ES Brasil** e Comunhão, com resumo, top 10 matérias, canais, dispositivos
4. **Base de sete dias** ao lado de cada leitura do dia, sempre que `semana` existir — mix de canais, páginas por sessão, CTR e posição média
5. Bloco de busca: cliques, impressões, CTR, posição média, top consultas e páginas
6. Cauda longa: posições 11–20 com a recomendação
7. Bloco GAM quando `selo` for `REAL`
8. Seção "O que este relatório não permite concluir"
9. Rodapé com origem, versão do coletor, schema e horário da coleta

Se o array `erros` não estiver vazio, abra uma seção "O que faltou" listando fonte, código e o que isso impede de concluir.

---

## 6. Saída 2 — Resumo de WhatsApp

Texto curto, para colar direto. Sem emojis, sem markdown pesado, sem link encurtado.

```
Audiência Next — [data]

ES Brasil: [sessões] sessões, [visualizações] visualizações
Destaque: [título da 1ª matéria humana] — [visualizações] views

Comunhão: [sessões] sessões, [visualizações] visualizações
Destaque: [título da 1ª matéria humana] — [visualizações] views

Base 7 dias: ES Brasil [sessões/dia] sessões por dia; Comunhão [sessões/dia]
Busca ([janela]): ES Brasil [cliques] cliques / CTR [x]%; Comunhão [cliques] cliques / CTR [x]%

Leitura: [uma a duas frases — o que explica o dia e o que fazer]
```

Adapte quando houver `PENDENTE`: diga que a fonte não respondeu, não omita a linha.

---

## 7. Convenções

- Sempre **ES Brasil** em negrito, nunca "S Brasil"
- Números em português: milhar com ponto, decimal com vírgula
- Percentuais com uma casa decimal
- Tom estratégico e direto; clareza acima de ornamento
- Sem emojis em material institucional

## 8. O que nunca fazer

- Tirar conclusão sobre o site a partir da coleta parcial do dia
- Chamar de queda a `variacao_sessoes` negativa de uma coleta horária
- Apresentar `PENDENTE` como zero ou como queda
- Misturar janela do GA4 com janela do Search Console na mesma comparação
- Afirmar tendência a partir de uma única coleta
- Atribuir diferença de CTR a título sem antes conferir a posição média
- Inventar número quando o arquivo não abrir
- Usar paleta de marca individual num painel que consolida as duas