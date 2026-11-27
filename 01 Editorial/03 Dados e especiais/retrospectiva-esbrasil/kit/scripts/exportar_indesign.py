#!/usr/bin/env python3
"""Pacote para o InDesign a partir das páginas aprovadas de um capítulo da Retrospectiva ES Brasil.

Uso:
    python3 exportar_indesign.py CAPITULO.html PASTA_SAIDA [--nome Retrospectiva2026_Rochas]

Lê o HTML aprovado (páginas article.page de 20,5 x 27,5 cm, texto corrido em template#texto e
caixas .flow), abre no Chromium e gera a pasta que o time de diagramação usa:

    <nome>/
      <nome>.idml            documento do InDesign (abre no InDesign 2018 ou mais novo)
      Links/                 fotos, selos, QR Codes e gráficos (PDF vetorial + SVG editável)
      Document fonts/        Inter (OFL); a Minion Pro Condensed vem da Adobe Fonts
      Referencia/            prova aprovada em PDF e PNG, página a página
      Textos/                texto corrido (.docx e .txt), tabelas (.xlsx), banco de aspas, fotos a buscar
      Leia-me.txt
    <nome>.zip               a mesma pasta compactada
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ESTILO_OBJETO_FOTO = "ObjectStyle/Frame Box de foto 2026"   # estilo de objeto das fotos na base V5

from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from idml import IDML, Para, Run, safe_name  # noqa: E402
from svg_vetor import JS_MEDIR, desenhar_svg  # noqa: E402
from casa import CAP, OBJ, PAR, Casa  # noqa: E402

W_PT, H_PT = 581.1024, 779.5276          # 205 x 275 mm
CHROME = next((c for c in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
                            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") if Path(c).exists()), None)
INTER_DIR = next((d for d in (Path("/usr/share/fonts/opentype/inter"), Path.home() / "Library/Fonts",
                              Path("/Library/Fonts"), Path("/usr/share/fonts/truetype/inter")) if (d / "Inter-Regular.otf").exists()),
                 Path("/usr/share/fonts/opentype/inter"))
INTER_LICENSE = Path("/usr/share/doc/fonts-inter/copyright")

# Corpo do texto corrido na revista impressa (Minion Pro Condensed, Adobe Fonts).
CORPO_FONTE = "Minion Pro"
CORPO_ESTILOS = {400: "Cond", 500: "Medium Cond", 600: "Semibold Cond", 700: "Bold Cond"}

SWATCHES = {
    (0, 28, 67): "ES Brasil Navy", (0, 66, 123): "ES Brasil Azul", (224, 30, 112): "ES Brasil Rosa",
    (161, 21, 237): "ES Brasil Roxo", (162, 210, 255): "ES Brasil Azul-pastel",
    (15, 45, 92): "Infografico Navy", (24, 166, 230): "Infografico Ciano", (221, 225, 230): "Infografico Painel",
    (231, 234, 238): "Infografico Painel claro", (211, 233, 247): "Infografico Total",
    (27, 36, 48): "Texto Tinta", (22, 28, 36): "Texto Corpo", (94, 107, 124): "Texto Cinza", (62, 74, 90): "Texto Cinza escuro",
    (15, 122, 63): "Variacao Alta", (192, 24, 47): "Variacao Queda",
    (217, 238, 252): "Prova Aspa verificada", (255, 227, 191): "Prova Aspa montada",
    (255, 227, 239): "Prova Buscar original", (224, 122, 0): "Prova Laranja",
}
# Base da Retrospectiva V6 (a V5, MATÉRIA 1 - RETROSPECTIVA 2026 - ESB V5, de 21/11/2026, com os estilos, as cores e
# as fontes do "GRAFICOS E TABELAS 1 - RETROSPECTIVA 2026 - ESB V1", de 26/11/2026): o pacote nasce
# com os estilos, as cores, as preferências e as páginas-mestre da casa. As mestres da V5 já trazem o fundo da
# Retrospectiva, a retranca "retrospectiva 2026", o selo, o logo da ES Brasil, as abas de cor e o paginador; o
# exportador copia a "A-Master" inteira e troca a retranca da página direita pela editoria.
# Papéis do HTML que usam os estilos da base pelo nome:
_ASSETS = Path(__file__).resolve().parent.parent / "assets"
BASE_PADRAO = _ASSETS / "base-retrospectiva-2026-v6.idml"
_B64 = _ASSETS / "base-retrospectiva-2026-v6.idml.b64.txt"   # o artefato do kit não serve .idml: a base vai em base64
if not BASE_PADRAO.exists() and _B64.exists():
    BASE_PADRAO.write_bytes(base64.b64decode(_B64.read_text(encoding="ascii")))
CASA_ESTILOS = {
    "Título": "Título 36pt 2026",
    "Linha fina": "Lead 2026",
    "Assinatura": "Assinatura 2026",
    "Legenda": "Legenda 2026",
    "Legenda sobre foto": "Legenda dentro foto 2026",
    "Crédito da foto": "Créditos 2026",
}
# estilos de objeto da casa para legendas e créditos de foto (base V6, 26/11/2026)
OBJ_FOTO = {"Legenda": "ObjectStyle/Frame Legenda fora da foto 2026",
            "Legenda sobre foto": "ObjectStyle/Frame Legenda dentro foto 2026",
            "Crédito da foto": "ObjectStyle/Frame Créditos 2026"}
MM = 72 / 25.4
# Papéis do HTML que, no pacote da revista, usam só os estilos de parágrafo da casa (26/11/2026: o .idml é para
# impressão; títulos em Inter, texto de box e números em Roboto Condensed, variando só o corpo). Nada de estilo
# "Retro 2026 - ..." gerado.
CASA_PAPEIS = {
    "Box · título": "Título de box 2026", "Box · subtítulo": "Texto de box 2026", "Box · etiqueta": "Texto de box 2026",
    "Box · número": "Texto de tabela e gráficos destaque grande azul 2026", "Box · texto": "Texto de box destaque 2026",
    "Box · QR Code": "Texto de box 2026", "Box · fontes": "Créditos 2026", "Box · aspa": "Texto de box 2026",
    "QR Code": "Texto de box 2026",
    "Linha do tempo · título": "Título de box 2026", "Linha do tempo · escopo": "Texto de box 2026",
    "Linha do tempo · mês": "Texto topo de tabela 2026", "Linha do tempo · marco": "Texto de tabela primeira coluna 2026",
    "Linha do tempo · detalhe": "Texto de box 2026", "Linha do tempo · fontes": "Créditos 2026",
    "Gráfico · título": "Título de box 2026", "Tabela · título": "Título de box 2026",
    "Gráfico · subtítulo": "Texto de box 2026", "Gráfico · fonte": "Créditos 2026",
    "Gráfico · número": "Texto de tabela e gráficos destaque azul 2026", "Gráfico · rótulo": "Texto de tabela normal 2026",
}
CASA_DERIVADOS = {}   # a V5 já traz título branco, intertítulo em caixa alta e baixa e legendas em Roboto Condensed
CASA_CORES = {   # cores do HTML -> amostras CMYK da casa
    (0, 66, 123): "Color/Azul ES Brasil 2026", (15, 45, 92): "Color/Azul ES Brasil 2026",
    (0, 28, 67): "Color/Azul ES Brasil 2026", (17, 62, 116): "Color/Azul ES Brasil 2026",
    (224, 30, 112): "Color/VermelhoRetro2025", (236, 1, 140): "Color/VermelhoRetro2025",
    (26, 26, 26): "Color/Preto 90%25", (22, 28, 36): "Color/Preto 90%25", (27, 36, 48): "Color/Preto 90%25",
    (204, 204, 204): "Color/Preto 20%25", (255, 255, 255): "Color/Paper", (0, 0, 0): "Color/Black",
    (24, 166, 230): "Color/C=70 M=20 Y=0 K=0", (221, 225, 230): "Color/Preto 10%25",
    # cores do NXtab e da prova -> amostras CMYK da paleta da casa (26/11/2026: o .idml é para impressão)
    (57, 53, 54): "Color/Preto 90%25", (35, 31, 32): "Color/Preto 90%25", (61, 61, 61): "Color/Preto 80%25",
    (189, 189, 189): "Color/Preto 30%25", (242, 242, 242): "Color/Preto 10%25", (231, 234, 238): "Color/Preto 10%25",
    (0, 173, 239): "Color/C=100 M=0 Y=0 K=0", (82, 165, 224): "Color/C=70 M=20 Y=0 K=0",
    (23, 102, 197): "Color/C=100 M=60 Y=0 K=0", (14, 52, 98): "Color/Destinos Navy 2026",
    (234, 248, 254): "Color/NX Fundo 2026", (157, 216, 243): "Color/ESB Azul Pastel 2026",
    (217, 243, 253): "Color/C=10 M=0 Y=0 K=0", (204, 239, 252): "Color/C=20 M=0 Y=0 K=0",
    (211, 233, 247): "Color/C=10 M=0 Y=0 K=0", (162, 210, 255): "Color/ESB Azul Pastel 2026",
    (161, 21, 237): "Color/ESB Roxo 2026", (94, 107, 124): "Color/NX Cinza 2026", (62, 74, 90): "Color/Preto 80%25",
    (15, 122, 63): "Color/Verde Escuro ESG", (192, 24, 47): "Color/NX Vermelho 600 2026",
    (122, 11, 58): "Color/NX Vermelho 800 2026",
}
PESOS = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold",
         700: "Bold", 800: "ExtraBold", 900: "Black"}


def slug(s: str, n: int = 40) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return (s[:n].rstrip("-")) or "item"


def parse_color(c: str):
    m = re.match(r"rgba?\(([^)]+)\)", c or "")
    if not m:
        return None, 1.0
    v = [float(x) for x in re.split(r"[,\s/]+", m.group(1).strip()) if x]
    a = v[3] if len(v) > 3 else 1.0
    return (int(round(v[0])), int(round(v[1])), int(round(v[2]))), a


class Exportador:
    def __init__(self, data: dict, out: Path, nome: str, pdf_page=None, base: Path | None = None):
        self.d, self.out, self.nome, self.pdf_page, self.base = data, out, nome, pdf_page, base
        self.vetor = True     # peças do NXtab como objetos nativos do InDesign (--graficos-vinculados desliga)
        self.casa = Casa(base) if base else None   # medidas dos estilos da base (espaçamentos e corpos)
        self.K = W_PT / data["width"]
        if base:
            primeira = (data["pages"][0].get("lado") if data.get("pages") else None) or "esq"
            self.doc = IDML(W_PT, H_PT, facing=True, primeira=primeira)
            self.doc.cmyk = True      # pacote para impressão: nenhuma amostra RGB (26/11/2026)
            import zipfile
            dm = zipfile.ZipFile(base).read("designmap.xml").decode("utf-8")
            camadas = dict((n, s) for s, n in re.findall(r'<Layer Self="([^"]+)" Name="([^"]+)"', dm))
            self.doc.layer_existente("textos", camadas.get("TEXTOS", "ua00a"), "TEXTOS")
            self.doc.layer_existente("fundos", camadas.get("FUNDOS E IMAGENS", "ub9"), "FUNDOS E IMAGENS")
            self.doc.layer_existente("base", camadas.get("TEXTOS", "ua00a"), "TEXTOS")   # texto corrido e o resto vão para TEXTOS
            for nome_d, a in CASA_DERIVADOS.items():
                self.doc.para_style(nome_d, **a)
        else:
            self.doc = IDML(W_PT, H_PT)
        self.doc.layer("prova", "Prova (não imprime)", printable=False)
        self.style_defs: dict[str, dict] = {}
        self.links: dict[str, str] = {}      # sha1 -> nome do arquivo
        self.fontes_usadas: set[str] = set()
        self.avisos: list[str] = []
        self.fotos: list[dict] = []
        self.graficos: list[tuple] = []      # (svg, nome, w, h)

    # ------------------------------------------------------------- cores e fontes
    def cor(self, css: str):
        rgb, a = parse_color(css)
        if rgb is None or a < 0.01:
            return None, 1.0
        if self.base and rgb in CASA_CORES:
            return CASA_CORES[rgb], a
        if self.casa:     # impresso: a amostra CMYK mais próxima da paleta da casa; se nenhuma servir, uma CMYK nova
            am = self.casa.amostra(rgb)
            if am:
                return am, a
        return self.doc.color(rgb, SWATCHES.get(rgb)), a

    def fonte(self, family: str, weight: int, italic: bool):
        w = min(PESOS, key=lambda k: abs(k - (weight or 400)))
        if family.lower().startswith(("crimson", "minion", "georgia")):
            st = CORPO_ESTILOS.get(min(CORPO_ESTILOS, key=lambda k: abs(k - w)))
            return CORPO_FONTE, st + (" Italic" if italic else "")
        st = PESOS[w]
        if italic:
            st = "Italic" if st == "Regular" else f"{st} Italic"
        if family.lower().startswith("roboto condensed"):   # legendas, créditos e textos de box da base V5
            return "Roboto Condensed", st
        if family.lower().startswith("myriad"):             # provas antigas com Myriad: desde 23/11/2026 a condensada da casa é a Roboto Condensed
            return "Roboto Condensed", st
        self.fontes_usadas.add(st)
        return "Inter", st

    def moldura_de_foto(self, doc, pg, it, papel, paras, x, y, w, h, fotos, lay):
        """Legenda e crédito de foto com o estilo de objeto da casa (26/11/2026): a moldura leva só o estilo, e o
        espaçamento até a foto é o Inset Spacing do estilo. Legenda logo abaixo da foto encosta na borda de baixo
        dela; crédito vertical encosta na lateral da foto."""
        cs, obj = self.casa, OBJ_FOTO[papel]
        t_in, l_in, b_in, r_in = cs.inset(obj)
        p = cs.par("ParagraphStyle/" + CASA_ESTILOS[papel])
        texto = " ".join("".join(r.text for r in pa.runs) for pa in paras)
        tol = 8 * MM
        if it.get("rot") == 90:
            # crédito vertical, de cima para baixo: a borda de baixo da moldura (já girada) encosta na foto
            esp = t_in + p["cap"] + b_in
            foto = next((fo for fo in fotos if abs(x - fo[2]) < tol and fo[1] - tol <= y <= fo[3]), None)
            fx = foto[2] if foto else x
            fy = foto[1] if foto and y - foto[1] < tol else y
            comp = max(h, cs.largura(texto, "ParagraphStyle/" + CASA_ESTILOS[papel]) + 4)
            doc.text_frame(pg, fx, fy, esp, comp, paras, name=papel.replace("·", "-"), layer=lay, rot=90,
                           object_style=obj, limpo=True)
            return
        base0 = it["paras"][0]["base0"] * self.K
        fy = base0 - p["cap"] - t_in
        fx, fw = x - l_in, w + l_in + r_in + 2
        if papel == "Legenda":
            foto = next((fo for fo in fotos if 0 <= fy - fo[3] < tol and fo[0] - tol <= x <= fo[2]), None)
            if foto:
                fy = foto[3]
        linhas = cs.linhas(texto, obj, "ParagraphStyle/" + CASA_ESTILOS[papel], fw)
        fh = cs.altura(obj, "ParagraphStyle/" + CASA_ESTILOS[papel], linhas) + 1
        doc.text_frame(pg, fx, fy, fw, fh, paras, name=papel.replace("·", "-"), layer=lay, object_style=obj, limpo=True)

    def fonte_grafico(self, family: str, weight: int, italic: bool):
        """Fonte dos textos das peças do NXtab: Arial Narrow na linha de apoio; o resto como no capítulo."""
        if family.lower().startswith("arial narrow"):
            st = "Bold" if (weight or 400) >= 600 else "Regular"
            return "Arial Narrow", (st + " Italic" if italic else st)
        return self.fonte(family, weight, italic)

    def run_attrs(self, r: dict) -> dict:
        font, style = self.fonte(r["family"], r["weight"], r["italic"])
        color, _ = self.cor(r["color"])
        size = round(r["size"] * self.K, 2)
        trk = round(r["ls"] / r["size"] * 1000) if r["size"] else 0
        return {"font": font, "FontStyle": style, "PointSize": size, "FillColor": color or "Color/Black", "Tracking": trk}

    # ------------------------------------------------------------- estilos de parágrafo
    def estilo(self, nome: str, base: dict, para: dict | None = None) -> str:
        nome = safe_name(nome.replace("·", "-"))
        if nome not in self.style_defs:
            a = dict(base)
            if para:
                lh = para.get("lh")
                if lh:
                    a["leading"] = round(lh * self.K, 2)
                a["Justification"] = {"center": "CenterAlign", "right": "RightAlign", "end": "RightAlign",
                                      "justify": "LeftJustified"}.get(para.get("align"), "LeftAlign")
            a.setdefault("Hyphenation", "false")
            self.style_defs[nome] = a
            self.doc.para_style(nome, **a)
        return nome

    def paras_da_casa(self, paras: list[dict], estilo: str) -> list[Para]:
        """Texto com estilo da casa: só o estilo e as marcas de prova; o resto vem do estilo."""
        out = []
        for p in paras:
            runs = [r for r in p["runs"] if r["text"]]
            if not runs:
                continue
            rr = []
            for r in runs:
                cs = None
                if "tbd" in (r.get("cls") or ""):
                    self.doc.char_style("Prova - pendência", FillColor=self.cor("rgb(224,30,112)")[0])
                    cs = "Prova - pendência"
                rr.append(Run(r["text"], char_style=cs))
            out.append(Para(rr, estilo))
        return out

    def para_casa(self, p: dict, runs: list[dict], estilo: str) -> Para:
        """Parágrafo só com o estilo da casa, no corpo do estilo (sem variação de tamanho); por trecho, só o branco
        quando o texto vai sobre fundo escuro. O alinhamento da prova entra no parágrafo quando difere do estilo."""
        sd = self.casa.par("ParagraphStyle/" + estilo)
        rr = []
        for r in runs:
            ra = self.run_attrs(r)
            cs = None
            if "tbd" in (r.get("cls") or ""):
                self.doc.char_style("Prova - pendência", FillColor=self.cor("rgb(224,30,112)")[0])
                cs = "Prova - pendência"
            branco = ra["FillColor"] == "Color/Paper"
            rr.append(Run(r["text"], char_style=cs,      # corpo do estilo, sem variação (Mário Fernando, 26/11/2026)
                          color="Color/Paper" if branco and not cs else None))
        ov = {}
        just = {"center": "CenterAlign", "right": "RightAlign", "end": "RightAlign", "justify": "LeftJustified"}.get(p.get("align"), "LeftAlign")
        if just != sd["just"]:
            ov["Justification"] = just
        return Para(rr, estilo, ov)

    def converter_paras(self, paras: list[dict], role_override: str | None = None) -> tuple[list[Para], float | None]:
        out: list[Para] = []
        prev_base = None
        for p in paras:
            runs = [r for r in p["runs"] if r["text"]]
            if not runs:
                continue
            first = next((r for r in runs if r["text"].strip()), runs[0])
            base = self.run_attrs(first)
            papel = role_override or p["role"]
            if self.casa and papel in CASA_PAPEIS and self.casa.tem("ParagraphStyle/" + CASA_PAPEIS[papel]):
                out.append(self.para_casa(p, runs, CASA_PAPEIS[papel]))
                prev_base = p["base1"]
                continue
            nome = self.estilo(("Retro 2026 - " + papel) if self.base else papel, base, p)
            sd = self.style_defs[nome]
            lead = round(p["lh"] * self.K, 2) if p.get("lh") else None
            rr = []
            for r in runs:
                ra = self.run_attrs(r)
                cs = None
                if "tbd" in (r.get("cls") or ""):
                    cs = self.doc.char_style("Prova - pendência", FillColor=self.doc.color((224, 30, 112), "ES Brasil Rosa")) and "Prova - pendência"
                rr.append(Run(r["text"], char_style=cs,
                              font=ra["font"] if ra["font"] != sd.get("font") else None,
                              style=ra["FontStyle"] if ra["FontStyle"] != sd.get("FontStyle") else None,
                              size=ra["PointSize"] if abs(ra["PointSize"] - sd.get("PointSize", 0)) > 0.05 else None,
                              color=None if cs else (ra["FillColor"] if ra["FillColor"] != sd.get("FillColor") else None),
                              tracking=ra["Tracking"] if ra["Tracking"] != sd.get("Tracking") else None))
            ov = {}
            just = {"center": "CenterAlign", "right": "RightAlign", "end": "RightAlign", "justify": "LeftJustified"}.get(p.get("align"), "LeftAlign")
            if just != sd.get("Justification"):
                ov["Justification"] = just
            if prev_base is not None and lead:
                sb = (p["base0"] - prev_base) * self.K - lead
                if sb > 0.3:
                    ov["SpaceBefore"] = f"{sb:.2f}"
            out.append(Para(rr, nome, ov, leading=lead if lead and abs(lead - sd.get("leading", 0)) > 0.05 else None))
            prev_base = p["base1"]
        return out, None

    # ------------------------------------------------------------- arquivos vinculados
    def render_pdf(self, svg: str, fn: str, w: float | None, h: float | None) -> tuple[float, float]:
        """Grava Links/<fn> (PDF vetorial) e o SVG irmão; devolve o tamanho real da página do PDF em pt."""
        import pymupdf
        if w is None:
            m = re.search(r'viewBox="[\d.\s-]*?([\d.]+)\s+([\d.]+)"', svg)
            w, h = (float(m.group(1)), float(m.group(2))) if m else (300, 150)
        (self.out / "Links" / fn.replace(".pdf", ".svg")).write_text(svg, encoding="utf8")
        html = (f"<!doctype html><html><head><meta charset='utf-8'><style>@page{{size:{w}px {h}px;margin:0}}"
                f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden}}svg{{display:block}}</style></head>"
                f"<body>{svg}</body></html>")
        pg = self.pdf_page
        pg.set_content(html)
        pg.wait_for_timeout(120)
        pg.pdf(path=str(self.out / "Links" / fn), width=f"{w}px", height=f"{h}px", print_background=True,
               page_ranges="1", margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        r = pymupdf.open(str(self.out / "Links" / fn))[0].rect
        self.graficos.append(fn)
        return r.width, r.height

    def salvar_link(self, data_uri: str, nome: str) -> tuple[str, str, float, float] | None:
        m = re.match(r"data:([^;,]+)(;base64)?,(.*)", data_uri, re.S)
        if m:
            mime, b64, payload = m.groups()
            raw = base64.b64decode(payload) if b64 else payload.encode()
        else:
            try:
                if data_uri.startswith("file:"):
                    from urllib.parse import unquote, urlparse
                    raw = Path(unquote(urlparse(data_uri).path)).read_bytes()
                else:
                    import urllib.request
                    raw = urllib.request.urlopen(data_uri, timeout=30).read()
                mime = "image/svg+xml" if data_uri.lower().split("?")[0].endswith(".svg") else "image/*"
            except Exception as e:  # noqa: BLE001
                self.avisos.append(f"Não consegui copiar a imagem {data_uri[:90]} ({e.__class__.__name__}); a moldura ficou vazia.")
                return None
        h = hashlib.sha1(raw).hexdigest()
        if h in self.links:
            fn = self.links[h]
        else:
            if "svg" in mime:
                fn = f"{nome}.pdf"
                self.render_pdf(raw.decode("utf8", "ignore"), fn, None, None)
            else:
                im = Image.open(io.BytesIO(raw))
                ext = {"JPEG": "jpg", "PNG": "png"}.get(im.format)
                if ext is None:
                    ext = "png"
                    buf = io.BytesIO(); im.save(buf, "PNG"); raw = buf.getvalue()
                fn = f"{nome}.{ext}"
                (self.out / "Links" / fn).write_bytes(raw)
            self.links[h] = fn
        p = self.out / "Links" / fn
        if fn.endswith(".pdf"):
            import pymupdf
            r = pymupdf.open(str(p))[0].rect
            return fn, "pdf", r.width, r.height
        im = Image.open(p)
        dpi = im.info.get("dpi", (72, 72))
        dx, dy = (float(dpi[0]) or 72), (float(dpi[1]) or 72)
        if not (10 <= dx <= 2400 and 10 <= dy <= 2400):
            dx = dy = 72.0
        return fn, ("jpg" if fn.endswith(".jpg") else "png"), im.width * 72 / dx, im.height * 72 / dy

    # ------------------------------------------------------------- páginas
    def construir(self):
        K, doc = self.K, self.doc
        flows = []
        nfoto = 0
        for pi, page in enumerate(self.d["pages"]):
            pg = doc.add_page()
            ng = 0
            nfoto = 0
            fotos_da_pagina = [(f["x"] * self.K, f["y"] * self.K, (f["x"] + f["w"]) * self.K, (f["y"] + f["h"]) * self.K)
                               for f in page["items"] if f.get("type") == "image" and f.get("inPhoto")]
            for it in page["items"]:
                t = it["type"]
                lay = it.get("layer")
                if self.base and lay != "prova" and t != "text":
                    lay = "textos" if t == "table" else "fundos"
                if t == "rect":
                    if it.get("w", 0) * K < 0.2 or it.get("h", 0) * K < 0.2:
                        continue
                    if self.base and (it.get("name") or "").startswith("Rodapé"):
                        continue
                    if it.get("fill"):
                        c, a = self.cor(it["fill"])
                        if c:
                            doc.rect(pg, it["x"] * K, it["y"] * K, it["w"] * K, it["h"] * K, fill=c,
                                     radius=(it.get("radius") or 0) * K, opacity=a, name=it.get("name"), layer=lay)
                    if it.get("stroke"):
                        c, a = self.cor(it["stroke"])
                        sw = it.get("strokeW", 1) * K
                        doc.rect(pg, it["x"] * K + sw / 2, it["y"] * K + sw / 2, it["w"] * K - sw, it["h"] * K - sw,
                                 stroke=c, stroke_w=sw, radius=(it.get("radius") or 0) * K, name=it.get("name"), layer=lay)
                elif t == "text":
                    papel = it.get("role", "")
                    if self.base and papel == "Rodapé":
                        continue          # o paginador vem da página-mestre da revista
                    if self.base and papel == "Cartola":
                        continue          # retranca e selo vêm da página-mestre (base V5)
                    if self.base and lay != "prova":
                        lay = "textos"
                    if self.base and papel in CASA_ESTILOS:
                        paras = self.paras_da_casa(it["paras"], CASA_ESTILOS[papel])
                    else:
                        paras, _ = self.converter_paras(it["paras"])
                    if not paras:
                        continue
                    x, y, w, h = it["x"] * K, it["y"] * K, it["w"] * K, it["h"] * K
                    if self.casa and papel in OBJ_FOTO and self.casa.tem(OBJ_FOTO[papel]):
                        self.moldura_de_foto(doc, pg, it, papel, paras, x, y, w, h, fotos_da_pagina, lay)
                        continue
                    if it.get("rot") == 90:
                        doc.text_frame(pg, x - 1, y, w + 2, h + 6, paras, name=papel.replace("·", "-"), layer=lay, rot=90)
                        continue
                    extra = max(2.0, w * 0.02)
                    al = (it["paras"][0].get("align") or "left")
                    if al in ("right", "end"):
                        x -= extra
                    elif al == "center":
                        x -= extra / 2
                    base = (it["paras"][0]["base0"] - it["y"]) * K
                    doc.text_frame(pg, x, y, w + extra, max(h, 4) + 2, paras, autosize=True,
                                   name=it.get("role", "Texto").replace("·", "-"), layer=lay,
                                   baseline=base if base > 0 else None)
                elif t == "flow":
                    flows.append(dict(page=pg, x=it["x"] * K, y=it["y"] * K, w=it["w"] * K, h=it["h"] * K,
                                      columns=it["columns"], gutter=it["gap"] * K, order=it["order"],
                                      baseline=(it["base0"] * K) if it.get("base0") else None))
                elif t == "image":
                    is_qr = "qr" in it["alt"].lower() or "qr" in it.get("cls", "")
                    if is_qr:
                        it["inPhoto"] = False
                        nome = "qr-" + slug(it["alt"].lower().replace("qr code", ""), 30)
                    elif self.base and any(c in it.get("cls", "").split() for c in ("selo", "logo-esb")):
                        continue          # selo e logo da ES Brasil estão na página-mestre (base V5)
                    elif "selo" in it.get("cls", ""):
                        nome = "selo-retrospectiva"
                    elif it["inPhoto"]:
                        nfoto += 1
                        nome = f"p{pi + 1}-foto-{nfoto}-{slug(it['alt'], 34)}"
                    else:
                        nome = slug(it["alt"] or "imagem", 40)
                    info = self.salvar_link(it["src"], nome)
                    cx, cy, cw, ch = (it["clip"][k] * K for k in ("x", "y", "w", "h"))
                    if not info:
                        doc.rect(pg, cx, cy, cw, ch, fill=doc.color((221, 225, 230)), name="FALTA imagem", layer=lay)
                        continue
                    fn, kind, gw, gh = info
                    x, y, w, h = it["x"] * K, it["y"] * K, it["w"] * K, it["h"] * K
                    fit = it.get("fit", "fill")
                    if fit == "cover":
                        sx = sy = max(w / gw, h / gh)
                    elif fit in ("contain", "scale-down"):
                        sx = sy = min(w / gw, h / gh)
                    elif fit == "none":
                        sx = sy = 1.0
                    else:
                        sx, sy = w / gw, h / gh
                    pos = [float(v[:-1]) / 100 if v.endswith("%") else 0.5 for v in (it.get("pos") or "50% 50%").split()[:2]]
                    tx, ty = x + (w - gw * sx) * pos[0], y + (h - gh * sy) * pos[1]
                    # Fotos do capítulo (inclusive a de abertura) usam o estilo de objeto da base V5,
                    # "Frame Box de foto 2026" (cantos arredondados), pedido de 26/11/2026.
                    estilo_foto = ESTILO_OBJETO_FOTO if (self.base and it["inPhoto"] and not is_qr) else None
                    doc.placed(pg, cx, cy, cw, ch, f"file:Links/{fn}", kind, gw, gh, sx, sy, tx, ty,
                               radius=(it.get("radius") or 0) * K, name=fn, layer=lay, object_style=estilo_foto)
                    if it["inPhoto"]:
                        self.fotos.append({"pagina": pi + 1, "arquivo": fn, "px": f"{it['nw']} x {it['nh']}",
                                           "uso_cm": f"{it['w'] * K / 28.3465:.1f} x {it['h'] * K / 28.3465:.1f}".replace(".", ","),
                                           "credito": it.get("credito", ""), "buscar": it.get("busca", ""), "alt": it["alt"]})
                elif t == "svg":
                    ng += 1
                    fn = f"p{pi + 1}-grafico-{ng}-{slug(it['title'], 34)}.pdf"
                    gw, gh = self.render_pdf(it["svg"], fn, it["w"], it["h"])
                    feito = None
                    if self.vetor:
                        # Peça do NXtab em objetos nativos do InDesign (26/11/2026): caminhos vetoriais, textos
                        # editáveis e degradês, num grupo só. O PDF e o SVG ficam em Links/ como referência.
                        try:
                            larguras = self.pdf_page.evaluate(JS_MEDIR) if self.pdf_page else None
                            feito = desenhar_svg(doc, pg, it["svg"], it["x"] * K, it["y"] * K, it["w"] * K, it["h"] * K,
                                                 cor=lambda rgb: self.cor(f"rgb({rgb[0]},{rgb[1]},{rgb[2]})")[0],
                                                 fonte=self.fonte_grafico, salvar_imagem=self.salvar_link,
                                                 larguras=larguras, layer=lay, nome=fn[:-4], avisos=self.avisos,
                                                 casa=self.casa)
                        except Exception as e:  # noqa: BLE001
                            self.avisos.append(f"{fn}: não consegui converter em vetores do InDesign "
                                               f"({e.__class__.__name__}: {e}); a peça foi vinculada como PDF.")
                    if not feito:
                        cx, cy, cw, ch = (it["clip"][k] * K for k in ("x", "y", "w", "h"))
                        s = K / 0.75
                        doc.placed(pg, cx, cy, cw, ch, f"file:Links/{fn}", "pdf", gw, gh, s, s, it["x"] * K, it["y"] * K,
                                   name=fn, layer=lay)
                elif t == "table":
                    self.tabela(pg, it)
        self.historia(flows)

    def tabela(self, pg: int, it: dict):
        K, doc = self.K, self.doc
        rows = []
        ncol = max(len(r["cells"]) for r in it["rows"])
        widths = None
        for r in it["rows"]:
            if len(r["cells"]) == ncol:
                widths = [c["w"] * K for c in r["cells"]]
                break
        for ri, r in enumerate(it["rows"]):
            cells = []
            for ci, c in enumerate(r["cells"]):
                role = "Tabela - cabeçalho" if c["header"] else ("Tabela - total" if c.get("total") else
                                                                ("Tabela - primeira coluna" if ci == 0 else "Tabela - célula"))
                paras, _ = self.converter_paras(c["paras"], role_override=role)
                fill, _a = self.cor(c["bg"])
                if fill == "Color/Paper":
                    fill = None
                sb = None
                if c.get("bb"):
                    bc, _ = self.cor(c["bb"][0])
                    sb = (bc, c["bb"][1] * K)
                t, l, b, rr = (v * K for v in c["pad"])
                cells.append({"paras": paras or [Para([Run("")])], "fill": fill, "insets": (t, l, b, rr), "stroke_bottom": sb,
                              "valign": {"top": "TopAlign", "bottom": "BottomAlign"}.get(c["valign"], "CenterAlign")})
            while len(cells) < ncol:
                cells.append({"paras": [Para([Run("")])]})
            rows.append({"height": r["h"] * K, "cells": cells})
        doc.table_frame(pg, it["x"] * K, it["y"] * K, it["w"] * K + 1, it["h"] * K + 6, rows, widths,
                        header_rows=it.get("header", 1), name="Tabela", layer=it.get("layer"))

    # ------------------------------------------------------------- texto corrido
    def historia(self, flows: list[dict]):
        if not flows:
            return
        K, doc, d = self.K, self.doc, self.d
        body = d.get("body") or {"family": "Crimson Pro", "weight": 400, "italic": False, "size": 14.6, "lh": 17.7, "ls": 0, "color": "rgb(22,28,36)", "indent": 14.6}
        inter = d.get("inter") or {"family": "Inter", "weight": 800, "italic": False, "size": 12.5, "lh": 17.7, "ls": 0.3, "color": "rgb(0,66,123)", "mt": 8.75, "mb": 3.1}
        size = round(body["size"] * K * 2) / 2
        lead = round((body["lh"] or body["size"] * 1.2) * K * 2) / 2
        if self.base:
            return self.historia_casa(flows, lead)
        font, st = self.fonte(body["family"], body["weight"], False)
        cor_corpo, _ = self.cor(body["color"])
        doc.para_style("Corpo", font=font, FontStyle=st, PointSize=size, leading=lead, FillColor=cor_corpo,
                       Justification="LeftJustified", FirstLineIndent=round(body.get("indent", body["size"]) * K, 2),
                       Hyphenation="true", AppliedLanguage=doc.lang)
        doc.para_style("Corpo - abertura", based_on="Corpo", FirstLineIndent=0, DropCapCharacters=1, DropCapLines=3)
        doc.para_style("Corpo - continuação", based_on="Corpo")
        f_i, st_i = self.fonte(inter["family"], inter["weight"], False)
        cor_i, _ = self.cor(inter["color"])
        doc.para_style("Intertítulo", font=f_i, FontStyle=st_i, PointSize=round(inter["size"] * K, 2), leading=lead,
                       FillColor=cor_i, Tracking=round(inter["ls"] / inter["size"] * 1000), SpaceBefore=round(inter["mt"] * K, 2),
                       SpaceAfter=round(inter["mb"] * K, 2), KeepWithNext=2, Hyphenation="false", Justification="LeftAlign")
        doc.para_style("Aspa destacada", font="Inter", FontStyle="SemiBold", PointSize=round(12.5 * K, 2), leading=round(16.9 * K, 2),
                       FillColor=doc.color((0, 28, 67), "ES Brasil Navy"), Hyphenation="false", SpaceBefore=4, SpaceAfter=4)
        cap = d.get("cap") or {"family": "Inter", "weight": 900, "italic": False, "color": "rgb(0,28,67)"}
        f_c, st_c = self.fonte(cap["family"], cap["weight"], False)
        doc.char_style("Capitular", font=f_c, FontStyle=st_c, FillColor=self.cor(cap["color"])[0])
        doc.char_style("Prova - aspa verificada", Underline="true", UnderlineColor=doc.color((217, 238, 252), "Prova Aspa verificada"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Prova - aspa montada", Underline="true", UnderlineColor=doc.color((255, 227, 191), "Prova Aspa montada"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Prova - pendência", FillColor=doc.color((224, 30, 112), "ES Brasil Rosa"))
        doc.char_style("Prova - dado atualizado", Underline="true", UnderlineColor=doc.color((221, 245, 227), "Prova Dado atualizado"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Fim de texto", font="Inter", FontStyle="Black", FillColor=doc.color((224, 30, 112), "ES Brasil Rosa"))
        doc.char_style("Negrito", FontStyle=CORPO_ESTILOS[700])
        doc.char_style("Itálico", FontStyle="Cond Italic")
        self.fontes_usadas.update({"Black", st_i, st_c})

        paras = []
        for blk in d["story"]:
            tag, cls = blk["tag"], blk.get("cls") or ""
            if tag in ("h2", "h3", "h4", "h5"):
                style = "Intertítulo"
            elif tag == "blockquote":
                style = "Aspa destacada"
            elif "cap" in cls.split():
                style = "Corpo - abertura"
            else:
                style = "Corpo"
            runs = []
            for k, r in enumerate(blk["runs"]):
                c = r.get("cls") or ""
                cs = None
                if "aspa-v" in c:
                    cs = "Prova - aspa verificada"
                elif "mont" in c:
                    cs = "Prova - aspa montada"
                elif "fim" in c.split():
                    cs = "Fim de texto"
                elif "tbd" in c:
                    cs = "Prova - pendência"
                elif "novo" in c.split():
                    cs = "Prova - dado atualizado"
                elif "negrito" in c:
                    cs = "Negrito"
                elif "italico" in c:
                    cs = "Itálico"
                text = r["text"]
                if cs == "Fim de texto":
                    text = " " + text
                runs.append(Run(text, char_style=cs))
            if style == "Corpo - abertura" and runs and runs[0].text:
                t0 = runs[0]
                runs = [Run(t0.text[0], char_style="Capitular"), Run(t0.text[1:], char_style=t0.char_style)] + runs[1:]
            paras.append(Para(runs, style))
        flows.sort(key=lambda f: f["order"])
        doc.threaded_story(flows, paras, name="Texto corrido")

    def historia_casa(self, flows: list[dict], lead: float):
        """Texto corrido com os estilos da revista: Texto geral 2026 (Minion Pro Cond 11/12), abertura com
        capitular de 3 linhas e intertítulo em caixa alta e baixa."""
        doc, d = self.doc, self.d
        size = 11.0
        rosa = self.cor("rgb(224,30,112)")[0]
        doc.char_style("Prova - aspa verificada", Underline="true", UnderlineColor=doc.color((217, 238, 252), "Prova Aspa verificada"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Prova - aspa montada", Underline="true", UnderlineColor=doc.color((255, 227, 191), "Prova Aspa montada"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Prova - pendência", FillColor=rosa)
        doc.char_style("Prova - dado atualizado", Underline="true", UnderlineColor=doc.color((221, 245, 227), "Prova Dado atualizado"),
                       UnderlineWeight=round(lead - 1.5, 2), UnderlineOffset=-round(size * 0.28, 2))
        doc.char_style("Fim de texto", font="Inter", FontStyle="Black", FillColor=rosa)
        doc.char_style("Negrito", FontStyle=CORPO_ESTILOS[700])
        doc.char_style("Itálico", FontStyle="Cond Italic")
        paras = []
        for blk in d["story"]:
            tag, cls = blk["tag"], blk.get("cls") or ""
            if tag in ("h2", "h3", "h4", "h5"):
                style = "Intertexto 2026"
            elif "cap" in cls.split():
                style = "Texto fatual cap 3 linhas 2026"
            else:
                style = "Texto geral 2026"
            runs = []
            for r in blk["runs"]:
                c = r.get("cls") or ""
                cs = ("Prova - aspa verificada" if "aspa-v" in c else "Prova - aspa montada" if "mont" in c else
                      "Fim de texto" if "fim" in c.split() else "Prova - pendência" if "tbd" in c else
                      "Prova - dado atualizado" if "novo" in c.split() else "Negrito" if "negrito" in c else
                      "Itálico" if "italico" in c else None)
                text = (" " + r["text"]) if cs == "Fim de texto" else r["text"]
                runs.append(Run(text, char_style=cs))
            if style.startswith("Texto fatual") and runs and runs[0].text:
                t0 = runs[0]
                runs = [Run(t0.text[0], char_style="Capitular 2026"), Run(t0.text[1:], char_style=t0.char_style)] + runs[1:]
            paras.append(Para(runs, style))
        flows.sort(key=lambda f: f["order"])
        for fr in flows:
            fr["baseline"] = None
        doc.threaded_story(flows, paras, name="Texto corrido")

    def retranca(self) -> str | None:
        """Nome da editoria para a retranca da página direita da mestre: a cartola das páginas que não é
        "retrospectiva 2026" (no HTML, header.top .tag)."""
        for pg in self.d.get("pages", []):
            for it in pg.get("items", []):
                if it.get("type") == "text" and it.get("role") == "Cartola":
                    t = " ".join(r["text"] for p in it["paras"] for r in p["runs"]).strip()
                    if t and t.lower() != "retrospectiva 2026":
                        return t.lower()
        return None

    # ------------------------------------------------------------- saída
    def salvar(self, pagina: int | None = None):
        if self.base:
            self.info_base = self.doc.save_on_base(str(self.base), str(self.out / f"{self.nome}.idml"), title=self.nome,
                                                   page_start=pagina, retranca=self.retranca())
        else:
            self.doc.save(str(self.out / f"{self.nome}.idml"), title=self.nome)


def textos(exp: Exportador, out: Path):
    from docx import Document
    from docx.shared import Pt
    import openpyxl
    d = exp.d
    t = out / "Textos"
    linhas, doc = [], Document()
    stl = doc.styles["Normal"]; stl.font.name = "Minion Pro"; stl.font.size = Pt(9.5)
    total = 0
    for blk in d["story"]:
        txt = "".join(r["text"] for r in blk["runs"]).replace("■", "").strip()
        if not txt:
            continue
        if blk["tag"] in ("h2", "h3", "h4", "h5"):
            linhas.append(f"\n## {txt}\n")
            doc.add_heading(txt, level=2)
        else:
            linhas.append(txt + "\n")
            total += len(txt) + 1
            par = doc.add_paragraph()
            for r in blk["runs"]:
                run = par.add_run(r["text"].replace("■", ""))
                c = r.get("cls") or ""
                if "aspa-v" in c:
                    run.font.highlight_color = 9  # azul-claro (validar)
                elif "mont" in c:
                    run.font.highlight_color = 7  # amarelo (aspa montada)
                elif "novo" in c.split():
                    run.font.highlight_color = 4  # verde (dado atualizado pela rotina de dados quentes)
    corrido = sum(len("".join(r["text"] for r in b["runs"]).replace("■", "").strip()) for b in d["story"] if b["tag"] not in ("h2", "h3", "h4", "h5"))
    cab = f"{exp.nome} · texto corrido\nCaracteres com espaços (corpo, sem intertítulos): {corrido}\n\n"
    (t / "texto-corrido.txt").write_text(cab + "".join(linhas), encoding="utf8")
    doc.save(t / "texto-corrido.docx")

    wb = openpyxl.Workbook(); wb.remove(wb.active)
    n = 0
    for pi, page in enumerate(d["pages"]):
        for it in page["items"]:
            if it["type"] != "table":
                continue
            n += 1
            ws = wb.create_sheet(f"p{pi + 1}-tabela-{n}")
            for r in it["rows"]:
                ws.append([" ".join("".join(x["text"] for x in p["runs"]) for p in c["paras"]) for c in r["cells"]])
    if n:
        wb.save(t / "tabelas.xlsx")
    if d.get("banco"):
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Banco de aspas"
        for i, row in enumerate(d["banco"]):
            ws.append(row + ([d["bancoLinks"][i]] if i and d["bancoLinks"][i] else (["Link"] if i == 0 else [])))
        wb.save(t / "banco-de-aspas.xlsx")
    with open(t / "fotos-buscar-original.txt", "w", encoding="utf8") as fh:
        fh.write("Fotos do capítulo: arquivo provisório em Links/ e onde buscar o original em alta (300 dpi no tamanho de uso)\n\n")
        for f in exp.fotos:
            fh.write(f"Página {f['pagina']} — {f['arquivo']} ({f['px']} px; uso {f['uso_cm']} cm)\n  {f['credito']}\n  {f['buscar'] or 'Sem etiqueta Buscar original'}\n\n")
    if d.get("fechamento"):
        (t / "para-o-fechamento.txt").write_text("Para o fechamento da edição\n\n" + "\n".join("- " + x for x in d["fechamento"]), encoding="utf8")
    return corrido


def leia_me_base(exp: Exportador, out: Path, corrido: int):
    info = getattr(exp, "info_base", {}) or {}
    txt = f"""{exp.nome} · pacote para o InDesign
Gerado pela skill da Retrospectiva 2026 da revista ES Brasil a partir das páginas aprovadas, sobre a base da
Retrospectiva ("MATÉRIA 1 - RETROSPECTIVA 2026 - ESB V5").

O que tem aqui
- {exp.nome}.idml: o capítulo em {len(exp.d['pages'])} páginas de 20,5 x 27,5 cm, espelhadas, com sangria de 3 mm, a
  grade da revista (margens de 22 e 15 mm, 17 mm na lombada e 12 mm do lado de fora, 3 colunas) e os estilos, as cores,
  as camadas e as páginas-mestre da base.
- Links: fotos, selo, QR Codes e gráficos do NXtab. Cada gráfico vem em PDF vetorial (é o que está na página) e em SVG.
- Referencia: a prova aprovada, em PDF e em JPG por página. É o gabarito para conferir a montagem.
- Textos: texto corrido em .docx e .txt ({corrido} caracteres com espaços), tabelas em .xlsx, banco de aspas, fotos a buscar e pendências.

Como abrir
1. No InDesign: Arquivo > Abrir > {exp.nome}.idml. Em seguida, salve como .indd nesta mesma pasta.
2. Fontes: o documento usa Inter, Minion Pro e Roboto Condensed (legendas, créditos e textos de box) do Adobe Fonts; o
   InDesign oferece ativá-las ao abrir.
3. Vínculos: se o painel Vínculos mostrar arquivos ausentes, revincule um deles à pasta Links e aceite procurar os demais ali.
   A página-mestre usa os arquivos da revista: fundo "BG Retrospectiva 2025.psd" (M:/ES Brasil/ESB 238 - RETRO2026/IMAGENS/Base),
   selo, logo da ES Brasil e paginador (M:/ES Brasil/ESB 226, 227 e 232).
4. Numeração: as páginas começam em {info.get('pagina_inicial', 2)}. Ajuste em Opções de numeração e seção com o número do espelho do NX Pages.

Como está montado
- Página-mestre "{info.get('mestre', 'R-Retrospectiva 2026')}": cópia da "A-Master" da base V5, com fundo da Retrospectiva,
  retranca "RETROSPECTIVA 2026" e selo na página esquerda, logo da ES Brasil e retranca da editoria
  ("{(info.get('retranca') or '').upper()}") na direita, abas de cor e paginador. Para trocar a cor da aba, mostre ou esconda as
  abas na mestre.
- Estilos da casa usados pelo nome, sem derivados: Texto geral 2026 (Minion Pro Cond 11/12), Texto fatual cap 3 linhas 2026
  (abertura com capitular), Intertexto 2026 (Inter Black 11/12, caixa alta e baixa), Título 36pt 2026 (branco, centralizado),
  Lead 2026, Assinatura 2026, Legenda 2026 e Legenda dentro foto 2026 (Roboto Condensed 9,5/11) e Créditos 2026 (Roboto
  Condensed Light 7, na vertical, ao lado da foto). O box usa os estilos "Retro 2026 - ...".
- Camadas: textos em TEXTOS, fotos, gráficos e fundos em FUNDOS E IMAGENS, e as marcas de prova em "Prova (não imprime)".
- O texto corrido é uma história só, encadeada por todas as páginas. Confira o sinal de texto excedente (+ vermelho) na última moldura.
- Cores: azul, rosa, preto e branco usam as amostras CMYK da casa (Azul ES Brasil 2026, VermelhoRetro2025, Preto 90%, Paper);
  as demais cores das tabelas e da linha do tempo estão em RGB, com nome. Converta para CMYK no padrão da gráfica.

Marcações de prova (saem na versão final)
- Camada "Prova (não imprime)": etiquetas rosa "Buscar original" e o espaço reservado para o mapa de criação manual.
- Estilos de caractere "Prova - aspa verificada" (fundo azul-claro), "Prova - aspa montada" (fundo laranja) e "Prova - dado atualizado"
  (fundo verde-claro): depois da validação, edite cada estilo e desligue o sublinhado.
- "Prova - pendência" (rosa): repórter e dados que ainda dependem de divulgação.
"""
    if exp.avisos:
        txt += "\nAvisos da exportação\n" + "\n".join("- " + a for a in exp.avisos) + "\n"
    (out / "Leia-me.txt").write_text(txt, encoding="utf8")


def leia_me(exp: Exportador, out: Path, corrido: int):
    if exp.base:
        return leia_me_base(exp, out, corrido)
    fontes = ", ".join(sorted(exp.fontes_usadas))
    txt = f"""{exp.nome} · pacote para o InDesign
Gerado pela skill da Retrospectiva 2026 da revista ES Brasil a partir das páginas aprovadas.

O que tem aqui
- {exp.nome}.idml: o capítulo em {len(exp.d['pages'])} páginas de 20,5 x 27,5 cm, com sangria de 3 mm.
- Links: fotos, selo, QR Codes e gráficos. Cada gráfico vem em PDF vetorial (é o que está na página) e em SVG, para editar no Illustrator.
- Document fonts: Inter ({fontes}), com a licença OFL.
- Referencia: a prova aprovada, em PDF e em JPG por página. É o gabarito para conferir a montagem.
- Textos: texto corrido em .docx e .txt ({corrido} caracteres com espaços), tabelas em .xlsx, banco de aspas, fotos a buscar e pendências do fechamento.

Como abrir
1. No InDesign 2018 ou mais novo: Arquivo > Abrir > {exp.nome}.idml. Em seguida, salve como .indd nesta mesma pasta.
2. Vínculos: se o painel Vínculos mostrar arquivos ausentes, selecione um, clique em Revincular e aponte a pasta Links. O InDesign oferece procurar os demais na mesma pasta; aceite.
3. Fontes: ative a Inter (pasta Document fonts) e a Minion Pro pela Adobe Fonts. O texto corrido usa o estilo de parágrafo "Corpo" ({CORPO_FONTE} {CORPO_ESTILOS[400]}). Se a fonte tiver outro nome no seu computador, troque só no estilo "Corpo" e o texto todo acompanha.

Como está montado
- O texto corrido é uma história só, encadeada por todas as páginas (molduras "Texto corrido 1, 2, 3..."). Se a Minion ocupar mais ou menos espaço que a fonte da prova, o texto reflui sozinho. Confira o sinal de texto excedente (+ vermelho) na última moldura.
- Título, linha fina, legendas, créditos, cartola, rodapé, box "2026 em Números" e linha do tempo são molduras de texto editáveis, com estilos de parágrafo nomeados.
- As tabelas são tabelas nativas do InDesign.
- Os gráficos entram como PDF vinculado. Para mudar um número, edite o SVG no Illustrator, salve como PDF com o mesmo nome e atualize o vínculo.
- As cores estão em RGB, com os nomes da paleta ES Brasil no painel Amostras. Converta para CMYK no padrão da gráfica.

Marcações de prova (saem na versão final)
- Camada "Prova (não imprime)": etiquetas rosa "Buscar original" sobre as fotos provisórias. A camada já está marcada para não imprimir; apague-a quando as fotos em alta entrarem.
- Estilos de caractere "Prova - aspa verificada" (fundo azul-claro) e "Prova - aspa montada" (fundo laranja): depois que a produção validar as aspas, edite os dois estilos e desligue o sublinhado. O texto fica limpo de uma vez.
- "Prova - pendência" (rosa): número de página "00", repórter e dados que ainda dependem de divulgação.
- "Prova - dado atualizado" (fundo verde-claro): números trocados pela rotina de dados quentes; confira e desligue o sublinhado do estilo.
- As fotos com etiqueta "Buscar original" são provisórias. A origem de cada uma está em Textos/fotos-buscar-original.txt.
"""
    if exp.avisos:
        txt += "\nAvisos da exportação\n" + "\n".join("- " + a for a in exp.avisos) + "\n"
    (out / "Leia-me.txt").write_text(txt, encoding="utf8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("saida")
    ap.add_argument("--nome", default=None)
    ap.add_argument("--base", default=None, help="IDML-base da revista (padrão: assets/base-retrospectiva-2026-v6.idml)")
    ap.add_argument("--sem-base", action="store_true", help="gera o IDML do zero, sem a base da revista")
    ap.add_argument("--pagina", type=int, default=None, help="número da primeira página no espelho do NX Pages")
    ap.add_argument("--graficos-vinculados", action="store_true",
                    help="vincula as peças do NXtab como PDF, em vez de convertê-las em objetos nativos do InDesign")
    a = ap.parse_args()
    base = None if a.sem_base else (Path(a.base) if a.base else (BASE_PADRAO if BASE_PADRAO.exists() else None))
    html = Path(a.html).resolve()
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"]) if CHROME else p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1000, "height": 1400}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(html.as_uri(), wait_until="networkidle")
        page.wait_for_function("document.fonts.status==='loaded'")
        page.wait_for_timeout(1500)
        # Referência: captura cada página antes de mexer no DOM.
        refs = []
        hi = ctx.new_page(); hi.set_viewport_size({"width": 1000, "height": 1400})
        hctx = br.new_context(viewport={"width": 1000, "height": 1400}, device_scale_factor=2)
        hp = hctx.new_page(); hp.goto(html.as_uri(), wait_until="networkidle")
        hp.wait_for_function("document.fonts.status==='loaded'"); hp.wait_for_timeout(1500)
        for el in hp.query_selector_all("article.page"):
            refs.append(el.screenshot(type="jpeg", quality=88))
        hctx.close(); hi.close()
        data = page.evaluate((Path(__file__).parent / "extrair.js").read_text(encoding="utf8"))
        titulo = data.get("title") or "Retrospectiva 2026"
        tema = unicodedata.normalize("NFKD", titulo.split("·")[-1]).encode("ascii", "ignore").decode()
        nome = a.nome or ("Retrospectiva2026_" + "_".join(re.findall(r"[A-Za-z0-9]+", tema))[:40])
        out = Path(a.saida).resolve() / nome
        if out.exists():
            shutil.rmtree(out)
        for sub in ("Links", "Referencia", "Textos") if base else ("Links", "Document fonts", "Referencia", "Textos"):
            (out / sub).mkdir(parents=True, exist_ok=True)
        exp = Exportador(data, out, nome, pdf_page=ctx.new_page(), base=base)
        exp.vetor = not a.graficos_vinculados
        exp.construir()
        exp.salvar(a.pagina)
        br.close()
    # referência em PNG e PDF
    ims = []
    for i, png in enumerate(refs):
        (out / "Referencia" / f"pagina-{i + 1}.jpg").write_bytes(png)
        ims.append(Image.open(io.BytesIO(png)).convert("RGB"))
    if ims:
        dpi = ims[0].width / (205 / 25.4)
        ims[0].save(out / "Referencia" / f"{nome}-prova-aprovada.pdf", save_all=True, append_images=ims[1:], resolution=dpi)
    # fontes: com a base, a Inter e a Minion Pro vêm do Adobe Fonts (ativação automática pelo documento)
    for st in ([] if base else sorted(exp.fontes_usadas)):
        fn = INTER_DIR / f"Inter-{st.replace(' ', '')}.otf"
        if fn.exists():
            shutil.copy(fn, out / "Document fonts" / fn.name)
    if INTER_LICENSE.exists() and not base:
        shutil.copy(INTER_LICENSE, out / "Document fonts" / "OFL.txt")
    corrido = textos(exp, out)
    leia_me(exp, out, corrido)
    (out / "Textos" / "extracao.json").write_text(json.dumps({"ocupacao": data.get("ocupacao"), "paginas": len(data["pages"]),
                                                            "avisos": exp.avisos}, ensure_ascii=False, indent=1), encoding="utf8")
    zipf = shutil.make_archive(str(out), "zip", root_dir=out.parent, base_dir=out.name)
    print(json.dumps({"pasta": str(out), "zip": zipf, "idml": str(out / f"{nome}.idml"), "paginas": len(data["pages"]),
                      "fotos": len(exp.fotos), "graficos": len(exp.graficos), "caracteres": corrido,
                      "ocupacao_na_prova": data.get("ocupacao"), "avisos": exp.avisos}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
