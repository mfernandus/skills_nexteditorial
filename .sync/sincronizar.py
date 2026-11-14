#!/usr/bin/env python3
"""Sincroniza as skills próprias da conta Claude de Mário Fernando com os dois repositórios:
mfernandus/skills_nexteditorial (skills da Next) e mfernandus/skills-mario-pessoal (pessoais e de terceiros).

Uso: python3 -I sincronizar.py --next <clone> --pessoal <clone> [--skills <pasta synced>] [--dry-run]

Regras:
- Fonte: ~/.claude/skills/synced/*/manifest.json, só skills próprias (origem que não começa com "anthropic").
  As skills de apoio da Anthropic em anthropic/ não são tocadas.
- Cada skill fica onde já está no repositório (a pasta é achada pelo nome). Skill nova sem pasta só entra
  depois que alguém grava a pasta dela em .sync/mapa.json do repositório da Next
  ("nome": "next:01 Editorial/01 Rotinas de notícias" ou "pessoal:pessoais"); até lá aparece em "sem_pasta".
- Pega tudo o que mudou desde a última sincronização (.sync/estado.json de cada repositório), não importa
  há quanto tempo, em ordem cronológica, um commit por skill com a data e a hora reais da alteração na conta.
- Antes de gravar, confere se a cópia do repositório foi mexida fora da sincronização (direto no GitHub ou no
  Mac). Se a mexida for mais nova que a versão da conta, não sobrescreve e avisa; se for mais antiga, a versão
  da conta entra e o aviso registra o que foi substituído.
- Arquivos que só existem no repositório (CONEXOES.md, kits, LEIA-ME.txt) são preservados.
- Varre chaves, tokens e senhas antes de gravar: com achado, a skill não sobe (os repositórios são públicos).
- Skill apagada da conta: na Next vai para "99 Arquivadas"; no pessoal só gera alerta. Trava contra sumiço em massa.
- Atualiza a descrição da skill no LEIA-ME.md da Next e acrescenta as novas na seção da pasta.
Não faz push. Imprime um resumo em JSON.
"""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")
AUTOR = ("Mário Fernando", "mfernandus@users.noreply.github.com")
IGNORAR = {".DS_Store", "__pycache__", "Thumbs.db"}
LIMITE_ARQUIVO = 50 * 1024 * 1024
ARQUIVADAS = "99 Arquivadas"

SEGREDOS = [
    ("token do GitHub", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}"),
    ("chave da Anthropic", r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("chave de API (sk-)", r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}"),
    ("chave da AWS", r"\bAKIA[0-9A-Z]{16}\b"),
    ("token da Meta/WhatsApp", r"\bEAA[A-Za-z0-9]{60,}"),
    ("token do Slack", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("chave privada", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("token JWT", r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}"),
    ("chave do Google", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("senha ou chave escrita no texto",
     r"(?i)\b(?:senha|password|passwd|secret|api[_-]?key|access[_-]?token|bearer)\b[\"'\s]*[:=][\"'\s]*"
     r"(?!os\.environ|process\.env|\$|\{\{|<|\[|getenv|None|null|\"\"|''|xxx|\*\*\*)[A-Za-z0-9_\-\.\/+=]{20,}"),
]
DATA_URI = re.compile(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=\s]+")


def git(repo, *args, env=None, check=True):
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(["git", "-C", repo, "-c", f"user.name={AUTOR[0]}", "-c", f"user.email={AUTOR[1]}",
                        "-c", "core.quotepath=off", *args], capture_output=True, text=True, env=e)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def ler_json(caminho, padrao):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao


def gravar_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def arquivos(pasta):
    saida = []
    for raiz, dirs, fs in os.walk(pasta):
        dirs[:] = sorted(d for d in dirs if d not in IGNORAR and d != ".git")
        for f in sorted(fs):
            if f not in IGNORAR:
                saida.append(os.path.relpath(os.path.join(raiz, f), pasta))
    return saida


def digital(pasta, lista=None):
    h = hashlib.sha256()
    for rel in (lista if lista is not None else arquivos(pasta)):
        caminho = os.path.join(pasta, rel)
        h.update(rel.encode())
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                h.update(hashlib.sha256(f.read()).digest())
        else:
            h.update(b"<ausente>")
    return h.hexdigest()


def varrer_segredos(pasta):
    achados = []
    for rel in arquivos(pasta):
        caminho = os.path.join(pasta, rel)
        if os.path.getsize(caminho) > LIMITE_ARQUIVO:
            achados.append(f"{rel}: arquivo acima de 50 MB")
            continue
        with open(caminho, "rb") as f:
            dados = f.read()
        if b"\x00" in dados[:8192]:
            continue
        try:
            texto = dados.decode("utf-8")
        except UnicodeDecodeError:
            texto = dados.decode("latin-1")
        texto = DATA_URI.sub("", texto)
        for nome, padrao in SEGREDOS:
            m = re.search(padrao, texto)
            if m:
                achados.append(f"{rel}, linha {texto.count(chr(10), 0, m.start()) + 1}: {nome}")
    return achados


def localizar(repo):
    loc = {}
    for raiz, dirs, fs in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", ".sync")]
        rel = os.path.relpath(raiz, repo)
        if rel.split(os.sep)[0] == "anthropic":
            dirs[:] = []
            continue
        if "SKILL.md" in fs:
            loc[os.path.basename(raiz)] = rel
            dirs[:] = []
    return loc


def quando(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(TZ)
    return d, d.strftime("%d/%m/%Y %H:%M")


def ultima_mexida(repo, rel):
    r = git(repo, "log", "-1", "--format=%cI", "--", rel, check=False)
    s = r.stdout.strip()
    return datetime.fromisoformat(s).astimezone(TZ) if s else None


def negrito_marcas(texto):
    texto = re.sub(r"(?<!\*)\b([Rr]evista ES Brasil)(?!\*)", r"**\1**", texto)
    texto = re.sub(r"(?<!\*)(?<![Rr]evista )\bES Brasil\b(?!\*)", "**ES Brasil**", texto)
    texto = re.sub(r"(?<!\*)\bCafé com Moqueca\b(?!\*)", "**Café com Moqueca**", texto)
    return texto


def atualizar_leia_me(repo, pasta_rel, nome, descricao, avisos):
    caminho = os.path.join(repo, "LEIA-ME.md")
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    desc = negrito_marcas(" ".join(descricao.split()))
    linha = f"- **{nome}** — {desc}"
    padrao = re.compile(rf"^- \*\*{re.escape(nome)}\*\* — (.*)$", re.M)
    achado = padrao.search(texto)
    if achado:
        limpo = lambda t: re.sub(r"[*\\]", "", t).lower()
        if limpo(achado.group(1)) == limpo(desc):
            return
        novo = texto[:achado.start()] + linha + texto[achado.end():]
    else:
        secao = pasta_rel.replace(os.sep, "/")
        partes = secao.split("/")
        titulo = "## " + " / ".join(partes[:2]) if partes[0].startswith("01 ") and len(partes) > 1 else "## " + partes[0]
        idx = texto.find(titulo + "\n")
        if idx == -1:
            obs = texto.find("## Observações")
            bloco = f"{titulo}\n\n{linha}\n\n"
            novo = texto[:obs] + bloco + texto[obs:] if obs != -1 else texto.rstrip() + "\n\n" + bloco
        else:
            fim = texto.find("\n## ", idx + len(titulo))
            fim = len(texto) if fim == -1 else fim
            corpo = texto[idx:fim].rstrip("\n")
            novo = texto[:idx] + corpo + "\n" + linha + "\n" + texto[fim:]
        avisos.append(f"{nome} entrou no LEIA-ME em {titulo[3:]}; o MAPA-DE-CONEXOES.md ainda não tem as ligações dela")
    if novo != texto:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(novo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--next", required=True)
    ap.add_argument("--pessoal", required=True)
    ap.add_argument("--skills", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    repos = {"next": os.path.abspath(a.next), "pessoal": os.path.abspath(a.pessoal)}
    trailer = os.environ.get("SYNC_TRAILER", "").strip()

    origem = a.skills or next(iter(sorted(glob.glob(os.path.expanduser("~/.claude/skills/synced/*/")))), None)
    if not origem or not os.path.exists(os.path.join(origem, "manifest.json")):
        print(json.dumps({"erro": "pasta das skills da conta não encontrada (~/.claude/skills/synced/*/manifest.json)"}, ensure_ascii=False))
        sys.exit(2)
    manifest = ler_json(os.path.join(origem, "manifest.json"), {})
    skills = [s for s in manifest.get("skills", []) if not str(s.get("source", "")).startswith("anthropic")
              and os.path.exists(os.path.join(origem, s["name"], "SKILL.md"))]
    skills.sort(key=lambda s: (s["updatedAt"], s["name"]))

    estados = {k: ler_json(os.path.join(r, ".sync/estado.json"), {}) for k, r in repos.items()}
    mapa_p = os.path.join(repos["next"], ".sync/mapa.json")
    mapa = ler_json(mapa_p, {})
    locais = {}
    for k, r in repos.items():
        for nome, rel in localizar(r).items():
            locais[nome] = (k, rel)
    resumo = {"commits": {"next": [], "pessoal": []}, "alertas": [], "avisos": [], "sem_pasta": [],
              "arquivadas": [], "sem_mudanca": 0}

    def commit(k, msg, data=None):
        repo = repos[k]
        if git(repo, "diff", "--cached", "--quiet", check=False).returncode == 0:
            return
        env = None
        if data:
            d = data.strftime("%Y-%m-%dT%H:%M:%S%z")
            env = {"GIT_AUTHOR_DATE": d, "GIT_COMMITTER_DATE": d}
        if not a.dry_run:
            git(repo, "commit", "-q", "-m", msg + (f"\n\n{trailer}" if trailer else ""), env=env)
        resumo["commits"][k].append(msg)

    for s in skills:
        nome = s["name"]
        src = os.path.join(origem, nome)
        if nome in locais:
            k, rel = locais[nome]
        elif nome in mapa and ":" in mapa[nome]:
            k, pasta = mapa[nome].split(":", 1)
            if k not in repos:
                resumo["alertas"].append({"skill": nome, "motivo": f"repositório desconhecido em .sync/mapa.json: {mapa[nome]}"})
                continue
            rel = os.path.join(pasta, nome)
        else:
            resumo["sem_pasta"].append({"skill": nome, "descricao": s["description"]})
            continue
        repo = repos[k]
        estado = estados[k]
        destino = os.path.join(repo, rel)
        conta_lista = arquivos(src)
        conta_dig = digital(src, conta_lista)
        ant = estado.get(nome)
        data_conta, hora_conta = quando(s["updatedAt"])

        if ant and ant.get("sha") == conta_dig:
            ant.setdefault("pasta", rel)
            resumo["sem_mudanca"] += 1
            continue
        if not ant and os.path.isdir(destino) and digital(destino, conta_lista) == conta_dig:
            estado[nome] = {"sha": conta_dig, "arquivos": conta_lista, "updatedAt": s["updatedAt"], "pasta": rel}
            resumo["sem_mudanca"] += 1
            continue

        # a cópia do repositório foi mexida fora da sincronização?
        if os.path.isdir(destino):
            base = ant["arquivos"] if ant else conta_lista
            repo_dig = digital(destino, base)
            mexida_fora = (ant and repo_dig != ant.get("sha")) or (not ant)
            if mexida_fora:
                quando_repo = ultima_mexida(repo, rel)
                if quando_repo and quando_repo > data_conta:
                    resumo["alertas"].append({"skill": nome, "motivo": (
                        f"a cópia do repositório ({k}) foi alterada em {quando_repo.strftime('%d/%m/%Y %H:%M')}, depois da "
                        f"versão salva na conta ({hora_conta}); não sobrescrevi. Salve a versão certa na conta ou confirme a troca")})
                    continue
                if quando_repo:
                    resumo["avisos"].append(
                        f"{nome}: a cópia do repositório tinha alteração de {quando_repo.strftime('%d/%m/%Y %H:%M')}, anterior à "
                        f"versão da conta ({hora_conta}); a da conta entrou")

        achados = varrer_segredos(src)
        if achados:
            resumo["alertas"].append({"skill": nome, "motivo": "possível segredo ou arquivo grande; não subiu", "onde": achados[:5]})
            continue
        if a.dry_run:
            resumo["commits"][k].append(f"{'adiciona' if not os.path.isdir(destino) else 'atualiza'} {nome}")
            continue

        nova = not os.path.isdir(destino)
        os.makedirs(destino, exist_ok=True)
        for velho in (ant or {}).get("arquivos", []):
            if velho not in conta_lista and os.path.exists(os.path.join(destino, velho)):
                os.remove(os.path.join(destino, velho))
        for rel_arq in conta_lista:
            alvo = os.path.join(destino, rel_arq)
            os.makedirs(os.path.dirname(alvo), exist_ok=True)
            shutil.copy2(os.path.join(src, rel_arq), alvo)
        estado[nome] = {"sha": conta_dig, "arquivos": conta_lista, "updatedAt": s["updatedAt"], "pasta": rel}
        gravar_json(os.path.join(repo, ".sync/estado.json"), estado)
        if k == "next":
            atualizar_leia_me(repo, os.path.dirname(rel), nome, s["description"], resumo["avisos"])
        elif nova:
            resumo["avisos"].append(f"{nome} entrou no repositório pessoal em {os.path.dirname(rel)}/; acrescente no README.md")
        git(repo, "add", "-A", "--", rel, ".sync/estado.json", *(["LEIA-ME.md"] if k == "next" else []))
        commit(k, f"{'adiciona' if nova else 'atualiza'} {nome} ({hora_conta}, horário de Brasília)", data_conta)

    # skills apagadas da conta
    na_conta = {s["name"] for s in skills}
    for k, repo in repos.items():
        estado = estados[k]
        sumidas = [n for n in estado if n not in na_conta]
        if not sumidas:
            continue
        if len(sumidas) > 3 or len(na_conta) < 0.8 * sum(len(e) for e in estados.values()):
            resumo["alertas"].append({"skill": ", ".join(sorted(sumidas)),
                                      "motivo": "sumiram da conta várias skills de uma vez; nada foi mexido no repositório por segurança"})
            continue
        for n in sorted(sumidas):
            if k == "pessoal":
                resumo["alertas"].append({"skill": n, "motivo": "apagada da conta; continua no repositório pessoal até você decidir"})
                continue
            rel = estado[n].get("pasta") or locais.get(n, (None, None))[1]
            if a.dry_run or not rel or rel.split(os.sep)[0] == ARQUIVADAS:
                continue
            novo_rel = os.path.join(ARQUIVADAS, n)
            git(repo, "mv", rel, novo_rel)
            estado[n]["pasta"] = novo_rel
            gravar_json(os.path.join(repo, ".sync/estado.json"), estado)
            git(repo, "add", "-A", "--", ".sync/estado.json")
            commit(k, f"arquiva {n} (apagada da conta do Claude)")
            resumo["arquivadas"].append(n)
            resumo["avisos"].append(f"{n} foi para {ARQUIVADAS}; mova a linha dela no LEIA-ME.md")

    if not a.dry_run:
        for k, repo in repos.items():
            gravar_json(os.path.join(repo, ".sync/estado.json"), estados[k])
            git(repo, "add", "--", ".sync/estado.json")
            commit(k, "registra o estado da sincronização das skills")
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
