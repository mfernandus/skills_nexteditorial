---
name: "revista-por-modelo-next"
description: "Cria revistas e cadernos (Prócidade, ES Brasil, Destinos ES, Comunhão) copiando a diagramação de uma edição-modelo em PDF, com boneca e versão para gráfica."
---

# Revista a partir de modelo estabelecido (Next Editorial)

Skill para produzir uma revista nova (ex.: Prócidade de uma cidade) **copiando a estrutura de uma edição já diagramada** (ex.: boneca de Viana, ESB_VIANA_BONECA_V4.pdf). Nasceu da produção da Prócidade Conceição da Barra (jan/2027) e das regras da Retrospectiva 2026 (skill `retrospectiva-esbrasil`). As seções "Erros que não podem se repetir" e "Conferência" valem como lei: foram os erros cometidos na produção e corrigidos a pedido do Mário Fernando.

Regra-mãe: **o modelo manda**. Não se inventa layout, tamanho de fonte, fonte, cabimento de capa nem paginador. Tudo se mede no PDF do modelo e se replica.

## Etapa 0 · Perguntas (uma mensagem só, antes de pesquisar)

1. Produto e paleta: Prócidade, ES Brasil, Comunhão, Destinos ES ou Next Editorial institucional.
2. Edição-modelo (PDF anexado) e quais páginas servem de exemplo de diagramação (ex.: 20, 21, 22 e 23).
3. Cidade ou tema, número da edição e mês de circulação.
4. Número de páginas final (ex.: 54, igual ao modelo) e se capa e contracapa contam.
5. Anúncios: anunciante, formato (1 página, página dupla) e posição; se é real ou simulado na boneca.
6. Páginas a copiar literalmente (ex.: 2 e 3) e o que troca nelas (logo, fotos).
7. Fontes de dados autorizadas (ex.: NX Fotos, ES em Números, Datafé, NEIA, site da prefeitura, {cidade}.procidade.com).

Campo em branco: usar o padrão do modelo e dizer qual foi usado.

## Etapa 1 · Ler e medir o modelo (obrigatória, antes de qualquer página)

- Rasterizar as páginas-exemplo (`pdftoppm -r 72`) e olhar uma a uma.
- Medir tudo em mm com `pdftotext -bbox-layout`. Em PDF com marcas de corte, descontar o deslocamento do refile (no modelo de Viana: 29,17 pt; mm = (pt − 29,17) × 0,3528).
- Fontes: `pdffonts -f N -l N`. Registrar família e peso de: título, texto corrido, legenda, chapéu, números de destaque, boxes, paginador, capa.
- **Corpo real do texto:** não basta o tamanho em pt. Medir caracteres por linha numa coluna (ex.: Viana, 63 caracteres em 85,3 mm a 10/12 pt, Minion Pro Condensed). Na fonte usada, o mesmo trecho precisa dar a mesma largura com margem de ±2%. Foi esse erro que deixou o texto 25% maior.
- Cores: amostrar os pixels (título navy, verde do número, verde-claro do box, vermelho do chapéu e do número de página).
- Para cada página-exemplo, montar um gabarito com as coordenadas de cada foto, título, texto, box, número de destaque, legenda e crédito. Exemplo do modelo de Viana no apêndice.

## Etapa 2 · Apuração

- Ordem: fontes da casa (NEIA, ES em Números, Datafé, NX Fotos, Prócidade), depois fontes oficiais (prefeitura, governo do ES, IBGE, Sebrae, Iema, IJSN), depois a web, sempre com crédito.
- Regras de dados da Retrospectiva: nunca inventar número, nome ou fala. Todo número tem recorte, período e unidade. Fato que não foi confirmado em duas fontes é atenuado ou sai do texto.
- ES Hoje só serve como pista, nunca como fonte.
- Toda citação tem fonte publicada.
- Guardar um dossiê: número → fonte → link.

## Etapa 3 · Espelho

- Página a página: o que é anúncio, o que é editorial e qual gabarito usa (página par usa só gabarito de página par, ímpar só de ímpar).
- Ao tirar ou pôr páginas, manter a paridade: tirar sempre em pares, ou trocar uma página por outra da mesma paridade. Depois, renumerar o paginador e atualizar as páginas citadas no sumário.
- Total de páginas igual ao pedido e conferido no PDF final (`pdfinfo`).

## Etapa 4 · Tipografia e cores (Prócidade, decisões de 27/11/2026)

| Elemento | Regra |
|---|---|
| Todos os títulos | **Inter**: títulos de matéria, chapéus, números de destaque, anos e números dos boxes, cabeçalhos de box, manchete e chamadas da capa, sumário, editorial, mapa e títulos de anúncio. Matérias: 800, 28 pt, entrelinha ~0,95, tracking −0,035 em. |
| Texto corrido do miolo | **Minion** (Minion Pro Condensed, 10/12 pt, justificado, capitular de 3 linhas). Os anúncios ficam com tipografia própria. |
| Legendas, boxes de texto, mapa | Roboto Condensed, como no modelo (legenda Light 8,6 pt, branca sobre a foto). |
| Capitular | Heebo Black, cinza-escuro, como no modelo. |
| Caixa alta | Nunca (regra do Mário Fernando). Chapéus e selos em caixa alta e baixa, mesmo quando o modelo usa caixa alta. |
| Paginador | Da marca do produto. Prócidade: página par com número em vermelho, "@procidade • procidade • procidade.org" e logo; página ímpar com logo à esquerda e "procidade.org" mais o número. Nunca "ES Brasil" no paginador da Prócidade. |

Fontes:
- A Minion é licenciada: usar os arquivos .otf do Mário Fernando (Minion.rar, kit da Retrospectiva) e nunca publicar em artefato, repositório público ou pasta compartilhada.
- Sem o arquivo, pode-se reconstruir a Minion Cn só para a boneca a partir da fonte embutida no PDF do próprio modelo: pypdf para extrair o FontFile3, fontTools para montar a fonte com as larguras do /Widths e converter para TrueType. Os glifos que faltam caem na EB Garamond.
- Instalar as fontes estáticas por npm (`@fontsource/inter`, `@fontsource/roboto-condensed`, `@fontsource/heebo`, `@fontsource/eb-garamond`), **nunca variáveis**: fonte variável e CFF saem como Type 3 no PDF, e a gráfica recusa.

## Etapa 5 · Montagem (HTML → PDF)

- Motor: HTML com posições absolutas em mm, página 205 × 275 mm (formato do modelo), Playwright/Chromium `page.pdf`.
- Um gabarito por página-exemplo (T20, T21, T22, T23 no modelo de Viana), com as coordenadas medidas. As matérias são distribuídas nos gabaritos e não se cria posição nova.
- **Encaixe do texto, sem buraco e sem estouro:**
  1. Script no navegador: o texto que sobra numa caixa passa, palavra a palavra, para a caixa seguinte (ex.: o box verde-claro da página ímpar).
  2. Medir, em cada caixa de texto, o estouro (palavras cortadas) e a sobra (mm vazios no pé).
  3. Sobra de mais de 1 linha: escrever frase nova, só com fatos já apurados, sem inventar. Estouro: cortar frase do texto, nunca diminuir o corpo.
  4. Ajuste fino permitido: tracking de no máximo −0,35 pt no parágrafo.
  5. Corte por frase inteira só em último caso (abre buraco).
- Título que passa da altura do gabarito: reescrever mais curto antes de reduzir o corpo.
- Capa: mesmo cabimento do modelo.
  - Nome da cidade grande no topo (duas linhas quando pedido), logo da marca com as três linhas da edição à direita.
  - Manchete em 4 linhas e linha fina na mesma altura do modelo.
  - 4 cartões com foto emoldurada, selo vermelho e chamada centralizada.

## Etapa 6 · Fotos

- Fonte: NX Fotos primeiro (`buscar`, original com `link_do_original`), depois a prefeitura e o governo do ES, com crédito vertical.
- Foto de abertura: paisagem, de dia, com ao menos 1.200 px de largura. Não repetir foto na mesma dupla. Nada de foto de outra cidade como se fosse da cidade.
- **Proibido degradê, rosa ou roxo.** Nenhum degradê por cima de foto (nem para dar leitura ao texto; usar faixa de cor chapada ou sombra no texto). Foto de entardecer ou de palco com céu ou luz rosa e roxa fica fora. Varrer o PDF final por matiz rosa/roxo antes de entregar.
- Imagem de IA (Krea) só quando não houver foto real com direito de uso, sempre com o crédito "Imagem gerada por IA". Pessoas de verdade e políticos identificáveis não entram em foto ilustrativa.
- Recorte de pessoa (como no modelo): tirar o fundo com rembg (u2net_human_seg).

## Etapa 7 · Anúncios

- Na boneca, todo anúncio simulado leva a etiqueta "Anúncio simulado • boneca".
- **Logo e imagens oficiais do anunciante**, nunca desenho genérico:
  - Logo enviada pelo Mário: recortar e tirar o fundo.
  - Site do anunciante: ler pelo Chrome. Se o site bloquear download, o navegador busca o arquivo e o envia para a URL de upload da Krea (`get_upload_url`), de onde se baixa. O SVG da logo pode ser lido em pedaços via JavaScript.
- Cores, letreiro e tipografia tirados da marca: logo, frota, fachada, site. O título do anúncio fica em Inter, e o nome da marca em letra próxima à do letreiro.
- Pesquisar o anunciante na web (fundação, endereço pelo CNPJ, linhas, produtos) e citar as fontes. Não pôr dado não confirmado (telefone de site de terceiro é marcado "a confirmar").
- Trocar anunciante quando pedido (ex.: sai Águia Branca, entra Viação Mar Aberto) sem sobra do anterior em nenhuma página.

## Etapa 8 · Conferência (antes de cada envio)

1. Ficha de contato de todas as páginas lado a lado com as páginas-exemplo do modelo.
2. Encaixe: nenhuma caixa com estouro e nenhuma com mais de 1 linha vazia.
3. `pdffonts`: nenhuma fonte Type 3, nenhuma DejaVu (sinal de glifo faltando) e nenhuma fonte de sistema.
4. Varredura de rosa e roxo e de degradê no código (`grep linear-gradient`).
5. Paginador da marca certa, numeração na ordem e sumário com as páginas certas.
6. Títulos em Inter e texto corrido em Minion.
7. Créditos de foto e de IA.

## Etapa 9 · Entrega

- Boneca: PDF no formato final (ex.: 205 × 275 mm), com versão numerada (v1, v2…) e uma linha do que mudou.
- **Versão para a gráfica:**
  - Sangria de 3 mm: elementos que tocam a borda crescem 3 mm.
  - Folha 231 × 301 mm, com marcas de corte fora da sangria e TrimBox/BleedBox gravados (pikepdf).
  - Rodapé técnico com título, página, formato e sangria.
  - Fontes embutidas, sem Type 3.
  - Texto dentro de SVG usado como imagem leva a fonte embutida em base64.
- Avisar: PDF em RGB (conversão CMYK com a gráfica), fotos da web abaixo de 300 dpi e versão definitiva no InDesign.

## Erros que não podem se repetir (lista da produção de Conceição da Barra)

1. Diagramar de cabeça em vez de medir o modelo, o que deixou buracos. Sempre gabarito com coordenadas medidas.
2. Paginador com "ES Brasil" numa revista Prócidade.
3. Capa sem o cabimento do modelo.
4. Texto corrido com fonte 25% mais larga que a do modelo: conferir caracteres por mm, não só o corpo em pt.
5. Degradê rosa, roxo ou azul sobre foto, e foto de céu roxo. Proibidos para sempre.
6. Contorno (`-webkit-text-stroke`) em fonte Inter: sai oco e quebrado no PDF. Usar anel de `text-shadow`.
7. Fonte variável ou CFF virando Type 3 no PDF da gráfica.
8. Fonte de sistema "Inter" com espaçamento errado nos anúncios: declarar a fonte estática com o mesmo nome.
9. Texto cortado por frase inteira e texto curto demais, abrindo buraco. Escrever ou enxugar até fechar a caixa.
10. Logo e foto genéricas ou de IA no anúncio de marca real. Usar logo e imagens oficiais.
11. Título fora da Inter, ou números e anos de box em outra fonte.
12. Caixa alta em chapéu e selo.
13. Página tirada sem respeitar a paridade, e sumário com página antiga.
14. Afirmações sem fonte (tempo de viagem, "gratuito", "centenas de famílias"). Confirmar ou tirar.

## Apêndice · Gabaritos medidos do modelo de Viana (mm, sem sangria)

- **Medidas gerais**
  - Página: 205 × 275 mm.
  - Título: Inter 800, 28 pt, navy #123E74.
  - Texto: 10/12 pt.
  - Paginador: y 266,8 mm.
  - Logo Prócidade na página ímpar: x 14,4, y 6,6, altura 4,4 mm.
  - Quadrado vermelho do chapéu: 3,5 × 6,2 mm, cor #B01C28, a 6 mm do topo.
- **T20 (página par, abertura)**
  - Foto de topo: 0,0 → 205 × 127.
  - Número de destaque: x 152,7, y 6,6.
  - Foto emoldurada 1: x 10,9, y 96,6, 112,2 × 77,7.
  - Foto emoldurada 2: x 121,6, y 123, 83,4 × 57,5.
  - Título: x 12,4, y 178, largura 88.
  - Box verde-claro: x 104,4, y 176, 82,4 × 31.
  - Texto: 2 colunas, x 12,3, y 210,2, 175,5 × 50,6.
- **T21 (página ímpar)**
  - Foto de topo: x 15,1, y 15,2, 189,9 × 107, com título branco em x 22,8, y 74, largura 82.
  - Foto emoldurada: x 110,7, y 98,4, 79,3 × 117.
  - Texto: x 17,2, y 126,4, 85,3 × 41,2.
  - Foto de baixo: 0, 170,4, 111,5 × 87,4.
  - Número de destaque: x 79,8, y 165,5.
  - Box verde-claro: x 94,5, y 217, 98,8 × 40 (recebe a continuação do texto).
- **T22 (página par)**
  - Foto de topo: 0,0 → 205 × 140.
  - Box navy (#14497F): x 15,5, y 73, largura 45.
  - Foto emoldurada: x 10,2, y 128,5, 108,3 × 120,5, legenda escura embaixo.
  - Título e texto: coluna x 123, y 147, 69 × 112.
- **T23 (página ímpar de fotos)**
  - 5 fotos:
    - 17,2/19,7, 184,2 × 86,3;
    - 135,8/88,5, 62 × 47;
    - 11,6/109,4, 60,8 × 92;
    - 71,6/109,4, 59,4 × 74,4;
    - 74,2/184,6, 119,4 × 68.
  - Box verde (#0C6742, borda superior #ED1639): x 130,8, y 135, 62,5 × 49,6.
  - Texto: x 11,6, y 213,5, 60,5 × 47.
- **Capa**
  - Nome da cidade: Inter 900, vermelho #E3262F com anel branco, x 14, y 9, largura 136.
  - Logo e edição: x 154, y 21, largura 37.
  - Manchete: Inter 800, 32 pt, x 19, y 126.
  - Linha fina: y 175.
  - Cartões: centros em x 34, 81,5, 129,5 e 177,5; y 212; 34 × 29 mm; selo vermelho em y 238,6; chamada em y 246.