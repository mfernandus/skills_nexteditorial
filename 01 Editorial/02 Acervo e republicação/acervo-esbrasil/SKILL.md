---
name: "acervo-esbrasil"
description: "Uma vez por dia, adapta uma matéria atemporal do acervo da ES Brasil, da Revista SAMP e do site esbrasil.com.br (NEIA, até 4 meses atrás), atualiza pessoas, cargos, dados e fatos datados e agenda para as 22h, nos Destaques até as 12h."
---

# Acervo ES Brasil — matérias do acervo atualizadas

Objetivo: trazer de volta ao site da **ES Brasil** (esbrasil.com.br) o melhor do acervo da Next Editorial, **uma matéria por dia, no ar às 22h**, atualizada para o leitor de hoje. A skill busca na NEIA (a IA da casa, via MCP) nas três fontes do acervo (Revista **ES Brasil**, Revista SAMP e o próprio site), escolhe a matéria, confere quem está vivo e em que cargo, refaz os dados que sustentam a conclusão, confere toda orientação de saúde, marca o que é datado e agenda a publicação para as 22h, com Destaques até o meio-dia seguinte.

Temas: gestão, saúde pessoal, família, história capixaba, cuidados pessoais, alimentação e dietas, comportamento e história. O copyright do acervo é da Next Editorial.

A Comunhão tem rotina irmã, `acervo-comunhao`, com as mesmas regras de atualização, crédito e rodapé. Mudança de regra comum às duas se faz nas duas.

Responda sempre em português do Brasil. Execução automática: não faça perguntas. Na dúvida, tome a decisão mais conservadora (trocar de matéria) e registre no resumo. Escreva **ES Brasil** em negrito no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns da casa: pautas proibidas (2.1, vale acima de tudo), matéria agendada (2.2, vale acima de tudo), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), SEO (8), imagem destacada (9) e avisos (10). Onde as duas divergirem, vale esta skill nestes pontos, decididos pelo Mário Fernando:

- **Agendada para as 22h, com Destaques até as 12h** do dia seguinte, e depois só na categoria dela (seção 9; decisão de 02/11/2026 para as matérias do acervo).
- **Título original mantido** (seção 6).
- **Crédito ao jornalista original, aviso de republicação e rodapé de origem** no lugar do "Com informações de" (seção 6).
- **Até três links externos**, todos na Nota da Redação, para as fontes dos dados atualizados.
- **Despublicação das versões antigas duplicadas** (seção 10).
- **Matéria inteira, nunca dividida em partes** (seção 6).

## 1. Roteiro

A skill tem duas rodadas. Hora certa: `TZ=America/Sao_Paulo date`.

**Rodada da noite** (tarefa por volta das 21h):

1. Carregue `padrao-publicacao-next` e as ferramentas da NEIA e do NX Feed (ToolSearch).
2. Faça a conferência da véspera (seção 10.1).
3. Escolha a matéria do dia (seções 2 a 4).
4. Leia, limpe e atualize (seções 5 e 6).
5. Monte a matéria no NX Feed (seções 7 e 8), com o teste do vizinho antes de gravar as categorias (seção 8).
6. Agende para as 22h, com Destaques (seção 9).
7. Mande o resumo (seção 11).

**Rodada do meio-dia** (tarefa por volta das 12h): tire do Destaques a matéria do acervo que entrou às 22h da véspera e despublique as versões antigas dela (seção 10.2). Resumo curto.

## 2. Fontes no NEIA

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch. Uma chamada de cada vez; "Não foi possível conectar": repita a mesma chamada.

| Fonte | Id | O que tem | Melhor para |
|---|---|---|---|
| REVISTA ESBRASIL (magazine) | 019d1cf8-4fc8-72e4-ab29-5ef31d204e4d | Edição 1 (abr/2005) à 229, mensal | gestão, história capixaba, comportamento, qualidade de vida e saúde do executivo |
| REVISTA SAMP (magazine) | 019dc101-8ff6-7103-9b75-03490da18cb7 | Edições 09 (jun/2010) e 14 a 28 (out/2011 a abr/2015), trimestral; revista da operadora de saúde SAMP, do acervo da Next Editorial | saúde, alimentação, cuidados pessoais, família |
| ESBRASIL.COM.BR (wordpress_portal) | 019d2231-a834-71ec-af78-1ad6fa55f69a | Posts do site, com data, id do post e link | todos os temas, sobretudo Saúde e Estilo |

- `search-content` com `source` (nunca sem escopo), `page_size` de 20 a 50 e `next_cursor` para paginar. Filtrar `content_type` "article" ou "interview" ajuda a fugir de colunas e notas, mas o tipo e a seção que a NEIA atribui são só pista: erram para os dois lados.
- `get-article-content` traz o texto completo e o `word_count`; no site, também `wp_post_id`, `wp_url`, `published_at`, `wp_categories` e `featured_image`.
- `list-editions` (project_id = id da revista) traz a data de cada edição. A resposta da **ES Brasil** é grande e vem salva em arquivo: leia só as edições que interessam (por exemplo, com um script que filtra pelo `edition_number`).
- **Corte de tempo:** até 4 meses antes do dia da execução. Post do site mais novo que isso não entra.
- **Prefira a revista** (**ES Brasil** ou SAMP). O post do site entra quando é melhor que o equivalente da revista ou quando o tema só existe lá.
- O título que a NEIA dá à matéria às vezes foi gerado na ingestão ("Entrevista com a dermatologista Fulana sobre Calvície"). O título que vale é o impresso, que aparece no começo do `full_content`, depois do cabeçalho da editoria.
- **SAMP:** as edições 10, 11, 12 e 13 estão extraídas, mas sem artigos detectados na NEIA (out/2026). Não são buscáveis: ignore-as até a NEIA processá-las.

### Datas: conferir antes de usar

- Na revista, use **só mês e ano**.
- **ES Brasil:** as edições 185 a 229 vêm com 01/01/2000 (data vazia) e a 195 vem com nov/2020, fora da sequência. Deduza pela sequência das vizinhas (184 = dez/2020; 196 = dez/2021; 223 = jun/2024; 225B = dez/2024; 228B = ago/2025) e por marcas do texto. Registre "data deduzida" no resumo e como chegou nela.
- **SAMP:** trimestral (jan, abr, jul, out); a edição 09 é de junho de 2010.
- A mesma matéria pode aparecer em mais de uma edição (ex.: "Relaxe, Divirta-se, Descanse!", de Letícia Vieira, na edição 161, e de novo na 197 como "O impacto do excesso de trabalho na saúde mental"). O original é a **edição mais antiga**; a mais nova pode ser citada no rodapé ("republicada na edição nº 197").
- **Site:** o `published_at` pode ser posterior ao original (republicação, migração, reedição). Confira com a pasta da imagem (`/uploads/AAAA/MM/`) e com marcas do texto ("o inverno começou neste domingo (21)"). Se o post for republicação da revista (o texto avisa), busque a edição original e use a data dela.
- O site tem posts duplicados (o mesmo texto postado duas vezes por usuários diferentes, como "Cinco dicas de cuidados com a pele para homens"). O original é o mais antigo; os dois entram na lista de duplicidade (seção 4).

## 3. Escolha da matéria do dia

### Tema do dia

| Dia | Tema | O que entra |
|---|---|---|
| Segunda | Gestão | carreira, liderança, gestão de pessoas, empresa familiar e sucessão, produtividade, gestão do tempo, finanças pessoais, clima organizacional |
| Terça | Saúde | prevenção, check-up, sono, estresse, saúde mental, coração, articulações, saúde bucal, doenças comuns |
| Quarta | Família | filhos e limites, educação, convivência, refeições em família, avós e idosos, casal, trabalho x família |
| Quinta | História capixaba | colonização, imigração (italiana, alemã, pomerana e outras), formação das cidades, personagens, patrimônio, identidade e tradições (congo, paneleiras, ticumbi, folias) |
| Sexta | Cuidados pessoais | pele, cabelo, autoestima, bem-estar, beleza com orientação médica |
| Sábado | Alimentação e dietas | reeducação alimentar, alimentação equilibrada, hábitos à mesa, dietas com respaldo científico |
| Domingo | Comportamento e história | consumo, gerações, trabalho e vida, tecnologia no dia a dia, migração, e história do Brasil contada como reportagem (a maior nota entre os dois) |

- O dia vale pela data de Brasília da execução. A seção que a NEIA atribui ("Cultura", "Saúde", "Gestão RH") não define o tema: ele se define pela leitura do texto.
- **Gancho forte manda no dia:** nos 3 dias antes de uma data do calendário (seção 3.2), o tema do dia pode ser trocado pelo tema da data. Registre a troca no resumo.
- Matéria de estação (verão, inverno, férias, volta às aulas) só entra na própria estação.

### Busca

Faça de 4 a 8 buscas com termos do tema, nas fontes da tabela da seção 2, e varie as épocas (2005–2012, 2013–2019, 2020 em diante). Separe de 3 a 5 candidatas antes de ler a fundo: a duplicidade (seção 4) costuma derrubar uma ou duas.

### 3.1 Nota de escolha (0 a 5 cada, mínimo 13 de 20)

- **Atemporalidade:** o tema vale hoje para o leitor da **ES Brasil** (5) ou é preso ao fato da época (0).
- **Atualização viável:** pessoas públicas, dados e orientações que dá para conferir (5); depende de fato que não se confere mais (1).
- **Qualidade do original:** texto completo, bem apurado, sem trechos quebrados pela digitalização (5).
- **Interesse e busca:** tema procurado na internet, com gancho de calendário próximo ou com pessoa e lugar conhecidos do leitor capixaba (5).

Empate: o gancho de calendário, depois a fonte menos usada nos últimos 7 dias (revista **ES Brasil**, SAMP, site), depois a época menos usada, depois a maior presença de dados que mudaram.

### 3.2 Calendário de ganchos

Imigração italiana no ES (21/2) · Dia Mundial da Saúde (7/4) · Dia das Mães (2º domingo de maio) · Dia do Espírito Santo e da colonização (23/5) · Dia dos Pais (2º domingo de agosto) · Dia dos Avós (26/7) · aniversário de Vitória (8/9) · Dia Mundial da Alimentação (16/10) · Outubro Rosa · Novembro Azul · Dia do Trabalho (1/5) · virada do ano, férias e volta às aulas.

### 3.3 Fora da escolha

- Pautas proibidas do padrão (2.1): denúncia, aumento de tarifa, origem em órgão de controle.
- Política partidária e eleitoral, e governo da época como assunto.
- **Texto autoral assinado** (artigo, opinião, análise de articulista ou colaborador): é da rotina `artigos-acervo-esbrasil`. Na revista, o cabeçalho "ARTIGO" ou a minibio do autor no fim denunciam. Exemplos: textos de Manoel Goes Neto, Idalberto Moro, Pablo Lira e dos demais articulistas da lista dela.
- **Colunas fixas:** O Endereço da História, Modus Vivendi, Fim de Papo, Som & Cia, Mindset, Essas Mulheres, Zoom Marketing, **Família S/A** (Adriano Salvi e Danielle Quintanilha Merhi, que a NEIA marca como "article"), Tira-Gosto, Pratos do Dia, Periscópio, Gente, O editor recomenda, Panorâmicas, Target, Motores, VipES; na SAMP, **Fala, Doutor!** (perguntas e respostas).
- Editorial, carta e depoimento de leitor, agenda, nota curta (menos de 400 palavras), receita isolada, resenha, tendência de moda da estação, publicidade, publieditorial e Conteúdo de Marca.
- **Institucional da SAMP:** planos, rede credenciada, eventos e homenagens da empresa, palavra da diretoria, responsabilidade social da operadora.
- Post do site cuja única fonte é uma clínica, um plano de saúde ou uma marca e que funciona como divulgação.
- Guia turístico com serviço (restaurantes, pousadas, horários, preços): é território do Destinos ES. A história de um lugar, sem o serviço, pode entrar.
- **Saúde e alimentação com orientação superada** que exigiria reescrever a matéria (ex.: texto construído em torno da pirâmide alimentar e das porções do guia de 2006); nota de uma página sobre um estudo isolado ("estudo aponta que maçã combate o colesterol"); dieta da moda; suplemento, remédio ou procedimento com promessa de resultado.
- Tema sensível que pede tratamento atual e revisão humana: suicídio, automutilação, transtornos alimentares, abuso, aborto, gravidez na adolescência, violência.
- Matéria cujo fato principal foi superado (evento com data, campanha de um ano, lançamento, inauguração, ranking anual, resultado).
- Matéria presa a um contexto que passou (pandemia, eleição, Copa, crise de um ano) sem argumento que se sustente fora dele.
- Retrospectiva, balanço do ano e matéria comemorativa da própria revista.
- Original com mais de 3.000 palavras que não dá para condensar sem perder argumento: escolha outra (a matéria nunca é dividida em partes).
- Obituário e cobertura de enterro.
- Matéria já adaptada por esta rotina (seção 4).

### 3.4 Ponto de partida (varredura de 02/11/2026)

Candidatas achadas na varredura inicial, ainda não lidas a fundo (a não ser quando indicado). Passam pela seção 4 e por toda a conferência como qualquer outra.

- **Gestão:** "De pai para filho: a complexidade da sucessão em empresas familiares" (Ana Lúcia Ayub, ES Brasil 13; 401b13f8-3227-4053-a51a-3557fedaa4e0) · "O desafio da sucessão familiar" (Katilaine Chroas, ES Brasil 155; 8d598c37-fbb8-4a95-93b5-1b24422869fe) · "Seja senhor do seu tempo" (ES Brasil 94; d7859309-8613-491c-a1b1-1f49c6abaea4) · "Metas, lucros e felicidade no ambiente corporativo" (Fabiana Tostes, ES Brasil 96; 1e04075e-155c-4688-9c9f-ec7b86373b9d).
- **Saúde:** "Dicas para dormir bem" (Lilia Barros, SAMP 15; 430624df-b9fd-4398-9e04-8ec0c19d3ae3) · "Estresse: como driblar esse mal" (Taís Hirschmann, SAMP 20; 8424cab2-7ea3-4345-87ca-4d15d4dc006f) · "Articulações: cuide bem delas" (SAMP 27; 6065b1f6-3299-4340-ac43-5cec4000f286) · "A importância do check-up para a saúde" (ES Brasil 98; 306cb911-1a75-48f9-a2ff-f3709f93b41f) · "Relaxe, divirta-se, descanse!" (Letícia Vieira, ES Brasil 161; 9dab7df5-b414-4099-8821-f3a259a7e44c).
- **Família:** "A arte de educar e impor limites" (Taís Hirschmann, SAMP 17; 38317bdb-eefb-4e2a-a1f0-d6e5fa5da6c7) · "O poder das refeições à mesa" (Nadia Baptista, SAMP 16; bd7db777-10af-4ac3-818d-5b9b07d1df20) · "Avós: uma contribuição valiosa" (SAMP 22; 0ada6625-82ec-4e6e-92be-ddb0a7c4eb74) · "Seus filhos vivem brigando? Você pode ser o problema" (SAMP 26; f00b18b5-0852-4878-b403-531ba3e74639) · "Sucesso na carreira, fracasso em família?" (Elayne Batista, ES Brasil 24; b4b45d3c-2dd8-4a21-907a-139563db71ac).
- **História capixaba:** "O jeito capixaba de ser" (Ana Lúcia Ayub, ES Brasil 40; 4fdbc8c9-55fd-4be8-962a-7edefa642467; lida: 2.253 palavras, pede condensação, atualização da população e da migração pelo Censo 2022 e conferência de historiadores e cargos) · "Lembrando como tudo começou: a formação da identidade capixaba" (Cynthia Silva, ES Brasil 20; bd804335-bb8f-43fa-b351-b64dda2670f7) · "Nossa história: a formação de Vila Velha" (Luciene Araújo, ES Brasil 140; 8fb24027-8959-4145-a93a-7e056ec25241) · "Vasco Fernandes Coutinho: o primeiro governador do Espírito Santo" (Heliomara Mulullo, ES Brasil 43; 82f4f9fe-8cd6-4e25-a99c-3035f477b0d7) · "150 anos da imigração italiana" (Kamila Rangel, ES Brasil 220; 2bd3a3a6-192d-4fe2-b3d2-9fad71ea78ca; gancho 21/2).
- **Cuidados pessoais:** "Saúde dos cabelos: importância e cuidados" (SAMP 21; ab7bb24e-a3e0-455b-9b35-9e63a90045b4) · entrevista sobre calvície com a dermatologista Renata Poubel (SAMP 09; a1ea84ca-be80-4191-9e4c-327822fd3d6e).
- **Alimentação:** "Comer bem para viver com saúde" (Pammela Volpato, SAMP 15; 92626d00-7b7f-4298-8068-3f89a067dde7; lida: 1.182 palavras; o box de porções segue o guia antigo e precisa do Guia Alimentar de 2014; o telefone do serviço sai) · "Pratos coloridos: por uma vida mais saudável" (SAMP 23; 979f5665-c498-4a2c-a875-a0a7d818a9a4) · "Coma bem e passe longe das doenças" (SAMP 21; 20f2a9f1-565b-4a8b-b7d3-83e82dde48f0).
- **Comportamento:** "Workaholic: é possível ser feliz?" (Lorena Vasques, ES Brasil 4; 585280ee-3471-4dc5-bf27-c9b646a970b0) · "Workaholic: existe cura para os viciados em trabalho?" (Jacqueline Vitória, ES Brasil 59; bfc44a6c-0fbb-4e6a-867d-ee717b3eb931) · "Escolhi ser capixaba" (Vitor Taveira, ES Brasil 191; 65ad18b8-3436-4fcd-9e55-3899b5800e0b).

## 4. Duplicidade

As matérias da rotina se reconhecem por três marcas: o título original mantido, a tag "Acervo ES Brasil" e a frase de republicação no pé do texto ("É uma republicação do acervo ES Brasil." ou "É uma republicação do acervo da Next Editorial.").

Antes de escrever e de novo antes de agendar:

1. **Rotina e NX Feed:** `listar_materias` com `busca` pelo título original (e por uma palavra forte dele), todos os estados, últimos 365 dias, formato compacto; rascunhos sem filtro de portal. Para ver as matérias recentes da rotina: `listar_materias` com `portal` 1, `estado` agendado e depois publicado, `autor` "Redação", últimos 30 dias, formato compacto, e confira com `ver_materia` as que têm a tag e a frase de republicação. A mesma matéria original nunca é adaptada duas vezes. Confira também a tag "Acervo de Artigos" (rotina `artigos-acervo-esbrasil`): o mesmo texto não vai para as duas.
2. **Site, na NEIA:** `search-content` na fonte do portal pelo título original e pelo tema central, com a pessoa principal quando houver.
3. **Site, na web:** WebSearch `site:esbrasil.com.br "<título original>"` e `site:esbrasil.com.br <tema> <pessoa>`.

Como decidir:

- **A mesma matéria original já está no site** (republicação antiga ou post duplicado): siga com a adaptação atualizada e guarde a lista dos posts antigos (link, id do post e se existe no NX Feed). Eles saem do ar depois que a versão nova estiver no ar (seção 10).
- **O site tratou o mesmo tema nos últimos 4 meses** (inclusive pela rotina de Estilo ou pelo turno noturno): troque de matéria. "Mesmo tema" é o mesmo assunto com o mesmo enfoque (ex.: higiene do sono), não a editoria inteira.
- **Rascunho ou matéria agendada da equipe sobre o tema:** troque de matéria.

## 5. Leitura e limpeza do texto

- Leia o texto inteiro com `get-article-content`. Texto incompleto ou com trecho ilegível que muda o sentido: troque de matéria.
- **Cabeçalho da página:** tire a editoria impressa ("ESPECIAL", "NUTRIÇÃO"), o "por Fulano" solto, os créditos de foto ("Foto: Shutterstock / …") e os olhos que só repetem o corpo. Guarde o nome do jornalista para o crédito.
- **Digitalização:** corrija palavras trocadas, hifenização quebrada, frases partidas por box ("Uma criança que … se alimenta adequadamente") e repetições. Corrigir erro evidente de transcrição numa citação é permitido; mudar o que a pessoa disse, não. Trecho truncado que não dá para reconstruir: resuma em palavras próprias ou tire, e registre no resumo.
- **Site:** tire "- Continua após a publicidade -", blocos "leia também" com links antigos, shortcodes velhos e qualquer link estranho (spam).
- **Nomes:** a mesma pessoa pode aparecer com várias grafias (Taís Hirschmann e Thaís Hirschman; Lilia e Lila Barros). Use a grafia mais limpa, confira na web quando for pessoa pública e registre no resumo quando houver dúvida.
- **Autoria:** vale o crédito impresso na revista. No site, o campo `author` é quem postou no WordPress, e o `metadata.llm_author` às vezes é o especialista citado, não o jornalista: vale o "Por Fulano" do texto; sem ele, "Redação **ES Brasil**".
- **Boxes:** box útil (dicas, enquete com depoimentos, serviço atemporal) pode ficar. **Box de serviço com telefone, endereço ou preço de consultório, clínica ou loja sai** (dado de contato envelhece e vira propaganda).
- **SAMP:** tire as menções à SAMP como operadora (planos, rede credenciada, serviços da empresa, "a SAMP oferece"). O especialista citado fica pela fala, com o cargo conferido (seção 6.1), sem vínculo comercial.
- **Grafias e métricas:** padronize unidades, moeda (R$), números (mil, milhões) e datas por extenso.

## 6. Atualização

### 6.1 Pessoas públicas (empresários, executivos, historiadores, especialistas, médicos, autoridades)

- **Vida:** confira se a pessoa está viva. Morte só com **duas fontes independentes** (a cobertura da própria **ES Brasil** no site vale como uma delas; comunicado da instituição da pessoa também). Falecida: "(in memoriam)" logo depois do nome **na primeira menção**, e o mês e o ano da morte na Nota da Redação. Personagem histórico morto antes da publicação original (Vasco Fernandes Coutinho, Maria Ortiz, Anchieta) não leva marca.
- **Cargo e função:** confira o cargo atual. Mudou: o texto do repórter traz o cargo atual; o antigo só aparece ("então presidente", "na época coordenadora do curso de Nutrição da…") quando explica a fala. Político citado na época: o cargo da época ("então deputado federal"), sem atualizar a trajetória política. Não deu para confirmar (comum com médicos e professores): "então da instituição X" no texto, um item na Nota da Redação dizendo que os vínculos são os da época e registro no resumo.
- **Médico, nutricionista, psicólogo, dentista:** a fala fica quando continua de acordo com a orientação atual (seção 6.5). Não divulgue consultório, telefone nem preço.
- **Grafia** do nome conforme a fonte oficial da pessoa ou da instituição.

### 6.2 Pessoas privadas (personagens, famílias, leitores, enquetes)

- Não pesquise a vida delas.
- Marque o tempo: "na época", "então com 14 anos", "que na época esperava o primeiro filho". Em enquete, a profissão vira "na época secretária".
- Quem era menor de idade na época: primeiro nome mantido, com "então com X anos".

### 6.3 Dados e números

- Todo número que **sustenta a conclusão** da matéria precisa ser atualizado com a fonte oficial mais recente (IBGE e Censo 2022, IJSN, Sesa, Ministério da Saúde e Vigitel, INCA, OMS, Sebrae, Caged, Findes, Fecomércio-ES, institutos de pesquisa), aberta com WebFetch.
- **Mesma métrica:** compare só o que mede a mesma coisa. Sem dado equivalente, use o dado mais próximo e diga na Nota da Redação que a medida é diferente.
- **Valores em reais:** diga se a comparação é nominal (sem descontar a inflação).
- **No texto do repórter:** troque o número pelo atual, com a fonte e o ano. Mantenha o número antigo quando a comparação muda a leitura ("em 2008, a Grande Vitória tinha 1,6 milhão de habitantes; no Censo 2022, …").
- **Dentro de citação:** a fala fica como foi dita; o número atual vai para a Nota da Redação.
- Número sem atualização possível e sem peso na conclusão: pode sair do texto; registre no resumo. Dado histórico (ano da chegada de um navio, data de fundação) não precisa de atualização, mas confira uma vez.
- Estudo citado como novidade ("um estudo publicado em dezembro…"): dê o ano e confira se ainda vale ou se houve revisão; se foi superado, diga na Nota da Redação ou tire.

### 6.4 Fatos e falas datados

- Expressões de tempo no texto do repórter viram datas ("este ano" → "em 2013"; "atualmente" → "na época"; "há 20 anos" → "em 1988"). Pergunta de entrevista que diz "hoje" pode ser ajustada ("Como era a rotina em 2013?").
- Fato que mudou (lei, norma, instituição extinta ou que mudou de nome, empresa vendida, tecnologia superada): explique na Nota da Redação quando muda o sentido; detalhe de época que não muda o sentido fica sem nota.
- Lei, norma e projeto de lei: confira a situação no site da Câmara, do Senado, do Planalto ou do órgão (ex.: NR-1 no Ministério do Trabalho) no dia da execução.
- Fala de época sobre governo, partido ou político ("após 12 anos de desgaste nos governos…"): tire com [...] quando não for essencial ao argumento; se for essencial, troque de matéria.
- Nunca invente fala, número, data, nome ou cargo.

### 6.5 Saúde, alimentação e cuidados pessoais

Toda orientação de saúde é conferida antes de ir ao ar. **Na dúvida, troque de matéria.**

- Confira cada recomendação na fonte oficial atual, aberta com WebFetch: Ministério da Saúde, **Guia Alimentar para a População Brasileira (2014)**, INCA, Anvisa, OMS e sociedades médicas (Sociedade Brasileira de Cardiologia, de Diabetes, de Endocrinologia, de Pediatria e de Dermatologia, Associação Brasileira do Sono).
- **Orientação que mudou, no texto do repórter:** atualize pelo guia ou pela sociedade atual e registre na Nota da Redação (ex.: o box de porções diárias do guia de 2006 vira as orientações do Guia Alimentar de 2014, que prioriza alimentos in natura e minimamente processados e não conta porções).
- **Orientação que mudou, dentro de citação:** a fala não pode ficar como recomendação. Tire o trecho com [...] e explique na Nota da Redação; se a fala é o coração da matéria, troque de matéria.
- Sem dose, sem prescrição, sem nome comercial de remédio ou suplemento, sem promessa de resultado. Termine as orientações com a recomendação de procurar o profissional (médico, nutricionista, dentista, psicólogo).
- Procedimento estético ou tecnologia citada como novidade: confira se ainda é usado e se é aprovado pela Anvisa; superado, tire ou troque de matéria.

## 7. Formato da matéria

- **Título:** o original, mantido. Só corrija caixa alta e erro de digitação. O título SEO (até 60 caracteres) pode ser diferente. Exceção: em entrevista cujo título impresso é só o nome do entrevistado, use o nome seguido de dois-pontos e de uma frase dita por ele na própria entrevista, entre aspas; registre no resumo.
- **Linha fina:** a original (a primeira frase, se ela tiver mais de uma); se não houver, uma frase de até 25 palavras.
- **Chapéu:** a chave do tema, em maiúsculas, até duas palavras. Exemplos: GESTÃO, CARREIRA, LIDERANÇA, EMPRESA FAMILIAR, SAÚDE, SONO, SAÚDE MENTAL, FAMÍLIA, FILHOS, HISTÓRIA CAPIXABA, IMIGRAÇÃO, IDENTIDADE CAPIXABA, HISTÓRIA, BELEZA, PELE, CABELOS, ALIMENTAÇÃO, NUTRIÇÃO, COMPORTAMENTO.
- **Abertura:** o primeiro parágrafo retoma o assunto do título (é o trecho que o Google e o Discover mais leem). Pode ajustar a primeira frase do original para isso, sem mudar o sentido.
- **Estrutura:** a do original. Entrevista continua pergunta e resposta (pergunta em negrito). Reportagem mantém a ordem dos argumentos. Intertítulos em `<h4>`, **no máximo a cada 300 palavras**: se o original tiver trechos maiores sem intertítulo, crie intertítulos curtos tirados do próprio texto, com a palavra-chave em pelo menos um deles. Listas em `<ul>`.
- Depois do 2º parágrafo: `[sc name="leia_mais" categoria="<slug da categoria mais específica gravada>" num_posts="2" ][/sc]` (a filha, se houver; se só a mãe foi gravada, o slug da mãe, por exemplo `cotidiano`).
- **Tamanho:** o do original, até cerca de 1.800 palavras no corpo. Acima disso, condense repetições, exemplos redundantes e citações longas (com [...]) sem perder argumento, fala ou dado. Registre o corte no resumo. **Nunca divida a matéria em partes nem use "continua no próximo post".**
- **Assinatura no NX Feed:** "Redação". O nome do autor original vai no crédito do bloco final.
- **Link interno:** um, para matéria recente da **ES Brasil** sobre o tema ou a pessoa, que já esteja no ar (nunca matéria agendada).

### Bloco final, nesta ordem

1. **Nota da Redação:** "Esta matéria foi publicada originalmente em [mês] de [ano] e atualizada em [data da execução]. O que mudou desde então:", e um item por mudança, com a fonte e o ano: pessoas falecidas (mês e ano da morte), cargos que mudaram ou que não deu para confirmar, dados atualizados, dado sem equivalente, orientação de saúde revista, fato superado, lei aprovada. Até três links externos, todos aqui.
2. **Crédito:** matéria assinada → "Texto: [nome do jornalista], adaptado pela redação da ES Brasil". Sem assinatura → "Redação ES Brasil".
3. **Aviso de republicação:** fonte **ES Brasil** (revista ou site) → "É uma republicação do acervo ES Brasil." Revista SAMP → "É uma republicação do acervo da Next Editorial."
4. **Origem:**
   - Revista **ES Brasil** → "Conteúdo adaptado da edição nº [X] da Revista ES Brasil. Publicação original: [mês] de [ano]."
   - Revista SAMP → "Conteúdo adaptado da edição nº [X] da Revista SAMP, do acervo da Next Editorial. Publicação original: [mês] de [ano]."
   - Site → "Conteúdo adaptado de esbrasil.com.br (post nº [N]). Publicação original: [dia] de [mês] de [ano]."

"ES Brasil" vai em negrito (`<strong>`) no bloco final.

Modelo HTML (fonte SAMP):

```html
<h4>Nota da Redação</h4>
<p>Esta matéria foi publicada originalmente em janeiro de 2012 e atualizada em 7 de novembro de 2026. O que mudou desde então:</p>
<ul>
<li>As orientações de porções diárias do box seguiam o guia alimentar de 2006. Foram trocadas pelas do <a href="https://..." target="_blank" rel="noopener">Guia Alimentar para a População Brasileira</a>, do Ministério da Saúde, de 2014, que prioriza alimentos in natura e minimamente processados.</li>
<li>Os vínculos profissionais da especialista ouvida são os da época.</li>
</ul>
<p><em>Texto: Pammela Volpato, adaptado pela redação da <strong>ES Brasil</strong>.</em></p>
<p><em>É uma republicação do acervo da Next Editorial.</em></p>
<p><em>Conteúdo adaptado da edição nº 15 da Revista SAMP, do acervo da Next Editorial. Publicação original: janeiro de 2012.</em></p>
```

## 8. Categorias, SEO e imagem (portal ES Brasil = 1)

### Categorias

Grave a mãe do tema e, quando houver uma filha certa para o assunto, a filha (no máximo duas filhas, quando o texto pertence claramente às duas), mais **Destaques 11966** na entrada (seção 9). Sem filha certa, fica só a mãe. Ids conferidos em 02/11/2026.

**Escolha pelo assunto central, não pela palavra.** A categoria é decidida pelo que a matéria trata de fato, não por palavras do título ou das tags: "educar os filhos" é criação de filhos (Família), não Educação; "em casa" no texto não leva para Em Casa. Erro corrigido em 05/11/2026: "A arte de educar e impor limites" foi gravada em Cotidiano › Educação, e o Mário Fernando mandou corrigir para a categoria certa.

| Tema | Categorias (ids) |
|---|---|
| Gestão | Economia 58 + Economia e Negócios 83880 · ou Empreendedorismo 16978 (pequena empresa, empresa familiar) · ou Mercado de Trabalho 10014 (carreira, RH) |
| Saúde | Cotidiano 1615 + Saúde 119 |
| Família | Cotidiano 1615, sem filha: criação dos filhos, limites, birra, adolescência, convivência, casal, avós, refeições em família, trabalho x família · Cotidiano 1615 + Saúde 119 só quando o assunto central é saúde (doença, vacina, sono, alimentação infantil, saúde mental com orientação clínica) · **nunca** Educação 1722 nem Em Casa 14737 |
| História capixaba | Destinos ES 74964 + O endereço da história 104 (fatos, personagens, cidades) · tradições e cultura popular: Diversão e arte 17028 + Cultura e Arte 74658 |
| Cuidados pessoais | Estilo 3971 + Saúde e estética 42109 |
| Alimentação e dietas | Cotidiano 1615 + Saúde 119 · culinária e receitas com história: Diversão e arte 17028 + Gastronomia 86 |
| Comportamento | Cotidiano 1615 · trabalho e carreira: Economia 58 + Mercado de Trabalho 10014 |
| História (Brasil e geral) | Diversão e arte 17028 + Cultura e Arte 74658 |
| Reportagem especial ou dossiê | Especial 35 + a categoria do tema |

- Nunca Artigos 11960 (é da rotina de artigos), Colunas e filhas, Conteúdo de Marca 13596, Edição Digital 77573 e 69, Eleições 2026 84181, Institucional 80596, Panorama 63, Últimas Notícias 65, Sem categoria 1, Vida Capixa 2 84219, Display AD 53445 ou Rede Social 32952.
- **Filhas que parecem servir e não servem** (conferido no site em 05/11/2026):
  - Educação 1722 é ensino: escola e rede de ensino, matrícula, Enem, Fies, universidades, cursos técnicos, pesquisa acadêmica, política educacional. Matéria de família só entra nela quando o assunto central é a própria escola (escolha da escola, adaptação escolar, dever de casa).
  - Em Casa 14737 é serviço da casa: contas de água, luz e gás, Procon e consumo, manutenção, segurança da casa, economia doméstica. Convivência e família não entram nela.
  - Saúde e estética 42109 é beleza e cuidados pessoais, não saúde em geral (essa é Saúde 119).
- **Teste do vizinho (obrigatório antes de gravar):** para cada filha escolhida, rode `listar_materias` com `categoria` = id da filha, `portal` 1, `estado` publicado, `campo_data` publicada, últimos 60 dias, formato compacto, 20 itens. Leia os títulos: a matéria do acervo tem de ser do mesmo tipo de assunto das vizinhas. Se não for, tire a filha e grave só a mãe (ou a filha que passar no teste). Registre no resumo a filha descartada e o motivo, em uma linha.
- Id recusado: siga o padrão (seção 3).
- Tags (5 a 10): sempre "Acervo ES Brasil", mais a pessoa principal, a instituição, o tema e a cidade quando houver.

### SEO

Pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo) depois de `criar_materia`. O título fica o original; a palavra-chave e o título SEO podem trazer o termo atual mais buscado. A meta description pode dizer que é reportagem do acervo, com o ano original. Nota SEO ≥ 85: os ajustes que mais sobem a nota são intertítulos a cada 300 palavras, abertura que retoma o título e imagem horizontal de 1.200 px ou mais.

### Imagem

Pelo padrão (seção 9): você escolhe e grava sozinho, olhando as fotos antes. Ordem de busca nesta rotina:

1. Foto do acervo da casa da pessoa, do lugar ou do tema (`buscar_imagens` recomendadas, NX Fotos e imagem destacada de posts antigos do site que a NEIA traz em `featured_image`, quando o autor e a fonte forem da casa).
2. História: foto histórica de acervo público com crédito (Arquivo Público do Estado, prefeitura, Iphan) ou divulgação oficial do lugar.
3. Divulgação oficial com crédito.
4. Imagem por IA (padrão 9.1), nunca de procedimento, remédio, rosto de personagem ou lugar reconhecível.

**As fotos da revista impressa não se reaproveitam:** na SAMP e na **ES Brasil** muitas vêm de banco pago (Shutterstock e semelhantes), com licença só para a edição. Foto antiga da casa: "foto de arquivo" na descrição. Pessoa citada no título: foto dela, de preferência com 1.200 px ou mais; menor que isso é aceita, mas vai para as pendências. Imagem de post antigo sem fonte e autor conhecidos não entra.

## 9. Agendamento às 22h, com Destaques

1. Refaça a duplicidade (seção 4).
2. `criar_materia` (autor "Redação", categorias do tema + Destaques 11966) → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar (com `trocar_trecho` e a `versao` mais recente) → `definir_imagem_destacada`.
3. `conferir_publicacao` (tipo agendar, portal 1) → `publicar_no_wordpress` com `portais` ["1"], `quando` "DD/MM/AAAA 22:00" (hoje) e o `codigo_confirmacao` (decisão de publicação direta, padrão seção 2). Se a matéria só ficar pronta depois das 21h55, agende para o próximo horário de 15 em 15 minutos (22h15, 22h30…). Uma chamada de cada vez; erro 429: espere e repita.
4. Guarde o `materia_id`, o horário agendado e o link de prévia para o resumo.
5. Redes: o NX Feed pode criar sozinho o story e o post do X da matéria agendada. Pelo padrão (2.2), nada de rede sai antes das 22h; esta rotina não cria, não aprova e não adianta conteúdo de rede.

A matéria fica nos Destaques da noite até as 12h do dia seguinte. A saída é a rodada do meio-dia (seção 10.2). Se a equipe ou o rodízio de Destaques tirar antes, não recoloque: registre no resumo do meio-dia.

## 10. Saída do Destaques e despublicação

### 10.1 Conferência da véspera (começo da rodada da noite)

1. `listar_materias` com `estado` publicado, `portal` 1, `campo_data` publicada, `autor` "Redação", de anteontem até hoje, formato compacto. Abra com `ver_materia` só as que podem ser da rotina e fique com as que têm a tag "Acervo ES Brasil" e a frase de republicação.
2. Se alguma ainda estiver em Destaques depois das 12h (a rodada do meio-dia falhou), tire agora, como em 10.2.
3. Se as versões antigas dela ainda estiverem no ar, despublique agora, como em 10.2.

### 10.2 Rodada do meio-dia

1. Ache a matéria do acervo que foi ao ar às 22h da véspera (como em 10.1, passo 1) e confirme que está no ar: `listar_publicacoes` com `portal` "1", `situacao` "publicado" e `busca` pelo título, e o link com o slug (não `?p=`).
2. **Tirar do Destaques:** `historico_da_materia` (confirme que é da rotina e se alguém da equipe editou depois; se editou e tirou o Destaques, não mexa) → `ver_materia` (formato_texto nenhum; pegue a `versao` e as categorias) → `editar_materia` com as mesmas categorias, só sem a 11966 → `atualizar_no_wordpress` com `portais` ["1"] (mantém status e data e não posta no X de novo), repetindo com o `codigo_confirmacao`. Nunca tire outra categoria; se o post ficaria sem categoria, não tire e registre.
3. **Despublicar as versões antigas da mesma matéria** (decisão do Mário Fernando, 28/10/2026, para o acervo; vale como o "sim" da confirmação dupla): refaça as buscas 2 e 3 da seção 4 e a busca no NX Feed pelo título original.
   - Post antigo que existe no NX Feed: `excluir_post_no_wordpress` com `portal` ES Brasil, **sempre para a lixeira** (restaurável por 30 dias), nunca `de_vez`. Repita a chamada com o `codigo_confirmacao`.
   - Post antigo publicado direto no WordPress (sem matéria no NX Feed): nenhuma ferramenta da rotina alcança. Liste no resumo, em "Para tirar do ar", com link, id do post e o link da versão nova (para redirecionar a URL antiga).
   - Nunca mexa em matéria de outra rotina, da equipe ou em post que não seja a mesma matéria original.
4. Resumo curto (seção 11).

## 11. Resumo e notificação

**Não envie e-mail.** Siga o padrão (seção 10): resumo curto, legível no celular, com `SendUserMessage`.

**Rodada da noite**, título "Acervo **ES Brasil** 22h · DD/MM", com estas seções:

- **Agendada para as 22h:** título, link de prévia, link do painel, tema, chapéu e categorias (com o resultado do teste do vizinho), origem (fonte, edição ou post, data original e autor), nota de escolha, nota SEO, imagem (real, arquivo ou IA).
- **O que foi atualizado:** pessoas (in memoriam, cargo), dados (antigo → atual, com fonte), orientações de saúde revistas, fatos datados e falas com nota.
- **Véspera:** saída do Destaques e despublicação feitas agora (seção 10.1), quando houver.
- **Imagens de IA para validar**, quando houver.
- **Pendências:** cargo não confirmado, data deduzida, grafia ou autoria em dúvida, dado sem equivalente, lei a reconfirmar, corte de texto, título de entrevista ajustado, imagem abaixo de 1.200 px.
- **Descartadas no caminho:** as candidatas que caíram e o motivo, em uma linha cada.

**Rodada do meio-dia**, título "Acervo **ES Brasil** 12h · DD/MM": saiu do Destaques (título, link, categorias que ficaram), versões antigas enviadas à lixeira, "Para tirar do ar" e pendências.

Seção sem itens: "nenhuma". Notificação do app Claude ao terminar a rodada da noite; na do meio-dia, só se houver problema. Rodada sem matéria (nenhuma candidata passou da nota 13, da duplicidade ou da conferência de saúde): resumo com o motivo e as candidatas descartadas, sem matéria.