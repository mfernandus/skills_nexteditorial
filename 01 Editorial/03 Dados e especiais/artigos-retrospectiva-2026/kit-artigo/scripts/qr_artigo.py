#!/usr/bin/env python3
"""QR Code dos artigos da Retrospectiva no padrão da revista ES Brasil (modelo: artigo do Sidemar Acosta, ES 238).

Uso:
    python3 qr_artigo.py URL PASTA_SAIDA --nome qr-artigo-lourenzo-de-oliveira

Padrão: link curto do Encurtador da Next (https://nx-t.me/ART-<NOME><INICIAL DO SOBRENOME>-ESB<edição>),
correção de erro alta (H), módulos 100% preto (K), selo ESB no centro (34% da largura) e margem de 2 módulos.
Na página: o QR ocupa 45,6 x 45,6 pt dentro de uma moldura de 53,3 x 53,3 pt com filete preto de 0,5 pt.

Grava:
    <nome>.png   prova (RGB, 1200 ppi no tamanho de uso)
    <nome>.pdf   para o InDesign (vetorial, módulos em K 100 e selo ESB em CMYK)
e confere a leitura do código gerado (OpenCV). Sai com erro se o QR não for lido.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LADO_PT = 45.6          # tamanho do QR na página
BORDA = 2               # módulos de margem dentro da imagem
LOGO = 0.34             # largura do selo ESB em relação ao QR


def slug_curto(nome: str, edicao: str = "238") -> str:
    """'Lourenzo de Oliveira' -> https://nx-t.me/ART-LOURENZOO-ESB238 (primeiro nome + inicial do último sobrenome)."""
    import unicodedata
    partes = [p for p in unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().upper().split()
              if p not in ("DE", "DA", "DO", "DOS", "DAS", "E")]
    cod = partes[0] + (partes[-1][0] if len(partes) > 1 else "")
    return f"https://nx-t.me/ART-{cod}-ESB{edicao}"


def matriz(url: str) -> np.ndarray:
    import segno
    q = segno.make(url, error="h", micro=False, boost_error=False)
    m = np.array([[bool(v) for v in row] for row in q.matrix_iter(border=BORDA)], dtype=bool)
    return m


def area_logo(n: int) -> tuple[int, int]:
    lado = int(round(n * LOGO))
    lado += (n - lado) % 2          # centralizado em módulos inteiros
    a = (n - lado) // 2
    return a, a + lado


def png(m: np.ndarray, destino: Path, ppi: int = 1200) -> Path:
    n = m.shape[0]
    px = int(round(LADO_PT / 72 * ppi))
    esc = px / n
    img = Image.new("RGB", (px, px), "white")
    arr = np.array(img)
    a, b = area_logo(n)
    for y in range(n):
        for x in range(n):
            if m[y, x] and not (a <= x < b and a <= y < b):
                arr[int(round(y * esc)):int(round((y + 1) * esc)), int(round(x * esc)):int(round((x + 1) * esc))] = (35, 31, 32)
    img = Image.fromarray(arr)
    logo = Image.open(ASSETS / "qr-centro-esb.png").convert("RGB")
    lw = int(round((b - a) * esc))
    img.paste(logo.resize((lw, lw), Image.LANCZOS), (int(round(a * esc)), int(round(a * esc))))
    img.save(destino, dpi=(ppi, ppi))
    return destino


def pdf(m: np.ndarray, destino: Path) -> Path:
    import pymupdf
    n = m.shape[0]
    mod = LADO_PT / n
    doc = pymupdf.open()
    pg = doc.new_page(width=LADO_PT, height=LADO_PT)
    a, b = area_logo(n)
    sh = pg.new_shape()
    for y in range(n):
        x = 0
        while x < n:
            if m[y, x] and not (a <= x < b and a <= y < b):
                x0 = x
                while x < n and m[y, x] and not (a <= x < b and a <= y < b):
                    x += 1
                sh.draw_rect(pymupdf.Rect(x0 * mod, y * mod, x * mod, (y + 1) * mod))
            else:
                x += 1
    sh.finish(color=None, fill=(0, 0, 0, 1), width=0)      # K 100
    sh.commit()
    logo = ASSETS / "qr-centro-esb-cmyk.tif"
    b64 = ASSETS / "qr-centro-esb-cmyk.tif.b64.txt"      # o artefato do kit não serve .tif: vai em base64
    if not logo.exists() and b64.exists():
        import base64
        logo.write_bytes(base64.b64decode(b64.read_text(encoding="ascii")))
    if not logo.exists():
        logo = ASSETS / "qr-centro-esb.png"
    pg.insert_image(pymupdf.Rect(a * mod, a * mod, b * mod, b * mod), filename=str(logo))
    doc.save(destino, deflate=True)
    return destino


def confere(caminho_png: Path) -> str:
    import cv2
    im = cv2.imread(str(caminho_png))
    im = cv2.resize(im, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    im = cv2.copyMakeBorder(im, 60, 60, 60, 60, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    v, _, _ = cv2.QRCodeDetector().detectAndDecode(im)
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="URL do QR (use --autor para montar o link curto padrão)")
    ap.add_argument("saida")
    ap.add_argument("--nome", default="qr-artigo")
    a = ap.parse_args()
    out = Path(a.saida); out.mkdir(parents=True, exist_ok=True)
    m = matriz(a.url)
    p = png(m, out / f"{a.nome}.png")
    pdf(m, out / f"{a.nome}.pdf")
    lido = confere(p)
    print(f"QR {m.shape[0] - 2 * BORDA}x{m.shape[0] - 2 * BORDA} módulos · {a.url} · leitura: {lido or 'FALHOU'}")
    if lido != a.url:
        sys.exit("FALHA: o QR gerado não foi lido corretamente; reduza o selo ou encurte o link")


if __name__ == "__main__":
    main()
