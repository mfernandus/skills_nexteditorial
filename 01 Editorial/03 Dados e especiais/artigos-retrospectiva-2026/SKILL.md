---
name: "artigos-retrospectiva-2026"
description: "Diagrama artigo assinado da Retrospectiva 2026 da revista ES Brasil no modelo do artigo do Sidemar Acosta: pergunta a página, trata a foto, gera o QR, encaixa o texto e entrega PDF e InDesign."
---

# Artigos Retrospectiva 2026 (revista ES Brasil, ESB 238)

Transforma o texto e a foto de um articulista numa página pronta da Retrospectiva 2026, no modelo visual do artigo do Sidemar Acosta (ES 238, p. 28): vinheta "ARTIGO" com aba rosa, selo Retrospectiva, nome e cargo do autor, foto de retrato com crédito na vertical, título em três linhas, QR Code com o selo ESB, texto em duas colunas com capitular e sinal de fim. Entrega o PDF da página e o pacote do InDesign (IDML na base da revista, com Links).

Use quando pedirem para diagramar, montar, reditar ou paginar um artigo assinado da Retrospectiva 2026, mesmo sem citar a skill. Capítulos de editoria ficam com a `retrospectiva-esbrasil`.

## Etapa 0 · Perguntar a página (sempre, antes de montar)

1. Procure o artigo no espelho do NX Pages (`listar_issues` → "ESB Retrospectiva 2026", nº 238; `get_espelho`; a resposta é grande e vai para um arquivo: procure nele `"section": "ARTIGO - <NOME>"`). Se o item tiver `pg`, use-o e confirme.
2. Se não tiver, pergunte ao usuário, com `AskUserQuestion`, exatamente: **"Qual página será?"** (opções: "Ainda não sei (usar 00)" e "Vou digitar o número"). Se ele só souber o lado, pergunte "par ou ímpar?".
3. A paridade define o lado da vinheta:
   - **Página par (esquerda):** aba rosa e "ARTIGO" à esquerda (lado de fora); selo Retrospectiva à direita; paginador com número e redes à esquerda e logo ESB à direita.
   - **Página ímpar (direita):** aba rosa e "ARTIGO" à direita (lado de fora); selo Retrospectiva à esquerda; paginador com logo ESB à esquerda e "radio.esbrasil.com.br" + número à direita.
   - O miolo (foto, título, QR, texto) não espelha: acompanha as margens (12 mm do lado de fora, 17 mm na lombada), andando 14,17 pt para a direita na página ímpar.
   - Sem número: monte com "00" em rosa no lado informado.

Depois da resposta, siga todas as etapas sem novas perguntas; o que faltar vira pendência rosa.

## Etapa 1 · Kits

```bash
pip install --break-system-packages -q pymupdf psd-tools segno "rembg[cpu]" mediapipe playwright opencv-python-headless pillow python-docx openpyxl
python3 -m playwright install chromium
```

- **Kit do artigo:** artefato "Artigos Retrospectiva 2026 · kit da skill", slug `3fc4555a-0c57-4453-8c6b-b5cd0dee2cdc`. Com a ferramenta de artefatos `read_file` (`paths`), baixe `scripts/tratar_foto.py.txt`, `scripts/qr_artigo.py.txt`, `scripts/montar_artigo.py.txt`, `scripts/exportar_artigo.py.txt`, `assets/selo-retrospectiva-artigo.png`, `assets/esb-paginador.png`, `assets/qr-centro-esb.png`, `assets/qr-centro-esb-cmyk.tif.b64.txt`, `assets/fontes/crimson-pro.css` e os seis `assets/fontes/CrimsonPro-*.woff2`. Copie para `kit-artigo/` com o mesmo caminho, tirando o `.txt` dos `.py`.
- **Kit da Retrospectiva** (exportador do InDesign, base da revista com Inter e página-mestre com o paginador): artefato slug `2662af95-77ba-43d3-8205-463326509342`. Baixe `scripts/exportar_indesign.py.txt`, `scripts/idml.py.txt`, `scripts/extrair.js`, `scripts/embutir_imagens.py.txt` e `assets/base-materia-esb2026-inter.idml.b64.txt` para `kit/` (tire o `.txt` dos `.py`; o exportador restaura a base sozinho).
- Arquivos do usuário são originais: copie para a pasta de trabalho antes de mexer.

## Etapa 2 · Foto

```bash
python3 kit-artigo/scripts/tratar_foto.py FOTO.psd saida/foto --nome sobrenome-nome --credito "Foto: Autor/Veículo"
```

- Aceita PSD/PSB (usa a composição visível), JPG/TIFF CMYK com perfil ICC ou RGB. Converte pelo perfil embutido; o TIFF final sai no mesmo perfil CMYK (o da revista é U.S. Web Coated SWOP v2).
- **Cabeça no padrão:** topo do cabelo a 3,0% da altura do quadro, cabeça (topo do cabelo ao queixo) com 72,1% da altura, olhos a 41,5% e centro da cabeça a 49% da largura, medidos na foto do Sidemar. Quadro: 39,7 × 54,8 mm, cantos de 1,4 mm. Assim todas as cabeças dos artigos ficam do mesmo tamanho.
- **Fundo:** troca pelo fundo de estúdio cinza-claro quente do modelo. O recorte é feito na foto inteira (paletó escuro sobre fundo escuro some no recorte parcial); cabelo e barba com borda macia para dentro, roupa com borda firme e nenhum furo dentro da pessoa. A troca usa C = I + (1 − alfa) × (fundo novo − fundo antigo), que tira a franja escura dos fios; onde só há fundo, entra o fundo novo puro (sem emendas da parede antiga).
- **Cor:** não mexer no tom da pele. A dominante sai só dos tons quase cinza (cabelo, barba, camisa clara); a pele só vai para perto da luz e da saturação do modelo (matiz em torno de 17°, luz 0,68; limites de ±8% na luz e −15% na saturação). Por fim, tira um pouco de magenta em Lab (`--menos-magenta`, padrão 2,5: reduz só o a* positivo, sem mexer no b*), porque a foto com dominante magenta ainda fica rosada depois do recorte. Nada de níveis fortes, curva em S ou ganho de canal na foto inteira: isso amarela a pele (erro já cometido e reprovado). Se ainda parecer magenta, suba o `--menos-magenta` aos poucos (3 a 4), nunca mexendo no amarelo. Retoque de pontos claros no paletó. Nada de IA generativa no rosto: camadas ocultas geradas por prompt (ex.: "Equalizar as cores…") ficam de fora e o script avisa.
- Confira sempre com os olhos antes de montar a página: comparação lado a lado (original, tratada, foto do modelo) e bordas do cabelo, da barba e dos ombros em 100%. Reprovar se a pele mudou de cor, se há furo ou transparência no corpo, franja escura ou emenda no fundo. O `.json` traz a pele antes e depois (matiz, saturação, luz). Resolução mínima de 300 ppi no quadro; o script avisa e não amplia.
- **Foto já tratada** (decisão do Mário Fernando de 25/11/2026): antes desta etapa, rode `python3 tratar_foto_next.py --verificar FOTO` da skill `tratamento-fotos-next`. Se a foto já tem a marca da casa (inclusive a invisível) ou foi editada pelo fotógrafo (Lightroom, Photoshop), ela não recebe a correção de cor desta etapa outra vez: só recorte, fundo e cabeça no padrão. Na comparação lado a lado, reprove qualquer mudança de pele. Foto crua segue a regra de cor acima, aprovada para o impresso.
- Crédito sem autoria confirmada vai em rosa (`credito_pendente: true`) e vira pendência.

## Etapa 3 · Reditar o texto

- Voz do autor (primeira pessoa, opinião dele), sem acrescentar fato nem número. Corte repetições, frases de transição e generalidades antes de dados. Sem intertítulos (o modelo não tem). Confira com código que todo número do texto novo está no original e vice-versa.
- Aponte, sem corrigir por conta própria, inconsistências do original (ex.: soma dos setores igual ao total e ainda "além de…"): viram pendência para confirmar com o autor ou a assessoria.
- **Título:** até 3 linhas de cerca de 24 caracteres (Inter Black 28/25,75), caixa alta e baixa, de preferência com as palavras do autor; quebras de linha decididas no `titulo` (lista).
- **Assinatura:** nome em caixa alta (como no modelo) e cargo começando por "é …".
- **Capacidade:** cerca de 3.400 caracteres com espaços (2 colunas de 30 linhas, Minion Pro Cond 11/11,7). Ajuste até o `encaixe.json` dar `cabe: true` e 0 a 2 `linhas_vazias_no_fim`. Se sobrar espaço, devolva trechos cortados do original; se faltar, corte de novo. Nunca estique espaço.

## Etapa 4 · QR Code

- Padrão: link curto do Encurtador da Next, `https://nx-t.me/ART-<PRIMEIRONOME><INICIAL DO ÚLTIMO SOBRENOME>-ESB238` (ex.: Lourenzo de Oliveira → `ART-LOURENZOO-ESB238`; `qr_artigo.slug_curto()` monta o código). Nunca reaproveite o código de outro artigo.
- Confira se o link existe: `curl -s -o /dev/null -w "%{http_code} %{redirect_url}" https://nx-t.me/CODIGO` (301 para o destino = ok; 302 para `nx-t.me/` = não cadastrado). Se não existir, vira pendência rosa: cadastrar no Encurtador (nx-t.me, com login da equipe), apontando para o artigo no esbrasil.com.br (ou para a home até o artigo ir ao ar).
- `python3 kit-artigo/scripts/qr_artigo.py URL trabalho --nome qr-artigo-sobrenome-nome` gera o PNG da prova e o PDF vetorial (K 100, selo ESB no centro) e confere a leitura; sai com erro se não ler.

## Etapa 5 · Página e prova

`artigo.json` na pasta de trabalho:

```json
{"pagina": 111, "cartola": "Artigo", "autor": "Nome Sobrenome", "cargo": "é …",
 "titulo": ["linha 1", "linha 2", "linha 3"], "texto": "texto.txt",
 "foto": "foto/sobrenome-nome-rgb.jpg", "credito": "Foto: …", "credito_pendente": false,
 "qr": "qr-artigo-sobrenome-nome.png", "qr_url": "https://nx-t.me/…",
 "etiquetas": [{"x": 300, "y": 300, "w": 240, "texto": "pendência (camada de prova)"}]}
```

`texto.txt` tem um parágrafo por linha; o primeiro abre com capitular. Rode `python3 kit-artigo/scripts/montar_artigo.py artigo.json saida/pagina` e olhe o `prova.png` (Read). Compare com o modelo: vinheta e selo no lado certo, cabeça no padrão, título em 3 linhas, capitular de 3 linhas, texto terminando na 2ª coluna. A prova usa Crimson Pro 15,79 px com espacejamento −0,038 em, calibrada no artigo do Sidemar (3.433 caracteres em 60 linhas, como no InDesign).

## Etapa 6 · Pacote do InDesign

```bash
python3 kit-artigo/scripts/exportar_artigo.py saida/pagina kit saida/indesign --nome Artigo_ESB238_p<PAG>_<NomeSobrenome> \
  --pagina <PAG> --foto-cmyk "$PWD/saida/foto/sobrenome-nome.tif" --qr-pdf "$PWD/trabalho/qr-artigo-sobrenome-nome.pdf" \
  --recorte "$PWD/saida/foto/sobrenome-nome-recorte.png"
```

Sai a pasta e o `.zip` com o `.idml` (base da revista, página-mestre "R-Retrospectiva 2026" com o paginador, seção começando na página pedida), `Links/` (foto TIFF CMYK, QR em PDF vetorial, selo), `Referencia/` (página e prova em PDF), `Textos/`, `Fotos de apoio/` (pessoa sem fundo) e `Leia-me.txt`. Estilos: "Texto artigo cap 2026" e "Texto artigo 2026" (Minion Pro Cond 11/11,7), "Título artigo 2026", "Autor artigo 2026", "Cargo articulista 2026", "QR Code texto 2026", "Créditos 2026" e "Retranca 2026 - Retrospectiva". Pendências ficam na camada "Prova (não imprime)".

Conferência, quando o conector da Adobe estiver disponível: envie o `.idml` (`asset_initialize_file_upload`, PUT, `asset_finalize_file_upload`) e renderize com `document_render_layout` em PNG. O servidor não tem Inter nem Minion e não recebe os Links: fonte trocada, texto estourado e molduras vazias são esperados; confira página, lado, paginador, molduras e estilos.

## Etapa 7 · Entrega

- Envie sempre os dois juntos, com `SendUserFile`: `pagina.pdf` (página limpa) e o `.zip` do InDesign (o `.idml` vai dentro, com a pasta Links). Nunca entregue só o PDF. A `prova.pdf` (com as etiquetas rosa) fica na pasta Referencia.
- Resumo curto: página e lado, caracteres e encaixe, o que foi cortado do original, e as pendências (crédito, link curto, dúvidas de dados para o autor).

## Geometria do modelo (pt, página de 581,1 × 779,5, sangria 8,5)

| Elemento | Par (modelo) | Ímpar |
|---|---|---|
| Aba rosa (VermelhoRetro2025) | x 0–5,3 (+ sangria), y 17–32,9 | x 575,8–581,1 (+ sangria) |
| "ARTIGO" (Inter Black 12, azul ES Brasil, caixa alta, tracking −20, letras justas; estilo "Retranca 2026 - Artigo") | começa em x 28,3, linha de base 29,4 | termina em x 552,8 |
| Selo Retrospectiva | x 445,9–535,4, y 17,9–31,6 | x 45,7–135,2 |
| Autor (Inter Black 12, caixa alta) / cargo (Inter Light 10) | alinhados à direita em x 538,6; bases 56,7 e 69,6 | à direita em x 552,8 |
| Foto | x 34, y 122,6, 112,6 × 155,4, cantos 3,9 | x 48,2 |
| Crédito (Inter Light 7, vertical, de baixo para cima, termina no topo da foto) | x 22,4 | x 36,6 |
| Título (Inter Black 28/25,75) | x 156,9, bases 222 / 247,8 / 273,5 | x 171,1 |
| QR: moldura 0,5 pt preta / QR 45,6 pt | x 34,3 / 38,1; y 300,4 / 304,3 | x 48,5 / 52,3 |
| Texto do QR (Inter 9,5/10): "Acesse o / QR Code e leia / a matéria em / esbrasil.com.br" | x 95,7, base 323,8 | x 109,9 |
| Texto corrido: 2 colunas de 245,7 com medianiz 9,1; capitular de 3 linhas | x 34–534,6, 1ª base 394 | x 48,2–548,8 |
| Fim de texto | sinal vermelho (C0 M100 Y80 K0) | igual |

Tinta do texto: Preto 90%. Paleta: azul #00427B, rosa da aba #EC018C. Inter em tudo, menos o texto corrido (Minion Pro Cond no InDesign).