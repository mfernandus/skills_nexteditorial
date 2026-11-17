---
name: "datafe-materia-diaria-comunhao"
description: "Matéria diária da Comunhão (editoria Igreja) com os números do Datafé: uma revelação por dia sobre o Brasil evangélico, com chamada provocativa à igreja do leitor, análise, peça do NXtab e fecho com link para o portal Datafé."
---

# Datafé · matéria do dia na Comunhão

Uma matéria por dia, todos os dias, na editoria **Igreja** do portal Comunhão (NX Feed, portal **4**), feita a partir dos dados do **Datafé** (datafe.com.br), o portal de dados da Revista Comunhão. Pedido de Mário Fernando em 13/11/2026.

**O que a matéria tem que provocar:** "eu não sabia disso", "eu não sabia que era desse tamanho". Não é notícia de dado. É uma revelação, com tamanho traduzido para algo que o leitor conhece e uma leitura da Comunhão sobre o que aquilo significa para a igreja e para o país.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, pautas proibidas (2.1), matéria agendada (2.2), feed só manual (2.3), NX Feed (3), duplicidade (4), fontes (5), direitos (6), texto (7), SEO (8), imagem (9), avisos (10), economia (11) e NXtab (12). Nada em caixa alta. Aqui fica só o que é desta rotina. Execução agendada não tem ninguém acompanhando: não faça perguntas. Na dúvida, escolha a pauta mais segura e registre no resumo.

## 1. Regras da editoria Igreja que valem aqui

- **Igreja Católica: só como dado de comparação** (exceção liberada por Mário Fernando em 13/11/2026, só para esta rotina; a regra de 10/11/2026 da editoria Igreja continua para o resto).
  - **Pode:** números do Censo, do CNEFE e de pesquisas que ponham católicos e evangélicos lado a lado (percentual, locais de culto por fiel, quando e se os evangélicos passam os católicos, quem foi criado católico e hoje é protestante).
  - **Não pode:** matéria sobre a Igreja Católica como instituição (papa, Vaticano, CNBB, dioceses, paróquias, padres, santos, movimentos), fala ou documento católico como fonte, link para site católico e imagem de templo, símbolo ou celebração católica.
  - **Tom:** a comparação mede, não compete. Nada de "vitória", "derrota", "perda de fiéis" ou "corrida"; nenhum juízo sobre a fé católica.
- **Missões, igreja perseguida e evangelização** são da rotina `missoes-comunhao`. Não use as categorias 67595, 116628 e 116627.
- **Política:** sem candidato, partido, pesquisa eleitoral ou intenção de voto. Os políticos evangélicos são da série Fé e Política (`politica-comunhao`). Eleição só entra como **mudança de costume** medida com dado oficial (TSE) ou com pesquisa de comportamento, sempre em tom neutro.
- **Pautas proibidas** da seção 2.1 do padrão valem acima de tudo. Número agregado sobre a situação cadastral das igrejas (CNPJ inapto, por exemplo) pode entrar como pauta de gestão, sem nomear igreja, pessoa ou denominação.

## 2. Horário, grade e categoria

- A tarefa agendada roda por volta das 8h40 (horário de Brasília) e **agenda a matéria para as 9h30** do mesmo dia (`publicar_no_wordpress` com `quando` = "dd/mm/aaaa 09:30"). Se a rodada começar depois das 9h25, publique "agora".
- Descubra o dia com `TZ=America/Sao_Paulo date '+%d/%m/%Y %u'` (`%u`: 1 = segunda … 7 = domingo).

| Dia | Eixo | O que cabe |
|---|---|---|
| Segunda | **Tamanho e lugar** | quantos são, onde estão, estados, cidades, idade |
| Terça | **Movimento** | crescimento, freio, conversão e gerações, projeções |
| Quarta | **Família e comportamento** | casamento, divórcio, Bíblia, livro, música, jovens |
| Quinta | **A igreja por dentro** | CNPJ, idade das igrejas, gestão, pastores, denominações estimadas |
| Sexta | **Datafé explica ou checagem** | método, mito desfeito, número que circula errado, costume que mudou nas eleições |
| Sábado | **A cidade do dia** | um município ou estado com um número que surpreende (rodízio de regiões; o Espírito Santo pelo menos uma vez por mês) |
| Domingo | **O Brasil e o mundo** | um número de fora (Barna, Lifeway, Pew, SBU) posto ao lado de um número brasileiro do Datafé |

- O eixo é preferência. Dado oficial novo no Datafé (carga do CNPJ, Registro Civil, pesquisa nova) passa na frente; registre "eixo trocado".
- **Categoria:** Igreja 6060. Some Ministério 44632 quando o assunto for o pastor e Gestão 16426 quando for gestão da igreja. Nunca Destaques 44517 nem Panorama 1.
- **Chapéu:** "Datafé". **Autor:** "Redação". **Tag obrigatória:** "Datafé" (é por ela e pelo chapéu que a rotina acha o que já saiu).

## 3. Escolha da pauta

1. **O que já saiu:** `listar_materias` com `busca` "Datafé", `portal` 4, últimos 120 dias, `formato` compacto. Nenhuma pauta repete o mesmo fato principal. Um desdobramento só vale com número e ângulo novos.
2. **Vizinhos do dia:** confira as publicações e os agendamentos da Comunhão das últimas 48 horas (`listar_publicacoes` e `listar_agendamentos`, portal 4). A rodada das 13h da rotina `igreja-comunhao` cobre estatísticas, e a matéria mensal `materia-igrejas-abertas-comunhao` sai às 9h nos dias de carga do CNPJ. Se uma delas tratar o mesmo dado, troque de pauta. No dia da matéria mensal, não use CNPJ.
3. **A régua do "não sabia"** (a pauta precisa passar nos quatro):
   - o número surpreende quem acha que conhece a igreja brasileira;
   - cabe numa comparação de escala conferida (seção 5);
   - sustenta uma leitura útil para quem lidera, para a família ou para quem está no banco da igreja;
   - sai do banco do Datafé ou de fonte oficial ou de referência aberta no dia.
4. Use o **banco de pautas** da seção 8 como ponto de partida, no eixo do dia. Pode criar pauta nova com os dados do banco, desde que passe na régua.

## 4. Dados: sempre do dia

Banco do Datafé: projeto Lovable `bd496ff6-6711-470b-aef0-fc1c2b6a611e`, ferramenta `query_database`, **só leitura** (nunca INSERT, UPDATE, DELETE ou DDL). Todo número do texto e da peça é consultado na rodada, mesmo que já esteja nesta skill.

| Assunto | Onde |
|---|---|
| Religião por Brasil, UF, município e idade | `religiao_censo` (ano 2022 ou 2010; `nivel` brasil, uf ou municipio; `faixa_idade` "total" ou grupos de idade; `base` "10_anos_ou_mais") e `v_municipio_religiao` (ranking no Brasil e na UF, variação 2010–2022) |
| Locais de culto (CNEFE 2022) e CNPJ | `mv_templos_municipio` (`origem` cnefe ou cnpj; `religiao`; `denominacao_slug`; `total`; `ativos`). Brasil: some tudo. UF: os dois primeiros dígitos de `codigo_ibge` |
| Aberturas, baixas, idade e situação do CNPJ | `templos_termometro(p_codigo_uf, p_codigo_ibge, p_meses)`, `templos_saldo_anual_resumo()`, `templos_idade_resumo()`, `templos_situacao_resumo()`, `mv_cnpj_aberturas_mes`, `mv_cnpj_baixas_mes` |
| Gerações × conversão | `decomposicao_avanco` (tipo, codigo, p2010, p2022, so_geracoes_2022, pontos_total, pontos_geracoes, pontos_conversao, parte_geracoes_pct) |
| Projeções | `modelo_parametros` e `projecao_geracoes`; os números publicados estão em datafe.com.br/projecoes (a página é feita em JavaScript e o WebFetch só mostra o cabeçalho: leia com `scrape` da `raspagem-web-next` e use o que ela mostra) |
| Denominações 2022 (estimativa com faixa) e 2010 | `denominacoes_2022_estimativa`, `denominacoes_2010`, `declarados` |
| Família | `familia_por_faixa_evangelica()`, `familia_por_uf()`, `registro_civil_uf`, `registro_civil_municipio` |
| Pesquisas e referências | `pesquisas_religiao`, `institutos_vies`, `termometro_pesquisas`, `pesquisas`, `temas_indicadores` (tema, indicador, valor, selo, fonte, url, nota) |
| Mercado e territórios | `mercado_territorios()` |

**Regras dos dados:**
- Toda comparação 2010 × 2022 usa a base de 10 anos ou mais. O percentual nacional é 26,8% (Censo definitivo); o preliminar de 26,9% não se usa.
- **Selo vira texto:** Real → "segundo o Censo 2022 do IBGE" (ou o órgão); Estimativa → "estimativa do Datafé", sempre com a faixa; Referência → "segundo a pesquisa X", com quem fez, quando e como; Declarado → "segundo a própria igreja" ou a entidade.
- Nunca escreva "o Censo 2022 mostra X fiéis da Assembleia de Deus": denominação de 2022 é estimativa do Datafé, com faixa.
- CNPJ não é igreja nova: é organização religiosa registrada. Locais do CNEFE são endereços identificados pelo nome (estimativa): 112 mil endereços religiosos sem pista ficam fora.
- Barna é painel online com cotas, não amostra probabilística: diga isso numa frase. Associação não é causa; membro não é frequentador; venda não é leitura.
- Fonte externa (Pew, Barna, Lifeway, SBB, Inep, IBGE fora do banco, TSE): abra com WebFetch na rodada. Se a página carregar por JavaScript e vier vazia, leia com `scrape` da `raspagem-web-next`; se o WebFetch recusar ou der bloqueio, não raspe. Não abriu, não entra.
- **Raspagem (decisão do Mário Fernando, 17/11/2026):** carregue a `raspagem-web-next` **todo dia**, no começo, siga a seção 1 dela (chaves da memória) e rode `creditos` e `teto 3`. Esta rotina é a sentinela dos créditos: o aviso diário de crédito baixo ou esgotado (seção 5 da `raspagem-web-next`) vai na primeira linha da notificação dela, mesmo quando a matéria não usar a raspagem. Usos: ler páginas do datafe.com.br, conferir a página da barra do fecho e, no domingo (O Brasil e o mundo), `search` dos últimos 30 dias por número novo da Barna, da Lifeway, do Pew ou da SBU.

## 5. Comparações de escala

A comparação é o que faz o leitor sentir o tamanho do número. Use uma, no máximo duas, por matéria.

- **Com coisa que o leitor conhece:** população de estado ou cidade (Censo 2022: SP 44,4 milhões; RJ 16,1 milhões; cidade de São Paulo 11,5 milhões; cidade do Rio 6,2 milhões), escolas de educação básica (Inep, Censo Escolar mais recente: 178,8 mil em 2025), estabelecimentos de ensino (264,4 mil) e de saúde (247,5 mil) no próprio CNEFE 2022.
- **Com o relógio:** "um a cada X minutos" ou "Y por dia" (ex.: 6.525 CNPJs abertos em 2025 = um a cada 80 minutos). Saldo é saldo: diga "a mais", não "novos convertidos".
- **Com a proporção:** "um em cada quatro", "quase o dobro".
- Recalcule na rodada e confira a base da comparação na fonte oficial (WebFetch). Mesmo ano sempre que der; se os anos forem diferentes, diga os dois.
- A comparação nunca muda o sentido do número. Se a conta der "quase", escreva "quase".

## 6. A matéria

**Estrutura (nesta ordem):**

1. **Título** (até 60 caracteres): o número que espanta, já traduzido em escala, ou uma pergunta direta à igreja do leitor. Ex.: "Brasil tem quase duas igrejas evangélicas para cada escola"; "Os jovens estão deixando a sua igreja?".
2. **Linha fina** (uma frase): se o título traz o número, a linha fina faz a pergunta à igreja do leitor; se o título é a pergunta, a linha fina traz o número exato. Ex.: "O Censo contou 339 mil locais de culto, um para cada 139 fiéis. Quantos cabem na sua?".
3. **Abertura** (25 a 70 palavras): a prova, com a fonte e o ano.
4. **Segundo parágrafo:** de onde vem (o Datafé, "o portal de dados da Revista Comunhão") e o contexto mínimo.
5. **Peça do NXtab** (seção 12 do padrão, `marca` "com", `fundo` "none"): logo depois do parágrafo com os dados. Até duas peças. `c-faixa` para três a cinco números-chave; `c-barras` para ranking de estados ou cidades (pode ter "Brasil" como barra de referência, em destaque); `c-percentual` ou `c-colunas` para série no tempo.
6. **Dois intertítulos (h2) com o porquê:** onde o número é maior e menor, o que explica, o que mudou. Um deles leva a palavra-chave.
7. **"Análise: …"** (h2, dois parágrafos): a leitura da Comunhão.
8. **Fecho: a barra do Datafé** (sempre; pedidos de Mário Fernando em 13, 14 e 16/11/2026), logo depois da análise. Ela substitui o fecho antigo (`<hr />` + `<h3>` + "Leia mais"), que não se usa mais. É o bloco abaixo, no mesmo padrão visual das barras do site (navy, fio laranja, Inter, botão dourado), com a marca completa do Datafé em branco (acento de três barras nas cores da marca) e "Evangélicos em números" ao lado:
   ```html
   <div class="nxb-datafe-bloco" style="margin:0;padding:0;"><a class="nxb-barra nxb-card nxb-datafe" data-nxb="datafe" href="{URL}" target="_blank" rel="noopener" aria-label="Datafé: {PERGUNTA}" style="box-sizing:border-box;width:100%;max-width:100%;margin:28px 0;padding:18px 16px 18px 20px;display:flex;align-items:center;gap:14px;background-color:#001C43 !important;background-image:linear-gradient(90deg,#001C43 0%,#00427B 100%) !important;border:0;border-left:6px solid #F58223;border-radius:14px;box-shadow:none;font-family:Inter,system-ui,-apple-system,Arial,sans-serif;text-align:left;text-decoration:none !important;color:#FFFFFF !important;"><span style="flex:1 1 auto;min-width:0;display:block;margin:0;padding:0;"><span style="display:flex;align-items:center;flex-wrap:wrap;gap:4px 10px;margin:0 0 10px;padding:0;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="76 -1635 6242.2 1679" width="89" height="24" role="img" aria-label="Datafé" style="flex:0 0 auto;display:block;width:89px;height:24px;"><path fill="#FFFFFF" d="M649 0H96V-1490H649Q876 -1490 1043.0 -1398.5Q1210 -1307 1301.5 -1140.0Q1393 -973 1393 -745Q1393 -517 1302.5 -350.0Q1212 -183 1045.0 -91.5Q878 0 649 0ZM456 -300H631Q836 -300 933.5 -412.5Q1031 -525 1031 -745Q1031 -965 932.0 -1077.5Q833 -1190 627 -1190H456Z"/><path fill="#FFFFFF" d="M1823.04 18Q1664.04 18 1562.54 -59.5Q1461.04 -137 1461.04 -295Q1461.04 -414 1516.54 -483.0Q1572.04 -552 1665.04 -585.0Q1758.04 -618 1871.04 -627Q2013.04 -639 2071.04 -656.0Q2129.04 -673 2129.04 -721V-726Q2129.04 -773 2089.54 -802.5Q2050.04 -832 1982.04 -832Q1910.04 -832 1867.54 -800.0Q1825.04 -768 1820.04 -714H1500.04Q1511.04 -886 1637.54 -982.5Q1764.04 -1079 1994.04 -1079Q2224.04 -1079 2347.04 -982.5Q2470.04 -886 2470.04 -711V0H2134.04V-148H2130.04Q2083.04 -63 2009.04 -22.5Q1935.04 18 1823.04 18ZM1928.04 -207Q2014.04 -207 2073.04 -254.5Q2132.04 -302 2132.04 -380V-476Q2105.04 -463 2057.04 -453.0Q2009.04 -443 1945.04 -432Q1876.04 -421 1831.54 -392.0Q1787.04 -363 1787.04 -311Q1787.04 -262 1826.04 -234.5Q1865.04 -207 1928.04 -207Z"/><path fill="#FFFFFF" d="M3286.08 -1056V-790H3069.08V-355Q3069.08 -304 3089.08 -285.0Q3109.08 -266 3167.08 -266H3286.08V0H3091.08Q2901.08 0 2812.58 -71.5Q2724.08 -143 2724.08 -297V-790H2544.08V-1056H2724.08V-1344H3069.08V-1056Z"/><path fill="#FFFFFF" d="M3721.12 18Q3562.12 18 3460.62 -59.5Q3359.12 -137 3359.12 -295Q3359.12 -414 3414.62 -483.0Q3470.12 -552 3563.12 -585.0Q3656.12 -618 3769.12 -627Q3911.12 -639 3969.12 -656.0Q4027.12 -673 4027.12 -721V-726Q4027.12 -773 3987.62 -802.5Q3948.12 -832 3880.12 -832Q3808.12 -832 3765.62 -800.0Q3723.12 -768 3718.12 -714H3398.12Q3409.12 -886 3535.62 -982.5Q3662.12 -1079 3892.12 -1079Q4122.12 -1079 4245.12 -982.5Q4368.12 -886 4368.12 -711V0H4032.12V-148H4028.12Q3981.12 -63 3907.12 -22.5Q3833.12 18 3721.12 18ZM3826.12 -207Q3912.12 -207 3971.12 -254.5Q4030.12 -302 4030.12 -380V-476Q4003.12 -463 3955.12 -453.0Q3907.12 -443 3843.12 -432Q3774.12 -421 3729.62 -392.0Q3685.12 -363 3685.12 -311Q3685.12 -262 3724.12 -234.5Q3763.12 -207 3826.12 -207Z"/><path fill="#FFFFFF" d="M5196.16 -1056V-790H4979.16V0H4634.16V-790H4442.16V-1056H4634.16V-1173Q4634.16 -1334 4724.66 -1412.0Q4815.16 -1490 5004.16 -1490H5196.16V-1224H5091.16Q5030.16 -1224 5004.66 -1198.5Q4979.16 -1173 4979.16 -1113V-1056Z"/><path fill="#FFFFFF" d="M5771.2 24Q5609.2 24 5486.7 -47.0Q5364.2 -118 5295.7 -242.5Q5227.2 -367 5227.2 -528Q5227.2 -689 5295.7 -813.5Q5364.2 -938 5485.2 -1009.0Q5606.2 -1080 5762.2 -1080Q5921.2 -1080 6041.7 -1010.5Q6162.2 -941 6230.2 -818.5Q6298.2 -696 6298.2 -536V-443H5563.2Q5566.2 -342 5623.7 -283.0Q5681.2 -224 5783.2 -224Q5859.2 -224 5910.7 -255.0Q5962.2 -286 5981.2 -338H6290.2Q6271.2 -232 6198.2 -150.0Q6125.2 -68 6014.7 -22.0Q5904.2 24 5771.2 24ZM5565.2 -649H5977.2Q5965.2 -732 5911.2 -779.0Q5857.2 -826 5771.2 -826Q5684.2 -826 5630.2 -779.0Q5576.2 -732 5565.2 -649Z"/><path fill="#FFC220" d="M5487.7 -1175H5657.7V-1375H5487.7Z"/><path fill="#FAA221" d="M5707.7 -1175H5877.7V-1495H5707.7Z"/><path fill="#F58223" d="M5927.7 -1175H6097.7V-1615H5927.7Z"/></svg><span style="display:block;margin:0;padding:0;color:#FFC220 !important;font-size:12px;line-height:1.2;font-weight:700;letter-spacing:0.2px;">Evangélicos em números</span></span><span style="display:block;margin:0;padding:0;color:#FFFFFF !important;font-family:Inter,system-ui,-apple-system,Arial,sans-serif;font-size:17px;line-height:1.3;font-weight:700;letter-spacing:-0.2px;overflow-wrap:break-word;">{PERGUNTA}</span><span style="display:block;margin:6px 0 0;padding:0;color:#C9D6E8 !important;font-size:14px;line-height:1.4;font-weight:400;overflow-wrap:break-word;">{PROMESSA}</span></span><span style="flex:0 0 auto;display:flex;align-items:center;justify-content:center;width:44px;height:44px;margin:0;padding:0;border-radius:50%;background:#FFC220;background:linear-gradient(135deg,#FFC220 0%,#F58223 100%);color:#001C43;"><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false" style="display:block;"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></span></a></div>
   ```
   - Troque só `{URL}`, `{PERGUNTA}` (aparece duas vezes: no `aria-label` e no título) e `{PROMESSA}`. Não mexa em estilos, cores, na marca nem em "Evangélicos em números" (só a inicial maiúscula, nunca tudo em caixa alta).
   - **Uma linha só:** a barra vai inteira numa linha, sem quebra dentro. Com quebra de linha, o WordPress enfia `<p>` e `<br>` no meio e a barra desmonta.
   - **Texto:** `{PERGUNTA}` com até 80 caracteres; `{PROMESSA}`, uma frase de até 110 caracteres com o que o leitor vai achar no Datafé. Escreva `"` como `&quot;` e `&` como `&amp;`.
   - Depois de `criar_materia`, confira com `ver_materia` (formato html) que a barra chegou inteira e numa linha.
   - **A pergunta da barra é genérica** (pedido de Mário Fernando, 16/11/2026): fala com qualquer leitor, em "você", "sua cidade", "sua igreja", sem chamar um grupo (nada de "Pastor,", "Líder," ou "Jovem,"). É diferente da pergunta do título ou da linha fina. Padrão: "Você conhece os números da igreja evangélica na sua cidade?". Varie só quando o eixo combinar melhor: igrejas ("Quantas igrejas evangélicas existem na sua cidade?"), ranking ("Em que posição a sua cidade está no ranking?"), checagem ("Antes de repassar aquele número no WhatsApp, você conferiu o oficial?"), movimento ("Como estará a igreja da sua cidade em 2030?"), família ("Na sua cidade, casa-se mais ou menos que a média?").
   - O link vai para a página que responde à pergunta: https://datafe.com.br/municipios (busca da cidade), /templos, /igrejas-abertas, /projecoes, /denominacoes, /pesquisas, /familia, /movimento, /biblia-e-livro, /musica-gospel, /mercado, /estados, /estado/<slug> ou /municipio/<slug>. Confira que a página abre e mostra conteúdo: no WebFetch só aparece o cabeçalho (o site é feito em JavaScript), então leia com `scrape` da `raspagem-web-next` (1 crédito); sem crédito, basta o título da página no WebFetch. Se não abrir, use https://datafe.com.br.
   - A barra não conta como intertítulo para a Nota SEO. Um aviso de "trecho sem intertítulo" no fim do texto é aceitável se a nota ficar em 85 ou mais.
   - O plugin nx-relacionados do WordPress põe barras automáticas no texto ("Ouça", "Leia também") e pode pôr uma logo acima da barra do Datafé. Isso se resolve no plugin (pedido ao Jhonatan em 16/11/2026); não tente tirar pelo texto da matéria.
   - Quando a pauta tiver recorte por cidade ou estado, ponha também, logo depois da peça do NXtab, uma linha curta: `<p><em>Procure a sua cidade no <a href="https://datafe.com.br/municipios">Datafé</a>.</em></p>`.
9. **"Como medimos"** (um parágrafo em itálico): fonte, ano, recorte, o que é estimativa e o que ficou de fora.
10. **Rodapé:** `<p><em>Com informações de [órgãos de origem dos dados]</em></p>`.

**Tamanho:** 500 a 750 palavras.

**A chamada provocativa (pedido de Mário Fernando, 14/11/2026):**
- Toda matéria fala diretamente com a igreja do leitor em dois lugares: no título ou na linha fina, e no fecho. Use "sua igreja", "sua cidade", "sua denominação", "o pastor da sua igreja", "os jovens da sua igreja".
- A pergunta nasce do número do dia, e o texto responde com dado. Nada de pergunta que acusa, que promete o que o Datafé não mede ou que o texto não sustenta.
- Modelos para adaptar ao dado do dia (reconsulte os números):
  - Quantas vidas se converteram na sua igreja no último ano? (saldo de 2010 a 2022: menos de duas pessoas por igreja por ano, além do que nascimentos e mortes explicam; estimativa do Datafé)
  - Os jovens estão deixando a sua igreja? (31,6% dos adolescentes de 10 a 14 anos são evangélicos; entre os de 20 a 24, 27,5%; o Censo mede religião declarada, não frequência, e o texto diz isso)
  - Sua igreja está pronta para cuidar da terceira idade? (7 milhões de evangélicos com 60 anos ou mais, 14,8% dos evangélicos)
  - Quantas igrejas evangélicas existem na sua cidade? / Sua igreja é grande ou pequena para o seu estado?
  - Qual o tamanho da sua denominação? (estimativa de 2022, com faixa)
  - O pastor da sua igreja pensa em desistir? (Barna e Lifeway, dos EUA, como espelho; no Brasil ninguém mediu)
  - Na sua cidade, casa-se mais ou menos que a média? / Como estará a igreja da sua cidade em 2030?
- Barna e Lifeway são dos Estados Unidos: entram como espelho, nunca como medida do Brasil. O Pew tem recorte brasileiro.

**A análise (opinião com régua):**
- Fala do significado do número para a igreja e para o país: o que ele pede de quem lidera, da família, da sociedade. Alterne o tom pastoral (provoca a liderança a agir) e o de cronista (explica o Brasil), conforme a pauta.
- **Opinião no significado, nunca no número.** Não force o dado para caber na tese. Não afirme fato que o dado não mostra; quando for leitura, escreva como leitura ("os números sugerem", "a pergunta que fica").
- O dado incômodo entra (previsão que errou, igreja inapta, pastor sem dado), sempre com respeito e em tom de serviço, sem culpado.
- Termine com uma provocação concreta para quem lidera, diferente da pergunta do fecho.
- Sem adjetivo de propaganda, sem "explosão", "boom", "crise"; sem partido, candidato ou ataque a pessoa ou igreja.
- Citação bíblica só se ajudar de verdade, curta, na NTLH (seção 7 do padrão).

**SEO:** palavra-chave de 2 a 4 palavras (ex.: "igrejas evangélicas", "evangélicos no Brasil"); título SEO começando por ela; meta description ≤ 155 caracteres só com números do texto; slug ≤ 51; 6 a 10 tags, sempre com "Datafé". Nota ≥ 85 (seção 8 do padrão).

**Imagem destacada:** seção 9 do padrão. NX Fotos primeiro (`buscar` com termos como "igreja evangélica culto", "fachada igreja evangélica", "Bíblia", "família igreja"); foto real que mostre a igreja evangélica, o culto ou o tema, com "imagem ilustrativa" e "foto de arquivo" na descrição quando for o caso. Nunca templo, símbolo ou celebração católica. A descrição não afirma o que o texto não prova. Original maior que o WordPress aceita: reduza para 2.000 px de largura, trate (9.3) e suba ao Studio.

## 7. Publicação e resumo

1. `criar_materia` (portal 4, categoria da seção 2, chapéu "Datafé", autor "Redação") → peças do NXtab enviadas ao Studio e postas no texto → `definir_imagem_destacada` → `ver_nota_seo`.
2. Reconferência de duplicidade (seção 4 do padrão) → `conferir_publicacao` → `publicar_no_wordpress` com `quando` 09:30 do dia (ou "agora", seção 2) e o `codigo_confirmacao` (a decisão de Mário Fernando de 13/11/2026 vale como o "sim").
3. Nada de redes antes de a matéria ir ao ar (2.2 do padrão). Feed do Instagram nunca (2.3). O story automático do NX Feed segue a cota do canal.
4. **Resumo** (seção 10 do padrão), título "Datafé · matéria do dia · DD/MM": título com link (ou horário em que vai ao ar), eixo do dia, o "não sabia" em uma linha, a pergunta da chamada e a do fecho, as peças do NXtab, a foto, a linha da raspagem quando usada (seção 6 da `raspagem-web-next`) e Pendências.

## 8. Banco de pautas (ponto de partida)

Marque no resumo qual pauta foi usada. Números abaixo são do levantamento de 13/11/2026: **reconsulte todos** na rodada.

**Tamanho e lugar**
- Há mais evangélicos de 10 anos ou mais no Brasil (47,3 milhões) do que gente no estado de São Paulo (44,4 milhões).
- A igreja é mais jovem que o país: 31,6% dos brasileiros de 10 a 14 anos são evangélicos, contra 18,9% dos de 80 anos ou mais (`religiao_censo` por faixa de idade).
- As 58 cidades de maioria evangélica; Arroio do Padre (RS) lidera com 88,7%.
- Acre, 44,8%: o estado mais evangélico do país. O ranking dos estados.
- A cidade mais evangélica do Espírito Santo, Santa Maria de Jetibá (73,5%, 3ª do Brasil), tem raiz pomerana e luterana.
- A Assembleia de Deus sozinha tem o tamanho do estado do Rio (estimativa de 17,3 milhões, faixa de 15,3 a 17,5 milhões).
- *Usada em 13/11/2026:* quase duas igrejas evangélicas para cada escola (339.281 locais; 139 fiéis por local).

**Movimento**
- Cerca de 1.700 brasileiros a mais por dia viraram evangélicos de 2010 a 2022, além do que a demografia explica (saldo; `decomposicao_avanco`, estimativa).
- A previsão mais repetida da década errou por cerca de 9 milhões de pessoas: previa 31,8% em 2022; o Censo mediu 26,8%.
- O Brasil evangélico de 2050 tende a ser um terço, não metade: 33,4% no cenário central (30,6% com freio forte e 41,6% no ritmo de 2010–2022).
- No Rio, no ES e no DF, quase metade do avanço veio do berço; no Acre, no Maranhão e no Tocantins, quase tudo de conversão.
- De 58 para cerca de 137 cidades de maioria evangélica em 2030 (faixa de 119 a 183).
- Um novo CNPJ de igreja evangélica a cada 80 minutos em 2025 (não usar na semana da matéria mensal do CNPJ).
- De 38 mil para 130 mil CNPJs evangélicos entre 2010 e 2022: quanto é igreja nova e quanto é formalização.

**Família e comportamento**
- Nas cidades com 35% a 50% de evangélicos, casa-se 66% mais do que nas com menos de 15% (associação, não causa).
- Casamentos caíram 14% em dez anos; divórcios foram de 31 para 45 a cada 100 casamentos.
- Uma Bíblia completa vendida a cada 9 segundos: o Brasil foi o 1º do mundo em 2025 (SBB/SBU, declarado).
- O livro cristão caiu quatro vezes e meia menos que o mercado editorial de 2016 a 2025 (CBL/SNEL).
- O que a igreja ouve: música gospel nas plataformas (`temas_indicadores`, tema musica-gospel).

**A igreja por dentro**
- Uma em cada cinco igrejas com CNPJ está inapta na Receita (32.755): pauta de gestão, sem nomes.
- Uma em cada quatro igrejas com CNPJ ativo tem menos de cinco anos; metade abriu depois de agosto de 2015.
- Ninguém sabe se o pastor brasileiro está esgotado: nos EUA, 24% pensaram em deixar o ministério (Barna) e 1,2% deixam por ano (Lifeway). O Brasil não tem série.
- Quanto pesa cada denominação em 2022 (estimativa com faixa) e quanto ela mudou desde 2010.
- Quase três locais de culto para cada CNPJ: como as igrejas se organizam em campos e congregações (Pará 8,9; São Paulo 1,6).

**Datafé explica ou checagem**
- Os 35,8% de evangélicos que circulam na imprensa não se sustentam: o número partia de 32,1% em 2022; o Censo mediu 26,8%.
- Quais institutos medem bem os evangélicos nas pesquisas de religião (viés contra o Censo; nunca intenção de voto).
- Por que o IBGE não publicou números por igreja em 2022 (nota metodológica 06/2026) e como o Datafé estima.
- O que muda quando se conta "10 anos ou mais".
- O "pastor" saindo do nome de urna: só com a proporção calculada a partir da base de candidaturas do TSE (2022 × 2026). Enquanto essa base não estiver no Datafé, fica no banco.
- Influência do líder religioso no voto declarada pelos evangélicos (Datafolha, pesquisa de comportamento, sem candidato).

**O Brasil e o mundo**
- Geração Z nos EUA voltou a ler a Bíblia (Barna, painel online) — e o que se sabe do jovem evangélico brasileiro.
- Quantos pastores deixam o ministério por ano nos EUA (Lifeway) e por que o Brasil não sabe o seu número.

**Comparações com os católicos (liberadas em 13/11/2026; regras da seção 1)**
- Para cada local de culto católico, há três e meio evangélicos (96.072 contra 339.281 no CNEFE 2022). Cada local católico atende em média cerca de mil fiéis de 10 anos ou mais; cada local evangélico, 139. Mesmo que os 112 mil endereços religiosos sem pista no nome fossem todos católicos, seriam 480 por local, mais de três vezes a média evangélica.
- Quando os evangélicos passam os católicos: no ritmo de 2010–2022, só em 2047; com o freio dos últimos 12 anos, não passam até 2050 (cenário central). Nos estados, o Acre já passou em 2022; no cenário central vêm Rondônia (2023), Roraima (2024), Amazonas (2028), Amapá e Rio de Janeiro (2033) e Pará (2043).
- Cerca de um em cada oito adultos brasileiros (13%) foi criado católico e hoje é protestante; outros 7% foram criados católicos e hoje não têm religião (Pew 2024; os percentuais são sobre todos os adultos).