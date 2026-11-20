---
name: "raspagem-web-next"
description: "Raspagem na web pela API do Firecrawl, com até três contas usadas em ordem até acabar o limite de cada uma (sem Apify desde 20/11/2026). Vale para tudo da Next que precise de raspagem: rotinas e skills da ES Brasil, da Comunhão, do Datafé, do Destinos ES e do Prócidade, e as conversas e buscas do Mário. Use sempre que uma página não abrir na leitura comum por ser feita em JavaScript, quando for preciso descobrir as páginas de um site ou trazer o texto de vários resultados de busca de uma vez. Diz onde ficam as chaves (na memória, nunca na skill) e traz o script raspar.py, os tetos de crédito, o que nunca se raspa e os avisos de crédito baixo ou esgotado."
---

# Raspagem na web: Firecrawl, com as contas usadas em ordem

Skill de apoio do `padrao-publicacao-next`, criada em 17/11/2026 a pedido de Mário Fernando e atualizada em 20/11/2026 (só Firecrawl, sem Apify; as contas do Firecrawl são usadas em ordem até acabar o limite de cada uma). Vale com a mesma força do padrão. Carregue uma vez por execução.

**Onde vale (decisão do Mário Fernando, 20/11/2026): em tudo da Next que precise de raspagem.** Rotinas e skills da **ES Brasil** e da Comunhão (as que carregam o padrão e as que citam esta skill: `diversao-e-arte-esbrasil`, `politica-comunhao`, `datafe-materia-diaria-comunhao`, `atualizacao-cnpj-templos`), do Datafé (`validacao-diaria-datafe`, `datafe-manchetes-semana`, `verificacao-es-em-numeros` e os trabalhos sob demanda da seção 7), do Destinos ES (`atualizacao-mapas-destinos-es`, `cacadores-destinos-levantamento`, `cacadores-destinos-conteudo`), do Prócidade (`cidade-em-numeros-procidade`) e as conversas e buscas do Mário.

**Quando usar:** a leitura e a busca comuns (WebFetch e WebSearch) continuam em primeiro lugar, porque não gastam crédito. O Firecrawl entra quando elas não resolvem:
1. a página abre vazia ou só com o cabeçalho no WebFetch porque é feita em JavaScript (datafe.com.br, Sympla por cidade, mapas e guias de turismo, painéis de prefeitura);
2. é preciso descobrir as páginas de um site (`map`), em vez de abrir uma por uma;
3. uma busca precisa trazer o texto de vários resultados de uma vez (`search --conteudo`), quando isso economiza várias leituras;
4. o Mário pede raspagem.

Site que bloqueia leitura automática continua fora, em qualquer caso (seção 3).

**Sem terminal** (conversa sem acesso a comandos, ou sem acesso à api.firecrawl.dev): use o conector Firecrawl do Claude, se estiver ligado, com as mesmas regras e tetos. Ele gasta da conta em que foi conectado, não das três contas da seção 1: diga isso no fim da resposta.

**Para que serve:** achar pauta e nome (de artista, bar, casa de show, político) com o texto das páginas na mesma chamada, descobrir as URLs de um site sem ler página por página e ler páginas que só carregam por JavaScript (Sympla por cidade, datafe.com.br). Não serve para abrir site que bloqueia leitura automática (seção 3).

## 1. Chaves e contas

**As chaves não ficam nesta skill.** As skills sobem de hora em hora para o repositório público do GitHub, e a varredura de segredos da sincronização não reconhece chave do Firecrawl. As chaves ficam só na memória do Claude, no arquivo `raspagem-chaves.md`, como as credenciais do WhatsApp.

No começo da execução:

1. Leia a memória com `memory_read`, nesta ordem, e use o primeiro arquivo que existir:
   - `/areas/raspagem-chaves.md` (memória geral, que toda rotina, skill e conversa enxerga: é o lugar certo para as chaves valerem em tudo);
   - `/projects/01a1cb9e-07c7-76ea-9665-d2ce3c8093e0/areas/raspagem-chaves.md` (memória do projeto "Evangelicos em numeros 2026": só as conversas e as rotinas desse projeto a enxergam, como a `datafe-materia-diaria-comunhao`).

   Se nenhum dos dois existir, não raspe: siga com WebFetch e WebSearch e registre em Pendências "raspagem: chaves não salvas na memória (raspagem-chaves.md)".
2. Grave o texto do arquivo em `memoria_chaves.txt`, na pasta de trabalho, e rode `python3 raspar.py importar memoria_chaves.txt`. O script pega as chaves do Firecrawl (começam com `fc-`) na ordem em que aparecem no arquivo, grava `raspagem_chaves.json` e apaga o texto.
3. **Ordem de uso (decisão do Mário Fernando, 20/11/2026):** a conta 1 até acabar o limite. Quando ela responde "sem créditos" (erro 402), o script passa sozinho para a conta 2 e depois para a 3. Chave recusada (erro 401 ou 403) também passa para a seguinte. Quando todas acabam, a raspagem para e a rotina segue com WebFetch e WebSearch (seção 5).
4. **Apify não se usa mais** (decisão do Mário Fernando, 20/11/2026). Chave do Apify que ainda estiver na memória é ignorada pelo script.

- **Trocar ou somar conta:** Mário pede para atualizar o arquivo de chaves, de preferência numa conversa comum (fora de projeto), para que ele fique em `/areas/` e valha para todas as rotinas. Nada muda nas skills.
- **Contas:** só contas próprias e legítimas, de pessoas ou empresas da casa, com autorização. Conta gratuita aberta só para ganhar créditos de novo pode ser suspensa pelo serviço, junto com as outras.
- Nunca escreva chave em skill, matéria, resumo, notificação, doc do projeto ou commit.

## 2. O script

Grave `raspar.py` na mesma pasta (o código está no fim desta skill) e use:

| Comando | O que faz | Custo no Firecrawl |
|---|---|---|
| `python3 raspar.py creditos` | Saldo de cada conta, a conta em uso, o saldo somado, a próxima renovação e o aviso geral | grátis |
| `python3 raspar.py teto N` | Teto de créditos desta execução, somando as contas (seção 4) | grátis |
| `python3 raspar.py search "consulta" --limite 5 --dias 7` | Busca na web, com título, resumo e URL | 2 a cada 10 resultados |
| `... search ... --conteudo` | A busca já traz o texto de cada página | + 1 por resultado |
| `python3 raspar.py scrape URL` | Lê uma página (inclusive JavaScript e PDF) em markdown | 1 por página |
| `python3 raspar.py map URL --busca termo` | Lista as URLs de um site que têm o termo | 1 |
| `python3 raspar.py uso` | Créditos gastos nesta execução, no total e por conta | grátis |

- A saída é JSON. `conta` diz qual conta respondeu; `aviso` aparece quando uma conta acabou e a seguinte assumiu ou quando a raspagem parou; `bloqueado: true` marca resultado de busca que é só pista (seção 3).
- Prefira `search` sem `--conteudo` e depois `scrape` só das páginas que vão virar pauta. `--conteudo` só quando os resultados forem quase todos fontes da rotina.
- Erro 429 (limite por minuto): o script espera 30 segundos e repete uma vez.

## 3. O que nunca se raspa

**Esta seção vale acima de qualquer rotina**, como as seções 2.1 a 2.3 do padrão.

1. **Site que bloqueia leitura automática não se abre pelo Firecrawl.** Vale a regra do padrão (seção 5: não use curl, Python, Firecrawl ou outro serviço de raspagem para burlar página bloqueada). O script recusa os conhecidos: Ales (al.es.gov.br), teatro.ufes.br, Folha Vitória, Le Billet, esbrasil.com.br, ES Hoje, Bandes, prefeituras de Guarapari, Cachoeiro, Linhares, Cariacica, Marataízes, Vila Velha, Domingos Martins e Anchieta e a página /biografia da Câmara. Esses continuam como cada rotina já manda (navegador só para ler, ou troca de pauta).
2. **Domínio novo:** tente primeiro o WebFetch. Se ele abrir a página vazia porque ela carrega por JavaScript, pode raspar. Se ele recusar, der bloqueio, robots ou erro de acesso, **não raspe**: troque de fonte e acrescente o domínio à lista do script na próxima revisão desta skill.
3. **Redes sociais nunca** (Instagram, Facebook, TikTok, X, LinkedIn, Threads, WhatsApp). Na busca, elas aparecem só como pista (título e resumo), marcadas `bloqueado`. A confirmação vem da fonte oficial; o perfil, quando precisar, pelo navegador e só para ler, como a rotina já manda.
4. **Nada de formulário, login, clique ou página paga.** Não use as funções de interação nem de agente do Firecrawl.
5. **Pessoas:** nomes só de artistas, produtores, donos de casa de show e agentes públicos, para a pauta. Não monte lista ou perfil de pessoa privada.
6. **Fé de político:** a raspagem só acha a fonte. A confirmação segue a regra da rotina (fé pública e declarada numa das fontes aceitas, aberta e lida). Nunca deduza fé ou igreja por nome, partido, foto, evento ou parente.
7. **Resultado de agregador** (TocaOnde, Vamos e afins) e de imprensa é pista, nunca fonte nem crédito (padrão, seção 5).

## 4. Tetos de crédito

O plano gratuito do Firecrawl tem 1.000 créditos por mês em cada conta, e cada conta renova na própria data (o `creditos` mostra a de cada uma). Com três contas, são até 3.000 créditos por mês. Logo depois de `creditos`, rode `python3 raspar.py teto N` com o teto da rotina. Chegou ao teto, siga com WebFetch e WebSearch.

| Rotina | Teto | Mês (estimado) |
|---|---|---|
| `diversao-e-arte-esbrasil` | 8 por rodada | cerca de 480 |
| `politica-comunhao` | 4 por rodada | cerca de 210 |
| `datafe-materia-diaria-comunhao` | 3 por dia | cerca de 90 |
| `atualizacao-cnpj-templos` | 2 por carga | 2 |
| `validacao-diaria-datafe` | 5 por rodada | cerca de 150 |
| `datafe-manchetes-semana` e `verificacao-es-em-numeros` | 3 por rodada | cerca de 30 |
| Destinos ES (`atualizacao-mapas-destinos-es`, `cacadores-destinos-*`) | 10 por lote | conforme os lotes |
| Prócidade (`cidade-em-numeros-procidade`) | 15 por município | conforme os sites |
| Outras rotinas e skills, sem teto próprio | 2 por rodada | cerca de 300 |
| Conversas e buscas do Mário | 30 por pedido, salvo ordem dele; diga no fim quantos créditos gastou | o que sobrar |
| Datafé sob demanda (seção 7) | 60 por pedido, salvo ordem de Mário | o que sobrar |

Com crédito **baixo** (seção 5), corte o teto da rotina pela metade. A soma dos tetos tem de caber nos cerca de 3.000 créditos do mês: se o saldo somado cair rápido demais, avise o Mário em vez de aumentar tetos.

## 5. Créditos baixos ou esgotados: avisar o Mário

Rode `python3 raspar.py creditos` no começo da execução. O campo `aviso` diz o estado:

- **aviso diário (sentinela):** a rotina `datafe-materia-diaria-comunhao` (8h37, todos os dias) roda `creditos` sempre, mesmo sem usar a raspagem, porque é ela que avisa o Mário uma vez por dia. Quando houver um destes avisos, ele vai na primeira linha da notificação dela, nesta ordem de gravidade:
  - `firecrawl_esgotado`: "Raspagem parada: as contas do Firecrawl estão sem créditos. Compre créditos ou mande outra chave."
  - `firecrawl_erro` ou `conta_com_erro`: "Raspagem: a conta N do Firecrawl não respondeu (HTTP X). Confira a chave."
  - `firecrawl_baixo` (saldo somado das contas em 20% do plano somado, ou menos): "Firecrawl com créditos baixos: N restantes nas contas, a próxima renova em DD/MM."
  - `sem_chave`: "Raspagem: chaves não salvas na memória."
  - A troca de conta (`conta_N_em_uso`) não vai para a primeira linha, porque é automática e não pede ação: entra só em Pendências do resumo, como "Firecrawl: conta 1 sem créditos até DD/MM; em uso a conta 2 (N restantes)".
- **baixo**, nas outras rotinas: registre em Pendências do resumo "créditos de raspagem baixos: Firecrawl N restantes, próxima renovação DD/MM"; elas não notificam só por isso.
- **uma conta acabou durante a execução** e a seguinte assumiu (`aviso` como "conta 1 sem créditos: usando a conta 2"): siga normalmente e registre em Pendências; não notifique só por isso.
- **a última conta acabou durante a execução** (`aviso` `raspagem_parada`): **notifique na hora**, mesmo que a rodada não tenha matéria nova, com PushNotification começando por "Raspagem parada: as contas do Firecrawl estão sem créditos. Compre créditos ou mande outra chave.", siga só com WebFetch e WebSearch e registre em Pendências.
- **já estava parada no começo:** siga com WebFetch e WebSearch e ponha a frase acima na primeira linha da notificação da rodada, se ela for notificar; se não for, só em Pendências (o aviso diário já saiu de manhã).

## 6. No resumo da rotina

Em Pendências ou na parte própria da rotina, uma linha: "Raspagem: N créditos do Firecrawl nesta rodada (conta X; saldo somado S; próxima renovação DD/MM)". O comando `uso` mostra os créditos por conta. Nunca as chaves.

## 7. Datafé sob demanda

Quando Mário pedir trabalho de dados do Datafé (projeto do portal e banco no Lovable, docs no projeto "Evangelicos em numeros 2026"):

1. **Selo de fé dos eleitos** (fase 8b): `search` pelo nome + "evangélico", "pastor", "igreja" ou a denominação, e `scrape` da fonte achada. Regra da fase 8b: selo só com pesquisa Iser/Pública, declaração do próprio, fonte oficial ou duas reportagens; igreja só com fonte forte ou duas reportagens que a nomeiem; uma reportagem só fica pendente; Wikipédia nunca aprova. Cada evidência sai com URL, trecho, tipo de fonte e data, para o painel de revisão.
2. **Pesquisas novas com religião** (termômetro do /projecoes e /pesquisas): `search` dos últimos 30 dias por instituto ("Quaest religião evangélicos", "Datafolha evangélicos") e `scrape` do relatório (PDF conta 1 crédito por página). Só entra pesquisa que publica a fatia de evangélicos da amostra, pela regra do doc "pesquisas-religiao".
3. **Ler o datafe.com.br:** as páginas são feitas em JavaScript, e o WebFetch só mostra o cabeçalho. Para conferir o que a página mostra, `scrape`.

## 8. Código do script (`raspar.py`)

```python
#!/usr/bin/env python3
"""Raspagem da Next: só Firecrawl, com várias contas usadas em ordem (skill raspagem-web-next).

python3 raspar.py creditos
python3 raspar.py teto 8                       # teto de créditos desta execução
python3 raspar.py search "consulta" [--limite 5] [--dias 7] [--conteudo]
python3 raspar.py scrape URL [--links] [--max 12000]
python3 raspar.py map URL [--busca termo] [--limite 50]
python3 raspar.py uso                          # créditos gastos nesta execução
python3 raspar.py importar ARQUIVO             # tira as chaves do texto da memória e grava raspagem_chaves.json

Lê as chaves de raspagem_chaves.json (pasta atual): {"firecrawl": ["fc-...", "fc-...", "fc-..."]}.
As contas são usadas na ordem: quando uma acaba (HTTP 402), a seguinte assume; quando todas acabam, a raspagem para.
Saída sempre em JSON. O campo "aviso" aparece quando uma conta acabou ou a raspagem parou.
"""
import json, math, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse

CHAVES = Path("raspagem_chaves.json")
USO = Path("raspagem_uso.json")
FC = "https://api.firecrawl.dev/v2"
BAIXO_FC = 0.20      # saldo somado das contas em 20% do plano somado, ou menos = baixo

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
PARADA = "Raspagem parada: as contas do Firecrawl estão sem créditos. Compre créditos ou mande outra chave."


def saida(obj, codigo=0):
    print(json.dumps(obj, ensure_ascii=False, indent=1)); sys.exit(codigo)


def chaves():
    if not CHAVES.exists():
        saida({"erro": "raspagem_chaves.json não existe: rode o passo da seção 1 da skill raspagem-web-next (importar da memória)"}, 2)
    c = json.loads(CHAVES.read_text())
    return [k for k in c.get("firecrawl", []) if k and "COLE" not in k]


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
    return json.loads(USO.read_text()) if USO.exists() else {"firecrawl": 0, "por_conta": {}, "teto": None}


def gastar(n, conta):
    u = uso()
    u["firecrawl"] += n
    u.setdefault("por_conta", {})[str(conta)] = u.get("por_conta", {}).get(str(conta), 0) + n
    USO.write_text(json.dumps(u))


def checar_teto(previsto):
    u = uso()
    if u.get("teto") is not None and u["firecrawl"] + previsto > u["teto"]:
        saida({"erro": f"teto da execução atingido ({u['firecrawl']} de {u['teto']} créditos): siga com WebFetch e WebSearch"}, 3)


def via_firecrawl(caminho, corpo, previsto):
    """Tenta as contas em ordem: 402 (sem créditos) ou 401/403 (chave recusada) passa para a seguinte.
    Todas fora: a raspagem para (código 4)."""
    checar_teto(previsto)
    fcs = chaves()
    if not fcs:
        saida({"aviso": "sem_chave", "erro": "Raspagem: chaves não salvas na memória. Siga com WebFetch e WebSearch."}, 4)
    puladas = []
    for i, k in enumerate(fcs):
        cod, dado = http("POST", f"{FC}/{caminho}", k, corpo)
        if cod == 402:
            puladas.append(f"conta {i + 1} sem créditos"); continue
        if cod in (401, 403):
            puladas.append(f"conta {i + 1} com chave recusada (HTTP {cod})"); continue
        av = (", ".join(puladas) + f": usando a conta {i + 1}") if puladas else None
        if 200 <= cod < 300:
            gastar(dado.get("creditsUsed", previsto) if isinstance(dado, dict) else previsto, i + 1)
            return {"provedor": "firecrawl", "conta": i + 1, "aviso": av, "dado": dado}
        saida({"provedor": "firecrawl", "conta": i + 1, "aviso": av, "erro": f"HTTP {cod}", "dado": dado}, 1)
    saida({"aviso": "raspagem_parada", "contas": puladas, "erro": PARADA + " Siga com WebFetch e WebSearch e avise o Mário."}, 4)


# ---------------- comandos ----------------
def cmd_creditos():
    fcs = chaves()
    out = {"firecrawl": [], "aviso": "ok"}
    if not fcs:
        out["aviso"] = "sem_chave"; saida(out)
    for i, k in enumerate(fcs):
        cod, d = http("GET", f"{FC}/team/credit-usage", k)
        dd = d.get("data", {}) if isinstance(d, dict) else {}
        rest, plano = dd.get("remainingCredits"), dd.get("planCredits")
        est = ("erro" if cod != 200 else "esgotado" if (rest or 0) <= 0 else
               "baixo" if plano and rest <= max(BAIXO_FC * plano, 1) else "ok")
        out["firecrawl"].append({"conta": i + 1, "restantes": rest, "plano": plano,
                                 "renova_em": dd.get("billingPeriodEnd"), "estado": est,
                                 **({"http": cod} if cod != 200 else {})})
    contas = out["firecrawl"]
    usaveis = [c for c in contas if c["estado"] in ("ok", "baixo")]
    total_rest = sum(c["restantes"] or 0 for c in usaveis)
    total_plano = sum(c["plano"] or 0 for c in contas if c["estado"] != "erro")
    out["total_restantes"] = total_rest
    out["conta_em_uso"] = usaveis[0]["conta"] if usaveis else None
    renov = sorted(str(c["renova_em"]) for c in contas if c.get("renova_em"))
    out["proxima_renovacao"] = renov[0] if renov else None
    avisos = []
    if not usaveis:
        avisos.append("firecrawl_esgotado" if all(c["estado"] == "esgotado" for c in contas) else "firecrawl_erro")
    elif total_plano and total_rest <= BAIXO_FC * total_plano:
        avisos.append("firecrawl_baixo")
    if usaveis and any(c["estado"] == "erro" for c in contas):
        avisos.append("conta_com_erro")
    if usaveis and usaveis[0]["conta"] > 1:
        avisos.append(f"conta_{usaveis[0]['conta']}_em_uso")
    out["aviso"] = ";".join(avisos) or "ok"
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
    r = via_firecrawl("search", corpo, previsto)
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


def cmd_scrape(url):
    if bloqueado(url):
        saida({"erro": f"{url} está na lista de sites que não se raspam (bloqueio de leitura automática ou rede social)."}, 5)
    links = arg("--links", False, bool); maxc = arg("--max", 12000, int)
    corpo = {"url": url, "formats": ["markdown"] + (["links"] if links else []), "onlyMainContent": True, "waitFor": 1500}
    r = via_firecrawl("scrape", corpo, 1)
    d = r.pop("dado").get("data", {})
    md = d.get("markdown") or ""
    meta = d.get("metadata", {})
    r.update({"url": meta.get("sourceURL") or url, "titulo": meta.get("title"), "status": meta.get("statusCode"),
              "markdown": md[:maxc], "cortado": len(md) > maxc, "links": d.get("links") if links else None})
    saida(r)


def cmd_map(url):
    if bloqueado(url):
        saida({"erro": f"{url} está na lista de sites que não se raspam."}, 5)
    busca = arg("--busca", None); n = arg("--limite", 50, int)
    corpo = {"url": url, "limit": n}
    if busca:
        corpo["search"] = busca
    r = via_firecrawl("map", corpo, 1)
    d = r.pop("dado")
    ls = d.get("links") or d.get("data", {}).get("links") or []
    r["links"] = [(l if isinstance(l, dict) else {"url": l}) for l in ls if not bloqueado(l if isinstance(l, str) else l.get("url"))]
    saida(r)


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
        CHAVES.write_text(json.dumps({"firecrawl": fcs})); p.unlink()
        saida({"firecrawl_contas": len(fcs), "aviso": "ok" if fcs else "sem_chave_firecrawl_na_memoria"})
    elif c == "search":
        cmd_search(sys.argv[2])
    elif c == "scrape":
        cmd_scrape(sys.argv[2])
    elif c == "map":
        cmd_map(sys.argv[2])
    else:
        saida({"erro": "comando desconhecido", "uso": __doc__}, 2)
```
