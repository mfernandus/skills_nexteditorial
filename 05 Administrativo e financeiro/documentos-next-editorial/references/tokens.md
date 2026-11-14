# Tokens de Design — Next Editorial (Brand System 2026)

Referência técnica para gerar documentos no padrão. Todas as folhas são **A4 retrato
(210×297 mm)**, margem interna 30 px, rodapé fixo no rodapé da página.

## Tipografia
- Família única: **Inter** (Google Fonts, pesos 300, 400, 500, 600, 700, 800).
- Título/display: 800, letter-spacing −0,02em a −0,04em.
- Seção de bloco: 800, CAIXA-ALTA.
- Corpo e descritores: 400 (300–500).
- Tracking global do sistema: −0,4px.
- Números sempre **tabulares** (`font-variant-numeric: tabular-nums`), alinhados à direita.
- Nunca itálico em títulos.

## Paleta base dos documentos
Estes são os tokens usados nas FOLHAS de documento (cabeçalho, KPIs, tabelas):
- `--navy:   #001C43`  (base de títulos e cabeçalho)
- `--azul:   #00427B`
- `--vermelho:#B11A27`  (marcador de seção, filete, selo confidencial)
- `--ambar:  #FFC220`  (cabeçalho de tabela, rótulo de KPI escurecido para #8A6300)
- `--laranja:#F58223`
- `--verde:  #1E7A3D`  (selo REAL)
- Texto: `#1a1a1a` · cinza de apoio: `#454C59` · linha: `#e4e7ec` · linha forte: `#c9ced8`

> Nota: o Brand Book institucional usa vermelho `#B20B27`. Nos documentos, o vermelho
> operacional é `#B11A27` (mantido por consistência com o histórico dos relatórios).
> Divergência conhecida, ainda não unificada.

## Paletas por marca (cabeçalho de assinatura + folha de marcas)
Ativar UMA marca por peça. Nunca misturar paletas de marcas diferentes.

| Marca          | Predominante / base | Secundárias / acentos                 | Gradiente do card             |
|----------------|---------------------|---------------------------------------|-------------------------------|
| Next Editorial | Vermelho #B20B27    | Azul #00427B · Amarelo #FFC220        | 135deg #B20B27→#8E0920        |
| ES Brasil      | Azul #00427B / Navy #001C43 | Roxo #A115ED · Rosa #E01E70   | 135deg #001C43→#00427B        |
| Comunhão       | Azul #00427B / Navy #001C43 | Amarelo #FFC220 → Laranja #F58223 (degradê) | 135deg #001C43→#00427B |
| Destinos ES    | Navy #0D2B45        | Rosa #E91E8C · Ciano #00C8E0          | 135deg #0D2B45→#003B6F        |
| Prócidade      | Carvão #2E2E2E      | Laranja #F58223 · Amarelo #FFC220 · Teal #16A6A0 · Vermelho #B20B27 | 135deg #2E2E2E→#4a4a4a |

## Ícones
- Biblioteca única: **Lucide** (outline, stroke 2px, grade 24px). Nunca preenchidos, nunca misturar com outra biblioteca.

## Sistema de selos de proveniência (relatórios de Performance)
Todo número recebe um selo. Nunca estimar sem comprovação — deixar PENDENTE.
- `REAL` (verde) — medido/comprovado.
- `SUBTOTAL REAL` (verde) — soma de valores reais.
- `PARCIAL` (âmbar) — parte comprovada, parte pendente.
- `PENDENTE` (vermelho) — sem comprovação disponível; nenhum valor estimado.
- Status de meta: `ACIMA DA META` (verde), `ATENÇÃO` (âmbar), `NEUTRO` (cinza).

## Regras de logo (rígidas)
- Cabeçalho dos documentos: usar o logo horizontal completo `next-editorial-horizontal.png`
  (N vermelho + wordmark), sobre fundo claro (o papel). Sem inversão.
- Co-marca (documento de um produto): logo Next + filete vertical + logo do produto.
- **NUNCA** aplicar ES Brasil, Next Editorial ou Prócidade sobre plaqueta/fundo branco
  chapado. Usar sempre no original (outline). Quando o fundo for escuro (card de marca),
  colocar o logo numa FAIXA CLARA no topo do card — não uma plaqueta atrás do logo.
- Comunhão e Destinos ES podem ir sobre faixa clara também, mantendo cores originais.

## Regras editoriais
- Escrever sempre "ES Brasil" (nunca "S Brasil").
- Destacar sempre: "Café com Moqueca", "ES Brasil", "revista ES Brasil".
- Sem emojis em material institucional.
- Nunca cartão com borda-lateral colorida (evitar "slop").
- Uma paleta de marca por peça.

## Dados canônicos (Plano Comercial / Metas)
- 4 executivos: Mário Fernando Souza, Claudio Janssen, Magno Araújo, Leticia Lima.
- Produtos: Comunhão (Impresso/Portal), ES Brasil (Impresso/Portal), Livro 100 Praias
  (Destinos ES), PróCidade, Serenatas de Natal.
- Fonte dos dados comerciais: NextorCRM.
