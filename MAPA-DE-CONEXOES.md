# Mapa de conexões

Quais skills da Anthropic e de terceiros servem a quais skills da Next Editorial e às pessoais. "Já usa" quer dizer que a skill da Next cita ou depende dela hoje; "pode usar" é uma ligação que faz sentido e ainda não está escrita na skill.

As skills da Next ficam em `~/Minhas Skills/skills-next-editorial` no Mac (versão em uso) e no repositório [skills_nexteditorial](https://github.com/mfernandus/skills_nexteditorial).

Skills marcadas como "na conta" não têm cópia aqui porque a licença não permite: o Claude as carrega direto da conta, pelo nome.

## Regras da casa que valem por cima de qualquer skill

- Tabela, gráfico e infográfico saem sempre do NXtab, na paleta do veículo.
- Documento ou relatório: perguntar antes para qual produto é (**ES Brasil**, Comunhão, Destinos ES, Prócidade ou Next institucional), usar Inter e a paleta da marca.
- Nada em caixa alta.

## Por skill de apoio

### docx

- Onde está: `anthropic/documentos-e-planilhas/docx` · licença: Apache 2.0 · grupo: Documentos e planilhas
- Já usa: `documentos-next-editorial` (versão em Word dos relatórios, borderôs e espelhos)
- Pode usar: `cartas-comerciais-next-editorial` (carta em Word quando o cliente pedir arquivo editável); `retrospectiva-esbrasil` (texto do capítulo em Word para revisão fora do InDesign)

### pdf

- Onde está: `anthropic/documentos-e-planilhas/pdf` · licença: Apache 2.0 · grupo: Documentos e planilhas
- Já usa: `documentos-next-editorial` (exporta relatórios e borderôs em PDF); `analise-semanal-vendas-next` (entrega o painel semanal de vendas em PDF); `noticias-noturnas-esbrasil` (lê os relatórios em PDF do Sindirochas e do CCCV)
- Pode usar: `cartas-comerciais-next-editorial` (juntar a carta em PDF com anexos e conferir o arquivo final); `retrospectiva-esbrasil` (conferir as páginas exportadas)

### xlsx

- Onde está: `anthropic/documentos-e-planilhas/xlsx` · licença: Apache 2.0 · grupo: Documentos e planilhas
- Já usa: —
- Pode usar: `analise-semanal-vendas-next` (exportar os números da semana em planilha); `atualizacao-cnpj-templos` (conferir a base da Receita antes da carga); `diversao-e-arte-esbrasil` (manter a planilha de fontes da editoria); `youtube-playlists-next` (inventário de vídeos e playlists em planilha)

### pptx

- Onde está: `anthropic/documentos-e-planilhas/pptx` · licença: Apache 2.0 · grupo: Documentos e planilhas
- Já usa: —
- Pode usar: `cartas-comerciais-next-editorial` (apresentação que acompanha a proposta); `analise-semanal-vendas-next` (versão em slides para a reunião de vendas)

### canvas-design

- Onde está: `anthropic/visual/canvas-design` · licença: Apache 2.0 (fontes em OFL) · grupo: Visual
- Já usa: —
- Pode usar: `youtube-esbrasil-titulos` (rascunho de capa fora dos templates oficiais); `youtube-comunhao-titulos` (rascunho de capa fora dos templates oficiais); `cartas-comerciais-next-editorial` (peça visual de projeto especial)
- Observação: Nunca para gráficos, tabelas ou infográficos: esses saem sempre do NXtab.

### theme-factory

- Onde está: `anthropic/visual/theme-factory` · licença: Apache 2.0 · grupo: Visual
- Já usa: —
- Pode usar: `documentos-next-editorial` (guardar as paletas das marcas como temas reaproveitáveis); `analise-semanal-vendas-next` (mesmo tema da casa no painel semanal); `monitor-audiencia-next` (mesmo tema da casa no painel de audiência)
- Observação: As paletas oficiais do Brand System 2026 mandam sobre qualquer tema pronto.

### skill-creator

- Onde está: `anthropic/criacao-de-skills/skill-creator` · licença: Apache 2.0 · grupo: Criação de skills
- Já usa: —
- Pode usar: `todas` (criar, ajustar, testar e medir qualquer skill da Next ou pessoal)

### chrome-browser

- Onde está: na conta do Claude · licença: Anthropic, cópia proibida · grupo: Navegador e computador
- Já usa: `politica-esbrasil` (cita a skill para ler páginas oficiais); `noticias-noturnas-esbrasil` (cita a skill para ler páginas oficiais); `padrao-publicacao-next` (Chrome só para confirmar uma pauta já escolhida); `diversao-e-arte-esbrasil` (agenda de casas e perfis oficiais); `atualizacao-mapas-destinos-es` (fotos e dados de locais no navegador); `youtube-lote-noturno-next` (YouTube Studio pelo Chrome); `cacadores-destinos-conteudo` (vídeo e legenda do YouTube pelo Chrome do Mário); `monitor-audiencia-next` (abrir o arquivo do coletor quando o conector falha)
- Pode usar: —

### built-in-browser

- Onde está: na conta do Claude · licença: Anthropic, cópia proibida · grupo: Navegador e computador
- Já usa: —
- Pode usar: `as mesmas da chrome-browser` (quando o Chrome não estiver aberto)

### computer-use

- Onde está: na conta do Claude · licença: Anthropic, cópia proibida · grupo: Navegador e computador
- Já usa: —
- Pode usar: `nx-mac-clean` (operar apps do Mac, como o CleanMyMac, quando o shell não basta)

### video-making

- Onde está: na conta do Claude · licença: Anthropic, cópia proibida · grupo: Visual
- Já usa: —
- Pode usar: `youtube-esbrasil-titulos` (Shorts); `youtube-comunhao-titulos` (Shorts); `youtube-lote-noturno-next` (Shorts em lote); `previsao-tempo-esbrasil` (stories animado)

### artifact-emulator

- Onde está: na conta do Claude · licença: Anthropic, cópia proibida · grupo: Artefatos
- Já usa: —
- Pode usar: `monitor-audiencia-next` (conferir o painel HTML como o leitor verá); `retrospectiva-esbrasil` (conferir o kit e as páginas em artefato); `documentos-next-editorial` (prévia do HTML antes do PDF)

### docs

- Onde está: na conta do Claude · licença: Anthropic, sem licença de redistribuição · grupo: Documentos e planilhas
- Já usa: —
- Pode usar: `retrospectiva-esbrasil` (capítulo em doc para revisão e comentários); `cacadores-destinos-conteudo` (entrega do texto corrido em doc)

### google-workspace

- Onde está: na conta do Claude · licença: Anthropic, sem licença de redistribuição · grupo: Documentos e planilhas
- Já usa: `youtube-lote-noturno-next` (escreve na planilha Central YouTube Next)
- Pode usar: —

### deep-research

- Onde está: na conta do Claude · licença: Anthropic, sem licença de redistribuição · grupo: Pesquisa
- Já usa: —
- Pode usar: `igreja-comunhao` (pesquisas e dados sobre fé e igreja); `missoes-comunhao` (apuração com várias fontes); `datafe-materia-diaria-comunhao` (contexto para os números do Datafé); `retrospectiva-esbrasil` (dados na divulgação mais recente); `cacadores-destinos-levantamento` (levantamento amplo de episódios)

### morning

- Onde está: na conta do Claude · licença: Anthropic, sem licença de redistribuição · grupo: Rotina e memória
- Já usa: —
- Pode usar: —
- Observação: Sem ligação com as skills da Next hoje; serve ao briefing pessoal da manhã.

### import-memory

- Onde está: na conta do Claude · licença: Anthropic, sem licença de redistribuição · grupo: Rotina e memória
- Já usa: —
- Pode usar: —
- Observação: Sem ligação com as skills da Next.

### karpathy-guidelines

- Onde está: `terceiros/karpathy-guidelines` · licença: MIT · grupo: Terceiros
- Já usa: —
- Pode usar: `youtube-esbrasil-titulos` (scripts de capa e Shorts); `youtube-comunhao-titulos` (scripts de capa e Shorts); `retrospectiva-esbrasil` (scripts do kit do InDesign); `atualizacao-cnpj-templos` (carga da base); `documentos-next-editorial` (geração de HTML e PDF)
- Observação: Vale também para os apps da casa no Lovable.

### nx-mac-clean

- Onde está: `pessoais/nx-mac-clean` · licença: Mário Fernando · grupo: Pessoais
- Já usa: —
- Pode usar: —
- Observação: Conversa com a computer-use (apps do Mac) e roda pelo Desktop Commander.

## Por skill da Next e pessoal

Para cada skill, as de apoio que conversam com ela.

- **analise-semanal-vendas-next**: `pdf` (já usa: entrega o painel semanal de vendas em PDF); `pptx` (pode usar: versão em slides para a reunião de vendas); `theme-factory` (pode usar: mesmo tema da casa no painel semanal); `xlsx` (pode usar: exportar os números da semana em planilha)
- **atualizacao-cnpj-templos**: `karpathy-guidelines` (pode usar: carga da base); `xlsx` (pode usar: conferir a base da Receita antes da carga)
- **atualizacao-mapas-destinos-es**: `chrome-browser` (já usa: fotos e dados de locais no navegador)
- **cacadores-destinos-conteudo**: `chrome-browser` (já usa: vídeo e legenda do YouTube pelo Chrome do Mário); `docs` (pode usar: entrega do texto corrido em doc)
- **cacadores-destinos-levantamento**: `deep-research` (pode usar: levantamento amplo de episódios)
- **cartas-comerciais-next-editorial**: `canvas-design` (pode usar: peça visual de projeto especial); `docx` (pode usar: carta em Word quando o cliente pedir arquivo editável); `pdf` (pode usar: juntar a carta em PDF com anexos e conferir o arquivo final); `pptx` (pode usar: apresentação que acompanha a proposta)
- **datafe-materia-diaria-comunhao**: `deep-research` (pode usar: contexto para os números do Datafé)
- **diversao-e-arte-esbrasil**: `chrome-browser` (já usa: agenda de casas e perfis oficiais); `xlsx` (pode usar: manter a planilha de fontes da editoria)
- **documentos-next-editorial**: `docx` (já usa: versão em Word dos relatórios, borderôs e espelhos); `pdf` (já usa: exporta relatórios e borderôs em PDF); `artifact-emulator` (pode usar: prévia do HTML antes do PDF); `karpathy-guidelines` (pode usar: geração de HTML e PDF); `theme-factory` (pode usar: guardar as paletas das marcas como temas reaproveitáveis)
- **igreja-comunhao**: `deep-research` (pode usar: pesquisas e dados sobre fé e igreja)
- **missoes-comunhao**: `deep-research` (pode usar: apuração com várias fontes)
- **monitor-audiencia-next**: `chrome-browser` (já usa: abrir o arquivo do coletor quando o conector falha); `artifact-emulator` (pode usar: conferir o painel HTML como o leitor verá); `theme-factory` (pode usar: mesmo tema da casa no painel de audiência)
- **noticias-noturnas-esbrasil**: `chrome-browser` (já usa: cita a skill para ler páginas oficiais); `pdf` (já usa: lê os relatórios em PDF do Sindirochas e do CCCV)
- **nx-mac-clean**: `computer-use` (pode usar: operar apps do Mac, como o CleanMyMac, quando o shell não basta)
- **padrao-publicacao-next**: `chrome-browser` (já usa: Chrome só para confirmar uma pauta já escolhida)
- **politica-esbrasil**: `chrome-browser` (já usa: cita a skill para ler páginas oficiais)
- **previsao-tempo-esbrasil**: `video-making` (pode usar: stories animado)
- **retrospectiva-esbrasil**: `artifact-emulator` (pode usar: conferir o kit e as páginas em artefato); `deep-research` (pode usar: dados na divulgação mais recente); `docs` (pode usar: capítulo em doc para revisão e comentários); `docx` (pode usar: texto do capítulo em Word para revisão fora do InDesign); `karpathy-guidelines` (pode usar: scripts do kit do InDesign); `pdf` (pode usar: conferir as páginas exportadas)
- **youtube-comunhao-titulos**: `canvas-design` (pode usar: rascunho de capa fora dos templates oficiais); `karpathy-guidelines` (pode usar: scripts de capa e Shorts); `video-making` (pode usar: Shorts)
- **youtube-esbrasil-titulos**: `canvas-design` (pode usar: rascunho de capa fora dos templates oficiais); `karpathy-guidelines` (pode usar: scripts de capa e Shorts); `video-making` (pode usar: Shorts)
- **youtube-lote-noturno-next**: `chrome-browser` (já usa: YouTube Studio pelo Chrome); `google-workspace` (já usa: escreve na planilha Central YouTube Next); `video-making` (pode usar: Shorts em lote)
- **youtube-playlists-next**: `xlsx` (pode usar: inventário de vídeos e playlists em planilha)

Todas as skills conversam também com a `skill-creator` (criar, ajustar e testar). Onde aparece a `chrome-browser`, a `built-in-browser` substitui quando o Chrome não estiver aberto.
