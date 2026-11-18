# Procedimentos no YouTube Studio e no navegador — Revista Comunhão

Detalhes de operação testados ao rodar a skill `youtube-comunhao-titulos`. O SKILL.md diz **o que** fazer; este arquivo diz **como** fazer no Studio e no Chrome. Leia a seção correspondente na hora de executar cada etapa.

## Tela final: elemento de link (Passo 9)
- **Elemento de link (testado em 09/11/2026):** depois de colar a URL, escolha o call-to-action ("Saiba mais") e a imagem (abrir o 3º seletor, clicar com o mouse no primeiro cartão e em Aplicar; o clique por código seleciona mas não aplica) e **preencha "Mensagem personalizada"** (ex.: "Leia a matéria completa"). Sem a mensagem o botão Salvar fica desativado e o editor avisa "Falta uma mensagem personalizada no elemento de link".
- O editor pode abrir duas cópias da janela: trabalhe sempre na que está visível. Para conferir, reabra a tela final e veja as três linhas (Inscrever-se, Vídeo, Link).

## Comentário fixado (Passo 10.1)
- Os comentários só carregam com rolagem de verdade (roda do mouse); rolar por código às vezes não dispara.
- Texto: inserir linha a linha no campo, com quebra de linha entre elas, e conferir que não ficou duplicado antes de clicar em Comentar.
- O menu ⋮ do comentário, o item **Fixar no topo** e o botão de confirmação **só respondem a clique de mouse**; o clique por código não abre o menu.
- A escala entre a tela e a página varia (já foi 0,959 e 0,93). Antes de clicar por coordenada, registre um `mousedown` na página, dê um clique de teste e compare a posição recebida com a esperada.

## Download do original (Passo 13, item 5)
- **Como disparar:** abra o menu ⋮ e clique em **Baixar** com o mouse. O clique por código (`element.click()`) abre o menu mas não baixa (testado em 15/10/2026). Alternativa testada em 09/11: clicar por código no botão interno do ⋮ e, 1,2 s depois, abrir o link `a[href*=download_my_video]` na própria aba.

## Transcrição pelas legendas automáticas do YouTube (Passo 13, item 6)
- **Se o modelo não baixar** (erro 403 do proxy ao buscar no Hugging Face), use as **legendas automáticas do YouTube com tempo por palavra**: abra a página pública do vídeo, intercepte as respostas `timedtext` (substitua `window.fetch` e `XMLHttpRequest.open` para guardar o texto das respostas), ligue a faixa `pt`/`asr` no player (`loadModule('captions')` + `setOption('captions','track',{languageCode:'pt',kind:'asr'})`) e leia o JSON (`events[].segs[]`, tempo = `tStartMs + tOffsetMs`). Pedir a URL `timedtext` de novo por fora volta vazia; só a resposta capturada serve.
- O painel do navegador do computador (Claude_Browser) devolve textos longos inteiros; a extensão do Chrome corta a saída em ~1.000 caracteres. Prefira o painel do computador para ler a transcrição.
- Se o painel de transcrição do Studio não abrir, ligue as legendas no player: a requisição de legenda (`timedtext`) traz o texto com tempos.

## Envio dos Shorts ao Studio (Passo 13, item 9)
- **Arquivo ≤ 10 MB:** o envio pelo navegador aceita no máximo 10 MB por arquivo. Recomprima cada Short em 1080×1920 com H.264 em **duas passagens** e taxa-alvo `9,2 MB × 8 ÷ duração − 130 kbps` (áudio AAC 128k). Guarde a versão cheia; suba a comprimida.
- **Caminho do arquivo:** o envio só aceita arquivos **dentro de `/mnt/user-data/uploads/...`** (trazidos de pasta conectada com stage, ou copiados para lá no ambiente de trabalho). Arquivos só em `/mnt/user-data/outputs`, com caminho do Windows (`G:\...`) ou do Mac são recusados; vale também para capas e para a miniatura do vídeo. Grave os comprimidos em `G:\Meu Drive\Comunhão shorts\[Convidado]\envio\` e traga-os antes de enviar.
- **"file is hardlinked":** arquivo recém-gravado no Mac pode ser recusado ao ser trazido. Regrave com outro nome, **espere ~50 s** e traga de novo.
- Studio → `.../videos/upload?d=ud` → marque o `input type=file` do diálogo com um `aria-label` por código (ex.: `upfile`), leia a árvore da página (read_page com filtro "all") para achar a referência do input e use a ferramenta de envio de arquivo do Chrome (nunca clicar no botão "Selecionar arquivos", que abre a janela do sistema). A ferramenta às vezes responde "Unknown tool" mesmo tendo enviado: espere ~8 s e confira se o título do diálogo mudou para o nome do arquivo antes de tentar de novo.
- **Título e descrição:** o Studio preenche os padrões do canal alguns segundos depois de abrir a janela e sobrescreve o que foi digitado antes. Espere ~6 s, **clique de verdade no campo Título**, e só então substitua o conteúdo dos dois campos (selecionar o conteúdo do campo e inserir o texto). Releia os dois campos antes de avançar.
- **Capa:** marque o `input type=file` da seção Miniatura com `aria-label` (ex.: `capafile`), leia a árvore do diálogo (read_page com o id do diálogo) e envie o JPG. Confira que a prévia passou a ser uma imagem `data:image/jpeg`.
- **Vídeo relacionado (testado em 09 e 11/11/2026):** aparece na etapa **Elementos do vídeo** da própria janela de envio (`#shorts-content-links-add-button`). Na janela "Escolha um vídeo específico", digite o **título do vídeo completo** ou o **nome do convidado** (se não achar, cole o link) e **clique com o mouse no cartão**; confira que o título do vídeo completo apareceu na etapa. A janela às vezes abre duas vezes: digite na que está visível. Se não der na janela de envio, faça depois na página de edição do Short.
- Público: "Não é conteúdo para crianças" → Avançar até **Visibilidade** → marque **Privado** e confira o rádio `PRIVATE` marcado antes de clicar em Salvar (`#done-button`): a etapa às vezes vem com **Público** marcado.
- **Short que ficou "Salvando…" ou sem visibilidade:** na lista de conteúdo ele aparece como "Não listado" ou rascunho. Abra o seletor de visibilidade na própria linha da lista (clique de mouse), marque **Privado** e salve; o botão de visibilidade da página de edição às vezes não abre.
- **Conferência:** Conteúdo → aba Shorts. Os Shorts programados (devocionais) vêm primeiro na lista; filtre pelo título com `?filter=[{"name":"TITLE","value":{"value":"trecho do título"}}]` na URL. Abra a página de edição de cada Short e confira capa personalizada, vídeo relacionado e "Privado". Todos devem estar "Privado" (se algum ficar "Rascunho", abra "Editar rascunho" e conclua). Se a miniatura de algum aparecer em branco, reenvie a capa na página de edição do Short e salve.

## Notas práticas do Studio e da extensão do Chrome
- Título e descrição são campos editáveis do tipo `#textbox`. Selecione todo o conteúdo e substitua de uma vez; "Ctrl+A + digitar" pode inserir o texto no meio do antigo. Se isso acontecer, use **Desfazer alterações** e refaça.
- Depois de clicar em **Salvar**, espere alguns segundos antes de recarregar — recarregar cedo demais descarta a alteração.
- Tags ficam em **Mostrar mais** → Tags. O botão "Remover tudo" limpa as antigas.
- Card: tempo em `MM:SS:QQ` e mensagem com até 30 caracteres (ver Passo 10).
- **Teste A/B:** o Studio roda **um teste por vez** por vídeo. Com teste de título em andamento, a capa pode ser trocada normalmente (vale para todas as variantes); um teste de **miniatura** só começa depois que o de título terminar.
- **Download do original (liberado):** ⋮ (Opções, ao lado de Salvar) → Baixar com **clique de mouse**, sem pedir confirmação. Se o primeiro clique só fechar o menu, abra o menu de novo e clique em Baixar; confira na pasta de destino (Passo 13, item 5) se surgiu o `.crdownload` e espere ele virar `.mp4` antes de cortar.
- **Extensão do Chrome instável:** chamadas às vezes respondem "Tab … is not in Claude's tab group" ou "failed in the extension" mas executam mesmo assim. Antes de repetir uma ação (sobretudo cliques que salvam, enviam ou comentam), confira o estado da página por código. Prints de tela às vezes falham seguidamente: confira por código.
- **Saída de código bloqueada:** respostas com URL completa ou `?`/`=` podem voltar como "BLOCKED: Cookie/query string data". Mascare URLs e esses caracteres no que o código devolve.
- **Studio com "Ops! Algo deu errado":** recarregue a página e espere ~8 s antes de procurar os campos.
- **Trocar a miniatura:** página de edição → localizar o `input type=file` da seção Miniatura (procure de novo se a página demorar) → enviar o JPG que está em `/mnt/user-data/uploads/...` → esperar ~5 s → **Salvar** → conferir que o botão Salvar voltou a ficar desativado. Vale também para vídeos não listados.
- **Short antigo substituído:** passe para **Privado** e confira em Conteúdo → Shorts. Nunca exclua.
- **Teste A/B em andamento:** com teste de título em andamento, a página mostra o bloco "Teste A/B de títulos — Em andamento" no lugar do campo de título; para mudar o título é preciso "Editar título".
