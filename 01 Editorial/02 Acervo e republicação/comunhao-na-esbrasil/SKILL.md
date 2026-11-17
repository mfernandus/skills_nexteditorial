---
name: "comunhao-na-esbrasil"
description: "Rotina dos dias úteis que adapta para a ES Brasil matérias da Comunhão sobre família, casamento, filhos, saúde emocional ou dinheiro, sem linguagem religiosa, com aviso à Joviana pelo WhatsApp."
---

# Comunhão na ES Brasil — comportamento adaptado, 1 por dia às 7h

Objetivo: levar ao site da **ES Brasil** (portal 1) o melhor conteúdo de comportamento do site da Comunhão, **uma matéria por dia, no ar às 7h**, com a mesma estrutura do original, sem a camada religiosa e com a cara da **ES Brasil**. Temas: família, casamento e relacionamentos, filhos e educação, saúde emocional (ansiedade, estresse, luto), dinheiro e família, trabalho e gerações.

As matérias são **preparadas e liberadas às 18h do último dia útil antes da publicação** e vão para a Joviana pelo WhatsApp, para conferência. Se ninguém barrar no painel, saem no horário.

Responda sempre em português do Brasil. Execução automática: não faça perguntas. Na dúvida, tome a decisão mais conservadora e registre no resumo.

**Carregue antes a skill `padrao-publicacao-next`.** Ela traz as regras comuns: pautas proibidas (2.1, vale acima de tudo), matéria agendada (2.2), cuidados com o NX Feed (3), duplicidade (4), fontes (5), direitos autorais (6), texto (7), SEO (8), imagem (9), avisos (10) e economia do plano (11). Onde as duas divergirem, vale esta skill nestes pontos (decisões do Mário Fernando, 05/11/2026):

- **O texto é da casa** (copyright da Next Editorial): a adaptação parte do texto da Comunhão e mantém a estrutura dele. Não vale aqui a regra de reescrever com estrutura própria (padrão 6), que é para texto de outros veículos.
- **Título original mantido**, com as exceções da seção 7.
- **Rodapé de origem** (seção 7) no lugar do "Com informações de".
- **Calendário próprio:** preparada no último dia útil anterior, no ar às 7h (seção 10).
- **Aviso prévio à Joviana pelo WhatsApp** (seção 11). Silêncio vale como aprovação; para barrar, ela cancela o agendamento no NX Feed.
- **Destaques no fim de semana e feriado:** a matéria que vai ao ar em sábado, domingo ou feriado entra já com Destaques (seção 10.3). Em dia útil, nunca.
- **Matéria inteira, nunca dividida em partes.**

## 1. Fontes no NEIA

Carregue as ferramentas `mcp__NEIA_IA__*` com ToolSearch.

| Fonte | Id | Uso |
|---|---|---|
| comunhao.com.br (wordpress_portal) | 019ca1ae-c3a6-718c-b1f2-e577c04f3ed8 | Fonte principal: post com data exata, `wp_post_id`, `wp_url`, `wp_author` |
| Revista Comunhão (magazine) | 019ca1b0-1295-72f0-baaf-31867a70431e | Só quando o tema não existe no site ou o texto da revista é claramente melhor, e os dados se atualizam |

- `search-content` sempre com `source` (nunca sem escopo), `page_size` até 50, `content_type` "article" ou "interview". `get-article-content` traz o texto completo e os metadados.
- **Janela:** só posts com **pelo menos 30 dias** no ar na Comunhão, para não disputar o Google com a própria Comunhão. Não há limite para trás, desde que os dados se confirmem hoje (seção 6).
- **Republicação:** o mesmo texto aparece às vezes duas vezes no site (ex.: "Como lidar com crises e conflitos no casamento", post 261620, de 05/09/2024, republicado como post 345000 em 16/03/2026). O original é o **mais antigo**: use a data e a URL dele.
- **Autoria:** vale a assinatura no corpo do texto ("Por Fulano" ou o nome em negrito no início) sobre o `wp_author`. Se divergirem, registre em Pendências. Sem assinatura: "Redação da Comunhão".

## 2. Tema de cada dia de publicação

O tema vale pelo **dia em que a matéria vai ao ar**, não pelo dia da rodada (no feriado, vale o dia da semana dele).

| Dia no ar | Tema | Buscas de exemplo |
|---|---|---|
| Segunda | Saúde emocional | ansiedade, estresse, esgotamento, burnout, sono, luto, solidão, autoestima |
| Terça | Casamento e relacionamentos | conflitos no casamento, comunicação do casal, rotina a dois, amizade, recomeço |
| Quarta | Filhos e educação | telas, adolescência, limites, escola, regulação emocional, ansiedade infantil |
| Quinta | Dinheiro e família | dívidas, ansiedade financeira, orçamento doméstico, mesada, consumo, finanças do casal |
| Sexta | Trabalho e comportamento | carreira, rotina, redes sociais, comparação, propósito, descanso |
| Sábado | Gerações | idosos, avós, cuidadores, pais e filhos adultos, convivência familiar |
| Domingo | Livre | a maior nota entre todos os temas |

Para cada matéria, faça de 3 a 6 buscas no site com termos do tema e separe de 3 a 5 candidatas antes de ler a fundo: as regras da seção 3 costumam derrubar uma ou duas. Na rodada com várias matérias (sexta-feira, véspera de feriado), uma candidata usada para um dia sai da lista dos outros.

### Nota de escolha (0 a 5 cada, mínimo 13 de 20)

- **Encaixe laico:** o argumento se sustenta inteiro sem a fé (5); a tese é espiritual (0). **Abaixo de 3, a candidata sai.**
- **Fontes técnicas:** psicólogo, médico, pesquisa, dado oficial (5); só falas de líderes religiosos (0, sai).
- **Interesse do leitor da ES Brasil** (público AB, gestores, pais, decisores): liga-se a trabalho, dinheiro, saúde ou educação, ou tem gancho de calendário próximo da data de publicação (Janeiro Branco, volta às aulas, Dia das Mães, Dia dos Namorados, Dia dos Pais, Setembro Amarelo, fim de ano, férias) (5).
- **Qualidade e dados conferíveis:** texto completo, bem apurado, números com fonte que ainda abre (5).

Empate: o gancho de calendário, depois o tema menos usado pela rotina nos últimos 14 dias.

## 3. Fora da escolha

- Pautas proibidas do padrão (2.1). Política partidária e eleitoral.
- **Tese religiosa:** vida cristã, oração, Bíblia, igreja, missões, ministério, louvor, devocional, estudo bíblico, teologia, testemunho de conversão, evangelização.
- **Matéria que se apoia em fala de pastor**, bispo, padre, apóstolo, missionário ou outro líder religioso. Sem essas falas ela fica sem fonte. Ex.: "A solidão dentro do casamento: quando o barulho some" (fev/2026) só tinha falas de pastores e sai.
- **Temas em que a Comunhão traz posição confessional:** aborto, sexualidade, identidade de gênero, ideologia, divórcio como pecado, casamento com quem não tem fé, castidade, pornografia sob enfoque moral.
- Resenha ou divulgação de livro de editora cristã, evento de igreja, agenda, nota curta (menos de 400 palavras), conteúdo de marca, notícia factual com prazo.
- Dado central que não se confirma na fonte primária e não tem substituto (seção 6).
- Original de mais de 2.000 palavras que não dá para condensar sem perder argumento.
- Matéria já adaptada por esta rotina (seção 4).
- Se, depois da limpeza da seção 5, cair **mais de um terço do texto**, a candidata sai: volte à escolha.

## 4. Duplicidade

As matérias da rotina se reconhecem pela tag "Revista Comunhão" e pela frase "Conteúdo adaptado da Revista Comunhão" no rodapé.

Antes de escrever e de novo antes de agendar:

1. **Rotina:** `listar_materias` com `portal` 1, `busca` pelo título original e por uma palavra forte dele, todos os estados, últimos 365 dias, formato compacto; rascunhos sem filtro de portal. A mesma matéria da Comunhão nunca é adaptada duas vezes.
2. **ES Brasil no tema:** `listar_materias` com `portal` 1 e `busca` pela palavra-chave do tema, últimos 60 dias (pega também o acervo da ES Brasil, a rodada de Estilo e o turno noturno), e WebSearch `site:esbrasil.com.br <tema>`. Mesmo assunto com o mesmo enfoque nos últimos 60 dias: troque de candidata.
3. Matéria agendada da equipe sobre o tema conta como duplicada (padrão 2.2).

## 5. Adaptação: tirar o "evangeliquês" sem mudar a estrutura

Princípio: é a mesma matéria, na mesma ordem, sem a camada religiosa e na voz da **ES Brasil**.

### 5.1 Sai sempre

- **Citações e referências bíblicas**, no corpo, nas listas e nos boxes (ex.: "Orientações bíblicas para momentos de ansiedade" sai inteira).
- **Vocabulário religioso:** Deus, Jesus, Senhor, Espírito Santo, oração, culto, igreja, fé, "irmãos", bênção, "propósito de Deus", aliança, discipulado, testemunho, ministério, unção, "liberar perdão", edificar, "lar cristão", "família cristã", "pais cristãos", "casal cristão".
- **Pessoas e instituições religiosas:** nome e título de pastor, bispo, padre, apóstolo, missionário e líder religioso, com as falas deles; nomes de igrejas, denominações, ministérios e movimentos (ex.: "a psicóloga, que participa do movimento Encontro de Casais com Cristo" → "a psicóloga").
- **Resíduos do site:** blocos "Leia mais", links internos para comunhao.com.br, "Continua após a publicidade", legendas de foto soltas no texto.

### 5.2 Como substituir

- A ideia universal por trás de um trecho religioso fica, em linguagem laica, **só quando o próprio original a sustenta**. Exemplos: "disciplina e admoestação do Senhor" → "limites com explicação"; "culto familiar" → "momentos em família"; "conselheiro cristão ou terapeuta de casais" → "terapeuta de casais"; "não se ponha o sol sobre a vossa ira" → "não ir dormir sem antes pedir desculpas pelas explosões do dia"; "o discipulado acontece pela imitação" → "a educação também acontece pela imitação".
- Parágrafo que só existia para o versículo ou para a fala do pastor: sai.
- **Nunca** ponha entre aspas, sem dono, frase que era de pastor, nem a atribua a outra pessoa.
- Pessoa com dupla função ("psicóloga e pastora"): fica só a função técnica, e só se ela não for identificada por igreja ou ministério no texto; na dúvida, a fala sai.

### 5.3 Estrutura mantida

- Mesma ordem de blocos e os mesmos intertítulos. Só se reescreve o intertítulo com termo religioso ("O desafio para os pais cristãos" → "O desafio para os pais"; "7 princípios bíblicos para..." → "7 cuidados com...").
- Listas mantêm a quantidade de itens: o item puramente religioso vira o equivalente laico que o texto sustenta ("Coloque a fé no cotidiano" → "Faça do dia a dia a principal escola") ou sai, se não houver equivalente.
- Não acrescente seção, box ou lista que o original não tem. Tamanho final entre 70% e 110% do original.
- Entrevista continua pergunta e resposta.

### 5.4 Cara de ES Brasil

- Tom sóbrio e informativo para o leitor AB capixaba: dado com fonte e ano, frases diretas, sem tom de aconselhamento pastoral, sem exclamações e sem clichês ("insights valiosos", "mal do século").
- Termo técnico explicado numa oração ("problemas internalizantes" → "os que se voltam para dentro, como ansiedade e retraimento").
- Datas completas ("28 de setembro de 2026"); "hoje" e "este ano" viram datas.
- Corrija erros de digitação e de grafia de nomes (ex.: "Eliasnalva" → "Elisnalva").
- Opcional: um dado capixaba, só com fonte oficial aberta e em uma frase, sem mudar a estrutura.
- Ao citar a revista, **ES Brasil** em negrito.

## 6. Dados e fontes

- Todo número que sustenta o texto é conferido na **fonte primária** aberta com WebFetch (padrão 5). Imprensa não serve de fonte.
- **Dado errado ou misturado:** corrija no texto, com fonte e ano. Ex.: "61% dos brasileiros sofrem de ansiedade financeira" (maio/2026) misturava uma pesquisa de 2022, só com inadimplentes, com a da Serasa de agosto de 2025 (84% já tiveram a saúde mental afetada). O texto passou a usar os dados de 2025.
- **Dado superado** por edição mais nova da mesma pesquisa: atualize. **Dado não confirmado:** sai do texto.
- Estudo científico: confira revista, data e autores na página do estudo ou de instituição científica; mantenha as ressalvas do original (associação não é causa).
- Um link externo, para a fonte principal. Saúde: sem dose nem prescrição.

## 7. Formato

- **Título:** o original, até 60 caracteres. Muda só quando tem termo religioso, dado errado ou passa de 60. Registre a mudança no resumo.
- **Linha fina:** a original (uma frase); sem ela, uma frase de até 25 palavras.
- **Chapéu:** o tema, em maiúsculas, até duas palavras: COMPORTAMENTO, FAMÍLIA, RELACIONAMENTOS, FILHOS, EDUCAÇÃO, SAÚDE MENTAL, FINANÇAS PESSOAIS, CARREIRA, GERAÇÕES.
- **Abertura:** o primeiro parágrafo retoma o título e traz a palavra-chave.
- **Intertítulos** em `<h4>`, os do original. **Autor no NX Feed:** "Redação".
- **Rodapé**, sempre o último parágrafo, com link para o post original:

```html
<p><em>Conteúdo adaptado da <a href="[URL do post original]" target="_blank" rel="noopener">Revista Comunhão</a>, publicação do Grupo Next Editorial, publicado originalmente em [dia] de [mês] de [ano], de autoria de [nome].</em></p>
```

  Revista impressa: "...publicado originalmente na edição nº [X], em [mês] de [ano], de autoria de [nome]." Sem assinatura: "de autoria da Redação da Comunhão".

## 8. Categoria e tags (portal 1)

- **Preferida: Vida Capixaba › Comportamento.** Em cada rodada, rode `listar_categorias_wordpress` (portal 1, busca "Comportamento") e use o id que vier.
- Enquanto ela não existir, use: Saúde emocional e Dinheiro e família → Vida Capixaba › Cotidiano › Saúde (119); Filhos e educação → Vida Capixaba › Cotidiano › Educação (1722); Casamento, Trabalho e Gerações → Vida Capixaba › Estilo › Em Casa (14737). Registre no resumo que a categoria foi provisória.
- **Destaques 11966** só na matéria que vai ao ar em sábado, domingo ou feriado (seção 10.3), junto com a subcategoria. Nunca Panorama, Últimas Notícias, Colunas, Especial, Conteúdo de Marca, Display AD, Institucional ou Sem categoria.
- **Tags (5 a 10):** sempre "Revista Comunhão", mais a palavra-chave e o tema.

## 9. SEO e imagem

- SEO pelo padrão (seção 8), com `prompt_do_nxfeed` (tipo seo) depois de `criar_materia`. Nota SEO ≥ 85.
- Imagem pelo padrão (seção 9), escolhida e gravada pela rotina. Ordem: `buscar_imagens` recomendadas → NX Fotos → imagem destacada do post original **só** com fonte e autor conhecidos e direito de uso claro → divulgação oficial com crédito → IA (Krea, autor "Krea AI / ES Brasil").
- O post original usa muitas vezes Freepik, Shutterstock ou foto sem crédito: proibido (ex.: o post de casamento de 2024 usa imagem do Freepik).
- Sem símbolo religioso na imagem: cruz, Bíblia, templo, mãos em oração, culto.

## 10. Calendário: preparada no dia útil anterior, no ar às 7h

Decisão do Mário Fernando (05/11/2026): a matéria vai ao ar **às 7h** e é **liberada às 18h do dia anterior** quando esse dia é útil. As de sábado, domingo, feriado e do primeiro dia útil depois deles são liberadas no **último dia útil anterior**.

### 10.1 Dia útil

Dia útil = segunda a sexta, menos os feriados abaixo (nacionais, Carnaval, Sexta-feira Santa, Corpus Christi, Nossa Senhora da Penha, que é feriado estadual pela Lei 11.010/2019, e 8 de setembro em Vitória).

| Ano | Feriados em dia de semana |
|---|---|
| 2026 | 20/11 (sex), 25/12 (sex) |
| 2027 | 01/01 (sex), 08/02 e 09/02 (Carnaval), 26/03 (Sexta-feira Santa), 05/04 (N. Sra. da Penha), 21/04 (qua), 27/05 (Corpus Christi), 07/09 (ter), 08/09 (qua), 12/10 (ter), 02/11 (ter), 15/11 (seg) |

A partir de 2028, monte a lista do ano com fonte oficial (Páscoa + 8 dias = Penha; Páscoa − 48 e − 47 = Carnaval; Páscoa − 2 = Sexta-feira Santa; Páscoa + 60 = Corpus Christi) e registre em Pendências que a lista precisa entrar na skill.

### 10.2 O que cada rodada prepara

A tarefa agendada começa às **16h30**, de segunda a sexta. Hora certa: `TZ=America/Sao_Paulo date`.

1. **Hoje não é dia útil** (feriado): encerre sem fazer nada, com o resumo "Sem rodada: feriado (as matérias foram preparadas no dia útil anterior)", sem notificação.
2. **Hoje é dia útil:** prepare uma matéria para **cada data de amanhã até o próximo dia útil, inclusive**. Segunda a quinta comuns: só amanhã. Sexta-feira: sábado, domingo e segunda (e a terça também, se a segunda for feriado). Véspera de feriado: o feriado e o dia útil seguinte.
3. Para cada data, `listar_agendamentos` do portal 1: se já houver matéria desta rotina às 7h daquela data, pule a data (não agende segunda).
4. Prepare as matérias em ordem de data (seções 2 a 9) e agende cada uma para **07h00 da sua data** (seção 10.3). Depois, a seção 11.

### 10.3 Agendamento

1. Refaça a duplicidade (seção 4).
2. `criar_materia` (autor "Redação", portal 1) → `prompt_do_nxfeed` (seo) → `editar_materia` com o que faltar (`trocar_trecho` e a `versao` mais recente) → `definir_imagem_destacada`.
3. `conferir_publicacao` (tipo agendar, portal 1) → `publicar_no_wordpress` com `portais` ["1"], `autores` ["Redação"], `quando` "DD/MM/AAAA 07:00" (a data da matéria) e o `codigo_confirmacao`. Uma chamada de cada vez; erro 429: espere e repita.
4. Confira em `listar_agendamentos` (ou `ver_materia`) que ficou às 7h da data certa, no portal 1, com a categoria certa (e com Destaques, se for sábado, domingo ou feriado). Guarde o id da matéria, o `link_painel` e o link de prévia que o NX Feed devolver (sem ele: `https://esbrasil.com.br/?p=<id do post>&preview=true`).
5. **Destaques (decisão de 05/11/2026):** a matéria que vai ao ar em sábado, domingo ou feriado é gravada no passo 2 com a subcategoria **e Destaques 11966**; como vai para a capa, a imagem destacada é obrigatória. A saída do Destaques fica com a rotina de Destaques (destaques-next), pelas regras de fim de semana e feriado: esta skill não tira nada do Destaques. Matéria de dia útil vai sem Destaques.
6. Sem Instagram (padrão 2.2 e 3). O post automático do X pelo NX Feed pode sair.

## 11. Aviso à Joviana pelo WhatsApp (decisão de 05/11/2026)

Cada matéria agendada vai para a Joviana pelo WhatsApp **às 18h** do dia da rodada, para conferência. **Silêncio vale como aprovação:** a matéria sai no horário. Para barrar ou corrigir, a Joviana (ou o Mário) cancela o agendamento ou edita a matéria no NX Feed. A rotina não lê as respostas do WhatsApp (elas caem no app DoctorChat), então resposta pelo WhatsApp não muda nada.

- **Destinatária:** Joviana, +55 27 99705-9413 (`to` = "5527997059413"). O Mário não recebe o WhatsApp por enquanto: acompanha pelo resumo da rodada. Não mande para mais ninguém.
- **Hora:** às 18h. Se as matérias ficarem prontas antes, espere até 18h00 (sleep em blocos de até 9 minutos). Se ficarem prontas depois, mande assim que estiverem agendadas.
- **Credenciais:** leia a memória `/areas/whatsapp-api-next.md` com `mcp__memory__memory_read` e pegue o Access Token e o Phone Number ID (número +55 27 98854-7222). **O token é senha:** use só numa variável de ambiente no comando, nunca o escreva em arquivo, resumo, matéria ou repositório.
- **Envio:** uma mensagem por matéria, em ordem de data, com o template aprovado `esbrasil_conferencia_materia` (pt_BR, categoria UTILITY, id 1181752567760232, aprovado em 16/11/2026). O texto que a Joviana recebe é: "Olá, Joviana! Uma matéria adaptada da Revista Comunhão foi agendada no site da *ES Brasil* para sua conferência." seguido de título, no ar, prévia e painel. Ele substitui o antigo `comunhao_esbrasil_aprovacao` (id 4407084732887835), que falava em "a rotina Comunhão na ES Brasil", um nome interno que a Joviana não reconhecia (16/11/2026). Não use mais o template antigo, salvo no caso de falha descrito abaixo. Os 4 parâmetros do corpo, em ordem: (1) título da matéria; (2) dia e hora no ar, ex.: "sábado, 07/11, às 7h"; (3) link de prévia; (4) link do painel. Parâmetro sem quebra de linha e sem mais de 4 espaços seguidos.
- **Uma chamada só por matéria:** não mande texto livre, não mande segunda mensagem e não reenvie quando a primeira resposta já trouxer `messages[0].id`.

```bash
curl -sS -X POST "https://graph.facebook.com/v21.0/$PHONE_ID/messages" \
  -H "Authorization: Bearer $WA_TOKEN" -H "Content-Type: application/json" \
  -d '{"messaging_product":"whatsapp","to":"5527997059413","type":"template","template":{"name":"esbrasil_conferencia_materia","language":{"code":"pt_BR"},"components":[{"type":"body","parameters":[{"type":"text","text":"<título>"},{"type":"text","text":"<dia e hora>"},{"type":"text","text":"<prévia>"},{"type":"text","text":"<painel>"}]}]}}'
```

- **Deu certo** quando a resposta traz `messages[0].id`: guarde o id para o resumo.
- **Falhou** (template pausado ou fora do ar, token vencido, erro da Meta): confira o status com GET `https://graph.facebook.com/v21.0/1736326550425075/message_templates?name=esbrasil_conferencia_materia`. Se ele não estiver APPROVED, mande **uma** vez com o template antigo `comunhao_esbrasil_aprovacao` (mesmos 4 parâmetros) e registre no resumo que o aviso saiu no modelo antigo. Se ele estiver APPROVED, tente **uma** vez mais com ele. Se falhar de novo, a matéria **continua agendada**; registre em Pendências "Joviana não recebeu o aviso" com o erro (sem o token) e mande a notificação do app.
- O WhatsApp desta rotina serve só para este aviso: nunca para outra mensagem, outro conteúdo ou outra pessoa.
- Data que ficou sem matéria não gera WhatsApp: fica só no resumo.

## 12. Resumo e notificação

**Não envie e-mail.** Resumo curto, legível no celular, com `SendUserMessage`, título "Comunhão na ES Brasil · liberadas DD/MM", nestas seções:

- **Agendadas:** por matéria, data e hora no ar, título, link de prévia, link do painel, chapéu, categoria (e se é provisória), Destaques (sim ou não), original (título com link, data, autor), nota de escolha, nota SEO, imagem (real ou IA).
- **WhatsApp à Joviana:** por matéria, hora do envio e id da mensagem, ou o erro.
- **O que saiu:** versículos, nomes de pastores e igrejas, termos religiosos, parágrafos cortados, tamanho final em % do original.
- **Dados:** conferidos, corrigidos (antigo → novo, com fonte) e retirados.
- **Imagens de IA para validar**, quando houver.
- **Pendências:** aviso que falhou, autoria em dúvida, título alterado, categoria provisória, SEO abaixo de 85, imagem abaixo de 1.200 px, lista de feriados a atualizar.
- **Descartadas no caminho:** cada candidata que caiu e o motivo, em uma linha.

Notificação do app Claude ao terminar. Data sem matéria (nenhuma candidata com nota 13 ou mais, ou todas duplicadas): registre a data e o motivo no resumo, sem agendar nada para ela.