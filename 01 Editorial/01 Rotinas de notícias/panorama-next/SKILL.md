---
name: "panorama-next"
description: "Panorama (noticiário geral: Brasil, Mundo, clima e ciência, gente) da ES Brasil e da Comunhão em 5 rodadas por dia, a partir das agências do NX Feed, publicado direto. Roda junto com o esporte."
---

# Panorama — ES Brasil e Comunhão (5 rodadas por dia)

Rotina que mantém vivo o bloco **Panorama** das homes da **ES Brasil** e da **Comunhão** com o noticiário geral nacional e internacional. Roda nos mesmos horários da rotina de esporte (7h, 12h, 16h, 21h50 e 23h50), na mesma execução, logo depois dela. O esporte não entra aqui: é da **esporte-noturno-next**. Notícia capixaba também não: é do turno noturno e da redação.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, cuidados do NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem, avisos e economia do plano (seção 11) estão lá. Se a skill-base não estiver disponível, não publique nada: deixe as matérias em rascunho e avise que a skill-base faltou.

**Junto com o esporte (mesma execução):** use as listagens que a esporte-noturno-next já fez nesta execução (pendências, feed nacional e a categoria 1 da Comunhão) e não as repita (skill-base, seção 11). Só quando o Panorama rodar sozinho faça as listagens dos passos 1 e 2.

**Princípio:** o Panorama é a vitrine do noticiário geral. Nunca deixar de falar do que é importante no país e no mundo para o público dos dois portais, com equilíbrio. Esta rotina tem seu próprio teto, separado do esporte, justamente para o Panorama não ficar parado nem ser tomado por esporte (problema de 25/10/2026).

## Rodadas (Brasília)

Descubra a rodada pela hora atual. Cada rodada cobre o que aconteceu desde a rodada anterior e ainda não tem matéria da casa. **Teto: 3 matérias por rodada** (até 15 por dia). Fora desses horários, use a janela "desde a última matéria de Panorama da casa".

| Rodada | Janela | Foco |
|---|---|---|
| **7h** | desde a das 23h50 | Madrugada no Brasil e no mundo e a agenda do dia (Congresso, STF, indicadores, alertas do Inmet). |
| **12h** | desde a das 7h | Noticiário da manhã. |
| **16h** | desde a das 12h | Noticiário da tarde. |
| **21h50** | desde a das 16h | Noticiário da noite. |
| **23h50** | desde a das 21h50 | O mais importante da noite. |

**Teto diário da Comunhão:** 5 matérias de Panorama por dia, somando todas as rodadas. Antes de pôr uma matéria na Comunhão, conte o que esta rotina já pôs hoje lá: com o esporte na mesma execução, conte na listagem da categoria 1 que ele fez no passo 0 (só as de hoje e que não são esporte); sozinha, `listar_materias` portal=4, estado publicado, data_de = hoje, categoria 1. Atingido o teto, a matéria sai só na ES Brasil.

## 1. Pendências das rodadas anteriores

Com o esporte na mesma execução, use as pendências de Panorama que ele separou no passo 0b. Sozinha: `listar_materias` com estado=rascunho (sem filtro de portal) e depois estado=rascunho_no_wp, data_de = ontem, formato compacto. Mexa só nas matérias de Panorama desta rotina (via Claude). Rascunho sobre fato das últimas 24 horas, ainda não superado e sem duplicata na casa → resolva foto e SEO e publique; superado ou duplicado → deixe quieto e cite no resumo. Conta no teto da rodada.

## 2. Varredura

1. **NX Feed primeiro (fonte principal e obrigatória):** com o esporte na mesma execução, use a listagem do feed nacional que ele já fez. Sozinha: `listar_materias` com `lista` = feed_nacional, `data_de` = início da janela, formato compacto, `por_pagina` = 100; pagine enquanto `tem_mais` = true e os itens estiverem dentro da janela. Fique com os itens gerais: todas as fontes gerais que aparecerem, inclusive fontes novas (em 21/10/2026: Agência Brasil – Últimas Notícias / Geral / Política / Economia / Justiça / Saúde / Internacional / Direitos Humanos / Meio Ambiente e Estadão Conteúdo – Geral / Política / Economia / Internacional / Variedades). Os de esporte são da outra rotina. O `feed_internacional` só traz veículos cristãos: pule-o.
2. Veja também o que a redação já publicou (`estado` = publicado, `campo_data` = publicada, data_de = início da janela, formato compacto) para não repetir e para o passo 6. Uma listagem serve para toda a rodada.
3. **Web só depois**, para ver se falta no feed algum fato grande do dia: abra no máximo duas páginas, a Agência Brasil (agenciabrasil.ebc.com.br/ultimas) e uma de Mundo (Euronews em português, Lusa, DW Brasil, ONU News em português ou CNN Brasil Internacional). g1, CNN Brasil, Folha e Estadão só quando um fato grande do dia não estiver no feed e precisar de conferência. A BBC News Brasil não abre por WebFetch.
4. Anote quantos itens gerais havia no NX Feed.

## 3. O que entra (por prioridade)

1. **Brasil:** fato nacional de grande impacto — decisões do governo, do Congresso e do STF que mexem no dia a dia (salário mínimo, impostos, MEI, previdência, escala de trabalho), tragédias, eleição (resultado, regras, prazos do TSE).
2. **Mundo:** guerras e acordos de paz, eleições e crises em países relevantes, decisões dos EUA, da China e da UE com efeito no Brasil, papa e Vaticano (só na ES Brasil, salvo doença ou morte; ver seção 4), catástrofes naturais.
3. **Clima e ciência:** alertas do Inmet, El Niño/La Niña, ondas de calor e chuvas fortes no país, meio ambiente nacional, saúde pública nacional (vacinas, novos tratamentos no SUS, surtos).
4. **Gente:** morte de personalidade conhecida do grande público, notícia grande de celebridade brasileira (sem fofoca).

**Não entra:** as pautas proibidas da seção 2.1 da skill-base (denúncia, inclusive operação policial contra alvo determinado; aumento ou reajuste de tarifa; o que nasce de Ministério Público, Tribunal de Contas ou controladoria), notícia capixaba, esporte, cotação do dia, balanço de empresa, declaração de político sem fato novo, crime sem repercussão nacional, pesquisa eleitoral avulsa (no máximo a pesquisa de referência do dia, com instituto, contratante, margem de erro e registro no TSE).

## 4. Texto

- Uma matéria por fato: se duas agências trazem o mesmo fato, aproveite a mais completa e use a outra como apuração.
- **Prefira aproveitar o item da agência** (é o que a casa contrata): revise título (≤ 60), linha fina, chapéu, SEO, tags, categorias e imagem, e mantenha o crédito no rodapé ("Com informações da Agência Brasil" / "do Estadão Conteúdo"). Só escreva matéria nova, "Redação", quando juntar fontes ou acrescentar apuração.
- Intertítulos `<h3>`.
- **Comunhão** (público cristão): leve todo fato de interesse geral, mas sem sensacionalismo de violência, sem conteúdo sexual e sem fofoca; o que não servir vai só para a ES Brasil. Fé e liberdade religiosa no mundo são bem-vindas, menos o que envolve a Igreja Católica (regra abaixo).
- **Igreja Católica, papa e Vaticano não vão para a Comunhão, salvo doença ou morte** (decisão de Mário Fernando, 10/11/2026; exceção incluída em 17/11/2026). Fora a exceção abaixo, na Comunhão não entra nada sobre a Igreja Católica, o papa, o Vaticano ou a Santa Sé, a CNBB, dioceses, paróquias, padres, bispos, freiras ou organizações católicas, nem mesmo como personagem secundário, fonte, aspas, link ou imagem. Ataque ou perseguição cujas vítimas são identificadas como católicas também fica fora da Comunhão. Esses fatos saem só na **ES Brasil**, pelas regras normais.
  - **Única exceção: doença ou morte.** Internação, doença grave ou morte do papa ou de uma liderança católica de grande relevância vai também para a Comunhão, em texto curto, factual e respeitoso: o fato, o estado de saúde ou a morte e, se houver, a repercussão entre líderes evangélicos. Sem doutrina católica, sem cobertura de rito, conclave ou sucessão e sem juízo sobre a fé católica. Nessa matéria, o boletim oficial (Vaticano, Santa Sé ou a instituição da pessoa) pode ser citado como fonte do fato, e uma foto da pessoa pode ilustrar; templo, símbolo ou celebração católica, não. Na ES Brasil, a cobertura segue as regras normais.

## 5. Categorias

**ES Brasil:**

| Tema | Categorias |
|---|---|
| Mundo; papa e Vaticano | 83982 (Panorama › Mundo) |
| Clima, tempo, meio ambiente e ciência | 83983 (Panorama › Clima e ciência) |
| Gente (morte de personalidade, celebridade) | 83984 (Panorama › Gente) |
| Governo, Congresso, eleição | 63 + 1740 (Política › Nacional) |
| Justiça, STF, TSE | 63 + 1744 (Política › Judiciário) |
| Economia que mexe no bolso | 63 + 83880 (Economia e Negócios) |
| Tecnologia | 63 + 109 (Tecnologia e inovação) |
| Fatos gerais, tragédias, polícia; saúde pública nacional | só 63 |

Com 83982, 83983 ou 83984, não marque a 63. **Nunca** coloque notícia nacional em Vida Capixaba › Cotidiano (Saúde 119, Meio Ambiente 2784 etc.): é a editoria local.

**Comunhão** — sempre **Cotidiano › Panorama (1)** + uma do tema:

| Tema | Categoria |
|---|---|
| Governo, Congresso, Justiça, eleição | 116630 (Política & Cidadania) |
| Fatos gerais, clima, ciência, tecnologia, gente sem ligação com o meio cristão | 116635 (Brasil & Mundo) |
| Mundo | 26 (Internacional) |
| Economia | 16422 |
| Saúde pública | 16423 |
| Educação nacional | 116632 |
| Comportamento | 116633 |
| Personalidades do meio cristão | 27 (Gente) |
| Posicionamento de igrejas e entidades evangélicas | 116629 (Fé & Sociedade) |
| Perseguição e liberdade religiosa | 116628 (Igreja Perseguida) |

Tecnologia 16427 não entra no Panorama da Comunhão. Notícia geral nunca vai para Destaques (11966 / 44517).

## 6. Gerais já publicadas pela redação

Matérias de agência de fontes gerais que a equipe publicou sem Panorama, que se encaixam no passo 3 e não são pauta proibida (2.1 da skill-base) ganham as categorias do passo 5, **somadas** às que já têm (`ver_materia` → `editar_materia` → `enviar_rascunho_ao_wordpress`, que atualiza o post no ar sem mudar o status). No máximo 3 por rodada, as mais importantes; não contam no teto. Nunca tire uma categoria que a redação marcou.

## 7. Imagem

Regra da skill-base. Ordem de busca do Panorama: imagem da própria agência → `buscar_imagens` recomendadas → editoriais → NX Fotos. Itens do Estadão Conteúdo costumam chegar sem imagem. Pessoa citada no título: foto dela. Tema de serviço ou clima: ilustrativa real com crédito.

## 8. Publicação

Tudo vai ao ar direto, pela regra da skill-base, nos portais definidos no passo 5, uma por vez. Quando o esporte rodar na mesma execução, intercale as publicações das duas rotinas, começando pela notícia mais importante.

## 9. Resumo

Avisos da skill-base. Título do resumo: **"Panorama – rodada das <hora>"**; quando rodar na mesma execução que o esporte, um resumo só: **"Esporte e Panorama – rodada das <hora>"**.

Parte do Panorama no resumo: publicadas (título, portal e categorias, link no ar, imagem real ou IA), não publicadas com o motivo, gerais da redação que ganharam Panorama, quantos itens gerais havia no NX Feed e quantas matérias de Panorama a Comunhão já recebeu hoje.