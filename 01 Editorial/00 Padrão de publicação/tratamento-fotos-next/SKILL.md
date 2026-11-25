---
name: "tratamento-fotos-next"
description: "Trata fotos reais no padrão da Next Editorial (calibrado no livro Destinos ES 2026 e na revista ES Brasil), por tipo — turismo, pessoas e editorial —, e grava a marca de foto tratada. Use antes de gravar, publicar, diagramar ou subir qualquer foto real nos sites, na Retrospectiva, nos mapas do Destinos ES, no Prócidade, nos artigos e no NX Fotos."
---

# Tratamento de fotos Next

Skill separada, de apoio, que todas as skills e rotinas da casa usam para tratar foto real. Foi criada pelo Mário Fernando em 25/11/2026 e substitui as receitas de cor que antes ficavam espalhadas em outras skills: a 9.3 da `padrao-publicacao-next`, o item 7 da `atualizacao-mapas-destinos-es` e o `tratar_fotos.py` da Retrospectiva. Recorte, troca de fundo e montagem continuam com a skill de origem. Toda a cor e a luz passam por aqui.

**Referências medidas.** As referências são 16 fotos do livro "As 100 Mais Belas Praias do Espírito Santo" (Destinos ES 2026, Fundão e Presidente Kennedy, em cor de impressão FOGRA39) e fotos de abertura da **revista ES Brasil** (capa da Retrospectiva 2026, mídia kit e capas). O livro tem cor viva (croma médio de 25,6), é claro e arejado, puxa os azuis para o ciano (cerca de 237°) e mostra o mar turquesa. A **ES Brasil** tem cor mais contida (croma de 18,4), contraste mais firme e azuis em torno de 253°.

**Modelo.** O trabalho pesado é do script, e a skill roda bem no Sonnet.

## 1. Quando usar e quando não usar

- **Usar:** em toda foto real, antes de gravar como destacada, diagramar na revista ou no livro, subir para os mapas do Destinos ES, para o Prócidade ou para o ES em Números, ou guardar no NX Fotos.
- **Não usar:** em arte, logo, print de tela, gráfico do NXtab, capa de revista e imagem gerada por IA (essa é da `imagem-ia-next`).
- **Foto que já passou por aqui** (veja a marca na seção 4) não é tratada de novo.
- **Foto tratada fora daqui** (fotógrafo, Photoshop, app, receita antiga, matéria já publicada) tem o que já foi feito respeitado (seção 5).
- **Foto que já está boa** passa pela análise e sai igual, com a marca de "mantida". É a regra do Mário Fernando de 11/11/2026: se a foto já está tratada e boa, não se mexe nela.

## 2. Os três tipos

O script escolhe sozinho:
- **Pessoas:** quando há rosto em destaque.
- **Turismo:** quando a marca é Destinos ES ou a cena é paisagem natural.
- **Editorial:** em todos os outros casos.

A rotina força o tipo com `--tipo` só quando a escolha automática errar.

| Tipo | Onde entra | Como fica |
|---|---|---|
| Turismo | Destinos ES, praias, montanha, cachoeira, lavoura e paisagem em qualquer marca | Padrão do livro: cor viva, claro, céu reforçado, mar turquesa, sombras abertas, clareza e nitidez moderadas. |
| Pessoas | Retrato, entrevista, evento, auditório | Exposição e pele medidas no rosto. Pele morena ou negra não é clareada à força. As sombras abrem na pessoa, o fundo de estúdio continua escuro e o preto da roupa continua preto. Contraste suave, sem realçar a textura da pele. |
| Editorial | Cidade, obra, porto, indústria, política (**ES Brasil**, Comunhão, Prócidade) | Contraste firme, brancos limpos e um pouco quentes, cor reforçada sem exagero, céu reforçado com moderação. |

Use `--marca destinos` em tudo do Destinos ES (os mapas, o livro e os cadernos de verão). Na **ES Brasil** e na Comunhão, use o padrão (`--marca esbrasil` ou `--marca comunhao`).

## 3. O que o automático mede e ajusta

Cada ajuste é medido na foto e só entra na medida do que falta:
- **Brilho:** só clareia foto escura. Escurece apenas foto estourada. Céu azul profundo não conta como foto escura.
- **Preto e branco:** pretos acinzentados e brancos apagados voltam ao ponto.
- **Sombras:** abrem a mata, a parte de baixo das estruturas e os rostos na sombra, sem lavar o preto.
- **Realces:** recupera nuvem e parede estourada.
- **Contraste:** curva S suave no meio-tom.
- **Cor:** vibração maior nas cores apagadas, com a pele protegida. Os azuis vão para o ciano ("azuis mais quentes") e o mar esverdeado vai para o turquesa no turismo.
- **Balanço:** tira a dominante de cor e deixa um calor leve e cítrico nos brancos, sem amarelar as nuvens.
- **Céu:** o céu azul fraco ganha densidade e um degradê no alto. O céu nublado só ganha volume nas nuvens. **O céu nunca é trocado e nunca fica azul onde não era.**
- **Nitidez:** calibrada pelo tamanho da saída, com limiar para não realçar granulado. É moderada no turismo: o Mário Fernando pediu em 25/11/2026 que fosse reduzida.
- **Foto já forte e bem exposta:** continua sem mudança.

Opção `--verde-citrico`: deixa o verde de lavoura, mata e pasto um pouco mais cítrico. O Mário Fernando pediu esse verde para a abertura do Agro da Retrospectiva em 22/11/2026.

## 4. Marca de foto tratada

Toda saída da skill leva a marca em cinco lugares. Assim, qualquer rotina e o NX Fotos sabem que a foto já foi tratada:

1. **XMP:** `nx:Tratamento="tratamento-fotos-next"`, com `nx:Versao`, `nx:Tipo`, `nx:Decisao` (tratada ou mantida), `nx:Ajustes`, `nx:Previo`, `nx:MarcaInvisivel` e `nx:Data`, no namespace `https://nexteditorial.com.br/ns/foto/1.0/`.
2. **EXIF Software:** `tratamento-fotos-next 1.1 (tipo, decisão)`. Os demais dados EXIF da câmera, do autor e do copyright ficam como vieram.
3. **Comentário JPEG:** `nx-tratada 1.1 tipo decisão data`.
4. **Nome do arquivo:** `-nxt1` para foto tratada e `-nxm1` para foto analisada e mantida, antes da extensão (ex.: `praia-de-setiba-nxt1.jpg`). Use `--sufixo` para o script pôr o sufixo sozinho.
5. **Marca invisível nos pixels:** um padrão de cerca de 1 ponto de luz espalhado pela foto, que não aparece nem a 100%. Ela sobrevive ao que apaga os metadados: versões do CDN (WebP de 800 e 1.600 px), WordPress, WhatsApp e miniaturas de 500 px. Some só com recorte forte, e por isso o recorte vem sempre depois do tratamento. Nos testes de 25/11/2026, a foto marcada deu força de 6 a 21, e a sem marca nunca passou de 3. O limite de detecção é 5.

Para conferir se uma foto já passou pela skill, rode `python3 tratar_foto_next.py --verificar foto.jpg` (aceita também uma pasta). Ele mostra a marca, a força da marca invisível e o que já foi feito fora. O script já faz essa conferência antes de tratar e devolve `"decisao": "ja_tratada"` sem mexer na foto. Use `--forcar` só por ordem expressa.

**No NX Fotos:**
- As versões de 800 e 1.600 px do CDN (`@w1600.webp`) perdem os metadados. Para tratar, baixe sempre o original com `link_do_original`.
- Foto tratada que voltar ao banco recebe a palavra-chave `tratada-nx-v1` (ou `mantida-nx-v1`) e o sufixo no nome do arquivo.
- Quando o NX Fotos passar a tratar sozinho, no envio ou no download, ele deve rodar este mesmo script, guardar a versão tratada com os metadados acima e devolver o original intocado no botão "Baixar original".
- Rotina que achar a marca, a palavra-chave ou o sufixo não trata a foto de novo.

## 5. Tratamento feito fora desta skill

Decisão do Mário Fernando de 25/11/2026: foto já tratada não pode ser estragada por um segundo tratamento. Antes de tratar, o script procura, nesta ordem:

1. **Marcas da casa:** a marca desta skill (seção 4, inclusive a invisível), o `t{k}` no nome das fotos dos mapas do Destinos ES e a palavra-chave `tratada-nx-v1` ou `mantida-nx-v1` do NX Fotos (passe as palavras-chave com `--palavras`). Achou: `ja_tratada`, e a foto não é tocada.
2. **Lightroom ou Camera Raw:** lê ajuste por ajuste o que o fotógrafo fez (luz, cor, balanço de branco, nitidez, máscaras locais). O que ele já acertou fica de fora; o resto é tratado. Exportação com os ajustes no padrão (perfil Adobe Color ou Standard, tudo zerado) conta como foto crua.
3. **Photoshop, apps** (Snapseed, VSCO, Picsart, Canva, Instagram e outros) **ou foto tirada de matéria já publicada** (`--origem site`, `revista` ou `instagram`): só entra correção de defeito grosseiro, como foto muito escura ou dominante forte. Fora isso, a foto fica como está, com a marca de mantida.
4. **Reveladores** (Capture One, DxO, darktable e outros): luz, balanço e nitidez ficam com o revelador, e a skill cuida da cor.
5. **Celular:** a nitidez e a cor que o aparelho já pôs são medidas na foto, e a skill não põe mais por cima.
6. **Sem nenhum rastro** (receita antiga, foto de terceiros sem metadados): só pela aparência não dá para separar foto tratada de foto viva de câmera. Por isso, os pisos de estilo da casa (calor, vibração, contraste, clareza, nitidez) só entram em foto que ainda não chegou à meta. E mudança total abaixo do perceptível (ΔE 1,5) não é gravada.

Na prática, use sempre `--origem` quando souber de onde a foto veio (`nxfotos`, `site`, `revista`, `agencia`, `google`, `prefeitura`, `instagram`).

## 6. Como aplicar

1. **Original:** baixe o arquivo em resolução cheia. No NX Fotos, use `link_do_original`, que vale 15 minutos. No NX Feed, use a URL da foto.
2. **Marca:** se a foto já tem a marca (inclusive a invisível) ou o script devolver `ja_tratada`, use como está.
3. **Tratar:** `python3 tratar_foto_next.py entrada.jpg saida.jpg --marca <destinos|esbrasil|comunhao> --origem <nxfotos|site|...> --sufixo`. Para site, acrescente `--largura 2400`. Para impresso (revista ou livro), use a resolução cheia, sem `--largura`. O script limita o lado maior a 5.000 px, que dão 42 cm a 300 dpi, por causa da memória do ambiente.
4. **Olhar:** confira a foto tratada antes de gravar. Se o tipo saiu errado, rode de novo com `--tipo`. Se ficou forte demais, use `--forca 0.7`.
5. **Gravar:**
   - **Sites (NX Feed):** `pedir_link_de_envio` com `tratamento="nao"` + `curl -T` e depois `definir_imagem_destacada` com `tratamento="nao"`. A foto já vai tratada, e o NX Feed não deve tratar de novo. O link de envio é de uso único: não mostre nem guarde.
   - **Retrospectiva e livro:** trate primeiro e recorte depois, com as ferramentas da skill de origem.
   - **Mapas do Destinos ES:** o sufixo `-nxt1` ou `-nxm1` substitui a marca antiga `t{k}` no nome do arquivo. Fotos antigas com `t{k}` continuam valendo como tratadas.
6. **Resumo da rodada:** registre "foto tratada (tipo e principais ajustes)" ou "foto mantida" (com o motivo, se for tratamento prévio). Se não der para tratar, por erro ou falta de memória, grave a original e registre "foto sem tratamento" em Pendências.

## 7. Instalação do script

- O script fica no bloco da seção 9. Grave-o como `tratar_foto_next.py` na pasta de trabalho.
- Dependências: `pip install --break-system-packages opencv-contrib-python-headless numpy pillow pillow-heif`. O `cv2.ximgproc` vem do pacote contrib, e o `pillow-heif` abre as fotos de iPhone (HEIC).
- Os detectores de rosto do OpenCV (frontal e perfil) são baixados sozinhos do GitHub para `~/.cache/next_fotos/` na primeira execução. Se a rede bloquear, a foto sai tratada como editorial, sem o tipo pessoas, e isso vai para o resumo.
- Em lote: `python3 tratar_foto_next.py pasta_entrada pasta_saida --marca destinos` trata todas as fotos da pasta, põe o sufixo e imprime uma linha JSON por foto.

## 8. Onde esta skill entra

Decisão do Mário Fernando de 25/11/2026: todas as skills que usam foto real passam por esta antes de gravar.
- **`padrao-publicacao-next`, seção 9.3:** vale para todas as rotinas dos sites **ES Brasil** e Comunhão (noturnas, Estilo, esporte, Panorama, política, Igreja, Missões, Diversão e arte, acervo, artigos, Datafé, Fórmula 1 e as que vierem).
- **`retrospectiva-esbrasil`, etapa 7, e `artigos-retrospectiva-2026`:** tratamento em resolução cheia, antes do recorte do kit.
- **`atualizacao-mapas-destinos-es`, item 7:** sempre `--marca destinos`, com o sufixo no nome no lugar de `t{k}`.
- **`artigos-acervo-esbrasil`, `artigos-acervo-comunhao` e `artigos-acervo-next`:** o retrato do articulista é tratado aqui (tipo pessoas) e entra no `padronizar_retrato.py` com `--sem-tratamento`. O recorte, a troca de fundo e o tamanho da cabeça continuam como estão.
- **`cidade-em-numeros-procidade` e `verificacao-es-em-numeros`:** as fotos do NX Fotos passam por aqui antes de entrar no site.
- **Capas do YouTube (`youtube-esbrasil-titulos` e `youtube-comunhao-titulos`):** a foto de origem pode vir tratada daqui. A restauração e o recorte da capa continuam no `tratar_foto.py` delas.

Quando uma skill dessas ainda trouxer receita própria de cor, vale esta skill no lugar dela.

## 9. Script `tratar_foto_next.py` (versão 1.1)

```python
#!/usr/bin/env python3
"""Tratamento de fotos no padrão Next Editorial, por tipo de foto.

Tipos (calibrados nas páginas impressas do livro Destinos ES 2026 e da revista ES Brasil):
  turismo    praia, montanha, cachoeira, paisagem: cor viva, claro e arejado, céu e mar reforçados,
             sombras abertas, clareza e nitidez de revista de viagem.
  pessoas    retrato, entrevista, evento: exposição e pele medidas no rosto, sombras abertas só na
             pessoa, contraste suave, pele sem textura exagerada, fundo contido.
  editorial  cidade, porto, indústria, obra, política: contraste firme, brancos neutros a levemente
             quentes, cor reforçada sem exagero, nitidez alta.
  auto       rosto relevante -> pessoas; marca destinos ou paisagem natural -> turismo; senão editorial.

Cada ajuste (brilho, contraste, sombras, realces, cor, céu, nitidez) é medido na foto e só entra
na medida do que falta. Foto que já está boa sai igual (decisao "mantida").
O céu é reforçado, nunca trocado: céu branco de dia nublado não vira azul.

Tratamento prévio (v1.1): antes de tratar, o script procura (1) a marca desta skill nos metadados e no
nome, (2) a marca invisível nos pixels, que sobrevive a CDN, WordPress e WhatsApp, (3) as marcas antigas
da casa (t{k} dos mapas, palavra-chave tratada-nx-v1) e (4) o que o fotógrafo ou outro programa já fez
(Lightroom/Camera Raw lido ajuste por ajuste, Photoshop, apps, reveladores, origem da foto). O que já foi
feito fica de fora; foto editada fora sem detalhe só recebe correção de defeito grosseiro. Os "pisos" de
estilo da casa só entram em foto que ainda não chegou à meta, e mudança total abaixo de 1,5 ΔE não é gravada.

Uso:
  python3 tratar_foto_next.py entrada.jpg saida.jpg [--tipo auto|turismo|pessoas|editorial]
         [--marca esbrasil|destinos|comunhao] [--forca 1.0] [--largura 0] [--qualidade 90]
         [--sufixo] [--forcar] [--verde-citrico] [--origem nxfotos|site|revista|agencia|google|...]
         [--palavras "palavras-chave do NX Fotos"]
  python3 tratar_foto_next.py pasta_entrada pasta_saida --marca destinos      (lote)
  python3 tratar_foto_next.py --verificar foto_ou_pasta                       (já foi tratada? o que já foi feito?)
Imprime JSON: tipo, decisao (tratada, mantida, ja_tratada), ajustes aplicados (0 a 1), previo e medidas.
Toda saída leva a marca de tratada: XMP nx:Tratamento, EXIF Software, comentário JPEG, marca invisível
nos pixels e, com --sufixo, -nxt1 (tratada) ou -nxm1 (mantida) no nome.
"""
import argparse, json, os, sys, urllib.request
import numpy as np
import cv2

PERFIS = {
    'turismo': dict(C_alvo=24.0, L_med=57.0, std_alvo=20.0, preto=4.0, branco=97.0,
                    contraste=0.12, sombras=1.4, realces=0.55, clareza=0.26, nitidez=0.42,
                    vib=0.90, ceu=1.0, ceu_C=30.0, ceu_h=242.0, azul_shift=-12.0, agua_shift=16.0,
                    quente=(0.5, 2.2), cast_fix=0.75),
    'editorial': dict(C_alvo=20.0, L_med=53.0, std_alvo=21.5, preto=3.0, branco=97.0,
                      contraste=0.20, sombras=1.1, realces=0.50, clareza=0.24, nitidez=0.60,
                      vib=0.80, ceu=0.7, ceu_C=27.0, ceu_h=248.0, azul_shift=-7.0, agua_shift=8.0,
                      quente=(0.3, 1.6), cast_fix=0.75),
    'pessoas': dict(C_alvo=17.0, L_med=None, std_alvo=19.0, preto=3.0, branco=97.0,
                    contraste=0.08, sombras=0.8, realces=0.45, clareza=0.10, nitidez=0.40,
                    vib=0.35, ceu=0.45, ceu_C=26.0, ceu_h=248.0, azul_shift=-4.0, agua_shift=0.0,
                    quente=(0.2, 1.0), cast_fix=0.5, pele_L=66.0, pele_a=15.5, pele_b=17.0),
}
HAAR_URL = 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml'


# ---------------------------------------------------------------- utilidades
def suave(x, a, b):
    t = np.clip((x - a) / max(b - a, 1e-6), 0, 1)
    return t * t * (3 - 2 * t)


def banda_h(h, centro, largura):
    d = np.abs(((h - centro + 180) % 360) - 180)
    return np.clip(1 - d / largura, 0, 1) ** 1.5


def to_lab(bgr01):
    return cv2.cvtColor(bgr01.astype(np.float32), cv2.COLOR_BGR2Lab)


def from_lab(lab):
    return cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_Lab2BGR)


def _cascade(nome='haarcascade_frontalface_default.xml'):
    base = getattr(getattr(cv2, 'data', None), 'haarcascades', '') or ''
    cands = [os.path.join(base, nome),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modelos', nome),
             os.path.expanduser('~/.cache/next_fotos/' + nome)]
    for c in cands:
        if c and os.path.exists(c):
            return cv2.CascadeClassifier(c)
    try:
        os.makedirs(os.path.dirname(cands[-1]), exist_ok=True)
        urllib.request.urlretrieve(HAAR_URL.replace('haarcascade_frontalface_default.xml', nome), cands[-1])
        return cv2.CascadeClassifier(cands[-1])
    except Exception:
        return None


def _nms(caixas):
    out = []
    for c in sorted(caixas, key=lambda r: -r[2] * r[3]):
        x, y, w, h = c
        if all(abs((x + w / 2) - (o[0] + o[2] / 2)) > 0.5 * max(w, o[2]) or abs((y + h / 2) - (o[1] + o[3] / 2)) > 0.5 * max(h, o[3]) for o in out):
            out.append(c)
    return out


def rostos(bgr8):
    h, w = bgr8.shape[:2]
    s = min(1.0, 1200 / max(h, w))
    small = cv2.resize(bgr8, (int(w * s), int(h * s))) if s < 1 else bgr8
    g = cv2.equalizeHist(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY))
    mn = (max(18, int(small.shape[1] * 0.018)),) * 2
    fs = []
    cf, cp = _cascade(), _cascade('haarcascade_profileface.xml')
    if cf is not None and not cf.empty():
        fs += [tuple(r) for r in cf.detectMultiScale(g, 1.1, 6, minSize=mn)]
    if cp is not None and not cp.empty():
        fs += [tuple(r) for r in cp.detectMultiScale(g, 1.1, 6, minSize=mn)]
        gw = g.shape[1]
        fs += [(gw - x - fw, y, fw, fh) for (x, y, fw, fh) in cp.detectMultiScale(cv2.flip(g, 1), 1.1, 6, minSize=mn)]
    fs = _nms(fs)
    # descarta "rostos" sem cor de pele (falso positivo em textura)
    lab = to_lab(small.astype(np.float32) / 255)
    ok = []
    for (x, y, fw, fh) in fs:
        r = lab[y + fh // 4:y + 3 * fh // 4, x + fw // 4:x + 3 * fw // 4]
        a, b = float(np.median(r[..., 1])), float(np.median(r[..., 2]))
        Cr = np.hypot(r[..., 1], r[..., 2]); hr = (np.degrees(np.arctan2(r[..., 2], r[..., 1])) + 360) % 360
        pele = ((hr > 15) & (hr < 85) & (Cr > 7) & (Cr < 55) & (r[..., 0] > 18) & (r[..., 0] < 93)).mean()
        if a > 3 and b > 4 and pele > 0.45:
            ok.append((int(x / s), int(y / s), int(fw / s), int(fh / s)))
    return ok


def medir(lab):
    if lab.shape[0] * lab.shape[1] > 3e6:
        e = (3e6 / (lab.shape[0] * lab.shape[1])) ** 0.5
        lab = cv2.resize(lab, (int(lab.shape[1] * e), int(lab.shape[0] * e)), interpolation=cv2.INTER_AREA)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    C = np.hypot(a, b)
    neu = (C < 12) & (L > 25) & (L < 90)
    m = dict(L_p01=float(np.percentile(L, 1)), L_p05=float(np.percentile(L, 5)), L_p50=float(np.median(L)),
             L_p995=float(np.percentile(L, 99.5)), L_std=float(L.std()), C_med=float(C.mean()),
             sombra=float((L < 20).mean()), estouro=float((L > 97).mean()), estouro98=float((L > 98.5).mean()))
    if neu.sum() > 500:
        m['cast_a'] = float(a[neu].mean()); m['cast_b'] = float(b[neu].mean())
    else:
        m['cast_a'] = m['cast_b'] = 0.0
    g = cv2.cvtColor(np.clip(L / 100 * 255, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)[..., 0]
    s = 1600 / max(g.shape)
    if s < 1:
        g = cv2.resize(g, (int(g.shape[1] * s), int(g.shape[0] * s)), interpolation=cv2.INTER_AREA)
    m['nitidez'] = float(np.abs(cv2.Laplacian(g, cv2.CV_32F)).mean())
    # nitidez que a foto já recebeu: quanto as bordas fortes passam do platô vizinho (halo)
    gf = g.astype(np.float32)
    mag = cv2.magnitude(cv2.Sobel(gf, cv2.CV_32F, 1, 0), cv2.Sobel(gf, cv2.CV_32F, 0, 1))
    borda = mag > np.percentile(mag, 98)
    k3, k9 = np.ones((3, 3), np.uint8), np.ones((9, 9), np.uint8)
    lis = cv2.GaussianBlur(gf, (0, 0), 2.5)
    mx9, mn9 = cv2.dilate(lis, k9), cv2.erode(lis, k9)
    sobra = np.clip(cv2.dilate(gf, k3) - mx9, 0, None) + np.clip(mn9 - cv2.erode(gf, k3), 0, None)
    m['halo'] = float(sobra[borda].mean() / max(1.0, float((mx9 - mn9)[borda].mean()))) if borda.any() else 0.0
    m['local'] = float(np.abs(gf - cv2.GaussianBlur(gf, (0, 0), 16)).mean() / 2.55)   # clareza que a foto já tem
    return m


# ---------------------------------------------------------------- máscaras
def mascara_ceu(lab):
    """Céu = região azul ou de nuvem, lisa, ligada à borda de cima. Devolve (máscara, peso_azul)."""
    H, W = lab.shape[:2]
    s = 480 / max(H, W)
    sm = cv2.resize(lab, (max(8, int(W * s)), max(8, int(H * s))), interpolation=cv2.INTER_AREA)
    L, a, b = sm[..., 0], sm[..., 1], sm[..., 2]
    C = np.hypot(a, b); h = (np.degrees(np.arctan2(b, a)) + 360) % 360
    mu = cv2.blur(L, (7, 7)); sd = np.sqrt(np.maximum(cv2.blur(L * L, (7, 7)) - mu * mu, 0))
    azul = (h > 195) & (h < 300) & (C > 4) & (L > 38) & (sd < 9)
    nuvem = (C < 11) & (L > 70) & (sd < 7)
    cand = ((azul | nuvem) * 255).astype(np.uint8)
    cand = cv2.morphologyEx(cand, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lbl, st, _ = cv2.connectedComponentsWithStats(cand, 8)
    topo = set(np.unique(lbl[:max(2, int(sm.shape[0] * 0.04)), :])) - {0}
    m = np.isin(lbl, list(topo)).astype(np.float32) if topo else np.zeros(L.shape, np.float32)
    # céu fica no alto: corta o que desce além de 75% da altura
    yy = np.linspace(0, 1, m.shape[0])[:, None]
    m *= 1 - suave(yy, 0.6, 0.8)
    m = cv2.GaussianBlur(m, (0, 0), 2.5)
    pa = (azul.astype(np.float32))
    pa = cv2.GaussianBlur(pa, (0, 0), 1.5)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    pa = cv2.resize(pa, (W, H), interpolation=cv2.INTER_LINEAR)
    return np.clip(m, 0, 1), np.clip(pa, 0, 1)


def mascaras_pessoa(lab, faces):
    """Máscaras de pele e de pessoa, calculadas em escala reduzida (rápido em foto grande)."""
    H, W = lab.shape[:2]
    e = min(1.0, 900 / max(H, W))
    sm = cv2.resize(lab, (max(8, int(W * e)), max(8, int(H * e))), interpolation=cv2.INTER_AREA) if e < 1 else lab
    L, a, b = sm[..., 0], sm[..., 1], sm[..., 2]
    C = np.hypot(a, b); h = (np.degrees(np.arctan2(b, a)) + 360) % 360
    hue_ok = banda_h(h, 50, 32) * suave(C, 6, 12) * (1 - suave(C, 48, 60)) * suave(L, 15, 25)
    hs, ws = sm.shape[:2]
    rosto = np.zeros((hs, ws), np.float32); corpo = np.zeros((hs, ws), np.float32)
    for (x, y, w, hh) in faces:
        x, y, w, hh = int(x * e), int(y * e), max(2, int(w * e)), max(2, int(hh * e))
        cv2.ellipse(rosto, (x + w // 2, y + int(hh * 0.6)), (int(w * 0.95), int(hh * 1.35)), 0, 0, 360, 1, -1)
        cv2.ellipse(corpo, (x + w // 2, y + int(hh * 2.6)), (int(w * 2.4), int(hh * 4.2)), 0, 0, 360, 1, -1)
    if faces:
        sg = max(1.5, faces[0][2] * e * 0.18)
        rosto = cv2.GaussianBlur(rosto, (0, 0), sg)
        corpo = np.maximum(cv2.GaussianBlur(corpo, (0, 0), sg * 3), rosto)
    pele = (hue_ok * np.maximum(rosto, 0.6 * corpo)).astype(np.float32)
    if e < 1:
        pele = cv2.resize(pele, (W, H), interpolation=cv2.INTER_LINEAR)
        corpo = cv2.resize(corpo, (W, H), interpolation=cv2.INTER_LINEAR)
    return pele, corpo


def classificar(lab, faces, marca):
    H, W = lab.shape[:2]
    area = sum(w * h for (_, _, w, h) in faces) / (H * W)
    maior = max([w for (_, _, w, _) in faces], default=0) / W
    if area > 0.006 or maior > 0.05:
        return 'pessoas'
    if marca == 'destinos':
        return 'turismo'
    s = 400 / max(H, W)
    sm = cv2.resize(lab, (int(W * s), int(H * s)), interpolation=cv2.INTER_AREA)
    L, a, b = sm[..., 0], sm[..., 1], sm[..., 2]
    C = np.hypot(a, b); h = (np.degrees(np.arctan2(b, a)) + 360) % 360
    veg = ((h > 95) & (h < 175) & (C > 8)).mean()
    agua = ((h > 170) & (h < 290) & (C > 6)).mean()
    areia = ((h > 50) & (h < 95) & (C > 9) & (C < 40) & (L > 45)).mean()
    g = np.clip(L * 2.55, 0, 255).astype(np.uint8)
    bordas = (cv2.Canny(g, 60, 160) > 0).mean()
    natural = veg + agua + areia
    neutro = ((C < 7) & (L > 30) & (L < 92)).mean()
    return 'turismo' if (natural > 0.6 or (natural > 0.5 and neutro < 0.3)) else 'editorial'


def gamut_ok(lab):
    for _ in range(6):
        bgr = from_lab(lab)
        fora = ((bgr < -0.002) | (bgr > 1.002)).any(-1)
        if fora.mean() < 0.0005:
            break
        lab[..., 1][fora] *= 0.9; lab[..., 2][fora] *= 0.9
    return np.clip(from_lab(lab), 0, 1)


# ---------------------------------------------------------------- tratamento
# Meta de cada ajuste: o valor a partir do qual a foto já está no padrão da casa (medianas da
# 1ª passada aprovada em 25/11/2026). Acima da meta, o ajuste não entra: foto já tratada não acumula.
METAS = {
    'turismo':   dict(local=7.0, halo=1.10, cast_b=0.8),
    'editorial': dict(local=7.8, halo=1.10, cast_b=0.9),
    'pessoas':   dict(local=3.8, halo=0.30, cast_b=1.1),
}
GRUPOS = ('luz', 'cor', 'balanco', 'nitidez', 'ceu')
LIMIAR_MUDANCA = 1.5   # ΔE médio; abaixo disso a mudança não se vê e a foto fica como veio


def tratar(bgr8, tipo='auto', marca='esbrasil', forca=1.0, verde_citrico=False, previo=None):
    previo = previo or {}
    feitos = set(previo.get('feitos', []))
    if previo.get('nivel', 0) >= 2:
        feitos |= set(GRUPOS)
    livre = lambda g: g not in feitos                          # grupo já feito fora: só defeito grosseiro
    bgr = bgr8.astype(np.float32) / 255
    lab = to_lab(bgr)
    faces = rostos(bgr8)
    if tipo == 'auto':
        tipo = classificar(lab, faces, marca)
    P, M = PERFIS[tipo], METAS[tipo]
    antes = medir(lab)
    L, a, b = lab[..., 0].copy(), lab[..., 1].copy(), lab[..., 2].copy()
    C0 = np.hypot(a, b)
    Hh, Ww = L.shape
    pele, corpo = mascaras_pessoa(lab, faces) if faces else (np.zeros(L.shape, np.float32),) * 2
    ceu, azul_px = mascara_ceu(lab)
    ceu_frac = float(ceu.mean())
    del bgr, lab

    # ---- o que falta em cada ajuste (0 = nada) ----
    aj = {}
    aj['cor'] = float(np.clip((P['C_alvo'] - antes['C_med']) / (P['C_alvo'] * 0.55), 0, 1)) if livre('cor') else 0.0
    cast = np.hypot(antes['cast_a'], antes['cast_b'])
    aj['balanco'] = float(np.clip((cast - 1.5) / 4.0, 0, 1)) if livre('balanco') else float(np.clip((cast - 5) / 4.0, 0, 1))
    if livre('luz'):
        aj['sombras'] = float(np.clip((antes['sombra'] - 0.03) / 0.12, 0, 1))
        aj['realces'] = float(np.clip((antes['estouro'] - 0.002) / 0.02, 0, 1))
        aj['contraste'] = float(np.clip((P['std_alvo'] - antes['L_std']) / 8, 0, 1))
        lavado = float(np.clip((antes['L_p01'] - (P['preto'] + 5)) / 10, 0, 1))
        aj['pontos'] = max(lavado, float(np.clip(((P['branco'] - 8) - antes['L_p995']) / 10, 0, 1)))
    else:                                                      # luz já acertada fora: só defeito grosseiro
        aj['sombras'] = float(np.clip((antes['sombra'] - 0.25) / 0.2, 0, 1))
        aj['realces'] = float(np.clip((antes['estouro98'] - 0.05) / 0.05, 0, 1))
        aj['contraste'] = float(np.clip((P['std_alvo'] - 8 - antes['L_std']) / 8, 0, 1))
        aj['pontos'] = float(np.clip(max(antes['L_p01'] - (P['preto'] + 15), (P['branco'] - 25) - antes['L_p995']) / 10, 0, 1))
    aj['brilho'] = 0.0
    hh0 = (np.degrees(np.arctan2(b, a)) + 360) % 360
    azul_forte = (C0 > 25) & (hh0 > 200) & (hh0 < 300)          # céu azul profundo não é foto escura
    Lmed_util = float(np.median(L[~azul_forte])) if (~azul_forte).mean() > 0.2 else antes['L_p50']
    if P['L_med'] and not livre('luz'):                       # luz feita fora: só foto escura de verdade
        if Lmed_util < 30:
            aj['brilho'] = float(np.clip((36 - Lmed_util) / 12, 0, 0.6))
    elif P['L_med']:
        if Lmed_util < P['L_med'] - 3:
            aj['brilho'] = float(np.clip((P['L_med'] - Lmed_util) / 12, 0, 1))
        elif antes['L_p50'] > P['L_med'] + 18 and antes['estouro'] > 0.02:
            aj['brilho'] = float(np.clip((antes['L_p50'] - P['L_med'] - 18) / 12, 0, 0.6))
    # céu: azul pálido pede reforço; céu branco (nublado) só recupera nuvens
    aj['ceu'] = 0.0; ceu_modo = 'sem céu'
    if ceu_frac > 0.05 and livre('ceu') and livre('cor'):
        wa = ceu * azul_px
        if wa.sum() / max(ceu.sum(), 1e-6) > 0.25:
            Cs = float(np.average(C0, weights=wa + 1e-6))
            aj['ceu'] = float(np.clip((P['ceu_C'] - Cs) / (P['ceu_C'] * 0.5), 0, 1)); ceu_modo = 'azul'
        else:
            Ls = float(np.average(L, weights=ceu + 1e-6))
            aj['ceu'] = float(np.clip((Ls - 80) / 12, 0, 1)) * 0.7; ceu_modo = 'nublado'
    if tipo == 'pessoas':
        aj['pele'] = 1.0 if (faces and livre('cor')) else 0.0
    if antes['C_med'] > 1.5 * P['C_alvo'] and tipo != 'pessoas':
        aj['cor'] = 0.0
        if antes['L_p995'] > 75:   # foto já forte e bem exposta: não mexe
            return bgr8, dict(tipo=tipo, decisao='mantida', motivo='foto já forte', ajustes={}, ceu=ceu_modo,
                              rostos=len(faces), previo=previo or None, antes=_r(antes), depois=_r(antes))
    principais = [v for k, v in aj.items()]
    if max(principais) < 0.15:
        return bgr8, dict(tipo=tipo, decisao='mantida', motivo='já está no padrão' if not feitos else 'tratamento prévio respeitado',
                          ajustes={}, ceu=ceu_modo, rostos=len(faces), previo=previo or None, antes=_r(antes), depois=_r(antes))
    f = forca
    # pisos de estilo (o "jeito da casa") só entram em foto que ainda não chegou à meta
    ja_viva = antes['C_med'] >= 0.85 * P['C_alvo']
    ja_quente = antes['cast_b'] >= M['cast_b'] - 0.3 and abs(antes['cast_a']) < 1.5

    # ---- 1. balanço: tira dominante, leve calor cítrico (pele fora) ----
    qa, qb = P['quente']
    if ja_quente or not livre('balanco'):
        qa = qb = 0.0
    kb = f * max(aj['balanco'], 0.5 * aj['cor'], 0.0 if (ja_quente or not livre('balanco')) else 0.3)
    peso = (1 - 0.5 * suave(C0, 10, 40)) * (1 - pele)
    a += kb * (-P['cast_fix'] * antes['cast_a'] + qa) * peso
    b += kb * (-P['cast_fix'] * antes['cast_b'] + qb) * peso

    # ---- 2. tons: base (luz) + detalhe (textura) ----
    Ln = (L / 100).astype(np.float32)
    esc = min(1.0, 2000 / max(Hh, Ww))
    if esc < 1:
        Ls = cv2.resize(Ln, (int(Ww * esc), int(Hh * esc)), interpolation=cv2.INTER_AREA)
        bs = cv2.ximgproc.guidedFilter(Ls, Ls, max(4, int(max(Ls.shape) / 60)), 0.01)
        base = cv2.resize(bs, (Ww, Hh), interpolation=cv2.INTER_LINEAR)
    else:
        base = cv2.ximgproc.guidedFilter(Ln, Ln, max(4, int(max(Hh, Ww) / 60)), 0.01)
    det = Ln - base
    # pontos de preto e branco
    amostra = base[::4, ::4] if base.size > 4e6 else base
    lo, hi = np.percentile(amostra, 0.5), np.percentile(amostra, 99.7)
    alvo = P['preto'] / 100 + (base - lo) / max(hi - lo, 1e-3) * (P['branco'] - P['preto']) / 100
    fora_ponto = lo > P['preto'] / 100 + 0.03 or hi < (P['branco'] - 9) / 100
    k_p = max(aj['pontos'], 0.5 if (fora_ponto and livre('luz')) else 0.0)
    base = base + f * k_p * (np.clip(alvo, 0, 1) - base)
    # brilho (meio-tom)
    if tipo == 'pessoas' and faces and livre('luz'):
        fm = pele > 0.45
        if fm.sum() > 150:
            Lf = float(np.median(L[fm]))
            # pele escura não é clareada à força: só sobe se a foto inteira está escura
            # (sem brancos de verdade) ou se o rosto está muito apagado
            sobe = antes['L_p995'] < 80 or Lf < 35
            alvoL = min(max(Lf, 58.0 if sobe else Lf), 76.0)
            g = float(np.clip(alvoL / max(Lf, 1), 0.88, 1.35))
            if abs(g - 1) > 0.02:
                aj['brilho'] = round(min(1.0, abs(g - 1) * 3), 2)
                loc = 0.35 + 0.65 * corpo                  # mais forte na pessoa
                base = base * (1 + f * (g - 1) * loc)
    elif aj['brilho'] > 0:
        med = float(np.median(base)); alvo = P['L_med'] / 100 if livre('luz') else 0.38
        if antes['L_p50'] > P['L_med']:
            alvo = (antes['L_p50'] - 8) / 100
        gam = float(np.clip(np.log(alvo) / np.log(max(med, 1e-3)), 0.72, 1.2))
        base = np.clip(base, 1e-4, 1) ** (1 + f * min(1, aj['brilho'] * 1.5) * (gam - 1))
    # sombras (abre o escuro sem lavar o preto)
    if aj['sombras'] > 0:
        t = 0.6
        s_amt = f * P['sombras'] * aj['sombras']
        lift = s_amt * base * np.clip(1 - base / t, 0, 1) ** 2 * suave(base, 0.04, 0.14)  # preto continua preto
        if tipo == 'pessoas':
            lift *= 0.25 + 0.75 * corpo                  # fundo de estúdio continua escuro
        base = base + lift
    # realces (segura céu, pele clara, branco)
    kr = aj['realces']
    t2 = 0.72
    base = base - f * P['realces'] * kr * np.clip(base - t2, 0, None) ** 2 / (1 - t2) * 0.9
    # contraste (curva S no meio-tom)
    kc = f * (P['contraste'] * ((0.5 if (antes['L_std'] < P['std_alvo'] + 1 and livre('luz')) else 0.0) + aj['contraste']))
    piv = float(np.clip(np.median(base), 0.35, 0.6))
    x = base - piv
    base = base + kc * x * (1 - np.abs(np.clip(x / max(piv, 1 - piv), -1, 1))) * 2
    base = np.clip(base, 0, 1)
    # clareza (detalhe de meia frequência), menos na pele e nas pontas
    meio = suave(base, 0.06, 0.22) * (1 - suave(base, 0.86, 0.98))
    k_cl = 1.0 if (livre('nitidez') and antes['local'] < M['local']) else 0.0
    cl = 1 + f * P['clareza'] * k_cl * meio * (1 - 0.85 * pele)
    L = np.clip((base + det * cl) * 100, 0, 100)

    # ---- 3. céu ----
    if aj['ceu'] > 0.05:
        r = f * P['ceu'] * aj['ceu']
        yy = np.linspace(1, 0, Hh)[:, None].astype(np.float32)   # 1 no topo
        if ceu_modo == 'azul':
            w = ceu * azul_px * (1 - pele)
            L = L - r * w * (3 + 5 * yy) * suave(L, 40, 60)       # filtro degradê
            Cc = np.hypot(a, b); hc = np.degrees(np.arctan2(b, a))
            dh = ((P['ceu_h'] - hc + 180) % 360) - 180
            hc = hc + r * w * 0.35 * dh
            Cc = Cc * (1 + r * w * 0.40)
            a, b = Cc * np.cos(np.radians(hc)), Cc * np.sin(np.radians(hc))
        wn = ceu * (1 - azul_px)                                   # nuvens: volume
        e2 = min(1.0, 1200 / max(Hh, Ww))
        Lp = cv2.resize(L, (int(Ww * e2), int(Hh * e2)), interpolation=cv2.INTER_AREA) if e2 < 1 else L
        Lp = cv2.GaussianBlur(Lp, (0, 0), max(Lp.shape) / 150)
        loc = L - (cv2.resize(Lp, (Ww, Hh), interpolation=cv2.INTER_LINEAR) if e2 < 1 else Lp)
        L = L + r * wn * (0.6 * loc - 0.10 * np.clip(L - 75, 0, None))

    # ---- 4. cor: vibração, azuis ao ciano, mar turquesa, pele ----
    C = np.hypot(a, b); h = np.degrees(np.arctan2(b, a)); hh = h % 360
    kv = f * max(aj['cor'], 0.0 if (ja_viva or not livre('cor')) else (0.45 if tipo == 'turismo' else 0.25))
    vib = P['vib'] * kv * (1 - np.clip(C / 60, 0, 1)) * (1 - 0.75 * pele)
    if tipo == 'pessoas':
        vib *= 0.6 + 0.4 * (1 - corpo)                            # roupa e fundo contidos
    C2 = C * (1 + vib)
    claro = 1 - 0.6 * suave(L, 78, 94)
    az = banda_h(hh, 260, 45) * suave(C, 3, 8) * claro * (1 - ceu * azul_px)
    h = h + kv * P['azul_shift'] * az
    C2 = C2 * (1 + kv * 0.25 * az)
    ag = suave(hh, 140, 155) * (1 - suave(hh, 205, 225)) * suave(C, 3, 8) * (1 - pele) * (1 - ceu)
    h = h + kv * P['agua_shift'] * ag
    C2 = C2 * (1 + kv * 0.25 * ag * (P['agua_shift'] > 0))
    if tipo == 'pessoas' and faces and livre('cor'):
        fm = pele > 0.45
        if fm.sum() > 150:
            aa, bb = C2 * np.cos(np.radians(h)), C2 * np.sin(np.radians(h))
            ma, mb = float(np.median(aa[fm])), float(np.median(bb[fm]))
            # só corrige pele fora da faixa natural (vermelha, alaranjada, verde ou cinza);
            # pele morena e negra tem b* mais alto e fica como está
            ca = float(np.clip(min(max(ma, 9.0), 21.0) - ma, -8, 8))
            cb = float(np.clip(min(max(mb, 11.0), 28.0) - mb, -8, 8))
            aa = aa + 0.6 * f * ca * pele; bb = bb + 0.6 * f * cb * pele
            C2, h = np.hypot(aa, bb), np.degrees(np.arctan2(bb, aa))
    if verde_citrico:                                            # lavoura, mata, pasto: verde mais cítrico
        vd = banda_h(hh, 130, 30) * suave(C, 4, 10) * (1 - pele)
        h = h - f * 7.0 * vd
        C2 = C2 * (1 + f * 0.12 * vd)
    C2 = np.minimum(C2, C * 1.75 + 4)
    a, b = C2 * np.cos(np.radians(h)), C2 * np.sin(np.radians(h))

    out = gamut_ok(np.dstack([L, a, b]).astype(np.float32))

    # ---- 5. nitidez (no L, com limiar para não realçar ruído) ----
    lab3 = to_lab(out)
    Lx = lab3[..., 0]
    sig = float(np.clip(0.7 * max(Hh, Ww) / 1600, 0.6, 1.6))
    hp = Lx - cv2.GaussianBlur(Lx, (0, 0), sig)
    falta_nit = float(np.clip((9.0 - antes['nitidez']) / 6.0, 0.35, 1.0))
    if not livre('nitidez') or antes['halo'] >= M['halo']:
        falta_nit = 0.0
    elif antes['halo'] > M['halo'] - 0.2:
        falta_nit *= (M['halo'] - antes['halo']) / 0.2
    aj['nitidez'] = round(falta_nit, 2)
    thr = suave(np.abs(hp), 0.4, 1.4)
    Lx = Lx + f * P['nitidez'] * falta_nit * hp * thr * (1 - 0.5 * pele) * 1.3
    lab3[..., 0] = np.clip(Lx, 0, 100)
    out8 = (np.clip(from_lab(lab3), 0, 1) * 255 + 0.5).astype(np.uint8)
    # trava final: mudança total abaixo do perceptível, a foto fica como veio
    pq = lambda x: cv2.resize(x, (max(4, int(x.shape[1] * min(1, 800 / max(x.shape[:2])))), max(4, int(x.shape[0] * min(1, 800 / max(x.shape[:2]))))), interpolation=cv2.INTER_AREA)
    mud = float(np.sqrt(((to_lab(pq(bgr8).astype(np.float32) / 255) - to_lab(pq(out8).astype(np.float32) / 255)) ** 2).sum(-1)).mean())
    if mud < LIMIAR_MUDANCA:
        return bgr8, dict(tipo=tipo, decisao='mantida', motivo='já está no padrão' if not feitos else 'tratamento prévio respeitado',
                          ajustes={}, mudanca=round(mud, 2), ceu=ceu_modo, rostos=len(faces), previo=previo or None,
                          antes=_r(antes), depois=_r(antes))
    depois = medir(to_lab(out8.astype(np.float32) / 255))
    return out8, dict(tipo=tipo, decisao='tratada', ceu=ceu_modo, rostos=len(faces), previo=previo or None,
                      ajustes={k: round(v, 2) for k, v in aj.items() if v >= 0.05}, mudanca=round(mud, 2),
                      antes=_r(antes), depois=_r(depois))


def _r(d):
    return {k: round(v, 3 if k in ('sombra', 'estouro') else 1) for k, v in d.items()}


# ---------------------------------------------------------------- marca de foto tratada
VERSAO = '1.1'
NS = 'https://nexteditorial.com.br/ns/foto/1.0/'
SUF_TRATADA, SUF_MANTIDA = '-nxt1', '-nxm1'
LADO_MAX = 5000   # 42 cm a 300 dpi; acima disso a memória do ambiente não aguenta


# ---------------------------------------------------------------- marca invisível (nos pixels)
# Padrão pseudoaleatório de baixa amplitude (cerca de 1 ponto de L) espalhado pela foto inteira.
# Sobrevive a redução de tamanho, JPEG, WebP, WordPress e WhatsApp; some só com recorte forte.
GRADE_MARCA = 160
LIMIAR_Z = 5.0           # foto sem marca dá z < 3; com marca, z > 6 mesmo em miniatura de 500 px
_PADRAO = np.random.default_rng(20261125).standard_normal((GRADE_MARCA, GRADE_MARCA)).astype(np.float32)


def _grade(h, w):
    return (max(16, round(GRADE_MARCA * h / w)), GRADE_MARCA) if w >= h else (GRADE_MARCA, max(16, round(GRADE_MARCA * w / h)))


def _passa_alta(x, s=1.5):
    return x - cv2.GaussianBlur(x, (0, 0), s)


def _padrao(gh, gw):
    p = _passa_alta(_PADRAO[:gh, :gw]); p = p / p.std()
    return np.clip(p, -2.2, 2.2).astype(np.float32)


def aplicar_marca_invisivel(bgr8, amp=1.35):
    h, w = bgr8.shape[:2]; gh, gw = _grade(h, w)
    pat = cv2.resize(_padrao(gh, gw), (w, h), interpolation=cv2.INTER_CUBIC)
    lab = to_lab(bgr8.astype(np.float32) / 255); L = lab[..., 0]
    tex = cv2.GaussianBlur(np.abs(_passa_alta(L, 2.0)), (0, 0), 4)       # mais forte na textura, fraca no liso
    A = amp * (0.45 + 0.55 * np.clip(tex / 3.0, 0, 1)) * np.clip(np.minimum(L, 100 - L) / 8, 0, 1)
    lab[..., 0] = np.clip(L + A * pat, 0, 100)
    return (np.clip(from_lab(lab), 0, 1) * 255 + 0.5).astype(np.uint8)


def ler_marca_invisivel(bgr8):
    """Devolve o z da marca invisível (>= LIMIAR_Z: a foto passou por esta skill)."""
    h, w = bgr8.shape[:2]
    if max(h, w) > 2000:
        e = 2000 / max(h, w); bgr8 = cv2.resize(bgr8, (int(w * e), int(h * e)), interpolation=cv2.INTER_AREA); h, w = bgr8.shape[:2]
    gh, gw = _grade(h, w)
    L = to_lab(bgr8.astype(np.float32) / 255)[..., 0]
    z = -1e9
    for d in (0, -1, 1):                                        # arredondamento da grade
        g = cv2.resize(L, (gw, gh + d) if w >= h else (gw + d, gh), interpolation=cv2.INTER_AREA)
        g = _passa_alta(g)[:gh, :gw]
        p = _padrao(*g.shape)
        z = max(z, float((g * p).sum() / (np.linalg.norm(g) * np.linalg.norm(p) + 1e-6) * np.sqrt(g.size)))
    return z


# ---------------------------------------------------------------- tratamento feito fora desta skill
_EDITORES_APP = ('snapseed', 'vsco', 'picsart', 'canva', 'instagram', 'meitu', 'photoshop express', 'adobe express',
                 'fotor', 'polarr', 'photodirector', 'afterlight', 'facetune', 'remini', 'gimp', 'affinity', 'pixelmator',
                 'lightroom mobile', 'picmonkey', 'befunky', 'pixlr', 'inshot', 'capcut', 'photoroom')
_REVELADORES = ('capture one', 'dxo', 'darktable', 'rawtherapee', 'on1', 'luminar', 'silkypix', 'digital photo professional',
                'imaging edge', 'nx studio', 'acdsee')
_CELULARES = ('apple', 'samsung', 'xiaomi', 'motorola', 'google', 'huawei', 'oppo', 'vivo', 'realme', 'oneplus', 'honor', 'nothing')
ORIGENS = {'site': 2, 'revista': 2, 'instagram': 2, 'redes': 2, 'agencia': 1, 'google': 1, 'prefeitura': 1,
           'nxfotos': 0, 'camera': 0, 'desconhecida': 0}


def _crs(xmp):
    """Lê os ajustes do Lightroom / Camera Raw gravados no XMP e diz o que o fotógrafo já fez."""
    import re
    v = dict(re.findall(r'crs:(\w+)="([^"]*)"', xmp)); v.update(dict(re.findall(r'<crs:(\w+)>([^<]*)</crs:\1>', xmp)))
    if v.get('HasSettings', '').lower() != 'true':
        return set(), []
    def n(k):
        try:
            return float(v.get(k, '0').replace('+', '') or 0)
        except ValueError:
            return 0.0
    feitos, motivos = set(), []
    luz = [k for k, lim in (('Exposure2012', 0.15), ('Contrast2012', 10), ('Highlights2012', 10), ('Shadows2012', 10),
                            ('Whites2012', 10), ('Blacks2012', 10), ('Dehaze', 10), ('ParametricShadows', 10),
                            ('ParametricDarks', 10), ('ParametricLights', 10), ('ParametricHighlights', 10)) if abs(n(k)) >= lim]
    if v.get('ToneCurveName2012', 'Linear') not in ('Linear', 'Medium Contrast', ''):
        luz.append('curva')
    cor = [k for k, lim in (('Vibrance', 10), ('Saturation', 10)) if abs(n(k)) >= lim]
    cor += [k for k in v if re.match(r'(Hue|Saturation|Luminance)Adjustment\w+', k) and abs(n(k)) >= 10]
    cor += [k for k in v if re.match(r'(ColorGrade\w*Sat|SplitToning\w*Saturation)$', k) and n(k) >= 5]
    look = v.get('LookName', '') or ' '.join(re.findall(r'<crs:Look>\s*<rdf:Description[^>]*crs:Name="([^"]*)"', xmp))
    criativo = ('Vivid', 'Landscape', 'Portrait', 'Artistic', 'Vintage', 'Modern', 'B&W', 'Monochrome', 'Matte', 'Cinematic')
    for perfil in (look, v.get('CameraProfile', '')):
        if any(c.lower() in perfil.lower() for c in criativo):   # Adobe Color / Standard / Camera Neutral são padrão
            cor.append('perfil ' + perfil)
    det = [k for k, lim in (('Clarity2012', 10), ('Texture', 10)) if abs(n(k)) >= lim] + (['Sharpness'] if n('Sharpness') >= 60 else [])
    local = bool(re.search(r'<crs:(MaskGroupBasedCorrections|GradientBasedCorrections|CircularGradientBasedCorrections|PaintBasedCorrections)>\s*<rdf:Seq>\s*<rdf:li', xmp))
    if luz:
        feitos.add('luz'); motivos.append('luz (' + ', '.join(luz[:4]) + ')')
    if cor:
        feitos |= {'cor', 'ceu'}; motivos.append('cor (' + ', '.join(cor[:4]) + ')')
    if v.get('WhiteBalance', 'As Shot') not in ('As Shot', ''):
        feitos.add('balanco'); motivos.append('balanço de branco ' + v.get('WhiteBalance'))
    if det:
        feitos.add('nitidez'); motivos.append('nitidez (' + ', '.join(det) + ')')
    if local:
        feitos |= {'luz', 'ceu'}; motivos.append('ajustes locais (máscaras)')
    return feitos, motivos


def detectar_previo(caminho, origem='desconhecida', palavras=''):
    """Procura sinais de que a foto já foi tratada fora desta skill. Devolve dict(nivel, feitos, motivos):
    nivel 3 = já tratada pela casa (não mexe); 2 = editada fora sem detalhe (só defeito grosseiro);
    1 = parte já feita (os grupos em 'feitos' ficam de fora); 0 = sem sinal."""
    import re
    from PIL import Image
    nivel, feitos, motivos = 0, set(), []
    nome = os.path.splitext(os.path.basename(caminho))[0].lower()
    if re.search(r'-(nx|google|instagram|parceiro|guia)-\d+-t\d{1,2}$', nome):
        return dict(nivel=3, feitos=list(GRUPOS), motivos=['marca antiga dos mapas do Destinos ES (t{k} no nome)'])
    kw = (palavras or '').lower()
    if 'tratada-nx-v' in kw or 'mantida-nx-v' in kw:
        return dict(nivel=3, feitos=list(GRUPOS), motivos=['palavra-chave do NX Fotos (tratada-nx / mantida-nx)'])
    o = ORIGENS.get((origem or 'desconhecida').lower(), 0)
    if o:
        nivel = max(nivel, o); motivos.append(f'origem: {origem}')
        if o == 1:
            feitos.add('nitidez')
    try:
        im = Image.open(caminho)
        ex = im.getexif()
        sw = ' '.join(str(ex.get(t, '')) for t in (0x0131, 0x010F, 0x0110)).lower()
        make = str(ex.get(0x010F, '')).lower()
        xmp = im.info.get('xmp') or b''
        xmp = xmp.decode('utf-8', 'ignore') if isinstance(xmp, bytes) else str(xmp)
    except Exception:
        return dict(nivel=nivel, feitos=sorted(feitos), motivos=motivos + ['não deu para ler os metadados'])
    ferr = ' '.join(re.findall(r'(?:CreatorTool|softwareAgent)[=>"\']+([^"<\']+)', xmp)).lower() + ' ' + sw
    f2, m2 = _crs(xmp)
    if f2:
        feitos |= f2; motivos += ['Lightroom/Camera Raw: ' + m for m in m2]
        nivel = max(nivel, 2 if ({'luz', 'cor'} <= f2) else 1)
    if 'photoshop' in ferr and not any(t in ferr for t in ('lightroom', 'camera raw', 'photoshop express')) \
            and ('photoshop:History' in xmp or 'stEvt:action="saved"' in xmp or 'photoshop' in sw):
        nivel = max(nivel, 2); motivos.append('editada no Photoshop')
    app = next((a for a in _EDITORES_APP if a in ferr), None)
    if app:
        nivel = max(nivel, 2); motivos.append(f'editada no app {app}')
    rev = next((r for r in _REVELADORES if r in ferr), None)
    if rev:
        feitos |= {'luz', 'balanco', 'nitidez'}; nivel = max(nivel, 1); motivos.append(f'revelada no {rev}')
    if any(c in make for c in _CELULARES):
        motivos.append('foto de celular (já sai com nitidez e cor do aparelho; a nitidez é medida na foto)')
    elif not make and not f2 and not app and not rev:
        motivos.append('sem dados de câmera (arquivo reprocessado ou de outra fonte)')
    return dict(nivel=nivel, feitos=sorted(feitos), motivos=motivos)


def ler_marca(caminho):
    """Diz se o arquivo já passou por esta skill (XMP nx:Tratamento, EXIF Software, comentário
    JPEG ou sufixo -nxt1/-nxm1 no nome). Devolve dict ou None."""
    from PIL import Image
    nome = os.path.splitext(os.path.basename(caminho))[0].lower()
    achou = {}
    for suf in (SUF_TRATADA, SUF_MANTIDA):
        if nome.endswith(suf) or (suf + '-') in nome:
            achou['nome'] = suf
    try:
        im = Image.open(caminho)
        xmp = im.info.get('xmp') or b''
        if isinstance(xmp, str):
            xmp = xmp.encode('utf-8', 'ignore')
        if b'nx:Tratamento' in xmp:
            achou['xmp'] = True
            for campo in (b'nx:Versao', b'nx:Tipo', b'nx:Decisao', b'nx:Data'):
                k = xmp.find(campo + b'="')
                if k >= 0:
                    v = xmp[k + len(campo) + 2:xmp.find(b'"', k + len(campo) + 2)]
                    achou[campo.decode()[3:].lower()] = v.decode('utf-8', 'ignore')
        sw = im.getexif().get(0x0131)
        if sw and 'tratamento-fotos-next' in str(sw):
            achou['exif'] = str(sw)
        com = im.info.get('comment')
        if com and b'nx-tratada' in (com if isinstance(com, bytes) else str(com).encode()):
            achou['comentario'] = True
    except Exception:
        pass
    return achou or None


def _xmp(info, data):
    aj = ' '.join(f'{k}:{v}' for k, v in info.get('ajustes', {}).items())
    pv = info.get('previo') or {}
    prev = '; '.join(pv.get('motivos', [])).replace('"', "'") if pv.get('nivel') else ''
    return ('<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
            f'<rdf:Description rdf:about="" xmlns:nx="{NS}" nx:Tratamento="tratamento-fotos-next" '
            f'nx:Versao="{VERSAO}" nx:Tipo="{info.get("tipo", "")}" nx:Decisao="{info.get("decisao", "")}" '
            f'nx:Ceu="{info.get("ceu", "")}" nx:Ajustes="{aj}" nx:Previo="{prev}" nx:MarcaInvisivel="sim" nx:Data="{data}"/>'
            '</rdf:RDF></x:xmpmeta><?xpacket end="w"?>').encode('utf-8')


def abrir_srgb(caminho):
    """Abre a foto na orientação certa e em sRGB (converte Adobe RGB, Display P3, CMYK)."""
    from PIL import Image, ImageOps, ImageCms
    import io
    try:
        import pillow_heif; pillow_heif.register_heif_opener()   # fotos de iPhone (HEIC)
    except Exception:
        pass
    im = Image.open(caminho)
    exif = im.getexif()
    im = ImageOps.exif_transpose(im)
    icc = im.info.get('icc_profile')
    try:
        if im.mode == 'CMYK':
            fogra = '/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc'
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc)) if icc else (ImageCms.getOpenProfile(fogra) if os.path.exists(fogra) else None)
            im = ImageCms.profileToProfile(im, src, ImageCms.createProfile('sRGB'), outputMode='RGB') if src else im.convert('RGB')
        elif icc:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            if 'srgb' not in (ImageCms.getProfileDescription(src) or '').lower():
                im = ImageCms.profileToProfile(im.convert('RGB'), src, ImageCms.createProfile('sRGB'), outputMode='RGB')
    except Exception:
        pass
    im = im.convert('RGB')
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR), exif


def salvar_marcado(bgr8, exif, saida, info, qualidade=90):
    from PIL import Image, ImageCms
    import datetime
    data = datetime.date.today().isoformat()
    im = Image.fromarray(cv2.cvtColor(aplicar_marca_invisivel(bgr8), cv2.COLOR_BGR2RGB))
    exif[0x0112] = 1                                            # já está na orientação certa
    exif[0x0131] = f'tratamento-fotos-next {VERSAO} ({info.get("tipo", "")}, {info.get("decisao", "")})'
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    im.save(saida, 'JPEG', quality=qualidade, subsampling=0, optimize=True, exif=exif.tobytes(),
            icc_profile=srgb, xmp=_xmp(info, data),
            comment=f'nx-tratada {VERSAO} {info.get("tipo", "")} {info.get("decisao", "")} {data}'.encode())


def nome_marcado(saida, decisao):
    base, ext = os.path.splitext(saida)
    for suf in (SUF_TRATADA, SUF_MANTIDA):
        if base.endswith(suf):
            base = base[:-len(suf)]
    return base + (SUF_MANTIDA if decisao == 'mantida' else SUF_TRATADA) + (ext or '.jpg')


def processar(entrada, saida, tipo='auto', marca='esbrasil', forca=1.0, largura=0, qualidade=90,
              sufixo=False, forcar=False, verde_citrico=False, origem='desconhecida', palavras=''):
    m = ler_marca(entrada)
    if m and not forcar:
        return dict(arquivo=entrada, decisao='ja_tratada', marca=m)
    prev = detectar_previo(entrada, origem, palavras)
    if prev['nivel'] >= 3 and not forcar:
        return dict(arquivo=entrada, decisao='ja_tratada', marca=dict(antiga=prev['motivos']))
    bgr, exif = abrir_srgb(entrada)
    z = ler_marca_invisivel(bgr)
    if z >= LIMIAR_Z and not forcar:
        return dict(arquivo=entrada, decisao='ja_tratada', marca=dict(invisivel=round(z, 1)))
    if forcar:
        prev = dict(nivel=0, feitos=[], motivos=[])
    if largura and bgr.shape[1] > largura:                     # reduz antes: rápido e nitidez na escala final
        s = largura / bgr.shape[1]
        bgr = cv2.resize(bgr, (largura, int(bgr.shape[0] * s)), interpolation=cv2.INTER_AREA)
    if max(bgr.shape[:2]) > LADO_MAX:                          # teto de memória: 5.000 px = 42 cm a 300 dpi
        s = LADO_MAX / max(bgr.shape[:2])
        bgr = cv2.resize(bgr, (int(bgr.shape[1] * s), int(bgr.shape[0] * s)), interpolation=cv2.INTER_AREA)
    out, info = tratar(bgr, tipo, marca, forca, verde_citrico, previo=prev if (prev['nivel'] or prev['motivos']) else None)
    if sufixo:
        saida = nome_marcado(saida, info['decisao'])
    salvar_marcado(out, exif, saida, info, qualidade)
    info['arquivo'] = saida
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada', help='foto ou pasta (lote)')
    ap.add_argument('saida', nargs='?', help='foto ou pasta de saída')
    ap.add_argument('--tipo', default='auto', choices=['auto', 'turismo', 'pessoas', 'editorial'])
    ap.add_argument('--marca', default='esbrasil', choices=['esbrasil', 'destinos', 'comunhao'])
    ap.add_argument('--forca', type=float, default=1.0)
    ap.add_argument('--largura', type=int, default=0, help='largura máxima da saída (0 = resolução cheia)')
    ap.add_argument('--qualidade', type=int, default=90)
    ap.add_argument('--sufixo', action='store_true', help='põe -nxt1 (tratada) ou -nxm1 (mantida) no nome')
    ap.add_argument('--forcar', action='store_true', help='trata mesmo se a foto já tiver a marca')
    ap.add_argument('--verificar', action='store_true', help='só diz se a foto já passou por esta skill')
    ap.add_argument('--verde-citrico', action='store_true', help='verde de lavoura, mata e pasto mais cítrico')
    ap.add_argument('--origem', default='desconhecida', choices=sorted(ORIGENS),
                    help='de onde a foto veio: site/revista/instagram = já publicada (só defeito grosseiro)')
    ap.add_argument('--palavras', default='', help='palavras-chave do NX Fotos (acha tratada-nx-v1 / mantida-nx-v1)')
    x = ap.parse_args()
    if x.verificar:
        alvos = [os.path.join(x.entrada, f) for f in sorted(os.listdir(x.entrada))] if os.path.isdir(x.entrada) else [x.entrada]
        for a in alvos:
            if not a.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif')):
                continue
            mk = ler_marca(a) or {}
            try:
                z = round(ler_marca_invisivel(abrir_srgb(a)[0]), 1)
            except Exception:
                z = None
            if z is not None and z >= LIMIAR_Z:
                mk['invisivel'] = z
            pv = detectar_previo(a, x.origem, x.palavras)
            print(json.dumps({'arquivo': a, 'tratada': bool(mk) or pv['nivel'] >= 3, 'marca': mk or None,
                              'z_invisivel': z, 'previo': pv}, ensure_ascii=False))
        return
    if os.path.isdir(x.entrada):
        os.makedirs(x.saida, exist_ok=True)
        for f in sorted(os.listdir(x.entrada)):
            if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif')):
                continue
            nome = os.path.splitext(f)[0] + '.jpg'
            try:
                info = processar(os.path.join(x.entrada, f), os.path.join(x.saida, nome), x.tipo, x.marca,
                                 x.forca, x.largura, x.qualidade, True, x.forcar, x.verde_citrico, x.origem, x.palavras)
            except Exception as e:
                info = dict(arquivo=f, decisao='erro', erro=str(e)[:200])
            print(json.dumps(info, ensure_ascii=False))
        return
    if not x.saida:
        sys.exit('informe a saída')
    print(json.dumps(processar(x.entrada, x.saida, x.tipo, x.marca, x.forca, x.largura, x.qualidade,
                               x.sufixo, x.forcar, x.verde_citrico, x.origem, x.palavras), ensure_ascii=False))


if __name__ == '__main__':
    main()
```

## 10. Decisões do Mário Fernando

- **11/11/2026:** foto crua é tratada no padrão das revistas impressas, mais viva, um pouco mais cítrica e quente, com azuis mais quentes. Foto já tratada e boa não é mexida.
- **25/11/2026:** calibragem nas publicações da casa, com o livro Destinos ES e a **revista ES Brasil** como referências principais. O automático foi o resultado mais próximo do verdadeiro nos testes.
- **25/11/2026:** padrões separados para turismo e pessoas (e editorial para o resto). O céu é reforçado quando precisa, e brilho, contraste, nitidez e sombras são medidos foto a foto.
- **25/11/2026:** a nitidez foi reduzida, porque o reforço tinha exagerado nas fotos de turismo.
- **25/11/2026:** toda foto tratada leva a marca da seção 4. O Mário Fernando vai incorporar esta skill ao NX Fotos, e foto baixada de lá com a marca já chega pré-tratada.
- **25/11/2026:** esta skill fica separada e entra em todas as skills que usam foto (seção 8).
- **25/11/2026:** foto já tratada não pode ser estragada por um segundo tratamento. A versão 1.1 acrescenta a marca invisível, lê o que foi feito fora (Lightroom, Photoshop, apps, celular, origem) e só põe o estilo da casa em foto que ainda não chegou à meta (seção 5). As 18 fotos do teste receberam a marca invisível sem mudar o tratamento aprovado.