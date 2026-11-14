---
name: "acervo-comunhao"
description: "Uma vez por dia, adapta uma matéria do acervo da Comunhão (NEIA, de 1997 até 4 meses atrás), atualiza pessoas, cargos, dados e fatos datados e agenda para as 22h, nos Destaques até as 12h."
---

# Acervo Comunhão — matérias do acervo atualizadas

Objetivo: trazer de volta ao portal Comunhão o melhor do acervo da revista e do site, **uma matéria por dia, no ar às 22h**, atualizada para o leitor de hoje. A skill busca na NEIA (a IA da casa, via MCP), escolhe a matéria, confere quem está vivo e em que cargo, refaz os dados que sustentam a conclusão, marca o que é datado e agenda a publicação para as 22h, nos Destaques da Comunhão até o meio-dia seguinte.

Responda sempre em português do Brasil. Execução automática: não faça perguntas. Na dúvida, tome a decisão mais conservadora e registre no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns da casa: pautas proibidas (2.1, vale acima de tudo), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), SEO (8), imagem destacada (9) e avisos (10). Onde as duas divergirem, vale esta skill nestes pontos, decididos pelo Mário Fernando em 28/10/2026 e confirmados nos testes de 02/11/2026:

- **Agendada para as 22h, com Destaques até as 12h** do dia seguinte, e depois só na categoria da editoria (seção 9; decisão de 02/11/2026, que substitui a de 28/10 de deixar só em rascunho).
- **Título original mantido** (seção 6).
- **Crédito ao jornalista original, aviso de republicação e rodapé de origem** no lugar do "Com informações de" (seção 6).
- **Até três links externos**, todos na Nota da Redação, para as fontes dos dados atualizados.
- **Despublicação das versões antigas duplicadas** (seção 9).
- **Matéria inteira, nunca dividida em partes** (seção 6; decisão de 02/11/2026).

## 1. Fontes no NEIA

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch.

| Fonte | Id | O que tem |
|---|---|---|
| Revista Comunhão (magazine) | 019ca1b0-1295-72f0-baaf-31867a70431e | Edições desde 1997; a base vai até a Edição 324 (set/2024) em out/2026 |
| comunhao.com.br (wordpress_portal) | 019ca1ae-c3a6-718c-b1f2-e577c04f3ed8 | Posts do site, com data exata, id do post e link |

- `search-content` com `source` (nunca sem escopo), `page_size` até 50, e `next_cursor` para paginar. Filtrar `content_type` "article" ou "interview" ajuda a fugir de colunas e notas.
- `get-article-content` traz o texto completo, a edição e, no site, `wp_post_id`, `wp_url` e `published_at`.
- `list-editions` (project_id = id da revista) traz a data de cada edição. A resposta é grande e vem salva em arquivo: leia só as edições que interessam (por exemplo, com um script que filtra pelo `edition_number`).
- **Corte de tempo:** de 1997 até 4 meses antes do dia da execução. Post do site mais novo que isso não entra.
- **Prefira a revista.** O post do site entra quando é melhor que o equivalente da revista ou quando o tema só existe lá.
- O título que a NEIA dá à matéria às vezes foi gerado na ingestão ("Entrevista com Fulano: O Chamado..."). O título que vale é o impresso, que aparece no começo do `full_content`.

### Datas: conferir antes de usar

- Na revista, a data vem sempre no dia 1º do mês: use **só mês e ano**.
- Algumas edições (17 a 32, por exemplo) vêm com 02/03/2026, que é a data de ingestão, não a de publicação. Deduza a data mais coerente pela sequência mensal das edições vizinhas e por marcas do próprio texto ("Campanha 2012", "o Censo de 2000", Copa, eleição). Registre no resumo "data deduzida" e como chegou nela.
- A mesma matéria pode aparecer em mais de uma edição (ex.: "Criança: um investimento para a vida", nas edições 73 e 298; "Luto: tempo de dor e de esperança", nas edições 230 e 273). O original é a **edição mais antiga**; a mais nova pode ser citada no rodapé ("republicada na edição nº 298").
- No site, use a data exata do post. Se o post for republicação da revista (o texto avisa "republicação da Revista Comunhão"), busque a edição original e use a data dela. A data do post no WordPress de republicações antigas pode ter sido trocada depois; desconfie quando ela não bater com a pasta da imagem (`/uploads/AAAA/MM/`).

## 2. Escolha da matéria do dia

### Editoria do dia

| Dia | Editoria |
|---|---|
| Segunda | Vida cristã |
| Terça | Família |
| Quarta | Missões |
| Quinta | Igreja |
| Sexta | Especiais (entrevistas, reportagens de capa, dossiês) |
| Sábado | Atuais (comportamento, sociedade, educação, saúde, tecnologia, ética) |
| Domingo | Livre: a maior nota entre todas as editorias |

O dia vale pela data de Brasília da execução (`TZ=America/Sao_Paulo date`). O campo "seção" da NEIA não serve: quase tudo vem como "Cultura". A editoria se define pela leitura do texto.

### Busca

Faça de 4 a 8 buscas na revista com temas da editoria e varie as décadas (1997–2005, 2006–2015, 2016 em diante). Exemplos de busca:

- Vida cristã: oração, santidade, espiritualidade, graça, fé no cotidiano, Bíblia, perdão, esperança.
- Família: casamento, filhos, adolescentes, finanças da família, idosos, refeições em família, novo casamento.
- Missões: missionários, povos não alcançados, povos indígenas, igreja perseguida, evangelização, agências missionárias.
- Igreja: liderança, pastores, gestão da igreja, ministério, teologia, crescimento da igreja.
- Especiais: entrevistas com líderes, reportagens de capa, séries.
- Atuais: comportamento, tecnologia, educação, saúde emocional, ética, sociedade.

Separe de 3 a 5 candidatas antes de ler a fundo: a regra dos 4 meses (seção 3) costuma derrubar uma ou duas.

### Nota de escolha (0 a 5 cada, mínimo 13 de 20)

- **Atemporalidade:** o tema vale hoje para o leitor cristão (5) ou é preso ao fato da época (0).
- **Atualização viável:** pessoas públicas e dados que dá para conferir (5); depende de fato que não se confere mais (1).
- **Qualidade do original:** texto completo, bem apurado, sem trechos quebrados pela digitalização (5).
- **Interesse e busca:** tema procurado na internet, com gancho de calendário próximo (Reforma Protestante, Finados, Dia de Ação de Graças, Dia da Bíblia, Natal, Páscoa, Dia das Mães e dos Pais, Dia do Pastor, volta às aulas) ou com pessoa conhecida do leitor (5).

Empate: o gancho de calendário, depois a década menos usada pelas matérias recentes da rotina (seção 3, busca 1), depois a maior presença de dados que mudaram.

### Fora da escolha

- Pautas proibidas do padrão (2.1): denúncia, aumento de tarifa, origem em órgão de controle.
- Política partidária e eleitoral.
- Editorial, carta de leitor, agenda, nota curta (menos de 400 palavras), coluna de serviço, resenha de livros, devocional, publicidade e conteúdo de marca.
- Matéria cujo fato principal foi superado (campanha de um ano, evento com data, inauguração, resultado de concurso, lista anual já substituída).
- Matéria presa a um contexto que passou (pandemia, eleição, Copa) sem argumento que se sustente fora dele.
- Original com mais de 3.000 palavras que não dá para condensar sem perder argumento: escolha outra (a matéria nunca é dividida em partes).
- Obituário e cobertura de enterro.
- Matéria já adaptada por esta rotina (seção 3).

## 3. Duplicidade

As matérias da rotina se reconhecem por três marcas: o título original mantido, a tag "Acervo Comunhão" e a frase "É uma republicação do acervo Comunhão." no pé do texto.

Antes de escrever e de novo antes de agendar:

1. **Rotina e NX Feed:** `listar_materias` com `busca` pelo título original (e por uma palavra forte dele), todos os estados, últimos 365 dias, formato compacto; rascunhos sem filtro de portal. Para ver as matérias recentes da rotina: `listar_materias` com `portal` 4, `estado` rascunho_no_wp, agendado e publicado, últimos 30 dias, formato compacto, e confira com `ver_materia` as que têm a tag e a frase de republicação (rascunhos e agendadas da rotina também contam). A mesma matéria original nunca é adaptada duas vezes.
2. **Site, na NEIA:** `search-content` na fonte do portal pelo título original e pelo tema central, com a pessoa principal quando houver.
3. **Site, na web:** WebSearch `site:comunhao.com.br "<título original>"` e `site:comunhao.com.br <tema> <pessoa>`.

Como decidir:

- **A mesma matéria original já está no site** (republicação antiga, como "Finanças: na medida certa para a saúde do lar", post 29732, de 2017, ou "Graça: que diferença faz para sua vida?", post 979): siga com a adaptação atualizada e guarde a lista dos posts antigos (link, id do post e se existe no NX Feed). Eles saem do ar depois que a versão nova for ao ar (seção 9). É comum: a maior parte das republicações antigas foi feita direto no WordPress, fora do NX Feed.
- **O site tratou o mesmo tema nos últimos 4 meses:** troque de matéria. "Mesmo tema" é o mesmo assunto com o mesmo enfoque (ex.: luto e esperança cristã), não a editoria inteira.
- **Rascunho da equipe sobre o tema:** troque de matéria.

## 4. Leitura e limpeza do texto

- Leia o texto inteiro com `get-article-content`. Texto incompleto ou com trecho ilegível que muda o sentido: troque de matéria.
- **Digitalização:** corrija palavras trocadas ("família toca" → "família toda"; "Prador" → "pastor"; "Horrar" → "Honrar"), hifenização quebrada e repetições. Corrigir erro evidente de transcrição numa citação é permitido; mudar o que a pessoa disse, não. Trecho que veio truncado e não dá para reconstruir (transliterações, números colados): resuma em palavras próprias ou tire, e registre no resumo.
- **Nomes:** a mesma pessoa pode aparecer com várias grafias (ex.: Syra Lippi, Syria Luppi, Seria Luppi, Syrta Lujos, Suria Luípe; "Boliomara" = Heliomara Mulullo). Use a grafia mais limpa e mais frequente nas edições recentes, confira na web quando for pessoa pública e registre no resumo quando houver dúvida.
- **Autoria:** vale o crédito impresso na revista. Se a republicação antiga do site assinar outra pessoa, mantenha o da revista e registre no resumo.
- **Olhos, boxes e legendas:** descarte o destaque que não aparece no corpo do texto e o que só repete o corpo. Box útil (dicas, serviço atemporal, enquete com depoimentos) pode ficar.
- **Grafias e métricas:** padronize unidades, moeda (R$), números (mil, milhões) e datas por extenso.

## 5. Atualização

### 5.1 Pessoas públicas (pastores, líderes, autores, autoridades, especialistas)

- **Vida:** confira se a pessoa está viva. Morte só com **duas fontes independentes** (a cobertura da própria Comunhão no site vale como uma delas; comunicado da instituição da pessoa também). Falecida: "(in memoriam)" logo depois do nome **na primeira menção**, e o mês e o ano da morte na Nota da Redação. Personagem histórico morto antes da publicação original (Lutero, Bonhoeffer) não leva marca.
- **Cargo e função:** confira o cargo atual. Mudou: o texto do repórter traz o cargo atual; o antigo só aparece ("então presidente", "na época pastor da…") quando explica a fala. Não deu para confirmar (comum com pastores locais): "então da igreja X" no texto, um item na Nota da Redação dizendo que os vínculos são os da época e registro no resumo.
- **Grafia** do nome conforme a fonte oficial da pessoa ou da instituição.

### 5.2 Pessoas privadas (testemunhos, famílias, leitores, enquetes)

- Não pesquise a vida delas.
- Marque o tempo: "na época", "então com 14 anos", "que na época esperava o primeiro filho". Em enquete, a profissão vira "na época secretária", "publicitário e, na época, seminarista".
- Quem era menor de idade na época: primeiro nome mantido, com "então com X anos".

### 5.3 Dados e números

- Todo número que **sustenta a conclusão** da matéria precisa ser atualizado com a fonte oficial mais recente (IBGE, Banco Central, Ipea, CNC, Serasa, AMTB, Sociedade Bíblica do Brasil, órgãos públicos, institutos de pesquisa), aberta com WebFetch.
- **Mesma métrica:** compare só o que mede a mesma coisa. Sem dado equivalente (vendas x distribuição, separações x conflitos), use o dado mais próximo e diga na Nota da Redação que a medida é diferente.
- **Valores em reais:** diga se a comparação é nominal (sem descontar a inflação).
- **No texto do repórter:** troque o número pelo atual, com a fonte e o ano. Mantenha o número antigo quando a comparação muda a leitura ("em 2010 eram R$ 2,2 trilhões; em 2026, R$ 8,6 trilhões").
- **Dentro de citação:** a fala fica como foi dita; o número atual vai para a Nota da Redação.
- Número sem atualização possível e sem peso na conclusão: pode sair do texto; registre no resumo. Dado lexical ou histórico (quantas vezes uma palavra aparece na Bíblia, ano de um livro) não precisa de atualização.

### 5.4 Fatos e falas datados

- Expressões de tempo no texto do repórter viram datas ("este ano" → "em 2010"; "atualmente" → "na época"; "há 74 anos" → "em 1937"). Pergunta de entrevista que diz "hoje" ou "atualmente" pode ser ajustada ("Como era a sua rotina em 2013?").
- Fato que mudou (lei aprovada, projeto encerrado, instituição extinta ou que mudou de nome, órgão que trocou de função, tecnologia superada como cheque pré-datado ou MP3): explique na Nota da Redação quando muda o sentido; detalhe de época que não muda o sentido fica sem nota.
- Lei e projeto de lei: confira a situação no site da Câmara, do Senado ou do Planalto no dia da execução.
- Nunca invente fala, número, data, nome ou cargo.

### 5.5 Bíblia

Toda citação bíblica no texto do repórter sai **sempre na NTLH** (Nova Tradução na Linguagem de Hoje; decisão de Mário Fernando, 2/11/2026), conferida palavra por palavra no NEIA com `get-bible-passage` e `bible_code` "NTLH". Nunca ACF, ARC, ARA, NVI, NVT ou outra versão no texto do repórter, mesmo que o original impresso traga: troque pelo texto da NTLH do mesmo versículo e registre no resumo. **Dentro da fala de uma pessoa** (entrevistado, personagem, autor citado), fica a versão que ela usou; corrija só a forma da referência. Confira também se a referência bate com o episódio citado (ex.: Emaús é Lucas 24, não Atos). Padrão da casa: citação curta, com a referência entre parênteses depois, ex.: "Porém a maior delas é o amor" (1 Coríntios 13.13). Referências soltas: (Provérbios 22.6), (1 Timóteo 6.8).

## 6. Formato da matéria

- **Título:** o original, mantido. Só corrija caixa alta e erro de digitação. O título SEO (até 60 caracteres) pode ser diferente. Exceção: em entrevista cujo título impresso é só o nome do entrevistado, use o nome seguido de dois-pontos e de uma frase dita por ele na própria entrevista, entre aspas (ex.: Ronaldo Lidório: "A Palavra de Deus é supracultural"); registre no resumo.
- **Linha fina:** a original (a primeira frase, se ela tiver mais de uma; a segunda pode abrir o texto); se não houver, uma frase de até 25 palavras.
- **Chapéu:** a editoria ou a chave da editoria, em maiúsculas, até duas palavras. Use o nome da subeditoria quando ele for mais preciso que o da editoria. Exemplos: VIDA CRISTÃ, ORAÇÃO, FAMÍLIA, CASAIS, FILHOS, MISSÕES, IGREJA PERSEGUIDA, IGREJA, LIDERANÇA, ESPECIAL, ENTREVISTA, COMPORTAMENTO, EDUCAÇÃO.
- **Abertura:** o primeiro parágrafo retoma o assunto do título (é o trecho que o Google e o Discover mais leem). Pode ajustar a primeira frase do original para isso, sem mudar o sentido.
- **Estrutura:** a do original. Entrevista continua pergunta e resposta (pergunta em negrito). Reportagem mantém a ordem dos argumentos. Intertítulos em `<h4>`, **no máximo a cada 300 palavras**: se o original tiver trechos maiores sem intertítulo, crie intertítulos curtos tirados do próprio texto, e use a palavra-chave em pelo menos um deles.
- **Tamanho:** o do original, até cerca de 1.800 palavras no corpo. Acima disso, condense repetições, exemplos redundantes e citações longas (com [...]) sem perder argumento, fala ou dado. Registre o corte no resumo. **Nunca divida a matéria em partes nem use "continua no próximo post"** (decisão de 02/11/2026).
- **Assinatura no NX Feed:** "Redação". O nome do autor original vai no crédito do bloco final.
- **Link interno:** um, para matéria recente da Comunhão sobre o tema ou a pessoa, que já esteja no ar (nunca matéria agendada).

### Bloco final, nesta ordem

1. **Nota da Redação:** "Esta matéria foi publicada originalmente em [mês] de [ano] e atualizada em [data da execução]. O que mudou desde então:", e um item por mudança, com a fonte e o ano. Pessoas falecidas (mês e ano da morte), cargos que mudaram ou que não deu para confirmar, dados atualizados, dado sem equivalente, fato superado, lei aprovada. Até três links externos, todos aqui.
2. **Crédito:** matéria assinada → "Texto: [nome do jornalista], adaptado pela redação da Comunhão". Sem assinatura → "Redação Comunhão".
3. **Aviso de republicação:** "É uma republicação do acervo Comunhão."
4. **Origem:** revista → "Conteúdo adaptado da edição nº [X] da Revista Comunhão. Publicação original: [mês] de [ano]." Site → "Conteúdo adaptado de comunhao.com.br (post nº [N]). Publicação original: [dia] de [mês] de [ano]."

Modelo HTML:

```html
<h4>Nota da Redação</h4>
<p>Esta matéria foi publicada originalmente em abril de 2013 e atualizada em 28 de outubro de 2026. O que mudou desde então:</p>
<ul>
<li>Russell Shedd morreu em novembro de 2016, aos 87 anos, em São Paulo. Patrícia Shedd morreu em março de 2018.</li>
<li>Os "mais de 40 milhões" de evangélicos citados por Shedd são hoje 47,4 milhões, 26,9% da população com 10 anos ou mais, segundo o <a href="https://..." target="_blank" rel="noopener">Censo 2022 do IBGE</a>.</li>
<li>A AMTB estimou 19 mil missionários transculturais brasileiros em 2022; a medida difere da usada na entrevista.</li>
</ul>
<p><em>Texto: Gustavo Costa, adaptado pela redação da Comunhão.</em></p>
<p><em>É uma republicação do acervo Comunhão.</em></p>
<p><em>Conteúdo adaptado da edição nº 187 da Revista Comunhão. Publicação original: abril de 2013.</em></p>
```

## 7. Categorias (portal Comunhão = id 4)

Grave **uma** subcategoria (no máximo duas, quando o texto pertence claramente às duas). Ids conferidos em 28/10/2026.

| Editoria | Subcategorias (id) |
|---|---|
| Vida cristã | Vida Cristã 68045 · Espiritualidade 6082 · Oração 116626 · Bíblia e Ensino Bíblico 116623 · Estudos Bíblicos 6015 · Saúde Emocional 116621 |
| Família | Família 67603 · Filhos 117231 · Casais 6083 · Relacionamentos 116620 · Gerações 116622 · Jovens 117272 · Dia a dia 6086 |
| Missões | Missões 67595 · Igreja Perseguida 116628 · Evangelização 116627 |
| Igreja | Igreja 6060 · Liderança 116624 · Ministério 44632 · Discipulado 116625 · Gestão 16426 |
| Especiais | Especial 14 · Comunhão Debate 8888 · Depoimentos 53886 |
| Atuais | Fé & Sociedade 116629 · Comportamento 116633 · Educação 116632 · Saúde 16423 · Economia & Trabalho 116631 · Brasil & Mundo 116635 |

- Nunca as categorias-mãe Vida e Família 13, Igreja e Missões 116618, Cotidiano 16425 e Plugue-se 6062. Especial 14 só para reportagem especial, entrevista de fundo ou dossiê.
- Destaques 44517 entra junto com a subcategoria, só para a entrada das 22h (seção 9). Nunca Panorama 1, Giro 360 41941, Vida e Família 2 (114979, 114980, 114981), Edição Digital 54, Eleições 2026 117421, Conteúdo de Marca 108675 ou Institucional 114186.
- Id recusado: siga o padrão (seção 3).
- Tags (5 a 10): sempre "Acervo Comunhão", mais a pessoa principal, a instituição, o tema e a denominação quando houver.

## 8. SEO e imagem

- SEO pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo) depois de `criar_materia`. O título fica o original; a palavra-chave e o título SEO podem trazer o termo atual mais buscado. A meta description pode dizer que é reportagem do acervo, com o ano original. Nota SEO ≥ 85: os ajustes que mais sobem a nota são intertítulos a cada 300 palavras, abertura que retoma o título e imagem horizontal de 1.200 px ou mais.
- Imagem pelo padrão (seção 9): você escolhe e grava sozinho, olhando as fotos antes. Nesta rotina, a ordem de busca é: foto do acervo da Comunhão da pessoa ou do tema (`buscar_imagens` recomendadas, NX Fotos e imagem destacada de posts antigos do site que a NEIA traz) → divulgação oficial com crédito → imagem por IA. Foto antiga: "foto de arquivo" na descrição. Pessoa citada no título: foto dela, de preferência com 1.200 px ou mais; divulgação menor que isso é aceita, mas vai para as pendências. Evite foto com texto sobreposto, capa de produto, foto de outra matéria com pessoa identificável e iconografia que destoe do texto. Imagem de post antigo sem fonte e autor conhecidos não entra (direito de uso em dúvida).

## 9. Agendamento às 22h, com Destaques até as 12h

Decisão do Mário Fernando (02/11/2026): a matéria do acervo entra no ar **sempre às 22h00** (Brasília) do dia da execução, nos Destaques da Comunhão, e fica lá até o meio-dia seguinte; depois, só na categoria da editoria. Esta decisão vale como o "sim" da confirmação dupla para agendar a matéria da rotina.

1. Refaça a duplicidade (seção 3).
2. `criar_materia` (autor "Redação") → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar (com `trocar_trecho` e a `versao` mais recente) → `definir_imagem_destacada`. Categorias no portal 4: a subcategoria da editoria (seção 7) + **Destaques 44517**. Como a matéria vai para a capa, a imagem destacada é obrigatória.
3. `listar_agendamentos` do portal 4 para hoje: se já houver outra matéria do acervo agendada para as 22h, não agende uma segunda; registre.
4. `conferir_publicacao` (tipo agendar, portal 4) → `publicar_no_wordpress` com `portais` ["4"], `autores` ["Redação"], `quando` "DD/MM/AAAA 22:00" (hoje) e o `codigo_confirmacao`. Se a matéria só ficar pronta depois das 21h55, agende para 5 minutos à frente e registre. Nunca "agora" fora desse caso e nunca para outro dia. Uma chamada de cada vez; erro 429: espere e repita.
5. Confira em `listar_agendamentos` (ou `ver_materia`) que ficou agendada para 22h00 no portal 4, com as duas categorias, e guarde o link de prévia para o resumo.
6. Redes: nada de Instagram nesta rotina. O NX Feed pode soltar sozinho o post do X na hora da publicação.

**Saída do Destaques:** é feita pela rotina de Destaques (destaques-next), na primeira rodada a partir das 12h20 do dia seguinte, em qualquer dia: ela retira só a 44517 e mantém a subcategoria, sem mudar a data. Até lá, destaque manual não empurra a matéria do acervo e a regra das 12 horas no ar não vale para ela. Se alguém da equipe editar a matéria depois de publicada, a rotina de Destaques não mexe nela. Esta skill não tira nada do Destaques.

### Despublicação das versões antigas (no começo de cada execução)

Quando a matéria da rotina vai ao ar, as versões antigas da mesma matéria saem do site (decisão do Mário Fernando, 28/10/2026; vale como o "sim" da confirmação dupla).

1. `listar_materias` com `estado` publicado, `portal` 4, `campo_data` publicada, `autor` "Redação", de ontem até hoje, formato compacto. Abra com `ver_materia` só as que podem ser da rotina (título que não parece notícia do dia) e fique com as que têm a tag "Acervo Comunhão" e a frase "É uma republicação do acervo Comunhão." no texto.
2. Para cada uma, refaça as buscas 2 e 3 da seção 3 e a busca no NX Feed pelo título original, e ache os posts antigos da mesma matéria.
3. Post antigo que existe no NX Feed: `excluir_post_no_wordpress` com `portal` Comunhão, **sempre para a lixeira** (restaurável por 30 dias), nunca `de_vez`. Repita a chamada com o `codigo_confirmacao`.
4. Post antigo publicado direto no WordPress (sem matéria no NX Feed): nenhuma ferramenta da rotina alcança. Liste no resumo, em "Para tirar do ar", com link, id do post e o link da versão nova (para redirecionar a URL antiga).
5. Nunca mexa no post novo da rotina, em matéria de outra rotina ou em post que não seja a mesma matéria original.

## 10. Resumo e notificação

**Não envie e-mail.** Siga o padrão (seção 10): resumo curto, legível no celular, com `SendUserMessage`, título "Acervo Comunhão · no ar às 22h · DD/MM" e estas seções:

- **Agendada para as 22h:** título, horário, link de prévia, link do painel, editoria, chapéu, categoria + Destaques, origem (edição ou post, data original e autor), nota de escolha, nota SEO, imagem (real, arquivo ou IA).
- **O que foi atualizado:** pessoas (in memoriam, cargo), dados (antigo → atual, com fonte), fatos datados e falas com nota.
- **Despublicação:** posts antigos enviados à lixeira e "Para tirar do ar" (os que só existem no WordPress, com o link da versão nova).
- **Imagens de IA para validar**, quando houver.
- **Pendências:** cargo não confirmado, data deduzida, grafia ou autoria em dúvida, dado sem equivalente, lei a reconfirmar, corte de texto, título de entrevista ajustado, imagem abaixo de 1.200 px, agendamento fora das 22h.
- **Descartadas no caminho:** as candidatas que caíram e o motivo, em uma linha cada.

Notificação do app Claude ao terminar. Rodada sem matéria (nenhuma candidata passou da nota 13 ou da duplicidade): resumo com o motivo e as candidatas descartadas, sem agendar nada.