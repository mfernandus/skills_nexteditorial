---
name: "noticias-noturnas-esbrasil"
description: "Turno noturno da ES Brasil (18h às 10h, 4 rodadas): apura em fonte oficial e publica uma matéria por editoria e vertical, parceiros primeiro, sem repetir a equipe. Sem Estilo nem Diversão e arte."
---

# Turno noturno de notícias — ES Brasil (18h às 10h)

Rotina que mantém o site da **ES Brasil** (esbrasil.com.br, portal 1 no NX Feed) atualizado enquanto a redação está fora: das 18h às 10h, em quatro rodadas.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, cuidados do NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem, avisos e economia do plano (seção 11) estão lá. Aqui fica só o que é do turno noturno. Se a skill-base não estiver disponível, não publique nada: deixe as matérias em rascunho e avise que a skill-base faltou.

**Princípio editorial:** a ES Brasil é um site local. Toda editoria e toda vertical começa pelo Espírito Santo. Notícia nacional só entra numa vertical quando não houver fato capixaba relevante, e sempre com um parágrafo sobre o que muda para o ES.

**Fora desta rotina:** Estilo (rotina estilo-diario-esbrasil, que roda de manhã), Diversão e arte (diversao-e-arte-esbrasil), esporte (esporte-noturno-next) e o noticiário nacional e internacional do Panorama (panorama-next).

## Meta de cada turno (das 18h de um dia às 10h do dia seguinte)

| Bloco | Meta mínima no turno |
|---|---|
| Editorias: Vida Capixaba, Economia, Política, Destinos ES | 1 notícia importante por editoria (4) |
| Verticais: Portos, ESG, Energia, Rochas naturais, Mercado imobiliário, Indústria, Agro | 1 notícia por vertical (7) |

Teto: 3 matérias por editoria ou vertical no turno. Mais vale uma matéria forte que três fracas.

**Diversão e arte não é deste turno** (decisão de 02/11/2026): a editoria é só da rotina `diversao-e-arte-esbrasil` (rodadas das 8h e das 14h). O turno não escreve, não aproveita de agência nem edita matéria de Diversão e arte; um fato da editoria achado na varredura vai para o resumo, em "Também na rodada", como "fica para a rotina de Diversão e arte".

## Rodadas (Brasília)

Descubra a rodada pela hora atual. Cada rodada cobre o que aconteceu desde a anterior e o que ficou faltando da meta. Em toda rodada, os parceiros comerciais do bloco são varridos primeiro (passo 1b).

| Rodada | Foco |
|---|---|
| **18h** (fechamento do dia) | Fatos da tarde ainda sem matéria da casa. Prioridade: Vida Capixaba, Economia e Política. Teto: 4 matérias. |
| **22h** (noite) | Verticais (dados e releases do fim do dia, comércio exterior, portos, energia). Em noite de eleição ou votação importante, Política vem primeiro. Teto: 5. |
| **6h** (madrugada e agenda) | O que saiu de madrugada nos sites oficiais, Diário Oficial do ES (dio.es.gov.br) e agenda do dia (inaugurações, leilões, indicadores, eventos). Destinos ES e o que faltou das verticais. Teto: 4. |
| **9h** (fecho do turno) | Completa o que faltou da meta e manda o balanço do turno. Teto: 4. |

Se a execução cair fora desses horários, use a janela "desde a última matéria da casa".

## 1. O que a equipe já fez (trava de duplicidade)

A trava é a da skill-base (seção 4), com estas janelas: `listar_publicacoes` (portal 1, data_de = 3 dias atrás, todas as páginas) e rascunhos dos últimos 3 dias, uma vez por rodada para todas as pautas; e, para cada pauta candidata, `listar_materias` com `busca` pelo nome da empresa, órgão, cidade ou fato (data_de = 30 dias atrás) e WebSearch `site:esbrasil.com.br <tema>`. Se a equipe já tem o fato, escolha outro assunto dentro do mesmo tema; sem outro assunto, registre "coberto pela equipe" e siga. Os rascunhos da simulação de 25/10/2026 (ids 269046 a 269091) contam como já feitos.

## 1a. Pendências do turno (rodada das 9h)

Liste os rascunhos do turno que ficaram parados (estado rascunho sem filtro de portal e rascunho_no_wp com portal 1, últimos 3 dias, só os criados via Claude — veja `historico_da_materia`). Os atuais (até 48 horas, indicador oficial mensal ainda não publicado ou evento futuro): resolva foto e SEO e publique pelo passo 7. Os superados (fato já publicado pela casa, evento já acontecido, notícia velha sem valor): não publique e cite no resumo. Rascunho da equipe humana: não mexa.

## 1b. Parceiros comerciais primeiro (pedido do Mário, 25/10/2026)

Em toda varredura, cada editoria e vertical começa pelos **parceiros comerciais da Next**. Se um parceiro tem fato novo de verdade, ele ganha a vaga do bloco antes de qualquer outra pauta. Relacionamento comercial não substitui critério editorial: sem fato novo, a vaga vai para a melhor notícia do ES.

**Onde está a lista:**
- Na rodada das 18h (uma vez por turno), leia a planilha **Blitz Editorial Out/25** (Google Sheets, spreadsheetId `1e3-3Zs4Nl0wOHsyiNyd99XaZKZYg0W0gjjMSRRI-xlg`), aba **Parceiros Comerciais 2026**, colunas A a O. Use só as linhas com **K = SIM** (cliente com proposta aprovada no Nextor). A coluna J traz editoria e temas; a coluna M, as variações do nome para buscar. As regras estão na aba **Regras Blitz 2026**.
- Some à planilha os parceiros que o Mário indicou por bloco (tabela abaixo), mesmo que não estejam com K = SIM.
- Organizações da Comunhão (igrejas, editoras e música cristã, como Igreja Cristã Maranata, Convenção Batista, Mundo Cristão e Musile) ficam fora desta rotina.

| Bloco | Parceiros a varrer primeiro |
|---|---|
| Vida Capixaba | prefeituras parceiras (Vitória, Vila Velha, Serra, Cariacica, Viana, Fundão, Aracruz, Colatina, Cachoeiro de Itapemirim, Marataízes, Piúma, Presidente Kennedy, Conceição da Barra), Cesan, HIFA, São Bernardo Saúde, Ecovias Capixaba, Águia Branca, Senac, FEST |
| Economia | ES em Ação, Banestes, Bandes, Sicoob, Sicredi, Banco do Nordeste, Sebrae, Fecomércio, Sindiex |
| Política | Assembleia Legislativa (Ales) e Governo do ES (Secom-ES) |
| Destinos ES | Sindihoteis, Cooptures, Chalé dos Lagos, Águia Branca, prefeituras parceiras (turismo) |
| Portos | Vports, Imetame, Portocel, ArcelorMittal, Sindamares, Intersindical da Orla Portuária, Ecovias Capixaba, Coope Serrana |
| ESG | Ufes, Fecomércio, Sebrae, Cesan, ArcelorMittal, Samarco |
| Energia | Petrobras, ES Gás, EDP, Fortlev Solar |
| Rochas naturais | Sindirochas, Centrorochas, Milanez & Milaneze, Sicoob Credirochas |
| Mercado imobiliário | Galwan, Vaz Desenvolvimento Imobiliário, Grand Construtora, Sinduscon-ES, Construtora Epura, CBL Lotes, Buaiz Imobiliária |
| Indústria | Findes, Sindiex, Sindifer, Sinduscon-ES, ArcelorMittal, Samarco, RDG Aços |
| Agro | Cooabriel, Sicoob, Banestes, OCB, Senar/Faes, Buaiz Alimentos, Carmomaq, Banco do Nordeste |

**Como varrer os parceiros (economia do plano, 04/11/2026; nenhum parceiro deixa de ser varrido):**
1. Por bloco, uma ou duas buscas WebSearch (modo standard) com os nomes dos parceiros do bloco juntos (4 a 6 por consulta, com as variações da coluna M) e o mês e o ano, em vez de uma busca por parceiro.
2. Abra a sala de imprensa ou a página de notícias dos parceiros do bloco que abrem por leitura automática (seção 2.2) e dos que a busca apontou com fato novo. Site que a seção 2.2 diz que não abre não é tentado de novo.
3. `listar_materias` com `busca` pelo nome (data_de = 30 dias atrás) só do parceiro que tiver fato novo, para saber se e quando a casa falou dele pela última vez.
4. Vale como fato novo: investimento, obra, inauguração, resultado ou balanço, dado setorial, lançamento, evento com data, prêmio, programa ou edital aberto, nomeação. O site ou o release do próprio parceiro conta como fonte primária.
5. Entre dois fatos de força parecida, prefira o parceiro que está há mais tempo sem matéria na casa.
6. A matéria sobre parceiro é jornalismo: mesmo padrão, mesma apuração, sem adjetivo promocional, sem "parceiro" no texto. Conteúdo pago é Conteúdo de Marca (categoria 13596) e não é feito por esta rotina.
7. Fato negativo envolvendo parceiro (acidente, multa, demissões): não esconda nem suavize. Escreva com a mesma régua, publique como as demais e marque "envolve parceiro" no resumo, para os gestores conferirem. Denúncia, aumento de tarifa e fato que nasce de órgão de controle ficam fora pela seção 2.1 da skill-base, também quando o parceiro é o assunto.
8. Quando a pauta do bloco não for de parceiro, use o parceiro do setor como fonte de dado sempre que houver número oficial dele (ex.: Sinduscon-ES numa matéria de imóveis).

## 2. Varredura

1. **NX Feed primeiro:** `listar_materias` lista = feed_nacional, data_de = início da janela, formato compacto, por_pagina 100. Separe o que tem relação com o ES ou com as verticais (Agência Brasil – Economia, Estadão Conteúdo – Economia etc.).
2. **Fontes oficiais do ES** (fonte de verdade): es.gov.br/Noticias e secretarias (Sedes, Seag, Setur, Secult, Sesa, Sedu, Sesp, Semobi, Seama, ARSP, IJSN, Incaper, Iema, Idaf, DER-ES), Diário Oficial do ES, Ales, TRE-ES, prefeituras (Vitória, Vila Velha, Serra, Cariacica, Guarapari, Linhares, Cachoeiro, Colatina, Aracruz, São Mateus e as demais quando o fato for delas), Findes, Fecomércio-ES, Sebrae-ES, Banestes, Bandes.
3. **Fontes oficiais das verticais:** Portos — Antaq, Vports, Portocel, Porto Central, Imetame, TVV, Ministério de Portos; Energia — ANP, Aneel, EPE, ONS, Petrobras, EDP, ES Gás, ARSP; Rochas — Centrorochas, Sindirochas, Comex Stat; Imobiliário — Sinduscon-ES, Ademi-ES, FipeZap, Caixa, Abecip; Indústria — Findes/Observatório Findes, IBGE (PIM-PF), Caged; Agro — Seag, Incaper, Conab, IBGE (LSPA), Cecafé, CCCV, Cooabriel, Coopeavi; ESG — Seama, Iema, Ufes, Fapes, relatórios e releases das empresas (Vale, ArcelorMittal, Suzano, Petrobras, Samarco).
4. **Imprensa só como pista:** A Gazeta, Folha Vitória, ES Hoje, Tribuna Online, Século Diário, Valor, Folha, Estadão, portais setoriais.
5. WebSearch no modo standard; o extended só quando o standard não trouxer um fato muito recente.

### 2.1 Calendário dos indicadores mensais (conferido em out/2026)

| Indicador | Fonte oficial | Quando sai | Bloco |
|---|---|---|---|
| Exportação de rochas (ES e Brasil) | Sindirochas, relatório em PDF (sindirochas.com/relatorio-exportacoes-rochas.php) | por volta do dia 13 | Rochas |
| Exportação de café pelos portos do ES | CCCV, estatística mensal em PDF (cccv.org.br/exportacao/estatistica-mensal) | por volta do dia 16 | Agro |
| Preço do m² (venda) e aluguel | FipeZAP (downloads.fipe.org.br/indices/fipezap/) | venda no início do mês; locação por volta do dia 13 | Imobiliário |
| Movimentação portuária | Vports (vports.com.br) | por volta do dia 13, dado de 2 meses antes | Portos |
| Confiança da indústria (ICEI-ES) | Observatório Findes (observatoriofindes.com.br) | por volta do dia 19 | Indústria |
| Produção de petróleo e gás por estado | ANP, Boletim Mensal da Produção (gov.br/anp) | início do mês | Energia |
| Estudos e leilões de energia | EPE, notícias (epe.gov.br/pt/imprensa/noticias) | contínuo | Energia |
| Malha fina, restituição, arrecadação | Receita Federal (gov.br/receitafederal) | contínuo | Economia |
| Turismo, missões, eventos de negócios | Agência Sebrae ES (es.agenciasebrae.com.br) | contínuo | Destinos ES, Economia |
| Universidade, pesquisa, inovação | Ufes (ufes.br/conteudo), Fapes | contínuo | ESG, Vida Capixaba |

Indicador fora da semana em que costuma sair não precisa ser conferido na rodada.

### 2.2 Sites oficiais que não abrem por WebFetch

vilavelha.es.gov.br, al.es.gov.br, in.gov.br (DOU), as listas de notícias de es.gov.br e das secretarias (abrem vazias), gov.br/antaq, tvv.com.br, esgas.com.br, imetame.com.br, ademi-es. Nesses casos, abra a página no navegador (Claude in Chrome, carregando antes a skill chrome-browser) só para LER; nunca preencha nada. No navegador, leia a lista de notícias de cada fonte uma vez por rodada e abra a notícia só quando ela for virar pauta (skill-base, seção 11). Para atos do DOU, procure a portaria pelo número em agregadores de atos oficiais e cite o DOU como fonte. Se nem assim houver fonte oficial, troque a pauta.

Também bloqueiam leitura automática ou dão erro (out/2026): vazdi.com.br, cbllotes.com.br, buaizimobiliaria.com.br, bandes.com.br, esemacao.org.br, cesan.com.br e os sites das prefeituras de Cachoeiro, Cariacica, Viana, Fundão, Marataízes e Piúma. Atalhos que funcionam: Findes pelo feed (findes.com.br/feed/); Fecomércio-ES, Agência Sebrae ES, Senar-ES, Sesc-ES, Senac-ES, Centrorochas e as prefeituras da Serra, de Aracruz e de Colatina abrem normalmente. O site da Construtora Epura ainda não foi identificado (epura.com.br é de outra empresa).

## 3. O que entra (por bloco)

- **Vida Capixaba** (cidades, mobilidade, educação, saúde, meio ambiente, segurança): o fato que mais mexe com o dia a dia do capixaba. Alterne as subcategorias ao longo da semana. Polícia só com interesse público claro e nunca sensacionalista; operação policial contra alvo determinado é denúncia e fica fora (2.1 da skill-base). Estilo não: é da rotina de Estilo.
- **Economia:** emprego, renda, tributos, comércio, serviços, crédito, MEI, com número do ES.
- **Política:** Governo do ES, Ales, prefeituras, bancada capixaba. Em eleição: resultado e números oficiais do TRE-ES/TSE.
- **Destinos ES:** turismo no ES (voos, rotas, eventos, destinos, dados da Setur).
- **Verticais:** fato capixaba primeiro (investimento, operação, recorde, licença, leilão, dado setorial do ES). Sem fato local na janela, notícia nacional com impacto direto no ES e um parágrafo "O que muda para o Espírito Santo".

Não entra: as pautas proibidas da seção 2.1 da skill-base (denúncia; aumento ou reajuste de tarifa, inclusive de Cesan, EDP, ES Gás, pedágio e ônibus; o que nasce de Ministério Público, Tribunal de Contas ou controladoria); release sem notícia; nota de agenda sem fato; notícia com mais de 7 dias sem desdobramento (exceção: indicador oficial mensal que a casa ainda não publicou vale até sair o dado do mês seguinte); esporte; Panorama nacional e internacional; Estilo.

## 4. Padrão da matéria

- Chapéu em maiúsculas (ex.: PORTOS, ROCHAS NATURAIS, MERCADO IMOBILIÁRIO, AGRO, ENERGIA, ESG, INDÚSTRIA, TURISMO, CULTURA, POLÍTICA, ECONOMIA, MOBILIDADE).
- **Tamanho:** 350 a 600 palavras.
- Intertítulos em `<h4>`; listas em `<ul>`; destaques em `<strong>`.
- Depois do 2º parágrafo: `[sc name="leia_mais" categoria="<slug da categoria>" num_posts="2" ][/sc]`.
- O resto do padrão (título, lide, link, rodapé, datas, SEO) está na skill-base.

## 5. Categorias (portal ES Brasil = 1; sempre mãe + filha)

| Bloco | Categorias |
|---|---|
| Vida Capixaba › Educação | 1615, 1722 |
| Vida Capixaba › Estado (cidades) | 1615, 9401 |
| Vida Capixaba › Meio Ambiente | 1615, 2784 |
| Vida Capixaba › Saúde | 1615, 119 |
| Vida Capixaba › Segurança | 1615, 9403 |
| Vida Capixaba › Mobilidade | 9402 |
| Economia (geral) | 58, 83880 |
| Economia › Mercado de trabalho | 58, 10014 |
| Economia › Comércio e serviços | 58, 2120 |
| Economia › Empreendedorismo / MEI | 58, 16978 |
| Economia › Comércio exterior | 58, 72227 |
| Política › Estado | 115, 73624 |
| Política › Municípios | 115, 1739 |
| Eleições (em ano eleitoral) | 115, 73624, 84181 |
| Destinos ES | 74964, 8314 |
| **Portos** | 16007, 45846 |
| **ESG** | 58, 72667 |
| **Energia** | 58, 16008 |
| **Rochas naturais** | 118, 72239 |
| **Mercado imobiliário** | 118, 72240 |
| **Indústria** | 58, 118 |
| **Agro** | 58, 66 |

- Aeroportos: 16007, 72247. Rodovias: 16007, 72245. Ferrovias: 16007, 72246.
- Nunca Destaques (11966).

## 6. Imagem

Regra da skill-base, com esta ordem de busca: `buscar_imagens` recomendadas (materia_id) → NX Fotos (termo) → editoriais (termo) → foto oficial de divulgação (governo, prefeitura, empresa, entidade, parceiro) com fonte, autor e legenda → imagem por IA. Prefira a foto real do fato: em notícia local quase sempre há foto oficial.

## 7. Criar e publicar

1. Reconferência leve de duplicidade imediatamente antes de publicar (skill-base, seção 4): `listar_publicacoes` do portal 1 desde a primeira conferência e `listar_materias` com `busca` pelo fato (todos os estados). As listagens de 3 dias e o WebSearch do passo 1 não se repetem.
2. `criar_materia` com todos os campos (título, linha fina, chapéu, autor "Redação", texto, palavra-chave, título SEO, meta, slug, tags, categorias do passo 5 e imagem).
3. Nota SEO pela skill-base.
4. Publique direto no portal ES Brasil, uma de cada vez: a primeira da rodada "agora" e as seguintes agendadas de 10 em 10 minutos (campo `quando`, horário de Brasília).

## 8. Resumo

Avisos da skill-base. Título do resumo: **"Turno noturno ES Brasil – rodada das <hora>"**.

Parte própria do resumo:
- publicadas: bloco (editoria ou vertical), título, local ou nacional, fonte oficial, parceiro (sim/não e qual), nota SEO, imagem (real / IA / sem imagem), horário e link no ar (ou agendado);
- parceiros: quais tiveram matéria, quais foram varridos sem fato novo, casos "envolve parceiro";
- meta do turno (na rodada das 9h, o balanço do turno inteiro): o que foi cumprido e o que faltou, com o motivo (sem fato novo, coberto pela equipe, sem fonte oficial);
- pautas descartadas por duplicidade e o que entrou no lugar; dados não confirmados; categoria recusada.

Rodada sem novidade termina com "Sem fato novo nesta rodada", sem notificação.