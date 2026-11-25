#!/usr/bin/env python3
"""Pacote do InDesign do artigo assinado da Retrospectiva 2026 (revista ES Brasil).

Usa o exportador da Retrospectiva (kit da skill retrospectiva-esbrasil: base da revista com Inter,
página-mestre com o paginador, estilos e amostras da casa) e acrescenta o que é próprio do artigo.

Uso:
    python3 exportar_artigo.py PASTA_DA_PAGINA KIT_RETROSPECTIVA PASTA_SAIDA --nome Artigo_ESB238_p111_LourenzoDeOliveira
        --pagina 111 --foto-cmyk foto/lourenzo-de-oliveira.tif --qr-pdf qr-artigo-lourenzo-de-oliveira.pdf
        [--recorte foto/lourenzo-de-oliveira-recorte.png]

PASTA_DA_PAGINA é a saída do montar_artigo.py (artigo.html, pagina.pdf, prova.pdf, encaixe.json).
KIT_RETROSPECTIVA é a pasta kit/ da retrospectiva-esbrasil (scripts/ e assets/).

Ajustes sobre o exportador da Retrospectiva:
- papéis novos: título do artigo, autor, cargo e texto do QR, cada um num estilo derivado dos da casa
  ("Título artigo 2026", "Autor artigo 2026", "Cargo articulista 2026", "QR Code texto 2026");
- vinheta "ARTIGO" em "Retranca 2026 - Artigo" (tracking -20: letras justas, como no modelo);
- texto corrido em "Texto artigo 2026" e "Texto artigo cap 2026" (Minion Pro Cond 11 pt, entrelinha 11,7,
  30 linhas por coluna, como no modelo do Sidemar Acosta);
- logo do paginador da prova (.so-prova) fica de fora: o paginador vem da página-mestre;
- foto trocada pelo TIFF em CMYK (perfil da revista) e QR Code pelo PDF vetorial em K 100 com o selo ESB;
- crédito da foto na vertical, de baixo para cima, terminando no topo da foto (como no modelo);
- sinal de fim de texto na cor do número de página (C=0 M=100 Y=80 K=0).
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import tempfile
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

PAPEIS = {
    "Título do artigo": "Título artigo 2026",
    "Autor do artigo": "Autor artigo 2026",
    "Cargo do articulista": "Cargo articulista 2026",
    "Texto do QR Code": "QR Code texto 2026",
    "Cartola": "Retranca 2026 - Artigo",
}
DERIVADOS = {
    "Título artigo 2026": {"based_on": "Título 36pt 2026", "PointSize": 28, "leading": 25.75},
    "Autor artigo 2026": {"based_on": "Assinatura 2026", "PointSize": 12, "leading": 13, "Justification": "RightAlign",
                          "SpaceAfter": 0, "Hyphenation": "false"},
    "Cargo articulista 2026": {"based_on": "Créditos 2026", "PointSize": 10, "leading": 12, "Justification": "RightAlign",
                               "FillColor": "Color/Preto 90%25"},
    "QR Code texto 2026": {"based_on": "Legenda 2026", "leading": 10},
    "Retranca 2026 - Artigo": {"based_on": "Retranca 2026", "Tracking": -20},   # "ARTIGO" justo, como no modelo
    "Texto artigo 2026": {"based_on": "Texto geral 2026", "leading": 11.7},
    "Texto artigo cap 2026": {"based_on": "Texto fatual cap 3 linhas 2026", "leading": 11.7},
}
CORES = {(64, 64, 65): "Color/Preto 90%25", (35, 31, 32): "Color/Black", (88, 89, 91): "Color/Preto 90%25",
         (236, 1, 140): "Color/VermelhoRetro2025"}
VERMELHO_FIM = "Color/C=0 M=100 Y=80 K=0"


def preparar_kit(kit: Path) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="kit-artigo-")) / "kit"
    shutil.copytree(kit, tmp)
    js = (tmp / "scripts" / "extrair.js").read_text(encoding="utf8")
    js = js.replace("const PAGES = [...document.querySelectorAll('article.page')];",
                    "document.querySelectorAll('.so-prova').forEach(e => e.remove());\n  "
                    "const PAGES = [...document.querySelectorAll('article.page')];", 1)
    js = js.replace("const tests = [",
                    "const tests = [\n      ['.titulo-artigo, .titulo-artigo *', 'Título do artigo'], ['.autor', 'Autor do artigo'], "
                    "['.cargo', 'Cargo do articulista'], ['.qrtxt, .qrtxt *', 'Texto do QR Code'],", 1)
    (tmp / "scripts" / "extrair.js").write_text(js, encoding="utf8")
    return tmp


def editar_idml(idml: Path, troca) -> None:
    zin = zipfile.ZipFile(idml)
    files = {n: zin.read(n) for n in zin.namelist()}
    infos = {n: zin.getinfo(n) for n in zin.namelist()}
    zin.close()
    troca(files)
    tmp = idml.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w") as z:
        z.writestr(infos["mimetype"], files.pop("mimetype"), compress_type=zipfile.ZIP_STORED)
        for n, b in files.items():
            z.writestr(n, b, compress_type=zipfile.ZIP_DEFLATED)
    tmp.replace(idml)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pagina_dir")
    ap.add_argument("kit")
    ap.add_argument("saida")
    ap.add_argument("--nome", required=True)
    ap.add_argument("--pagina", type=int, default=None)
    ap.add_argument("--foto-cmyk", default=None)
    ap.add_argument("--qr-pdf", default=None)
    ap.add_argument("--recorte", default=None)
    a = ap.parse_args()
    pdir = Path(a.pagina_dir).resolve()
    kit = preparar_kit(Path(a.kit).resolve())
    sys.path.insert(0, str(kit / "scripts"))
    import exportar_indesign as ex
    ex.CASA_ESTILOS.update(PAPEIS)
    ex.CASA_DERIVADOS.update(DERIVADOS)
    ex.CASA_CORES.update(CORES)
    sys.argv = ["exportar_indesign.py", str(pdir / "artigo.html"), str(Path(a.saida).resolve()), "--nome", a.nome]
    if a.pagina:
        sys.argv += ["--pagina", str(a.pagina)]
    buf = io.StringIO()
    with redirect_stdout(buf):
        ex.main()
    res = json.loads(buf.getvalue()[buf.getvalue().index("{"):])
    out = Path(res["pasta"])
    idml = Path(res["idml"])
    links = out / "Links"
    avisos = list(res.get("avisos", []))

    foto_jpg = next((p for p in links.glob("p1-foto-*.jpg")), None)
    qr_png = next((p for p in links.glob("qr-*.png")), None)
    foto_tif = qr_pdf = None
    if a.foto_cmyk and foto_jpg:
        foto_tif = links / (foto_jpg.stem + ".tif")
        shutil.copy(pdir / a.foto_cmyk if not Path(a.foto_cmyk).is_absolute() else a.foto_cmyk, foto_tif)
    if a.qr_pdf and qr_png:
        qr_pdf = links / (qr_png.stem + ".pdf")
        shutil.copy(pdir / a.qr_pdf if not Path(a.qr_pdf).is_absolute() else a.qr_pdf, qr_pdf)

    def troca(files: dict):
        # estilos do texto corrido do artigo
        for n in [n for n in files if n.startswith("Stories/")]:
            s = files[n].decode("utf8")
            s2 = (s.replace('"ParagraphStyle/Texto fatual cap 3 linhas 2026"', '"ParagraphStyle/Texto artigo cap 2026"')
                   .replace('"ParagraphStyle/Texto geral 2026"', '"ParagraphStyle/Texto artigo 2026"'))
            if s2 != s:
                files[n] = s2.encode("utf8")
        st = files["Resources/Styles.xml"].decode("utf8")
        st = re.sub(r'(<CharacterStyle Self="CharacterStyle/Fim de texto"[^>]*?)FillColor="[^"]*"', rf'\1FillColor="{VERMELHO_FIM}"', st)
        files["Resources/Styles.xml"] = st.encode("utf8")
        for n in [n for n in files if n.startswith("Spreads/")]:
            s = files[n].decode("utf8")
            # foto: JPG -> TIFF CMYK
            if foto_tif:
                s = s.replace(f"file:Links/{foto_jpg.name}", f"file:Links/{foto_tif.name}").replace(f'Name="{foto_jpg.name}"', f'Name="{foto_tif.name}"')
                s = re.sub(rf'(<Image [^>]*?)ImageTypeName="\$ID/JPEG"([^>]*>(?:(?!</Image>).)*?file:Links/{re.escape(foto_tif.name)})',
                           r'\1ImageTypeName="$ID/TIFF"\2', s, flags=re.S)
                s = re.sub(rf'LinkResourceURI="file:Links/{re.escape(foto_tif.name)}" LinkResourceFormat="\$ID/JPEG"',
                           f'LinkResourceURI="file:Links/{foto_tif.name}" LinkResourceFormat="$ID/TIFF"', s)
            # QR: PNG -> PDF vetorial
            if qr_pdf:
                s = s.replace(f'Name="{qr_png.name}"', f'Name="{qr_pdf.name}"')
                def para_pdf(m):
                    bloco = m.group(0)
                    gid = re.search(r'<Image Self="([^"]+)"', bloco).group(1)
                    xf = re.search(r'ItemTransform="([^"]+)"', bloco).group(1)
                    gb = re.search(r"<GraphicBounds [^>]*/>", bloco).group(0)
                    link = re.search(r"<Link [^>]*/>", bloco).group(0)
                    link = (link.replace(f"file:Links/{qr_png.name}", f"file:Links/{qr_pdf.name}")
                            .replace('LinkResourceFormat="$ID/Portable Network Graphics (PNG)"',
                                     'LinkResourceFormat="$ID/Adobe Portable Document Format (PDF)"'))
                    return (f'<PDF Self="{gid}" ItemTransform="{xf}"><Properties>{gb}</Properties>'
                            f'<PDFAttribute PageNumber="1" PDFCrop="CropMedia" TransparentBackground="true"/>{link}</PDF>')
                s = re.sub(rf'<Image [^>]*>(?:(?!</Image>).)*?file:Links/{re.escape(qr_png.name)}(?:(?!</Image>).)*?</Image>', para_pdf, s, flags=re.S)
            # moldura do QR: filete de 0,5 pt (o navegador arredonda para 1 px)
            s = re.sub(r'(<Rectangle [^>]*Name="Contorno"[^>]*StrokeColor="Color/Black"[^>]*StrokeWeight=")[\d.]+(")', r'\g<1>0.5\2', s)
            s = re.sub(r'(<Rectangle [^>]*StrokeColor="Color/Black"[^>]*Name="Contorno"[^>]*StrokeWeight=")[\d.]+(")', r'\g<1>0.5\2', s)
            # crédito: de baixo para cima (270 graus), alinhado ao topo da foto
            def gira(m):
                el = m.group(0)
                xf = re.search(r'ItemTransform="0 1 -1 0 ([-\d.e]+) ([-\d.e]+)"', el)
                if not xf:
                    return el
                tx, ty = float(xf.group(1)), float(xf.group(2))
                pts = [tuple(map(float, q.split())) for q in re.findall(r'Anchor="([^"]+)"', el)]
                L = max(p[0] for p in pts) - min(p[0] for p in pts)
                T = max(p[1] for p in pts) - min(p[1] for p in pts)
                return el.replace(xf.group(0), f'ItemTransform="0 -1 1 0 {tx - T:.4f} {ty + L:.4f}"')
            s = re.sub(r'<TextFrame [^>]*Name="Crédito da foto"[^>]*>.*?</TextFrame>', gira, s, flags=re.S)
            files[n] = s.encode("utf8")
        # crédito alinhado à direita (o fim do texto encosta no topo da foto)
        for n in [n for n in files if n.startswith("Spreads/")]:
            s = files[n].decode("utf8")
            for sid in re.findall(r'<TextFrame [^>]*Name="Crédito da foto"[^>]*ParentStory="([^"]+)"', s) + \
                       re.findall(r'<TextFrame [^>]*ParentStory="([^"]+)"[^>]*Name="Crédito da foto"', s):
                k = f"Stories/Story_{sid}.xml"
                if k in files:
                    files[k] = re.sub(r"<ParagraphStyleRange ", '<ParagraphStyleRange Justification="RightAlign" ',
                                      files[k].decode("utf8")).encode("utf8")

    editar_idml(idml, troca)
    if foto_tif and foto_jpg:
        foto_jpg.unlink()
    if qr_pdf and qr_png:
        qr_png.unlink()
    # fotos de apoio e provas vetoriais
    extra = out / "Fotos de apoio"
    extra.mkdir(exist_ok=True)
    if a.recorte:
        shutil.copy(pdir / a.recorte, extra / Path(a.recorte).name)
    for f in ("pagina.pdf", "prova.pdf"):
        if (pdir / f).exists():
            shutil.copy(pdir / f, out / "Referencia" / f"{a.nome}-{f}")
    leia = out / "Leia-me.txt"
    leia.write_text(leia.read_text(encoding="utf8") + f"""

ARTIGO ASSINADO (modelo: artigo do Sidemar Acosta, ES 238, p. 28)
- Página {a.pagina or '00'} ({'ímpar: vinheta e aba rosa do lado direito, selo Retrospectiva à esquerda' if (a.pagina or 1) % 2 else 'par: vinheta à esquerda, selo à direita'}). O paginador vem da página-mestre "R-Retrospectiva 2026".
- Texto corrido: estilos "Texto artigo cap 2026" e "Texto artigo 2026" (Minion Pro Cond 11 pt, entrelinha 11,7, 30 linhas por coluna).
- Título: "Título artigo 2026" (Inter Black 28/25,75). Autor: "Autor artigo 2026". Cargo: "Cargo articulista 2026". Texto do QR: "QR Code texto 2026".
- Foto: {foto_tif.name if foto_tif else '—'} (CMYK, já recortada no padrão de cabeça dos artigos). A pessoa sem fundo está em "Fotos de apoio", para trocar o fundo se precisar.
- QR Code: {qr_pdf.name if qr_pdf else '—'} (vetorial, K 100, selo ESB no centro). Confira se o link curto já abre antes de fechar.
- Fim de texto: o sinal ■ está no estilo "Fim de texto", na cor do número da página; troque pelo glifo da casa, se usar outro.
""", encoding="utf8")
    zipf = shutil.make_archive(str(out), "zip", root_dir=out.parent, base_dir=out.name)
    res.update({"zip": zipf, "foto": foto_tif.name if foto_tif else None, "qr": qr_pdf.name if qr_pdf else None, "avisos": avisos})
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
