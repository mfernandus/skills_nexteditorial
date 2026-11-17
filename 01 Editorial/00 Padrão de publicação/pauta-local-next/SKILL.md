---
name: "pauta-local-next"
description: "Apoio da padrao-publicacao-next (seção 10, item 0): quando a rodada publica número com eco no Espírito Santo (ES Brasil) ou na igreja brasileira (Comunhão), grava a pauta local no NX Feed e avisa a Joviana por e-mail."
---

# Pauta local — ES Brasil e Comunhão

Quando uma rotina publica um número nacional ou internacional (pesquisa, índice, ranking, balanço oficial) sobre algo que também acontece no Espírito Santo ou na igreja brasileira, a casa não para na notícia de agência: a pergunta seguinte é "e aqui?". Esta skill avalia a matéria publicada, grava no NX Feed uma pauta de contexto local pronta para a equipe e avisa a Joviana por e-mail na hora (decisão do Mário Fernando, 17/11/2026).

Os dois exemplos que deram origem à regra:
- **ES Brasil:** a agência publica que deslizamentos e desabamentos aumentaram no país por efeito do El Niño. Pauta: quantas áreas de risco o ES tem e em quais municípios, o que a Defesa Civil e as prefeituras já fazem e como o morador reduz o risco em casa.
- **Comunhão:** a Lifeway ou o Barna divulgam que a saída de jovens das igrejas nos Estados Unidos cresceu 19% em cinco anos. Pauta: o que os números mostram nas igrejas brasileiras, o que dizem pastores e líderes de jovens de várias regiões do país e o que fazem de diferente as igrejas que mantêm seus jovens.

**"Local" depende do veículo** (decisão do Mário Fernando, 17/11/2026): na **ES Brasil**, é o Espírito Santo; na **Comunhão**, que circula no país inteiro, é o Brasil. A apuração da Comunhão é nacional, e o ES não é o foco dela.

A skill **não** escreve a matéria local, não publica nada e não apura os números locais: aponta onde eles estão. A reportagem é da equipe.

Carregue depois da `padrao-publicacao-next`, que a chama na seção 10, item 0. Valem as regras dela, em especial as pautas proibidas (2.1), as fontes da Comunhão (5) e o padrão do texto (7).

## 1. Quais matérias entram

Só as matérias que a rodada **publicou** e que passaram no filtro rápido da padrão: número nacional ou internacional, com fonte identificável, sobre tema que também acontece no ES (ES Brasil) ou na igreja brasileira (Comunhão). Item da varredura que não foi publicado não gera pauta.

Na Comunhão, entram dois casos: número de fora do Brasil sobre igreja, fé, família ou juventude (pede o equivalente no Brasil) e número nacional da sociedade sem o recorte da igreja (pede o recorte da igreja evangélica brasileira).

Ficam de fora: matéria que já é do ES, esporte, previsão do tempo, Diversão e Arte, republicação de acervo, artigos, pesquisa eleitoral, declaração de político sem dado e número sem fonte identificável. Na Comunhão, também a matéria que já traz o recorte da igreja no Brasil (ex.: as do Datafé).

## 2. Régua

**Travas (qualquer uma descarta):**
1. O ângulo local viraria pauta proibida (padrão, 2.1): denúncia, cobrança a governo, prefeitura, empresa ou parceiro, aumento de tarifa, dado de Ministério Público, tribunal de contas ou controladoria. Risco se trata como serviço e prevenção, nunca como acusação.
2. Comunhão: tema católico (mesma regra das rotinas da Comunhão), crítica a igreja, denominação ou líder, ou ângulo que dependa de veículo jornalístico do ES.
3. A casa já tem o ângulo local: pauta local sobre o mesmo assunto ou matéria local publicada sobre ele nos últimos 30 dias (seção 4). Exceção: número novo que muda a história; aí a pauta é de atualização e o título diz isso.

**Nota (0 a 2 em cada critério):**

| Critério | 0 | 1 | 2 |
|---|---|---|---|
| Peso do número | curiosidade | relevante | forte: recorde, virada de tendência, risco à vida, bolso, saúde, futuro da igreja |
| Eco aqui | o fenômeno quase não existe no ES (ES Brasil) ou na igreja brasileira (Comunhão) | existe, com alcance limitado | ES Brasil: atinge muita gente ou o ES tem marca própria no tema (líder, pior ou melhor índice, vertical da casa); Comunhão: atinge muitas igrejas ou fiéis no país |
| Dado local | não há fonte local | ES Brasil: fonte nacional com recorte por UF; Comunhão: dado brasileiro geral, sem recorte de evangélicos | ES Brasil: fonte oficial com recorte do ES ou dos municípios; Comunhão: dado brasileiro com recorte de evangélicos ou de igrejas (seção 3) |
| Serviço ou solução | nada a fazer | dá para explicar o que muda | dá para dizer como prevenir, mitigar, aproveitar ou agir |

Vira pauta com **nota 6 ou mais e "dado local" de pelo menos 1**. Se duas passarem na mesma rodada para o mesmo veículo, fica a de maior nota (empate: a mais recente); a outra pode entrar numa rodada seguinte, se ainda valer.

**Teto:** ES Brasil até 3 pautas por dia; Comunhão até 2. No máximo 1 por veículo por rodada. A mesma matéria só gera pauta para os dois veículos quando os ângulos forem de fato diferentes (ex.: saúde emocional de jovens: na ES Brasil, a rede pública do ES; na Comunhão, as igrejas do país).

## 3. O ângulo local

**ES Brasil:** o tamanho do fenômeno no ES e nos municípios, a comparação Brasil × ES, quem é afetado, o que governo, prefeituras, entidades e empresas já fazem (parceiros primeiro) e o que o leitor pode fazer. Ligue às verticais da casa quando couber: portos e logística, petróleo e gás, energia, agro, rochas, indústria, educação, saúde, segurança, turismo.

**Comunhão** (circulação nacional: o recorte é o Brasil): o que o número quer dizer para a igreja evangélica brasileira. Dado de fora pede o equivalente no Brasil; dado nacional da sociedade pede o recorte da igreja. Ouvir lideranças de denominações e convenções nacionais, pastores e líderes de jovens, família ou ação social de várias regiões e pesquisadores de religião; mostrar o que já dá certo em igrejas do país; caminho pastoral, sem tom de crítica. O ES entra só como um dos exemplos, se couber. Versículo, se houver, na NTLH (padrão, seção 7).

**Onde estão os números** (cite as fontes sem abrir; abra no máximo uma página quando precisar do endereço exato de um indicador):

| Tema | Fontes |
|---|---|
| Clima, chuva e áreas de risco | Defesa Civil-ES, Cemaden, Incaper, Inmet, Agerh, Serviço Geológico do Brasil (setorização de risco) |
| Economia, emprego, renda, social | ES em Números (esemnumeros.esbrasil.com.br), IJSN, IBGE Cidades e Sidra, Novo Caged, Findes/Ideies, Fecomércio-ES, Sebrae-ES |
| Saúde | Sesa (painéis), DataSUS/Tabnet |
| Educação | Sedu, Inep (Ideb e Saeb por UF e município), ESEDUCA |
| Segurança | Sesp-ES, Anuário Brasileiro de Segurança Pública (recorte por UF) |
| Portos, petróleo, energia, transporte | Antaq, ANP, Aneel, ANTT, DER-ES |
| Agro | Incaper, Seag, IBGE (PAM e PPM), Conab |
| Igrejas e fé (Comunhão, recorte Brasil) | Datafé (datafe.com.br: evangélicos, templos e CNPJs no Brasil, por região e UF), IBGE Censo 2022 (religião), IBGE Estatísticas do Registro Civil (casamentos e divórcios), pesquisas nacionais com recorte de evangélicos (Datafolha, Ipec, Quaest), o instituto da pesquisa original (Lifeway, Barna, Pew) |

## 4. Antes de gravar (uma conferência por rodada)

1. `listar_materias` com `busca` = "Pauta local", sem filtro de portal, `data_de` = 30 dias atrás, formato compacto, todas as páginas. Daí saem o que já foi sugerido (trava 3) e quantas pautas cada veículo já recebeu hoje (teto). O veículo está no título.
2. Matéria local já publicada: use as listagens de publicadas que a rodada já fez (padrão, seção 4) e uma `listar_materias` com `busca` pelo tema local (todos os estados, 30 dias). Sem WebSearch `site:`.

## 5. Gravar a pauta no NX Feed

`criar_materia`, uma por pauta:

- **titulo:** "Pauta local · ES Brasil: recorte" ou "Pauta local · Comunhão: recorte", com o recorte em até 60 caracteres (ex.: "Pauta local · ES Brasil: áreas de risco e El Niño no ES"; "Pauta local · Comunhão: jovens que deixam a igreja no Brasil").
- **chapeu:** "Pauta local".
- Sem autor, sem categorias, sem imagem e sem campos de SEO: o painel mostra o rascunho como incompleto e ninguém o publica por engano. Não precisa de `prompt_do_nxfeed`.
- **texto_html**, até 350 palavras, neste molde:

```html
<p><strong>Para:</strong> ES Brasil · <strong>Gancho vale até:</strong> sexta-feira (20/11)</p>
<h3>Gancho</h3>
<p>Fato e número, com a fonte e a data. Matéria no ar: <a href="LINK">título</a>. Fonte original: <a href="LINK">instituição</a>.</p>
<h3>Por que interessa aqui</h3>
<p>Duas ou três frases.</p>
<h3>Perguntas para apurar</h3>
<ul><li>De três a cinco perguntas, começando pelo número local.</li></ul>
<h3>Onde estão os números</h3>
<ul><li>Fonte: o que buscar (link).</li></ul>
<h3>Quem ouvir</h3>
<ul><li>Cargo e instituição, parceiros primeiro.</li></ul>
<h3>Serviço</h3>
<p>O que o leitor (ou a igreja) pode fazer.</p>
<h3>Formato sugerido</h3>
<p>Título provisório (até 60 caracteres), peça do NXtab (ex.: barras Brasil × ES na ES Brasil; EUA × Brasil na Comunhão) e foto (termo para o NX Fotos).</p>
<p><em>Pauta sugerida pela rotina NOME em DD/MM, às HHh. Rascunho de pauta: não publicar como está.</em></p>
```

Regras do texto:
- Nenhum número local (do ES na ES Brasil, do Brasil na Comunhão) sem fonte aberta na rodada. Se a própria agência trouxe o recorte, ele entra com a fonte.
- Nenhum nome de pessoa como fonte a ouvir, só cargo e instituição, salvo quem já está na matéria publicada ou em página oficial aberta.
- Caixa alta e baixa (padrão, seção 7). Gancho costuma valer de 3 a 7 dias.

Guarde o id e o link do painel que `criar_materia` devolver.

## 6. Avisar a Joviana por e-mail

- **Quando:** logo depois de gravar, a qualquer hora, um e-mail por pauta.
- **Para:** os dois endereços da Joviana, juntos no campo `to`: `joviana.venturini.jornalista@gmail.com` e `jovianav@nxte.net`. Mais ninguém; o Mário acompanha pelo resumo da rodada.
- **Como:** `mcp__Gmail__send_message` (carregue com ToolSearch; sai da conta do Mário), com `includeSignature` = false.
- **Assunto:** o título da pauta (ex.: "Pauta local · Comunhão: jovens que deixam a igreja no Brasil").
- **htmlBody:** "Olá, Joviana! Nova sugestão de pauta para a <b>ES Brasil</b>." (ou para a Comunhão); na linha seguinte, "Pauta no NX Feed" e "Matéria de origem", cada um com o link; depois, o mesmo texto_html gravado na pauta; no fim, "Sugestão automática das rotinas de conteúdo da Next Editorial." **ES Brasil** sempre em negrito.
- **body** (texto puro, alternativa): as três primeiras linhas com os links, sem Markdown.
- **Deu certo:** guarde o id da mensagem para o resumo.
- **Falhou:** tente mais uma vez. Se falhar de novo, a pauta fica no NX Feed, o resumo registra em Pendências "Joviana não recebeu o e-mail da pauta" com o erro, e a rodada manda a notificação do app.
- Este e-mail é a única exceção à regra de não mandar e-mail (padrão, seção 10) e serve só para o aviso de pauta local.

## 7. No resumo da rodada

Seção "Pautas locais" do resumo (padrão, seção 10), só quando houver: para cada pauta, veículo, recorte, link do painel, nota (ex.: 7/8) e o aviso (e-mail às HHh ou não recebido). Matéria que passou no filtro e não virou pauta não entra no resumo.

## 8. Economia do plano

- O filtro rápido fica na padrão: esta skill só é carregada quando há matéria candidata, uma vez por execução (padrão, 11.7).
- Dê a nota com o que a rodada já tem (texto publicado, fonte já aberta). Nenhuma busca nova para avaliar.
- Uma conferência por rodada (seção 4), um `criar_materia` e um e-mail por pauta.
- Não abra fontes locais para preencher números: a pauta aponta onde estão.

## Modelo recomendado
- Nível: Haiku como etapa; na prática roda no modelo da rotina que a carrega (não tem tarefa agendada própria)
- Nota: 2/12 (raciocínio 1, fontes 1, texto 0, números 0, fluxo 0, risco 0)
- Motivo: julga com régua escrita, grava um molde curto que não vai ao ar e manda um e-mail interno
- Teste: não testado; primeira execução monitorada pelo resumo da rodada
- Subir para Sonnet se: virar tarefa própria ou se as pautas chegarem rasas ou repetidas na conferência da Joviana