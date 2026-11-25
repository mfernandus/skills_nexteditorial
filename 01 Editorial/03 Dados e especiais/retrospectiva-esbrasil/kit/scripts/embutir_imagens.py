#!/usr/bin/env python3
"""Deixa o capítulo num arquivo só, pronto para publicar como artefato.

Uso:
    python3 embutir_imagens.py capitulo.html capitulo-final.html [--qr-materia URL]

- Troca cada <img src="caminho/relativo"> por data URI (as fotos ficam dentro do HTML).
- selo-retrospectiva.png, logo-es-brasil.png e logo-es-em-numeros.png vêm da pasta assets do kit quando não estão ao lado do HTML.
- Gera qr-materia.png (link da matéria no site) e qr-es-em-numeros.png quando faltam (precisa de: pip install segno).
"""
import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path

KIT_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def gerar_qr(url: str, destino: Path) -> bool:
    try:
        import segno
    except ImportError:
        print(f"aviso: instale segno (pip install segno) para gerar {destino.name}", file=sys.stderr)
        return False
    segno.make(url, error="m").save(str(destino), scale=8, border=1, dark="#001C43")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--qr-materia", default="https://esbrasil.com.br")
    a = ap.parse_args()
    src = Path(a.entrada).resolve()
    base = src.parent
    html = src.read_text(encoding="utf8")
    if 'src="qr-materia.png"' in html and not (base / "qr-materia.png").exists():
        gerar_qr(a.qr_materia, base / "qr-materia.png")
    if 'src="qr-es-em-numeros.png"' in html and not (base / "qr-es-em-numeros.png").exists():
        gerar_qr("https://esemnumeros.esbrasil.com.br", base / "qr-es-em-numeros.png")
    faltando = []

    def troca(m):
        ref = m.group(2)
        if ref.startswith(("data:", "http:", "https:")):
            return m.group(0)
        p = (base / ref)
        if not p.exists() and (KIT_ASSETS / Path(ref).name).exists():
            p = KIT_ASSETS / Path(ref).name
        if not p.exists():
            faltando.append(ref)
            return m.group(0)
        mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
        return f'{m.group(1)}data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"'

    html = re.sub(r'(<img[^>]*?\ssrc=")([^"]+)"', troca, html)
    Path(a.saida).write_text(html, encoding="utf8")
    print(f"ok: {a.saida} ({len(html) / 1e6:.1f} MB)")
    if faltando:
        print("imagens não encontradas: " + ", ".join(faltando), file=sys.stderr)


if __name__ == "__main__":
    main()
