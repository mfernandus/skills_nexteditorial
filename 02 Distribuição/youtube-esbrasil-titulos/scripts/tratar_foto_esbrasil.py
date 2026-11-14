"""Trata a foto do convidado para a capa ES Brasil Entrevista.
Uso: python3 tratar_foto_esbrasil.py quadro.png recorte.png [peso_restauracao=0.6]

1. Restauração do rosto com IA (GFPGAN v1.4, 2x): limpa ruído e compressão, mantém os traços.
   Só roda se o pacote gfpgan e os pesos weights/GFPGANv1.4.pth existirem; senão a etapa é pulada
   com aviso (foto de estúdio dispensa a restauração).
   Pesos: https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
2. Recorte (rembg isnet-general-use + alpha matting), preservando os fios de cabelo.
3. Cor: +10% contraste, +8% saturação, +5% brilho, nitidez leve. Tom NEUTRO (não aquecer).
4. Sem luz de recorte colorida: o template ES Brasil usa o convidado limpo sobre o fundo azul.

Requisitos: pip install rembg opencv-python pillow numpy   (e, para a etapa 1, gfpgan)
"""
import sys, pathlib, numpy as np, cv2
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove, new_session

src, out = sys.argv[1], sys.argv[2]
peso = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
img = cv2.imread(src)
assert img is not None, f"não consegui abrir {src}"

pesos = pathlib.Path(__file__).resolve().parent.parent / "weights" / "GFPGANv1.4.pth"
try:
    from gfpgan import GFPGANer
    assert pesos.exists(), f"pesos não encontrados em {pesos}"
    r = GFPGANer(model_path=str(pesos), upscale=2, arch="clean", channel_multiplier=2, bg_upsampler=None)
    _, _, img = r.enhance(img, has_aligned=False, only_center_face=True, paste_back=True, weight=peso)
    img = cv2.bilateralFilter(img, 5, 25, 5)
    print("restauração do rosto: aplicada (peso", peso, ")")
except Exception as e:                                   # noqa: BLE001
    print("restauração do rosto: PULADA —", e)

rgb = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
mask = remove(rgb, session=new_session("isnet-general-use"), only_mask=True, post_process_mask=True,
              alpha_matting=True, alpha_matting_foreground_threshold=240,
              alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
a = np.asarray(mask).astype(np.float32) / 255
a = np.where(a < 0.08, 0, a)
a = cv2.GaussianBlur(a, (0, 0), 1.0)

rgb = ImageEnhance.Contrast(rgb).enhance(1.10)
rgb = ImageEnhance.Color(rgb).enhance(1.08)
rgb = ImageEnhance.Brightness(rgb).enhance(1.05)
rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.8, percent=70, threshold=3))

res = Image.fromarray(np.dstack([np.asarray(rgb), (a * 255).astype(np.uint8)]), "RGBA")
res = res.crop(res.getbbox())
res.save(out)
print("recorte salvo:", out, res.size)
