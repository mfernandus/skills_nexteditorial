# O que muda nesta versão (18/11/2026)

Base: a versão do Git de 18/11, 13:17 (corte limpo, selos, capa foto cheia). Nada do padrão visual novo foi alterado.
Entrou por cima o que foi aprendido rodando a skill nos vídeos 8, 9 e 10 do lote.

## Falta no repositório
- Pasta `assets/selos/` (com_quadrado.png, programa_[nome].png, selos_[programa].png, selos_so_marca.png). A skill pede esses arquivos e eles não estão no Git. Sem eles não dá para montar Shorts nem capas no padrão novo.

## Scripts trocados
- `scripts/tratar_foto.py`: GFPGAN virou opcional. Sem o pacote ou sem os pesos, o script avisa e segue (antes derrubava tudo).
- `scripts/cortar_shorts.py`: aceita .srt com ponto e do Windows, tem fade de áudio, modos webcam/cheio, `centro_x` por Short, `delogo` e `marca_branca`. Continua fora da montagem do corte limpo; fica como referência dos filtros.

## SKILL.md: o que entrou
- Tabela de ferramentas: captura_quadros.js, folha_de_contato.py, montar_dupla.py, comprimir_envio.py e o aviso dos selos pendentes.
- Tela final: o elemento de link só salva com "Mensagem personalizada"; a imagem do link precisa de clique de mouse.
- Comentário fixado: menu, "Fixar no topo" e confirmação só com clique de mouse; como medir a escala de clique.
- 12.5.1: captura de quadros, folha de contato, recorte antes do rembg, dupla de convidados.
- Download do original: clique de mouse, pasta do estúdio e do Drive, tempo de espera, plano B.
- Transcrição: legendas automáticas do YouTube quando o whisper não baixa, regras do .srt, corte conferido pelo nível do áudio.
- Montagem: quando o desfoque da tarja fica feio, terminar o Short antes dela; gráficos do canal no original; conferir enquadramento antes e depois de cortar.
- Envio: só aceita arquivos em `/mnt/user-data/uploads`; aria-label + read_page; "Unknown tool" que envia mesmo assim; vídeo relacionado direto na etapa Elementos do vídeo; conferir Privado (às vezes vem Público); visibilidade pela lista quando a página de edição falha; filtro da lista por título.
- Drive: pastas do convidado, `envio\`, `Originais\`, arquivos acima de 25 MB e o `progresso_16_videos.md`.
- Notas práticas: extensão instável, saída bloqueada por URL, Studio com erro, troca de miniatura, Short antigo vai para Privado, título com teste A/B em andamento.
- Execução: pausa das 19h às 9h, só o estudio001-pc e o Chrome da Comunhão.
- Troca de capas em lote (vídeos antigos).

## Segunda rodada (18/11/2026, tarde)
- Montagem dos Shorts: comandos ffmpeg movidos para `references/montagem_shorts.md`, com duas variantes novas testadas com vídeo de teste:
  - **com gráficos do canal**: `marca_branca` + `delogo` aplicados antes do recorte (antes a skill citava os filtros, mas o comando do corte limpo não os tinha);
  - **webcam (720p)**: recorte do alto do quadro com fundo desfocado, adaptado ao corte limpo. Mostrar o primeiro Short de webcam ao Mário antes de seguir com o lote.
- Enquadramento: voltou o `centro_x` ~0,36 do estúdio com a bandeira e a explicação de por que a webcam não usa o corte na altura inteira.
- Fontes: `Inter-ExtraBold.otf`, `Inter-Bold.otf` e `Inter-Regular.otf` (OFL) entraram em `assets/fonts/`; a capa do Short passa a medir e desenhar com as fontes do kit, não com as do sistema. Legenda conferida: continua saindo em ExtraBold Italic.
- SKILL.md mais leve: os procedimentos do Studio e do Chrome foram para `references/studio.md` e a troca de capas em lote para `references/capas_lote.md`. O SKILL.md aponta para cada um no passo certo.
- Arquivo de progresso: deixou de ser fixo em `progresso_16_videos.md`; lote novo cria `progresso_[nome-do-lote].md`.
- Voltou o limite de 100 MB somados por envio de arquivos ao computador.
- Continua pendente: pasta `assets/selos/`.

## Manchete da capa horizontal até 60 caracteres (18/11/2026, orientação em áudio)
- A manchete da thumb do vídeo (1600×900) passou de 38 para **até 60 caracteres**. Até 38 caracteres, nada muda (2 linhas, corpo 44). De 39 a 60: **3 linhas**, corpo de 32 a 38. **4 linhas, nunca.**
- Entrelinha (0,88) e entreletras (−1,6) mantidas; nenhuma letra pode encostar no rosto do convidado.
- Título do jornalista acima de 60 caracteres, ou que não caiba em 3 linhas no corpo 32: a IA **avisa** que precisa reduzir e sugere versões mais curtas para aprovação. Não corta por conta própria.
- `gerar_thumb.py` aplica a regra: limite de 60 caracteres e 3 linhas, corpo mínimo conforme o tamanho e parada com AVISO em vez de reduzir a fonte. Testado com manchetes de 29, 55 e 57 caracteres (ok) e com 4 linhas, 62, 79 e linha larga demais (aviso).
- A troca de capas em lote segue o mesmo limite.

## Melhorias 1, 3 e 4 (18/11/2026, noite)
- **Novo `scripts/gerar_capa_short.py`:** gera a capa do Short no modelo foto cheia com todas as medidas do Passo 13, item 8, e a trava do texto (título até 30 caracteres, 2 linhas, corpo 56–92; nome e cargo com mínimo 30). Para com AVISO quando o título não cabe ou falta o selo oficial (`assets/selos/com_quadrado.png`). Exemplo em `exemplos/capa_short_danielle.json`. Testado com selo provisório: as medidas saem certas; com o selo oficial ainda ausente, o script para com o aviso, como deve.
- **Checagem do rosto no `gerar_thumb.py`:** com a foto recortada, mede se alguma letra encosta no rosto ou no cabelo e para com AVISO. Raspar um fio solto (< 150 px) é aceito, como no modelo aprovado da Danielle. Testado: o modelo aprovado passa; a manchete de 3 linhas que entrava no cabelo é barrada e passa depois de recuar a foto.
- **Pasta `legado/`:** `gerar_visual_short.py`, `cortar_shorts.py` e os modelos antigos dos Shorts com moldura saíram de `scripts/` e `exemplos/`, com um LEIA-ME explicando o que usar no lugar.

## Selos dos Shorts (18/11/2026, noite)
- Entrou o selo oficial `assets/selos/com_quadrado.png` (arquivo "Logo-Comunhao-redux_novo.png", enviado pela equipe).
- Novo `scripts/montar_selos.py`, que gera as camadas de selos; já geradas `selos_entrevista.png` (logo do Comunhão Entrevista + quadradinho) e `selos_so_marca.png`.
- Testado: capa do Short com `gerar_capa_short.py` e Short com o comando base do ffmpeg, os dois com o selo oficial.
- Faltam os logos dos programas Na Estrada, O Pastor Responde, Fim de Papo, Persona e Texto & Contexto.
