---
name: "atualizacao-cnpj-templos"
description: "Atualização mensal dos CNPJs de organizações religiosas do Datafé (datafe.com.br): baixa a base da Receita, classifica, carrega pela função templos-ingest e confere os números."
---

# Atualização mensal dos CNPJs de templos (Datafé)

Atualiza a tabela `templos` (origem `cnpj`) do portal Datafé com a base de CNPJ mais nova da Receita Federal: organizações religiosas, natureza jurídica 3220. Depois da carga, a matéria mensal sai pela skill `materia-igrejas-abertas-comunhao`.

## Onde estão as coisas

- **Portal:** https://datafe.com.br. É o projeto Lovable `bd496ff6-6711-470b-aef0-fc1c2b6a611e` (consultas SQL com `query_database` do conector Lovable).
- **Supabase:** https://mvxzozxjzbrzndaunlxj.supabase.co. A leitura pública usa a chave publicável que já está no script.
- **Função de carga:** `templos-ingest` (POST com `{token, acao, origem, rows}`; `acao` = `validar` | `upsert` | `refresh` | `apagar_origem`; até 5.000 linhas por chamada).
  - O token é conferido pelo hash SHA-256 na tabela `ingest_tokens` (colunas `id`, `token_hash`, `escopo`, `criado_em`, `expira_em`).
  - `refresh` roda `refresh_templos_views()`, que atualiza as views `mv_templos_municipio`, `mv_cnpj_aberturas_mes`, `mv_cnpj_baixas_mes`, `mv_templos_base`, `templos_cnpj_resumo` e `templos_cnpj_leituras`.
- **Receita Federal:** compartilhamento WebDAV `https://arquivos.receitafederal.gov.br/public.php/webdav/Dados/Cadastros/CNPJ/`, com uma pasta por mês (`AAAA-MM`).
  - Cada pasta tem Empresas0–9 (cerca de 1,3 GB) e Estabelecimentos0–9 (cerca de 5,2 GB).
  - O servidor entrega perto de 1 MB/s por conexão; o script usa 4 conexões e retoma downloads interrompidos.
  - Os CSV vêm em latin-1, separados por `;`.
- **Municípios:** o código SIAFI da Receita vira código IBGE pela tabela kelvins/municipios-brasileiros, que o script baixa sozinho.
- **Base de referência:** a carga de 11/11/2026 usou a base 2026-10, com 209.864 linhas no total.
  - 121.825 CNPJs evangélicos ativos.
  - Em 2025: 6.525 aberturas e 816 baixas.

## Regras que não mudam

- **Classificação:** CNPJ que já está no banco com a mesma razão social e o mesmo nome mantém religião, denominação e regra. Só CNPJ novo ou que mudou de nome passa pelo `classificador.py`. Isso deixa as séries estáveis de um mês para o outro. O classificador concorda com a carga de referência em 98,9% das linhas.
- **Token:**
  - Nunca imprima o token, nunca o coloque na linha de comando nem em mensagem ou relatório.
  - Ele fica num arquivo com permissão 600 e entra no script pela variável de ambiente `CARGA_TOKEN`.
  - O token vale 6 horas e é apagado no fim, tanto a linha do banco quanto o arquivo.
- **Linhas que sumiram da base:** só são apagadas se forem até 1% da base anterior. Acima disso, pare e avise o Mário.
- **Sem base nova:** se `verificar` disser que não há base nova, encerre sem tocar em nada e diga isso em uma linha.
- **Recusa:** se qualquer etapa de gravação for recusada (permissão, conector, classificador de segurança), não procure outro caminho. Pare, deixe os arquivos preparados e diga ao Mário o que falta.

## Passo a passo

### 1. Preparar a pasta de trabalho

Crie a pasta `~/cnpj-templos` e grave nela os três arquivos do fim desta skill, exatamente como estão: `classificador.py`, `atualiza_cnpj.py` e `valida_local.py`. Confira o espaço em disco com `df -h ~`; o download precisa de 7 GB livres.

### 2. Verificar se há base nova

```bash
cd ~/cnpj-templos && python3 atualiza_cnpj.py verificar
```

- **Código de saída 3:** não há base nova. Encerre.
- **Código de saída 0:** anote `mais_nova_na_receita` (o `MES` a carregar) e `carregada` (o mês anterior).

### 3. Baixar e preparar (40 a 90 minutos)

Rode em segundo plano, com log, e acompanhe:

```bash
cd ~/cnpj-templos && nohup python3 atualiza_cnpj.py preparar --mes MES > preparar_MES.log 2>&1 &
```

Acompanhe o log com `sleep` de alguns minutos e `tail -5 preparar_MES.log`.

- Se cair (rede), rode de novo o mesmo comando: os downloads retomam de onde pararam.
- Se a pasta do mês ainda estiver incompleta (menos de 10 Empresas ou 10 Estabelecimentos), encerre e avise. A Receita costuma completar a pasta em poucos dias.

### 4. Conferir o resumo

Leia `dados/resumo_MES.json` e compare com o mês anterior (consulta no banco ou o relatório anterior):

| Campo | Faixa aceitável | O que significa |
|---|---|---|
| `linhas` | até ±3% da base anterior | total de CNPJs de organizações religiosas |
| `evangelicos_ativos` | até ±3% | evangélicos com situação ativa |
| `sem_municipio` | algumas dezenas, no máximo | estabelecimentos sem código de município válido (ficam de fora) |
| `pct_sumiram` | até 1 | percentual de CNPJs do banco que não vieram na base nova |
| `classificados_agora` | poucos milhares | CNPJs novos ou renomeados que passaram pelo classificador |

Qualquer número fora da faixa: pare e mostre ao Mário antes de carregar.

### 5. Validar localmente

```bash
python3 valida_local.py dados/cnpj_MES.jsonl
```

Precisa sair com `"erros": 0`. As regras são as mesmas da função `templos-ingest`.

### 6. Criar o token de carga

1. Gere o token sem mostrá-lo e grave só o hash num arquivo à parte:

   ```bash
   cd ~/cnpj-templos && umask 077 && python3 -c "import secrets,hashlib;t=secrets.token_urlsafe(48);open('.carga_token','w').write(t);open('.carga_hash','w').write(hashlib.sha256(t.encode()).hexdigest())" && cat .carga_hash
   ```

2. Insira o hash (só o hash, nunca o token) com `query_database` do Lovable no projeto `bd496ff6-6711-470b-aef0-fc1c2b6a611e`:

   ```sql
   insert into ingest_tokens (id, token_hash, escopo, expira_em)
   select coalesce(max(id), 0) + 1, 'HASH', 'templos', now() + interval '6 hours' from ingest_tokens
   returning id, expira_em;
   ```

3. Anote o `id` devolvido.

Se a inserção for recusada, não tente de outra forma:

- Apague `.carga_token` e `.carga_hash`.
- Mande ao Mário o resumo do passo 4 e diga que a base está pronta, faltando só a autorização da carga.
- Encerre.

### 7. Carregar

```bash
cd ~/cnpj-templos && CARGA_TOKEN="$(cat .carga_token)" python3 atualiza_cnpj.py carregar --mes MES
```

O script valida todos os lotes antes de gravar qualquer um, grava em lotes de 5.000 (upsert por origem e identificador) e roda o `refresh` no fim.

### 8. Apagar as linhas que sumiram (só se `pct_sumiram` ≤ 1)

Se `dados/apagar_MES.txt` não estiver vazio:

1. Apague essas linhas em blocos de até 1.000 identificadores com `query_database`:

   ```sql
   delete from templos where origem = 'cnpj' and identificador = any (array['ID1','ID2', ...]);
   ```

2. Depois, atualize os resumos:

   ```bash
   CARGA_TOKEN="$(cat .carga_token)" python3 atualiza_cnpj.py refresh
   ```

### 9. Limpar

1. Apague o token do banco com `query_database`:

   ```sql
   delete from ingest_tokens where id = ID_DO_PASSO_6;
   ```

2. Apague os arquivos locais:

   ```bash
   rm -f .carga_token .carga_hash
   rm -rf zips
   ```

### 10. Conferir no banco e relatar

Rode com `query_database`:

```sql
select referencia, count(*) from templos where origem = 'cnpj' group by 1;   -- só deve aparecer "CNPJ Receita Federal MES"
select religiao, situacao, count(*) from templos where origem = 'cnpj' group by 1, 2 order by 3 desc;
select * from templos_cnpj_resumo;
select * from mv_cnpj_aberturas_mes order by 1 desc limit 6;
select * from mv_cnpj_baixas_mes order by 1 desc limit 6;
```

Abra também a página de igrejas abertas em https://datafe.com.br e confira se os números novos aparecem.

O relatório para o Mário deve ser curto e em português:

- a base carregada;
- as linhas gravadas;
- os evangélicos ativos, comparados com o mês anterior;
- as aberturas e baixas dos últimos meses;
- quantos CNPJs foram classificados agora;
- quantos sumiram e foram apagados;
- qualquer alerta.

Grave também um resumo no doc do projeto `claude/fase2-templos.md`, na seção de atualizações mensais.

### 11. Matéria

Com a carga conferida, siga para a skill `materia-igrejas-abertas-comunhao`.

## Arquivos

### classificador.py

```python
"""Classificador de religião e denominação pelo nome (razão social + nome fantasia).

Regras em ordem; a primeira que casa decide. Texto normalizado: sem acento, maiúsculas,
pontuação vira espaço. Reconstruído em 13/11/2026 a partir das 209.864 classificações da
carga de 11/11/2026 (base CNPJ 2026-10).
"""
import re, unicodedata

def normalizar(s):
    s = unicodedata.normalize('NFD', s or '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper()
    s = re.sub(r'[^A-Z0-9]+', ' ', s)
    return ' ' + re.sub(r'\s+', ' ', s).strip() + ' '

# (regra, religiao, denominacao_slug, padrão)
REGRAS = [
    # 1. exceções católicas
    ('catolica_joao_batista', 'catolica', None, r' (SAO|S|SANTO) JOAO BATISTA '),
    ('catolica_medalha', 'catolica', None, r' MEDALHA MILAGROSA '),
    # 2. outras religiões
    ('icab', 'outras', None, r' CATOLICA APOSTOLICA BRASILEIRA | ICAB '),
    ('sud', 'outras', None, r' SANTOS DOS ULTIMOS DIAS | MORMON'),
    ('jeova', 'outras', None, r' TESTEMUNHAS DE JEOVA | SALAO DO REINO | MACONIC| VALE DO AMANHECER '),
    ('seicho', 'outras', None, r' SEICHO | MESSIANICAS? | ESTUDANTES DA BIBLIA | PERFECT LIBERTY | SGI | SOKA GAKKAI | RELIGIAO DE DEUS | LEGIAO DA BOA VONTADE | LBV | MAHIKARI | TENRIKYO | OOMOTO '),
    ('rosacruz', 'outras', None, r' ROSACRUZ| ROSA CRUZ | AMORC | GNOSTIC| RACIONALISMO CRISTAO | TEOSOF| EUBIOSE | LECTORIUM | ESOTERIC'),
    ('daime', 'outras', None, r' DAIME | UNIAO DO VEGETAL | UDV | BARQUINHA | AYAHUASCA | CEFLURIS | ICEFLU'),
    ('ortodoxa', 'outras', None, r' ORTODOX'),
    ('krishna', 'outras', None, r' KRISHNA| KRSNA| ISKCON | BRAHMA KUMARIS | RAMAKRISHNA | VEDANTA | HARE KRISHNA '),
    ('budista', 'outras', None, r' BUDIS| BUDDH| BUDA | ZEN | HONGWANJI | KADAMPA | DHARMA | NICHIREN | TIBET| GONPA | SANGHA '),
    ('islamica', 'outras', None, r' ISLAM| MUCULMAN| MESQUITA | MUSULMAN'),
    ('judaica', 'outras', None, r' ISRAELITA | JUDAIC| SINAGOGA | BEIT | BETH | CHABAD | JUDEU| JUDAISMO '),
    # 3. matriz africana
    ('afro', 'matriz_africana', None, r' UMBANDA | CANDOMBL| ORIXA| ORISA| TERREIRO | CABOCLO | IEMANJA | YEMANJA | OXALA | OGUM | OGUN | OXOSSI | XANGO | ILE | AXE | ASE | QUIMBAND| MATRIZ(ES)? AFRICANA| AFRO BRASILEIR| PRETO VELHO | PAI JOAO | JUREMA | BATUQUE | BABALORIXA | IALORIXA | EGBE | ABASSA '),
    # 4. espírita
    ('espirita', 'espirita', None, r' ESPIRITAS? | ESPIRITISM| KARDEC| ESPIRITUALISTA | CASA DO CAMINHO | ESPIRITUALISTAS | CENTRO REDENTOR '),
    # 5. denominações evangélicas
    ('iurd', 'evangelica', 'universal-do-reino-de-deus', r' UNIVERSAL DO REINO DE DEUS | IURD | IGREJA UNIVERSAL '),
    ('ccb', 'evangelica', 'congregacao-crista-do-brasil', r' CONGREGACAO CRISTA (NO|DO) BRASIL '),
    ('ieq', 'evangelica', 'evangelho-quadrangular', r' QUADRANGULAR '),
    ('mundial', 'evangelica', 'mundial-do-poder-de-deus', r' MUNDIAL DO PODER | IGREJA MUNDIAL '),
    ('graca', 'evangelica', 'internacional-da-graca', r' INTERNACIONAL DA GRACA | IGREJA DA GRACA '),
    ('sara', 'evangelica', 'sara-nossa-terra', r' SARA NOSSA TERRA | S NOSSA TERRA '),
    ('bpc', 'evangelica', 'o-brasil-para-cristo', r' BRASIL PARA CRISTO | OBPC '),
    ('dea', 'evangelica', 'deus-e-amor', r' DEUS E AMOR | IPDA '),
    ('boladeneve', 'evangelica', 'bola-de-neve', r' BOLA DE NEVE '),
    ('renascer', 'evangelica', 'renascer-em-cristo', r' RENASCER EM CRISTO '),
    ('casabencao', 'evangelica', 'casa-da-bencao', r' CASA DA BENCAO | TABERNACULO EVANGELICO DE JESUS '),
    ('adventista', 'evangelica', 'adventista', r' ADVENTISTA'),
    ('luterana', 'evangelica', 'luterana', r' LUTERAN| IECLB | IELB '),
    ('metodista', 'evangelica', 'metodista', r' METODIST| WESLEYAN'),
    ('presbiteriana', 'evangelica', 'presbiteriana', r' PRESBITER| PREBISTER| PRESBETER'),
    ('congregacional', 'evangelica', 'congregacional', r' CONGREGACIONA'),
    ('nazareno', 'evangelica', 'nazareno', r' NAZARENO '),
    ('anglicana', 'evangelica', 'anglicana', r' ANGLICAN| EPISCOPAL '),
    ('batista', 'evangelica', 'batista', r' BATISTA| BASTISTA'),
    ('ad', 'evangelica', 'assembleia-de-deus', r' AS+[EI]N?M?B?L?[EI]+I?AS? DE DEUS | ASSEMBLEIAS? | IEAD | ADVEC | AD | ASS DE DEUS '),
    ('maranata', 'evangelica', 'maranata', r' MARANATA '),
    ('novavida', 'evangelica', 'nova-vida', r' NOVA VIDA '),
    # 6. católica forte
    ('catolica', 'catolica', None, r' PAROQUIA | DIOCES| ARQUIDIOCES| MITRA | CATOLIC| FRANCISCAN| BENEDITIN| CARMELITA| JESUITA| SALESIAN| NOSSA SENHORA | N SRA | IRMAS | CONVENTO | MOSTEIRO | SEMINARIO | SANTUARIO | PADRE | PADRES | FREI | FREIS | CAPUCHINH| DOMINICAN| VICENTIN| SAGRADO CORACAO | CANCAO NOVA | CURIA | BASILICA | IRMANDADE | CONFRARIA | PASTORAL | IRMAZINHAS | MARIST| CLARISSAS | OBLATA| PALOTIN| REDENTORIST| SACRAMENTIN| PROVINCIA | PASSIONIST| RELIGIOSAS | OFICINAS DE ORACAO | BISPADO | PRELAZIA | ROSARIO | CATEDRAL | SAGRADA FAMILIA | DIVINO ESPIRITO SANTO | PAROQUIAL | CLERICAL | SCHOENSTATT | CAPELINHA | MAE RAINHA | RENOVACAO CARISMATICA '),
    # 7. pentecostal genérica
    ('pentecostal', 'evangelica', 'outras-pentecostais', r' PENTECOST| PENTENCOST| PETENCOST| PENTESCOST'),
    ('comunidadeevang', 'evangelica', 'comunidade-evangelica', r' COMUNIDADE EVANGELICA '),
    ('pentecostal', 'evangelica', 'outras-pentecostais', r' APOSTOLIC| AVIVAMENTO | IGREJA DE DEUS | DEUS E FIEL | PODER DE DEUS | GRACA DE DEUS | VIDA DE DEUS '),
    # 8. evangélica genérica
    ('evangelica', 'evangelica', None, r' EVANG | EVANGEL| MINISTERIO | CRISTA | MISSIONARI| CHURCH | EVANGELHO | RESTAURACAO | VIDEIRA | TABERNACULO | AGAPE | VERBO | UNCAO | CASA DE ORACAO | IGREJA DE CRISTO | IGREJA DA PAZ | JERUSALEM | PRIMITIVA | FILADELFIA | PAO DIARIO '),
    # 9. católica fraca
    ('catolica_fraca', 'catolica', None, r' CAPELA | SANTO | SANTA | SAO | SANTISSIM| CAPELANIA | IMACULAD| CARMELO | ORDEM TERCEIRA | CORACAO DE MARIA | N S DE '),
    # 10. evangélica fraca
    ('evangelica_fraca', 'evangelica', None, r' BIBLIC| MISSAO | ALIANCA | BOAS NOVAS | GRACA | PALAVRA | ADORACAO | MILAGRE| DIVULGADORA | PLENITUDE | DEUS VIVO | COMUNHAO | MANANCIAL | FOGO | PREGADORES | BETEL | REINO | SENHOR JESUS| JESUS CRISTO | SEMEAR | SHADDAI | LIBERTACAO '),
]
_COMPILADAS = [(r, rel, slug, re.compile(p)) for r, rel, slug, p in REGRAS]

def classificar(razao_social, nome_fantasia=None):
    texto = normalizar(razao_social) + '|' + normalizar(nome_fantasia)
    sem_es = texto.replace(' ESPIRITO SANTO ', ' ')
    for regra, religiao, slug, padrao in _COMPILADAS:
        if padrao.search(sem_es if regra == 'catolica_fraca' else texto):
            return religiao, slug, regra
    return 'nao_identificada', None, 'sem_regra'
```

### atualiza_cnpj.py

```python
"""Atualização mensal dos CNPJs de organizações religiosas (natureza jurídica 3220) no Datafé.

Uso:
  python3 atualiza_cnpj.py verificar
      Mostra a pasta mais nova da Receita e a base já carregada. Sai com código 3 se não houver base nova.
  python3 atualiza_cnpj.py preparar --mes AAAA-MM [--so-arquivos Empresas1,Estabelecimentos1]
      Baixa Empresas e Estabelecimentos do mês, filtra natureza 3220, monta as linhas no formato
      da tabela templos e grava dados/cnpj_AAAA-MM.jsonl, dados/resumo_AAAA-MM.json e
      dados/apagar_AAAA-MM.txt (identificadores que sumiram da base).
  CARGA_TOKEN=... python3 atualiza_cnpj.py carregar --mes AAAA-MM
      Valida e grava em lotes de 5.000 pela função templos-ingest e atualiza os resumos (refresh).
  CARGA_TOKEN=... python3 atualiza_cnpj.py refresh
      Só atualiza os resumos (use depois de apagar linhas que sumiram da base).

A classificação de religião e denominação fica a mesma para CNPJ que já está no banco com o
mesmo nome; só CNPJ novo ou que mudou de nome passa pelo classificador.py.
Nunca imprime o token.
"""
import argparse, csv, io, json, os, re, sys, time, unicodedata, urllib.request, zipfile, base64
import concurrent.futures as cf
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from classificador import classificar, normalizar  # noqa: E402

RF_BASE = 'https://arquivos.receitafederal.gov.br/public.php/webdav/Dados/Cadastros/CNPJ/'
RF_SHARE = os.environ.get('RFB_SHARE_TOKEN', 'gn672Ad4CF8N6TK')
SUPA = 'https://mvxzozxjzbrzndaunlxj.supabase.co'
PUB_KEY = 'sb_publishable_ewekwTa4nrpdlXkhyfdYGg_IZkZskj2'
INGEST = SUPA + '/functions/v1/templos-ingest'
KELVINS = 'https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv'
DADOS = os.path.join(AQUI, 'dados')
ZIPS = os.path.join(AQUI, 'zips')
SITUACAO = {'01': 'nula', '1': 'nula', '02': 'ativa', '2': 'ativa', '03': 'suspensa', '3': 'suspensa',
            '04': 'inapta', '4': 'inapta', '08': 'baixada', '8': 'baixada'}
MINUSCULAS = {'de', 'do', 'da', 'em', 'e', 'dos', 'no', 'das', 'a', 'o', 'para', 'com', 'na', 'ao', 'nos', 'nas'}
MAIUSCULAS = {'II', 'III', 'IV', 'AD', 'IASD', 'IECLB', 'PIB', 'IEAD', 'IPB', 'CCB', 'IELB', 'IPDA', 'IEQ', 'IURD'}


def _auth():
    return 'Basic ' + base64.b64encode((RF_SHARE + ':').encode()).decode()


def _req(url, method='GET', headers=None, data=None, timeout=120):
    h = dict(headers or {})
    return urllib.request.Request(url, method=method, headers=h, data=data)


def meses_receita():
    req = _req(RF_BASE, 'PROPFIND', {'Depth': '1', 'Authorization': _auth()})
    with urllib.request.urlopen(req, timeout=120) as r:
        xml = r.read().decode('utf-8', 'replace')
    return sorted(set(re.findall(r'/CNPJ/(\d{4}-\d{2})/</d:href>', xml)))


def arquivos_do_mes(mes):
    req = _req(RF_BASE + mes + '/', 'PROPFIND', {'Depth': '1', 'Authorization': _auth()})
    with urllib.request.urlopen(req, timeout=120) as r:
        xml = r.read().decode('utf-8', 'replace')
    out = {}
    for resp in re.findall(r'<d:response>(.*?)</d:response>', xml, re.S):
        href = re.search(r'<d:href>([^<]*)</d:href>', resp).group(1)
        tam = re.search(r'<d:getcontentlength>(\d+)</d:getcontentlength>', resp)
        nome = href.rstrip('/').split('/')[-1]
        if tam and nome.endswith('.zip'):
            out[nome] = int(tam.group(1))
    return out


def base_carregada():
    url = SUPA + '/rest/v1/templos?select=referencia&origem=eq.cnpj&limit=1'
    req = _req(url, headers={'apikey': PUB_KEY, 'Authorization': 'Bearer ' + PUB_KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        rows = json.load(r)
    if not rows:
        return None
    m = re.search(r'(\d{4}-\d{2})', rows[0]['referencia'])
    return m.group(1) if m else None


def baixar(mes, nome, tamanho, tentativas=8):
    """Baixa com retomada (Range). Servidor lento (cerca de 1 MB/s por conexão)."""
    os.makedirs(ZIPS, exist_ok=True)
    destino = os.path.join(ZIPS, f'{mes}_{nome}')
    for t in range(tentativas):
        atual = os.path.getsize(destino) if os.path.exists(destino) else 0
        if atual == tamanho:
            return destino
        if atual > tamanho:
            os.remove(destino)
            atual = 0
        h = {'Authorization': _auth()}
        if atual:
            h['Range'] = f'bytes={atual}-'
        try:
            with urllib.request.urlopen(_req(RF_BASE + mes + '/' + nome, headers=h), timeout=300) as r, \
                    open(destino, 'ab' if atual else 'wb') as f:
                while True:
                    bloco = r.read(1 << 20)
                    if not bloco:
                        break
                    f.write(bloco)
        except Exception as e:  # noqa: BLE001
            print(f'  {nome}: tentativa {t + 1} falhou ({type(e).__name__}); retomando', flush=True)
            time.sleep(min(60, 5 * (t + 1)))
    if os.path.getsize(destino) != tamanho:
        raise RuntimeError(f'download incompleto de {nome}')
    return destino


def linhas_csv(caminho):
    with zipfile.ZipFile(caminho) as z:
        for info in z.infolist():
            with z.open(info) as f:
                texto = io.TextIOWrapper(f, encoding='latin-1', newline='')
                yield from csv.reader(texto, delimiter=';', quotechar='"')


def sem_acento(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def titulo(s, siglas=True):
    """Maiúscula inicial por palavra; preposições em minúscula (menos na primeira palavra)."""
    s = re.sub(r'\s+', ' ', (s or '').strip())
    if not s:
        return None
    palavras = s.split(' ')
    out = []
    for i, w in enumerate(palavras):
        up = w.upper()
        if siglas and up in MAIUSCULAS:
            out.append(up)
        elif i > 0 and w.lower() in MINUSCULAS:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return ' '.join(out)


def data_iso(s):
    s = (s or '').strip()
    if not re.fullmatch(r'\d{8}', s) or s == '00000000':
        return None
    try:
        time.strptime(s, '%Y%m%d')
    except ValueError:
        return None
    return f'{s[:4]}-{s[4:6]}-{s[6:]}'


def mapa_siafi():
    caminho = os.path.join(DADOS, 'municipios_kelvins.csv')
    if not os.path.exists(caminho):
        os.makedirs(DADOS, exist_ok=True)
        with urllib.request.urlopen(KELVINS, timeout=120) as r, open(caminho, 'wb') as f:
            f.write(r.read())
    with open(caminho, encoding='utf-8') as f:
        return {int(r['siafi_id']): int(r['codigo_ibge']) for r in csv.DictReader(f)}


def classificacao_atual():
    """Lê do banco (leitura pública) a classificação e os nomes de cada CNPJ já carregado."""
    url = SUPA + '/rest/v1/templos?select=identificador,nome,razao_social,religiao,denominacao_slug,regra&origem=eq.cnpj&order=identificador'
    atual = {}

    def pagina(i):
        req = _req(url, headers={'apikey': PUB_KEY, 'Authorization': 'Bearer ' + PUB_KEY, 'Range': f'{i * 1000}-{i * 1000 + 999}'})
        for t in range(5):
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    return json.load(r)
            except Exception:  # noqa: BLE001
                time.sleep(3 * (t + 1))
        raise RuntimeError('falha ao ler o banco')
    i = 0
    with cf.ThreadPoolExecutor(8) as ex:
        while True:
            paginas = list(ex.map(pagina, range(i, i + 40)))
            for p in paginas:
                for r in p:
                    atual[r['identificador']] = r
            if any(len(p) < 1000 for p in paginas):
                break
            i += 40
    return atual


def preparar(mes, so=None):
    t0 = time.time()
    arquivos = arquivos_do_mes(mes)
    emp = sorted(n for n in arquivos if n.startswith('Empresas'))
    est = sorted(n for n in arquivos if n.startswith('Estabelecimentos'))
    if so:
        emp = [n for n in emp if n.split('.')[0] in so]
        est = [n for n in est if n.split('.')[0] in so]
    if not so and (len(emp) != 10 or len(est) != 10):
        raise RuntimeError(f'pasta {mes} incompleta: {len(emp)} Empresas e {len(est)} Estabelecimentos')
    print(f'{mes}: baixando {len(emp)} Empresas e {len(est)} Estabelecimentos '
          f'({sum(arquivos[n] for n in emp + est) / 1e9:.1f} GB)', flush=True)
    with cf.ThreadPoolExecutor(4) as ex:
        caminhos = dict(zip(emp + est, ex.map(lambda n: baixar(mes, n, arquivos[n]), emp + est)))
    print(f'  download em {(time.time() - t0) / 60:.0f} min', flush=True)

    razoes = {}
    for n in emp:
        for row in linhas_csv(caminhos[n]):
            if len(row) > 2 and row[2].strip() == '3220':
                razoes[row[0]] = row[1]
    print(f'  empresas com natureza 3220: {len(razoes):,}', flush=True)

    siafi = mapa_siafi()
    atual = classificacao_atual() if not so else {}
    linhas, sem_municipio, novos, mantidos = [], 0, 0, 0
    ref = f'CNPJ Receita Federal {mes}'
    for n in est:
        for c in linhas_csv(caminhos[n]):
            if len(c) < 21 or c[0] not in razoes:
                continue
            cnpj = c[0] + c[1] + c[2]
            try:
                ibge = siafi[int(c[20])]
            except (ValueError, KeyError):
                sem_municipio += 1
                continue
            razao = titulo(razoes[c[0]])
            nome = titulo(c[4]) or razao
            numero = (c[15] or '').strip()
            numero = 'S/N' if numero == '0' else numero
            log = ' '.join(x.strip() for x in (c[13], c[14]) if x and x.strip())
            endereco = titulo(', '.join(x for x in (log, numero) if x))
            antigo = atual.get(cnpj)
            if antigo and normalizar(antigo['razao_social']) == normalizar(razao) and normalizar(antigo['nome']) == normalizar(nome):
                religiao, slug, regra = antigo['religiao'], antigo['denominacao_slug'], antigo['regra']
                mantidos += 1
            else:
                religiao, slug, regra = classificar(razao, nome if nome != razao else None)
                novos += 1
            linhas.append({
                'origem': 'cnpj', 'identificador': cnpj, 'codigo_ibge': ibge, 'nome': nome, 'razao_social': razao,
                'endereco': endereco, 'bairro': titulo(c[17]), 'cep': (re.sub(r'\D', '', c[18] or '') or None),
                'latitude': None, 'longitude': None, 'precisao_coord': None,
                'religiao': religiao, 'denominacao_slug': slug, 'regra': regra,
                'situacao': SITUACAO.get((c[5] or '').strip(), None),
                'data_abertura': data_iso(c[10]), 'data_situacao': data_iso(c[6]),
                'cnae': (c[11] or '').strip() or None, 'referencia': ref, 'selo': 'Real',
            })
    os.makedirs(DADOS, exist_ok=True)
    with open(os.path.join(DADOS, f'cnpj_{mes}.jsonl'), 'w', encoding='utf-8') as f:
        for r in linhas:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    novos_ids = {r['identificador'] for r in linhas}
    sumiram = sorted(set(atual) - novos_ids) if atual else []
    with open(os.path.join(DADOS, f'apagar_{mes}.txt'), 'w') as f:
        f.write('\n'.join(sumiram))
    rel = Counter(r['religiao'] for r in linhas)
    ev_ativas = sum(1 for r in linhas if r['religiao'] == 'evangelica' and r['situacao'] == 'ativa')
    resumo = {'mes': mes, 'linhas': len(linhas), 'sem_municipio': sem_municipio,
              'classificados_agora': novos, 'classificacao_mantida': mantidos,
              'evangelicos_ativos': ev_ativas, 'por_religiao': dict(rel),
              'sumiram_da_base': len(sumiram),
              'pct_sumiram': round(100 * len(sumiram) / max(1, len(atual)), 3) if atual else None,
              'minutos': round((time.time() - t0) / 60, 1)}
    with open(os.path.join(DADOS, f'resumo_{mes}.json'), 'w') as f:
        json.dump(resumo, f, ensure_ascii=False, indent=1)
    print(json.dumps(resumo, ensure_ascii=False, indent=1), flush=True)
    return resumo


def _ingest(payload):
    corpo = json.dumps(payload).encode()
    h = {'Content-Type': 'application/json', 'apikey': PUB_KEY}
    for t in range(5):
        try:
            with urllib.request.urlopen(_req(INGEST, 'POST', h, corpo), timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode('utf-8', 'replace')[:500]
            if e.code < 500:
                raise RuntimeError(f'templos-ingest {e.code}: {msg}')
            time.sleep(5 * (t + 1))
        except Exception:  # noqa: BLE001
            time.sleep(5 * (t + 1))
    raise RuntimeError('templos-ingest indisponível')


def carregar(mes):
    token = os.environ.get('CARGA_TOKEN')
    if not token:
        raise SystemExit('defina CARGA_TOKEN no ambiente (não passe na linha de comando)')
    with open(os.path.join(DADOS, f'cnpj_{mes}.jsonl'), encoding='utf-8') as f:
        linhas = [json.loads(x) for x in f]
    t0 = time.time()
    gravadas = 0
    lotes = [linhas[i:i + 5000] for i in range(0, len(linhas), 5000)]
    # valida tudo antes de gravar qualquer coisa
    for i, lote in enumerate(lotes):
        r = _ingest({'token': token, 'acao': 'validar', 'origem': 'cnpj', 'rows': lote})
        if not r.get('ok'):
            raise RuntimeError(f'lote {i + 1} inválido: {json.dumps(r.get("resumo"), ensure_ascii=False)[:800]}')
    for i, lote in enumerate(lotes):
        r = _ingest({'token': token, 'acao': 'upsert', 'origem': 'cnpj', 'rows': lote})
        gravadas += int(r.get('quantidade', 0))
        print(f'  lote {i + 1}/{len(lotes)}: {gravadas:,} linhas', flush=True)
    t1 = time.time()
    _ingest({'token': token, 'acao': 'refresh'})
    out = {'mes': mes, 'linhas_gravadas': gravadas, 'minutos_carga': round((t1 - t0) / 60, 1),
           'segundos_refresh': round(time.time() - t1)}
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('acao', choices=['verificar', 'preparar', 'carregar', 'refresh'])
    ap.add_argument('--mes')
    ap.add_argument('--so-arquivos', help='teste: lista de arquivos, ex.: Empresas1,Estabelecimentos1')
    a = ap.parse_args()
    if a.acao == 'verificar':
        meses = meses_receita()
        carregada = base_carregada()
        nova = meses[-1] if meses else None
        print(json.dumps({'mais_nova_na_receita': nova, 'carregada': carregada,
                          'ha_base_nova': bool(nova and carregada and nova > carregada)}))
        sys.exit(0 if nova and carregada and nova > carregada else 3)
    if a.acao == 'refresh':
        token = os.environ.get('CARGA_TOKEN')
        if not token:
            raise SystemExit('defina CARGA_TOKEN no ambiente')
        t = time.time()
        _ingest({'token': token, 'acao': 'refresh'})
        print(json.dumps({'refresh_segundos': round(time.time() - t)}))
        return
    if not a.mes or not re.fullmatch(r'\d{4}-\d{2}', a.mes):
        raise SystemExit('informe --mes AAAA-MM')
    if a.acao == 'preparar':
        preparar(a.mes, set(a.so_arquivos.split(',')) if a.so_arquivos else None)
    else:
        carregar(a.mes)


if __name__ == '__main__':
    main()
```

### valida_local.py

```python
"""Confere o arquivo preparado com as mesmas regras da função templos-ingest (validation.ts), sem gravar nada."""
import json, re, sys, datetime
REL = {"evangelica", "catolica", "espirita", "matriz_africana", "outras", "nao_identificada"}
TEXTOS = ["nome", "razao_social", "endereco", "bairro", "cep", "denominacao_slug", "regra", "situacao", "cnae"]
def data_ok(v):
    if v is None: return True
    if not isinstance(v, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v): return False
    try: datetime.date.fromisoformat(v); return True
    except ValueError: return False
erros = []; vistos = set()
linhas = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
for i, r in enumerate(linhas, 1):
    if r.get("origem") != "cnpj": erros.append((i, "origem"))
    if not isinstance(r.get("codigo_ibge"), int): erros.append((i, "codigo_ibge"))
    if r.get("religiao") not in REL: erros.append((i, "religiao"))
    for c in ("identificador", "referencia", "selo"):
        if not isinstance(r.get(c), str) or not r[c].strip(): erros.append((i, c))
    for c in TEXTOS:
        if r.get(c) is not None and not isinstance(r[c], str): erros.append((i, c))
    for c in ("data_abertura", "data_situacao"):
        if not data_ok(r.get(c)): erros.append((i, c))
    if r.get("identificador") in vistos: erros.append((i, "duplicado"))
    vistos.add(r.get("identificador"))
print(json.dumps({"linhas": len(linhas), "erros": len(erros), "exemplos": erros[:10]}, ensure_ascii=False))
sys.exit(1 if erros else 0)
```