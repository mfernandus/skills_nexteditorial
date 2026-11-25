#!/usr/bin/env python3
"""Foto do articulista no padrão dos artigos da Retrospectiva 2026 (revista ES Brasil).

Uso:
    python3 tratar_foto.py ENTRADA PASTA_SAIDA --nome sobrenome-nome [--credito "Foto: ..."]
                           [--quadro 39.7x54.8] [--perfil-cmyk FOGRA39.icc] [--forca-cor 0.8]

ENTRADA pode ser PSD/PSB (usa a composição visível; camadas ocultas, como as geradas por IA, ficam de fora),
JPG ou TIFF em CMYK com perfil ICC, ou RGB. O script:

1. converte para sRGB pelo perfil embutido (CMYK do PSD vem invertido e é corrigido);
2. recorta a pessoa na foto inteira (rembg, isnet-general-use): cabelo e barba com borda macia para dentro,
   roupa com borda firme e nenhum furo dentro da pessoa;
3. corrige a cor sem mexer no tom da pele: tira a dominante só dos tons quase cinza (cabelo, barba, camisa
   clara), leva a luz e a saturação da pele para perto do modelo (limites de ±8% e -15%) e tira um pouco de
   magenta em Lab (só o a* positivo, --menos-magenta, padrão 2,5), sem amarelar; nada de níveis fortes;
4. troca o fundo pelo fundo de estúdio cinza-claro quente medido na foto do Sidemar Acosta (ES 238, p. 28),
   por C = I + (1 - alfa) * (fundo novo - fundo antigo), que tira a franja escura dos fios;
5. enquadra a cabeça no PADRÃO (medido no mesmo modelo): topo do cabelo a 3,0% da altura do quadro,
   cabeça (topo do cabelo ao queixo) com 72,1% da altura, linha dos olhos a 41,5% e centro da cabeça (na linha dos olhos) a 49%
   da largura. Assim todas as cabeças dos artigos ficam do mesmo tamanho na revista;
6. grava: <nome>.tif (CMYK, perfil de impressão embutido, para o InDesign), <nome>-rgb.jpg (prova),
   <nome>-recorte.png (pessoa sem fundo, para a diagramação trocar o fundo se quiser) e <nome>.json
   (medidas, resolução efetiva e avisos).

Quadro padrão do artigo: 39,7 x 54,8 mm (112,6 x 155,4 pt), cantos arredondados de 1,4 mm no InDesign.
Resolução mínima: 300 ppi no quadro (cerca de 470 x 650 px). Abaixo disso, o script avisa e não amplia.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms, ImageFilter

# Padrão medido na foto do modelo (Sidemar Acosta, ES 238, 478 x 657 px no quadro de 39,7 x 54,8 mm)
PADRAO = {"topo": 0.030, "cabeca": 0.721, "olhos_y": 0.415, "olhos_x": 0.450, "cabeca_x": 0.490}
QUADRO_MM = (39.7, 54.8)
FUNDO = {"topo": (229, 226, 226), "meio": (236, 233, 230), "base": (233, 230, 227), "brilho": (240, 236, 229)}
MODELO_ROSTO = Path.home() / ".cache" / "artigos-retrospectiva" / "face_landmarker.task"
URL_ROSTO = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
FOGRA = next((p for p in (Path("/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc"),
                          Path("/Library/ColorSync/Profiles/CoatedFOGRA39.icc"),
                          Path("/Library/Application Support/Adobe/Color/Profiles/Recommended/CoatedFOGRA39.icc"))
              if p.exists()), None)


PERFIL_ORIGEM: list[bytes] = []   # perfil CMYK da foto recebida (o da revista é o U.S. Web Coated SWOP v2)


def carregar(caminho: Path) -> tuple[Image.Image, list[str]]:
    """Abre a foto e devolve sRGB + avisos."""
    avisos = []
    srgb = ImageCms.createProfile("sRGB")
    if caminho.suffix.lower() in (".psd", ".psb"):
        from psd_tools import PSDImage
        psd = PSDImage.open(caminho)
        for l in psd.descendants():
            if not l.visible:
                avisos.append(f"camada oculta ignorada: {l.name[:90]}")
        a = psd.numpy()
        icc = psd.image_resources.get_data(1039) if psd.image_resources else None
        if icc and psd.color_mode == 4:
            PERFIL_ORIGEM.append(icc)
        if a.shape[2] >= 4 and psd.color_mode == 4:          # CMYK: o psd-tools devolve 1 - tinta
            cmyk = Image.fromarray((255 - (a[..., :4] * 255).round()).astype(np.uint8), "CMYK")
            perfil = ImageCms.ImageCmsProfile(io.BytesIO(icc)) if icc else ImageCms.ImageCmsProfile(str(FOGRA))
            return ImageCms.profileToProfile(cmyk, perfil, srgb, renderingIntent=1, outputMode="RGB"), avisos
        return Image.fromarray((a[..., :3] * 255).round().astype(np.uint8), "RGB"), avisos
    im = Image.open(caminho)
    icc = im.info.get("icc_profile")
    if im.mode == "CMYK":
        if icc:
            PERFIL_ORIGEM.append(icc)
        perfil = ImageCms.ImageCmsProfile(io.BytesIO(icc)) if icc else ImageCms.ImageCmsProfile(str(FOGRA))
        return ImageCms.profileToProfile(im, perfil, srgb, renderingIntent=1, outputMode="RGB"), avisos
    if icc:
        try:
            return ImageCms.profileToProfile(im.convert("RGB"), ImageCms.ImageCmsProfile(io.BytesIO(icc)), srgb,
                                             renderingIntent=1, outputMode="RGB"), avisos
        except Exception:
            pass
    return im.convert("RGB"), avisos


def marcos_do_rosto(im: Image.Image) -> dict:
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions, vision
    if not MODELO_ROSTO.exists():
        MODELO_ROSTO.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL_ROSTO, MODELO_ROSTO)
    det = vision.FaceLandmarker.create_from_options(
        vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=str(MODELO_ROSTO)), num_faces=1))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(np.asarray(im))))
    det.close()
    if not r.face_landmarks:
        sys.exit("FALHA: nenhum rosto encontrado na foto")
    W, H = im.size
    L = r.face_landmarks[0]
    P = lambda i: np.array([L[i].x * W, L[i].y * H])
    olhos = (P(468) + P(473)) / 2
    bochechas = [P(i) for i in (50, 280, 187, 411, 205, 425)]
    return {"olhos": olhos, "queixo": P(152), "testa": P(10), "bochechas": bochechas,
            "rosto_x": (min(p.x for p in L) * W, max(p.x for p in L) * W)}


def mascara(im: Image.Image) -> np.ndarray:
    """Máscara suave da pessoa (rembg isnet-general-use) na foto inteira, 0..1. Na foto inteira: no recorte
    parcial, paletó escuro sobre fundo escuro vira fundo."""
    from rembg import new_session, remove
    s = new_session("isnet-general-use")
    return np.asarray(remove(im, session=s, only_mask=True), np.float32) / 255


def _degrau(m: np.ndarray, a: float, b: float) -> np.ndarray:
    t = np.clip((m - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def alfa_final(m: np.ndarray, queixo_y: float, cabeca: float) -> np.ndarray:
    """Cabelo com borda suave (fios); roupa com borda firme; sem furos dentro da pessoa."""
    from scipy import ndimage
    H = m.shape[0]
    y = np.arange(H, dtype=np.float32)[:, None]
    w = np.clip((queixo_y + 0.12 * cabeca - y) / (0.12 * cabeca), 0, 1)        # 1 na cabeça, 0 abaixo do pescoço
    cab = _degrau(m, 0.06, 0.94)
    suave = ndimage.gaussian_filter(cab, 1.6)
    cab = np.minimum(cab, suave * 1.04)              # borda do cabelo e da barba macia, para dentro (sem halo escuro)
    corpo = np.asarray(Image.fromarray((_degrau(m, 0.40, 0.60) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),
                       np.float32) / 255
    a = w * cab + (1 - w) * corpo
    cheio = ndimage.binary_fill_holes(a > 0.5)
    miolo = ndimage.binary_erosion(cheio, iterations=4)
    a[miolo] = 1.0                                     # tapa furos e transparências dentro da pessoa
    return np.clip(a, 0, 1)


def fundo_original(rgb: np.ndarray, m: np.ndarray, raio: float = 18) -> np.ndarray:
    """Estimativa do fundo antigo atrás das bordas (média local só dos pixels de fundo)."""
    from scipy import ndimage
    bg = (m < 0.03).astype(np.float32)
    num = np.stack([ndimage.gaussian_filter(rgb[..., c].astype(np.float32) * bg, raio) for c in range(3)], -1)
    den = ndimage.gaussian_filter(bg, raio)[..., None]
    est = num / np.maximum(den, 1e-4)
    falta = den[..., 0] < 0.02
    if falta.any():                                     # longe do fundo: cor média do fundo
        est[falta] = rgb[m < 0.03].mean(0) if (m < 0.03).any() else 0
    return est


def tirar_pontos(rgb: np.ndarray) -> np.ndarray:
    """Retoque de poeira: pontos claros isolados em áreas escuras (paletó, fundo) somem pela mediana local."""
    im = Image.fromarray(rgb)
    med = np.asarray(im.filter(ImageFilter.MedianFilter(5)), np.float32)
    x = rgb.astype(np.float32)
    lum = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lmed = med @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    ponto = (lum - lmed > 38) & (lmed < 70)
    ponto = np.asarray(Image.fromarray((ponto * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
    x[ponto] = med[ponto]
    return x.round().astype(np.uint8)


PELE_ALVO = {"lum": 0.68, "sat": 0.70}     # pele medida na foto do modelo (matiz 17°, sat 0,69, lum 0,67)


def corrigir_cor(rgb: np.ndarray, m: np.ndarray, marcos: dict, forca: float, menos_magenta: float = 2.5) -> tuple[np.ndarray, dict]:
    """Correção conservadora, sem mudar o tom da pele:
    1. tira a dominante só dos tons neutros (cabelo, barba, camisa clara), pesando pela saturação;
    2. leva a luminância e a saturação da pele para perto do modelo (limites de ±8% e -15%);
    3. nada de níveis agressivos nem curva forte (foto de estúdio, contraste suave)."""
    import colorsys
    x = rgb.astype(np.float32) / 255
    H, W = m.shape
    lum = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    mx, mn = x.max(2), x.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-4)
    yy, xx = np.mgrid[0:H, 0:W]
    ox, oy = marcos["olhos"]
    lado = (marcos["rosto_x"][1] - marcos["rosto_x"][0])
    perto = (np.abs(xx - ox) < lado * 0.9) & (yy > marcos["testa"][1] - lado * 0.9) & (yy < marcos["queixo"][1] + lado * 0.25)
    neutro = (m > 0.95) & perto & (sat < 0.12) & (lum > 0.30) & (lum < 0.95)
    info = {"pixels_neutros": int(neutro.sum())}
    if neutro.sum() > 500:
        med = x[neutro].mean(0)
        ganho = med.mean() / np.maximum(med, 1e-4)
        peso = np.clip(1 - sat / 0.20, 0, 1)[..., None] * forca          # só o que é quase cinza
        x = x * (1 + (ganho - 1) * peso)
        info["dominante_neutros_rgb"] = [round(float(v) * 255, 1) for v in med]
    # pele: amostras nas bochechas
    r = max(3, int(lado * 0.04))
    amostras = np.concatenate([x[int(p[1]) - r:int(p[1]) + r, int(p[0]) - r:int(p[0]) + r].reshape(-1, 3)
                               for p in marcos["bochechas"]])
    mu = amostras.mean(0)
    h, l, s = (float(v) for v in colorsys.rgb_to_hls(*(float(c) for c in mu)))
    fl = float(np.clip(PELE_ALVO["lum"] / max(l, 1e-3), 0.92, 1.08))
    fs = float(np.clip(PELE_ALVO["sat"] / max(s, 1e-3), 0.85, 1.0))
    x = np.clip(x * fl, 0, 1)
    cinza = (x @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    x = cinza + (x - cinza) * fs
    info.update({"pele_antes": {"matiz": round(h * 360, 1), "sat": round(s, 2), "lum": round(l, 2)},
                 "fator_luz": round(fl, 3), "fator_saturacao": round(fs, 3)})
    mu2 = np.concatenate([x[int(p[1]) - r:int(p[1]) + r, int(p[0]) - r:int(p[0]) + r].reshape(-1, 3)
                          for p in marcos["bochechas"]]).mean(0)
    h2, l2, s2 = (float(v) for v in colorsys.rgb_to_hls(*(float(c) for c in np.clip(mu2, 0, 1))))
    info["pele_depois"] = {"matiz": round(h2 * 360, 1), "sat": round(s2, 2), "lum": round(l2, 2)}
    saida = (np.clip(x, 0, 1) * 255).round().astype(np.uint8)
    if menos_magenta > 0:
        saida = tirar_magenta(saida, menos_magenta)
        info["menos_magenta_a"] = menos_magenta
    return saida, info


def tirar_magenta(rgb: np.ndarray, k: float) -> np.ndarray:
    """Tira um pouco de magenta sem amarelar: em Lab, reduz só o a* positivo (magenta/vermelho) em até k
    unidades; o b* (amarelo) fica igual. Tons neutros e verdes quase não mudam."""
    srgb, lab = ImageCms.createProfile("sRGB"), ImageCms.createProfile("LAB")
    ida = ImageCms.buildTransformFromOpenProfiles(srgb, lab, "RGB", "LAB")
    volta = ImageCms.buildTransformFromOpenProfiles(lab, srgb, "LAB", "RGB")
    L = np.array(ImageCms.applyTransform(Image.fromarray(rgb), ida))
    a = L[..., 1].view(np.int8).astype(np.float32)
    a = a - k * np.clip(a / 5.0, 0, 1)
    L[..., 1] = np.clip(np.round(a), -128, 127).astype(np.int8).view(np.uint8)
    return np.asarray(ImageCms.applyTransform(Image.fromarray(L, "LAB"), volta))


def fundo(W: int, H: int, centro: tuple[float, float]) -> np.ndarray:
    t, mi, b = (np.array(FUNDO[k], np.float32) for k in ("topo", "meio", "base"))
    grad = np.empty((H, 1, 3), np.float32)
    for c in range(3):
        grad[:, 0, c] = np.interp(np.linspace(0, 1, H), [0, 0.5, 1], [t[c], mi[c], b[c]])
    img = np.repeat(grad, W, axis=1)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - centro[0]) / (W * 0.55)) ** 2 + ((yy - centro[1]) / (H * 0.45)) ** 2)
    brilho = np.clip(1 - d, 0, 1)[..., None] ** 2 * 0.35
    img = img * (1 - brilho) + np.array(FUNDO["brilho"], np.float32) * brilho
    rng = np.random.default_rng(7)
    img += rng.normal(0, 0.9, img.shape)          # grão leve: evita faixas no impresso
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--nome", required=True)
    ap.add_argument("--credito", default="")
    ap.add_argument("--quadro", default=f"{QUADRO_MM[0]}x{QUADRO_MM[1]}")
    ap.add_argument("--perfil-cmyk", default=None,
                    help="perfil ICC de saída; padrão: o CMYK da foto recebida (SWOP v2, o mesmo da base da revista) ou FOGRA39")
    ap.add_argument("--forca-cor", type=float, default=0.7)
    ap.add_argument("--menos-magenta", type=float, default=2.5,
                    help="unidades de a* (Lab) tiradas do magenta da pessoa; 0 desliga")
    a = ap.parse_args()
    out = Path(a.saida); out.mkdir(parents=True, exist_ok=True)
    qw, qh = (float(v) for v in a.quadro.lower().split("x"))

    im, avisos = carregar(Path(a.entrada))
    m = marcos_do_rosto(im)
    W, H = im.size

    # máscara na foto inteira e enquadramento da cabeça no padrão
    mfull = mascara(im)
    ox, oy = int(m["olhos"][0]), int(m["olhos"][1])
    faixa = mfull[:, max(0, ox - W // 7): ox + W // 7]
    linhas = np.where(faixa.max(1) > 0.5)[0]
    topo = float(linhas[0]) if len(linhas) else m["testa"][1] - (m["queixo"][1] - m["testa"][1]) * 0.45
    cols = np.where(mfull[oy] > 0.5)[0]
    cols = cols[np.abs(cols - ox) < (m["rosto_x"][1] - m["rosto_x"][0]) * 1.2]
    centro_x = (cols.min() + cols.max()) / 2 if len(cols) else m["olhos"][0]
    cabeca = m["queixo"][1] - topo
    alt = cabeca / PADRAO["cabeca"]
    larg = alt * qw / qh
    y0 = topo - PADRAO["topo"] * alt
    x0 = centro_x - PADRAO["cabeca_x"] * larg
    caixa = [x0, y0, x0 + larg, y0 + alt]
    falta = [max(0, -caixa[0]), max(0, -caixa[1]), max(0, caixa[2] - W), max(0, caixa[3] - H)]
    if any(f > 0 for f in falta):
        avisos.append(f"a foto não cobre o quadro inteiro no padrão (faltam px esq/topo/dir/base: {[round(f) for f in falta]}); "
                      "o fundo de estúdio completa a área")
    mg = int(alt * 0.06)
    bx = [int(max(0, caixa[0] - mg)), int(max(0, caixa[1] - mg)), int(min(W, caixa[2] + mg)), int(min(H, caixa[3] + mg))]
    regiao = np.ascontiguousarray(np.asarray(im)[bx[1]:bx[3], bx[0]:bx[2]])
    mreg = mfull[bx[1]:bx[3], bx[0]:bx[2]]
    m2 = {k: (v - np.array(bx[:2]) if isinstance(v, np.ndarray) else v) for k, v in m.items()}
    m2["rosto_x"] = (m["rosto_x"][0] - bx[0], m["rosto_x"][1] - bx[0])
    m2["bochechas"] = [p - np.array(bx[:2]) for p in m["bochechas"]]
    corr, info_cor = corrigir_cor(regiao, mreg, m2, a.forca_cor, a.menos_magenta)
    corr = tirar_pontos(corr)
    alfa = alfa_final(mreg, m2["queixo"][1], cabeca)
    velho = fundo_original(corr, mreg)

    # composição sobre o fundo de estúdio: C = I + (1 - alfa) * (fundo novo - fundo antigo).
    # Troca o fundo sem franja escura nos fios (o fundo antigo misturado na borda sai junto).
    Wc, Hc = int(round(larg)), int(round(alt))
    fundo_img = fundo(Wc, Hc, (PADRAO["cabeca_x"] * Wc, PADRAO["olhos_y"] * Hc))
    final = fundo_img.copy()
    lay_a = np.zeros((Hc, Wc), np.float32)
    lay_f = np.zeros((Hc, Wc, 3), np.float32)
    dx, dy = int(round(bx[0] - caixa[0])), int(round(bx[1] - caixa[1]))
    h, w = alfa.shape
    sx0, sy0 = max(0, -dx), max(0, -dy)
    tx0, ty0 = max(0, dx), max(0, dy)
    cw, ch = min(w - sx0, Wc - tx0), min(h - sy0, Hc - ty0)
    I = corr[sy0:sy0 + ch, sx0:sx0 + cw].astype(np.float32)
    A = alfa[sy0:sy0 + ch, sx0:sx0 + cw][..., None]
    B = velho[sy0:sy0 + ch, sx0:sx0 + cw]
    Bn = fundo_img[ty0:ty0 + ch, tx0:tx0 + cw]
    troca = I + (1 - A) * (Bn - B)
    so_fundo = np.clip((A - 0.02) / 0.10, 0, 1)            # fundo puro: só o fundo novo (sem emendas da parede antiga)
    final[ty0:ty0 + ch, tx0:tx0 + cw] = so_fundo * troca + (1 - so_fundo) * Bn
    lay_a[ty0:ty0 + ch, tx0:tx0 + cw] = A[..., 0]
    lay_f[ty0:ty0 + ch, tx0:tx0 + cw] = np.where(A > 0.05, (I - (1 - A) * B) / np.maximum(A, 0.05), 0)
    base_linha = ty0 + ch - 1                      # corpo cortado na base da foto continua até a borda
    if base_linha < Hc - 1 and ch > 0:
        final[base_linha + 1:] = final[base_linha]
        lay_a[base_linha + 1:] = lay_a[base_linha]
        lay_f[base_linha + 1:] = lay_f[base_linha]
    lay_fg = lay_f
    final = Image.fromarray(np.clip(final, 0, 255).round().astype(np.uint8), "RGB")
    final = final.filter(ImageFilter.UnsharpMask(radius=1.0, percent=25, threshold=3))
    ppi = Wc / (qw / 25.4)
    if ppi < 300:
        avisos.append(f"resolução efetiva de {ppi:.0f} ppi no quadro (mínimo 300): pedir foto original maior")

    nome = a.nome
    final.save(out / f"{nome}-rgb.jpg", quality=93, dpi=(ppi, ppi), icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes())
    rec = Image.fromarray(np.dstack([np.clip(lay_fg, 0, 255).round().astype(np.uint8), (lay_a * 255).round().astype(np.uint8)]), "RGBA")
    rec.save(out / f"{nome}-recorte.png", dpi=(ppi, ppi))
    prof = (ImageCms.ImageCmsProfile(a.perfil_cmyk) if a.perfil_cmyk else
            ImageCms.ImageCmsProfile(io.BytesIO(PERFIL_ORIGEM[0])) if PERFIL_ORIGEM else
            ImageCms.ImageCmsProfile(str(FOGRA)) if FOGRA else None)
    if prof:
        cmyk = ImageCms.profileToProfile(final, ImageCms.createProfile("sRGB"), prof, renderingIntent=0, outputMode="CMYK")
        cmyk.save(out / f"{nome}.tif", compression="tiff_lzw", dpi=(ppi, ppi), icc_profile=prof.tobytes())
    else:
        avisos.append("sem perfil CMYK: o TIFF sai em RGB e o InDesign converte na exportação")
        final.save(out / f"{nome}.tif", compression="tiff_lzw", dpi=(ppi, ppi))
    rel = {"arquivo": f"{nome}.tif", "perfil_cmyk": ImageCms.getProfileDescription(prof).strip() if prof else "RGB", "px": [Wc, Hc], "ppi_no_quadro": round(ppi), "quadro_mm": [qw, qh],
           "caixa_na_original": [round(v) for v in caixa], "cabeca_px": round(cabeca), "padrao": PADRAO,
           "cor": info_cor, "credito": a.credito, "avisos": avisos}
    (out / f"{nome}.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf8")
    print(json.dumps(rel, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
