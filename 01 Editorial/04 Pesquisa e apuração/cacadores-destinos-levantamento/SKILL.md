---
name: "cacadores-destinos-levantamento"
description: "Levanta todos os episódios do Caçadores de Destinos (Rede Tribuna — TV Tribuna/SBT e Band) no YouTube e no Tribuna Online e relaciona as localidades visitadas até a data de corte pedida."
---

# Caçadores de Destinos — levantamento de episódios e localidades

Varre o programa **Caçadores de Destinos**, da Rede Tribuna (ES), e entrega a lista de localidades já visitadas na TV, com data, temporada e link de cada episódio. Data de corte padrão: 31/12/2025 (Mário pode pedir outra).

## O programa (contexto para classificar)

| Fase | Período | Formato | Apresentação |
| --- | --- | --- | --- |
| T1 | mar/2023 – início/2024 | Quadro de ~5 min no Tribuna Notícias 1ª Edição, quintas (TV Tribuna/SBT) + podcast | Liliajane Mallmann e Matheus Simão |
| T2 | 04/05/2024 – dez/2024 | Programa de sábado, ~26 min (TV Tribuna/SBT) + quadro no TN1 | Kamila Rangel |
| T3 | 2025 em diante | Programa de sábado, 30 min, 18h50, reprise domingo 8h (TV Tribuna/Band) | Kamila Rangel |

O jornal A Tribuna publica, toda semana, duas matérias sobre o destino do programa (editoria `/cacadoresdedestinos/`). Em 2023 o quadro de TV seguia o tema do jornal de domingo.

## Fontes

1. **YouTube — canal Tribuna Online** (`@tribunaonline`, ID `UCqfWrrb93DNG-HywXC_46Lw`)
   - Playlist principal "Caçadores de Destinos": `PLQ6gIP3yEUmWoPJrbymuyksCZh9oOJxib`
   - ~41 playlists "Conheça <Município> | Caçadores de Destinos" (agrupam os vídeos por município — use para atribuir município a vídeos sem data)
   - Episódios completos trazem no título `[COMPLETO] - dd/mm/aaaa`
2. **Tribuna Online** — sitemaps públicos (`/sitemap/statics/sitemap-articles.xml`), que dão data e título de cada matéria. Não usar `/ajax/` (bloqueado no robots.txt).

## Passo 1 — YouTube (listagem rasa funciona da nuvem)

```bash
pip install --break-system-packages -q yt-dlp
mkdir -p cd && cd cd
# todas as playlists do canal, filtrando as do programa
yt-dlp --flat-playlist --extractor-args "youtube:lang=pt" --print "%(id)s|%(title)s" \
  "https://www.youtube.com/@tribunaonline/playlists" | grep -i -E "ca[cç]adores" > playlists.txt
# itens de cada playlist (id|título|duração)
mkdir -p pls; while IFS='|' read -r id t; do
  yt-dlp --flat-playlist --extractor-args "youtube:lang=pt" --print "%(id)s|%(title)s|%(duration)s" \
    "https://www.youtube.com/playlist?list=$id" > "pls/$id.txt"; done < playlists.txt
# busca no canal para pegar o que não está em playlist
yt-dlp --flat-playlist --extractor-args "youtube:lang=pt" --print "%(id)s|%(title)s|%(duration)s" \
  "https://www.youtube.com/@tribunaonline/search?query=Ca%C3%A7adores%20de%20Destinos" > busca.txt
```

- Sempre `lang=pt`: sem isso o YouTube devolve títulos traduzidos para o inglês.
- Os títulos contêm `|` — ao separar campos, o id é o primeiro e a duração o último; o título é o meio.
- Itens com título `NA` são vídeos indisponíveis: contar e relatar, não inventar.
- **Não** abrir vídeo a vídeo (extração completa) a partir da nuvem: o YouTube responde "Sign in to confirm you're not a bot". Não trocar de cliente, usar proxy, espelho ou cookies de terceiros para contornar — a data já vem no título dos completos e o resto se resolve pelo jornal.

## Passo 2 — Tribuna Online (matérias datadas)

Script `cd_tribuna.py` (listar matérias por período e extrair texto + fotos de uma matéria):

```python
#!/usr/bin/env python3
import csv, html, json, os, re, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://tribunaonline.com.br/sitemap/statics/"
def get(url, timeout=60):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")
def listar(de="2023-03-01", ate="2025-12-31"):
    idx = get(BASE + "sitemap-articles.xml")
    parts = sorted((int(n), u) for u, n in re.findall(r"<loc>([^<]*sitemap-articles-(\d+)-\d+\.xml)</loc>", idx) if int(n) >= 136001)
    w = csv.writer(sys.stdout); w.writerow(["data", "titulo", "url"])
    for n, u in parts:
        try: t = get(u)
        except Exception as e: print(f"falhou {u}: {e}", file=sys.stderr); continue
        last = ""
        for blk in re.findall(r"<url>(.*?)</url>", t, re.S):
            loc = re.search(r"<loc>(.*?)</loc>", blk).group(1)
            pd = re.search(r"<news:publication_date>(.*?)</news:publication_date>", blk)
            tt = re.search(r"<news:title>(.*?)</news:title>", blk, re.S)
            d = pd.group(1)[:10] if pd else ""; title = html.unescape(tt.group(1).strip()) if tt else ""
            last = max(last, d)
            if ("cacadoresdedestinos" in loc or "caçadores de destino" in (loc + title).lower()) and de <= d <= ate:
                w.writerow([d, title, loc])
        if last and last > ate: break
def materia(url, saida):
    os.makedirs(saida, exist_ok=True); t = get(url)
    i = t.find('class="mw-article-body"'); seg = t[i:i + 80000]
    for stop in ("Ícone tags", "Sugerimos este vídeo", "MATÉRIAS RELACIONADAS"):
        j = seg.find(stop); seg = seg[:j] if j > 0 else seg
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", seg, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(br|/p|/h\d|/li|/figcaption)[^>]*>", "\n", txt)))
    texto = "\n".join(l for l in (re.sub(r"[ \t]+", " ", x).strip() for x in txt.splitlines()) if l and not l.startswith('class="'))
    fotos = []
    for u in re.findall(r'https://cdn\d?\.tribunaonline\.com\.br/img/inline/[^"\'\s)?]+', t[max(0, i - 30000):i + 80000]):
        u = html.unescape(u)
        if "/970x600/" in u and u not in fotos: fotos.append(u)
    for k, u in enumerate(fotos, 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                open(os.path.join(saida, f"foto_{k:02d}.webp"), "wb").write(r.read())
        except Exception as e: print(f"foto falhou {u}: {e}", file=sys.stderr)
    open(os.path.join(saida, "materia.txt"), "w").write(texto)
    json.dump({"url": url, "fotos": fotos}, open(os.path.join(saida, "materia.json"), "w"), ensure_ascii=False, indent=1)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "listar":
        listar(a[a.index("--de") + 1] if "--de" in a else "2023-03-01", a[a.index("--ate") + 1] if "--ate" in a else "2025-12-31")
    elif a and a[0] == "materia":
        materia(a[1], a[a.index("--saida") + 1] if "--saida" in a else "materia")
```

`python3 cd_tribuna.py listar --ate 2025-12-31 > materias.csv` (leva ~5 min; os IDs de artigo pulam faixas — sitemap 404 é normal).

Para descobrir o município de uma matéria com apelido ("Princesinha do Caparaó", "Suíça Capixaba", "Capital da Amizade"), leia o `articleBody`/`description` do JSON-LD da página.

## Passo 3 — montar a linha do tempo e decidir cada semana

Para cada sábado de 04/05/2024 até o corte, ponha lado a lado: o episódio `[COMPLETO]` com data a ±3 dias e as matérias publicadas 1 a 7 dias depois. Regras:

- Episódio `[COMPLETO]` com data no título = fonte principal ("vídeo").
- Sábado sem vídeo completo, mas com par de matérias sobre um destino na semana seguinte = episódio daquele destino ("jornal", data aproximada).
- Datas de título trocadas ou inválidas acontecem (ex.: Iúna e Santa Teresa em ago/2025, "37/06/2025" em Venda Nova): corrija pela sequência semanal e anote na observação.
- 2023 (T1): confirme pelas matérias "Caçadores na TV" / "Assista ao episódio" (até jun/2023) e pelos vídeos numerados `#1…#8`; depois disso, tema do jornal de domingo + vídeo curto do canal com o mesmo título.
- Vídeos curtos sem data: use a playlist "Conheça <Município>" para atribuir o município.
- Episódios temáticos (Dia das Crianças, Dia da Mulher, Restaurant Week, Feira dos Municípios, Grande Vitória) entram na lista de episódios, mas não na contagem por município.

## Passo 4 — entregar

Um Doc (tipo Docs, pelo conector Claude Docs) com:

1. Lead de uma frase: quantos municípios dos 78, quantos episódios por fase.
2. **Municípios visitados** — tabela Município | Vezes | Quando foi ao ar (ordem alfabética).
3. **Municípios ainda não visitados** — lista corrida (compare com os 78 municípios do ES).
4. **Episódios** — tabela Data | Localidade/tema | Fonte (link do YouTube quando houver), do mais recente ao mais antigo.
5. **Como foi feito e fontes** — bases cruzadas, contagem de vídeos indisponíveis, ressalvas de data.

Guarde também `episodios.csv` (data, temporada, localidade_tema, municipios, youtube, comprovacao, obs) — é a entrada da skill `cacadores-destinos-conteudo`.

## Atualização

Para atualizar depois do corte: rode os passos 1–2 só com `--de` igual ao último sábado já levantado e acrescente as linhas novas. Levantamento de referência (corte 31/12/2025): 115 episódios/quadros (34 em 2023, 32 em 2024, 49 em 2025), 53 municípios visitados, 25 não visitados, 73 episódios com vídeo.