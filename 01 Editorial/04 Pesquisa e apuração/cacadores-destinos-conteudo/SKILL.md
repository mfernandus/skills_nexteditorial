---
name: "cacadores-destinos-conteudo"
description: "Puxa o conteúdo de episódios do Caçadores de Destinos (Rede Tribuna) — transcrição em texto corrido, frames do vídeo e matérias e fotos do Tribuna Online — a partir do link do YouTube, da localidade ou da lista de episódios."
---

# Caçadores de Destinos — conteúdo dos episódios

Para cada episódio pedido, entrega: **texto corrido** do programa (transcrição limpa), **frames** do vídeo com minutagem, as **matérias e fotos** do Tribuna Online da mesma semana e uma tabela dos **lugares, pessoas e contatos** citados.

Entrada aceita: link/ID do YouTube; localidade + data ("Araguaia, jul/2025"); "aleatório"; ou "todos" (lote). Para localidade, data, aleatório ou lote, use o `episodios.csv` da skill `cacadores-destinos-levantamento` (rode-a antes se não houver).

## Onde cada parte roda

| Parte | Onde | Por quê |
| --- | --- | --- |
| Legenda e vídeo do YouTube | **Mac do Mário**, pelo app desktop (`device_bash`) — ou o Chrome dele | O YouTube bloqueia servidores em nuvem com "Sign in to confirm you're not a bot" |
| Matérias e fotos do Tribuna Online | Nuvem ou Mac | Páginas públicas, sem bloqueio |
| Limpeza do texto, escolha dos frames, Doc | Nuvem | — |

Regras firmes:
- **Não contornar** o bloqueio do YouTube na nuvem: nada de trocar de cliente do yt-dlp, proxy, espelhos (Invidious/Piped) ou cookies de terceiros. Se o Mac não estiver conectado, entregue o que dá e diga que legenda e frames completos ficam para quando o Mac estiver ligado com o app aberto.
- **Plano B na nuvem (sem Mac):** as imagens estáticas do YouTube são públicas e já são frames do programa — `https://i.ytimg.com/vi/<ID>/maxresdefault.jpg` (capa) e `maxres1.jpg`, `maxres2.jpg`, `maxres3.jpg` (cenas em ~25%, ~50% e ~75% da duração). Pegue as quatro do episódio completo e as quatro do corte de ~5 min do TN1 (vídeo curto da mesma playlist "Conheça <Município>"): são 8 frames. Olhe cada uma antes de legendar. O texto corrido, nesse caso, sai provisório, escrito com as matérias do jornal, e é marcado assim no Doc.
- No Mac, se faltar `yt-dlp` ou `ffmpeg`, peça para instalar (`brew install yt-dlp ffmpeg`) antes de seguir.
- O conteúdo é da Rede Tribuna: serve de referência e pauta interna. Não republicar texto, frames ou fotos nos sites da Next; para matéria própria, reescrever e usar imagens próprias (NX Fotos).

## Passo 1 — no Mac: legenda, vídeo e frames

Pasta padrão: `~/CacadoresDeDestinos/<aaaa-mm-dd>_<localidade>/`. Script `extrair_episodio.sh`:

```bash
#!/bin/bash
# Uso: bash extrair_episodio.sh <ID_YOUTUBE> <pasta_destino>
set -euo pipefail
ID="$1"; OUT="$2"; mkdir -p "$OUT/frames"; cd "$OUT"
command -v yt-dlp >/dev/null || { echo "Falta yt-dlp (brew install yt-dlp)"; exit 2; }
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg (brew install ffmpeg)"; exit 2; }
yt-dlp --skip-download --write-info-json --write-subs --write-auto-subs \
  --sub-langs "pt.*,pt" --sub-format vtt -o "episodio.%(ext)s" -- "$ID"
yt-dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]/b" \
  --merge-output-format mp4 -o "episodio.%(ext)s" -- "$ID"
# frames: cada troca de cena + 1 a cada 45 s como garantia
ffmpeg -loglevel error -y -i episodio.mp4 \
  -vf "select='gt(scene,0.35)',scale=1280:-2,showinfo" -vsync vfr frames/cena_%03d.jpg 2> frames/cenas.log || true
ffmpeg -loglevel error -y -i episodio.mp4 -vf "fps=1/45,scale=1280:-2" frames/t45_%03d.jpg
grep -o "pts_time:[0-9.]*" frames/cenas.log | cut -d: -f2 > frames/cenas_tempos.txt || true
ls frames/*.jpg | wc -l | xargs echo "frames extraídos:"
```

`device_bash` tem limite de 45 s por chamada: rode o download em segundo plano (`nohup bash extrair_episodio.sh ID PASTA > log.txt 2>&1 &`) e acompanhe pelo `log.txt`. Para trazer arquivos para a nuvem, use `device_stage_files`; para gravar o resultado no Mac, `device_commit_files`.

## Passo 2 — transcrição limpa (`vtt_para_texto.py`)

A legenda automática repete cada fala 2–3 vezes. Este script deixa cada fala uma vez, em blocos de ~30 s com minutagem:

```python
#!/usr/bin/env python3
import re, sys
def ts(s):
    h, m, r = s.split(":"); return int(h) * 3600 + int(m) * 60 + float(r)
def main(path, bloco=30):
    txt = open(path, encoding="utf-8").read()
    cues = re.findall(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> [^\n]+\n(.*?)(?:\n\n|\Z)", txt, re.S)
    falas, ultima = [], ""
    for ini, corpo in cues:
        for linha in corpo.splitlines():
            linha = re.sub(r"<[^>]+>", "", linha).strip()
            linha = re.sub(r"\[(Música|Aplausos|Risos)\]", "", linha, flags=re.I).strip()
            if not linha or linha == ultima: continue
            if ultima and linha.startswith(ultima): falas[-1] = (falas[-1][0], linha)
            else: falas.append((ts(ini), linha))
            ultima = linha
    atual, inicio = [], None
    for t, linha in falas:
        if inicio is None: inicio = t
        if t - inicio >= bloco and atual:
            print(f"[{int(inicio)//60:02d}:{int(inicio)%60:02d}] " + " ".join(atual) + "\n"); atual, inicio = [], t
        atual.append(linha)
    if atual: print(f"[{int(inicio)//60:02d}:{int(inicio)%60:02d}] " + " ".join(atual))
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 30)
```

## Passo 3 — texto corrido

A partir da transcrição limpa, Claude escreve o texto corrido do episódio:
- Pontuação e maiúsculas corrigidas; parágrafos por atrativo/parada; minutagem no início de cada parágrafo.
- Falas identificadas quando claro: **Kamila Rangel** (T2/T3) ou **Liliajane Mallmann / Matheus Simão** (T1) e entrevistados pelo nome/cargo que aparecem.
- Nomes próprios (lugares, pratos, pessoas) conferidos contra a matéria do Tribuna da mesma semana — a legenda automática erra nomes (ex.: "Araguaya", "Itagraçu").
- Nada inventado: trecho inaudível vira `[inaudível]`.

## Passo 4 — matérias do Tribuna Online

Ache as matérias da semana no `materias.csv` do levantamento (mesmo município, 1 a 12 dias após o sábado) e extraia texto + fotos 970x600 com `python3 cd_tribuna.py materia <URL> --saida materias/1` (script na skill de levantamento).

## Passo 5 — escolher frames

De todos os frames, escolha 12–20: um ou dois por atrativo, nítidos, sem tarja de crédito cobrindo a cena, incluindo abertura, apresentadora em cena e paisagens. Olhe cada imagem (Read) antes de escolher. Legenda: `mm:ss — o que aparece`.

## Passo 6 — entregar

Um Doc por episódio (tipo Docs, conector Claude Docs), título `Caçadores de Destinos — <Localidade> (<dd/mm/aaaa>)`:
1. Lead: data, temporada/canal, apresentação, duração, link do vídeo.
2. **Roteiro do episódio** — tabela Minutagem | Parada/atrativo | O que mostra.
3. **Texto corrido** (Passo 3).
4. **Frames** — imagens enviadas pelo conector (topic.uploads), cada uma com a legenda.
5. **Lugares, pessoas e contatos** — tabela Nome | Tipo | Contato/horário (telefone, @, horário citados).
6. **Fontes** — vídeo e matérias.

Em lote ("todos"): processe um episódio por vez, pule os que já têm pasta completa, espere ~20 s entre downloads, e ao final entregue um Doc índice com o link de cada episódio e o que faltou.