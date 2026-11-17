---
name: "igreja-comunhao"
description: "Editoria Igreja da Comunhão em 5 rodadas diárias (7h, 10h, 13h, 16h e 20h), 1 matéria publicada direto por rodada nos eixos igreja, gestão, estatísticas, tecnologia, audiovisual e direito. Carregar depois da padrao-publicacao-next."
---

# Igreja — Comunhão (5 rodadas por dia)

Rotina da editoria **Igreja** do portal Comunhão (comunhao.com.br; no NX Feed, portal **4**). Em cada rodada ela produz e **publica 1 matéria nova** sobre a vida das igrejas evangélicas, no eixo do horário.

- Carregue antes a `padrao-publicacao-next`: publicação direta, NX Feed, duplicidade, direitos, SEO, imagem e avisos vêm de lá. Aqui fica só o que é da editoria Igreja. Onde as duas divergirem, vale esta skill naquele ponto (por exemplo, o crédito a veículo internacional do item 5), **salvo as pautas proibidas da seção 2.1 da padrão, que valem acima desta skill**: denúncia, aumento de tarifa e o que nasce de Ministério Público, Tribunal de Contas ou controladoria não entram em nenhum eixo.
- É irmã da rotina de **Missões** (`missoes-comunhao`), com a mesma configuração e outra pauta. **Missões, igreja perseguida, violência contra cristãos no exterior e evangelização são de Missões**: esta rotina não escreve sobre eles nem usa as categorias 67595, 116628 e 116627.
- **Igreja Católica, papa e Vaticano ficam fora desta rotina, salvo doença ou morte** (decisão de Mário Fernando, 10/11/2026; exceção incluída em 17/11/2026). Fora a exceção abaixo, nenhuma matéria sobre a Igreja Católica, o papa, o Vaticano ou a Santa Sé, nem mesmo com eles como personagem secundário. Isso inclui declarações e documentos do papa e do Vaticano, CNBB, dioceses, paróquias, padres, bispos, ordens religiosas, santos, movimentos, organizações, rádios e TVs católicas. Eles também não entram como fonte, aspas, link externo ou interno, dado de comparação (por exemplo, o percentual de católicos no Censo) nem imagem. Item do feed internacional ou da web sobre esses temas é descartado direto, sem nota de pauta, salvo os de doença ou morte. Lei, decisão judicial ou pesquisa que afeta todas as igrejas continua valendo, contada só pelo lado das igrejas evangélicas.
  - **Única exceção: doença ou morte.** Internação, doença grave ou morte do papa ou de uma liderança católica de grande relevância pode virar matéria, curta, factual e respeitosa: o fato, o estado de saúde ou a morte e a repercussão entre líderes evangélicos. Sem doutrina católica, sem cobertura de rito, conclave ou sucessão e sem juízo sobre a fé católica. Nessa matéria, o boletim oficial (Vaticano, Santa Sé ou a instituição da pessoa) pode ser citado como fonte do fato, e uma foto da pessoa pode ilustrar; templo, símbolo ou celebração católica, não.
- Execução agendada não tem ninguém acompanhando: não faça perguntas. Não envie e-mail.

## 1. Rodadas e eixos

O agendamento começa 20 minutos antes de cada rodada. Descubra a rodada e o dia com `TZ=America/Sao_Paulo date '+%H:%M %u'`: a rodada é a próxima hora cheia entre 7h, 10h, 13h, 16h e 20h; `%u` é o dia da semana (1 = segunda … 7 = domingo).

| Rodada | Eixo preferido | Categorias (portal Comunhão) |
|---|---|---|
| 7h | **Igreja**: vida das igrejas no Brasil e no ES, fato das últimas 24 h | Igreja 6060 |
| 10h | **Gestão** | Gestão 16426 (ou Liderança 116624 / Ministério 44632, ver 2.2) |
| 13h | **Estatísticas** | Igreja 6060 (+ a do assunto, ver 2.3) |
| 16h | **Tecnologia** (seg, qua, sex, dom) · **Audiovisual** (ter, qui, sáb) | 6060 + 16427 · 6060 (+ 116637) |
| 20h | **Direito** | Igreja 6060 (+ Gestão 16426, ver 2.6) |

- O eixo é preferência: **fato forte de qualquer eixo passa na frente** (lei ou decisão que afeta todas as igrejas, divulgação do Censo, fato do ES). Registre no resumo "eixo trocado" e o motivo.
- Não repita o eixo da rodada anterior sem fato forte.
- **Teto: 1 matéria por rodada.** Duas só com fato extraordinário, e a segunda de outro eixo.
- Sem pauta com nota mínima (item 3) no eixo: (a) outro eixo com nota ≥ 8; (b) **guia prático com gancho** (item 3.1) no eixo da rodada; (c) "Sem fato novo nesta rodada".

## 2. O que cada eixo cobre e o que a Comunhão vem pautando

Base: 493 matérias publicadas em Igreja, Gestão, Liderança, Discipulado e Ministério de 27/02 a 26/10/2026, mais as seções Tecnologia, Filmes & Séries e Fé & Sociedade. Os temas recorrentes abaixo são **preferência de pauta e mapa do que a casa já tem**: busque o fato novo dentro deles e, antes de escrever, confira na duplicidade (item 6) se o ângulo já saiu.

### 2.1 Igreja (6060)

**Cobre:** vida das igrejas e denominações (cultos, encontros, congressos, aniversários, novos templos, posse e eleição de lideranças), ação social das igrejas, juventude e gerações, mulheres na igreja, acolhimento (pessoas com deficiência, autistas, dependentes), crescimento ou queda de frequência, datas do calendário cristão, mudanças institucionais (cisão, fusão, sucessão) a partir de nota oficial, desde que não envolvam acusação contra a igreja ou seus líderes.

**Recorrentes no período:** volta de jovens à igreja e aumento de frequência no Reino Unido e na Europa; igrejas em enchentes, presídios e alfabetização com a Bíblia; igrejas que acolhem autistas; Marcha para Jesus, congressos e cruzadas; aniversários de convenções (batistas, Assembleia de Deus); megatemplo no ES; posse de presidentes de convenções e entidades.

**Fontes:** sites e canais oficiais das denominações e convenções (CGADB, CONAMAD, Convenção Batista Brasileira, Convenção Batista Nacional, Igreja Presbiteriana do Brasil, Igreja Presbiteriana Independente, Igreja Metodista, IECLB, Igreja Adventista, Igreja do Evangelho Quadrangular, Igreja Cristã Maranata, Igreja Batista da Lagoinha, O Brasil Para Cristo e as demais), Aliança Cristã Evangélica Brasileira, Sociedade Bíblica do Brasil, Marcha para Jesus; no **ES**: Igreja Cristã Maranata, Igreja Evangélica Batista de Vitória, Primeira Igreja Batista de Vitória, Convenção Batista do ES, Assembleias de Deus no ES, Sínodo Espírito Santo da IECLB. Portal oficial de denominação (o da Universal, por exemplo) é **release da própria igreja**, não imprensa: atribua à igreja.

### 2.2 Gestão (16426 · Liderança 116624 · Ministério 44632)

**Lacuna a ocupar:** Gestão, Ministério e Liderança são as subcategorias da editoria com menos matérias (levantamento de out/2026). A rodada das 10h é a que mais alimenta essas três; antes de escolher, confira qual delas está há mais tempo sem matéria.

**Categoria:** Gestão 16426 para administração, finanças, governança, equipe, voluntariado, segurança, comunicação e mídia da igreja; Liderança 116624 quando o foco for formação e perfil de líder; Ministério 44632 quando for a vida, a saúde e a rotina do pastor.

**Cobre:** orçamento, prestação de contas e transparência; doações e dízimo como gestão (não como doutrina); governança e sucessão pastoral; equipe e voluntariado; segurança de templos e eventos; planejamento; comunicação e ministério de mídia; saúde emocional e esgotamento de pastores; formação de líderes.

**Recorrentes no período:** características de um líder eficaz; saúde emocional de pastores; falta de conselheiros; pastor acessível à congregação; cursos de capacitação pastoral (Sepal e outros); "10 passos para ter uma igreja viva"; organização do ministério de mídia.

**Fontes:** Sepal, Lifeway Research, Barna Group, ChurchLeaders, Christianity Today, Baptist Press, seminários e faculdades teológicas, departamentos de pastores das convenções; Receita Federal e Conselho Federal de Contabilidade quando o assunto for contábil ou fiscal.

### 2.3 Estatísticas (6060 + a categoria do assunto)

**Categoria:** Igreja 6060 e, quando o assunto for óbvio, a dele também (pesquisa sobre pastores: + Ministério 44632; sobre tecnologia: + 16427; sobre gestão: + 16426).

**Cobre:** pesquisas e dados sobre fé, igreja e evangélicos, no Brasil e no mundo.

**Recorrentes no período:** Censo 2022 (religião por cor ou raça, adolescentes sem religião); número de igrejas evangélicas abertas; saúde emocional de pastores; atuação feminina nas igrejas; medo dos evangélicos em relação à IA; frequência a cultos no exterior; engajamento recorde em apps bíblicos.

**Fontes primárias:** IBGE, Datafolha (só pesquisa de religião e comportamento), ISER, Lifeway Research, Barna Group, Pew Research Center, Gallup, Bible Society (Reino Unido), American Bible Society, YouVersion.

**Regras do eixo:**
- Número no título ou no lide, com quem fez a pesquisa.
- Box "Sobre a pesquisa" (item 8) sempre que a fonte informar amostra, período e margem.
- Compare com o dado anterior da mesma série quando a fonte trouxer.
- **Pesquisa eleitoral e intenção de voto ficam fora** (política partidária), mesmo quando o recorte é "evangélicos".

### 2.4 Tecnologia (6060 + Plugue-se › Tecnologia 16427)

**Cobre:** tecnologia a serviço da igreja ou que a coloca em risco: IA no ministério e na preparação de sermões, apps bíblicos, discipulado e culto on-line, segurança de dados e LGPD (vazamento de dados de fiéis), redes sociais e proteção de crianças e adolescentes, ferramentas de gestão e de doação on-line.

**Recorrentes no período:** riscos da IA para a igreja; IA mudando a preparação de sermões; 67% dos evangélicos temem o impacto da IA na fé; engajamento recorde no YouVersion e app da Bíblia em alta na África; ataque hacker que expôs dados de 939 mil fiéis; plataformas em lista de risco para crianças; discipular jovens no mundo virtual.

**Fontes:** YouVersion, Sociedade Bíblica do Brasil, Barna, Lifeway, ANPD (proteção de dados), comunicados oficiais das empresas, estudos acadêmicos. O Plugue-se › Tecnologia tem cerca de 75 matérias no período: confira a duplicidade também lá. O ângulo aqui é sempre **o que isso muda para a igreja**.

### 2.5 Audiovisual (6060 + Filmes & Séries 116637 quando for filme, série, animação ou documentário)

**Cobre:** produção audiovisual cristã com ângulo de igreja (estúdios e produções de fé, igrejas que produzem conteúdo), rádio e TV evangélicas (novas emissoras, outorgas, programação), transmissão de cultos (direitos de música e imagem, alcance, estrutura), comunicadores cristãos.

**Recorrentes no período:** nova emissora da Rádio Novo Tempo em Brasília; rádio que pediu desculpas por fala sobre cristãos; morte de referência da comunicação cristã; animação com valores cristãos de ex-produtor da Nickelodeon; The Chosen e seus derivados.

**Fronteira:** lançamento comercial de filme ou série sem ângulo de igreja é da equipe do Plugue-se (Filmes & Séries tem cerca de 117 matérias no período). Só entre se houver o que muda para a igreja: produção feita por igreja ou ministério, exibição em igrejas, dado de audiência oficial, decisão de regulação.

**Fontes:** comunicados oficiais de estúdios, distribuidoras e emissoras; Ancine; Ministério das Comunicações e Anatel (outorgas); ECAD (direito autoral em transmissões).

### 2.6 Direito (6060 + Gestão 16426 quando for obrigação legal da igreja como organização)

**Cobre:** liberdade religiosa e de culto; leis e projetos municipais, estaduais e federais que afetam igrejas; decisões dos tribunais superiores e das casas legislativas que mudam regras para as igrejas; imunidade tributária e obrigações fiscais; LGPD; relações de trabalho (pastores, funcionários, voluntários); direito autoral (ECAD); reconhecimento de patrimônio cultural; decisões internacionais sobre religião (escolas, liberdade religiosa).

**Recorrentes no período:** leis de Dia de Oração e de selo para igrejas que acolhem autistas; reconhecimento de montes de oração e da cultura evangélica como patrimônio; Dez Mandamentos em escolas nos EUA; liberdade religiosa em outros países.

**Fontes:** STF, STJ, tribunais de Justiça (TJES no ES), Câmara, Senado, Assembleia Legislativa do ES e câmaras municipais (site oficial e Diário Oficial), Receita Federal, ANAJURE, Instituto Brasileiro de Direito e Religião (IBDR); Agência Brasil para o noticiário do Judiciário.

**Regras do eixo:**
- No texto: número da lei, do projeto ou do processo, o órgão e a data.
- Diga a fase: proposto, aprovado em comissão, aprovado em plenário, sancionado, em vigor; decisão liminar ou de mérito; se cabe recurso.
- "O que muda para as igrejas" só com base no texto oficial. Sem orientação jurídica individual: quando houver passo prático, feche com "Na dúvida, procure um advogado ou contador."
- **Fora do eixo (pautas proibidas, 2.1 da padrão):** processo, ação, investigação, denúncia ou condenação que acusa igreja, denominação ou líder; ação, recomendação ou parecer de Ministério Público, Tribunal de Contas ou controladoria, inclusive sobre religião em escolas ou órgãos públicos. Entram leis, projetos e decisões que mudam regras para todas as igrejas.

## 3. Nota de pauta

Dê de 0 a 5 em cada critério e publique a maior soma, **mínimo 8**:

- **Relevância:** impacto concreto para igrejas, pastores ou fiéis, e fonte primária conferida.
- **Data:** 5 = últimas 24 h; 4 = até 72 h, agenda com prazo em até 30 dias ou pesquisa divulgada na semana; 2 = mais antigo, sem gancho novo.
- **Audiência da Comunhão:** 5 = Espírito Santo, ou fato que afeta todas as igrejas do país (lei federal, decisão do STF, Censo); 4 = grandes denominações brasileiras, dado nacional, tema recorrente da seção 2; 3 = internacional com ângulo brasileiro claro; 2 = internacional sem ligação com o Brasil.

Busque sempre o ângulo brasileiro ou capixaba (o que a pesquisa americana diz sobre as igrejas daqui, se há lei parecida no Brasil, como a denominação brasileira trata o tema).

### 3.1 Guia prático com gancho

Formato que a Comunhão já usa com bom resultado ("10 passos para ter uma igreja viva", "4 riscos da IA que exigem atenção da igreja"). Serve de pauta reserva em Gestão, Tecnologia, Direito e Audiovisual:

- Gancho real: pesquisa recente, data, lei nova ou fato da semana.
- Cada passo, dica ou risco vem de fonte publicada (pesquisa, organização, especialista em texto assinado, livro de editora cristã), com atribuição no texto. Nada de lista de opinião.
- Título com o número ("5 cuidados…", "4 passos…") e até 60 caracteres.

## 4. Onde procurar

1. **Parceiros comerciais da Comunhão primeiro:** Igreja Cristã Maranata, Convenção Batista, Mundo Cristão e Musile. Só entram com fato novo e pela mesma régua do item 3.
2. Feed internacional do NX Feed: `listar_materias` com `lista` = feed_internacional, desde a rodada anterior, todas as páginas (Christian Post, Christianity Today, Christian Today, Charisma, Relevant, Crosswalk, Christianity.com). É pista: abra a fonte original.
3. Feed nacional do NX Feed (agências contratadas), útil para Direito e Estatísticas (Judiciário, IBGE).
4. Sites das fontes do eixo (seção 2): páginas de notícias, imprensa e relatórios.
5. WebSearch com o mês e o ano correntes, por eixo (ex.: "lei igrejas outubro 2026", "pesquisa evangélicos 2026", "STF liberdade religiosa", "IA igreja pesquisa").

Abra a fonte com WebFetch antes de escrever; nunca redija a partir do trecho da busca. Fonte que não abre: troque de pauta. Os sites da IPB, da Convenção Batista Brasileira, da IECLB e dos Adventistas costumam não abrir por WebFetch: não contorne com curl ou Python; use comunicado da mesma igreja em outro canal oficial ou troque de pauta.

## 5. Crédito (mesma regra da rotina de Missões, decisão do Mário Fernando de 27/10/2026)

- **Veículos internacionais** (Christianity Today, The Christian Post, Religion News Service, Baptist Press, Christian Today, Christian Daily International, Evangelical Focus, Premier Christian News, ChurchLeaders, Charisma, Relevant, Crosswalk, CBN News e outros de fora do Brasil): em pauta internacional, mantenha o crédito. Atribua no corpo ("segundo o Religion News Service"), credite no rodapé e use a matéria do veículo como link externo quando ela for a base. Se a fonte primária que ele cita estiver acessível (pesquisa, decisão, comunicado), cite-a também e o rodapé leva as duas. Aspas e apuração própria do veículo internacional entram sempre com crédito explícito.
- **Veículos nacionais** (G1, A Gazeta, Folha, portais gospel brasileiros e outros do Brasil): só pista. Não cite, não linke, não escreva "segundo o portal X". A atribuição vai para a fonte primária; fato que só existe na reportagem de veículo nacional não entra.
- Lifeway Research, Barna, Pew, Gallup, Bible Society, IBGE, tribunais, casas legislativas, denominações e organizações são **fontes primárias**, não veículos.

## 6. Duplicidade (antes de escrever e de novo antes de publicar)

1. `listar_publicacoes` no portal 4, últimos 3 dias.
2. `listar_materias` com `portal` = 4, estado publicado, últimos 7 dias, na Igreja 6060 e na categoria do eixo (16426, 116624, 44632, 16427, 116637 ou 116629 Fé & Sociedade para Direito e Estatísticas).
3. Rascunhos e agendados dos últimos 7 dias **sem** filtro de portal (outras rotinas do Claude, como Missões e a Comunhão editorial, também publicam em Igreja e Missões e agendam para a hora cheia); `busca` pelo fato, pessoa, igreja ou lei nos últimos 30 dias, em todos os estados.
4. Acervo no NEIA (`search-content`, source "COMUNHAO.COM.BR") e WebSearch `site:comunhao.com.br <tema>`.

A equipe publica parte das matérias direto no WordPress, fora do NX Feed: o passo 4 é obrigatório. Se a casa já tem o fato, troque por outro assunto do mesmo eixo ou por um desdobramento realmente novo. Fato que também cabe em Missões (perseguição, evangelização) fica para a rotina de Missões.

## 7. Texto

- Autor "Redação"; chapéu de até 2 palavras em maiúsculas; título de até 60 caracteres com o fato e, se couber, o lugar; linha fina de até 20 palavras; lide de 25 a 70 palavras.
- Contexto com atribuição no corpo ("Segundo [cargo] [nome]…"); aspas curtas só quando a fonte primária ou o veículo internacional creditado as publicou, sempre com a origem; dado de referência quando houver.
- Intertítulos `<h4>`; 400 a 650 palavras; 1 link externo (`target="_blank" rel="noopener"`) para a fonte primária ou, em pauta internacional, para a matéria do veículo internacional creditado, nunca para veículo nacional; 1 link interno para matéria da Comunhão (achada no NEIA ou no NX Feed).
- Rodapé `<p><em>Com informações de [fonte primária e, em pauta internacional, o veículo internacional]</em></p>`.
- Datas como "nesta segunda-feira (27)". Nunca invente fala, dado, data ou cargo. Reescreva com estrutura e palavras próprias, mesmo quando a matéria-base é creditada: não traduza parágrafos nem siga a ordem ou o título dela.
- Tom informativo e interdenominacional, sem moralismo e sem ataque a denominações. Versículo só conferido no NEIA (`get-bible-passage`), em citação curta com a referência entre parênteses depois, ex.: "porém o maior destes é o amor" (1 Coríntios 13.13).
- **Fora:** as pautas proibidas da seção 2.1 da padrão (denúncia, aumento de tarifa e o que nasce de Ministério Público, Tribunal de Contas ou controladoria), política partidária, eleições e pesquisa eleitoral, ataque a denominações, conteúdo patrocinado, devocional (é da equipe), Igreja Católica, papa e Vaticano em qualquer papel, salvo a exceção de doença ou morte (ver o início desta skill), e os temas da rotina de Missões.

## 8. Box (no máximo um por matéria, depois do corpo e antes do rodapé)

- **"Sobre a pesquisa"** (Estatísticas, sempre que a fonte informar): quem fez, quando, quantas pessoas ou igrejas, margem de erro, link do relatório.
- **"Na prática, para a sua igreja"** (Gestão, Direito e Tecnologia, opcional): 3 a 5 pontos tirados da fonte oficial, nunca da cabeça. Em Direito e em assunto fiscal, feche com "Na dúvida, procure um advogado ou contador."
- **"Serviço"** (evento, curso, inscrição, estreia): O quê, Quando, Onde, Inscrições ou Onde assistir, Contato oficial; dados conferidos nesta rodada no site oficial. Nunca escreva chave PIX, conta bancária ou telefone de doação.

Modelo (troque o título e os itens):

```html
<div class="box-servico" style="background:#F4F6FA;border-left:4px solid #00427B;border-radius:6px;padding:16px 20px;margin:28px 0;"><h4 style="margin-top:0;">Sobre a pesquisa</h4><ul><li><strong>Quem fez:</strong> …</li><li><strong>Quando:</strong> …</li></ul></div>
```

## 9. Categorias e SEO

- `criar_materia` com `categorias` = `[{portal: "Comunhão", ids: [...]}]`, com os ids da tabela do item 1 e da seção 2.
- **Nunca:** Igreja e Missões 116618 sozinha, Destaques 44517, Panorama 1, nem as categorias de Missões (67595, 116628, 116627).
- Depois de criar, `prompt_do_nxfeed` (tipo seo) e ajuste. SEO pela `padrao-publicacao-next` (palavra-chave, título SEO, meta, slug, 5 a 10 tags, nota ≥ 85 com até duas correções).

## 10. Imagem destacada (a rotina escolhe e grava sozinha)

Ordem e regras da `padrao-publicacao-next`: `buscar_imagens` recomendadas (materia_id) → NX Fotos → editoriais → divulgação oficial com crédito. Por eixo:

- **Igreja e Gestão:** foto oficial da igreja ou do evento com crédito; sem foto do fato, foto real de acervo de culto ou igreja com "imagem ilustrativa".
- **Direito:** foto oficial do tribunal ou da casa legislativa (STF, Câmara, Senado, Ales, Agência Brasil) com crédito.
- **Estatísticas:** foto real de acervo do tema, com "imagem ilustrativa".
- **Tecnologia e Audiovisual:** material oficial de divulgação do app, estúdio ou emissora, com crédito.

Proibido: Reuters, AFP, AP, Getty, Shutterstock, iStock ou Freepik achados na web, Pinterest, Instagram de terceiros, foto de outro veículo (inclusive do veículo internacional creditado no texto), "Reprodução" sem dono, rosto de menor em contexto sensível. Imagem por IA só como último recurso, pelas regras 9.1 e 9.2 da padrão: autor "Krea AI / Comunhão", descrição = legenda-fato, alt terminando com "(imagem ilustrativa gerada por IA)"; proibido gerar pessoa real, templo ou símbolo de denominação específica, marca ou logotipo, ou recriar o fato.

## 11. Publicar

Refaça a duplicidade → `conferir_publicacao` (tipo publicar) → `publicar_no_wordpress` no portal Comunhão, autor "Redação". Se faltarem 3 minutos ou mais para a hora cheia da rodada, agende para ela (`quando` = "dd/mm/aaaa HH:00"); senão, "agora". A primeira chamada devolve o `codigo_confirmacao`: repita com os mesmos dados e o código. Se vier resultado incerto, confira com `listar_publicacoes` antes de repetir.

## 12. Resumo da rodada

`SendUserMessage`, curto, para celular, com o título **"Igreja Comunhão HHh · DD/MM"** e as seções da padrão (Publicadas, Imagens de IA para validar, Também na rodada, Pendências; seção vazia = "nenhuma"). Acrescente: eixo da rodada (e "eixo trocado: motivo", se for o caso), nota de pauta, nota SEO, imagem (real / ilustrativa / IA / sem imagem), box (qual ou não) e fontes usadas (primárias e veículo internacional creditado, se houver). Notifique ao terminar. Não envie e-mail.