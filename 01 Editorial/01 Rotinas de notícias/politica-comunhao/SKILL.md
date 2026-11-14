---
name: "politica-comunhao"
description: "Série Fé e Política da Comunhão: 2 matérias por dia, de segunda a sábado (11h e 17h), valorizando mandatos de políticos evangélicos de todos os partidos. Carregar depois da padrao-publicacao-next."
---

# Fé e Política — Comunhão (segunda a sábado, 11h e 17h)

Rotina da série **Fé e Política** do portal Comunhão (comunhao.com.br; no NX Feed, portal **4**). Em cada rodada ela produz e **publica 1 matéria** que valoriza o trabalho de um político evangélico brasileiro na defesa de valores cristãos durante o mandato.

- Carregue antes a `padrao-publicacao-next`: publicação direta, NX Feed, duplicidade, direitos, SEO, imagem e avisos vêm de lá. Aqui fica só o que é da série. Onde as duas divergirem, vale esta skill naquele ponto, **salvo as seções 2.1 (pautas proibidas) e 2.2 (matéria agendada) da padrão, que valem acima desta skill**.
- **Exceções declaradas à padrão** (decisões do Mário Fernando, 05/11/2026): (1) a regra "Política: tom neutro, mesmo espaço aos lados" da seção 7 não vale para esta série: aqui a linha editorial é positiva, e a matéria mostra o que o político fez de bom no mandato; (2) o rodapé "Com informações de..." não entra quando a base é agência ou Casa legislativa (item 8). O resto das seções 5 e 7 continua valendo.
- Irmãs: `igreja-comunhao` e `missoes-comunhao`. Lei ou decisão que muda regra para todas as igrejas, sem protagonista político, é da Igreja (eixo Direito); perseguição e missões são de Missões.
- Execução agendada não tem ninguém acompanhando: não faça perguntas. Não envie e-mail.

## 1. A linha da série

1. **Falar bem, com fatos.** Cada matéria valoriza um mandato a partir de um fato verificável: projeto apresentado, aprovado ou relatado; lei sancionada; ação ou programa com resultado oficial; sessão solene, homenagem, frente parlamentar; trajetória pública. O elogio está no fato, não no adjetivo: nada de "o melhor", "o maior defensor", "histórico", "incansável".
2. **Não falar mal de ninguém.** Sem crítica, ironia ou comparação com adversários, partidos, governos, tribunais, imprensa ou outras igrejas. Não cite opositores nem quem votou contra. Se o fato só existe como reação contra alguém (pedido de impeachment, ataque a ministro, briga com governo), não é pauta.
3. **De todos os partidos.** Evangélico de qualquer partido entra, e o equilíbrio do item 5 é obrigatório: a série é da fé, não de um lado.
4. **Valores cristãos, em sentido amplo:** vida e dignidade humana; família, infância e adolescência; liberdade religiosa e de consciência; recuperação de dependentes e combate às drogas; ação social, combate à fome e à pobreza; proteção da mulher, do idoso e da pessoa com deficiência; trabalho digno; ética e serviço público; reconhecimento das igrejas e da cultura evangélica.
5. **Sem eleição.** Nada de campanha, candidatura, pré-candidatura, pesquisa, resultado eleitoral, pedido de voto, apoio de igreja a candidato, vitória ou derrota em eleição. A matéria trata do mandato, nunca da disputa. Eleito que ainda não tomou posse só entra depois da posse.

## 2. Quem entra

**Evangélico confirmado.** O político entra só se a fé evangélica é pública e verificável em uma destas fontes: (a) título religioso no nome parlamentar registrado (Pastor, Pastora, Bispo, Missionária, Apóstolo, Irmão, Irmã); (b) biografia oficial na Casa, site ou rede oficial do próprio político; (c) discurso dele nas notas taquigráficas ou nos anais; (d) site oficial do partido; (e) matéria anterior da Comunhão que o apresente como evangélico (acervo NEIA). **Assinar a Frente Parlamentar Evangélica não basta**: a frente tem signatários de outras crenças. Denominação só quando a fonte disser.

**Quem pode:** deputados federais, senadores, governadores e vices, deputados estaduais (prioridade à Assembleia Legislativa do ES), prefeitos e vereadores (prioridade à Grande Vitória), em exercício. Ex-parlamentar só em perfil histórico com gancho de data.

**Fica fora** (não escreva sobre ele e não explique o motivo na matéria):
- quem foi alvo de denúncia, investigação, processo, operação ou condenação noticiados nos últimos 12 meses, ou condenado em qualquer tempo. Antes de escolher, faça uma busca rápida no WebSearch com "nome + investigação" e "nome + denúncia"; na dúvida, troque de político e registre no resumo como "fora por cautela";
- quem está no centro de polêmica nacional na semana (o assunto do momento sobre ele é crítica ou ataque).

## 3. Rodadas e formatos

O agendamento começa 20 minutos antes. Descubra a rodada e o dia com `TZ=America/Sao_Paulo date '+%H:%M %u'`: a rodada é a próxima hora cheia entre 11h e 17h; `%u` vai de 1 (segunda) a 6 (sábado). Domingo não tem rodada.

| Rodada | Formato preferido |
|---|---|
| 11h (seg a sex) | **Fato do mandato**, de algo das últimas 72 h |
| 17h (seg a sex) | **Espírito Santo**: fato do mandato de político capixaba; sem fato do ES, **Mandato em foco** |
| Sábado (as duas) | **Agenda da fé no Legislativo** da semana ou **Mandato em foco** |

- **Fato do mandato:** um fato novo (aprovação, relatoria, lei sancionada, sessão solene, homenagem, programa com resultado oficial). 400 a 600 palavras.
- **Mandato em foco:** perfil de um político com 2 ou 3 realizações do mandato, todas com data e fonte oficial, e um gancho (data do calendário ligada ao tema dele, marco do mandato, projeto que avançou no mês). 450 a 650 palavras. É o formato reserva quando não há fato do dia.
- **Agenda da fé no Legislativo:** o que parlamentares evangélicos aprovaram ou celebraram na semana (sessões solenes, datas comemorativas, frentes, projetos de família e infância). Até 3 políticos, de partidos diferentes. 450 a 650 palavras.

**Teto: 1 matéria por rodada.** Sem pauta que passe na nota (item 6): "Sem fato novo nesta rodada", sem notificação.

## 4. Onde procurar

1. **Espírito Santo:** notícias da Assembleia Legislativa (al.es.gov.br), da Câmara de Vitória e das câmaras da Grande Vitória; Agência Senado para os senadores do ES; Agência Câmara para os deputados do ES. Acervo NEIA da Comunhão e da ES Brasil para saber quais políticos capixabas a casa já apresentou como evangélicos.
2. **Senado:** página de tag por parlamentar da Agência Senado (`https://www12.senado.leg.br/noticias/tags/Senador%20<Nome>` ou `Senadora%20<Nome>`), que lista as notícias com data e hora; Rádio Senado; comissões (CDH, CAS, CE) e Plenário.
3. **Câmara:** página do deputado (`https://www.camara.leg.br/deputados/<id>`: notícias, cargos e números do mandato) e Agência Câmara de Notícias. A página `/biografia` é bloqueada para leitura automática: use a página principal.
4. Feed nacional do NX Feed (Agência Brasil, Estadão Conteúdo), com `busca` por "evangélic", "frente parlamentar", "igrejas" ou pelo nome do político: é pista para chegar à fonte oficial.
5. WebSearch com o mês e o ano correntes ("frente parlamentar evangélica novembro 2026", "sessão solene evangélicos 2026", "Ales aprova projeto deputado pastor").

Abra a fonte com WebFetch antes de escrever. Fonte que não abre: troque de pauta.

**Crédito.** Agência Câmara, Agência Senado, Rádio Senado, assembleias, câmaras, diários oficiais e sites oficiais do político ou do partido são **fontes primárias**. Veículo de imprensa nacional é só pista: não cite nem linke (padrão, seção 5). Fala do político só se publicada pela agência da Casa, por nota taquigráfica ou por canal oficial dele, sempre atribuída. Release do mandato entra como "segundo o gabinete do deputado".

## 5. Rodízio e equilíbrio

Antes de escolher, liste as matérias da série dos últimos 30 dias: `listar_materias` com `portal` = 4 e `busca` = "FÉ E POLÍTICA" (o filtro pega o chapéu), uma vez com `estado` = publicado e outra com `estado` = agendado. Anote político, partido e UF.

- O mesmo político no máximo **1 vez a cada 15 dias** (com fato extraordinário dele, 7 dias).
- **Partidos:** nunca duas matérias seguidas centradas no mesmo partido; nas últimas 10, nenhum partido com mais de 4. Matéria com dois políticos conta para os dois partidos.
- **Espírito Santo:** pelo menos 3 das 12 matérias da semana com político capixaba, quando houver fato.
- Varie também mulheres e homens, Câmara e Senado, Congresso e ES.

## 6. Nota de pauta

Dê de 0 a 5 em cada critério e publique a maior soma, **mínimo 8** (Mandato em foco: mínimo 7):

- **Relevância:** impacto concreto para famílias, igrejas ou a sociedade, com fonte primária conferida.
- **Data:** 5 = últimas 24 h; 4 = até 72 h; 3 = na semana, ou gancho de data em até 30 dias; 2 = sem gancho.
- **Audiência da Comunhão:** 5 = Espírito Santo, ou tema que toca todas as igrejas e famílias do país; 4 = parlamentar nacional conhecido do público evangélico, ou tema de família e infância; 3 = demais.

## 7. Duplicidade

Seção 4 da padrão, e mais:
1. `listar_materias` com `portal` = 4, categoria 116630, publicadas nos últimos 7 dias.
2. `busca` pelo nome do político e pelo número do projeto, todos os estados, 30 dias (pega rascunhos e agendadas de outras rotinas).
3. NEIA `search-content` (source "Comunhão", source_type "wordpress_portal") e WebSearch `site:comunhao.com.br <nome ou projeto>`.

Se a Comunhão já deu o fato, só entra **desdobramento realmente novo** (nova fase da tramitação, sanção, regulamentação), e a matéria anterior vira o link interno ("como a Comunhão mostrou em junho").

## 8. Texto

- Autor "Redação". **Chapéu fixo: FÉ E POLÍTICA.**
- Título de até 60 caracteres, com o nome do político ou o tema no início; linha fina de até 20 palavras com nome, partido e o que ele fez; lide de 25 a 70 palavras (o quê, quem, quando, onde).
- Na primeira menção: nome parlamentar, (PARTIDO-UF) e o cargo.
- Fé: uma frase, com a fonte do item 2 ("pastor evangélico", "evangélica, segundo o partido"). Nunca deduza denominação.
- Intertítulos `<h4>`, um deles com a palavra-chave. Frases curtas, uma ideia por frase (o NX Feed cobra legibilidade).
- Projeto de lei: número, fase exata (apresentado, aprovado em comissão, aprovado no Plenário, enviado à sanção, sancionado) e próximo passo. Nunca diga que "virou lei" antes da sanção.
- Aspas curtas, só das fontes do item 4, com a origem. Nunca invente fala, número, data, cargo ou denominação.
- 1 link externo para a fonte oficial (`target="_blank" rel="noopener"`) e 1 link interno da Comunhão. **O link interno não pode levar a matéria cujo protagonista ou personagem seja alvo de denúncia ou condenação**: leia a matéria no NEIA (`get-article-content`) antes de linkar.
- **Rodapé "Com informações de..."** (decisão do Mário Fernando, 05/11/2026): **não entra** quando a base da matéria é agência (Agência Câmara, Agência Senado, Rádio Senado, Agência Brasil ou outra agência) ou a própria Casa legislativa (Câmara dos Deputados, Senado, Assembleia Legislativa, câmara municipal). Nesses casos a atribuição fica só no corpo ("segundo a Agência Senado"), com o link externo, e a matéria termina no último parágrafo do texto. O rodapé `<p><em>Com informações de [fonte]</em></p>` só entra quando a base é outra fonte oficial (site ou gabinete do político, partido, governo, prefeitura).
- Datas como "nesta quarta-feira (4)"; confira o dia da semana no calendário.
- Versículo só quando o próprio político o citou (fala dele) ou, na voz da redação, pela regra bíblica da padrão (NTLH, conferido no NEIA).
- **Fora:** as pautas proibidas da seção 2.1 da padrão; tudo o que o item 1.5 exclui; crítica a qualquer pessoa ou instituição; polêmica do dia; pedido de doação, PIX ou contato de gabinete para "ajuda"; conteúdo pago ou patrocinado de mandato (pauta que chegou de gabinete com contrapartida não é desta rotina: registre "envolve parceiro" e não publique).

**Box opcional** (no máximo um, no fim do corpo, antes do rodapé quando houver):
- **"O que o projeto prevê"**: 3 a 5 pontos tirados do texto oficial.
- **"O mandato em números"**: proposições, relatorias e presença em Plenário, só do painel oficial da Câmara ou do Senado, com o ano.

```html
<div class="box-servico" style="background:#F4F6FA;border-left:4px solid #00427B;border-radius:6px;padding:16px 20px;margin:28px 0;"><h4 style="margin-top:0;">O que o projeto prevê</h4><ul><li>…</li><li>…</li></ul></div>
```

## 9. Categorias e SEO

- `criar_materia` com `categorias` = `[{portal: "4", ids: [116630]}]` (Cotidiano › Política & Cidadania). Tema de igrejas pode levar também Igreja 6060.
- **Nunca:** Destaques 44517, Panorama 1, categorias de Missões (67595, 116628, 116627).
- Depois de criar, `prompt_do_nxfeed` (tipo seo) e ajuste. SEO pela padrão: palavra-chave = nome do político ou o tema, nota ≥ 85. Tags: nome do político, Casa legislativa, tema, "Espírito Santo" quando for do ES, e "Fé e Política". Partido não vira tag.

## 10. Imagem destacada

Ordem e regras da padrão, com estas particularidades:

1. **Foto do próprio político**, nesta ordem: recomendadas do NX Feed (`buscar_imagens` com materia_id) → editoriais pelo nome → foto da matéria oficial da Casa. Na Agência Câmara, a foto fica em `camara.leg.br/midias/image/AAAA/MM/imgNNNN-768x473.jpg`: tente primeiro a mesma URL sem o sufixo `-768x473`, que é a original grande; crédito "Nome do fotógrafo/Câmara dos Deputados". Fotos da Agência Senado já no acervo da Comunhão servem com o crédito original.
2. Contexto da foto: o político trabalhando (tribuna, comissão, sessão, evento oficial). **Nunca** foto dele em crise, protesto, tragédia, operação policial, campanha eleitoral ou ao lado de alguém alvo de denúncia.
3. Sem foto dele com direito de uso: foto do plenário da Casa (Câmara, Senado ou Ales), com crédito e "foto de arquivo".
4. Imagem por IA só como último recurso, pela padrão 9.1, e **nunca com pessoa**: cena genérica do tema.

Na descrição, diga o que a foto mostra e marque "(foto de arquivo)" quando não for do fato. O crédito da foto continua normal (fonte e autor), mesmo sem rodapé no texto.

## 11. Período eleitoral

Em ano de eleição, de **16 de agosto até o dia do segundo turno**, a rotina não publica: encerra com "Pausa eleitoral: a série volta depois do segundo turno", sem notificação. Fora desse período, o item 1.5 continua valendo. Próxima: eleições municipais de 2028.

## 12. Publicar

Refaça a duplicidade → `conferir_publicacao` (tipo publicar) → `publicar_no_wordpress` no portal 4, autor "Redação". Faltando 3 minutos ou mais para a hora cheia da rodada, agende para ela (`quando` = "dd/mm/aaaa HH:00"); senão, "agora". A primeira chamada devolve o `codigo_confirmacao`: repita com os mesmos dados e o código. Resultado incerto: confira com `listar_publicacoes` antes de repetir. Redes sociais e Destaques não são desta rotina (padrão, seções 2.2 e 3).

## 13. Resumo da rodada

`SendUserMessage`, curto, para celular, com o título **"Fé e Política Comunhão HHh · DD/MM"** e as seções da padrão (Publicadas, Imagens de IA para validar, Também na rodada, Pendências; seção vazia = "nenhuma"). Acrescente: formato, político (PARTIDO-UF), fonte que confirma a fé (item 2), nota de pauta, nota SEO, imagem (do político / da Casa / IA), fontes usadas, contagem por partido das últimas 10 e quantas da semana foram do ES. Notifique só com matéria nova ou problema. Não envie e-mail.