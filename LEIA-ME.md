# Skills da Next Editorial

Cópia das skills da Next Editorial na conta de Mário Fernando, organizadas por atividade em 14/11/2026. Cada pasta traz o SKILL.md na versão em uso na conta.

Esta pasta é cópia de consulta e backup: editar um arquivo aqui não altera a skill que roda no Claude. As skills pessoais e as de apoio (Anthropic e terceiros) ficam em `../skills-mario-pessoal`, também no GitHub (github.com/mfernandus/skills-mario-pessoal). O `MAPA-DE-CONEXOES.md` mostra quais skills de apoio servem a cada skill daqui.

## 01 Editorial / 00 Padrão de publicação

- **padrao-publicacao-next** — Regras comuns das rotinas que publicam nos sites **ES Brasil** e Comunhão via NX Feed (publicação, pautas proibidas, matéria agendada, feed só manual, duplicidade, fontes, direitos, SEO, imagem e avisos). Carregar antes de cada rotina; gráficos, republicação e imagem por IA ficam nas skills de apoio.
- **imagem-ia-next** — Apoio da padrao-publicacao-next (9.1 e 9.2): imagem por IA na Krea e legenda-fato. Carregar só quando nenhuma foto real com direito de uso servir para a matéria.
- **dados-e-graficos-next** — Apoio da padrao-publicacao-next (seções 12 e 13): gráficos, tabelas e infográficos no NXtab e dados atualizados na republicação. Carregar antes de montar qualquer peça e em toda republicação.
- **raspagem-web-next** — Busca e leitura de páginas pela API do Firecrawl, com o Apify de reserva quando os créditos acabam, para as rotinas Diversão e Arte, Fé e Política e Datafé. Diz onde ficam as chaves (na memória, nunca na skill) e traz o script raspar.py, os tetos de crédito por rotina, o que nunca se raspa e os avisos de crédito baixo ou esgotado. Carregar só quando a rotina citar esta skill.
- **pauta-local-next** — Apoio da padrao-publicacao-next (seção 10, item 0): quando a rodada publica número com eco no Espírito Santo (**ES Brasil**) ou na igreja brasileira (Comunhão), grava a pauta local no NX Feed e avisa a Joviana por e-mail.

## 01 Editorial / 01 Rotinas de notícias

- **diversao-e-arte-esbrasil** — Rotina diária de Diversão e Arte da **ES Brasil**: agenda cultural, estreias de cinema, shows, teatro, exposições e música capixaba, apuradas na base de fontes da editoria e publicadas direto. Use quando pedirem a rodada de Diversão e Arte.
- **esporte-noturno-next** — Esporte da **ES Brasil** e da Comunhão em 5 rodadas por dia (7h, 12h, 16h, 21h50, 23h50): resultados, notícias e resumo do Brasileirão, publicados direto. O noticiário geral fica na panorama-next.
- **estilo-diario-esbrasil** — Rodada diária de Estilo da **ES Brasil**: 1 matéria por subcategoria (7 por dia), com apuração, SEO e imagem, publicada direto. Única rotina de Estilo; use quando pedirem a rodada.
- **formula-1** — Fórmula 1 na **ES Brasil** em todo fim de semana de GP (sexta a domingo, 7h20, 13h20 e 19h20): ficha do GP refeita toda semana nas fontes oficiais, volume reduzido e fotos oficiais. Substitui a f1-gp-eua-2026.
- **igreja-comunhao** — Editoria Igreja da Comunhão em 5 rodadas diárias (7h, 10h, 13h, 16h e 20h), 1 matéria publicada direto por rodada nos eixos igreja, gestão, estatísticas, tecnologia, audiovisual e direito. Carregar depois da padrao-publicacao-next.
- **missoes-comunhao** — Produz e publica no portal Comunhão as matérias da editoria Missões (missões, igreja perseguida, evangelização) no padrão da casa, com fontes verificadas e box de serviço.
- **noticias-noturnas-esbrasil** — Turno noturno da **ES Brasil** (18h às 10h, 4 rodadas): apura em fonte oficial e publica uma matéria por editoria e vertical, parceiros primeiro, sem repetir a equipe. Sem Estilo nem Diversão e arte.
- **panorama-next** — Panorama (noticiário geral: Brasil, Mundo, clima e ciência, gente) da **ES Brasil** e da Comunhão em 5 rodadas por dia, a partir das agências do NX Feed, publicado direto. Roda junto com o esporte.
- **politica-comunhao** — Série Fé e Política da Comunhão: 2 matérias por dia, de segunda a sábado (11h e 17h), valorizando mandatos de políticos evangélicos de todos os partidos. Carregar depois da padrao-publicacao-next.
- **politica-esbrasil** — Política da **ES Brasil**: uma matéria por hora (dias úteis 7h–20h; fim de semana e feriado de 2 em 2 horas), só agenda positiva da política capixaba — Governo, Ales, prefeituras, bancada, TJES e TCE-ES —, parceiros primeiro. Só ato político-institucional: ação de serviço do governo (saúde, educação, agro etc.) é da editoria do tema, não de Política.
- **previsao-tempo-esbrasil** — Rotina diária da previsão do tempo da **ES Brasil**: às 19h prepara o Post A (dia seguinte + 3 dias), o Post B (2 dias) e o stories animado, e agenda tudo no NX Feed para 00h01.
- **coluna-target-esbrasil** — Coluna Target da **ES Brasil**: três notas por rodada (cliente da Next, mercado capixaba, nacional ou internacional) sobre publicidade e comunicação, publicadas direto, seg, qua e sex às 11h.

## 01 Editorial / 02 Acervo e republicação

- **acervo-comunhao** — Uma vez por dia, adapta uma matéria do acervo da Comunhão (NEIA, de 1997 até 4 meses atrás), atualiza pessoas, cargos, dados e fatos datados e agenda para as 22h, nos Destaques até as 12h.
- **acervo-esbrasil** — Uma vez por dia, adapta uma matéria atemporal do acervo da **ES Brasil**, da Revista SAMP e do site esbrasil.com.br (NEIA, até 4 meses atrás), atualiza pessoas, cargos, dados e fatos datados e agenda para as 22h, nos Destaques até as 12h.
- **artigos-acervo-comunhao** — Rotina diária que republica às 8h, no site da Comunhão, um texto autoral assinado do acervo (artigo, opinião ou gestão que não seja repercussão de factual), com in memoriam, data original, nota de contexto, regras de rejeição e story enviado para revisão da Joviana e do Mário.
- **artigos-acervo-esbrasil** — Rotina diária que republica às 8h, no site da **ES Brasil**, um texto autoral assinado do acervo (artigo, opinião ou gestão que não seja repercussão de factual), com in memoriam, data original, nota de contexto, regras de rejeição e story enviado para revisão da Joviana e do Mário.
- **artigos-acervo-next** — Rotina diária das 8h que republica um artigo assinado da editoria Artigos (revistas e sites) da **ES Brasil** e da Comunhão, com in memoriam, data original, nota de contexto, regras de rejeição e story automático. Não vale para colunas.
- **comunhao-na-esbrasil** — Rotina dos dias úteis que adapta para a **ES Brasil** matérias da Comunhão sobre família, casamento, filhos, saúde emocional ou dinheiro, sem linguagem religiosa, com aviso à Joviana pelo WhatsApp.

## 01 Editorial / 03 Dados e especiais

- **datafe-materia-diaria-comunhao** — Matéria diária da Comunhão (editoria Igreja) com os números do Datafé: uma revelação por dia sobre o Brasil evangélico, com chamada provocativa à igreja do leitor, análise, peça do NXtab e fecho com link para o portal Datafé.
- **materia-igrejas-abertas-comunhao** — Matéria mensal da Comunhão sobre CNPJs de igrejas evangélicas abertos e baixados, com os números do Evangélicos em Números, logo depois da carga mensal do CNPJ.
- **retrospectiva-esbrasil** — Produz capítulos da Retrospectiva 2026 da **revista ES Brasil** (ESB 238) para qualquer editoria, da ficha às páginas de 20,5 x 27,5 cm com texto encaixado e dados sempre na divulgação mais recente, e, depois da aprovação, pergunta se gera o pacote do InDesign (IDML com vínculos e pasta para o time).
- **datafe-manchetes-semana** — Rotina de toda segunda (5h36) que troca as 4 a 6 manchetes de números que giram no topo da home do Datafé, a partir das matérias do Datafé publicadas na Comunhão, com números reconsultados no banco.

## 01 Editorial / 04 Pesquisa e apuração

- **cacadores-destinos-conteudo** — Puxa o conteúdo de episódios do Caçadores de Destinos (Rede Tribuna) — transcrição em texto corrido, frames do vídeo e matérias e fotos do Tribuna Online — a partir do link do YouTube, da localidade ou da lista de episódios.
- **cacadores-destinos-levantamento** — Levanta todos os episódios do Caçadores de Destinos (Rede Tribuna — TV Tribuna/SBT e Band) no YouTube e no Tribuna Online e relaciona as localidades visitadas até a data de corte pedida.

## 02 Distribuição

- **youtube-comunhao-titulos** — Publica de ponta a ponta um vídeo da Revista Comunhão no YouTube: títulos A/B, descrição, tags, cards, tela final, capa publicada e 3 a 5 Shorts no corte limpo, com selos do programa e da marca e capa, prontos no canal. Download do original já liberado.
- **youtube-esbrasil-titulos** — Publica de ponta a ponta um vídeo do canal **Revista ES Brasil** no YouTube: títulos A/B, descrição, capítulos, tags, cards, tela final, playlists, capa nos templates **ES Brasil** Entrevista, Destinos ES e **Café com Moqueca**, e 3 a 5 Shorts no corte limpo dos Reels, com selos do programa e da marca e capa oficial. Pergunta o tipo de capa no início e pede ok antes de salvar no Studio. Download do original já liberado.
- **youtube-lote-noturno-next** — Roda em lote, por comando, a atualização dos vídeos dos canais da Next Editorial no YouTube em modo noturno, com teste A/B nativo de capas, Shorts exportados para as redes e a Central sempre atualizada.
- **youtube-playlists-next** — Organiza e mantém as playlists e a página inicial dos canais **revista ES Brasil** e Revista Comunhão no YouTube, no modelo em camadas (programa, editoria, tema, especial, cortes): inventário, diagnóstico, plano para aprovação, aplicação no Studio depois do ok e manutenção semanal.

## 03 Comercial e marketing

- **cartas-comerciais-next-editorial** — Gera cartas comerciais de propostas de veiculação no padrão Next Editorial — para **ES Brasil**, Comunhão, Destinos ES e Prócidade. Use esta skill sempre que o usuário pedir uma carta, proposta comercial, oferta publicitária, oferta de mídia, proposta de patrocínio, carta de prospecção, ou qualquer comunicação dirigida a um cliente/anunciante com proposta de presença editorial — mesmo quando ele não usar literalmente a palavra "carta". Também acione quando ele apenas der os insumos (destinatário + edição + investimento) sem explicitar o pedido. Esta é a skill canônica da casa para o padrão de cartas comerciais Next Editorial.

## 04 Controle

- **analise-semanal-vendas-next** — Gera a Análise Semanal de Vendas da Next Editorial — performance individual dos executivos (propostas geradas, aprovadas, pendentes) espelhada com a meta, análise do time no gráfico, e leitura imediata de fechamento da semana. Analisa por produto, por produto editorial e por projeto, com dados do NextorCRM. Acione sempre que o usuário pedir "análise de vendas", "relatório de performance", "como está o time", "fechamento da semana", "análise por executivo", ou quando a tarefa agendada das 18:30 disparar. Também é a skill canônica do painel comercial diário/semanal da casa.
- **monitor-audiencia-next** — Gera a análise de audiência dos sites da Next — **ES Brasil** e Comunhão — lendo o audiencia-latest.json do coletor. Entrega painel HTML no padrão Next e resumo curto de WhatsApp, sempre lendo o dia contra a base de sete dias e com selos REAL/REFERENCIA/SIMULADO/PENDENTE.

## 05 Administrativo e financeiro

- **documentos-next-editorial** — Gera documentos e relatórios no padrão visual da Next Editorial — Borderô (NX Fina), Espelho de paginação, Relatório de Metas (NextorCRM) e Next Performance Report — e documentos no Estilo Pessoal de Mário Fernando (verde-escuro, verde cítrico, navy e cinza). Use SEMPRE que o usuário pedir para criar, montar ou formatar relatório, borderô, espelho, plano de metas, relatório de performance ou comercial, ou qualquer documento interno da Next Editorial, **ES Brasil**, Comunhão, Destinos ES ou Prócidade, mesmo sem dizer \"no padrão\"; e quando pedir algo \"no meu estilo\", \"estilo pessoal\" ou \"estilo Mário Fernando\". Acione também quando ele der só os dados sem explicitar o formato. Aplica Inter, paletas por marca, logos oficiais, grade A4 e selos de proveniência.

## 06 Plataformas e dados

- **atualizacao-cnpj-templos** — Atualização mensal dos CNPJs de organizações religiosas do Datafé (datafe.com.br): baixa a base da Receita, classifica, carrega pela função templos-ingest e confere os números.
- **atualizacao-mapas-destinos-es** — Atualiza pontos turísticos do mapas.nx.tv.br (Destinos ES): locais próximos novos (comer, ficar, serviços, fazer), fotos NX Fotos e Google com crédito, tags de experiência, textos e informações. Plano antes de gravar.
- **verificacao-es-em-numeros** — Verifica o site ES em Números (esemnumeros.esbrasil.com.br): erros, números novos nas fontes oficiais, coletores quebrados e fotos novas do NX Fotos. Use para a rodada semanal ou mensal.
- **validacao-diaria-datafe** — Validação diária dos números do Datafé (datafe.com.br): confere o banco, uma amostra de municípios contra o IBGE (SIDRA) e o site publicado, e acusa igreja escondida, soma errada, dado vencido e erro de texto. Só lê.
- **cidade-em-numeros-procidade** — Gera o site "{Cidade} em Números" (Prócidade, by NextLab) para um município do ES a partir do modelo de Conceição da Barra e Piúma, com as mesmas fontes, NX Fotos, mapa com relevo e ligação ao Destinos ES.

## 99 Arquivadas

- **f1-gp-eua-2026** — Cobertura temporária do GP dos Estados Unidos de F1 (Austin, 22 a 25/10/2026) na **ES Brasil** — rodadas a cada 4h e boletins logo após cada treino, classificação e corrida.

## Observações

- youtube-esbrasil-titulos: além do SKILL.md atual, traz o kit de capas (scripts, assets e exemplos) copiado de Documentos/Claude Skills.
- f1-gp-eua-2026 foi arquivada porque a formula-1 a substitui.
