# Legado — não usar na produção

Arquivos do padrão antigo dos Shorts ("Comunhão play": faixa laranja em cima, rodapé vermelho com o logo play e capa vermelha). Esse padrão saiu de uso em 18/11/2026: os Shorts agora saem no **corte limpo** e a capa segue o **modelo foto cheia** (SKILL.md, Passo 13, itens 7 e 8).

| Arquivo | O que era | O que usar no lugar |
|---|---|---|
| `gerar_visual_short.py` | Moldura e capa no padrão antigo | `scripts/gerar_capa_short.py` (capa) e os comandos de `references/montagem_shorts.md` (vídeo) |
| `cortar_shorts.py` | Montagem com moldura (usa o `gerar_visual_short.py`) | `references/montagem_shorts.md`; os filtros `delogo`, `marca_branca` e o recorte de webcam já estão lá |
| `modelo_short_interno.jpg`, `modelo_short_capa.jpg` | Modelos aprovados do padrão antigo (a palavra "linguágem" está com acento errado) | — |

Ficam guardados só como referência e histórico. Nenhum passo da skill deve chamar estes arquivos.
