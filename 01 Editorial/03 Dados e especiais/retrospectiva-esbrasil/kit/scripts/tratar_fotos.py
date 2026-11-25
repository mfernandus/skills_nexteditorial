"""Tratamento padrão das fotos da Next: recorte na proporção da vaga, níveis, eliminação de névoa (dehaze),
claridade, vibração, saturação e nitidez. Fotos moles ou ampliadas recebem nitidez mais forte."""
import io
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageCms


def abrir(caminho):
    im = Image.open(caminho)
    if im.mode == 'CMYK':
        try:
            srgb = ImageCms.createProfile('sRGB'); icc = im.info.get('icc_profile')
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), srgb, outputMode='RGB') if icc else im.convert('RGB')
        except Exception:
            im = im.convert('RGB')
    return im.convert('RGB')


def recortar(im, proporcao, cy=0.5, cx=0.5, zoom=1.0):
    w, h = im.size
    if w / h > proporcao:
        nh = int(h / zoom); nw = int(nh * proporcao)
    else:
        nw = int(w / zoom); nh = int(nw / proporcao)
    x0 = int(max(0, min(w - nw, cx * w - nw / 2))); y0 = int(max(0, min(h - nh, cy * h - nh / 2)))
    return im.crop((x0, y0, x0 + nw, y0 + nh))


def niveis(a, baixo=0.3, alto=99.7):
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    lo, hi = np.percentile(lum, baixo), np.percentile(lum, alto)
    hi = max(hi, lo + 30)
    return np.clip((a - lo) / (hi - lo) * 255, 0, 255)


def dehaze(im, forca=0.45):
    """Névoa: canal escuro (He et al.) suave, sobre a imagem reduzida, com transmissão mínima alta."""
    a = np.asarray(im).astype(np.float32) / 255
    peq = im.resize((max(1, im.width // 8), max(1, im.height // 8)), Image.BILINEAR)
    pa = np.asarray(peq).astype(np.float32) / 255
    escuro = Image.fromarray((pa.min(axis=2) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(7))
    esc = np.asarray(escuro).astype(np.float32) / 255
    A = np.percentile(pa.reshape(-1, 3)[esc.reshape(-1) >= np.percentile(esc, 99.9)], 90, axis=0).clip(0.6, 1)
    t = 1 - forca * esc
    t = np.asarray(Image.fromarray((t * 255).astype(np.uint8)).resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    t = np.clip(t, 0.62, 1)[..., None]
    j = (a - A) / t + A
    return np.clip(j * 255, 0, 255)


def vibracao(a, forca=0.25):
    mx, mn = a.max(axis=2, keepdims=True), a.min(axis=2, keepdims=True)
    sat = (mx - mn) / (mx + 1e-3)
    media = a.mean(axis=2, keepdims=True)
    k = 1 + forca * (1 - sat)          # mais nas cores apagadas, pouco nas já saturadas e na pele
    return np.clip(media + (a - media) * k, 0, 255)


def citrico(im, matiz=-7, sat=1.18, luz=1.04):
    """Verdes mais cítricos: puxa o verde para o amarelo, satura e clareia um pouco a vegetação."""
    hsv = np.asarray(im.convert('HSV')).astype(np.float32)
    h, s_, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    verde = ((h > 28) & (h < 120)).astype(np.float32)          # amarelo-esverdeado a verde (escala 0-255 do PIL)
    peso = verde * np.clip(s_ / 60, 0, 1)
    h = h + matiz * peso
    s_ = np.clip(s_ * (1 + (sat - 1) * peso), 0, 255)
    v = np.clip(v * (1 + (luz - 1) * peso), 0, 255)
    out = np.stack([h % 256, s_, v], axis=2).astype(np.uint8)
    return Image.fromarray(out, 'HSV').convert('RGB')


def tratar(src, dst, proporcao, largura=2400, cy=0.5, cx=0.5, zoom=1.0, nevoa=0.45, claridade=30,
           vibra=0.25, saturacao=1.06, contraste=1.04, quente=0.0, nitidez=80, mole=False, qualidade=90, verde_citrico=False):
    im = abrir(src)
    if proporcao:
        im = recortar(im, proporcao, cy, cx, zoom)
    if im.size[0] != largura:
        im = im.resize((largura, int(largura * im.size[1] / im.size[0])), Image.LANCZOS)
    a = dehaze(im, nevoa) if nevoa else np.asarray(im).astype(np.float32)
    a = niveis(a)
    a = vibracao(a, vibra)
    if quente:
        a[..., 0] *= 1 + quente; a[..., 2] *= 1 - quente
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if verde_citrico:
        im = citrico(im)
    im = ImageEnhance.Color(im).enhance(saturacao)
    im = ImageEnhance.Contrast(im).enhance(contraste)
    if claridade:   # contraste local (claridade), raio grande e leve
        im = im.filter(ImageFilter.UnsharpMask(radius=max(20, largura // 80), percent=claridade, threshold=0))
    if mole:        # foto fora de foco ou ampliada: nitidez em duas passadas
        im = im.filter(ImageFilter.UnsharpMask(radius=2.4, percent=90, threshold=1))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=nitidez, threshold=2))
    im.save(dst, 'JPEG', quality=qualidade, dpi=(300, 300), subsampling=0)
    return im.size
