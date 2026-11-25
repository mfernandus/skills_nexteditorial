# Retrospectiva 2026 · pacote da equipe

Versão de **25/11/2026**, preparada por Mário Fernando para a equipe de diagramação e produção da revista **ES Brasil** (ESB 238). **Substitui todos os pacotes anteriores (20/11 e 23/11): apague as cópias antigas antes de usar este.**

A equipe trabalha sem depender do Mário. A palavra final sobre os capítulos (aprovação, cortes, fotos, mudanças de regra) é da **Kamila, da produção**.

## O que mudou nesta versão (conferência de 25/11)

O pacote de 23/11 saiu com peças defasadas. Esta versão traz:

1. **Prompt v13, igual à skill.** O prompt v12 ainda tinha regras antigas, que contradiziam a skill: QR Code na abertura, caixa alta errada em intertítulos e títulos de peça, box do ES em Números com indicadores e QR, capacidades de página antigas, lateral de 55 mm. Agora o prompt é cópia fiel da skill.
2. **NXtab atual**, o mesmo do link publicado, com os botões **Exportar gráfico** e **Publicar na web (animado)** pela senha da equipe. O de 23/11 era de 22/11.
3. **Datas pelo NX Pages**, e não mais as datas antigas de 29/11, 03/12 e 09/12 (tabela abaixo).
4. **Fonte condensada da casa: Roboto Condensed** (correção de 23/11, no lugar da Myriad) no exportador do InDesign, nas legendas, na base das provas e nos gráficos dos capítulos.
5. **Skill de gráficos** (`dados-e-graficos-next`) na versão de 25/11, **kit dos artigos assinados** incluído e o **guia de publicação dos gráficos na web**.
6. Provas e PDFs de Supermercados, Serviços Financeiros e Agronegócio refeitos com essa base.

## Prazos da ESB 238 (NX Pages, consulta de 25/11/2026)

| Marco | Data |
|---|---|
| Entrega de textos | 03/12 |
| Diagramação | 04/12 |
| Fechamento da diagramação, fechamento comercial e entrega de material | 10/12 |
| Gráfica (CTP) | 11/12 |
| Circulação impressa | 14/12 |
| Circulação digital | 16/12 |

As datas podem mudar: o NX Pages é a referência.

## O que vem em cada pasta

| Pasta | Conteúdo |
|---|---|
| `01-prompt/` | Prompt da Retrospectiva, **versão 13** (25/11/2026), cópia fiel da skill. Só para quem não puder instalar a skill. |
| `02-skills/retrospectiva-esbrasil.zip` | A skill de criação dos capítulos, com o kit inteiro: modelo das páginas, base do InDesign V5, scripts, NXtab atual e fontes Minion. Instalar como skill no Claude, sem descompactar. |
| `02-skills/retrospectiva-esbrasil/` | A mesma skill aberta, para consulta (o `SKILL.md` traz todas as regras). |
| `02-skills/artigos-retrospectiva-2026.zip` | Skill dos artigos assinados (modelo do artigo do Sidemar Acosta), com o `kit-artigo`. Instalar do mesmo jeito. |
| `02-skills/dados-e-graficos-next/` | Skill de apoio para peças do NXtab e conferência de números. |
| `03-oficina/` | Bancada de trabalho: scripts, kit e uma pasta por capítulo já feito. |
| `04-pdfs/` | PDFs de prova de cada capítulo (205 × 275 mm). |
| `05-historico/` | Histórico da conversa de produção, cópia do registro canônico e o guia “NXtab · como publicar gráficos animados na web”. |
| `06-capitulos-para-o-claude/` | Um arquivo por capítulo, pronto para anexar numa conversa do Claude. |

## O jeito mais simples: tudo pelo Claude, sem código

1. **Instalar a skill, uma vez por pessoa:** nas configurações do Claude, na área de skills, envie `02-skills/retrospectiva-esbrasil.zip`, sem descompactar. Quem já tinha instalado a versão antiga instala esta por cima.
2. **Para atualizar um capítulo:** abra uma conversa nova, anexe o arquivo do capítulo que está em `06-capitulos-para-o-claude` e peça em português. Por exemplo: “Use a skill da Retrospectiva. Atualize este capítulo: troque a foto da página 129, corte o parágrafo do Sicredi e me devolva a prova em PDF.”
3. **Para conferir:** o Claude devolve o PDF e diz se o texto coube, sem buracos e sem viúvas. Quem aprova é a Kamila.
4. **Para mandar para o InDesign:** depois da aprovação, peça “Gere o pacote do InDesign deste capítulo.”
5. **Gráfico animado para o site:** abra o NXtab (https://claude.ai/artifact/G5Zau8SX9BaWydqLmndR7Z), monte a peça, clique em **Exportar**, cole a **senha da equipe** e clique em **Publicar na web (animado)**. A página devolve o código para colar num bloco HTML do WordPress. A senha fica com a Kamila; o passo a passo completo está no guia da pasta `05-historico`.

## Situação dos capítulos (25/11/2026)

| Capítulo | Páginas | Estado | Principais pendências |
|---|---|---|---|
| Supermercados e Atacados | 112–113 | Em dia com todas as regras | Aspa de João Falqueto (Acaps); repórter |
| Serviços Financeiros | 128–129 | Em dia com todas as regras | Confirmar com o BNB os números do FNE 2027 (fonte única); foto do BNB em alta; espelho do NX Pages com 2 páginas; repórter |
| Agronegócio | 54–64 (7 págs.) | Grade e respiros em dia. **Faltam:** texto em Minion, fotos arredondadas e menos achatadas | Aspas a colher (Fabrício Tristão, do CCCV; Júlio Rocha, da Faes, confirmar cargo); fotos com etiqueta “Buscar original” |
| Portos e Logística | 36–40 | **Precisa ser remontado** com as regras de 23/11 e reencaixado (cerca de 530 caracteres acima do espaço) | Julgamento do TCU sobre as contas vinculadas (25/11); nova data do leilão da EF-118; originais em alta da Vports e da Imetame |
| Rochas Naturais | ver espelho | **Precisa ser remontado** com as regras de 23/11 e reencaixado (cerca de 240 caracteres acima do espaço) | Ver registro canônico |
| ESG e Meio Ambiente | ver espelho | Montado no padrão de 21/11, com outro script (pasta própria) | Ver registro canônico |

Energia foi feita em outubro no padrão antigo e não está neste pacote.

Para remontar Portos e Rochas pelo Claude, anexe o arquivo do capítulo e peça: “Remonte este capítulo com as regras atuais da skill e reencaixe o texto, sem buracos.” Os PDFs de Portos, Rochas e ESG nesta pasta são de 22/11 e 23/11.

As marcas da prova saem na versão final: **rosa** = pendência; **azul-claro** = aspa publicada, a conferir com a origem; **laranja** = aspa montada, a confirmar com a pessoa; **verde-claro** = número trocado por divulgação mais recente.

## Regras de 23/11/2026 (na skill e no prompt v13)

1. Texto corrido em **Minion Pro Cond 11/12**, tracking -15, também na prova.
2. Fotos internas (menos a de abertura) com **cantos arredondados** no raio das tabelas do NXtab (cerca de 2,2 mm) e **cerca de 20% mais altas**.
3. **Tabelas sem quebra de linha** em nenhuma célula nem no cabeçalho.
4. **Intertítulo sem palavra sozinha** na última linha, com o espaço maior acima e um respiro antes do texto.
5. **Grade alinhada:** colunas e lateral começam na mesma altura e terminam na mesma linha de base; na lateral, gráficos em cima e texto por baixo; respiro de cerca de 5 mm abaixo das fotos internas e da tabela do alto.
6. **Roboto Condensed** é a fonte condensada da casa (legendas, créditos, linha do tempo); onde aparecer “Myriad”, leia Roboto Condensed.

## Para quem quiser rodar os scripts no computador (opcional)

Precisa de Python 3 com `playwright`, `pillow`, `pymupdf` e `pyphen` e do Chromium do Playwright (`pip install playwright pillow pymupdf pyphen` e `python3 -m playwright install chromium`). Os comandos rodam de dentro da pasta do capítulo.

```
cd 03-oficina/supermercados-e-atacados
python3 ../montar.py
python3 ../kit/scripts/legendas.py capitulo.html
python3 ../montar.py
python3 ../shot.py capitulo.html s          # ocupação, buracos, viúvas e órfãs
python3 ../alinha.py capitulo.html          # alinhamento das colunas
python3 ../dup.py capitulo.html             # texto inteiro, sem duplicar
python3 ../kit/scripts/embutir_imagens.py capitulo.html capitulo-prova.html
python3 ../pdf.py capitulo-prova.html prova.pdf
```

Só entregar quando o `shot.py` disser “Texto cabe nas páginas” e não listar buraco, viúva nem órfã.

**Agronegócio:** o capítulo está todo em `agronegocio/capitulo-prova.html` (texto no bloco `<template id="texto">`). Para mexer no texto, rode dentro da pasta `agronegocio`: `python3 ../agro_edit.py trocas.json`, com trocas no formato `[["trecho antigo","trecho novo"]]`.

**ESG e Meio Ambiente:** tem `montar.py` próprio dentro da pasta.

**Gráficos:** sempre do NXtab, a partir do `graficos.json` (CSV de cada peça na pasta `graficos/`), com `kit/scripts/nxtab_grafico.py`. O script não publica nada na web sem as chaves; para o site, use o NXtab publicado com a senha da equipe (passo 5 acima).

## Cuidados

- **Senha da equipe:** fica com a Kamila. Não escreva em matéria, grupo aberto, arquivo ou documento público. Chaves do R2 a equipe não usa.
- **Fontes Minion Pro** (`kit/assets/fonts/`): licenciadas, só para uso interno da Next. Não publicar em site, artefato público nem repositório público.
- **ES Hoje** serve só como pista, nunca como fonte: todo número, fala ou fato se confirma na fonte oficial.
- **Fotos:** conferir a data de toda candidata (preferir 2025 e 2026) e se o lugar ainda existe. Foto não tapa buraco.
- **Registro canônico:** toda decisão entra no Google Doc “ES Brasil — Retrospectiva 2026”. A Kamila aprova; o resto entra como proposta. Nada se apaga.
- **Skills:** cada pessoa instala a skill na própria conta. Mudança de regra passa pela Kamila e vale nos dois lugares: no `SKILL.md` e no prompt.

## Links

- NXtab (gráficos): https://claude.ai/artifact/G5Zau8SX9BaWydqLmndR7Z
- Guia de publicação na web: https://claude.ai/artifact/V7HkUkjAKKi2XDtgB7FDro (cópia em `05-historico`)
- Registro canônico: https://docs.google.com/document/d/1Jt1EmOZry-_Pla0Klp-hsNR4aiY2Vyziuzyu8pa2LpU/edit
- Pasta do Drive da equipe: https://drive.google.com/drive/folders/1mnsqrYjd-Lg_hQWfgFfMO-FPctrqRBLI

Mário Fernando

Dúvidas e aprovações: Kamila (produção).
