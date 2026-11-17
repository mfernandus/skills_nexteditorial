---
name: "padrao-publicacao-next"
description: "Regras comuns das rotinas que publicam nos sites ES Brasil e Comunhão via NX Feed (publicação, pautas proibidas, matéria agendada, feed só manual, duplicidade, fontes, direitos, SEO, imagem e avisos). Carregar antes de cada rotina; gráficos, republicação e imagem por IA ficam nas skills de apoio."
---

# Padrão de publicação Next — ES Brasil e Comunhão

Regras que valem para **toda** rotina de conteúdo dos sites (turno noturno, Estilo, esporte, Panorama e as que vierem). Cada rotina carrega esta skill primeiro e traz só o que é dela: pauta, rodadas, tetos, categorias e o título do resumo. Onde a rotina disser algo diferente, vale a rotina naquele ponto, **salvo as seções 2.1 (pautas proibidas), 2.2 (matéria agendada), 2.3 (feed do Instagram só manual), 12 (gráficos e tabelas no NXtab) e 13 (dados atualizados na republicação) e a regra de caixa alta da seção 7, que valem acima de qualquer rotina e de qualquer tarefa agendada**. Onde uma rotina ainda pedir chapéu "em maiúsculas", escreva em caixa alta e baixa. A seção 11 (economia do plano) vale como padrão para todas: a rotina só a contraria quando disser expressamente que precisa do contrário naquele ponto. **Mudança de regra comum se faz só aqui** (e nas skills de apoio abaixo).

**Skills de apoio** (economia do plano, decisão do Mário Fernando de 17/11/2026). Partes deste padrão que nem toda rodada usa ficam em skills próprias, carregadas só quando a rodada precisa delas, uma vez por execução (11.7). Valem com a mesma força que se estivessem aqui:
- **`dados-e-graficos-next`** (seções 12 e 13): carregue antes de montar qualquer tabela, gráfico ou infográfico e, sempre, nas rotinas de republicação (`acervo-esbrasil`, `acervo-comunhao`, `artigos-acervo-esbrasil`, `artigos-acervo-comunhao`, `artigos-acervo-next`).
- **`imagem-ia-next`** (9.1 e 9.2): carregue só quando nenhuma foto real com direito de uso servir, antes de gerar a imagem.
- **`raspagem-web-next`** (busca e leitura de páginas pelo Firecrawl, com o Apify de reserva; decisão do Mário Fernando de 17/11/2026): carregue só nas rotinas que a citam. A seção 3 dela (o que nunca se raspa) vale acima de qualquer rotina, e a seção 5 diz quando avisar que os créditos estão baixos ou acabaram.

## 1. Portais e idioma

- NX Feed: **ES Brasil = portal 1** (esbrasil.com.br); **Comunhão = portal 4** (comunhao.com.br).
- Português do Brasil. Ao citar a revista, **ES Brasil** em negrito (no resumo também).
- Execução agendada não tem ninguém acompanhando: não faça perguntas. Na dúvida, tome a decisão mais conservadora e registre no resumo.

## 2. Publicação direta (decisão do Mário Fernando, 26/10/2026)

- Tudo o que a rotina produz vai ao ar sozinho, sem fila de aprovação e sem esperar "sim", inclusive política eleitoral (tom neutro, só com base em agência ou fonte oficial). Os gestores recebem o aviso e corrigem depois; a conferência pós-publicação é da Joviana, da Elisângela, do Mário ou de quem eles delegarem.
- Confirmação dupla do NX Feed: a primeira chamada devolve um `codigo_confirmacao`; repita a chamada com **os mesmos dados e o código**. Esta decisão vale como o "sim".
- Problema de SEO, foto ou texto se resolve na própria rodada e a matéria vai ao ar.
- **Só não publica:** pauta proibida (2.1), duplicado (a casa já tem o fato), superado (fato velho sem valor, pré-jogo de partida já encerrada), dado sem fonte oficial confirmada ou erro técnico do NX Feed. Esses vão para o resumo com o motivo.
- Fluxo: `conferir_publicacao` (tipo publicar) → `publicar_no_wordpress`. Uma matéria por vez. Quando a rotina pedir agendamento, a primeira sai "agora" e as seguintes de 15 em 15 minutos.

## 2.1 Pautas proibidas (decisão do Mário Fernando, 28/10/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada; nenhuma pode afrouxá-la.** Nenhuma rotina publica, aproveita de agência ou atualiza matéria destes três tipos. Vale também para matéria que a equipe publicou: a rotina não a escolhe para o Instagram, não lhe dá categoria de Panorama e não acrescenta atualização.

1. **Denúncia.** O fato principal é acusação, suspeita, investigação ou apuração de irregularidade, crime, fraude, corrupção, desvio, improbidade ou má conduta contra pessoa, empresa, entidade, igreja ou órgão público. Entram aqui: operação policial contra alvo determinado; prisão ou indiciamento por esse tipo de caso; ação judicial que acusa alguém; denúncia de leitor, de entidade, de sindicato ou de parlamentar; reportagem de outro veículo que "revela" irregularidade. Na Justiça Desportiva, só o resultado do julgamento (punição decidida), nunca a denúncia da procuradoria.
2. **Aumento de tarifa.** Aumento ou reajuste de tarifa de serviço público ou concessionado: energia elétrica (inclusive bandeira tarifária), água e esgoto, gás canalizado, pedágio e transporte coletivo. Redução ou manutenção de tarifa pode entrar.
3. **Origem em órgão de controle.** Matéria que nasce de Ministério Público (MPF, MPES e demais estaduais, MPT, MP de Contas), de Tribunal de Contas (TCU, TCE-ES e demais) ou de controladoria (CGU e controladorias estaduais e municipais): ação, recomendação, inquérito, denúncia, auditoria, parecer, julgamento de contas, operação ou release. Esses órgãos também não servem de fonte para outras matérias.
   - **Única exceção: TCE-ES na rotina `politica-esbrasil`** (decisão do Mário Fernando, 05/11/2026). Só essa rotina, e só com notícia boa e importante do Tribunal de Contas do Espírito Santo: posse ou eleição de presidente e conselheiros; programa, capacitação ou ferramenta oferecida ao Estado ou aos municípios; prêmio, selo ou ranking positivo de gestão ou transparência (só o lado de quem foi bem); parecer ou decisão pela aprovação das contas do governador ou de prefeito, sem ressalvas; acordo de cooperação com outro poder. "Importante" = afeta o Estado ou vários municípios, envolve parceiro ou é marco institucional; curso ou evento de rotina fica fora. **Nunca:** auditoria, fiscalização, irregularidade, multa, rejeição de contas, ressalva, cautelar, suspensão de licitação, alerta ou recomendação a gestor, ranking de quem foi mal. MP, controladorias, TCU e os demais tribunais de contas continuam fora, e nenhuma outra rotina usa esta exceção.

Na dúvida se o assunto se encaixa, não publique. Registre no resumo, em "Também na rodada", com o título e a marca "fora por regra de pauta".

## 2.2 Matéria agendada só existe quando vai ao ar (decisão do Mário Fernando, 30/10/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada, como a 2.1.** Matéria agendada no WordPress, pela equipe ou por uma rotina, ainda não está no ar: o leitor não a vê e o link dela não abre. Até a hora em que ela vai ao ar (`vai_ao_ar`):

1. **Nenhuma rede social.** Não crie arte, story, post, carrossel ou reels dela. Não aprove, não agende e não publique nada dela no Instagram, no Facebook ou em outra rede, nem a mande ao WhatsApp. Vale também para a matéria que a própria rotina acabou de agendar.
2. **Conteúdo de rede que já existe** (o NX Feed cria story ou post sozinho, com o Claude pela API, na hora em que a matéria é agendada): não mande "publicar agora" e não ponha horário antes do `vai_ao_ar`. O horário certo é o do `vai_ao_ar` ou depois. Se a matéria foi reagendada, o conteúdo de rede vai junto para o novo horário. Nunca escreva em nota, legenda ou resumo que o conteúdo deve sair "antes" da matéria.
3. **Nenhuma mexida em matéria agendada da equipe.** Não a publique "agora", não mude o horário, não a reenvie (`publicar_no_wordpress`, `atualizar_no_wordpress`, `enviar_rascunho_ao_wordpress`), não a edite (`editar_materia`, `definir_imagem_destacada`), não lhe dê Destaques nem Panorama e não a use como link interno.
4. **Na trava de duplicidade ela conta** (seção 4): a casa já tem o fato, então não escreva sobre o mesmo assunto.

**Como reconhecer.** Em alguns lugares o NX Feed trata "enviada ao WordPress" como "publicada":
- `materias_para_instagram` lista como publicada a matéria só agendada (`publicada_em` = hora do envio). Antes de usar qualquer item dela, rode `listar_agendamentos` do portal (de agora até 7 dias, todas as páginas) e descarte todo `materia_id` que aparecer ali. Depois confirme que o item está em `listar_publicacoes` com situação "publicado".
- Link com `?p=` (ex.: esbrasil.com.br/?p=417326) no lugar do endereço com o slug: trate como agendada.
- `listar_materias` com `estado` = publicado já deixa as agendadas de fora (elas têm `estado` = agendado). `listar_publicacoes` mistura as duas: filtre `situacao` = publicado.

Na dúvida, fica fora. Registre no resumo, em "Também na rodada", como "aguardando ir ao ar (DD/MM HHh)".

## 2.3 Feed do Instagram só com conteúdo manual (decisão do Mário Fernando, 10/11/2026)

**Esta seção vale acima de qualquer rotina e de qualquer tarefa agendada, como a 2.1 e a 2.2.** Nenhuma rotina automática posta no feed da **ES Brasil** (conta 7, @revistaesbrasil) nem da Comunhão (conta 6, @oficialcomunhao). Post de feed é só da equipe, feito à mão.

1. **Nada de feed.** Não crie, não aprove, não agende e não publique post de feed, carrossel ou reels, nem como rascunho ou para revisão: nada de `criar_arte_de_noticia` ou `criar_post_instagram` com formato ou tipo de feed, nada de `revisar_post_instagram` com "aprovar" em post de feed, nada de `publicar_post_instagram` com destino "feed". Vale também para o Facebook.
2. **Não escolha matéria para o feed.** `materias_para_instagram` não serve para montar post de feed.
3. **Feed que já está no Studio** (da equipe ou de rotina antiga): não mexa. Não aprove, não edite, não cancele e não apague.
4. **Stories continuam** como cada rotina define: o story automático que o painel do NX Feed cria quando a matéria vai ao ar, o story dos artigos do acervo para revisão e o stories animado da previsão do tempo. Esta seção trata só do feed. Antes de criar story, confira a fila do dia do canal no Studio (`listar_posts_instagram`): se a cota diária de stories daquele canal já estiver cheia, a matéria fica só no site e o resumo registra "story fora: cota do dia cheia".
5. Se uma rotina ou tarefa agendada ainda mandar fazer post de feed, ignore esse trecho e registre no resumo: "feed do Instagram: só manual desde 10/11".

## 3. NX Feed: cuidados de uso

- Carregue as ferramentas com ToolSearch e faça **uma chamada de cada vez** (códigos de confirmação pedidos em paralelo se invalidam).
- Erro 429 ou aviso de espera: espere o tempo indicado e repita a mesma chamada. Não pule o item por isso.
- Os filtros de `categoria` e `estado` de `listar_materias` não separam portais (os ids colidem): nas listagens de publicadas, passe sempre `portal`.
- Rascunho que ainda não foi ao WordPress não tem portal: busque rascunhos **sem** filtro de portal e confira o destino com `ver_materia`.
- `editar_materia` com "categorias" **substitui as categorias de todos os portais**: leia antes com `ver_materia` (pegue a `versao`) e mande as categorias de todos os portais já com a mudança. Ao reenviar, passe `portais` só com os portais em que a matéria já tem post (senão o NX Feed cria rascunho no outro).
- Para atualizar um post no ar sem mudar o status: `enviar_rascunho_ao_wordpress` (ou `atualizar_no_wordpress` num portal só).
- Mexa só nas matérias da própria rotina (criadas ou editadas via Claude; `historico_da_materia` mostra), nunca nos rascunhos da equipe, a não ser que a rotina diga o contrário. Matéria agendada da equipe nunca: seção 2.2.
- Id de categoria recusado: rode `listar_categorias_wordpress` no portal, use o id atual da **mesma** categoria e avise no resumo. Nunca grave em categoria aproximada.
- **Destaques** (11966 na ES Brasil, 44517 na Comunhão) é da redação e só das rotinas que o tratam expressamente, cada uma pela sua regra (decisões do Mário Fernando de 30/10, 02/11, 05/11 e 12/11/2026): a **rotina de Destaques**, as **rotinas de acervo** (matéria das 22h), a **`comunhao-na-esbrasil`** (sábado, domingo e feriado) e a da **previsão do tempo** (Post A das 00h01). Nenhuma outra rotina, nem a de esporte, marca ou tira Destaques.

## 4. Trava de duplicidade

Duas etapas, para conferir tudo sem repetir conferência:

**Antes de escrever:**

1. O que já foi ao ar no portal (`listar_publicacoes` ou `listar_materias` publicadas, com `portal`), na janela que a rotina indicar. Uma listagem por rodada serve para todas as pautas.
2. Rascunhos (`estado` = rascunho e depois rascunho_no_wp), sem filtro de portal. Também uma vez por rodada.
3. Por pauta: `listar_materias` com `busca` pelo fato, pessoa, empresa, órgão ou time (todos os estados) e WebSearch `site:<domínio do portal> <tema>`.

**Imediatamente antes de publicar** (por matéria): `listar_publicacoes` do portal desde a primeira conferência e de novo `listar_materias` com `busca` pelo fato (todos os estados). Não é preciso repetir o WebSearch `site:`: o buscador leva horas para indexar e não mostra o que entrou nos últimos minutos.

Se a casa já tem o mesmo fato, publicado ou em rascunho da equipe, não escreva: troque por **outro assunto do mesmo tema** (outro dado, outra empresa, outro município, desdobramento realmente novo) ou registre "coberto pela equipe". Nunca publique o item de feed **e** uma matéria manual sobre o mesmo fato.

## 5. Fontes e apuração

- A fonte oficial ou primária (órgão público, entidade, documento, release no site da própria empresa, dado público) é a fonte de verdade. Órgão de controle (Ministério Público, Tribunal de Contas, controladoria) não serve de fonte (2.1), salvo o TCE-ES na exceção da rotina `politica-esbrasil`, e só na própria matéria do TCE-ES. Abra com WebFetch antes de escrever; nunca redija a partir de snippet. Fonte que não abre: procure outra ou troque a pauta. Não use curl, Python, Firecrawl ou Apify para burlar página bloqueada (`raspagem-web-next`, seção 3).
- Imprensa serve só de pista e de conferência. **Não dê crédito a outro veículo:** não cite, não linke, não escreva "segundo o jornal X". A atribuição vai para a fonte oficial.
- Agências contratadas que chegam no NX Feed (Agência Brasil, Estadão Conteúdo e as demais cadastradas) podem ser aproveitadas, com o crédito no rodapé.
- O que só existe no outro veículo (entrevista exclusiva, levantamento próprio, bastidor) não entra. Se o fato depende disso, troque a pauta.
- **Comunhão: nenhum veículo do Espírito Santo** (pedido da Joviana, repassado pelo Mário Fernando, 16/11/2026). Matéria da Comunhão não menciona veículo jornalístico capixaba de fora da casa (A Gazeta, Folha Vitória, ES Hoje, A Tribuna/Tribuna Online, Século Diário, TV Gazeta, TV Vitória, TV Tribuna, CBN Vitória e afins) em lugar nenhum: texto, rodapé "Com informações de", link, legenda ou crédito, nem como "reproduzido por". Vale também quando o site capixaba só republicou agência nacional (Folhapress, Estadão Conteúdo, Agência Brasil): vá à fonte primária ou à agência no original e atribua a ela. Personagem ou entrevista que só existe nessa reportagem não entra; troque por dado ou serviço da fonte oficial. **Única exceção:** factual urgente (acidente, tragédia, desastre, alerta de chuva ou da Defesa Civil, emergência) quando o veículo capixaba é a única fonte disponível do fato naquele momento; assim que a fonte oficial (Defesa Civil, Bombeiros, PRF, Sesa, prefeitura) publicar, a atribuição passa para ela.
- Dado que não bate: vale o oficial. Dado que não deu para confirmar: fica de fora e vai para o resumo.
- Nunca invente fala, número ou data. Citação só quando a fonte a publicou, curta e atribuída.
- Na apuração, guarde um ou dois dados conferidos que **não** vão entrar no texto: se a matéria acabar com imagem por IA, um deles vira a legenda-fato (9.2).

## 6. Direitos autorais

- Texto sempre próprio ou de agência contratada com crédito. Reescreva com estrutura e palavras próprias; nunca copie nem traduza parágrafos de outro veículo; não siga a ordem, o título nem as frases da matéria que serviu de pista.
- Foto só com direito de uso: acervo da casa (NX Fotos, ES Brasil, Comunhão), Agência Brasil, Fotos Públicas ou divulgação oficial com crédito visível (governo, prefeitura, empresa, entidade, clube, federação, liga).
- **Proibido:** Reuters, AFP, AP, Getty, Zimel/Estadão, USA Today/Imagn, Shutterstock/iStock/Freepik achados na web, Pinterest, Instagram de terceiros, "Reprodução" sem dono, foto de jornal ou de outro veículo, Google Imagens sem dono e licença claros. Item da Agência Brasil com `imagem_reuters` = true: troque a foto.
- Na dúvida sobre o direito de uso, não use a foto: vá para a imagem por IA (9.1).

## 7. Padrão do texto (comum a todas)

- Autor "Redação" (ou o crédito da agência, quando o item é aproveitado).
- **Nada em caixa alta** (decisão do Mário Fernando, 11/11/2026: caixa alta é gritar). Chapéu, título, linha fina, intertítulo, tags, legenda e texto de arte saem em caixa alta e baixa, ex.: chapéu "Identidade visual", nunca "IDENTIDADE VISUAL". Maiúscula inteira só em sigla (ES, Secom, IBGE) ou dentro de aspas, na fala de alguém que foi dita ou escrita assim.
- **Título até 60 caracteres, contando espaços**, informativo, com a palavra-chave de preferência no início. Se passar, corte o acessório e leve o complemento para a linha fina (uma frase).
- Abertura de 25 a 70 palavras respondendo ao título (o quê, quem, quando, onde).
- Um link externo para a fonte oficial: `<a href="..." target="_blank" rel="noopener">`. Links internos para matérias do próprio portal, quando houver.
- Rodapé: `<p><em>Com informações de [fonte]</em></p>`.
- Datas como "neste domingo (25)", nunca "ontem" ou "hoje". Confira no calendário o dia da semana de toda data. Valores com a unidade da fonte.
- Política: tom neutro, sem adjetivos, mesmo espaço aos lados; em eleição, só números oficiais (TRE-ES/TSE) e nada de pesquisa avulsa.
- Saúde e pet: sem dose nem prescrição; oriente a procurar o profissional.
- **Bíblia (vale para toda rotina da Comunhão e para qualquer rotina que cite a Bíblia):** Toda citação bíblica escrita pela redação sai **sempre na NTLH** (Nova Tradução na Linguagem de Hoje; decisão de Mário Fernando, 2/11/2026), conferida palavra por palavra no NEIA com `get-bible-passage` e `bible_code` "NTLH". Nunca ACF, ARC, ARA, NVI, NVT ou outra versão no texto da redação, mesmo que o original ou a fonte tragam: troque pelo texto da NTLH do mesmo versículo e registre no resumo. **Quando quem cita é uma pessoa** (fala, entrevista, depoimento, texto de articulista ou de autor convidado) e ela usou outra versão, fica a versão dela; só a forma da referência é padronizada. Confira também se a referência bate com o episódio citado. Formato da casa: citação curta, entre aspas, com a referência entre parênteses depois, ex.: "Porém a maior delas é o amor" (1 Coríntios 13.13), sem ler nem repetir a versão no texto. Na NTLH, a numeração de alguns versículos difere da de outras versões: use a da NTLH no texto da redação.
- Tamanho do texto, nível dos intertítulos e shortcodes: cada rotina define.
- Antes de gerar texto, `prompt_do_nxfeed` traz a linha editorial do NX Feed: siga-a.

## 8. SEO

- Palavra-chave de 2 a 4 palavras, escrita igual no 1º parágrafo, em um intertítulo e 2 ou mais vezes no texto.
- Título SEO ≤ 60 começando por ela; meta description ≤ 155 caracteres, só com números e datas que estão no texto e na mesma grafia; slug minúsculo com hífens, ≤ 51; 5 a 10 tags (a rotina pode pedir mais).
- **Nota SEO ≥ 85.** Se vier abaixo, corrija com `editar_materia` (`trocar_trecho`) até duas tentativas; depois publique com a nota que tiver e avise no resumo.

## 9. Imagem destacada

- A rotina escolhe e grava a foto sozinha; **o Mário não escolhe foto**. Critérios, nesta ordem: (1) informação — mostra o fato, o lugar, o produto ou as pessoas da matéria; (2) atualidade — a mais recente que sirva (evite obra inacabada ou cenário que já mudou); (3) beleza e qualidade — nítida, bem composta, boa luz, horizontal, de preferência ≥ 1200 px.
- **Onde cada campo aparece no site:** a **descrição** é a legenda visível embaixo da imagem, seguida automaticamente de " – Foto: <fonte>/<autor>"; a **legenda** é o texto alternativo (alt), que o leitor não vê; o **título** é o nome interno da mídia; **fonte** e **autor** formam o crédito.
- Ordem de busca (a rotina pode mudar): **NX Fotos (termo), que é o banco central da casa** → `buscar_imagens` recomendadas (materia_id) → editoriais (termo) → divulgação oficial com crédito. Olhe a foto antes de gravar e passe pela conferência da 9.3. Em foto real, a descrição diz o que ela mostra.
- Sem foto do próprio fato (obra que não começou, estudo, indicador): foto real de acervo do mesmo tipo de cena, com "imagem ilustrativa" na descrição; "foto de arquivo" quando for. Pessoa citada no título: foto dela.
- Grave com `definir_imagem_destacada` preenchendo título, fonte, autor, descrição e legenda (alt): esses campos vão para o WordPress.
- Recusa por "dimensões muito grandes": use a versão reduzida que o WordPress do próprio site gera (o mesmo arquivo com sufixo como -1536x1024).
- Nunca rosto de menor identificável em contexto sensível.

### 9.1 e 9.2 Imagem por IA e legenda-fato (autorizada em 26/10/2026 para todas as rotinas)

Último recurso, só quando nenhuma foto real com direito de uso servir: carregue a skill **`imagem-ia-next`** e siga-a (Krea, prompt, o que é proibido gerar, gravação, legenda-fato e resumo). Se ela não estiver disponível, publique sem imagem e registre em Pendências "imagem por IA: skill de apoio indisponível".

### 9.3 Conferência e tratamento da foto (decisão do Mário Fernando, 11/11/2026)

Vale para toda foto real, de qualquer rotina, antes de gravar.

1. **Assunto exato.** A foto mostra exatamente o que a matéria diz. Troca de marca mostra a marca nova, nunca a antiga. Órgão mostra o prédio certo: a Secom-ES fica no Palácio da Fonte Grande, não no Palácio Anchieta. Na dúvida sobre o lugar, confira no site oficial do órgão antes de gravar.
2. **Atual e sem repetição.** A mais recente que sirva. Confira nas publicações do portal já listadas na rodada (seção 4) se a mesma foto foi usada há pouco; se foi, escolha outra.
3. **Origem limpa.** Nada com crédito de órgão de controle (2.1) e nada tirado de matéria crítica a cliente ou parceiro da casa. Pichação, faixa de protesto ou marca de terceiros em destaque: troque.
4. **Tratamento no padrão das revistas impressas.** As fotos do banco chegam cruas. Olhe a foto: se já está viva e bem tratada, não mexa. Se está apagada, fria ou lavada, trate no padrão vivid da casa: um pouco mais quente e cítrica, azuis mais quentes (puxados para o ciano), cor e contraste reforçados sem estourar pele nem céu. Valores provisórios, até a calibragem com páginas da revista: balanço quente (vermelho +5%, verde +1,5%, azul −6%), curva S suave, vibrance +45% nas cores apagadas, azuis −8° de matiz, tudo na força 0,85.
5. **Como aplicar.** Baixe a foto em resolução cheia (no NX Fotos, `link_do_original`), trate com o script abaixo, suba com `pedir_link_de_envio` + `curl -T` e grave a URL do Studio com `definir_imagem_destacada`. O link de envio é de uso único: não mostre nem guarde. Se não der para tratar, grave a original e registre "foto sem tratamento" em Pendências.
6. **Lacuna no banco.** Sem foto boa do assunto no NX Fotos, registre em Pendências o que falta, para a equipe de fotografia produzir e subir ao banco.

Script (`python3 tratar_foto.py entrada.jpg saida.jpg 0.85`):

```python
import sys
import numpy as np
from PIL import Image

def tratar(im, forca=1.0):
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    a[..., 0] *= 1 + 0.05 * forca; a[..., 1] *= 1 + 0.015 * forca; a[..., 2] *= 1 - 0.06 * forca
    a = np.clip(a, 0, 1)
    k = 0.12 * forca
    a = np.clip(a + k * (a - 0.5) * (1 - np.abs(2 * a - 1)), 0, 1)
    hsv = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).convert("HSV")).astype(np.float32)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    s = np.clip(s + 0.45 * forca * s * (1 - s), 0, 1)
    azul = (h > 195) & (h < 255)
    h = np.where(azul, h - 8 * forca, h)
    hsv2 = np.stack([(h % 360) * 255 / 360, s * 255, v * 255], -1).astype(np.uint8)
    return Image.fromarray(hsv2, "HSV").convert("RGB")

if __name__ == "__main__":
    forca = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    tratar(Image.open(sys.argv[1]), forca).save(sys.argv[2], quality=92, subsampling=0)
```

## 10. Avisos ao fim da rodada

**Não envie e-mail** (decisão do Mário Fernando, 27/10/2026). O aviso da rodada é o resumo na conversa e a notificação do app.

1. **Resumo na conversa** (SendUserMessage), curto, para celular, com o título que a rotina define. Se a execução rodar mais de uma rotina, um resumo só, com uma parte por rotina. Seções, nesta ordem:
   - **Publicadas:** título com o link no ar, portal e categoria;
   - **Imagens de IA para validar:** link da matéria, link da imagem e a legenda-fato (ou "legenda sem fato novo"), com a frase "Se precisar, troque no NX Feed.";
   - **Também na rodada:** o que não foi publicado e o motivo (fora por regra de pauta, duplicado, superado, erro técnico), ajustes em matérias da redação, casos marcados "envolve parceiro";
   - **Pendências:** erro técnico, SEO abaixo de 85, categoria recusada, dado não confirmado, conector fora, foto sem tratamento, lacuna no banco de fotos, peça do NXtab fora.
   - Seção sem itens: "nenhuma". A rotina pode acrescentar a parte própria dela (tabelas, metas, contagens).
2. **Notificação do app Claude:** só quando houver matéria nova ou problema (a rotina pode pedir sempre). Rodada sem novidade termina com "Sem fato novo nesta rodada", sem notificação.

## 11. Economia do plano (decisão do Mário Fernando, 04/11/2026)

As rotinas dividem o mesmo limite de uso do plano com tudo o que o Mário faz no Claude. Quando ele acaba, as rodadas seguintes falham sem publicar nada (foi o que derrubou as rotinas da manhã de 04/11/2026). Esta seção vale como padrão para toda rotina e **não afrouxa as seções 2.1, 2.2, 4, 5 e 6**: economizar é fazer cada conferência uma vez só, nunca pular conferência.

1. **Uma varredura por execução.** Quando duas rotinas rodam na mesma execução (ex.: esporte e Panorama), faça uma só listagem do feed, uma só listagem de rascunhos e pendências e uma só listagem do que já foi ao ar em cada portal, e reparta os itens entre as rotinas. Listagem que já está na conversa não se repete; a exceção é a reconferência antes de publicar (seção 4).
2. **Listagens enxutas.** `listar_materias` sempre com `formato` compacto e `data_de` no início da janela da rodada; "todas as páginas" quer dizer até a lista sair da janela. `ver_materia` só nas matérias que a rodada vai usar ou que a regra manda conferir.
3. **Web na medida.** WebSearch no modo standard; o extended só quando o standard vier vazio, fora do assunto ou desatualizado. WebFetch só nas páginas que sustentam a matéria ou conferem um dado. Para saber "o que está grande no dia", uma ou duas páginas bastam. Site que a skill diz que não abre por leitura automática: não tente, nem pela raspagem. Firecrawl e Apify (`raspagem-web-next`) só nas rotinas que os citam, dentro do teto de créditos de cada uma.
4. **Navegador só para confirmar.** Claude in Chrome só para ler uma página específica que confirma uma pauta já escolhida e que não abre por WebFetch (ex.: o perfil oficial do evento). Nunca para varrer perfis, feeds ou listas: cada tela do navegador custa muitas vezes uma leitura de página.
5. **Imagem pela ordem.** Siga a ordem de busca da seção 9 e só passe para a fonte seguinte quando nenhuma opção da fonte da vez atender aos critérios. Imagem por IA: uma geração, e a segunda só com defeito visível (9.1).
6. **Sair cedo.** Sem pauta que passe na régua da rotina depois da varredura, não procure pauta para preencher: vá ao resumo com "Sem fato novo nesta rodada". Pauta descartada não volta a ser aberta na mesma rodada.
7. **Uma vez cada.** Carregue cada skill uma vez por execução e não a releia. `prompt_do_nxfeed` uma vez por matéria e tipo, de novo só se a matéria mudou. `regras_de_arte` uma vez por rodada.
8. **Resumo curto.** O resumo da seção 10 traz títulos, links e motivos; não copia texto de matéria nem listagens inteiras.

## 12. Gráficos, tabelas e infográficos: sempre no NXtab (decisão do Mário Fernando, 13/11/2026)

**Vale acima de qualquer rotina e de qualquer tarefa agendada.** Toda tabela, gráfico ou infográfico de matéria dos sites sai do NXtab, na paleta do veículo. Nada de tabela HTML feita à mão, gráfico de outra biblioteca, imagem de IA com números ou print de outro site (única exceção: o quadro da previsão do tempo). As regras completas (quando entra, modelo pela natureza do dado, paleta, como gerar e como entra na matéria) estão na skill **`dados-e-graficos-next`**: carregue-a antes de montar a primeira peça. Se ela não estiver disponível, a matéria vai sem peça, com os números no texto, e o resumo registra em Pendências "peça do NXtab fora: skill de apoio indisponível".

## 13. Republicação: dados sempre atualizados (decisão do Mário Fernando, 13/11/2026)

**Vale acima de qualquer rotina e de qualquer tarefa agendada**, para toda matéria que volta ao ar (`acervo-esbrasil`, `acervo-comunhao`, `artigos-acervo-esbrasil`, `artigos-acervo-comunhao`, `artigos-acervo-next` e as que vierem): todo dado datado do texto é procurado na fonte oficial mais recente. As regras completas estão na skill **`dados-e-graficos-next`**, que essas rotinas carregam sempre. Se ela não estiver disponível, siga a regra de dados da própria rotina e registre em Pendências "republicação: skill de apoio indisponível".