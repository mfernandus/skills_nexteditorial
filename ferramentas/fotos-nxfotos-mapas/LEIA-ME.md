# Fotos do NX Fotos no mapas do Destinos ES

Ferramenta usada em 19/11/2026 para dar a cara do NX Fotos aos pontos turísticos e aos locais de "o que fazer" de São Mateus e Linhares no mapas.nx.tv.br. Roda por script, fora do Lovable. O painel do mapas só entra no fim, para gravar, pela sessão logada de Mário Fernando no Chrome.

## Como roda

1. **Busca no NX Fotos** (MCP do NX Fotos, `buscar` com `completo: true` e `limit: 60`). Cada resultado é registrado com `reg.py rotulo=arquivo`.
2. **`selecionar.py`** cruza os resultados com a base do mapas (`alvo.json` e `base.json`, lidos da API pública). Por local, aplica a regra de palavras, o raio de 8 km do GPS (fotos da biblioteca), a foto horizontal com 1.600 px ou mais e a licença rf. Mede cor, contraste, nitidez e exposição na miniatura, descarta fotos que o local já tem (hash médio 16×16, distância ≤ 20) e indica a intensidade do tratamento (k).
3. **`revisar.py`** monta folhas com as 12 melhores candidatas de cada local, para a escolha visual. Só entram fotos que mostram o lugar.
4. **`gravar_no_mapas.js`** roda numa aba do painel logado: baixa a foto pelo CDN, trata no canvas só as cruas (receita da casa), sobe com `/api/upload-image`, anexa com crédito, legenda e texto alternativo e troca a principal quando a atual é do Google.

## Regras seguidas

- Até 4 fotos novas por local e total do local até 12. A exceção foi o Projeto Tamar Regência: ele já tinha 13 fotos, todas do Google, e recebeu 1 foto do NX Fotos para virar a principal.
- Crédito obrigatório: o autor do NX Fotos e, quando ele não está cadastrado, "Acervo NX Fotos".
- Nada apagado. Foto de outro município fica de fora: a do Rio Cricaré em Conceição da Barra, por exemplo.
- O resultado da rodada está em `plano-2026-11-19-sao-mateus-linhares.json`.
