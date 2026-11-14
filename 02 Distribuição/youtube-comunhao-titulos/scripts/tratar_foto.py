"""Trata a foto do convidado para a thumb.
Uso: python3 tratar_foto.py quadro.png saida.png [peso_gfpgan=0.6]
1. Restauração de rosto com IA (GFPGAN v1.4, 2x): limpa manchas e ruído, mantém traços.
2. Recorte (rembg isnet-general-use + alpha matting) com refino de bordas do cabelo.
Requisitos: pip install gfpgan rembg opencv-python pillow; pesos GFPGANv1.4.pth em weights/
(https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth).
Se o basicsr acusar 'torchvision.transforms.functional_tensor', troque o import por
'torchvision.transforms.functional' em basicsr/data/degradations.py.
Em máquinas com pouca memória, rode as etapas em processos separados.
3. Cor: contraste, saturação, brilho, nitidez e tom levemente quente.
4. Integração: rim light laranja e escurecimento na base.
"""
import sys, numpy as np, cv2
from PIL import Image, ImageEnhance, ImageFilter
from gfpgan import GFPGANer
from rembg import remove, new_session

src, out = sys.argv[1], sys.argv[2]
w8 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6

img = cv2.imread(src)
r = GFPGANer(model_path=str(__import__('pathlib').Path(__file__).resolve().parent.parent/'weights'/'GFPGANv1.4.pth'), upscale=2, arch='clean',
             channel_multiplier=2, bg_upsampler=None)
_, _, rest = r.enhance(img, has_aligned=False, only_center_face=True, paste_back=True, weight=w8)
# suaviza o restante da imagem ampliada (cabelo/roupa) sem perder nitidez
rest = cv2.bilateralFilter(rest, 5, 25, 5)

rgb = Image.fromarray(cv2.cvtColor(rest, cv2.COLOR_BGR2RGB))
sess = new_session('isnet-general-use')
mask = remove(rgb, session=sess, only_mask=True, post_process_mask=True,
              alpha_matting=True, alpha_matting_foreground_threshold=240,
              alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
a = np.asarray(mask).astype(np.float32) / 255
# remove restos de fundo e suaviza a borda
a = np.where(a < 0.08, 0, a)
a = cv2.GaussianBlur(a, (0, 0), 1.0)
h, w = a.shape
a *= np.clip(np.arange(w) / (w * 0.07), 0, 1)[None, :]          # esfuma borda esquerda (corpo encosta no quadro)
a *= np.clip((w - 1 - np.arange(w)) / (w * 0.03), 0, 1)[None, :]

rgb = ImageEnhance.Contrast(rgb).enhance(1.10)
rgb = ImageEnhance.Color(rgb).enhance(1.08)
rgb = ImageEnhance.Brightness(rgb).enhance(1.05)
rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.8, percent=70, threshold=3))
arr = np.asarray(rgb).astype(np.float32)
arr[..., 0] *= 1.035; arr[..., 2] *= 0.96

edge = a - cv2.GaussianBlur(cv2.erode(a, np.ones((11, 11), np.uint8)), (0, 0), 8)
rim = np.clip(edge * 2.0, 0, 1) * np.linspace(1, 0.3, w)[None, :]
arr = arr * (1 - rim[..., None] * 0.5) + np.array([255, 170, 60], np.float32) * rim[..., None] * 0.5
grad = np.clip((np.arange(h)[:, None] - h * 0.82) / (h * 0.18), 0, 1)
arr = arr * (1 - 0.30 * grad[..., None])

res = Image.fromarray(np.dstack([arr.clip(0, 255), a * 255]).astype(np.uint8), 'RGBA')
res = res.crop(res.getbbox())
res.save(out)
print(res.size)
