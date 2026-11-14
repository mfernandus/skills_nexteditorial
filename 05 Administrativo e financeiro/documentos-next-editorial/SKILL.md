---
name: "documentos-next-editorial"
description: "Gera documentos e relatórios no padrão visual da Next Editorial — Borderô (NX Fina), Espelho de paginação, Relatório de Metas (NextorCRM) e Next Performance Report — e documentos no Estilo Pessoal de Mário Fernando (verde-escuro, verde cítrico, navy e cinza). Use SEMPRE que o usuário pedir para criar, montar ou formatar relatório, borderô, espelho, plano de metas, relatório de performance ou comercial, ou qualquer documento interno da Next Editorial, ES Brasil, Comunhão, Destinos ES ou Prócidade, mesmo sem dizer \"no padrão\"; e quando pedir algo \"no meu estilo\", \"estilo pessoal\" ou \"estilo Mário Fernando\". Acione também quando ele der só os dados sem explicitar o formato. Aplica Inter, paletas por marca, logos oficiais, grade A4 e selos de proveniência."
---

# Documentos Next Editorial

Gera documentos e relatórios no padrão do Next Editorial Brand System 2026. Toda saída é
uma página **A4 retrato** em HTML autossuficiente, pronta para visualizar, imprimir ou
exportar em PDF, com os logos oficiais embutidos.

## Antes de começar

1. **Identifique o tipo de documento** a partir do pedido:
   - Saldos, contas, aplicações, cartões → **Borderô** (NX Fina)
   - Páginas de uma edição, status de produção, diagramação → **Espelho de paginação**
   - Metas por produto/executivo, plano comercial, atingimento → **Relatório de Metas**
   - Entrega de mídia, contratado × comprovado, impressões, CTR → **Next Performance Report**
   Se ambíguo, pergunte qual dos quatro. Documento no **Estilo Pessoal** não precisa ser um
   dos quatro: pode ser nota executiva, memorando, plano, análise ou folha livre.

2. **Identifique o estilo** (define a cor-assinatura e o cabeçalho):
   ES Brasil, Comunhão, Destinos ES, Prócidade, Next Editorial (institucional) ou
   **Pessoal — Mário Fernando**. Se o pedido não deixar claro, pergunte, oferecendo as
   seis opções.

3. **Leia `references/tokens.md`** para as paletas, tipografia e regras exatas. Leia
   **sempre**, mesmo que você "lembre" — os hexes e regras de logo são específicos e mudam.
   Os tokens do Estilo Pessoal estão nesta página, na seção própria.

4. **Consulte `references/manual-visual.html`** quando precisar ver como um bloco é
   montado (é o manual renderizado com os 5 tipos e a folha de marcas).

## Como construir

Trabalhe em HTML + CSS puro, fonte Inter via Google Fonts. Parta de
`references/template-base.html` (esqueleto de folha A4 com cabeçalho, KPIs, seção, análise
e rodapé já no padrão) e preencha com os dados do usuário. Os logos ficam em
`assets/logos/` — **embuta-os como base64** para o arquivo final ser autossuficiente
(rode um pequeno script Python para converter PNG→base64 e injetar no HTML).

### Estrutura vertical (toda folha, nesta ordem)
1. **Cabeçalho de assinatura** — logo horizontal Next Editorial à esquerda (base64, sobre o
   papel claro, sem inversão). Para documento de um produto, adicione filete vertical +
   logo do produto. Metadados à direita (folha, emissão, status).
2. **Filete duplo** navy + vermelho abaixo do cabeçalho.
3. **Eyebrow** (rótulo do tipo) + **título** (Inter 800) + subtítulo.
4. **Faixa de KPIs** — 4 a 7 células de largura igual, hairline entre elas, rótulo âmbar
   escuro (#8A6300), número Inter 800 tabular. Nos formulários, mantenha **sempre 4 colunas**
   (não deixe quebrar para 2 no responsivo).
5. **Blocos de seção** — título CAIXA-ALTA com marcador quadrado vermelho + descritor;
   tabela com cabeçalho âmbar, linhas hairline, linha de total destacada.
6. **Bloco de análise** — eyebrow âmbar sobre régua superior (nunca borda-lateral colorida).
7. **Rodapé** — origem à esquerda; selo de confidencialidade + produto à direita, CAIXA-ALTA.

### Regras não-negociáveis (ver tokens.md para detalhes)
- Inter em tudo; números tabulares à direita; tracking −0,4px.
- Escrever sempre "ES Brasil"; destacar "Café com Moqueca", "ES Brasil", "revista ES Brasil".
- **Assinatura de Mário**: sempre que um documento levar o nome dele como assinatura ou
  autoria, escrever **"Mário Fernando"** — nunca só "Mário", nunca "Mário Fernando Souza".
- Uma paleta de marca por peça; nunca misturar marcas.
- Ícones só Lucide (outline, 2px).
- Sem emojis; sem cartão de borda-lateral colorida.
- **Logos**: nunca ES Brasil, Next Editorial ou Prócidade sobre plaqueta branca chapada —
  sempre no original; se o fundo for escuro, o logo vai numa faixa clara no topo.
- **Performance**: todo número recebe selo de proveniência; nunca estimar — o que não tem
  comprovação fica PENDENTE.

## Os quatro modelos

### 1. Borderô (NX Fina)
Cabeçalho co-marca Next + "NX Fina". KPIs: Saldo CC, Limite, Disponível, Aplicações,
Liquidez, Cartão utilizado, Cartão disponível (até 7). Seções: Contas Correntes,
A Receber, A Pagar, Cartões de Crédito (cada uma tabela com total). Análise do ciclo
(liquidez, cartões). Rodapé: "Gerado automaticamente pelo NX Fina · não substitui extratos".

### 2. Espelho de paginação
Co-marca Next + logo do produto (ex.: Comunhão). KPIs: Páginas, Conteúdos, Anúncios,
Em copy, Comercializado. Tabela página-a-página: Pg · Local/Título · Responsável · Status
(chip) · Diagramador. Uma folha por ~33 páginas; paginar em Folha 1/2. Resumo de produção.

### 3. Relatório de Metas (Plano Comercial)
Cabeçalho com metadados NextorCRM (PERÍODO · EMISSÃO · FONTE · chip de status). Caixa de
"Leitura" azul-clara. KPIs: Meta consolidada, Produto prioritário, Contatos válidos,
Propostas, Meta por executivo. Tabela produto × executivo (colunas: os 4 executivos +
Total). Tabela de contatos válidos (ritmo dia/semana/mês). Ver dados canônicos em tokens.md.

### 4. Next Performance Report (pós-venda)
Cabeçalho "NEXT PERFORMANCE REPORT" (PERFORMANCE em vermelho). Caixa de aviso âmbar
tracejada ("Relatório com dados reais"). KPIs com régua superior colorida + selo por
cartão. Tabela Presença Contratada × Comprovada (coluna Status com chips REAL/PARCIAL/
PENDENTE). Bloco Resultado da Entrega Digital (impressões, CTR, visíveis).

## Estilo Pessoal — Mário Fernando

Sexto estilo da skill, ao lado das cinco marcas. É a identidade dos documentos que Mário
assina em nome próprio — notas executivas, memorandos, planos, análises, estudos e
material de despacho. Usa a mesma folha A4, a mesma estrutura vertical e a mesma
tipografia Inter do padrão da casa; mudam a paleta e o cabeçalho.

### Quando usar
- Quando ele pedir "no meu estilo", "estilo pessoal", "estilo Mário Fernando" ou escolher
  **Pessoal** na pergunta de estilo.
- Em documento pessoal ou autoral dele que não seja peça editorial ou comercial de uma marca.
- **Não usar** em material de marca: proposta, mídia kit, relatório de produto, peça
  editorial ou comercial de ES Brasil, Comunhão, Destinos ES ou Prócidade seguem a paleta
  da marca; relatórios institucionais e dos sistemas (Nextor, NX Fina, NX Page) seguem o
  layout Next Editorial. Na dúvida, pergunte.

### Identificação — sempre "Mário Fernando", sem cargo e sem empresa
A assinatura dele é **sempre "Mário Fernando"** — nunca só "Mário" e nunca "Mário
Fernando Souza". Neste estilo, o nome vem sozinho: não escrever cargo ("Diretor",
"Diretor Executivo") e não escrever "Next Editorial" nem qualquer empresa ou marca — nem
no cabeçalho, nem no rodapé, nem em assinatura ou metadados da folha. A regra vale para a
identificação do documento; o conteúdo pode citar a empresa quando o assunto exigir.

### Paleta
| Papel | Token | Hex | Onde entra |
|---|---|---|---|
| Predominante | `--verde-escuro` | `#194F30` | logo, filete do cabeçalho, cabeçalho de tabela, títulos de seção, selo do rodapé |
| Acento | `--citrico` | `#B6D930` | marcador de seção, régua superior de KPIs e de caixas, chip de status do documento |
| Acento para texto | `--citrico-dk` | `#4F6B12` | eyebrows e rótulos de KPI (texto pequeno em caixa-alta) |
| Tinta clara | `--citrico-lt` | `#EEF6CF` | linha de total, caixa de leitura, fundo de chip positivo |
| Tinta | `--navy` | `#001C43` | nome no cabeçalho, título do documento, números, negrito de destaque |
| Apoio | `--cinza` | `#5B6470` | subtítulo, descritores, metadados, rodapé |

O verde-escuro é o verde da logo pessoal (`#194F30`) — logo e folha usam exatamente o
mesmo tom. Superfícies: linha `#E3E7E5`, linha forte `#C5CCC8`, fundo de bloco `#F3F5F4`,
papel `#FFFFFF`. Texto corrente continua em `#1a1a1a`.

### Logo pessoal (provisória) — versão verde
Monograma "M" em quadrado de cantos arredondados, com a haste que vaza pela lateral
direita. É a logo **provisória** de Mário; quando ele enviar a definitiva, substitua o SVG
abaixo e, se o verde mudar, atualize `--verde-escuro` junto.

```html
<svg class="marca" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 288 284" role="img" aria-label="Mário Fernando"><path fill="#194F30" d="M48 0H240A48 48 0 0 1 288 48V119H241V51A4 4 0 0 0 237 47H193L143.5 96.5 94 47H51A4 4 0 0 0 47 51V233A4 4 0 0 0 51 237H90A4 4 0 0 0 94 233V113L143.5 162.5 193 113V233A4 4 0 0 0 197 237H237A4 4 0 0 0 241 233V165H288V236A48 48 0 0 1 240 284H48A48 48 0 0 1 0 236V48A48 48 0 0 1 48 0Z"/></svg>
```

- Usar **sempre a versão verde** neste estilo. Existem versões navy e preta da mesma
  marca; só entram se ele pedir.
- Embutir o SVG direto no HTML (inline), sem arquivo externo. O "M" é vazado: aparece na
  cor do fundo, então aplicar sobre papel branco ou superfície clara.
- Não recolorir, distorcer, girar, contornar nem aplicar sombra. Altura padrão no
  cabeçalho: 36px; mínima: 20px. Respiro mínimo em volta: um quarto da altura da marca.
- Não combinar com logos das marcas da casa na mesma folha, salvo pedido explícito.

### Regras do estilo
- **Verde cítrico é sempre preenchimento, nunca texto.** Sobre papel branco ele não tem
  contraste (1,6:1). Para texto na família cítrica use `#4F6B12`; texto sobre fundo
  cítrico vai em verde-escuro `#194F30` ou navy.
- Texto sobre verde-escuro é branco.
- Proporção: verde-escuro conduz, cítrico pontua (pouco e nos mesmos lugares), navy é a
  tinta de leitura, cinza é apoio. Não usar o cítrico em áreas grandes.
- **Filete único** verde-escuro de 2px sob o cabeçalho — nunca filete duplo.
- **Cabeçalho**: logo pessoal verde à esquerda + "Mário Fernando" em Inter 800 navy, e
  nada mais do lado esquerdo (sem cargo, sem empresa, sem filete vertical). Metadados à
  direita (folha, emissão, status).
- Não misturar com vermelho, âmbar, roxo, rosa ou laranja das marcas. Exceção: os chips
  semânticos de status (ATENÇÃO âmbar, PENDENTE vermelho, NEUTRO cinza) permanecem como no
  padrão; os positivos (REAL, ACIMA DA META, CONCLUÍDO) passam para verde-escuro sobre
  tinta cítrica clara.
- Valem todas as regras não-negociáveis da casa: Inter em tudo, números tabulares à
  direita, sem emojis, sem cartão de borda-lateral colorida, ícones só Lucide, destaque
  para "Café com Moqueca", "ES Brasil" e "revista ES Brasil".
- Rodapé: origem à esquerda ("Documento pessoal · Mário Fernando" ou a origem real do
  dado); classificação à direita em verde-escuro (ex.: "Uso interno", "Confidencial").

### Como aplicar no template-base
Parta de `references/template-base.html` e cole este bloco **no fim do `<style>`** (ele
sobrepõe o `:root` e os componentes). No cabeçalho, troque o `<img class="logo-full">` pelo
SVG da logo pessoal (bloco acima) seguido de `<span class="nome">Mário Fernando</span>`, os
dois dentro do `<div class="lockup">`.

```css
:root{
  --verde-escuro:#194F30; --citrico:#B6D930; --citrico-dk:#4F6B12; --citrico-lt:#EEF6CF;
  --navy:#001C43; --cinza:#5B6470;
  --linha:#E3E7E5; --linha-forte:#C5CCC8; --fundo:#F3F5F4; --analise:#F3F5F4;
}
.sig .marca{height:36px;width:auto;display:block;flex:none;}
.sig .nome{font-size:19px;font-weight:800;letter-spacing:-.03em;color:var(--navy);line-height:1;}
.rule2{border-top:2px solid var(--verde-escuro);}
.rule2::after{content:none;}
.eyebrow{color:var(--citrico-dk);}
.kpis{border-top:3px solid var(--citrico);}
.kpi .lab{color:var(--citrico-dk);}
.sec-h h2{color:var(--verde-escuro);}
.sec-h h2::before{background:var(--citrico);}
thead th{background:var(--verde-escuro);color:#fff;}
tr.total td{border-top:1.5px solid var(--verde-escuro);background:var(--citrico-lt);color:var(--navy);}
.nota{background:var(--citrico-lt);border-left:0;border-top:2px solid var(--citrico);color:#24352d;}
.nota b{color:var(--verde-escuro);}
.analise{border-top:2px solid var(--citrico);}
.analise .eyebrow{color:var(--citrico-dk);}
.analise h5{color:var(--verde-escuro);}
.chip.status-doc{color:var(--verde-escuro);background:var(--citrico);border-color:var(--citrico);}
.chip.acima,.chip.real,.chip.subtotal{color:var(--verde-escuro);border-color:var(--verde-escuro);background:var(--citrico-lt);}
.foot .conf{color:var(--verde-escuro);}
```

### Em Word (.docx) e PDF
Mesmos hexes e papéis: título e títulos de seção em Inter ExtraBold (800), título em navy,
títulos de seção em verde-escuro, cabeçalho de tabela verde-escuro com texto branco, linha
de total em `#EEF6CF`, filete único verde-escuro sob o cabeçalho. Inter em todo o
documento e respiro antes e depois de toda caixa ou tabela. A logo entra no cabeçalho com
cerca de 1 cm de altura, ao lado de "Mário Fernando": renderize o SVG acima em PNG de alta
resolução (fundo transparente) e insira a imagem, já que o Word não lê SVG inline.

## Entrega
Salve o HTML em disco e, se `present_files` estiver disponível, apresente-o. Ofereça
exportar em PDF (o CSS já tem `@page A4` e `print-color-adjust: exact`). Antes de gerar,
se o usuário não indicou o estilo, pergunte — a paleta e o cabeçalho dependem disso.