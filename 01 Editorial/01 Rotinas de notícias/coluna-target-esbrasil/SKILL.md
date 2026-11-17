---
name: "coluna-target-esbrasil"
description: "Coluna Target da ES Brasil: três notas por rodada (cliente da Next, mercado capixaba, nacional ou internacional) sobre publicidade e comunicação, publicadas direto, seg, qua e sex às 11h."
---

# Coluna Target — ES Brasil

Alimenta a coluna **Target** da **ES Brasil** com notas sobre o mercado publicitário, a comunicação corporativa, a mídia exterior e tudo que movimenta a comunicação, no Espírito Santo, no Brasil e no mundo. Cada nota é um post separado no site, na categoria Colunas › Target.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, pautas proibidas (2.1), matéria agendada (2.2), feed só manual (2.3), cuidados do NX Feed, duplicidade, fontes, direitos autorais, caixa alta, SEO, imagem, avisos e economia do plano. Aqui fica só o que é da Target. Onde esta skill diz algo diferente, vale esta skill, salvo nas seções 2.1, 2.2 e 2.3 do padrão. Sem a skill-base, não publique nada.

## 1. Quando roda e o que cobre

- Segunda, quarta e sexta; as notas entram no ar a partir das 11h (horário de Brasília).
- Cada rodada cobre o que aconteceu desde a rodada anterior. A de segunda pega também o fim de semana.
- Publicação direta (decisão do Mário Fernando, 11/11/2026). A aprovação nota a nota pelo WhatsApp fica suspensa: nada vai ao WhatsApp nesta rotina.

## 2. Composição da rodada

Três notas, uma de cada tipo:

1. **Cliente da Next:** movimentação de comunicação, marketing, marca, campanha ou evento de um cliente principal da Next (ex.: Galvan, Parque do China, Governo do Estado). A lista vem da carteira comercial do Nextor (`get_comercial_carteira`; para conferir um nome, `search_clients`). **Agência de publicidade não conta como cliente**, mesmo estando no Nextor: entra como nota de mercado.
2. **Mercado capixaba:** agências, profissionais, contas novas, mídia exterior, gráficas, comunicação corporativa, sindicatos, prêmios locais e licitações de comunicação no ES.
3. **Nacional ou internacional:** grandes lançamentos, rebrandings, contas, fusões, prêmios e tendências.

O Espírito Santo fica com dois terços da coluna. Vaga sem fato que valha nota fica vazia e vai para o resumo com o motivo: não encha com pauta fraca.

## 3. Fontes fixas

**Mercado local:** Sinapro-ES; Sindigraf-ES; Abracom e Aberje com recorte capixaba; sites, blogs e redes públicas das principais agências e dos principais publicitários capixabas; empresas de mídia exterior que atuam no ES; áreas de comunicação das grandes empresas capixabas e do Governo do Estado; portais de notícias do ES (só como pista).

**Licitações de comunicação e publicidade:** Diário Oficial do ES e portal de compras do Governo do Estado; diários oficiais e portais de licitação das prefeituras da Grande Vitória e das maiores cidades do interior; Assembleia Legislativa e estatais com atuação no ES; PNCP com filtro para o ES.

**Nacional:** Meio & Mensagem, Propmark, Adnews, Valor Econômico, Exame e B9; Cenp, Abap e Kantar Ibope Media.

**Internacional:** Ad Age, Adweek, Campaign, The Drum e Contagious.

**Prêmios:** Cannes Lions, Effie, Clio, One Show, D&AD, Colunistas, Prêmio Abracom e Prêmio Aberje.

**Redes sociais:** a rotina só lê o que está público e indexado (busca e páginas abertas). Não raspa Instagram nem LinkedIn e não usa navegador para varrer perfis.

**Crédito.** Nota nacional ou internacional pode levar no rodapé "Com informações de" a imprensa especializada que a sustenta (Meio & Mensagem, Propmark, Adnews, B9, Valor, Ad Age, Adweek, Campaign, The Drum), além da fonte oficial. Nota local credita a fonte primária (agência, empresa, sindicato, órgão); veículo capixaba de fora da casa é só pista e nunca recebe crédito nem link.

## 4. Cuidados de pauta

- As pautas proibidas do padrão valem integralmente. Na Target, atenção a: licitação suspensa, cautelar ou questionada por Tribunal de Contas, Ministério Público ou controladoria (origem em órgão de controle: fora); denúncia contra agência, profissional ou anunciante (fora); disputa judicial entre agências (fora).
- Duplicidade: além da trava do padrão, confira as notas da própria Target dos últimos 30 dias (`listar_materias`, portal 1, categoria 30, formato compacto) e não repita assunto sem fato novo.

## 5. Tom

- Nacional e internacional: opinativo e com uma pitada de sarcasmo, sem ser crítico demais.
- Mercado capixaba e clientes da Next: tom de bastidor e reconhecimento. Nada agressivo e nada que permita dupla interpretação por um parceiro da casa. Na dúvida, tire a piada.
- Os fatos sempre vêm de fonte conferida; a graça fica na leitura, nunca no dado.

## 6. Formato da nota

- Título com sacada, até 60 caracteres; linha fina de uma frase, informativa (ex.: título "Caixa troca de roupa, mas não de guarda-roupa"; linha fina "Banco apresenta a primeira nova marca em quase 30 anos, preserva o X azul e laranja e mira jovens").
- Chapéu curto em caixa alta e baixa, pelo assunto (ex.: "Identidade visual", "Licitação publicitária", "Publicidade capixaba").
- Texto de quatro a seis frases, em dois ou três parágrafos curtos, sem intertítulo. Um link externo para a fonte. Rodapé `<p><em>Com informações de [fonte]</em></p>`.
- Autor "Redação". Categoria só Colunas › Target (portal 1, id 30); nunca Destaques.
- SEO pelo padrão, com uma diferença: nota curta não chega fácil a 85. Ajuste palavra-chave, título SEO e meta description uma vez; mire 80 ou mais e não estique o texto para subir a nota.

## 7. Imagem

A foto tem que mostrar exatamente o assunto da nota.

1. **Busca:** comece pelo NX Fotos. Só sem foto certa lá passe para as recomendadas do NX Feed, o banco editorial, a divulgação oficial com crédito e, por último, imagem por IA (padrão, 9.1 e 9.2).
2. **Conferência visual:** olhe a foto antes de gravar. Mostra o assunto certo, é atual e tem o local correto? Em nota de rebranding, entra a marca nova, nunca a antiga. A Secom-ES fica no Palácio da Fonte Grande, não no Palácio Anchieta (o NX Fotos ainda não tem foto do Fonte Grande: registre a lacuna e use outra imagem certa do assunto).
3. **Sem repetição:** não use foto que já saiu em matéria recente; prefira outro ângulo ou uma foto mais nova.
4. **Tratamento:** pelo padrão, seção 9.3.

## 8. Publicação

1. Apure e escreva as três notas antes de criar qualquer uma no NX Feed.
2. Crie cada nota (`criar_materia`), grave a imagem e ajuste o SEO.
3. Agende uma por vez no portal 1 (`conferir_publicacao` e `publicar_no_wordpress`, autor Redação, categoria 30): cliente da Next às 11h00, mercado capixaba às 11h15 e nacional ou internacional às 11h30. Se a hora de uma nota já passou ou faltam menos de 3 minutos, ela sai "agora" e as seguintes mantêm o intervalo de 15 minutos. Vaga vazia não desloca as outras.

## 9. Stories

No máximo um story por rodada, no @revistaesbrasil (conta 7). Feed, nunca (padrão, 2.3).

1. Prioridade: a nota de cliente da Next; depois, a do mercado capixaba. Se a nota de cliente não tiver foto boa para story (resolução baixa ou origem delicada), o story vai para a de mercado. Nota nacional ou internacional não leva story.
2. O painel do NX Feed cria sozinho um story de cada nota agendada. Logo depois de agendar as três, `listar_posts_instagram` (conta 7, tipo story, filtro "agendados" e depois "aprovados") e fique só com os itens cujo `materia_id` é de uma nota desta rodada; se não achar, espere 2 minutos e procure de novo, até 3 vezes.
3. Mantenha o story automático da nota escolhida e cancele (`cancelar_agendamento_instagram`) o das outras. Nunca mexa em story de outra matéria.
4. Se o Studio mostrar a cota diária de stories do canal cheia, cancele também o da nota escolhida e registre "story fora: cota do dia cheia".
5. Story automático que já saiu não se desfaz: registre em Pendências.

## 10. Resumo

Avisos do padrão (seção 10). Título: **"Target · DD/MM"**. Parte própria, por nota: tipo (cliente, mercado capixaba, nacional ou internacional), título, link no ar ou horário agendado, chapéu, fonte principal, nota SEO, imagem (real, ilustrativa, IA) e a marca **Cliente da Next** quando a nota citar empresa da carteira do Nextor (para revisão com mais atenção). Depois: story (qual nota ficou e quais foram cancelados), vagas vazias com o motivo e pendências. Notificação do app sempre que publicar ou houver problema.