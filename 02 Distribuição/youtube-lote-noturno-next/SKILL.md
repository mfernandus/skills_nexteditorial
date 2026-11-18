---
name: "youtube-lote-noturno-next"
description: "Roda em lote, por comando, a atualização dos vídeos dos canais da Next Editorial no YouTube em modo noturno, com teste A/B nativo de capas, Shorts exportados para as redes e a Central sempre atualizada."
---

# Lote noturno de vídeos — canais da Next Editorial

Esta skill não substitui as skills de cada canal: ela as **orquestra em lote**. Para cada vídeo da fila, aplica a skill do canal (títulos, A/B, descrição, capítulos, tags, cards, tela final, comentário fixado, playlists, capa e Shorts), mas troca as paradas de aprovação daquelas skills por regras definidas aqui, para que o trabalho siga de madrugada sem ninguém na frente da máquina. As paradas trocadas são: na `youtube-esbrasil-titulos`, a pergunta do tipo de capa no início e o ok antes de salvar no Studio; na `youtube-comunhao-titulos`, a exibição do pacote antes de salvar nos pedidos avulsos (a execução completa dela já roda sem parar).

**Nunca roda sozinha.** Só começa por comando do Mário Fernando ("preparar o lote", "rodar o lote", "retomar o lote") ou pela tarefa agendada criada por ele. Não monitora canais nem dispara ao detectar vídeo novo.

## Mapa de canais → skill

| Canal | Skill aplicada | Observação |
|---|---|---|
| Revista ES Brasil (@RevistaESBrasil) | `youtube-esbrasil-titulos` | Templates entrevista, cafe e destinos |
| Revista Comunhão (@revistacomunhaooficial) | `youtube-comunhao-titulos` | |
| Destinos ES (canal próprio, se existir) | `youtube-esbrasil-titulos`, template `destinos` | Confirmar o canal na primeira rodada |
| Next Editorial (nexteditorial@gmail.com) | sem skill de marca ainda | Só pacote de texto; capa e Shorts viram pendência "criar skill Next Editorial" |
| Outro canal | sem skill | Registrar na Central e perguntar ao Mário qual skill usar |

Cada canal fica numa conta Google diferente no Chrome (Comunhão em comunhao70@gmail.com; ES Brasil em conta própria; Next Editorial em nexteditorial@gmail.com). Antes de mexer em qualquer vídeo, troque para o canal certo (menu do avatar → Mudar de conta) e confirme no Studio o nome do canal. Nunca digite senha: se a conta não estiver no Chrome, marque o vídeo como `erro: conta ausente` e siga para o próximo canal.

## A Central (planilha Google "Central YouTube Next")

É a única fonte de verdade do lote e deve estar **sempre atualizada**: a skill escreve na Central ao começar cada vídeo, ao terminar cada etapa e ao terminar o vídeo. Quem abrir a planilha de madrugada vê exatamente onde o trabalho está.

Aba **Fila**, uma linha por vídeo:

| Coluna | Conteúdo |
|---|---|
| canal | ES Brasil, Comunhão, Destinos ES, Next Editorial… |
| video_id / link | ID e URL do vídeo |
| título atual | como está no YouTube |
| publicado / duração / views | dados do inventário |
| tipo de capa | entrevista, cafe, destinos, coluna, outro — **confirmado pelo Mário** |
| playlist categoria | sugerida pela regra da skill do canal, confirmada pelo Mário |
| promoção paga | sim / não — confirmado pelo Mário |
| prioridade | 1 = primeiro (padrão: mais recente e mais visto primeiro) |
| status | ver abaixo |
| etapa | última etapa concluída (permite retomar) |
| título aplicado / capa / shorts | o que foi feito (IDs dos Shorts) |
| aprovar shorts | Mário escreve "sim" para liberar a publicação |
| teste capa / capa vencedora / resultado teste | acompanhamento do A/B nativo |
| pasta redes / redes | link da pasta no Drive e status da exportação |
| pendências / erro | texto curto |
| atualizado em / sessão | carimbo de data e link da sessão |

Status possíveis: `novo` → `aguardando confirmação` → `pronto` → `em andamento` → `aplicado (shorts privados)` → `shorts aprovados` → `concluído`; ou `erro` / `pulado`.

Aba **Resumo**: totais por canal e por status, vídeos processados na última noite, previsão de término no ritmo atual.

## Comando 1 — "preparar o lote" (de dia, com o Mário presente)

1. **Ambiente** (seção abaixo): confirme a máquina local, o Chrome e as contas.
2. **Inventário**: para cada canal pedido, liste todos os vídeos longos (não Shorts) pela página `/videos` do canal, paginando pela API interna do YouTube no próprio navegador (`/youtubei/v1/browse` com o token de continuação). Grave na Fila os que ainda não estão lá, com status `novo`.
3. **Sugestões**: preencha tipo de capa, playlist de categoria e promoção paga sugeridos a partir do título, da descrição e das playlists atuais (ex.: título com "Café com Moqueca" → `cafe`; com patrocinadores citados na descrição → promoção paga `sim?`).
4. **Pergunta no começo, vídeo a vídeo**: apresente ao Mário as sugestões em blocos (até 4 vídeos por pergunta, com a sugestão como primeira opção) para ele confirmar o tipo de capa de cada vídeo. Ele também pode confirmar direto na planilha. Só vídeos confirmados passam para `pronto`.
5. **Priorize**: ordene a fila (recentes e mais vistos primeiro, salvo ordem diferente do Mário).

## Comando 2 — "rodar o lote" (modo noturno, sem paradas)

Antes da fila, leia os testes A/B de capa em andamento (seção "Teste A/B de capas", item 4) e registre os resultados.

Para cada vídeo `pronto`, na ordem de prioridade:

1. Marque `em andamento` na Central.
2. Aplique a skill do canal **inteira**, com estas trocas:
   - **Sem pergunta inicial**: o tipo de capa vem da Central.
   - **Sem ok final**: estão pré-autorizados pelo Mário título com teste A/B, descrição, capítulos, tags (removendo as do padrão do canal), cards, tela final, comentário fixado, playlists da regra confirmadas na Central, promoção paga confirmada e capa.
   - **Shorts sobem sempre como PRIVADOS**, com capa e vídeo relacionado. Só viram públicos quando a coluna "aprovar shorts" tiver "sim" (o próximo lote publica).
   - **Nunca**: enviar e-mail ou mensagem, excluir vídeo/Short/comentário, marcar playlist fora da regra, tornar público o que estiver privado sem aprovação.
   - **Capa com teste A/B nativo** (seção "Teste A/B de capas") e **Shorts exportados para as redes** (seção "Exportação dos Shorts").
3. Após cada etapa, atualize `etapa` e `atualizado em`. Ao fim, `aplicado (shorts privados)`.
4. **Trava de segurança, sem parar o lote**: se faltar dado, a capa reprovar na avaliação (nota < 4 em algum critério depois de duas correções), o tema for político sensível ou algo sair do padrão, registre a pendência na linha, marque `pulado` e siga para o próximo vídeo.
5. **Retomada**: se a sessão cair, o próximo "rodar o lote" retoma cada vídeo a partir da coluna `etapa`, sem refazer o que já foi salvo.
6. **Janela**: não comece vídeo novo depois das 06:30; termine o atual, atualize a aba Resumo e encerre.
7. **Limites do YouTube**: no máximo 15 envios de Shorts por canal por noite; o excedente fica para a noite seguinte (status permanece `em andamento`, etapa `shorts pendentes`).

Ao fim, escreva na aba Resumo o relatório da noite: vídeos concluídos, Shorts aguardando aprovação (com links), pulados e o motivo, erros.

## Comando 3 — "publicar aprovados"

Publica os Shorts das linhas com "aprovar shorts" = "sim" e marca `concluído`. Pode rodar junto com o lote.

## Máquina de execução

O lote não depende de um computador específico. Serve qualquer máquina sempre ligada (computador dedicado ou máquina virtual na nuvem) que tenha:

1. o app desktop do Claude aberto, logado na conta do Mário e vinculado à sessão;
2. o Chrome com a extensão do Claude e as contas Google de cada canal já logadas (login feito pelo Mário; a skill nunca digita senha);
3. o kit de capas da **ES Brasil** copiado para `Documents/Claude Skills/youtube-esbrasil-titulos` (o da Comunhão já vem dentro da própria skill `youtube-comunhao-titulos`, em `scripts/` e `assets/`);
4. ffmpeg e os pacotes de transcrição e de capa (faster-whisper, rembg, GFPGAN, Playwright com Chromium) instalados, e o Google Drive para computador, se a exportação para as redes for usada.

Se faltar algum desses itens, registre na aba Resumo o que falta e não improvise a arte.

## Ambiente local — a máquina que executa a skill é o ambiente de download

Qualquer computador em que a skill estiver rodando (pelo app do Claude vinculado à sessão) é o ambiente de download e corte. No início de todo comando:

1. Confirme que o computador responde (`get_device_info`). Se não responder, escreva na Resumo "computador indisponível" e encerre: sem ele não há download, corte nem envio.
2. Use a pasta **Downloads** dessa máquina (peça acesso uma vez) e a pasta do kit de capas: `Documents/Claude Skills/youtube-esbrasil-titulos` para **ES Brasil** e Destinos ES; para a Comunhão, `scripts/` e `assets/` da própria skill `youtube-comunhao-titulos`.
3. **Downloads sempre pelo Chrome dessa máquina**: original pelo Studio (⋮ → Baixar), quadros e transcrição pelo próprio navegador (captura do player em 1080p para canvas e download do arquivo). Arquivos baixados pelo Chrome podem ser trazidos ao ambiente de trabalho diretamente.
4. **Cortes na própria máquina**: o original costuma passar de 400 MB, que é o limite para trazê-lo inteiro. Corte os trechos ali mesmo com ffmpeg (`-ss início -t duração -c copy`, com folga) e, antes de trazê-los, **regrave cada corte pelo terminal nativo da máquina** (`cat corte_vm.mp4 > corte.mp4`): arquivos gravados pelo shell isolado aparecem como "hardlinked" e são recusados; a cópia feita pelo terminal nativo é aceita.
5. Processamento pesado (transcrição com faster-whisper, recorte de foto, montagem de capa e Shorts) roda no ambiente de trabalho; os resultados voltam para `Downloads/shorts_<canal>_<convidado>/` na máquina local.
6. Se a máquina não tiver ffmpeg nativo, use o shell isolado para cortar e o terminal nativo apenas para regravar o arquivo.

## Corte e montagem automáticos dos Shorts

1. Transcrição do vídeo pelo painel "Mostrar transcrição" do YouTube (salva como .txt pelo navegador).
2. Escolha de 3 a 5 trechos segundo as regras da skill do canal (gancho, ideia completa, 30–60 s; nada político sensível, número sem contexto ou trecho publicitário).
3. Corte dos trechos na máquina local (item 4 acima) e tempos exatos por palavra com faster-whisper (`small`, `language='pt'`, `word_timestamps=True`), passando o áudio como array — a função de abrir arquivo da biblioteca falha com a versão instalada do PyAV.
4. Legendas em blocos de até 4 palavras, com revisão de nomes próprios, siglas e números; remova falas do entrevistador nas pontas.
5. Tarja do vídeo original: detectar por cor nos quadros e desfocar só nos intervalos em que aparece; ajustar `centro_x` para não cortar o logo do canal pela metade.
6. Montagem e capa, conforme o kit do canal:
   - **Corte limpo nos dois canais (desde 18/11/2026):** nada de moldura. O vídeo ocupa a tela inteira e leva por cima só os selos e a legenda. Selos: logo do programa no canto esquerdo e quadradinho da marca (ESB ou COM) no direito; Short sem programa leva só o quadradinho. Programa sem logo oficial no kit vira pendência na Central e o Short sai só com o quadradinho.
   - **ES Brasil e Destinos ES** (kit em `Documents/Claude Skills/youtube-esbrasil-titulos`): montagem pelo comando ffmpeg do Passo 13, item 7, da `youtube-esbrasil-titulos`, com a camada `selos_[programa].png`; `montar_short.py` e o modo `moldura` não se usam mais. Capa com `gerar_short_esbrasil.py capa` sobre quadro em 1080p.
   - **Comunhão** (kit na própria skill `youtube-comunhao-titulos`): montagem pelo comando ffmpeg do Passo 13, item 7, da `youtube-comunhao-titulos`, com a camada `selos_[programa].png`; o `cortar_shorts.py` e o modo `moldura` não se usam mais para montar. Capa com `gerar_visual_short.py capa` sobre quadro em 1080p.
   - Nos dois casos, apague por inpaint o logo do canal que aparece no quadro usado na capa.
7. Versão de envio ≤ 10 MB (H.264 duas passagens), gravada na máquina local e trazida para o envio.

## Teste A/B de capas (nativo do YouTube)

Toda capa longa sai com pelo menos duas versões (A e B). Em vez de trocar a capa manualmente (A por 5 dias, depois B por mais 5 dias), use o recurso nativo **Testar e comparar** do Studio: ele mostra A e B ao mesmo tempo para públicos diferentes, elimina o efeito do dia da semana e da idade do vídeo e, ao final, mantém sozinho a vencedora pelo **tempo de exibição**.

1. **Um teste por vídeo de cada vez.** Se o vídeo já tem teste de título em andamento, escolha uma das duas saídas:
   - **Padrão para vídeo novo:** rodar o teste combinado "Título e miniatura" (até 3 pares título+capa: A com título 1, B com título 2), em vez de dois testes separados.
   - **Vídeo antigo com teste de título já rodando:** registrar na Central `capa B aguardando` e iniciar o teste de capa no primeiro lote depois que o teste de título terminar.
2. **Configuração:** Detalhes → Miniatura → "Testar e comparar" → "Somente miniatura" (ou "Título e miniatura") → enviar capa A e capa B (até 3) → Concluído → Salvar. Se uma terceira capa (C) passou na avaliação, incluí-la também.
3. **Duração:** o YouTube encerra o teste sozinho quando há dados suficientes (de alguns dias a duas semanas). Não interrompa antes.
4. **Leitura do resultado:** a cada "rodar o lote", antes da fila, abra os vídeos da Central com `teste capa = em andamento` e confira o status em Detalhes → Miniatura. Se terminou, registre a **vencedora**, a participação de cada versão no tempo de exibição e o veredito do YouTube ("Vencedora", "Teve melhor desempenho" ou "Sem diferença"). Em "Sem diferença", mantenha a capa A (a de padrão da marca) e anote.
5. **Definitiva:** confirme que a capa vencedora ficou aplicada; se o YouTube não aplicou (ex.: sem diferença), aplique a escolhida manualmente.
6. **Vídeo com pouca audiência** (menos de ~1.000 impressões por semana): o teste pode não concluir. Depois de 14 dias sem veredito, encerrar com a capa A, anotar `inconclusivo` e seguir.
7. Colunas da Central: `teste capa` (não iniciado / em andamento / concluído / inconclusivo), `capa vencedora` (A, B, C) e `resultado teste` (texto curto com as porcentagens).

## Exportação dos Shorts para Instagram, TikTok e Facebook

Os mesmos cortes feitos para o YouTube ficam disponíveis para as outras redes numa pasta do Google Drive, organizada por canal e convidado.

1. **Estrutura no Drive:** `Shorts Next/<canal>/<AAAA-MM-DD> <convidado>/` (canais: ES Brasil, Comunhão, Destinos ES, Next Editorial). Crie a pasta do convidado pelo conector do Google Drive se ela ainda não existir.
2. **O que vai em cada pasta:**
   - os Shorts em **qualidade máxima** (`short_01.mp4`…), não a versão de envio ≤ 10 MB: 1080×1920, H.264, AAC, corte limpo com selos e legenda queimada (o mesmo arquivo do YouTube);
   - as capas dos Shorts (`capa_short_01.jpg`…), que servem como capa no Reels e no TikTok;
   - um Google Doc **"Legendas para redes – <convidado>"** com, para cada Short: título curto, legenda para Instagram/Facebook, legenda para TikTok, hashtags e o link do vídeo completo.
3. **Regras das legendas:**
   - nada de "#Shorts" nem chamadas do YouTube;
   - Instagram e TikTok: "link na bio" (link clicável não funciona na legenda);
   - Facebook: link direto para o vídeo completo no YouTube;
   - de 3 a 5 hashtags da marca e do tema; marcar o perfil do convidado ou da instituição quando a skill do canal indicar;
   - mesma checagem de nomes, siglas e números das legendas do vídeo.
4. **Como os arquivos chegam ao Drive:** o conector do Drive cria pastas e documentos, mas não envia vídeos. Copie os arquivos pela pasta do **Google Drive para computador** na máquina local (no Mac, `~/Meu Drive/Shorts Next/...` ou `~/Library/CloudStorage/GoogleDrive-<conta>/Meu Drive/...`), com `cp` pelo terminal nativo; a sincronização sobe sozinha. Se o Google Drive para computador não estiver instalado, deixe os arquivos em `Downloads/shorts_<canal>_<convidado>/` e registre a pendência na Central.
5. **Publicação nas redes é manual** (ou pela ferramenta de agendamento da equipe): a skill não publica no Instagram, TikTok ou Facebook. Os vídeos podem ir para as redes mesmo com o Short do YouTube ainda privado.
6. Colunas da Central: `pasta redes` (link da pasta do convidado no Drive) e `redes` (pronto / pendente).

## Notas técnicas do Studio (aprendidas na execução)

- Título e descrição: preencher por script (`focus` + `execCommand('selectAll')` + `execCommand('insertText')`), que é estável; digitar pode misturar com o texto antigo. Na janela de envio, esperar ~8 s antes, porque o Studio sobrescreve com os padrões do canal.
- Tags: campo "Tags" em Mostrar mais; digitar separadas por vírgula.
- Teste A/B: botão abaixo do título → "Somente título" → segundo título → Começar teste → Salvar.
- Cards de link exigem call-to-action, título de até 50 caracteres e imagem (a da matéria aparece em "Imagens do site").
- Busca dentro das janelas de escolha (vídeo/playlist): se o texto digitado não entrar, preencher o campo por script e disparar o evento `input`.
- Vídeo relacionado dos Shorts: abrir "Vídeo relacionado" e clicar no card cujo texto contém o título do vídeo completo; depois Salvar.
- Envio de Shorts: `input type=file` na página de upload; "Não é conteúdo para crianças"; Avançar ×3; visibilidade conforme a regra; conferir em Conteúdo → Shorts.
- O original baixado pelo Studio vem em 720p; prefira quadros capturados do player em 1080p para capas.
- Se o Studio mostrar "Ops, você não tem permissão", a conta ativa é de outro canal: trocar de conta antes de qualquer coisa.

## Ritmo e honestidade sobre prazos

O pacote completo leva de 30 a 60 minutos por vídeo. Com uma janela noturna de ~7 horas, o ritmo esperado é de 8 a 12 vídeos por noite. Informe sempre na aba Resumo quantos vídeos faltam e a previsão de término nesse ritmo, para o Mário decidir se quer priorizar subconjuntos.