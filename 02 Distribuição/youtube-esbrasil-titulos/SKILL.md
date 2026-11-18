---
name: "youtube-esbrasil-titulos"
description: "Publica de ponta a ponta um vídeo do canal Revista ES Brasil no YouTube: títulos A/B, descrição, capítulos, tags, cards, tela final, playlists, capa nos templates ES Brasil Entrevista, Destinos ES e Café com Moqueca, e 3 a 5 Shorts no corte limpo dos Reels, com capa oficial. Pergunta o tipo de capa no início e pede ok antes de salvar no Studio. Download do original já liberado."
---

# Pacote de publicação no YouTube — Revista ES Brasil

Esta skill padroniza a forma como a equipe publica os vídeos do canal oficial da ES Brasil (youtube.com/@RevistaESBrasil — ID do canal `UCKhj3LkxBnIQ7oU6hZED_nA`): título, teste A/B, descrição, capítulos, links rastreados, tags, Spotify, tela final, cards, playlist, capa e Shorts. O objetivo é fazer cada vídeo ser encontrado na busca do YouTube e do Google, ser clicado por quem vê a miniatura e levar o espectador para o próximo vídeo, para o canal e para o portal esbrasil.com.br.

Use SEMPRE que alguém da equipe pedir título de vídeo, sugestão de título, teste A/B, descrição de YouTube, tags, capítulos, tela final, cards, playlist, thumb/capa, Shorts/cortes ou "subir vídeo" da ES Brasil — mesmo que mande só o tema, o nome do convidado, uma transcrição ou um link. Vale para todos os programas do canal: ES Brasil Entrevista, Café com Moqueca, ES Brasil Debate, Destinos ES, Diálogos ES Brasil (podcast), Direito ao Direito, reportagens e eventos.

É a versão ES Brasil da skill `youtube-comunhao-titulos`. O processo é o mesmo; mudam a marca, o tom, os links, as playlists e a arte. Para vídeos do canal Revista Comunhão, use a outra skill.

## Ferramentas

**Kit de artes do canal.** A skill salva guarda só estas instruções; as artes e os scripts ficam numa pasta do computador do Mário Fernando:

`~/Documents/Claude Skills/youtube-esbrasil-titulos/`

| Arquivo | Para quê |
|---|---|
| `assets/thumbs/entrevista.png` | Base da capa **ES Brasil Entrevista** (1600×900), sem texto e sem convidado. Selos prontos. |
| `assets/thumbs/destinos.png` | Base da capa **Destinos ES**: logo, apresentadora (Kamila Rangel) e ES BRASIL play prontos. |
| `assets/thumbs/cafe.png` | Base da capa **Café com Moqueca**: logo, apresentador (Renzo Colnago) e ES BRASIL play prontos. |
| `assets/shorts/moldura_esbrasil.png`, `moldura_destinos.png` | Fora de uso desde 18/11/2026: os Shorts saem no corte limpo, sem moldura (Passo 13). Guardadas só como referência. |
| `assets/shorts/capa_esbrasil.png`, `capa_destinos.png` | Bases das capas (thumbs) dos Shorts, com janela transparente para a foto. |
| `assets/referencias/` | As artes originais enviadas pelo Mário (02/10/2026). São o gabarito visual. |
| `assets/fonts/` | Inter ExtraBold Italic, Inter SemiBold Italic e Inter ExtraBold. |
| `scripts/gerar_thumb_esbrasil.py config.json saida.png` | Monta a capa 1600×900 no template `entrevista`, `destinos` ou `cafe`. Avisa quando a manchete passa da largura útil. Requer `pip install playwright` + Chromium. |
| `scripts/gerar_short_esbrasil.py moldura\|capa config.json saida.png` | Gera a capa do Short (foto + título + nome), marca `esbrasil` ou `destinos`. O modo `moldura` saiu de uso em 18/11/2026 (corte limpo). |
| `scripts/montar_short.py video.mp4 INICIO FIM moldura.png saida.mp4 [centro_x] [legendas.srt]` | Versão antiga, com moldura: não usar. A montagem do corte limpo é o comando ffmpeg do Passo 13, item 7. |
| `scripts/tratar_foto_esbrasil.py quadro.png recorte.png [0.6]` | Restauração do rosto (GFPGAN, opcional), recorte com refino de cabelo e cor neutra. Requer `rembg`; para a restauração, `gfpgan` e os pesos em `weights/GFPGANv1.4.pth`. |
| `exemplos/` | Configurações e artes de teste de cada template. |

Como usar: peça acesso à pasta **Documents** uma vez, traga o kit para o ambiente de trabalho mantendo a estrutura `assets/` e `scripts/`, e rode os scripts lá. Exemplos de configuração:
```json
{"template": "cafe", "linha1": "Inovação\nno campo", "linha2": "Nome do Convidado",
 "foto": "recorte.png", "foto_h": 860, "foto_right": -20}
```
```json
{"marca": "esbrasil", "titulo": "Quem domina\nsua linguagem?", "nome": "Nome do Convidado",
 "foto": "quadro.png", "centro_x": 0.5, "centro_y": 0.42}
```

No template `destinos`, ponha sempre `"lh": 0.92` no config (entrelinha justa, desde 16/11/2026), mesmo que o script do kit seja de antes dessa data:
```json
{"template": "destinos", "linha1": "Turismo, o motor\nda Barra", "linha2": "Erivan Tavares",
 "foto": "recorte.png", "foto_h": 860, "foto_right": -20, "lh": 0.92}
```

Se a pasta do kit não estiver acessível (computador desligado, sessão sem vínculo com o computador, outro usuário da equipe), **não improvise a arte**: entregue manchetes, nomes e foto tratada, registre "capa e Shorts no template" como pendência e avise que o kit está no computador do Mário.

Regras que valem sempre:
- **Bases reconstruídas.** As bases das capas e das capas de Shorts foram refeitas a partir das artes de referência (texto e convidado de exemplo removidos). Nas capas Destinos ES e Café com Moqueca a textura da faixa ficou lisa onde havia texto. Quando o design enviar as artes limpas, basta substituir os arquivos em `assets/` (mesmo nome e tamanho).
- **Nunca** use arte, cores, faixa amarela, luz laranja ou logos da Comunhão em peça da ES Brasil.
- **Logos, selos e apresentadores** vêm prontos nas bases. Nunca redesenhe um logo. Em qualquer peça fora destes templates, use o arquivo oficial (pacote de logos da skill `documentos-next-editorial` ou arquivo enviado pela equipe); sem arquivo, a peça sai sem logo e isso vira pendência.

## Sobre a marca

A ES Brasil é a revista de economia, política e infraestrutura do Espírito Santo, com alcance nacional. Assinatura: "Quem decide lê. Quem lê decide." O público é formado por lideranças, empresários, gestores públicos e tomadores de decisão.

O tom é estratégico, analítico e premium: informa com autoridade e respeita o tempo de quem decide. Clareza acima de ornamento. Pode despertar curiosidade, mas não promete o que o vídeo não entrega.

Regras de marca:
- Sempre "ES Brasil" — nunca "S Brasil", "Es Brasil" ou "ESBrasil" em texto corrido.
- Em relatórios e mensagens à equipe, **ES Brasil**, **revista ES Brasil** e **Café com Moqueca** vão em negrito. Nos campos do YouTube (título, descrição, tags) não existe negrito: escreva normalmente.
- Sem emojis em título, descrição e comentário fixado. A marca usa rótulos em texto ("CAPÍTULOS", "Leia mais").
- Sem caixa-alta gritada, sem adjetivo vazio, sem tom de torcida.

## Regra de ouro

**Nunca invente** tempos de capítulo, links, episódios do Spotify, dados, citações ou credenciais do convidado. Em jornalismo econômico isso vale em dobro: **nenhum número, índice, percentual, valor de investimento, projeção ou data entra em título, capa, descrição ou Short se não tiver sido dito no vídeo** — e sempre com o contexto em que foi dito (período, fonte, base de comparação). Cargo e empresa do convidado saem do próprio vídeo, da matéria do portal ou do que a equipe informar. Quando faltar a informação, deixe marcado e avise o que precisa ser preenchido.

## Cuidados editoriais (política e negócios)

- **Política e eleições:** título, capa e Shorts descrevem o tema; não julgam nem favorecem candidato, partido ou governo. Nada de adjetivo sobre pessoas públicas. Pesquisa eleitoral só com o nome do instituto e o recorte ditos no vídeo; nunca transforme análise em previsão de resultado. Em período eleitoral, não use como Short trecho com pedido de voto, ataque a adversário nomeado ou número de pesquisa solto.
- **Empresas e convidados:** o vídeo é jornalismo, não publicidade. Não escreva título ou descrição em tom de anúncio da empresa do convidado. Se o conteúdo for patrocinado ou de projeto especial, mantenha a identificação que a equipe indicar e marque "Inclui promoção paga" no Studio quando for o caso — pergunte se houver dúvida.
- **Terceiros:** acusação ou crítica a pessoa ou empresa nomeada não vira título, capa nem Short.

## O que reunir antes de começar

- **Tema do vídeo** (obrigatório)
- **Programa/formato**: ES Brasil Entrevista, Café com Moqueca, ES Brasil Debate, Destinos ES (com o número do episódio), Diálogos ES Brasil, Direito ao Direito, reportagem, evento, corte/Short
- **Convidado(s)**: nome, cargo e empresa/instituição
- **Apresentador(a)**, quando o programa tiver
- **Transcrição com minutagem** — base dos capítulos, da manchete da capa e dos Shorts. Se tiver acesso ao vídeo, busque você mesmo (ver Passo 4)
- **Playlist(s)** em que o vídeo está — base da tela final e da checagem de editoria
- **Matéria correspondente no portal** (esbrasil.com.br) e **episódio no Spotify**, se existirem

Se só vier o tema, entregue assim mesmo e indique o que melhoraria com mais informação. Não trave o trabalho esperando dados.

## Antes de executar — as duas paradas obrigatórias

**1. No início, pergunte o tipo de capa.** Antes de qualquer outra etapa, pergunte (uma vez só) qual é o tipo do vídeo, porque cada tipo tem a sua arte:

| Resposta | Capa do vídeo | Capa dos Shorts |
|---|---|---|
| **ES Brasil Entrevista** | Template `entrevista` — a skill gera e publica. | ES Brasil (azul) |
| **Destinos ES** | Template `destinos` — a skill gera e publica. | Destinos ES (rosa/roxo) |
| **Café com Moqueca** | Template `cafe` — a skill gera e publica. | ES Brasil (azul), até existir capa própria |
| **Coluna** | Arte própria das colunas, ainda não incluída — entregar só textos e foto tratada. | ES Brasil (azul) |
| **Outro programa ou quadro** (ES Brasil Debate, Diálogos ES Brasil, Direito ao Direito, reportagem, evento) | Arte própria, ainda não incluída — entregar só textos e foto tratada. | ES Brasil (azul) |

Não deduza pelo título nem pela playlist: pergunte. Só dispense a pergunta quando o pedido já disser com todas as letras o tipo de capa. Cada template vale **apenas** para o seu programa; outro quadro só passa a usar um deles quando o Mário Fernando indicar.

**2. No fim, peça o ok antes de salvar no Studio.** Monte o pacote inteiro, mostre e **só altere o canal depois do ok explícito** (ver "Execução completa"). Enquanto o ok não vem, nada é salvo, enviado nem publicado no YouTube.

## Passo 1 — Palavra-chave

Defina **uma palavra-chave principal**: o termo que um empresário, gestor ou leitor interessado digitaria no YouTube ou no Google para achar esse conteúdo. Pense no assunto e na pergunta, não no nome do programa.

- Bom: "mercado imobiliário no ES", "pesquisas eleitorais", "reforma tributária", "inovação no Espírito Santo", "exportação de rochas", "El Niño no ES"
- Ruim: "ES Brasil Entrevista", "Café com Moqueca", "Bate-papo com Fulano", "Edição 250"

**O recorte geográfico faz parte da palavra-chave.** Quase toda busca relevante para o canal tem "ES", "Espírito Santo", "capixaba" ou o nome do município. Use "no ES" no título (economiza caracteres) e "Espírito Santo" por extenso na primeira linha da descrição e nas tags.

Escolha também 2 ou 3 palavras-chave secundárias (setor, empresa/instituição do convidado, termo técnico do tema).

## Passo 2 — Títulos

Entregue **5 opções**, cada uma com um ângulo diferente, e indique a recomendada.

**Regras obrigatórias**
- Palavra-chave principal nos **primeiros 40 caracteres**
- Máximo de **70 caracteres**
- **Nunca começar com o nome do programa** ("ES Brasil Entrevista –", "Entrevista ES Brasil:", "Café com Moqueca –", "Destinos ES:"). Hoje quase todos os títulos do canal começam assim: é o principal ponto a corrigir.
- O nome do programa pode ir **no fim**, se couber: "… | Café com Moqueca", "… | Destinos ES #68". Se não couber, fica só na descrição e na playlist.
- Nome do convidado **depois** do tema. No canal da ES Brasil o convidado costuma ser uma liderança e o nome é termo de busca: inclua-o quando couber. Cargo e empresa só entram no título quando a empresa/instituição for o que o público busca (ex.: "Galwan", "Findes", "Sebrae"); senão ficam na descrição.
- Sem caixa-alta no título inteiro; no máximo uma palavra em destaque
- Sem clickbait enganoso, sem adjetivo de torcida, sem emoji
- Número no título só se foi dito no vídeo (Regra de ouro)
- Português correto, com acentos

**Ângulos**: Pergunta · Dado/número · Explicação ("como", "por que", "o que muda") · Contraste/tensão · Autoridade (quem fala e por que importa).

Exemplo de reescrita: de "ES Brasil Entrevista – José Luiz Galvêas, Fundador da Galwan" para "Mercado imobiliário no ES: o que muda, com José Luiz Galvêas".

Mostre a contagem de caracteres ao lado de cada opção.

**Shorts**: até 40 caracteres, palavra-chave logo no início. Shorts não entram em teste A/B, capítulos, tela final nem cards.

## Passo 3 — Par de títulos para teste A/B

O Studio tem o botão **Teste A/B** logo abaixo do campo de título. Ele mostra versões diferentes para públicos diferentes e escolhe a vencedora pelo tempo de exibição.

- **Título A** = o recomendado do Passo 2 (vai no campo principal).
- **Título B** = desafiante com **ângulo diferente** (ex.: A em explicação, B em pergunta; A com o nome do convidado, B só com o tema). Trocar uma palavra não vale.
- Os dois seguem todas as regras do Passo 2 e são **coerentes com a miniatura**, sem repetir o texto dela.
- Opcional: **Título C** se houver um terceiro ângulo forte.

| Versão | Título | Caracteres | Ângulo | Hipótese |
|---|---|---|---|---|
| A | ... | 00 | Explicação | Quem busca o tema clica pela resposta |
| B | ... | 00 | Pergunta | A dúvida gera mais curiosidade que a explicação |

Orientações: não mexer no título durante o teste; vídeo com pouco tráfego pode terminar sem vencedor; registrar o ângulo vencedor e priorizá-lo nos próximos vídeos. O Studio roda um teste por vez (título, miniatura ou os dois juntos).

## Passo 4 — Capítulos

Capítulos dividem o vídeo em blocos com título próprio, aparecem na barra de progresso e podem aparecer na busca do Google.

**De onde vem a minutagem**
1. Transcrição enviada pela equipe, com tempos; ou
2. Studio → vídeo → **Legendas** → faixa "Português (automático)" — o texto vem com tempos; ou
3. Página pública do vídeo → descrição → **Mostrar transcrição** (ou as legendas automáticas do player).

**Como dividir**
- Leia a transcrição e marque cada **mudança de assunto** (nova pergunta do entrevistador, novo setor, novo dado, nova fase da conversa).
- Entrevistas de 30 a 60 minutos: entre **6 e 10 capítulos**. Evite capítulos com menos de 1 minuto.
- O primeiro é sempre `00:00`. Mínimo de 3 capítulos, cada um com 10 segundos ou mais (exigência do YouTube).
- Use o tempo em que o assunto **começa**, não o meio da fala.

**Como titular cada capítulo**
- 2 a 6 palavras, dizendo o assunto do bloco — não "Parte 2" nem "Pergunta 3".
- Prefira termos de busca: "Juros e crédito imobiliário", "Incorporação por administração", "Cenário eleitoral no ES", "Tendências para 2027".
- Pelo menos um capítulo deve conter a palavra-chave principal ou uma secundária.
- Último bloco: "Considerações finais", "Perspectivas" ou o assunto real do encerramento.

**Capítulos automáticos**
No Studio → Detalhes → Mostrar mais → **Capítulos automáticos**, manter **"Permitir capítulos automáticos" marcado**. Ele funciona como reserva: quando a descrição traz capítulos manuais, o YouTube usa os manuais. Se não houver minutagem real, publique sem o bloco de capítulos e deixe os automáticos agirem — nunca publique marcadores `00:00` vazios.

## Passo 5 — Spotify do episódio

A ES Brasil tem um programa no Spotify: "Revista ES Brasil - Podcasts" (https://open.spotify.com/show/0F9mlRN62BTxnA00Nh48B9). No YouTube, o podcast do canal é a playlist "Diálogos ES Brasil".

- Procure o **episódio correspondente** (busca no Spotify por nome do convidado + ES Brasil) e confira que é do programa da ES Brasil. Use o link do episódio: `https://open.spotify.com/episode/[ID]`.
- Linha na descrição: `Ouça este episódio no Spotify: [link do episódio]`
- Se o episódio não existir, **confira primeiro se o programa está sendo atualizado**. Se estiver, use o link do programa com a linha `Ouça a ES Brasil no Spotify:` e avise que o link deve ser trocado quando o episódio sair. Se o programa estiver parado, **não inclua a linha do Spotify** e registre no relatório.

## Passo 6 — Marcação de analíticas (UTM)

Todo link para o **portal** (esbrasil.com.br) e para o **Spotify** leva parâmetros UTM, para o GA4 do portal mostrar quanta visita veio de cada vídeo.

Padrão:
```
?utm_source=youtube&utm_medium=video&utm_campaign=[slug-do-video]
```
- `slug-do-video`: palavra-chave + convidado, minúsculas, sem acento, com hífen. Ex.: `mercado-imobiliario-es-jose-luiz-galveas`.
- Se o link já tiver `?`, use `&` antes do primeiro UTM.
- Não colocar UTM em links de Instagram, TikTok, Facebook e X.
- Se houver matéria específica do portal sobre o mesmo tema, prefira-a à home, também com UTM. Sem matéria, use a editoria (ex.: `https://esbrasil.com.br/economia/`) em vez da home.

## Passo 7 — Descrição

```
[Linha 1 — resumo com a palavra-chave principal e "Espírito Santo", até 150 caracteres.]

[Parágrafo 1 — a pergunta ou o problema que o vídeo responde e por que importa para quem decide. 2 a 3 frases.]

[Parágrafo 2 — quem é o convidado (nome, cargo, empresa/instituição) e por que vale ouvir. 2 a 3 frases.]

[Linha do programa — ex.: "Café com Moqueca é o programa de entrevistas da ES Brasil, com apresentação de [nome]." Só com dados confirmados.]

CAPÍTULOS
00:00 [Abertura / assunto inicial]
MM:SS [Título do capítulo]
MM:SS [Título do capítulo]
...
MM:SS Considerações finais

Leia mais no portal: https://esbrasil.com.br/[materia-ou-editoria]/?utm_source=youtube&utm_medium=video&utm_campaign=[slug]
Ouça este episódio no Spotify: [link do episódio]?utm_source=youtube&utm_medium=video&utm_campaign=[slug]

Siga a ES Brasil:
Instagram: https://instagram.com/revistaesbrasil
TikTok: https://tiktok.com/@revistaesbrasil
Facebook: https://www.facebook.com/esbrasil
X: https://x.com/esbrasil

ES Brasil — economia, política e infraestrutura do Espírito Santo. Quem decide lê. Quem lê decide.

#ESBrasil #[TemaDoVídeo] #EspíritoSanto
```

- A primeira linha aparece na busca: precisa se sustentar sozinha.
- **O link do portal vai escrito por extenso.** As descrições atuais trazem "Acesse nosso portal: ES Brasil" sem endereço — é texto morto. Sempre a URL completa, com UTM.
- Não repetir o bloco genérico "Gostou do vídeo? Deixe seu like…": o convite à inscrição vai no comentário fixado, no card do canal e na tela final.
- Como o YouTube não deixa card apontar para redes sociais (ver Passo 10), o site e o Instagram também vão no **comentário fixado** (Passo 10.1).
- No máximo 3 hashtags.

## Passo 8 — Tags

Até **500 caracteres**. Primeiro as específicas (5 a 10: palavra-chave, secundárias, convidado, empresa/instituição, variações de busca), depois a base:
```
es brasil, revista es brasil, espírito santo, economia capixaba, economia do espírito santo, negócios no es, notícias do es
```

**Apague as tags padrão do canal.** Hoje todos os vídeos sobem com o mesmo conjunto genérico ("vida capixaba, cotidiano, economia, espirito santo, educação, artigos, politica"), que vem do padrão de envio do Studio. Use "Remover tudo" e cole as novas. Inclua na mensagem ao administrador a sugestão de limpar esse padrão em Studio → Configurações → Padrões de envio.

Bancos por tema:
- Economia e negócios: economia capixaba, negócios no es, empresas capixabas, investimentos no espírito santo, mercado capixaba
- Indústria: indústria capixaba, indústria do espírito santo, findes, setor industrial
- Agro: agronegócio capixaba, agro es, café conilon, agricultura no espírito santo
- Comércio e serviços: comércio capixaba, varejo no es, serviços, consumo
- Logística e infraestrutura: infraestrutura no es, portos do espírito santo, logística capixaba, rodovias, ferrovia, mobilidade
- Comércio exterior: exportação capixaba, comércio exterior es, importação, rochas naturais, rochas ornamentais
- Energia e saneamento: energia no es, petróleo e gás, saneamento, energia renovável
- Mercado imobiliário: mercado imobiliário no es, construção civil, imóveis em vitória, incorporação
- Política: política capixaba, política no espírito santo, eleições no es, governo do es, assembleia legislativa, municípios capixabas
- Ciência, tecnologia e inovação: inovação capixaba, tecnologia no es, startups capixabas, inteligência artificial
- ESG e sustentabilidade: esg, sustentabilidade, meio ambiente no es
- Turismo (Destinos ES): turismo no espírito santo, destinos es, turismo capixaba, o que fazer no es, praias do espírito santo
- Vida capixaba e cultura: vida capixaba, cultura capixaba, gastronomia capixaba, vitória es

Use o nome de entidade ou sigla só quando ela for assunto do vídeo. Entregue as tags separadas por vírgula, com a contagem. No Studio, o campo Tags fica em Detalhes → rolar até o fim → **Mostrar mais**.

## Passo 9 — Tela final (multitelas)

Studio → vídeo → **Tela final**. Ela aparece nos últimos 5 a 20 segundos (o vídeo precisa ter pelo menos 25 segundos). Use o modelo **"1 vídeo, 1 playlist, 1 botão de inscrição"**, durante os últimos 20 segundos:

1. **Vídeo específico** — o **mesmo vídeo do card "Próximo vídeo"** (Passo 10): o próximo vídeo da **playlist da categoria** (Passo 11). Se ele for o último da playlist, use o vídeo mais assistido dela.
2. **Playlist** — a **playlist da categoria**, para quem quiser maratonar o tema.
3. **Inscrever-se** — botão de inscrição no canal.

Regras:
- Não usar "Vídeo mais recente" nem "Melhor para o espectador" como substituto — a categoria é o que segura o espectador.
- Os elementos não cobrem rosto nem texto importante do encerramento; confira na prévia.
- Se o canal tiver card/elemento de **Link** liberado (ver Passo 10), o modelo passa a ser "1 vídeo, 1 link, 1 botão de inscrição", com o link para esbrasil.com.br.

## Passo 10 — Cards (padrão fixo, nesta ordem)

Studio → vídeo → **Editor** → **Cards de informações**. Tipos disponíveis: **Vídeo, Playlist, Canal e Link**. A mensagem personalizada e o teaser têm **no máximo 30 caracteres**; o tempo é digitado em **MM:SS:QQ** (16:40 vira `16:40:00`). Espaçar os cards em pelo menos 3 minutos e nunca usar os primeiros 30 segundos.

| # | Papel | Tipo | Destino | Mensagem / teaser | Quando |
|---|---|---|---|---|---|
| 1 | **Acesse nosso perfil** (canal) | **Canal** | Revista ES Brasil (@RevistaESBrasil) — abre a página do canal com o botão Inscrever-se | Siga o canal da ES Brasil / Acesse nosso perfil | Logo após o 1º momento forte (25%–40% do vídeo) |
| 2 | **Acesse nosso site** | **Link** | esbrasil.com.br (matéria do mesmo tema, com UTM) | Leia a matéria completa / Acesse esbrasil.com.br | Perto da metade, quando o assunto da matéria estiver em pauta |
| 3 | **Playlist da categoria** | **Playlist** | Playlist temática (Passo 11) | Mais sobre [categoria] / Playlist [nome] | Entre o card 2 e o fim |
| 4 | **Próximo vídeo** | **Vídeo** | Próximo vídeo da playlist da categoria | Assista ao próximo / Próxima: [tema curto] | No final, logo após a fala de encerramento e antes da tela final |

**Limites do YouTube (não contornar):**
- **Card de Link (site)** só funciona para canais no **Programa de Parcerias do YouTube** e para **sites associados ao canal** (Studio → Configurações → Canal → Recursos avançados → Site associado). Se, ao escolher "Link", o Studio não abrir o campo de URL ou recusar o endereço, o canal ainda não está liberado: **pule o card 2**, registre a pendência ("associar esbrasil.com.br ao canal / habilitar cards de link") na mensagem ao administrador e mantenha o site no comentário fixado e na descrição.
- **Redes sociais não podem ser destino de card** nem de tela final. Nunca escreva "Siga nosso Instagram" no teaser de um card que leva a outro lugar (é enganoso). O convite ao Instagram vai no **comentário fixado** (10.1), na descrição e nos links do banner do canal.
- Card 1 com o próprio canal funcionou no canal da Comunhão. Se o Studio recusar, use Playlist → Comece por aqui | ES Brasil com os mesmos textos.
- Se a equipe já tiver ajustado tempos ou textos dos cards, **não sobrescreva**: compare com o padrão e só complete o que falta.

**Complemento (configuração única do canal):** Studio → Personalização → **Marca d'água do vídeo** (botão de inscrição em todos os vídeos) e **links no banner do canal** com site e Instagram @revistaesbrasil. Se ainda não estiverem ativos, inclua na mensagem ao administrador.

### 10.1 — Comentário fixado (site + Instagram)

Logo após publicar, comente no vídeo **como Revista ES Brasil** e **fixe** o comentário. Modelo:
```
Leia a matéria completa no portal: https://esbrasil.com.br/[materia]?utm_source=youtube&utm_medium=comentario&utm_campaign=[slug]
Siga a ES Brasil no Instagram: https://instagram.com/revistaesbrasil
Inscreva-se no canal e ative as notificações.
```
Como fazer: página pública do vídeo → pause o player → role até os comentários e **espere carregar** (alguns segundos) → "Adicione um comentário…" → colar o texto → **Comentar** → ⋮ do comentário → **Fixar no topo** → confirmar. Confira se aparece "Fixado por @RevistaESBrasil". Se a conta logada não for a do canal, não comente por outra conta: registre como pendência.

## Passo 11 — Playlist por categoria (checagem obrigatória)

Todo vídeo longo precisa estar em **duas** playlists: **uma** de **programa/formato** e **uma** de **categoria** (editoria). Quando o assunto for um dos temas da tabela abaixo, ele entra também na playlist do **tema** (no máximo uma). Use só playlists públicas que já existem no canal (Studio → Detalhes → Playlists). A playlist da categoria alimenta os cards 3 e 4 e a tela final. Os nomes abaixo estão como ficaram no canal em novembro de 2026; escreva-os exatamente assim.

Regras do modelo de playlists do canal (skill `youtube-playlists-next`):
- **Um programa por vídeo**: o vídeo entra só na playlist do seu programa. Ex.: um Café com Moqueca não entra em ES Brasil Entrevista. ES Brasil Entrevista, **Café com Moqueca**, ES Brasil Debate e Direito ao Direito são **séries oficiais** do YouTube, e um vídeo só pode pertencer a uma série.
- **Uma editoria por vídeo**: escolha a do assunto principal; não marque duas editorias.
- **Shorts não entram** em playlists de vídeos longos (nem de programa, nem de editoria, nem de tema). O lugar do Short é a playlist **de cortes do programa** do vídeo completo (ver "Playlists de cortes", abaixo).

Nomes exatos das playlists, para copiar (nas tabelas abaixo a barra aparece como `\|` só por causa da formatação):
```
Economia do Espírito Santo | ES Brasil
Política no Espírito Santo | ES Brasil
Vida capixaba | ES Brasil
Cultura, gastronomia e lazer no ES | ES Brasil
Ciência, tecnologia e inovação no ES | ES Brasil
Destinos ES
Portos e logística no ES | ES Brasil
Agro capixaba | ES Brasil
ESG no Espírito Santo | ES Brasil
Mercado imobiliário no ES | ES Brasil
Rochas naturais no ES | ES Brasil
Energia no Espírito Santo | ES Brasil
ES Brasil Entrevista
Café com Moqueca
ES Brasil Debate
Diálogos ES Brasil
Direito ao Direito
Reportagens | ES Brasil
Eventos e feiras no ES | ES Brasil
Comece por aqui | ES Brasil
Cortes | ES Brasil Entrevista
Cortes | ES Brasil Debate
Cortes | Café com Moqueca
Cortes | Destinos ES
```

**Playlists de categoria (editoria)**

| Assunto do vídeo | Playlist da categoria | Editoria no portal |
|---|---|---|
| Economia, negócios, indústria, agro, comércio e serviços, logística e infraestrutura, comércio exterior, energia e saneamento, mercado imobiliário | Economia do Espírito Santo \| ES Brasil | /economia/ (e subeditorias: /economia/industria/, /economia/agro/, /economia/comercio-servicos/, /economia/logistica-infraestrutura/, /economia/comercio-exterior/, /economia/energia-saneamento/) |
| Política capixaba e nacional, eleições, Judiciário, municípios, gestão pública | Política no Espírito Santo \| ES Brasil | /politica/ |
| Cotidiano, estilo, mobilidade, saúde, educação, comportamento | Vida capixaba \| ES Brasil | /vida-capixaba/ |
| Cultura, gastronomia, lazer, entretenimento | Cultura, gastronomia e lazer no ES \| ES Brasil | /diversao-e-arte/ |
| Ciência, tecnologia, inovação, startups, inteligência artificial, transformação digital | Ciência, tecnologia e inovação no ES \| ES Brasil | /ciencia-e-tecnologia/ |
| Turismo e destinos | Destinos ES | /destinos-es/ |

Quando o vídeo de tecnologia ou inovação tratar principalmente de negócio de uma empresa (resultado, investimento, mercado), use Economia; quando tratar da tecnologia em si, use Ciência, tecnologia e inovação.

**Playlists de tema** (opcional, até uma por vídeo, além da editoria)

| Tema do vídeo | Playlist do tema |
|---|---|
| Portos, rodovias, ferrovias, aeroporto, logística | Portos e logística no ES \| ES Brasil |
| Agronegócio, café, produção rural, pesquisa agrícola | Agro capixaba \| ES Brasil |
| ESG, sustentabilidade, responsabilidade social, meio ambiente nas empresas | ESG no Espírito Santo \| ES Brasil |
| Construção civil, lançamentos, mercado imobiliário | Mercado imobiliário no ES \| ES Brasil |
| Rochas ornamentais, mármore e granito, feiras do setor | Rochas naturais no ES \| ES Brasil |
| Petróleo, gás, energia solar, transição energética | Energia no Espírito Santo \| ES Brasil |

Só marque o tema quando ele for o assunto principal do vídeo, não uma menção.

**Playlists de programa/formato** (uma por vídeo; complementam a de categoria, não a substituem)

| Programa ou formato | Playlist |
|---|---|
| Entrevistas | ES Brasil Entrevista |
| **Café com Moqueca** | Café com Moqueca |
| Debates com mais de um convidado | ES Brasil Debate |
| Destinos ES (episódios numerados) | Destinos ES |
| Podcast (episódio completo) | Diálogos ES Brasil |
| Quadro jurídico | Direito ao Direito |
| Reportagens | Reportagens \| ES Brasil |
| Cobertura de eventos e feiras | Eventos e feiras no ES \| ES Brasil |

**Playlists de cortes** (só Shorts; um Short entra só na de cortes do programa do vídeo completo)

| Programa do vídeo completo | Playlist de cortes |
|---|---|
| ES Brasil Entrevista | Cortes \| ES Brasil Entrevista |
| ES Brasil Debate | Cortes \| ES Brasil Debate |
| **Café com Moqueca** | Cortes \| Café com Moqueca |
| Destinos ES | Cortes \| Destinos ES |

- O Short entra na playlist de cortes **quando ficar público** (tornar público continua exigindo aprovação; ver Passo 13). Short privado não entra.
- Playlist só de Shorts não pode ser reordenada: cada Short novo entra no fim, e assim a playlist fica em ordem de publicação.
- Programas sem playlist de cortes (Diálogos ES Brasil, Direito ao Direito, Reportagens, Eventos e feiras): não crie playlist por conta própria. Registre a pendência "Short de [programa] sem playlist de cortes" na mensagem ao administrador; a playlist é criada quando o programa juntar 5 Shorts.
- Shorts de notícia e chamadas de produto não são cortes de programa: ficam fora das playlists de cortes.
- A descrição do Short **sempre** traz a linha "Entrevista completa: [link do vídeo]" (Passo 13). É ela que liga o Short ao programa certo.

Atenção:
- **Vitrine:** "Comece por aqui | ES Brasil" é a vitrine curada da página inicial (10 a 15 vídeos, revisada todo mês). **Não acrescente vídeos a ela** na publicação; mudanças só por indicação do Mário Fernando.
- A antiga duplicidade de "ES Brasil Debate" foi resolvida: use **ES Brasil Debate** (pública). "ES Brasil Debate (arquivo)" é privada e não recebe vídeos.
- Um episódio de Destinos ES entra em "Destinos ES" como programa e como categoria; nesse caso basta ela (mais o tema, se houver).
- **Não use** playlists de especiais e de temporadas antigas, salvo se o vídeo for daquele especial: Acaps Trade Show 2022/2023, ES Brasil Retrospectiva 2021/2022, Especial doação de órgãos - 2018, VipES, Prodfor, 140 Destinos, Os 50 destinos mais amados pelos capixabas, Roteiros Metropolitanos de Agroturismo, De olho na Cidade, Institucional, Conteúdos complementares, ES Brasil em áudio.
- **Não use** playlists privadas, não listadas ou de arquivo: HOME - ESBRASIL (arquivo), ES Brasil Debate (arquivo), Revista ES Brasil - Podcasts (RSS).

- **Se a playlist da categoria não estiver marcada, não marque por conta própria:** registre como pendência e prepare a **mensagem ao administrador** (destinatários: edineim@nxte.net, audiovisual@nxte.com.br, esdrase@nxte.net), relacionando todas as pendências do processo. Mostre a mensagem e só envie com aprovação explícita.

Modelo da mensagem:
```
Assunto: Pendências de publicação — ES Brasil — [título do vídeo]

Olá, equipe,
Na revisão do vídeo "[título]" ([link]), do canal Revista ES Brasil, ficaram estas pendências:
1. Playlist: o vídeo não está em "[playlist da categoria]".
2. [outra pendência]
Podem ajustar até [prazo]? Obrigado!
```

## Passo 12 — Thumb (capa)

A capa depende da resposta à pergunta inicial ("Antes de executar"):

| Tipo de vídeo | Template do kit | O que a skill entrega |
|---|---|---|
| **ES Brasil Entrevista** | `entrevista` — faixa azul, selo ES BRASIL ENTREVISTA | Capa pronta, avaliada e publicada depois do ok final. |
| **Destinos ES** | `destinos` — rosa/roxo, logo Destinos ES, apresentadora no círculo | Capa pronta, avaliada e publicada depois do ok final. |
| **Café com Moqueca** | `cafe` — laranja, logo Café com Moqueca, apresentador no círculo | Capa pronta, avaliada e publicada depois do ok final. |
| **Colunas** | Arte própria, a caminho | Manchetes A/B, nome e foto tratada (PNG recortado) + pendência "capa no template de colunas". |
| **Outros programas e quadros** | Arte própria, a caminho | Manchetes A/B, nome e foto tratada + pendência "capa no template do programa". |

Para colunas e outros quadros, **não use os templates acima** (cada um traz o selo do seu programa), não imite as capas antigas do canal e não redesenhe arte por conta própria: a capa atual permanece até a arte oficial entrar na skill. As regras de manchete (12.1 a 12.3) e de foto (12.5) valem para todos os tipos.

A capa é uma **capa de revista**, não uma legenda. Ela vende o assunto em dois segundos, numa tela de celular: uma manchete forte, um rosto bem tratado olhando para quem rola o feed, e nada mais competindo.

### 12.1 — A manchete (linha 1)

O texto da capa é uma **manchete planejada**, escrita para a capa — não precisa ser uma frase dita pelo convidado, mas tem de ser fiel ao que ele disse.

Limites por template:

| Template | Linhas | Caracteres por linha | Total |
|---|---|---|---|
| `entrevista` | até 3 (padrão da arte) | ~15 | máx. 42 |
| `destinos` | 2, nunca 3 (uma só também funciona) | até 17, e nenhuma linha acima de 945 px | máx. **6 palavras** e 34 caracteres |
| `cafe` | 2 (uma só também funciona) | ~17 | máx. 34 |

**Destinos ES: limite rígido.** A manchete tem no máximo 6 palavras, em 2 linhas. Uma 3ª linha passa por trás do nome do convidado e do círculo da apresentadora e some: foi isso que cortou "da Barra" na capa de Erivan Tavares (16/11/2026). Nome de município comprido não cabe numa linha ("Conceição da Barra" sozinho mede 1.081 px, e o limite é 945). Reescreva a manchete em vez de quebrar em 3 linhas. Ex.: "O turismo como motor de Conceição da Barra" (8 palavras) vira "Turismo, o motor / da Barra". O script para com erro, sem gerar a capa, quando a manchete passa de 2 linhas, 6 palavras, 17 caracteres numa linha, 34 no total ou 945 px.

- Nasce da **tese central**, do dado mais forte ou da pergunta que o vídeo responde. Pergunte: o que um empresário contaria a um sócio depois de assistir?
- Palavras concretas e verbos fortes; corte artigos e adjetivos vazios. Palavra comprida (mais de 13 letras) ocupa uma linha sozinha: confira se cabe antes de fechar a manchete.
- Diferente do título do YouTube: os dois se completam (o título traz a palavra-chave de busca; a capa traz a tese).
- Quebre as linhas por sentido, com larguras parecidas; evite uma palavra curta isolada.
- Sem adjetivo sobre pessoas, sem número que não esteja no vídeo, sem promessa.
- Sem ponto final, salvo interrogação.

**Fórmulas que funcionam** (escolha a que o conteúdo pede; nos templates de programa, reescreva para caber em 2 linhas):
| Fórmula | Exemplo |
|---|---|
| A pergunta de quem decide | "Em quem / o eleitor deve / acreditar?" |
| O que muda | "O que muda / no mercado / imobiliário" |
| O dado (dito no vídeo) | "[número] que / explica o / setor no ES" |
| A tese do convidado | "Juro alto trava / a construção" |
| O contraste | "Muita pesquisa, / pouca inovação" |
| O futuro | "O próximo ciclo / da economia / capixaba" |
| A frase do convidado | Entre aspas, só quando a fala for mais forte que qualquer manchete; fiel à transcrição |

**Manchete ou nome em destaque?** Nos templates, **a manchete é a primeira leitura e o nome é a segunda**. Só inverta quando o convidado for amplamente conhecido do público (governador, senador, presidente de grande entidade ou empresa) — aí o nome vira a manchete e a linha 2 traz o gancho.

Entregue sempre **duas manchetes com fórmulas diferentes** (A = recomendada, B = alternativa), justificando a escolha em uma frase — servem para teste A/B de miniatura.

### 12.2 — Linha 2: o nome
- Nome do convidado como ele é conhecido (ou o gancho, se o nome for a manchete).
- No template `entrevista` o nome fica à esquerda, abaixo da manchete; em `destinos` e `cafe`, **alinhado à direita**, abaixo da manchete.

### 12.3 — Linha 3 (opcional): cargo e empresa
- Só existe no template `entrevista`, e **só quando a manchete tiver até 2 linhas**. As artes de referência trazem apenas manchete + nome; em `destinos` e `cafe` não há linha de cargo.
- Quando usada: cargo + empresa/instituição em forma curta (ex.: "Fundador da Galwan", "Cientista político"), até ~32 caracteres, com dado confirmado.
- Nome do programa e do apresentador ficam nos elementos fixos da arte, nunca no bloco de texto.

### 12.4 — Medidas dos templates (arte 1600×900)

Medidas tiradas das artes de referência e já gravadas no script; servem de gabarito para conferir o resultado. Corpo em pontos a 300 dpi (1 pt = 4,1667 px); entreletras em milésimos do corpo.

**Template `entrevista`**

| Elemento | Especificação |
|---|---|
| Faixa | Inclinada a **−5,35°**, do azul-ciano (#01C1F2, à esquerda) ao azul (#005E96) e ao navy (à direita). No eixo inclinado, vai de 267 a 774 px (centro 520). |
| Selos | **ES BRASIL ENTREVISTA** (canto superior esquerdo) e **ES BRASIL play** (canto inferior esquerdo), prontos na base. |
| Manchete | **Inter ExtraBold Italic**, 123,5 px (corpo ~30), entreletras −52 (letras quase coladas), entrelinha 0,886. Piso: 116 px. |
| Nome | **Inter SemiBold Italic**, 61 px (corpo ~15), alinhado à esquerda. |
| Cargo (opcional) | Inter SemiBold Italic, 43 px. |
| Cor do texto | Branco que vai ao lilás-rosado para a direita (#FFFFFF → #F8D4FF), com sombra azul-escura suave. |
| Posição | Texto inclinado junto com a faixa, à esquerda (x≈70). O bloco manchete + nome fica **centralizado na faixa**. |
| Largura útil | **900 px**. |

**Templates `destinos` e `cafe`** (mesma diagramação, cores de cada programa)

| Elemento | Especificação |
|---|---|
| Fundo e faixa | Destinos ES: rosa → roxo → azul, com mapa em marca-d'água. Café com Moqueca: laranja com faixa marrom de borda rasgada e retícula. Prontos na base. |
| Elementos fixos | Logo do programa (alto, à esquerda); círculo com a foto do apresentador, "Apresentação:" + nome e **ES BRASIL play** (embaixo, à esquerda). Prontos na base; nunca redesenhar nem cobrir. |
| Manchete | **Inter ExtraBold Italic**, corpo **28** (116,67 px), entreletras −30. Entrelinha **0,92 (107 px) no Destinos ES**, mais justa (desde 16/11/2026), e 1,05 (122,5 px) no Café com Moqueca. 2 linhas, alinhadas à esquerda em x≈72; o bloco fica centrado na altura original (linha de base da 1ª linha em y≈362 no Destinos ES e y≈354 no Café com Moqueca). |
| Nome | **Inter SemiBold Italic**, corpo **15** (62,5 px), entreletras −35, **alinhado à direita em x=990**, linha de base em y≈505. |
| Inclinação do texto | **−4,9°**. |
| Cor do texto | Branco puro, com sombra suave. |
| Largura útil | **945 px**. |

- **Sempre itálico** nestas capas: é a tipografia das artes oficiais (exceção à regra de títulos retos do Brand System, que continua valendo para documentos).
- O corpo não é reduzido para caber. Se a manchete passar da largura útil, o script avisa (no Destinos ES, para com erro e não gera a capa): reescreva ou quebre de outro jeito.
- Uma única paleta na peça: a da arte. Não acrescente cores, faixas, contornos nem elementos.

### 12.5 — Base e imagem do convidado

**Bases: `assets/thumbs/`.** Nunca redesenhe fundo, faixa, selos, logos ou o apresentador. As bases foram reconstruídas a partir das artes de referência; a área atrás do convidado é aproximada e fica coberta pela foto, e em `destinos` e `cafe` a textura da faixa ficou lisa onde havia texto. Se o design enviar as artes limpas, basta substituir os arquivos (1600×900) — o script não muda. Se o apresentador do programa mudar, a base precisa ser trocada: registre como pendência em vez de cobrir o círculo.

**Imagem do convidado — tratamento obrigatório, nesta ordem:**
1. **Escolha do quadro:** percorra o vídeo e teste vários momentos (pause e capture em tela cheia, na maior resolução). Olhos abertos, rosto frontal, olhando para a câmera, expressão serena ou sorriso leve. Nunca rosto inclinado, olhos fechados ou boca no meio de uma palavra. Se houver foto de estúdio ou da matéria da revista, prefira-a ao quadro do vídeo.
2. **Restauração do rosto com IA:** modelo de restauração facial (ex.: GFPGAN v1.4, ampliação 2×, intensidade ~0,6). Regra: **melhorar sem descaracterizar** — o convidado tem de continuar reconhecível; nada de mudar formato do rosto, cor de pele, idade aparente ou traços. Se parecer artificial, reduza a intensidade (0,4–0,5). Foto de estúdio profissional dispensa esta etapa. Compare antes/depois lado a lado.
3. **Recorte de qualidade:** remova o fundo com modelo de segmentação (rembg isnet-general-use) **com refino de bordas (alpha matting)**, preservando os fios de cabelo. Limpe restos de cenário e confira o recorte sobre um fundo de cor chapada.
4. **Tratamento de cor:** +10% de contraste, +8% de saturação, +5% de brilho e nitidez leve. Tom neutro — **não aqueça a imagem** e não aplique luz de recorte colorida: nos templates, o convidado entra limpo sobre o fundo.
5. **Posição:** à direita, ancorado na base, altura entre 850 e 880 px (`foto_h`), topo da cabeça a ~40–50 px do alto, rosto entre x≈1050 e x≈1450. O ombro pode sair pela borda direita. O corpo não avança para a esquerda de x≈930 e o rosto nunca fica atrás do texto; ajuste com `foto_right`.

Quando houver dois convidados, trate e recorte os dois; a ordem na capa segue a ordem de fala ou a hierarquia do tema, e a manchete encurta para caber.

### 12.6 — Avaliação obrigatória: gerar, comparar, escolher

Nunca entregue a primeira versão. Para cada capa:

1. **Gere ao menos duas composições** da mesma manchete (outra quebra de linha; 2 × 3 linhas no template `entrevista`; com e sem linha de cargo, quando ela for cogitada). Quando houver duas manchetes (A e B), avalie cada uma.
2. **Olhe as versões lado a lado, reduzidas a 320×180** (tamanho real no celular), e compare com a arte de `assets/referencias/` do mesmo template.
3. **Dê nota de 1 a 5** em cada critério:

| Critério | Pergunta |
|---|---|
| Legibilidade no celular | Em 320×180, a manchete se lê sem esforço? |
| Impacto | A manchete é o primeiro elemento que o olho pega? |
| Equilíbrio | O bloco está bem assentado na faixa, com linhas de largura parecida e sem linhas encostando? |
| Hierarquia | Manchete → nome (→ cargo) ficam claramente em pesos diferentes? |
| Rosto | O rosto está livre do texto, nítido, bem tratado e reconhecível? |
| Fidelidade ao template | Parece a arte de referência (faixa, logos, apresentador, tipografia, cores)? |
| Fidelidade ao conteúdo | A manchete corresponde ao que o vídeo entrega, sem número ou juízo que não esteja lá? |

4. **Escolha a versão com maior soma** e, se algum critério ficou abaixo de 4, corrija e reavalie.
5. Na entrega, mostre a versão escolhida e diga **em uma frase por que ela venceu**.

### 12.7 — Conferência final
- Corpo da manchete e do nome conforme o template — confira o corpo **final** renderizado e o aviso de largura do script.
- Nada encosta nos logos, no apresentador, no rosto nem nas bordas da faixa.
- A manchete aparece inteira: nenhuma palavra atrás do nome, do círculo da apresentadora ou do convidado. No Destinos ES, confira também a entrelinha 0,92.
- Elementos fixos intactos; rosto tratado e reconhecível; recorte sem restos de fundo.
- Exportar JPG 1600×900 com menos de 2 MB e salvar também em `Downloads/shorts_esbrasil_[convidado]/`.
- **Publicar no Studio só depois do ok final** (Detalhes → Miniatura → Enviar arquivo → Salvar) e conferir a miniatura pública.

## Passo 13 — Shorts (mínimo 3, máximo 5 por entrevista) — com capa

1. Leia a transcrição inteira e escolha de **3 a 5 trechos** que se sustentam sozinhos: começo com gancho, uma ideia completa, final que fecha.
2. Duração ideal de **30 a 60 segundos** (máximo 90). Corte no início e no fim de frases completas.
3. **O que rende Short na ES Brasil:** um dado com a explicação junto, uma previsão ou tendência, um conselho prático para quem empreende ou administra, uma tese forte de quem tem autoridade no assunto, uma explicação didática de tema técnico.
   **O que evitar:** número sem o contexto (período, fonte, base de comparação); crítica ou acusação a pessoa ou empresa nomeada; fala política que soe como pedido de voto, ataque a adversário ou previsão de resultado; pesquisa eleitoral sem instituto e recorte; trecho que funcione como propaganda da empresa do convidado; informação que o convidado tratou como reservada; falas fora de contexto.
4. Para cada Short: tempos, duração, título do YouTube (até 40 caracteres, palavra-chave no início, terminando em #Shorts), **título da capa do Short (2 linhas, máximo de 30 caracteres no total)** e descrição neste modelo:
   ```
   [1–2 frases com a palavra-chave, o nome e o cargo do convidado]

   Entrevista completa: https://www.youtube.com/watch?v=[ID do vídeo completo]
   Instagram: https://instagram.com/revistaesbrasil
   Portal: https://esbrasil.com.br/?utm_source=youtube&utm_medium=shorts&utm_campaign=[slug]

   #[Tema] #EspíritoSanto #ESBrasil
   ```
5. **Arquivo original — download liberado, sem pergunta:** Studio → vídeo → ⋮ (Opções, ao lado de Salvar) → **Baixar**. **Não pergunte "posso baixar?"**: o download do original do próprio canal já está autorizado (ver "Download liberado", na Execução completa). Avise em uma linha o que está sendo baixado (nome do arquivo, origem e tamanho) e siga. O arquivo vai para **Downloads** do computador. Peça acesso à pasta Downloads uma vez. Se o envio direto do arquivo inteiro para o ambiente de trabalho for recusado (arquivo grande ou "hardlinked"), **corte os trechos brutos no próprio computador** com ffmpeg (`-ss início -t duração -c copy`, com 1 s de folga de cada lado) e traga só os trechos.
6. **Tempo exato por palavra:** transcreva cada trecho com faster-whisper (modelo `small`, `language='pt'`, `word_timestamps=True`). Use os tempos das palavras para cortar no começo e no fim da frase e para as legendas. Confira a grafia de nomes próprios, empresas, siglas e números nas legendas — o reconhecimento automático erra justamente neles. (Alternativa: `.srt` do Studio → Legendas → ⋮ → Baixar.)
7. **Montagem 1080×1920 (30 fps, H.264 + AAC) no corte limpo — o mesmo padrão dos Reels da ES Brasil no Instagram (desde 18/11/2026, decisão do Mário Fernando):**
   - **Sem moldura:** nada de faixa de título em cima nem rodapé com a marca. O vídeo ocupa a tela inteira e o único elemento sobre ele é a legenda. Título, nome do convidado e marca ficam na capa do Short (item 8), no título e na descrição.
   - **Enquadramento:** corte vertical 9:16 na altura inteira do original (largura = altura × 9/16), centrado no rosto de quem fala (`centro_x`, de 0 a 1), escalado para 1080×1920 com lanczos. Em debates e entrevistas com dois enquadramentos, o corte acompanha quem está falando (divida o trecho em partes e troque o `centro_x` em cada uma). Plano aberto com duas pessoas não funciona no vertical: prefira trechos em plano fechado.
   - **Qualidade:** monte sempre a partir do original baixado pelo Studio, na maior resolução disponível. O corte vertical amplia o quadro (num original 1080p, 1,78×); nunca use cópia comprimida.
   - **Legendas queimadas:** Inter ExtraBold, brancas com contorno escuro, blocos de até 4 palavras, centralizadas, com a base em y≈1450. Deixe livres as áreas que o YouTube e o Instagram cobrem com botões e textos: 420 px de baixo, 220 px de cima e 120 px de cada lado.
   - Se a tarja com nome/cargo do vídeo original aparecer cortada no enquadramento vertical, **desfoque a tarja** no intervalo em que ela aparece. As marcas d'água dos cantos do original (logo do programa, marca ES Brasil) normalmente ficam fora do corte; se um pedaço entrar, ajuste o `centro_x` para tirá-lo.
   - Fade de áudio de 0,15 s na entrada e 0,3 s na saída.
   - Como fazer (ffmpeg, sem depender do kit): gere as legendas do trecho em `.ass` (tempos por palavra do item 6) com este cabeçalho e estilo:
     ```
     [Script Info]
     ScriptType: v4.00+
     PlayResX: 1080
     PlayResY: 1920

     [V4+ Styles]
     Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
     Style: Legenda,Inter ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00201010,&H64000000,0,0,0,0,100,100,0,0,1,6,2,2,120,120,470,1
     ```
     e monte o Short (CX = `centro_x`; DURACAO = FIM − INICIO, em segundos):
     ```
     ffmpeg -ss INICIO -to FIM -i original.mp4 \
       -vf "crop=w='ih*9/16':h=ih:x='min(max(iw*CX-ih*9/32,0),iw-ih*9/16)':y=0,scale=1080:1920:flags=lanczos,setsar=1,subtitles=legendas.ass" \
       -af "afade=t=in:d=0.15,afade=t=out:st=DURACAO-0.3:d=0.3" \
       -r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart short_01.mp4
     ```
     Comando testado em 18/11/2026. O `montar_short.py` do kit aplica a moldura antiga: não use.
   - **Um arquivo só para todas as redes:** o Short limpo é o mesmo que segue para Instagram, TikTok e Facebook (exportação da skill `youtube-lote-noturno-next`), sem versão separada.
8. **Capa de cada Short (1080×1920):** base `capa_esbrasil.png` (azul) ou `capa_destinos.png` (rosa/roxo, só Destinos ES), conforme a tabela de "Antes de executar". A capa continua no template: é ela que leva título, nome e marca, já que o vídeo sai limpo, e serve também de capa no Reels e no TikTok. Logo no alto; foto do convidado na janela (de y=357 até a faixa inclinada); faixa com o **título da capa do Short** (item 4: 2 linhas, máximo de 30 caracteres) e o nome; ES BRASIL play embaixo.
   - Título: Inter ExtraBold Italic, corpo 29 (120 px), entrelinha 1,0, entreletras −35. Nome: Inter SemiBold Italic, corpo 14 (58 px). Centralizados e inclinados a −4,85°. Essas medidas foram tiradas da arte de referência.
   - Foto: quadro do convidado com olhos abertos e sem tarja, rosto no centro da janela (`centro_x`, `centro_y`). Não precisa recortar o fundo.
   - Como fazer: `gerar_short_esbrasil.py capa`. Exporte em JPG com menos de 2 MB para enviar ao Studio. Gere todas as capas e confira lado a lado com `assets/referencias/`.
9. **Publicar — só depois do ok final** (ver "Execução completa"). Passo a passo testado no canal da Comunhão:
   - **Arquivo ≤ 10 MB:** o envio pelo navegador aceita no máximo 10 MB por arquivo. Recomprima cada Short em 1080×1920 com H.264 em **duas passagens** e taxa-alvo `9,2 MB × 8 ÷ duração − 130 kbps` (áudio AAC 128k). Guarde a versão cheia; suba a comprimida.
   - **Caminho do arquivo:** o envio só aceita arquivos de pasta conectada **trazidos para o ambiente de trabalho** (`/mnt/user-data/uploads/...`). Grave os comprimidos em `Downloads/shorts_esbrasil_[convidado]/envio/` no computador e traga-os (stage) antes de enviar. Arquivos só em `/mnt/user-data/outputs` ou com caminho do Mac são recusados.
   - **Confira o canal antes de enviar:** o Studio precisa estar no canal **Revista ES Brasil**. Se estiver em outro canal da casa (ex.: Revista Comunhão), troque de canal antes de qualquer envio ou edição.
   - Studio → `.../videos/upload?d=ud` → localizar o `input type=file` e enviar o arquivo (nunca clicar no botão "Selecionar arquivos").
   - **Título e descrição:** o Studio preenche os padrões do canal alguns segundos depois de abrir a janela e sobrescreve o que foi digitado antes. Espere ~6 s, **clique de verdade no campo Título**, e só então substitua o conteúdo dos dois campos. Releia os dois campos antes de avançar. Apague também as tags padrão.
   - **Capa:** envie o JPG no `input type=file` da seção Miniatura.
   - Público: "Não é conteúdo para crianças" → Avançar ×3 → **Privado** → Salvar.
   - **Vídeo relacionado** não aparece na janela de envio: depois de salvar, abra a página de edição de cada Short → campo **Vídeo relacionado** → buscar colando o **link** do vídeo completo → escolher → Salvar. A janela de escolha às vezes abre duas vezes; digite na que está visível.
   - **Conferência:** Conteúdo → aba Shorts. Todos devem estar "Privado" (se algum ficar "Rascunho", abra "Editar rascunho" e conclua). Se a miniatura de algum aparecer em branco, reenvie a capa na página de edição do Short e salve.
   - Tornar público só com aprovação.
   - **Playlist de cortes:** quando o Short for tornado público (com a aprovação), abra a página de edição do Short → Detalhes → **Playlists** → marque a playlist de cortes do programa do vídeo completo (Passo 11: Cortes | ES Brasil Entrevista, Cortes | ES Brasil Debate, Cortes | Café com Moqueca ou Cortes | Destinos ES) → Salvar. Se o programa não tiver playlist de cortes, registre a pendência na mensagem ao administrador.
10. Salve os Shorts e as capas também em `Downloads/shorts_esbrasil_[convidado]/` no computador.

## Formato da entrega

Em blocos fáceis de copiar, nesta ordem:

1. Palavra-chave principal e secundárias
2. 5 títulos (com caracteres) + recomendado
3. Teste A/B: tabela A/B (e C)
4. Capítulos: lista com tempos reais e títulos (ou aviso de que não há minutagem)
5. Descrição completa, já com capítulos, portal, Spotify (se houver) e UTMs
6. Tags + contagem
7. Tela final: vídeo sugerido, playlist, inscrição, tempo de início
8. Cards: tabela no padrão do Passo 10 (perfil/canal, site, playlist da categoria, próximo vídeo) + comentário fixado com site e Instagram
9. Playlists: marcadas x corretas (programa + categoria + tema, se houver), pendências e mensagem ao administrador (se houver)
10. Capa: tipo de capa respondido no início; manchetes A e B, nome e foto tratada. Para ES Brasil Entrevista, Destinos ES e Café com Moqueca, a capa escolhida após a avaliação 12.6, com a frase que explica por que venceu; para colunas e outros quadros, a pendência do template
11. Shorts: tabela com 3 a 5 recortes (tempos, título do YouTube, título da capa, `centro_x`, playlist de cortes que recebe o Short quando ficar público) + capas
12. Checklist de publicação:
    - Palavra-chave no título, na 1ª linha da descrição, em um capítulo e nas tags
    - Título não começa com o nome do programa
    - Nenhum número, cargo ou citação que não esteja no vídeo
    - Teste A/B configurado
    - Capítulos com tempos reais e "Permitir capítulos automáticos" marcado
    - Link do portal escrito por extenso, com UTM; Spotify com UTM (ou ausente, com registro)
    - Tags padrão do canal removidas e substituídas
    - Vídeo em uma playlist de programa e em uma de categoria, mais o tema quando houver (ou pendência ao administrador); Shorts fora das playlists de vídeos longos; nada acrescentado à vitrine Comece por aqui
    - Tipo de capa perguntado no início
    - Capa no template do programa (entrevista: até 3 linhas, ≤ 42 caracteres; Destinos ES: 2 linhas, até 6 palavras, ≤ 34 caracteres, nenhuma linha acima de 945 px, entrelinha 0,92; Café com Moqueca: 2 linhas, ≤ 34), Inter itálico, elementos fixos intactos, foto tratada sem luz colorida, versão escolhida por avaliação. Colunas e outros quadros: só textos e foto, com pendência
    - Ok final recebido antes de salvar qualquer coisa no Studio
    - Original baixado pelo Studio (download liberado) e trechos cortados
    - 3 a 5 Shorts no corte limpo (vídeo em tela cheia 1080×1920, sem faixa de título nem rodapé, só a legenda dentro da área segura), com capa no template (título em 2 linhas com até 30 caracteres e nome), publicados como privados, com vídeo relacionado
    - Short que ficar público: na playlist de cortes do programa (Cortes | [programa]), e em nenhuma playlist de vídeo longo
    - Tela final com o próximo vídeo da playlist da categoria + essa playlist + inscrição
    - Cards: perfil (canal), site (se liberado), playlist da categoria, próximo vídeo
    - Comentário fixado com site e Instagram @revistaesbrasil

## Aplicando no Studio

Sempre mostre o pacote e espere o ok antes de salvar — na execução completa e em pedidos avulsos. Antes de qualquer alteração, confirme que o Studio está no canal **Revista ES Brasil**. Depois de salvar, recarregar a página e conferir título, descrição, tags, tela final e cards (os cards podem levar alguns minutos para aparecer na página pública).

**Notas práticas (aprendidas na execução):**
- Título e descrição são campos editáveis do tipo `#textbox`. Selecione todo o conteúdo e substitua de uma vez; "Ctrl+A + digitar" pode inserir o texto no meio do antigo. Se isso acontecer, use **Desfazer alterações** e refaça.
- Depois de clicar em **Salvar**, espere alguns segundos antes de recarregar — recarregar cedo demais descarta a alteração.
- Tags ficam em **Mostrar mais** → Tags. O botão "Remover tudo" limpa as antigas.
- Card: tempo em `MM:SS:QQ` e mensagem com até 30 caracteres (ver Passo 10).
- **Teste A/B:** o Studio roda **um teste por vez** por vídeo. Com teste de título em andamento, a capa pode ser trocada normalmente (vale para todas as variantes); um teste de **miniatura** só começa depois que o de título terminar.
- **Download do original (liberado):** ⋮ (Opções, ao lado de Salvar) → Baixar, sem pedir confirmação. Se o primeiro clique só fechar o menu, abra o menu de novo e clique em Baixar; confira em Downloads se surgiu o `.crdownload` e espere ele virar `.mp4` antes de cortar.
- **Transcrição com minutagem:** se o painel de transcrição não abrir, ligue as legendas no player; a requisição de legenda (`timedtext`) traz o texto com tempos.

## Execução completa ("rode a skill neste vídeo") — duas paradas, e só elas

A execução completa tem **duas paradas obrigatórias** e nenhuma outra: a pergunta do tipo de capa, no início, e o ok final, antes de salvar no Studio. Entre uma e outra, trabalhe sem perguntar a cada etapa.

**Fase 1 — Pergunta inicial.** Tipo de capa: ES Brasil Entrevista, Destinos ES, Café com Moqueca, coluna ou outro programa/quadro (ver "Antes de executar").

**Fase 2 — Montar tudo, sem tocar no canal.**
1. Leitura do vídeo (Studio, transcrição, playlists, Spotify, matéria no portal).
2. Passos 1 a 8: palavra-chave, títulos, par A/B, capítulos, Spotify, UTMs, descrição e tags.
3. Plano de cards (Passo 10), tela final (Passo 9), comentário fixado (10.1) e checagem de playlists (Passo 11).
4. Capa (Passo 12). ES Brasil Entrevista, Destinos ES ou Café com Moqueca: tratar a foto, gerar no mínimo 2 versões no template do programa, avaliar (12.6) e escolher. Coluna ou outro quadro: manchetes, nome e foto tratada, com a pendência do template.
5. Baixar o original (download liberado, sem pergunta), montar os Shorts no corte limpo e gerar as capas deles (Passo 13), guardando tudo em `Downloads/shorts_esbrasil_[convidado]/`.

**Fase 3 — Mostrar o pacote e pedir o ok.** Apresente o pacote no "Formato da entrega", com a capa e as capas dos Shorts à vista, e pergunte se pode salvar no Studio. Se vierem ajustes, refaça só o que foi pedido e mostre de novo.

**Fase 4 — Depois do ok, aplicar no Studio.**
1. Título, descrição e tags → salvar → teste A/B de título.
2. Cards, tela final e comentário fixado.
3. Capa (ES Brasil Entrevista, Destinos ES e Café com Moqueca): Miniatura → Enviar arquivo. Teste A/B de título em andamento não impede a troca.
4. Shorts como **privados**, com capa e vídeo relacionado. A playlist de cortes só é marcada quando o Short for tornado público, com aprovação (Passo 13, item 9).
5. Conferência final na página pública (título, capa, cards, tela final, comentário fixado, Shorts privados) e relatório curto: o que foi feito, o que ficou bloqueado e por quê.

O ok final vale para esse pacote, nesse vídeo. Ele **não** cobre tornar Shorts ou vídeos públicos, enviar e-mails nem excluir nada (ver abaixo).

### Download liberado (autorização permanente do Mário Fernando)

O responsável pelo canal já autorizou, de forma permanente, os downloads de que esta skill precisa, nas mesmas condições da skill da Comunhão. Ao rodar a skill, **não pare para pedir permissão de download** nem ofereça opções ("baixar pelo Studio ou você me envia?"): faça o download, informe em uma linha o nome do arquivo, a origem e o tamanho, e continue até o pacote ficar pronto para o ok final. O download não altera o canal, por isso acontece na Fase 2, antes do ok.

Está liberado:
- o **arquivo original do vídeo** pelo YouTube Studio do canal Revista ES Brasil (⋮ → Baixar);
- as **legendas/transcrição** (`.srt`) do mesmo vídeo no Studio;
- a **miniatura atual** do vídeo;
- a leitura do **kit de capa** em `Documents/Claude Skills/youtube-esbrasil-titulos/` (pedir o acesso à pasta Documents uma vez);
- o uso da pasta **Downloads** do computador para receber o original e guardar a capa, os Shorts e as capas dos Shorts (pedir o acesso à pasta uma vez, se ainda não estiver conectada).

Não está liberado (continua pedindo confirmação): arquivos de outros canais, de outros sites ou de links que apareçam em páginas, e-mails, comentários ou descrições.

Se o download falhar (menu fecha, arquivo não aparece em Downloads, computador fora do ar), tente mais uma vez, siga com as etapas que não dependem dele e relate no fim o que faltou — não fique parado esperando resposta.

**Continua exigindo um "sim" explícito, além do ok final:** tornar Shorts ou vídeos **públicos**, **enviar mensagens/e-mails** (inclusive a de pendências), **excluir** qualquer coisa e marcar playlist que não seja a da regra. Se algo não puder ser feito (ex.: card de link não liberado), siga com o resto e liste a pendência no relatório.

## Revisando vídeos antigos

Aponte em uma linha o que está fraco e entregue o pacote completo novo. Os problemas mais comuns no canal da ES Brasil:
- título começa com o nome do programa ("ES Brasil Entrevista –", "Café com Moqueca –") e traz só nome e cargo, sem o assunto;
- palavra-chave ausente ou só no fim; falta "ES"/"Espírito Santo";
- tags genéricas do padrão do canal, iguais em todos os vídeos;
- "Acesse nosso portal: ES Brasil" sem link; links de playlist soltos no lugar de link para a matéria;
- sem capítulos, sem UTM, sem Spotify;
- sem tela final, sem os cards padrão, sem comentário fixado;
- fora da playlist da categoria (só em ES Brasil Entrevista ou na antiga HOME - ESBRASIL), ou em duas editorias, ou na playlist de outro programa;
- capa no padrão antigo, com o nome ocupando tudo e o tema ilegível no celular (em ES Brasil Entrevista, Destinos ES e Café com Moqueca, refazer no template novo);
- Shorts sem capa no template. (Shorts antigos com moldura não precisam ser refeitos; o corte limpo vale para os novos.)