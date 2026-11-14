---
name: "youtube-comunhao-titulos"
description: "Publica de ponta a ponta um vídeo da Revista Comunhão no YouTube: títulos A/B, descrição, tags, cards, tela final, capa publicada e 3 a 5 Shorts com capa, prontos no canal. Download do original já liberado."
---

# Pacote de publicação no YouTube — Revista Comunhão

Esta skill padroniza a forma como a equipe da Comunhão publica os vídeos do canal oficial (youtube.com/revistacomunhaooficial): título, teste A/B, descrição, capítulos, links rastreados, tags, Spotify, tela final, cards, playlist, thumb e Shorts. O objetivo é fazer cada vídeo ser encontrado na busca do YouTube e do Google, ser clicado por quem vê a miniatura e levar o espectador para o próximo vídeo, para o canal e para o portal.

Use SEMPRE que alguém da equipe pedir título de vídeo, sugestão de título, teste A/B, descrição de YouTube, tags, capítulos, tela final, cards, playlist, thumb/capa, Shorts/cortes ou "subir vídeo" da Comunhão — mesmo que mande só o tema, o nome do convidado, uma transcrição ou um link.

## Ferramentas do pacote

O arquivo `youtube-comunhao-titulos.skill` distribuído ao time traz tudo o que é preciso para reproduzir thumb e Shorts sem refazer o trabalho de base (se a pasta da skill não tiver `scripts/` e `assets/`, peça o arquivo .skill completo):

| Arquivo | Para quê |
|---|---|
| `scripts/gerar_thumb.py config.json saida.png` | Monta a thumb 1600×900 sobre a arte do template (manchete, nome, apoio opcional, foto). Centraliza o bloco na faixa sozinho (`"y0": "auto"`) e nunca deixa a manchete abaixo do corpo 38. Requer `pip install playwright` + Chromium. |
| `scripts/tratar_foto.py quadro.png recorte.png [0.6]` | Tratamento da foto: restauração facial com IA (GFPGAN, **opcional**), recorte com refino de cabelo, cor, rim light. Requer `rembg`. A restauração só roda se o pacote `gfpgan` e os pesos `weights/GFPGANv1.4.pth` existirem; sem eles, o script avisa "restauração PULADA" e segue (os pesos não vão no pacote: baixe pelo link no topo do arquivo). |
| `scripts/gerar_visual_short.py moldura\|capa config.json saida.png` | Visual dos Shorts no padrão **Comunhão play** (1080×1920 PNG): `moldura` = camada que vai por cima do vídeo (faixa laranja com título e nome, rodapé vermelho com logo, janela transparente de 1260 px); `capa` = miniatura do Short (logo Comunhão no alto, foto, faixa laranja com título e nome, logo play). Valida o limite de 30 caracteres e 2 linhas. Requer `playwright` + Chromium. |
| `scripts/cortar_shorts.py video.mp4 shorts.json pasta [legendas.srt]` | Gera os Shorts 1080×1920: vídeo do convidado na área livre de 1260 px (recorte no rosto), moldura do `gerar_visual_short.py` e legendas queimadas. Requer `ffmpeg` e `playwright`. |
| `scripts/captura_quadros.js` | Trecho para o Chrome: salva 12 quadros em 1080p do vídeo, direto do player do YouTube, em Downloads. Para escolher a foto quando o original ainda não foi baixado (ver 12.5). |
| `scripts/folha_de_contato.py saida.jpg quadros...` | Junta até 24 quadros numa folha numerada para escolher o melhor. |
| `scripts/montar_dupla.py esq.png dir.png saida.png [0.25] [direita]` | Junta os recortes de dois convidados (rostos inteiros, quem está na frente cobre só cabelo/ombro do outro). |
| `scripts/comprimir_envio.py pasta [9.2]` | Recomprime os Shorts para o envio pelo navegador (≤ 10 MB, H.264 em 2 passagens) em `pasta/envio/`. |
| `assets/` | `base_clean.png` (template sem texto e sem a pessoa de exemplo), `template.jpg` (original), logos isolados (`logo_play.png`, `logo_entrevista.png`, `logo_comunhao.png` — só a palavra Comunhão, para a capa do Short) e fontes Inter ExtraBold/SemiBold Italic. |
| `exemplos/` | Caso real (Danielle Nazário): `thumb_danielle.json`, a foto tratada, a thumb final e `shorts_danielle.json`. Use como modelo de configuração. Modelos aprovados dos Shorts: `exemplos/modelo_short_interno.jpg` e `exemplos/modelo_short_capa.jpg` (atenção: a palavra "linguágem" nos modelos está com acento errado; o certo é "linguagem"). |

Se os scripts não estiverem disponíveis, reproduza o mesmo resultado com Python (Pillow, numpy, rembg, faster-whisper) e ffmpeg, seguindo as especificações dos Passos 12 e 13. A thumb já publicada de outro vídeo (ex.: `thumb_comunhao_danielle.jpg` no Drive) serve de referência para amostrar cores e copiar os selos.

Configuração da thumb (exemplo real):
```json
{"linha1": "A fé me tirou\nda prostituição", "linha2": "Danielle Nazário",
 "foto": "recorte.png", "foto_h": 880, "foto_right": -190,
 "corpo1": 44, "corpo2": 24, "track": -1.6, "lh": 0.88, "gap": 0.34}
```

## Sobre a marca

A Revista Comunhão existe desde 1997 e apoia a família cristã e a Igreja no Brasil e em países de língua portuguesa. Os temas centrais são vida conjugal, educação de filhos, questões sociais, fé, Igreja e temas globais que afetam famílias e igrejas. O tom é acolhedor, sério e fundamentado — nunca sensacionalista. Pode despertar curiosidade, mas não promete o que o vídeo não entrega.

## Regra de ouro

**Nunca invente** tempos de capítulo, links, episódios do Spotify, dados, citações ou credenciais do convidado. Quando faltar a informação, deixe marcado e avise o que precisa ser preenchido.

## O que reunir antes de começar

- **Tema do vídeo** (obrigatório)
- **Convidado(s)**: nome e credencial
- **Formato**: entrevista, reflexão, estudo bíblico, reportagem, corte/Short, podcast
- **Transcrição com minutagem** — base dos capítulos, da manchete da thumb e dos Shorts. Se tiver acesso ao vídeo, busque você mesmo (ver Passo 4)
- **Playlist(s)** em que o vídeo está — base da tela final e da checagem de editoria
- **Episódio correspondente no Spotify**, se existir

Se só vier o tema, entregue assim mesmo e indique o que melhoraria com mais informação. Não trave o trabalho esperando dados.

## Passo 1 — Palavra-chave

Defina **uma palavra-chave principal**: o termo que uma pessoa comum digitaria no YouTube para achar esse conteúdo. Pense na dor ou na pergunta, não no nome do programa.

- Bom: "educação de filhos", "crise no casamento", "ansiedade e fé", "testemunho de conversão"
- Ruim: "Edição 327", "Bate-papo com Fulano", "Comunhão Entrevista"

Escolha também 2 ou 3 palavras-chave secundárias.

## Passo 2 — Títulos

Entregue **5 opções**, cada uma com um ângulo diferente, e indique a recomendada.

**Regras obrigatórias**
- Palavra-chave principal nos **primeiros 40 caracteres**
- Máximo de **70 caracteres**
- Nome do convidado só **depois** do tema, e só se ele for conhecido do público
- Nunca começar com "Comunhão Entrevista" ou nome de programa
- Sem caixa-alta no título inteiro; no máximo uma palavra em destaque
- Sem clickbait enganoso
- Português correto, com acentos

**Ângulos**: Pergunta · Promessa/benefício · Lista · Contraste/tensão · Autoridade.

Mostre a contagem de caracteres ao lado de cada opção.

**Shorts**: até 40 caracteres, palavra-chave logo no início. Shorts não entram em teste A/B, capítulos, tela final nem cards.

## Passo 3 — Par de títulos para teste A/B

O Studio tem o botão **Teste A/B** logo abaixo do campo de título. Ele mostra versões diferentes para públicos diferentes e escolhe a vencedora pelo tempo de exibição.

- **Título A** = o recomendado do Passo 2 (vai no campo principal).
- **Título B** = desafiante com **ângulo diferente** (ex.: A em promessa, B em pergunta; A com o nome do convidado, B só com o tema). Trocar uma palavra não vale.
- Os dois seguem todas as regras do Passo 2 e são **coerentes com a miniatura**, sem repetir o texto dela.
- Opcional: **Título C** se houver um terceiro ângulo forte.

| Versão | Título | Caracteres | Ângulo | Hipótese |
|---|---|---|---|---|
| A | ... | 00 | Promessa | Quem busca o tema clica pelo benefício |
| B | ... | 00 | Pergunta | A dúvida gera mais curiosidade que a promessa |

Orientações: não mexer no título durante o teste; vídeo com pouco tráfego pode terminar sem vencedor; registrar o ângulo vencedor e priorizá-lo nos próximos vídeos. O Studio roda um teste por vez (título, miniatura ou os dois juntos).

## Passo 4 — Capítulos

Capítulos dividem o vídeo em blocos com título próprio, aparecem na barra de progresso e podem aparecer na busca do Google.

**De onde vem a minutagem**
1. Transcrição enviada pela equipe, com tempos; ou
2. Studio → vídeo → **Legendas** → faixa "Português (automático)" — o texto vem com tempos; ou
3. Página pública do vídeo → descrição → **Mostrar transcrição** (ou as legendas automáticas do player).

**Como dividir**
- Leia a transcrição e marque cada **mudança de assunto** (nova pergunta do entrevistador, nova fase da história, novo tema).
- Entrevistas de 30 a 50 minutos: entre **6 e 10 capítulos**. Evite capítulos com menos de 1 minuto.
- O primeiro é sempre `00:00`. Mínimo de 3 capítulos, cada um com 10 segundos ou mais (exigência do YouTube).
- Use o tempo em que o assunto **começa**, não o meio da fala.

**Como titular cada capítulo**
- 2 a 6 palavras, dizendo o assunto do bloco — não "Parte 2" nem "Pergunta 3".
- Prefira termos de busca: "Como começou na prostituição", "O momento da conversão", "Preconceito na igreja".
- Pelo menos um capítulo deve conter a palavra-chave principal ou uma secundária.
- Último bloco: "Considerações finais", "Mensagem final" ou o assunto real do encerramento.

**Capítulos automáticos**
No Studio → Detalhes → Mostrar mais → **Capítulos automáticos**, manter **"Permitir capítulos automáticos" marcado**. Ele funciona como reserva: quando a descrição traz capítulos manuais, o YouTube usa os manuais. Se não houver minutagem real, publique sem o bloco de capítulos e deixe os automáticos agirem — nunca publique marcadores `00:00` vazios.

## Passo 5 — Spotify do episódio

A mesma entrevista costuma sair como episódio no podcast da Comunhão no Spotify (programa: https://open.spotify.com/show/49HHKf3Bn0gEkTjLGU0aOQ).

- Procure o **episódio correspondente** (busca no Spotify por nome do convidado + Comunhão) e confira que é do programa Revista Comunhão. Use o link do episódio: `https://open.spotify.com/episode/[ID]`.
- Linha na descrição: `🎧 Ouça este episódio no Spotify: [link do episódio]`
- Se o episódio ainda não existir, use o link do programa com a linha `🎧 Ouça a Comunhão no Spotify:` e avise que o link deve ser trocado quando o episódio sair.

## Passo 6 — Marcação de analíticas (UTM)

Todo link para o **portal** (comunhao.com.br) e para o **Spotify** leva parâmetros UTM, para o GA4 do portal mostrar quanta visita veio de cada vídeo.

Padrão:
```
?utm_source=youtube&utm_medium=video&utm_campaign=[slug-do-video]
```
- `slug-do-video`: palavra-chave + convidado, minúsculas, sem acento, com hífen. Ex.: `testemunho-conversao-danielle-nazario`.
- Se o link já tiver `?`, use `&` antes do primeiro UTM.
- Não colocar UTM em links de Instagram, TikTok e Facebook.
- Se houver link para matéria específica do portal sobre o mesmo tema, prefira-o à home, também com UTM.

## Passo 7 — Descrição

```
[Linha 1 — resumo com a palavra-chave principal, até 150 caracteres.]

[Parágrafo 1 — o problema ou a pergunta que o vídeo responde. 2 a 3 frases.]

[Parágrafo 2 — quem é o convidado e por que vale ouvir. 2 a 3 frases.]

📌 CAPÍTULOS
00:00 [Abertura / assunto inicial]
MM:SS [Título do capítulo]
MM:SS [Título do capítulo]
...
MM:SS Considerações finais

📖 Leia mais no portal: https://comunhao.com.br/?utm_source=youtube&utm_medium=video&utm_campaign=[slug]
🎧 Ouça este episódio no Spotify: [link do episódio]?utm_source=youtube&utm_medium=video&utm_campaign=[slug]

Siga a Revista Comunhão:
Instagram: https://instagram.com/oficialcomunhao
TikTok: https://www.tiktok.com/@revistacomunhao
Facebook: https://www.facebook.com/revistacomunhao/

Desde 1997, a Revista Comunhão apoia a família cristã e a Igreja no Brasil e em países de língua portuguesa.

#RevistaComunhão #[TemaDoVídeo] #FamíliaCristã
```

- A primeira linha aparece na busca: precisa se sustentar sozinha.
- O Instagram oficial é **@oficialcomunhao** (perfil ativo, ~20 mil seguidores). **Não use @revistacomunhao**: é um perfil vazio. O portal comunhao.com.br ainda aponta para @revistacomunhao no menu de redes; se continuar assim, inclua como pendência na mensagem ao administrador.
- Como o YouTube não deixa card apontar para o Instagram (ver Passo 10), o site e o Instagram também vão no **comentário fixado** (Passo 10.1).
- No máximo 3 hashtags.

## Passo 8 — Tags

Até **500 caracteres**. Primeiro as específicas (5 a 10: palavra-chave, secundárias, convidado, variações de busca), depois a base:
```
revista comunhão, comunhão, revista cristã, família cristã, vida cristã, fé cristã, igreja, cristianismo
```

Bancos por tema:
- Casamento: casamento cristão, vida conjugal, relacionamento a dois, crise no casamento
- Filhos: educação de filhos, criação de filhos, pais cristãos, família e fé
- Igreja: liderança cristã, pastores, missões, igreja evangélica
- Sociedade: fé e sociedade, ética cristã, cristãos na política, temas atuais
- Espiritualidade: oração, estudo bíblico, devocional, saúde emocional e fé
- Testemunho: testemunho de conversão, testemunho cristão, recomeço, fé transforma vidas

Entregue separadas por vírgula, com a contagem. No Studio, o campo Tags fica em Detalhes → rolar até o fim → **Mostrar mais**.

## Passo 9 — Tela final (multitelas)

Studio → vídeo → **Tela final**. Ela aparece nos últimos 5 a 20 segundos (o vídeo precisa ter pelo menos 25 segundos). Use o modelo **"1 vídeo, 1 playlist, 1 botão de inscrição"**, durante os últimos 20 segundos:

1. **Vídeo específico** — o **mesmo vídeo do card "Próximo vídeo"** (Passo 10): o próximo vídeo da **playlist da categoria** (Passo 11). Se ele for o último da playlist, use o vídeo mais assistido dela.
2. **Playlist** — a **playlist da categoria**, para quem quiser maratonar o tema.
3. **Inscrever-se** — botão de inscrição no canal.

Regras:
- Não usar "Vídeo mais recente" nem "Melhor para o espectador" como substituto — a categoria é o que segura o espectador.
- Os elementos ficam à esquerda e não cobrem rosto nem texto importante do encerramento; confira na prévia.
- Se o canal tiver card/elemento de **Link** liberado (ver Passo 10), o modelo passa a ser "1 vídeo, 1 link, 1 botão de inscrição", com o link para comunhao.com.br.

## Passo 10 — Cards (padrão fixo, nesta ordem)

Studio → vídeo → **Editor** → **Cards de informações**. Tipos disponíveis: **Vídeo, Playlist, Canal e Link**. A mensagem personalizada e o teaser têm **no máximo 30 caracteres**; o tempo é digitado em **MM:SS:QQ** (16:40 vira `16:40:00`). Espaçar os cards em pelo menos 3 minutos e nunca usar os primeiros 30 segundos.

| # | Papel | Tipo | Destino | Mensagem / teaser | Quando |
|---|---|---|---|---|---|
| 1 | **Acesse nosso perfil** (canal) | **Canal** | Revista Comunhão (@revistacomunhaooficial) — abre a página do canal com o botão Inscrever-se | Siga o canal da Comunhão / Acesse nosso perfil | Logo após o 1º momento forte (25%–40% do vídeo) |
| 2 | **Acesse nosso site** | **Link** | comunhao.com.br (matéria do mesmo tema, com UTM) | Leia a matéria completa / Acesse comunhao.com.br | Perto da metade, quando o assunto da matéria estiver em pauta |
| 3 | **Playlist da categoria** | **Playlist** | Playlist temática (Passo 11) | Mais sobre [categoria] / Playlist [nome] | Entre o card 2 e o fim |
| 4 | **Próximo vídeo** | **Vídeo** | Próximo vídeo da playlist da categoria | Assista ao próximo / Próxima: [tema curto] | No final, logo após a mensagem final e antes da tela final |

**Limites do YouTube (não contornar):**
- **Card de Link (site)** só funciona para canais no **Programa de Parcerias do YouTube** e para **sites associados ao canal** (Studio → Configurações → Canal → Recursos avançados → Site associado). Se, ao escolher "Link", o Studio não abrir o campo de URL ou recusar o endereço, o canal ainda não está liberado: **pule o card 2**, registre a pendência ("associar comunhao.com.br ao canal / habilitar cards de link") na mensagem ao administrador e mantenha o site no comentário fixado e na descrição.
- **Instagram não pode ser destino de card** nem de tela final — o YouTube não permite redes sociais nesses elementos. Nunca escreva "Siga nosso Instagram" no teaser de um card que leva a outro lugar (é enganoso). O convite ao Instagram vai no **comentário fixado** (10.1), na descrição e nos links do banner do canal.
- Card 1 com o próprio canal funciona (testado). Se um dia o Studio recusar, use Playlist → HOME COMUNHÃO com os mesmos textos.
- Se a equipe já tiver ajustado tempos ou textos dos cards, **não sobrescreva**: compare com o padrão e só complete o que falta.

**Complemento (configuração única do canal):** Studio → Personalização → **Marca d'água do vídeo** (botão de inscrição em todos os vídeos) e **links no banner do canal** com site e Instagram @oficialcomunhao. Se ainda não estiverem ativos, inclua na mensagem ao administrador.

### 10.1 — Comentário fixado (site + Instagram)

Logo após publicar, comente no vídeo **como Revista Comunhão** e **fixe** o comentário. Modelo:
```
📖 Leia a matéria completa no portal: https://comunhao.com.br/[materia]?utm_source=youtube&utm_medium=comentario&utm_campaign=[slug]
📸 Curta e siga nosso Instagram oficial: https://instagram.com/oficialcomunhao
🔔 Inscreva-se no canal e ative o sininho!
```
Como fazer: página pública do vídeo → pause o player → role até os comentários e **espere carregar** (alguns segundos) → "Adicione um comentário…" → colar o texto → **Comentar** → ⋮ do comentário → **Fixar no topo** → confirmar. Confira se aparece "Fixado por @revistacomunhaooficial".

## Passo 11 — Playlist por categoria (checagem obrigatória)

Todo vídeo precisa estar em **duas** playlists: a do **formato** (ex.: Comunhão Entrevista) e a da **categoria temática**, usando só playlists públicas que já existem no canal (Studio → Detalhes → Playlists). A playlist da categoria alimenta os cards 3 e 4 e a tela final.

| Assunto do vídeo | Playlist da categoria | Editoria no portal |
|---|---|---|
| Casamento, filhos, família, espiritualidade no dia a dia | Comunhão Vida e Família | /categoria/vida-e-familia/ |
| Igreja, liderança, pastores, ministério, missões, fé e sociedade/política | Comunhão Igreja | /categoria/igreja/ |
| Notícias e factuais | Comunhão Notícias | /categoria/noticias/ |
| Debates com mais de um convidado | Comunhão Debate | — |
| Testemunhos de conversão e de vida | Entrevistas e testemunhos | /categoria/colunas/testemunho/ |
| Música e artistas gospel | A Música do Dia | /categoria/mercado-gospel-cristao/ |
| Devocionais | Devocional | /categoria/multimidia/devocional/ |
| Reportagens | Matérias e Reportagens | — |
| Viagens e roteiros | Comunhão Na Estrada | /categoria/na-estrada/ |

Playlists de formato: Comunhão Entrevista e HOME COMUNHÃO (complementares, não substituem a de categoria). Não use playlists privadas, não listadas ou de temporadas antigas ("Revista Comunhão" do podcast é privada; "Café da Comunhão" é não listada; "Testemunho de fé" está vazia e fora da página do canal).

- **Se a playlist da categoria não estiver marcada, não marque por conta própria:** registre como pendência e prepare a **mensagem ao administrador** (destinatários: edineim@nxte.net, audiovisual@nxte.com.br, esdrase@nxte.net), relacionando todas as pendências do processo. Mostre a mensagem e só envie com aprovação explícita.

Modelo da mensagem:
```
Assunto: Pendências de publicação — [título do vídeo]

Olá, equipe,
Na revisão do vídeo "[título]" ([link]) ficaram estas pendências:
1. Playlist: o vídeo não está em "[playlist da categoria]".
2. [outra pendência]
Podem ajustar até [prazo]? Obrigado!
```

## Passo 12 — Thumb (capa) no template Comunhão Entrevista

A thumb é uma **capa de revista**, não uma legenda. Ela vende a história em dois segundos, numa tela de celular. Pense como editor de capa: uma manchete forte, um rosto bonito e bem tratado olhando para quem rola o feed, e nada mais competindo. Por padrão, a thumb tem **duas camadas de texto: manchete e nome**. A linha de apoio é **opcional** (ver 12.3).

### 12.1 — A manchete (linha 1)

O título da thumb é uma **manchete planejada**, escrita para a capa — não precisa ser uma frase dita pelo convidado. Ela tem de ser **muito boa**: é o que decide o clique.

- **Máximo de 38 caracteres**, em **2 linhas** (padrão) ou 3 linhas, conforme a avaliação (12.6).
- Nasce da **virada da história**, do conflito central ou da promessa do vídeo. Pergunte: qual é o "antes e depois"? Qual é a frase que a pessoa contaria a um amigo depois de assistir?
- Em testemunhos, prefira a **primeira pessoa, afirmativa e direta**: soa como a voz do convidado e cria identificação imediata. Ex.: "A fé me tirou da prostituição" — sem rodeios, sem "Como" quando a afirmação é mais forte.
- Palavras concretas e verbos fortes; corte artigos e adjetivos vazios.
- Fiel ao conteúdo: a manchete resume o que o vídeo entrega, sem exagero nem promessa falsa.
- Diferente do título do YouTube: os dois se completam (o título traz a palavra-chave de busca; a thumb traz a emoção).
- Quebre as linhas por sentido, com as linhas de largura parecida; evite uma linha curta isolada ("A fé" sozinho em cima enfraquece a capa). Em 3 linhas, prefira quebras como "A Bíblia / diz em quem / votar?".

**Fórmulas que funcionam** (escolha a que a história pede):
| Fórmula | Exemplo |
|---|---|
| Afirmação em 1ª pessoa (padrão para testemunhos) | "A fé me tirou / da prostituição" |
| Antes → depois | "Da prostituição / para Jesus" |
| A virada | "Deus fechou / todas as portas" |
| A pergunta que dói | "A Bíblia / diz em quem / votar?" |
| O contraste | "Famosa na noite, / livre em Cristo" |
| A revelação | "Seu candidato / não é Deus" |
| A frase do convidado | “Deus me libertou” (só quando a fala for mais forte que qualquer manchete; fiel à transcrição) |

**Quando o nome vai em destaque:** se o convidado é conhecido do público (pastor famoso, artista, autoridade), o nome pode ser a manchete e a linha 2 vira o gancho. Caso contrário, a manchete vem primeiro e o **nome vai na linha 2**.

Entregue sempre **duas manchetes com fórmulas diferentes** (A = recomendada, B = alternativa), justificando a escolha em uma frase — servem para teste A/B de miniatura.

### 12.2 — Linha 2: o nome
- Nome do convidado (ou o gancho, se o nome for a manchete).

### 12.3 — Linha 3 (opcional): a linha de apoio
- **Por padrão, não use.** Só entra se o usuário pedir ou se a avaliação (12.6) mostrar que ela acrescenta sem pesar a capa.
- Quando usada: frase curta que reforça a história de transformação, sem repetir a manchete (ex.: "A transformação de vida da Dani"), até ~32 caracteres, inteira dentro da faixa.
- Créditos, cargos e informações técnicas nunca entram na thumb: vão na descrição.

### 12.4 — Tipografia e diagramação: Inter ITÁLICO, grande, letras coladas, bloco centralizado
| Linha | Fonte | Corpo | Entreletras (tracking) |
|---|---|---|---|
| 1 — manchete | Inter ExtraBold Italic (800) | **mínimo 38; padrão 44** | **apertado: −1,6** (letras quase coladas) |
| 2 — nome | Inter ExtraBold Italic (800) | **22 a 24** (padrão 24) | **apertado: −1,6** |
| 3 — apoio (opcional) | Inter SemiBold Italic (600) | 13 a 14 | −0,6 |

- **Sempre itálico, nunca reto.** As letras ficam **juntas, quase encostando** — é o entreletras que dá peso de capa.
- O corpo **38 é piso, não teto.** Nunca reduza a manchete abaixo de 38. Se a linha não couber, afaste a foto do convidado para a direita ou reescreva a manchete.
- **Entrelinha da manchete ~0,88 do corpo**: justa, mas sem que descendentes e acentos de uma linha encostem na linha de baixo. Espaço entre manchete e nome ~0,34 do corpo da manchete.
- **Bloco centralizado na faixa amarela:** o conjunto manchete + nome (+ apoio, se houver) fica **equilibrado no meio da faixa**, com a mesma folga em cima e embaixo. Nada encosta nas bordas da faixa, nada sai dela. Centro vertical da faixa na margem esquerda: y≈503 px.
- Na arte 1600×900, 1 unidade ≈ 3,05 px (38 → 116 px; 44 → 134 px; 24 → 73 px; entreletras −1,6 → −4,9 px). Largura máxima da manchete: ~1.000 px.
- Cor creme (#FFF4DC), sombra suave laranja-escura, texto inclinado junto com a faixa (−4,95°), alinhado à esquerda em x≈70 px.

### 12.5 — Base e imagem
**Base: o template oficial.** Use a arte do template oficial como base (1600×900). Nunca redesenhe fundo, faixa ou selos. Se o arquivo não estiver disponível, use uma thumb já publicada no template (ex.: `thumb_comunhao_danielle.jpg` no Drive): copie dela os selos e amostre as cores. Remova só o texto e a pessoa de exemplo e reconstitua a faixa e o fundo com as cores amostradas do próprio template (faixa amarelo #FBB800 → laranja/vermelho; fundo vermelho escuro com vinheta e retícula). Selo **Comunhão ENTREVISTA** (canto superior esquerdo) e **Comunhão ▶ play** (canto inferior esquerdo) ficam intactos.

**Imagem do convidado — tratamento obrigatório, nesta ordem:**
1. **Escolha do quadro:** percorra o vídeo e teste vários momentos (pause e capture em tela cheia, na maior resolução). Olhos abertos, rosto frontal, olhando para a câmera, expressão serena ou sorriso leve. Nunca rosto inclinado, olhos fechados ou boca no meio de uma palavra. Se houver foto de estúdio (inclusive na miniatura antiga do vídeo) ou da matéria da revista, prefira-a ao quadro do vídeo.
2. **Restauração do rosto com IA:** passe o quadro por um modelo de restauração facial (ex.: GFPGAN v1.4, ampliação 2×, intensidade ~0,6). Ele reduz manchas, ruído de webcam e compressão, e deixa olhos e boca mais nítidos. Regra: **embelezar sem descaracterizar** — o convidado tem de continuar reconhecível; nada de mudar formato do rosto, cor de pele, idade aparente ou traços. Se o resultado parecer artificial, reduza a intensidade (0,4–0,5). Foto de estúdio profissional dispensa esta etapa. Compare antes/depois lado a lado antes de seguir.
3. **Recorte de qualidade:** remova o fundo com modelo de segmentação (ex.: rembg isnet-general-use) **com refino de bordas (alpha matting)**, para preservar os fios de cabelo soltos em vez de cortá-los reto. Limpe restos de cenário (cantos, móveis), esfume a borda onde o corpo encosta no limite do quadro e confira o recorte sobre um fundo de cor chapada antes de compor.
4. **Tratamento de cor:** +10% de contraste, +8% de saturação, +5% de brilho, nitidez leve (unsharp mask) e tom levemente aquecido para conversar com o laranja da faixa.
5. **Integração:** luz de recorte (rim light) laranja na borda, brilho laranja suave atrás do convidado e escurecimento leve na base para fundir com o fundo.
6. **Posição:** à direita, ancorado na base, rosto no terço superior, altura ~860–880 px. O rosto nunca fica atrás do texto; se a manchete precisar de espaço, a foto vai para a direita.

#### 12.5.1 — Quadros e composição (mesmos parâmetros técnicos da skill da ES Brasil, revisados com o Mário em 17/10/2026)
- **Quadros em boa resolução sem baixar o original:** use `scripts/captura_quadros.js` no Chrome, na página pública do vídeo (o script força 1080p, pausa e salva 12 quadros entre 6% e 94% do vídeo em Downloads). Uma chamada por vídeo e verificação pelo título da aba (`CAPDONE`), porque o navegador corta chamadas longas. O servidor de trabalho não consegue baixar do YouTube; não insista por lá.
- **Escolha numa folha de contato** (`folha_de_contato.py`), nunca às cegas. Se nenhum quadro servir, capture **mais 24 quadros** em outros pontos do vídeo antes de aceitar um ruim. Critérios: rosto de frente ou 3/4, olhando para o centro da capa; olhos abertos; boca fechada ou sorriso; **sem tarja de nome** (se só houver quadro com tarja, recorte acima dela); **sem microfone na frente do rosto**; cabeça inteira no quadro; nunca o apresentador.
- **Recorte antes do rembg:** corte um retângulo de ~900–1.000 px de largura em volta da pessoa, deixando de fora microfone, copo e tarja; confira na folha que nada sobrou.
- **Cabeça nunca cortada:** nem pelo topo da capa nem pelo outro convidado. Confira o recorte sobre fundo chapado e a capa reduzida a 320×180, lembrando que o selo de duração do YouTube cobre o canto inferior direito.
- **Dois convidados:** recorte cada um separadamente e junte com `montar_dupla.py` (rostos inteiros, um ao lado do outro, olhando para o centro; quem está na frente cobre só cabelo ou ombro do outro). Na thumb, reduza a dupla (`foto_h` ~530–560) para o texto não passar por cima de cabeças; se ainda encostar, use nomes curtos ("Thiago e Thayná").
- **Mostre a grade antes de trocar no canal** sempre que forem várias capas (ver "Revisando vídeos antigos").

### 12.6 — Avaliação obrigatória: gerar, comparar, escolher

Nunca entregue a primeira versão. Para cada thumb:

1. **Gere ao menos duas composições** da mesma manchete (ex.: 2 linhas no corpo 44 × 3 linhas com corpo maior; com e sem linha de apoio, quando ela for cogitada). Quando houver duas manchetes (A e B), aplique a avaliação a cada uma.
2. **Olhe as versões lado a lado e reduzidas a 320×180** (tamanho real no celular).
3. **Dê nota de 1 a 5** em cada critério:

| Critério | Pergunta |
|---|---|
| Legibilidade no celular | Em 320×180, a manchete se lê sem esforço? |
| Impacto | A manchete é o primeiro elemento que o olho pega? |
| Equilíbrio | O bloco de texto está centralizado na faixa, com linhas de largura parecida e sem linhas encostando? |
| Hierarquia | Manchete → nome (→ apoio) ficam claramente em pesos diferentes? |
| Rosto | O rosto está livre do texto, nítido, bem tratado e reconhecível? |
| Fidelidade | A manchete corresponde ao que o vídeo entrega? |

4. **Escolha a versão com maior soma** e, se algum critério ficou abaixo de 4, corrija e reavalie (reposicionar o bloco, ajustar entrelinha, mover a foto, refazer o tratamento, reescrever a manchete).
5. Na entrega, mostre a versão escolhida e diga **em uma frase por que ela venceu** (ex.: "2 linhas no 44 ficou mais equilibrada que 3 linhas, que deixava 'A fé' isolado").

### 12.7 — Conferência final
- Manchete com corpo ≥ 38 e nome entre 22 e 24 — confira o corpo **final** renderizado, não só o pedido.
- Bloco de texto centralizado na faixa; nada encosta nos selos, no rosto nem nas bordas da faixa.
- Rosto tratado e reconhecível; recorte sem restos de fundo.
- Exportar JPG 1600×900 com menos de 2 MB.
- **Publicar no Studio** (Detalhes → Miniatura → Enviar arquivo → Salvar) e conferir a miniatura pública (`i.ytimg.com/vi/[ID]/hqdefault.jpg`).

## Passo 13 — Shorts (mínimo 3, máximo 5 por entrevista) — com capa

1. Leia a transcrição inteira e escolha de **3 a 5 trechos** que se sustentam sozinhos: começo com gancho, uma ideia completa, final que fecha.
2. Duração ideal de **30 a 60 segundos** (máximo 90). Corte no início e no fim de frases completas.
3. Evite trechos com detalhes sexuais explícitos, uso de drogas descrito em detalhe, menção a menores, nomes de terceiros, candidatos/partidos citados nominalmente ou falas fora de contexto. Prefira virada de vida, ensino bíblico, frase de impacto, conselho final.
4. Para cada Short: tempos, duração, título (até 40 caracteres, palavra-chave no início, terminando em #Shorts), **faixa de título na tela (até 30 caracteres, contando espaços, em 2 linhas)**, o **nome do convidado** (1 linha) e descrição neste modelo:
   ```
   [1–2 frases com a palavra-chave e o nome do convidado]

   ▶️ Entrevista completa: https://www.youtube.com/watch?v=[ID do vídeo completo]
   📸 Instagram oficial: https://instagram.com/oficialcomunhao
   🌐 https://comunhao.com.br/?utm_source=youtube&utm_medium=shorts&utm_campaign=[slug]

   #[Tema] #[Tema2] #RevistaComunhão
   ```
5. **Arquivo original — download liberado, sem pergunta:** Studio → vídeo → ⋮ (Opções, ao lado de Salvar) → **Baixar**. **Não pergunte "posso baixar?"**: o download do original do próprio canal já está autorizado (ver "Download liberado", na Execução completa). Avise em uma linha o que está sendo baixado (nome do arquivo, origem e tamanho) e siga. O arquivo vai para **Downloads** do computador. Peça acesso à pasta Downloads uma vez. Se o envio direto do arquivo inteiro para o ambiente de trabalho for recusado (arquivo grande ou "hardlinked"), **corte os trechos brutos no próprio computador** com ffmpeg (`-ss início -t duração -c copy`, com 1 s de folga de cada lado) e traga só os trechos.
6. **Tempo exato por palavra:** transcreva cada trecho com faster-whisper (modelo `small`, `language='pt'`, `word_timestamps=True`). Use os tempos das palavras para cortar no começo e no fim da frase e para as legendas. (Alternativa: `.srt` do Studio → Legendas → ⋮ → Baixar, com `cortar_shorts.py`.)
7. **Montagem 1080×1920 (30 fps, H.264 + AAC)** — padrão Comunhão play (modelo: `exemplos/modelo_short_interno.jpg`). Use `gerar_visual_short.py moldura` (chamado pelo `cortar_shorts.py`):
   - **Área livre do vídeo: 1260 px de altura** (y 344 a 1604), largura total, com o convidado recortado no rosto.
   - **Topo:** faixa em degradê amarelo → laranja, com a borda de baixo inclinada (−4,95°: y 455 na esquerda, 362 na direita), cobrindo o começo do vídeo.
   - **Título** (na faixa, centralizado e inclinado com ela): **Inter ExtraBold Italic, corpo 22, entrelinha 22, tracking −35, máximo 30 caracteres, 2 linhas**, cor creme.
   - **Nome** do convidado logo abaixo: **Inter ExtraBold Italic, corpo 11, tracking −35, 1 linha**.
   - Escala: a arte é uma prancheta 270×480 exportada em 4×, então **1 unidade de corpo = 4 px** (corpo 22 = 88 px; corpo 11 = 44 px; tracking −35 = −0,035 do corpo).
   - **Rodapé** (y 1604 a 1920): vermelho com retícula, filete escuro no topo e logo **Comunhão ▶ play** centralizado.
   - Legendas queimadas: Inter ExtraBold Italic, ~80 px, creme com contorno preto, blocos de até 4 palavras, terminando logo acima do rodapé (~y 1460).
   - Se o título não couber em 2 linhas com o corpo 22, **reescreva o título** — nunca reduza o corpo.
   - Se a tarja com nome/cargo do vídeo original aparecer cortada no enquadramento vertical, **desfoque a tarja** no intervalo em que ela aparece.
   - Fade de áudio de 0,15 s na entrada e 0,3 s na saída.
8. **Capa de cada Short (1080×1920, PNG)** — modelo: `exemplos/modelo_short_capa.jpg`. Use `gerar_visual_short.py capa`:
   - Fundo vermelho com retícula; logo **Comunhão** (só a palavra, amarelo) centralizado no alto (y ~207).
   - Foto do convidado de y 358 para baixo, largura total (quadro com olhos abertos e sem tarja; pode ser tratada com `tratar_foto.py`). **A foto tem de ser do próprio convidado do Short.**
   - Faixa laranja inclinada (−4,95°) de y 1228 a 1645 na esquerda, com o **mesmo título** do Short e o nome: Inter ExtraBold Italic, tracking −35, entrelinha igual ao corpo; na capa o bloco é maior, como no modelo: **título corpo 30 (120 px) e nome corpo 14 (56 px)**, ainda com no máximo 30 caracteres em 2 linhas.
   - Logo **Comunhão ▶ play** centralizado logo abaixo da faixa (y ~1697).
   - Gere todas as capas e confira lado a lado; revise a acentuação do título antes de exportar.
   Configuração (`moldura` e `capa` usam o mesmo arquivo):
   ```json
   {"titulo": "Quem domina\nsua linguagem?", "nome": "Tassos Lycurgo", "foto": "quadro_tassos.png"}
   ```
9. **Publicar (sem parar para perguntar)** — passo a passo testado:
   - **Arquivo ≤ 10 MB:** o envio pelo navegador aceita no máximo 10 MB por arquivo. Recomprima cada Short em 1080×1920 com H.264 em **duas passagens** e taxa-alvo `9,2 MB × 8 ÷ duração − 130 kbps` (áudio AAC 128k): `comprimir_envio.py pasta`. Guarde a versão cheia; suba a comprimida.
   - **Caminho do arquivo:** o envio só aceita arquivos de pasta conectada **trazidos para o ambiente de trabalho** (`/mnt/user-data/uploads/...`). Grave os comprimidos em `Downloads/shorts_[convidado]/envio/` no computador e traga-os (stage) antes de enviar. Arquivos só em `/mnt/user-data/outputs` ou com caminho do Mac são recusados — vale também para capas.
   - **"file is hardlinked":** arquivo recém-gravado no Mac pode ser recusado ao ser trazido. Regrave no próprio Mac (`sips -s format jpeg -s formatOptions 93 entrada.jpg --out saida.jpg`; para vídeo, `cp` para outro nome), **espere ~50 s** e traga de novo. Não fique repetindo na hora.
   - Studio → `.../videos/upload?d=ud` → localizar o `input type=file` e enviar o arquivo (nunca clicar no botão "Selecionar arquivos").
   - **Título e descrição:** o Studio preenche os padrões do canal alguns segundos depois de abrir a janela e sobrescreve o que foi digitado antes. Espere ~6 s, **clique de verdade no campo Título**, e só então substitua o conteúdo dos dois campos (selecionar o conteúdo do campo e inserir o texto). Releia os dois campos antes de avançar.
   - **Capa:** envie o JPG no `input type=file` da seção Miniatura.
   - Público: "Não é conteúdo para crianças" → Avançar ×3 → **Privado** → Salvar.
   - **Vídeo relacionado** não aparece na janela de envio: depois de salvar, abra a página de edição de cada Short → campo **Vídeo relacionado** → buscar colando o **link** do vídeo completo (buscar pelo título novo costuma não achar) → escolher → Salvar. A janela de escolha às vezes abre duas vezes; digite na que está visível.
   - **Conferência:** Conteúdo → aba Shorts. Todos devem estar "Privado" (se algum ficar "Rascunho", abra "Editar rascunho" e conclua). Se a miniatura de algum aparecer em branco, reenvie a capa na página de edição do Short e salve.
   - Tornar público só com aprovação.
10. Salve os Shorts e as capas também em `Downloads/shorts_[convidado]/` no computador.

## Formato da entrega

Em blocos fáceis de copiar, nesta ordem:

1. Palavra-chave principal e secundárias
2. 5 títulos (com caracteres) + recomendado
3. Teste A/B: tabela A/B (e C)
4. Capítulos: lista com tempos reais e títulos (ou aviso de que não há minutagem)
5. Descrição completa, já com capítulos, Spotify do episódio e UTMs
6. Tags + contagem
7. Tela final: vídeo sugerido, playlist, inscrição, tempo de início
8. Cards: tabela no padrão do Passo 10 (perfil/canal, site, playlist da categoria, próximo vídeo) + comentário fixado com site e Instagram
9. Playlists: marcadas x corretas (formato + categoria), pendências e mensagem ao administrador (se houver)
10. Thumb: versão escolhida após a avaliação (12.6), com a fórmula da manchete e a frase que explica por que venceu
11. Shorts: tabela com 3 a 5 recortes (tempos, título, gancho) + capas
12. Checklist de publicação:
    - Palavra-chave no título, na 1ª linha da descrição, em um capítulo e nas tags
    - Teste A/B configurado
    - Capítulos com tempos reais e "Permitir capítulos automáticos" marcado
    - Links do portal e do Spotify com UTM
    - Link do episódio no Spotify (ou programa, com aviso)
    - Vídeo na playlist de formato e na da categoria (ou pendência ao administrador)
    - Thumb sobre a arte do template: manchete planejada (≤ 38 caracteres, corpo ≥ 38), nome em 22–24, linha de apoio só se pedida, Inter itálico com letras coladas, bloco centralizado na faixa, foto tratada e bem recortada, versão escolhida por avaliação
    - Capa publicada no Studio
    - Original baixado pelo Studio (download liberado) e trechos cortados
    - 3 a 5 Shorts no padrão Comunhão play (vídeo na área de 1260 px; título Inter corpo 22 / entrelinha 22 / tracking −35, até 30 caracteres em 2 linhas; nome corpo 11), com legenda e capa no modelo aprovado, publicados como privados, com vídeo relacionado
    - Tela final com o próximo vídeo da playlist da categoria + essa playlist + inscrição
    - Cards: perfil (canal), site (se liberado), playlist da categoria, próximo vídeo
    - Comentário fixado com site e Instagram @oficialcomunhao

## Aplicando no Studio

Na execução completa, salve direto (ver "Execução completa"); em pedidos avulsos, mostre o pacote antes de salvar. Depois de salvar, recarregar a página e conferir título, descrição, tags, tela final e cards (os cards podem levar alguns minutos para aparecer na página pública).

**Notas práticas (aprendidas na execução):**
- Título e descrição são campos editáveis do tipo `#textbox`. Selecione todo o conteúdo e substitua de uma vez; "Ctrl+A + digitar" pode inserir o texto no meio do antigo. Se isso acontecer, use **Desfazer alterações** e refaça.
- Depois de clicar em **Salvar**, espere alguns segundos antes de recarregar — recarregar cedo demais descarta a alteração.
- Tags ficam em **Mostrar mais** → Tags. O botão "Remover tudo" limpa as antigas.
- Card: tempo em `MM:SS:QQ` e mensagem com até 30 caracteres (ver Passo 10).
- **Teste A/B:** o Studio roda **um teste por vez** por vídeo. Com teste de título em andamento, a capa pode ser trocada normalmente (vale para todas as variantes); um teste de **miniatura** só começa depois que o de título terminar.
- **Download do original (liberado):** ⋮ (Opções, ao lado de Salvar) → Baixar, sem pedir confirmação. Se o primeiro clique só fechar o menu, abra o menu de novo e clique em Baixar; confira em Downloads se surgiu o `.crdownload` e espere ele virar `.mp4` antes de cortar.
- **Transcrição com minutagem:** se o painel de transcrição não abrir, ligue as legendas no player; a requisição de legenda (`timedtext`) traz o texto com tempos.
- **Trocar a miniatura:** página de edição → localizar o `input type=file` da seção Miniatura (a página às vezes demora; espere ~8 s e procure de novo) → enviar o JPG trazido para `/mnt/user-data/uploads/...` → esperar ~5 s → **Salvar** → conferir que o botão Salvar voltou a ficar desativado. Vale também para vídeos não listados.
- **Vídeo relacionado do Short:** no seletor, a busca pelo link mostra um cartão com a miniatura; clique no cartão (nem sempre há item com `role=option`) e salve.
- **Short antigo substituído:** passe para **Privado** (Visibilidade → Privado → Concluir → Salvar) e confira em Conteúdo → Shorts. Nunca exclua.
- **Legendas `.srt`:** o `cortar_shorts.py` aceita tempos com vírgula ou ponto (`00:00:02,000` ou `00:00:02.000`) e arquivos com quebra de linha do Windows.

## Execução completa ("rode a skill neste vídeo") — ponta a ponta, sem paradas

Pedir para rodar a skill num vídeo **é a autorização** para fazer, sem parar para perguntar a cada etapa: salvar título/descrição/tags, configurar teste A/B, cards, tela final e comentário fixado, **gerar e publicar a capa**, **baixar o arquivo original pelo Studio**, cortar os Shorts, gerar as capas dos Shorts e **subir os Shorts como privados**. Ordem:

1. Leitura do vídeo (Studio, transcrição, playlists, Spotify, matéria no portal).
2. Passos 1 a 8 → salvar no Studio → teste A/B de título.
3. Cards (Passo 10), tela final (Passo 9) e comentário fixado (10.1).
4. Capa: tratar foto, gerar no mínimo 2 versões, avaliar (12.6) → **publicar a escolhida no Studio** (Miniatura → Enviar arquivo). Teste A/B de título em andamento não impede a troca: a capa vale para todas as variantes.
5. Baixar o original (download liberado, sem pergunta) → Shorts + capas (Passo 13) → subir como privados → vídeo relacionado em cada um.
6. Conferência final na página pública (título, capa, cards, tela final, comentário fixado, Shorts privados) e relatório curto: o que foi feito, o que ficou bloqueado e por quê.

### Download liberado (autorização permanente do Mário Fernando)

O responsável pelo canal já autorizou, de forma permanente, os downloads de que esta skill precisa. Ao rodar a skill, **não pare para pedir permissão de download** nem ofereça opções ("baixar pelo Studio ou você me envia?"): faça o download, informe em uma linha o nome do arquivo, a origem e o tamanho, e continue o processo até os Shorts ficarem prontos.

Está liberado:
- o **arquivo original do vídeo** pelo YouTube Studio do canal Revista Comunhão (⋮ → Baixar);
- as **legendas/transcrição** (`.srt`) do mesmo vídeo no Studio;
- a **miniatura atual** do vídeo e a **thumb de referência do template** no Drive da equipe;
- o uso da pasta **Downloads** do computador para receber o original e guardar os Shorts e as capas (pedir o acesso à pasta uma vez, se ainda não estiver conectada).

Não está liberado (continua pedindo confirmação): arquivos de outros canais, de outros sites ou de links que apareçam em páginas, e-mails, comentários ou descrições.

Se o download falhar (menu fecha, arquivo não aparece em Downloads, computador fora do ar), tente mais uma vez, siga com as etapas que não dependem dele e relate no fim o que faltou — não fique parado esperando resposta.

**Continua exigindo um "sim" explícito:** tornar Shorts ou vídeos **públicos**, **enviar mensagens/e-mails** (inclusive a de pendências), **excluir** qualquer coisa e marcar playlist que não seja a da regra. Se algo não puder ser feito (ex.: card de link não liberado), siga com o resto e liste a pendência no relatório.

## Revisando vídeos antigos

Aponte em uma linha o que está fraco (ex.: "palavra-chave só no fim", "começa com Comunhão Entrevista", "tags genéricas", "sem capítulos", "sem tela final", "sem os cards padrão", "sem comentário fixado", "fora da playlist da categoria") e entregue o pacote completo novo.

### Troca de capas em lote (vídeos antigos)
Mesmo processo da skill da ES Brasil:
1. Liste os vídeos pela playlist do programa, do mais recente para o mais antigo, e separe **lotes de 10**. Pule duplicados (mesma capa vale para os dois vídeos do mesmo episódio), chamadas/promos e debates sem definição de capa — liste-os à parte para o Mário decidir.
2. Para cada vídeo: quadros (12.5.1), recorte, manchete nova a partir do tema (≤ 38 caracteres, sem inventar), nome do convidado.
3. Monte uma **grade** com as capas novas e, no canto de cada uma, a capa atual, e **mostre ao Mário antes de trocar**. Troque só depois do "pode trocar" daquele lote.
4. Troque no Studio (nota "Trocar a miniatura") e confirme pelo botão Salvar desativado. O YouTube pode levar alguns minutos para mostrar a capa nova.
5. Guarde as capas em `Downloads/comunhao_capas/<lote>/`. Nunca exclua nada; Short antigo substituído vai para Privado.