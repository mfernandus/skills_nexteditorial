---
name: "raspagem-web-next"
description: "Busca e leitura de páginas pela API do Firecrawl, com o Apify de reserva quando os créditos acabam, para as rotinas Diversão e Arte, Fé e Política e Datafé. Diz onde ficam as chaves (na memória, nunca na skill) e traz o script raspar.py, os tetos de crédito por rotina, o que nunca se raspa e os avisos de crédito baixo ou esgotado. Carregar só quando a rotina citar esta skill."
---

# Raspagem na web: Firecrawl, com Apify de reserva

Skill de apoio do `padrao-publicacao-next`, criada em 17/11/2026 a pedido de Mário Fernando. Vale com a mesma força do padrão. Carregue uma vez por execução, só nas rotinas que a citam: `diversao-e-arte-esbrasil`, `politica-comunhao`, `datafe-materia-diaria-comunhao`, `atualizacao-cnpj-templos` e os trabalhos sob demanda do Datafé (seção 7).

**Para que serve:** achar pauta e nome (de artista, bar, casa de show, político) com o texto das páginas na mesma chamada, descobrir as URLs de um site sem ler página por página e ler páginas que só carregam por JavaScript (Sympla por cidade, datafe.com.br). Não serve para abrir site que bloqueia leitura automática (seção 3).

## 1. Chaves e contas

**As chaves não ficam nesta skill.** As skills sobem de hora em hora para o repositório público do GitHub, e a varredura de segredos da sincronização não reconhece chave do Firecrawl nem do Apify. As chaves ficam só na memória do Claude, no arquivo **`/areas/raspagem-chaves.md`**, como as credenciais do WhatsApp.

No começo da execução:

1. Leia `/areas/raspagem-chaves.md` com `memory_read`. Se não existir, não raspe: siga com WebFetch e WebSearch e registre em Pendências "raspagem: chaves não salvas na memória (/areas/raspagem-chaves.md)".
2. Grave o texto do arquivo em `memoria_chaves.txt`, na pasta de trabalho, e rode `python3 raspar.py importar memoria_chaves.txt`. O script pega as chaves do Firecrawl (começam com `fc-`) e do Apify (começam com `apify_api_`) na ordem em que aparecem, grava `raspagem_chaves.json` e apaga o texto.
3. As contas são usadas nessa ordem: quando uma conta do Firecrawl acaba (erro 402), o script passa para a próxima; quando todas acabam, passa para o Apify.

- **Trocar ou somar conta:** Mário pede, numa conversa comum (fora de projeto), para atualizar `/areas/raspagem-chaves.md`. Nada muda nas skills.
- **Contas novas:** só contas próprias e legítimas (plano pago, ou conta de outra pessoa ou empresa da casa, com autorização). Conta gratuita aberta só para ganhar créditos de novo pode ser suspensa pelo serviço, junto com as outras.
- Nunca escreva chave em skill, matéria, resumo, notificação, doc do projeto ou commit.

## 2. O script

Grave `raspar.py` na mesma pasta (o código está no fim desta skill) e use:

| Comando | O que faz | Custo no Firecrawl |
|---|---|---|
| `python3 raspar.py creditos` | Saldo de cada conta (Firecrawl e Apify) e o aviso geral | grátis |
| `python3 raspar.py teto N` | Teto de créditos desta execução (seção 4) | grátis |
| `python3 raspar.py search "consulta" --limite 5 --dias 7` | Busca na web, com título, resumo e URL | 2 a cada 10 resultados |
| `... search ... --conteudo` | A busca já traz o texto de cada página | + 1 por resultado |
| `python3 raspar.py scrape URL` | Lê uma página (inclusive JavaScript e PDF) em markdown | 1 por página |
| `python3 raspar.py map URL --busca termo` | Lista as URLs de um site que têm o termo | 1 |
| `python3 raspar.py uso` | Créditos gastos nesta execução | grátis |

- A saída é JSON. `provedor` diz quem respondeu (firecrawl ou apify); `aviso` aparece quando uma conta acabou ou a reserva entrou; `bloqueado: true` marca resultado de busca que é só pista (seção 3).
- Prefira `search` sem `--conteudo` e depois `scrape` só das páginas que vão virar pauta. `--conteudo` só quando os resultados forem quase todos fontes da rotina.
- O Apify (ator `apify/rag-web-browser`) faz busca no Google e leitura de página; o `map` dele é a lista de links da página. É mais lento: conte até 2 minutos por chamada.
- Erro 429 (limite por minuto): o script espera 30 segundos e repete uma vez.

## 3. O que nunca se raspa

**Esta seção vale acima de qualquer rotina**, como as seções 2.1 a 2.3 do padrão.

1. **Site que bloqueia leitura automática não se abre por Firecrawl nem Apify.** Vale a regra do padrão (seção 5: não use curl, Python, Firecrawl ou Apify para burlar página bloqueada). O script recusa os conhecidos: Ales (al.es.gov.br), teatro.ufes.br, Folha Vitória, Le Billet, esbrasil.com.br, ES Hoje, Bandes, prefeituras de Guarapari, Cachoeiro, Linhares, Cariacica, Marataízes, Vila Velha, Domingos Martins e Anchieta e a página /biografia da Câmara. Esses continuam como cada rotina já manda (navegador só para ler, ou troca de pauta).
2. **Domínio novo:** tente primeiro o WebFetch. Se ele abrir a página vazia porque ela carrega por JavaScript, pode raspar. Se ele recusar, der bloqueio, robots ou erro de acesso, **não raspe**: troque de fonte e acrescente o domínio à lista do script na próxima revisão desta skill.
3. **Redes sociais nunca** (Instagram, Facebook, TikTok, X, LinkedIn, Threads, WhatsApp). Na busca, elas aparecem só como pista (título e resumo), marcadas `bloqueado`. A confirmação vem da fonte oficial; o perfil, quando precisar, pelo navegador e só para ler, como a rotina já manda.
4. **Nada de formulário, login, clique ou página paga.** Não use as funções de interação nem de agente do Firecrawl.
5. **Pessoas:** nomes só de artistas, produtores, donos de casa de show e agentes públicos, para a pauta. Não monte lista ou perfil de pessoa privada.
6. **Fé de político:** a raspagem só acha a fonte. A confirmação segue a regra da rotina (fé pública e declarada numa das fontes aceitas, aberta e lida). Nunca deduza fé ou igreja por nome, partido, foto, evento ou parente.
7. **Resultado de agregador** (TocaOnde, Vamos e afins) e de imprensa é pista, nunca fonte nem crédito (padrão, seção 5).

## 4. Tetos de crédito

O plano gratuito do Firecrawl tem 1.000 créditos por mês (renova no dia 16). Logo depois de `creditos`, rode `python3 raspar.py teto N` com o teto da rotina. Chegou ao teto, siga com WebFetch e WebSearch.

| Rotina | Teto | Mês (estimado) |
|---|---|---|
| `diversao-e-arte-esbrasil` | 8 por rodada | cerca de 480 |
| `politica-comunhao` | 4 por rodada | cerca de 210 |
| `datafe-materia-diaria-comunhao` | 3 por dia | cerca de 90 |
| `atualizacao-cnpj-templos` | 2 por carga | 2 |
| Datafé sob demanda (seção 7) | 60 por pedido, salvo ordem de Mário | o que sobrar |

Com crédito **baixo** (seção 5), corte o teto da rotina pela metade.

## 5. Créditos baixos ou esgotados: avisar o Mário

Rode `python3 raspar.py creditos` no começo da execução. O campo `aviso` diz o estado:

- **aviso diário (sentinela):** a rotina `datafe-materia-diaria-comunhao` (8h37, todos os dias) roda `creditos` sempre, mesmo sem usar a raspagem, porque é ela que avisa o Mário uma vez por dia. Com qualquer conta baixa, esgotada, com erro, ou sem chave na memória, a primeira linha da notificação dela é o aviso, nesta ordem de gravidade: "Raspagem parada: Firecrawl e Apify sem créditos. Compre créditos ou mande outra chave." / "Firecrawl sem créditos: compre créditos ou mande outra chave. As rotinas estão usando o Apify." / "Firecrawl com créditos baixos: N restantes, renova em DD/MM." / "Apify com crédito baixo: US$ X de US$ Y usados no mês." / "Raspagem: chaves não salvas na memória." O aviso "Apify ainda sem chave" sai só às segundas.
- **baixo** (`firecrawl_baixo`: 20% do plano ou menos; `apify_baixo`: 80% do limite do mês já gasto), nas outras rotinas: registre em Pendências do resumo "créditos de raspagem baixos: Firecrawl N restantes até DD/MM"; elas não notificam só por isso.
- **esgotou durante a execução** (o `creditos` do começo mostrava saldo e uma chamada devolveu `aviso` com "esgotado" ou "usando Apify"): **notifique na hora**, mesmo que a rodada não tenha matéria nova, com PushNotification começando por "Firecrawl sem créditos: compre créditos ou mande outra chave." e dizendo se o Apify assumiu.
- **já estava esgotado no começo:** siga com o Apify e ponha a frase acima na primeira linha da notificação da rodada, se ela for notificar; se não for, só em Pendências (o aviso diário já saiu de manhã).
- **raspagem parada** (Firecrawl e Apify sem saldo, ou sem chave do Apify): siga só com WebFetch e WebSearch, notifique na hora com "Raspagem parada: Firecrawl e Apify sem créditos. Compre créditos ou mande outra chave." e registre em Pendências.

## 6. No resumo da rotina

Em Pendências ou na parte própria da rotina, uma linha: "Raspagem: N créditos do Firecrawl nesta rodada (saldo S até DD/MM)", com "Apify usado M vezes" quando a reserva entrou. Nunca as chaves.

## 7. Datafé sob demanda

Quando Mário pedir trabalho de dados do Datafé (projeto do portal e banco no Lovable, docs no projeto "Evangelicos em numeros 2026"):

1. **Selo de fé dos eleitos** (fase 8b): `search` pelo nome + "evangélico", "pastor", "igreja" ou a denominação, e `scrape` da fonte achada. Regra da fase 8b: selo só com pesquisa Iser/Pública, declaração do próprio, fonte oficial ou duas reportagens; igreja só com fonte forte ou duas reportagens que a nomeiem; uma reportagem só fica pendente; Wikipédia nunca aprova. Cada evidência sai com URL, trecho, tipo de fonte e data, para o painel de revisão.
2. **Pesquisas novas com religião** (termômetro do /projecoes e /pesquisas): `search` dos últimos 30 dias por instituto ("Quaest religião evangélicos", "Datafolha evangélicos") e `scrape` do relatório (PDF conta 1 crédito por página). Só entra pesquisa que publica a fatia de evangélicos da amostra, pela regra do doc "pesquisas-religiao".
3. **Ler o datafe.com.br:** as páginas são feitas em JavaScript, e o WebFetch só mostra o cabeçalho. Para conferir o que a página mostra, `scrape`.

## 8. Código do script (`raspar.py`)

```python
#!/usr/bin/env python3
"""Raspagem da Next: Firecrawl primeiro, Apify de reserva (skill raspagem-web-next).

python3 raspar.py creditos
python3 raspar.py teto 8                       # teto de créditos desta execução
python3 raspar.py search "consulta" [--limite 5] [--dias 7] [--conteudo]
python3 raspar.py scrape URL [--links] [--max 12000]
python3 raspar.py map URL [--busca termo] [--limite 50]
python3 raspar.py uso                          # créditos gastos nesta execução
python3 raspar.py importar ARQUIVO             # tira as chaves do texto da memória e grava raspagem_chaves.json

Lê as chaves de raspagem_chaves.json (pasta atual): {"firecrawl": ["fc-..."], "apify": ["apify_api_..."]}.
Saída sempre em JSON. O campo "aviso" aparece quando uma conta acabou ou a reserva entrou.
"""
import json, math, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse

CHAVES = Path("raspagem_chaves.json")
USO = Path("raspagem_uso.json")
FC = "https://api.firecrawl.dev/v2"
AP = "https://api.apify.com/v2"
BAIXO_FC = 0.20      # 20% do plano ou menos = baixo
BAIXO_AP = 0.80      # 80% do limite mensal gasto ou mais = baixo

# Sites que bloqueiam leitura automática ou que as skills mandam não raspar.
BLOQUEADOS = {
    "al.es.gov.br", "teatro.ufes.br", "folhavitoria.com.br", "lebillet.com.br",
    "esbrasil.com.br", "eshoje.com.br", "bandes.com.br",
    "guarapari.es.gov.br", "cachoeiro.es.gov.br", "linhares.es.gov.br", "cariacica.es.gov.br",
    "marataizes.es.gov.br", "vilavelha.es.gov.br", "domingosmartins.es.gov.br", "anchieta.es.gov.br",
    "instagram.com", "facebook.com", "fb.com", "tiktok.com", "x.com", "twitter.com", "linkedin.com",
    "threads.net", "whatsapp.com", "kwai.com",
}
CAMINHOS_BLOQUEADOS = [("camara.leg.br", "/biografia")]


def saida(obj, codigo=0):
    print(json.dumps(obj, ensure_ascii=False, indent=1)); sys.exit(codigo)


def chaves():
    if not CHAVES.exists():
        saida({"erro": "raspagem_chaves.json não existe: rode o passo da seção 1 da skill raspagem-web-next (importar da memória)"}, 2)
    c = json.loads(CHAVES.read_text())
    return [k for k in c.get("firecrawl", []) if k and "COLE" not in k], [k for k in c.get("apify", []) if k and "COLE" not in k]


def bloqueado(url):
    try:
        h = urlparse(url).hostname or ""
    except Exception:
        return True
    h = h.lower()
    if any(h == d or h.endswith("." + d) for d in BLOQUEADOS):
        return True
    return any((h == d or h.endswith("." + d)) and p in urlparse(url).path for d, p in CAMINHOS_BLOQUEADOS)


def http(metodo, url, token, corpo=None, timeout=120):
    cmd = ["curl", "-sS", "-m", str(timeout), "-X", metodo, "-H", f"Authorization: Bearer {token}",
           "-H", "Content-Type: application/json", "-w", "\n%{http_code}", url]
    if corpo is not None:
        cmd[cmd.index(url):cmd.index(url)] = ["--data-binary", json.dumps(corpo)]
    for tentativa in range(2):
        r = subprocess.run(cmd, capture_output=True, text=True)
        txt, _, cod = r.stdout.rpartition("\n")
        cod = int(cod) if cod.strip().isdigit() else 0
        if cod == 429 and tentativa == 0:
            time.sleep(30); continue
        try:
            dado = json.loads(txt) if txt.strip() else {}
        except Exception:
            dado = {"bruto": txt[:500]}
        return cod, dado
    return cod, dado


def uso():
    return json.loads(USO.read_text()) if USO.exists() else {"firecrawl": 0, "apify_execucoes": 0, "teto": None}


def gastar(n, prov="firecrawl"):
    u = uso()
    if prov == "firecrawl":
        u["firecrawl"] += n
    else:
        u["apify_execucoes"] += 1
    USO.write_text(json.dumps(u))


def checar_teto(previsto):
    u = uso()
    if u.get("teto") is not None and u["firecrawl"] + previsto > u["teto"]:
        saida({"erro": f"teto da execução atingido ({u['firecrawl']} de {u['teto']} créditos): siga com WebFetch e WebSearch"}, 3)


# ---------------- Apify (reserva) ----------------
def apify(token, query, n=3, js=False, links=False):
    corpo = {"query": query, "maxResults": n, "outputFormats": ["markdown"] + (["links"] if links else []),
             "scrapingTool": "browser-playwright" if js else "raw-http", "requestTimeoutSecs": 90}
    return http("POST", f"{AP}/acts/apify~rag-web-browser/run-sync-get-dataset-items", token, corpo, timeout=150)


def item_apify(it, maxc):
    md = it.get("markdown") or it.get("text") or ""
    meta = it.get("metadata") or {}
    sr = it.get("searchResult") or {}
    return {"url": meta.get("url") or sr.get("url") or it.get("url"), "titulo": meta.get("title") or sr.get("title"),
            "descricao": sr.get("description") or meta.get("description"), "markdown": md[:maxc] if md else None,
            "links": it.get("links")}


def via_apify(fazer, motivo):
    _, aps = chaves()
    for i, t in enumerate(aps):
        cod, dado = fazer(t)
        if cod in (402, 403) or (isinstance(dado, dict) and "usage" in json.dumps(dado.get("error", "")).lower()):
            continue
        if 200 <= cod < 300:
            gastar(0, "apify")
            return {"provedor": "apify", "conta": i + 1, "aviso": motivo, "dado": dado}
        return {"provedor": "apify", "conta": i + 1, "aviso": motivo, "erro": f"HTTP {cod}", "dado": dado}
    saida({"aviso": "raspagem_parada", "erro": motivo + "; Apify sem conta com saldo (ou sem chave). Siga com WebFetch e WebSearch e avise o Mário."}, 4)


def via_firecrawl(caminho, corpo, previsto):
    """Tenta as contas do Firecrawl em ordem; devolve (resultado, aviso) ou (None, motivo) se todas acabaram."""
    checar_teto(previsto)
    fcs, _ = chaves()
    esgotadas = []
    for i, k in enumerate(fcs):
        cod, dado = http("POST", f"{FC}/{caminho}", k, corpo)
        if cod == 402:
            esgotadas.append(i + 1); continue
        if 200 <= cod < 300:
            gastar(dado.get("creditsUsed", previsto) if isinstance(dado, dict) else previsto)
            av = f"firecrawl_conta_{esgotadas}_esgotada: usando a conta {i + 1}" if esgotadas else None
            return {"provedor": "firecrawl", "conta": i + 1, "aviso": av, "dado": dado}, None
        return {"provedor": "firecrawl", "conta": i + 1, "erro": f"HTTP {cod}", "dado": dado}, None
    return None, ("firecrawl_esgotado" if fcs else "firecrawl_sem_chave")


# ---------------- comandos ----------------
def cmd_creditos():
    fcs, aps = chaves()
    out = {"firecrawl": [], "apify": [], "aviso": "ok"}
    estados = []
    for i, k in enumerate(fcs):
        cod, d = http("GET", f"{FC}/team/credit-usage", k)
        dd = d.get("data", {}) if isinstance(d, dict) else {}
        rest, plano = dd.get("remainingCredits"), dd.get("planCredits")
        est = "erro" if cod != 200 else ("esgotado" if (rest or 0) <= 0 else
               "baixo" if plano and rest <= max(BAIXO_FC * plano, 1) else "ok")
        estados.append(est)
        out["firecrawl"].append({"conta": i + 1, "restantes": rest, "plano": plano,
                                 "renova_em": dd.get("billingPeriodEnd"), "estado": est})
    for i, t in enumerate(aps):
        cod, d = http("GET", f"{AP}/users/me/limits", t)
        dd = d.get("data", {}) if isinstance(d, dict) else {}
        lim = (dd.get("limits") or {}).get("maxMonthlyUsageUsd")
        cur = (dd.get("current") or {}).get("monthlyUsageUsd")
        est = "erro" if cod != 200 else ("esgotado" if lim and cur is not None and cur >= lim else
               "baixo" if lim and cur is not None and cur >= BAIXO_AP * lim else "ok")
        out["apify"].append({"conta": i + 1, "uso_usd": cur, "limite_usd": lim, "estado": est})
    fc_ok = [e for e in estados if e in ("ok", "baixo")]
    if fcs and not fc_ok:
        out["aviso"] = "firecrawl_esgotado"
    elif fcs and all(e != "ok" for e in estados):
        out["aviso"] = "firecrawl_baixo"
    ap_est = [a["estado"] for a in out["apify"]]
    if aps and all(e in ("esgotado", "erro") for e in ap_est):
        out["aviso"] += ";apify_esgotado"
    elif aps and all(e != "ok" for e in ap_est):
        out["aviso"] += ";apify_baixo"
    if not aps:
        out["aviso"] += ";apify_sem_chave"
    saida(out)


def arg(nome, padrao=None, tipo=str):
    if nome in sys.argv:
        i = sys.argv.index(nome)
        return tipo(sys.argv[i + 1]) if tipo is not bool else True
    return padrao


def cmd_search(q):
    n = arg("--limite", 5, int); dias = arg("--dias", None, int); conteudo = arg("--conteudo", False, bool)
    maxc = arg("--max", 2500, int)
    if conteudo:   # não deixa o Firecrawl abrir site bloqueado ao trazer o conteúdo da busca
        q = q + " " + " ".join(f"-site:{d}" for d in sorted(BLOQUEADOS))
    corpo = {"query": q, "limit": n, "sources": ["web"], "location": "Brazil"}
    if dias:
        corpo["tbs"] = "qdr:d" if dias <= 1 else "qdr:w" if dias <= 7 else "qdr:m" if dias <= 31 else "qdr:y"
    if conteudo:
        corpo["scrapeOptions"] = {"formats": ["markdown"], "onlyMainContent": True}
    previsto = 2 * math.ceil(n / 10) + (n if conteudo else 0)
    r, motivo = via_firecrawl("search", corpo, previsto)
    if r and "erro" not in r:
        d = r.pop("dado").get("data", {})
        itens = d.get("web", d) if isinstance(d, dict) else d
        res = []
        for it in itens or []:
            url = it.get("url")
            md = it.get("markdown")
            if bloqueado(url):      # fica só como pista (título e resumo da busca), sem conteúdo da página
                res.append({"url": url, "titulo": it.get("title"), "descricao": it.get("description"), "bloqueado": True})
                continue
            res.append({"url": url, "titulo": it.get("title"), "descricao": it.get("description"),
                        "markdown": md[:maxc] if md else None})
        r["resultados"] = res
        saida(r)
    if r:
        saida(r, 1)
    qq = q + ("" if conteudo else " " + " ".join(f"-site:{d}" for d in ("instagram.com", "facebook.com", "tiktok.com"))) + (f" after:{time.strftime('%Y-%m-%d', time.localtime(time.time() - dias * 86400))}" if dias else "")
    rr = via_apify(lambda t: apify(t, qq, n), motivo + ": usando Apify")
    if "erro" not in rr:
        rr["resultados"] = [({**x, "markdown": None, "bloqueado": True} if bloqueado(x["url"]) else x)
                            for x in (item_apify(i, maxc) for i in rr.pop("dado") or [])]
    saida(rr)


def cmd_scrape(url):
    if bloqueado(url):
        saida({"erro": f"{url} está na lista de sites que não se raspam (bloqueio de leitura automática ou rede social)."}, 5)
    links = arg("--links", False, bool); maxc = arg("--max", 12000, int)
    corpo = {"url": url, "formats": ["markdown"] + (["links"] if links else []), "onlyMainContent": True, "waitFor": 1500}
    r, motivo = via_firecrawl("scrape", corpo, 1)
    if r and "erro" not in r:
        d = r.pop("dado").get("data", {})
        md = d.get("markdown") or ""
        meta = d.get("metadata", {})
        r.update({"url": meta.get("sourceURL") or url, "titulo": meta.get("title"), "status": meta.get("statusCode"),
                  "markdown": md[:maxc], "cortado": len(md) > maxc, "links": d.get("links") if links else None})
        saida(r)
    if r:
        saida(r, 1)
    rr = via_apify(lambda t: apify(t, url, 1, js=True, links=links), motivo + ": usando Apify")
    if "erro" not in rr:
        its = rr.pop("dado") or []
        rr.update(item_apify(its[0], maxc) if its else {"erro": "Apify não devolveu conteúdo"})
    saida(rr)


def cmd_map(url):
    if bloqueado(url):
        saida({"erro": f"{url} está na lista de sites que não se raspam."}, 5)
    busca = arg("--busca", None); n = arg("--limite", 50, int)
    corpo = {"url": url, "limit": n}
    if busca:
        corpo["search"] = busca
    r, motivo = via_firecrawl("map", corpo, 1)
    if r and "erro" not in r:
        d = r.pop("dado")
        ls = d.get("links") or d.get("data", {}).get("links") or []
        r["links"] = [(l if isinstance(l, dict) else {"url": l}) for l in ls if not bloqueado(l if isinstance(l, str) else l.get("url"))]
        saida(r)
    if r:
        saida(r, 1)
    rr = via_apify(lambda t: apify(t, url, 1, js=True, links=True), motivo + ": usando Apify (lista de links da página)")
    if "erro" not in rr:
        its = rr.pop("dado") or []
        ls = (its[0].get("links") or []) if its else []
        ls = [l if isinstance(l, str) else l.get("url") for l in ls]
        rr["links"] = [{"url": l} for l in ls if l and not bloqueado(l) and (not busca or busca.lower() in l.lower())][:n]
    saida(rr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        saida({"uso": __doc__})
    c = sys.argv[1]
    if c == "creditos":
        cmd_creditos()
    elif c == "teto":
        u = uso(); u["teto"] = int(sys.argv[2]); USO.write_text(json.dumps(u)); saida(u)
    elif c == "uso":
        saida(uso())
    elif c == "importar":
        p = Path(sys.argv[2]); txt = p.read_text(encoding="utf-8")
        fcs = list(dict.fromkeys(re.findall(r"\bfc-[0-9a-f]{32}\b", txt)))
        aps = list(dict.fromkeys(re.findall(r"\bapify_api_[A-Za-z0-9]{20,}\b", txt)))
        CHAVES.write_text(json.dumps({"firecrawl": fcs, "apify": aps})); p.unlink()
        saida({"firecrawl_contas": len(fcs), "apify_contas": len(aps),
               "aviso": "ok" if fcs else "sem_chave_firecrawl_na_memoria"})
    elif c == "search":
        cmd_search(sys.argv[2])
    elif c == "scrape":
        cmd_scrape(sys.argv[2])
    elif c == "map":
        cmd_map(sys.argv[2])
    else:
        saida({"erro": "comando desconhecido", "uso": __doc__}, 2)
```
