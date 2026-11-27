"""Converte uma peça do NXtab (SVG) em objetos nativos do InDesign dentro do IDML.

Em vez de vincular o gráfico como PDF, cada forma vira um caminho vetorial do InDesign (Polygon,
GraphicLine), cada texto vira uma moldura de texto editável (com estilo de parágrafo
"Retro 2026 - Gráfico - ..."), os degradês viram amostras de degradê e a foto de fundo vira uma
imagem vinculada com a transparência da peça. Tudo fica agrupado num único Group, que se move
como uma peça só e se desagrupa para editar.

Uso no exportador:

    from svg_vetor import desenhar_svg
    desenhar_svg(doc, pagina, svg, x_pt, y_pt, w_pt, h_pt, cor=..., fonte=..., salvar_imagem=..., larguras=...)

Pede o pacote svgelements (pip install --break-system-packages svgelements), usado só para ler os
caminhos (d), as formas e as transformações.
"""
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from svgelements import (Circle, CubicBezier, Close, Ellipse, Line, Matrix, Move, Path, Polygon as SPolygon,
                         Polyline, QuadraticBezier, Rect, SimpleLine, Arc)

from casa import CAP, COR, MM as MM_CASA, OBJ, PAR
from idml import NONE, attrs, f, safe_name

SVGNS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"

HERDADOS = ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "stroke-dasharray",
            "font-family", "font-size", "font-weight", "font-style", "letter-spacing", "text-anchor",
            "fill-opacity", "stroke-opacity", "visibility")

CORES_NOMEADAS = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 128, 0),
                  "blue": (0, 0, 255), "gray": (128, 128, 128), "grey": (128, 128, 128)}

ABA_MM = (20.0, 1.0)     # barrinha de cor do topo de toda peça, em mm na página
MM = 72 / 25.4            # pontos por milímetro

CAPS = {"butt": "ButtEndCap", "round": "RoundEndCap", "square": "ProjectingEndCap"}
JOINS = {"miter": "MiterEndJoin", "round": "RoundEndJoin", "bevel": "BevelEndJoin"}


URL = re.compile(r"""url\(\s*["']?#([^"')]+)["']?\s*\)""")


def _tag(el) -> str:
    return el.tag.split("}")[-1] if isinstance(el.tag, str) else ""


def _num(v, padrao=0.0) -> float:
    if v is None:
        return padrao
    m = re.match(r"\s*(-?[\d.]+(?:e-?\d+)?)", str(v))
    return float(m.group(1)) if m else padrao


def _rgb(v: str | None):
    """Cor CSS -> (r, g, b) ou None (sem cor)."""
    if not v:
        return None
    v = v.strip()
    if v in ("none", "transparent"):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        try:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return None
    m = re.match(r"rgba?\(([^)]+)\)", v)
    if m:
        p = [x for x in re.split(r"[,\s/]+", m.group(1).strip()) if x]
        return tuple(int(round(float(x.rstrip("%")) * (2.55 if x.endswith("%") else 1))) for x in p[:3])
    return CORES_NOMEADAS.get(v.lower())


def _estilo(el) -> dict:
    d = {}
    for k in HERDADOS + ("opacity", "clip-path", "display", "transform", "stop-color", "stop-opacity", "offset"):
        if el.get(k) is not None:
            d[k] = el.get(k)
    for parte in (el.get("style") or "").split(";"):
        if ":" in parte:
            k, v = parte.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def _fonte_svg(family: str) -> str:
    for nome in (family or "").split(","):
        nome = nome.strip().strip("'\"")
        if nome:
            return nome
    return "Inter"


class Conversor:
    def __init__(self, doc, page: int, cor, fonte, salvar_imagem=None, larguras=None, layer=None, nome="Gráfico",
                 avisos=None, casa=None):
        self.casa = casa      # medidas da base (casa.Casa): monta a peça com os estilos de objeto e de texto da casa
        self.doc, self.page, self.layer, self.nome = doc, page, layer, nome
        self.cor_cb, self.fonte_cb, self.salvar_imagem = cor, fonte, salvar_imagem
        self.larguras = list(larguras or [])        # comprimento medido de cada <text>, em unidades do SVG
        self.itens: list[str] = []
        self.ids: dict[str, ET.Element] = {}
        self.avisos = avisos if avisos is not None else []
        self.n_texto = 0
        self.vb = None
        self._tabela_fim = None

    # ------------------------------------------------------------------ cores e degradês
    def cor(self, rgb):
        return self.cor_cb(rgb) if rgb else None

    def pintura(self, valor: str | None, bbox, ctm: Matrix):
        """fill/stroke -> (atributos IDML de cor, opacidade da tinta)."""
        if not valor or valor == "none":
            return None, {}
        m = URL.match(valor)
        if m:
            g = self.ids.get(m.group(1))
            if g is None or _tag(g) not in ("linearGradient", "radialGradient"):
                return None, {}
            return self.degrade(g, bbox, ctm)
        rgb = _rgb(valor)
        return (self.cor(rgb), {}) if rgb else (None, {})

    def _stops(self, g):
        stops = [s for s in g if _tag(s) == "stop"]
        href = g.get("href") or g.get(XLINK)
        if not stops and href and href[1:] in self.ids:
            stops = [s for s in self.ids[href[1:]] if _tag(s) == "stop"]
        out = []
        for s in stops:
            st = _estilo(s)
            off = st.get("offset", "0")
            loc = _num(off) / (100 if str(off).strip().endswith("%") else 1)
            rgb = _rgb(st.get("stop-color", "#000"))
            out.append((self.cor(rgb) or "Color/Black", max(0.0, min(1.0, loc)) * 100))
        return out

    def degrade(self, g, bbox, ctm: Matrix):
        stops = self._stops(g)
        if not stops:
            return None, {}
        if len(stops) == 1 or _tag(g) == "radialGradient":
            if _tag(g) == "radialGradient":
                self.avisos.append(f"{self.nome}: degradê radial convertido em cor chapada (primeira parada).")
            return stops[0][0], {}
        x0, y0, x1, y1 = bbox
        unidades = g.get("gradientUnits", "objectBoundingBox")

        def val(k, padrao):
            v = g.get(k, padrao)
            return _num(v) / 100 if str(v).strip().endswith("%") else _num(v)

        gx1, gy1, gx2, gy2 = val("x1", "0"), val("y1", "0"), val("x2", "1"), val("y2", "0")
        if unidades == "userSpaceOnUse":
            a = ctm.point_in_matrix_space((gx1, gy1))
            b = ctm.point_in_matrix_space((gx2, gy2))
            sx, sy, ex, ey = a[0], a[1], b[0], b[1]
        else:   # caixa do objeto, já em pontos da página
            sx, sy = x0 + gx1 * (x1 - x0), y0 + gy1 * (y1 - y0)
            ex, ey = x0 + gx2 * (x1 - x0), y0 + gy2 * (y1 - y0)
        comp = math.hypot(ex - sx, ey - sy) or 1.0
        # InDesign mede o ângulo com o eixo y para cima; a página do IDML tem o y para baixo.
        ang = math.degrees(math.atan2(-(ey - sy), ex - sx))
        nome = self.doc.gradient(stops)
        return nome, {"start": f"{f(sx)} {f(sy)}", "length": f(comp), "angle": f(ang)}

    # ------------------------------------------------------------------ caminhos
    @staticmethod
    def _forma(el, tag):
        g = lambda k, p=0.0: _num(el.get(k), p)  # noqa: E731
        if tag == "path":
            return Path(el.get("d") or "")
        if tag == "rect":
            w, h = g("width"), g("height")
            if w <= 0 or h <= 0:
                return None
            rx, ry = el.get("rx"), el.get("ry")
            rx = _num(rx if rx is not None else ry)
            ry = _num(ry if ry is not None else rx)
            return Path(Rect(g("x"), g("y"), w, h, rx=min(rx, w / 2), ry=min(ry, h / 2)))
        if tag == "circle":
            return Path(Circle(g("cx"), g("cy"), g("r")))
        if tag == "ellipse":
            return Path(Ellipse(g("cx"), g("cy"), g("rx"), g("ry")))
        if tag == "line":
            return Path(SimpleLine(g("x1"), g("y1"), g("x2"), g("y2")))
        if tag in ("polyline", "polygon"):
            nums = [float(v) for v in re.findall(r"-?[\d.]+(?:e-?\d+)?", el.get("points") or "")]
            pts = list(zip(nums[0::2], nums[1::2]))
            if len(pts) < 2:
                return None
            return Path(SPolygon(pts) if tag == "polygon" else Polyline(pts))
        return None

    @staticmethod
    def subcaminhos(path: Path, ctm: Matrix):
        """Path do svgelements -> lista de (pontos IDML [(âncora, esquerda, direita)], aberto?) em pontos."""
        p = Path(path) * ctm
        p.reify()
        p.approximate_arcs_with_cubics()
        subs, atual, aberto = [], None, True

        def fecha():
            if atual and len(atual) >= 1:
                subs.append((atual, aberto))

        for seg in p:
            if isinstance(seg, Move):
                fecha()
                e = (seg.end.x, seg.end.y)
                atual, aberto = [[e, e, e]], True
            elif atual is None:
                continue
            elif isinstance(seg, Close):
                ini, ult = atual[0], atual[-1]
                if len(atual) > 1 and math.hypot(ini[0][0] - ult[0][0], ini[0][1] - ult[0][1]) < 1e-3:
                    ini[1] = ult[1]          # a direção de entrada do último ponto passa para o primeiro
                    atual.pop()
                aberto = False
                fecha()
                atual = None
            elif isinstance(seg, CubicBezier):
                atual[-1][2] = (seg.control1.x, seg.control1.y)
                e = (seg.end.x, seg.end.y)
                atual.append([e, (seg.control2.x, seg.control2.y), e])
            elif isinstance(seg, QuadraticBezier):
                s, c, e = atual[-1][0], (seg.control.x, seg.control.y), (seg.end.x, seg.end.y)
                c1 = (s[0] + 2 / 3 * (c[0] - s[0]), s[1] + 2 / 3 * (c[1] - s[1]))
                c2 = (e[0] + 2 / 3 * (c[0] - e[0]), e[1] + 2 / 3 * (c[1] - e[1]))
                atual[-1][2] = c1
                atual.append([e, c2, e])
            elif isinstance(seg, (Line, Arc)):
                e = (seg.end.x, seg.end.y)
                atual.append([e, e, e])
        if atual:
            fecha()
        return [(pts, ab) for pts, ab in subs if len(pts) >= 2 or not ab]

    @staticmethod
    def _bbox(subs):
        xs = [pt[0][0] for pts, _ in subs for pt in pts] + [d[0] for pts, _ in subs for pt in pts for d in pt[1:]]
        ys = [pt[0][1] for pts, _ in subs for pt in pts] + [d[1] for pts, _ in subs for pt in pts for d in pt[1:]]
        return min(xs), min(ys), max(xs), max(ys)

    @staticmethod
    def _geometria(subs) -> str:
        gs = []
        for pts, aberto in subs:
            pp = "".join(f'<PathPointType Anchor="{f(a[0])} {f(a[1])}" LeftDirection="{f(l[0])} {f(l[1])}" '
                         f'RightDirection="{f(r[0])} {f(r[1])}"/>' for a, l, r in pts)
            gs.append(f'<GeometryPathType PathOpen="{"true" if aberto else "false"}"><PathPointArray>{pp}'
                      f'</PathPointArray></GeometryPathType>')
        return f"<Properties><PathGeometry>{''.join(gs)}</PathGeometry></Properties>"

    @staticmethod
    def _transparencia(o: float) -> str:
        if o is None or o >= 0.999:
            return ""
        return f'<TransparencySetting><BlendingSetting Opacity="{f(max(0.0, o) * 100)}"/></TransparencySetting>'

    def forma(self, el, tag, st, ctm, opac):
        if tag == "rect" and self.vb and abs(_num(el.get("x")) - self.vb[0]) < 0.5 \
                and abs(_num(el.get("y")) - self.vb[1]) < 0.5 and 0 < _num(el.get("height")) <= 10:
            # barrinha do topo da peça: sempre 20 x 1 mm na página (26/11/2026), inclusive em provas antigas
            esc = math.sqrt(abs(ctm.a * ctm.d - ctm.b * ctm.c)) or 1.0
            el = ET.Element("rect", {"x": el.get("x"), "y": el.get("y"),
                                     "width": f"{ABA_MM[0] * MM / esc:.4f}", "height": f"{ABA_MM[1] * MM / esc:.4f}"})
        aba = tag == "rect" and self.vb and abs(_num(el.get("x")) - self.vb[0]) < 0.5 \
            and abs(_num(el.get("y")) - self.vb[1]) < 0.5 and 0 < _num(el.get("height")) <= 10
        caminho = self._forma(el, tag)
        if caminho is None:
            return
        subs = self.subcaminhos(caminho, ctm)
        if not subs:
            return
        bbox = self._bbox(subs)
        escala = math.sqrt(abs(ctm.a * ctm.d - ctm.b * ctm.c)) or 1.0
        fill_v = st.get("fill", "black")
        stroke_v = st.get("stroke", "none")
        fill, gf = self.pintura(fill_v, bbox, ctm)
        stroke, gs = self.pintura(stroke_v, bbox, ctm)
        sw = _num(st.get("stroke-width"), 1.0) * escala if stroke else 0
        if tag in ("line", "polyline") or (fill is None and stroke is None):
            fill = None if tag in ("line", "polyline") else fill
        if fill is None and stroke is None:
            return
        o = opac * _num(st.get("fill-opacity" if fill else "stroke-opacity"), 1.0)
        a = {"Self": self.doc.uid("v"), "ItemLayer": self.doc._lid(self.layer),
             "FillColor": fill or NONE, "StrokeColor": stroke or NONE, "StrokeWeight": f(sw),
             "EndCap": CAPS.get(st.get("stroke-linecap", "butt"), "ButtEndCap"),
             "EndJoin": JOINS.get(st.get("stroke-linejoin", "miter"), "MiterEndJoin"),
             "StrokeAlignment": "CenterAlignment", "AppliedObjectStyle": "ObjectStyle/$ID/[None]",
             "ItemTransform": "@@XF@@"}
        if gf:
            a.update(GradientFillStart=gf["start"], GradientFillLength=gf["length"], GradientFillAngle=gf["angle"])
        if gs:
            a.update(GradientStrokeStart=gs["start"], GradientStrokeLength=gs["length"], GradientStrokeAngle=gs["angle"])
        if st.get("stroke-dasharray") and st["stroke-dasharray"] != "none" and stroke:
            a["StrokeType"] = "StrokeStyle/$ID/Dashed"
        linha_simples = (len(subs) == 1 and subs[0][1] and len(subs[0][0]) == 2
                         and all(pt[0] == pt[1] == pt[2] for pt in subs[0][0]))
        tipo = "GraphicLine" if linha_simples else "Polygon"
        self.itens.append({"k": "forma", "xml": f"<{tipo} {attrs(a)}>{self._geometria(subs)}{self._transparencia(o)}</{tipo}>",
                           "bbox": bbox, "tag": tag, "fill": fill, "gf": gf, "rgb": _rgb(fill_v), "stroke": stroke,
                           "aba": bool(aba), "vertical": linha_simples and abs(bbox[2] - bbox[0]) < 0.6,
                           "horizontal": linha_simples and abs(bbox[3] - bbox[1]) < 0.6})

    # ------------------------------------------------------------------ imagens
    def imagem(self, el, st, ctm, opac, clip):
        if not self.salvar_imagem:
            return
        href = el.get("href") or el.get(XLINK) or ""
        info = self.salvar_imagem(href, f"{self.nome}-fundo")
        if not info:
            return
        fn, kind, gw, gh = info
        x, y, w, h = (_num(el.get(k)) for k in ("x", "y", "width", "height"))
        moldura = Path(Rect(x, y, w, h))
        if clip is not None:
            filhos = [c for c in clip if _tag(c) in ("path", "rect", "circle", "ellipse", "polygon")]
            if filhos:
                moldura = self._forma(filhos[0], _tag(filhos[0])) or moldura
        subs = self.subcaminhos(moldura, ctm)
        if not subs:
            return
        p0 = ctm.point_in_matrix_space((x, y))
        p1 = ctm.point_in_matrix_space((x + w, y + h))
        rx, ry, rw, rh = p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1]
        par = (el.get("preserveAspectRatio") or "xMidYMid meet").split()
        s = max(rw / gw, rh / gh) if len(par) > 1 and par[1] == "slice" else min(rw / gw, rh / gh)
        if par[0] == "none":
            sx, sy = rw / gw, rh / gh
        else:
            sx = sy = s
        tx, ty = rx + (rw - gw * sx) / 2, ry + (rh - gh * sy) / 2
        rid, gid, lid = self.doc.uid("v"), self.doc.uid("g"), self.doc.uid("l")
        fmt = {"jpg": "$ID/JPEG", "png": "$ID/Portable Network Graphics (PNG)",
               "pdf": "$ID/Adobe Portable Document Format (PDF)"}.get(kind, "$ID/JPEG")
        link = (f'<Link {attrs({"Self": lid, "AssetURL": "$ID/", "AssetID": "$ID/", "LinkResourceURI": f"file:Links/{fn}", "LinkResourceFormat": fmt, "StoredState": "Normal", "LinkClassID": 35906, "LinkClientID": 257, "LinkResourceModified": "false", "LinkObjectModified": "false", "ShowInUI": "true", "CanEmbed": "true", "CanUnembed": "true", "CanPackage": "true", "ImportPolicy": "NoAutoImport", "ExportPolicy": "NoAutoExport"})}/>')
        gb = f'<GraphicBounds Left="0" Top="0" Right="{f(gw)}" Bottom="{f(gh)}"/>'
        g = (f'<Image Self="{gid}" ItemTransform="{f(sx)} 0 0 {f(sy)} {f(tx)} {f(ty)}" ImageTypeName="{fmt}"><Properties>'
             f'<Profile type="string">$ID/Embedded</Profile>{gb}</Properties>{link}</Image>')
        a = {"Self": rid, "Name": fn, "ItemLayer": self.doc._lid(self.layer), "ContentType": "GraphicType",
             "FillColor": NONE, "StrokeColor": NONE, "StrokeWeight": "0", "AppliedObjectStyle": "ObjectStyle/$ID/[None]",
             "ItemTransform": "@@XF@@"}
        self.itens.append({"k": "imagem", "bbox": self._bbox(subs),
                           "xml": f'<Polygon {attrs(a)}>{self._geometria(subs)}{self._transparencia(opac)}'
                                  f'<FrameFittingOption AutoFit="false"/>{g}</Polygon>'})

    # ------------------------------------------------------------------ textos
    def _ps(self, fam, est, size, cor, trk, just) -> str:
        cor_nome = (cor or "Color/Black").split("/", 1)[-1].replace("%25", "%")
        m = re.match(r"R=(\d+) G=(\d+) B=(\d+)", cor_nome)
        if m:
            cor_nome = "RGB " + "".join(f"{int(v):02X}" for v in m.groups())
        cor_nome = {"Paper": "branco", "Black": "preto"}.get(cor_nome, cor_nome)
        lado = {"CenterAlign": " centro", "RightAlign": " direita"}.get(just, "")
        nome = safe_name(f"Retro 2026 - Gráfico - {fam} {est} {size:.1f} pt {cor_nome}{lado}".replace(".", ","))
        return self.doc.para_style(nome, font=fam, FontStyle=est, PointSize=round(size, 2), FillColor=cor or "Color/Black",
                                   Tracking=trk, Justification=just, Hyphenation="false", FirstLineIndent=0,
                                   LeftIndent=0, SpaceBefore=0, SpaceAfter=0, leading=round(size * 1.2, 2),
                                   AppliedLanguage=self.doc.lang)

    def texto(self, el, st, ctm, opac):
        idx = self.n_texto
        self.n_texto += 1
        escala = math.sqrt(abs(ctm.a * ctm.d - ctm.b * ctm.c)) or 1.0
        x, y = _num((el.get("x") or "0").split()[0]), _num((el.get("y") or "0").split()[0])
        y += _num((el.get("dy") or "0").split()[0])
        x += _num((el.get("dx") or "0").split()[0])
        blocos = [{"x": x, "y": y, "st": st, "runs": []}]

        def acrescenta(texto, stl, shift):
            t = re.sub(r"\s+", " ", texto or "")
            if t:
                blocos[-1]["runs"].append((t, stl, shift))

        acrescenta(el.text, st, 0.0)
        dy_acum = 0.0
        for filho in el:
            if _tag(filho) != "tspan":
                acrescenta(filho.tail, st, dy_acum)
                continue
            fst = dict(st)
            fst.update(_estilo(filho))
            if filho.get("x") is not None or filho.get("y") is not None:
                bx = _num((filho.get("x") or str(blocos[-1]["x"])).split()[0])
                by = _num((filho.get("y") or str(blocos[-1]["y"])).split()[0]) + _num(filho.get("dy"))
                blocos.append({"x": bx, "y": by, "st": fst, "runs": []})
                dy_acum = 0.0
                acrescenta(filho.text, fst, 0.0)
            else:
                dy_acum += _num(filho.get("dy"))
                acrescenta(filho.text, fst, dy_acum)
            acrescenta(filho.tail, st, dy_acum)
        medido = self.larguras[idx] if idx < len(self.larguras) else None
        for bi, b in enumerate(blocos):
            runs = b["runs"]
            if not runs:
                continue
            runs[0] = (runs[0][0].lstrip(), *runs[0][1:])
            runs[-1] = (runs[-1][0].rstrip(), *runs[-1][1:])
            texto_total = "".join(r[0] for r in runs)
            if not texto_total.strip():
                continue
            bst = b["st"]
            size_u = _num(bst.get("font-size"), 16)
            size = size_u * escala
            anchor = bst.get("text-anchor", "start")
            just = {"middle": "CenterAlign", "end": "RightAlign"}.get(anchor, "LeftAlign")
            ref = {"middle": "CenterPoint", "end": "RightCenterPoint"}.get(anchor, "LeftCenterPoint")
            if medido and len(blocos) == 1:
                w = medido * escala * 1.08 + size * 0.5
            else:
                w = sum(len(r[0]) * _num(r[1].get("font-size"), size_u) for r in runs) * 0.62 * escala + size
            px, py = ctm.point_in_matrix_space((b["x"], b["y"]))
            fx = {"CenterAlign": px - w / 2, "RightAlign": px - w}.get(just, px)
            base = size * 0.95
            sobe = max([-r[2] for r in runs] + [0]) * escala
            base += sobe
            fy = py - base
            fh = base + size * 0.35
            # estilo de parágrafo pela primeira letra do bloco
            fam0, est0 = self.fonte_cb(_fonte_svg(bst.get("font-family")), int(_num(bst.get("font-weight"), 400)),
                                       bst.get("font-style") == "italic")
            cor0 = self.cor(_rgb(bst.get("fill", "black"))) or "Color/Black"
            ls0 = _num(bst.get("letter-spacing"), 0)
            trk0 = round(ls0 / size_u * 1000) if size_u else 0
            rr = []
            for t, rst, shift in runs:
                fam, est = self.fonte_cb(_fonte_svg(rst.get("font-family")), int(_num(rst.get("font-weight"), 400)),
                                         rst.get("font-style") == "italic")
                rsize_u = _num(rst.get("font-size"), size_u)
                rr.append({"t": t, "fam": fam, "est": est, "size": rsize_u * escala,
                           "cor": self.cor(_rgb(rst.get("fill", "black"))) or "Color/Black",
                           "trk": round(_num(rst.get("letter-spacing"), 0) / rsize_u * 1000) if rsize_u else 0,
                           "shift": shift * escala})
            self.itens.append({"k": "texto", "texto": texto_total, "runs": rr, "fam0": fam0, "est0": est0, "size": size,
                               "cor0": cor0, "trk0": trk0, "just": just, "ref": ref, "px": px, "py": py, "w": w,
                               "base": base, "fh": fh, "opac": opac, "peso": int(_num(bst.get("font-weight"), 400)),
                               "familia": _fonte_svg(bst.get("font-family")), "rgb": _rgb(bst.get("fill", "black")),
                               "linha": idx})

    def _story(self, rec, ps=None, limpo=False) -> str:
        """História do texto. Com ps da casa e limpo=True, o texto entra só com o estilo de parágrafo (sem
        formatação local); senão leva o estilo gerado "Retro 2026 - Gráfico - ..." e as diferenças por trecho."""
        if ps is None:
            ps = self._ps(rec["fam0"], rec["est0"], rec["size"], rec["cor0"], rec["trk0"], rec["just"])
            limpo = False
        crs = []
        for r in rec["runs"]:
            ca = {"AppliedCharacterStyle": "CharacterStyle/$ID/[No character style]"}
            props = ""
            if not limpo:
                if r["fam"] != rec["fam0"]:
                    props = f'<Properties><AppliedFont type="string">{escape(r["fam"])}</AppliedFont></Properties>'
                if r["est"] != rec["est0"]:
                    ca["FontStyle"] = r["est"]
                if abs(r["size"] - rec["size"]) > 0.05:
                    ca["PointSize"] = f(r["size"])
                if r["cor"] != rec["cor0"]:
                    ca["FillColor"] = r["cor"]
                if r["trk"] != rec["trk0"]:
                    ca["Tracking"] = f(r["trk"])
            if abs(r["shift"]) > 0.01:
                ca["BaselineShift"] = f(-r["shift"])
            crs.append(f"<CharacterStyleRange {attrs(ca)}>{props}<Content>{escape(r['t'])}</Content></CharacterStyleRange>")
        sid = self.doc.uid("st")
        inner = f'<ParagraphStyleRange AppliedParagraphStyle="{ps}">{"".join(crs)}</ParagraphStyleRange>'
        self.doc._add_story(self.doc._wrap_story(sid, inner), sid)
        return sid

    def _xf(self, dy=0.0) -> str:
        ox, oy = self.doc._off(self.page)
        return f"1 0 0 1 {f(ox)} {f(oy + dy)}"

    def _texto_simples(self, rec, dy=0.0) -> str:
        sid = self._story(rec)
        tp = {"TextColumnCount": 1, "FirstBaselineOffset": "FixedHeight", "MinimumFirstBaselineOffset": f(rec["base"]),
              "VerticalJustification": "TopAlign", "IgnoreWrap": "true", "UseFixedColumnWidth": "false",
              "AutoSizingType": "WidthOnly", "AutoSizingReferencePoint": rec["ref"], "UseNoLineBreaksForAutoSizing": "true"}
        fx = {"CenterAlign": rec["px"] - rec["w"] / 2, "RightAlign": rec["px"] - rec["w"]}.get(rec["just"], rec["px"])
        a = {"Self": self.doc.uid("tf"), "Name": rec["texto"][:40], "ItemLayer": self.doc._lid(self.layer),
             "ParentStory": sid, "PreviousTextFrame": "n", "NextTextFrame": "n", "ContentType": "TextType",
             "FillColor": NONE, "StrokeColor": NONE, "StrokeWeight": "0",
             "AppliedObjectStyle": "ObjectStyle/$ID/[None]", "ItemTransform": self._xf(dy)}
        ins = ('<Properties><InsetSpacing type="list"><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
               '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem></InsetSpacing></Properties>')
        return (f"<TextFrame {attrs(a)}>{self.doc._path(fx, rec['py'] - rec['base'], rec['w'], rec['fh'])}"
                f"{self._transparencia(rec['opac'])}<TextFramePreference {attrs(tp)}>{ins}</TextFramePreference></TextFrame>")

    def _moldura_casa(self, sid, obj, x, y, w, h, nome, dy=0.0) -> str:
        """Moldura de texto só com o estilo de objeto da casa: espaçamento, linha de base e o resto vêm do estilo
        (nada local, para a paleta não mostrar "+")."""
        a = {"Self": self.doc.uid("tf"), "Name": nome[:40], "ItemLayer": self.doc._lid(self.layer), "ParentStory": sid,
             "PreviousTextFrame": "n", "NextTextFrame": "n", "ContentType": "TextType", "AppliedObjectStyle": obj,
             "ItemTransform": self._xf(dy)}
        return f"<TextFrame {attrs(a)}>{self.doc._path(x, y, w, h)}</TextFrame>"

    # ------------------------------------------------------------------ arranjo nos estilos da casa
    NUM = re.compile(r"^[+\-−–]?\s*(US\$|R\$)?\s*\d[\d.,]*\s*(%|mil|mi|bi|t)?$")

    @staticmethod
    def _tom(rgb):
        """'rosa', 'azul' ou None pela cor do texto ou do preenchimento."""
        if not rgb:
            return None
        r, g, b = rgb
        if r > 180 and g < 90 and b > 60:
            return "rosa"
        if b > r + 30 and (0.299 * r + 0.587 * g + 0.114 * b) < 140:
            return "azul"
        return None

    @staticmethod
    def _escuro(rgb):
        return rgb is not None and (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) < 90

    def _topo_texto(self, rec):
        return rec["py"] - CAP.get(rec["fam0"], 0.72) * rec["size"]

    def _arranjo_casa(self):
        """Monta a peça no padrão da casa (exemplo "GRAFICOS E TABELAS 1 - RETROSPECTIVA 2026 - ESB V1", 26/11/2026):
        box com "Frame Box 2026"; título, linha de apoio e fonte em molduras com os estilos de objeto da casa,
        encostadas umas nas outras (o espaçamento entre elas é o Inset Spacing de cada estilo); números e rótulos
        com "Frame números de gráficos 2026" e "Frame legenda de gráficos 2026"; tabela como tabela do InDesign."""
        cs = self.casa
        it = self.itens
        formas = [x for x in it if x["k"] == "forma"]
        if not formas:
            return None
        # --- box (o cartão do NXtab): a maior forma que começa no canto da peça
        x0 = min(b["bbox"][0] for b in it if b["k"] != "texto")
        y0 = min(b["bbox"][1] for b in it if b["k"] != "texto")
        card = None
        for fm in formas:
            bx = fm["bbox"]
            if abs(bx[0] - x0) < 1.5 and abs(bx[1] - y0) < 1.5 and not fm["aba"] and fm["fill"]:
                if card is None or (bx[2] - bx[0]) * (bx[3] - bx[1]) > (card["bbox"][2] - card["bbox"][0]) * (card["bbox"][3] - card["bbox"][1]):
                    card = fm
        if card is None:
            return None
        L, T, R, B = card["bbox"]
        W = R - L
        textos = [x for x in it if x["k"] == "texto"]
        # --- papéis dos textos: título e linha de apoio (no topo, em ordem) e fonte (abaixo do box)
        titulo, apoio, fonte = [], [], []
        for rec in textos:
            if rec["py"] > B - 0.5 or re.match(r"^(Fontes?|Fotos?)\s*:", rec["texto"]):
                fonte.append(rec)
        resto = [r for r in textos if r not in fonte]
        for rec in resto:
            narrow = rec["fam0"] in ("Arial Narrow", "Roboto Condensed") and rec["peso"] >= 600
            if not apoio and rec["peso"] >= 800 and rec["fam0"] == "Inter" and rec["py"] < T + (B - T) * 0.4:
                titulo.append(rec)
            elif titulo and narrow and rec["py"] < T + (B - T) * 0.5 and (not apoio or rec["py"] - apoio[-1]["py"] < rec["size"] * 2):
                apoio.append(rec)
            else:
                break
        corpo_t = [r for r in resto if r not in titulo and r not in apoio]
        corpo_f = [x for x in it if x["k"] in ("forma", "imagem") and x is not card and not (x["k"] == "forma" and x["aba"])]
        fundo = [x for x in corpo_f if x["k"] == "imagem" and abs(x["bbox"][0] - L) < 2 and abs(x["bbox"][1] - T) < 2]
        corpo_f = [x for x in corpo_f if x not in fundo]
        aba = [x for x in formas if x["aba"]]
        if not titulo:
            return None
        saida = []
        # --- título
        tit = " ".join(r["texto"] for r in titulo)
        h_t = cs.altura(OBJ["titulo"], PAR["titulo"], cs.linhas(tit, OBJ["titulo"], PAR["titulo"], W))
        sid = self._story_casa(tit, PAR["titulo"])
        moldura_tit = self._moldura_casa(sid, OBJ["titulo"], L, T, W, h_t, tit)
        topo_corpo = T + h_t
        moldura_apoio = ""
        if apoio:
            txt = " ".join(r["texto"] for r in apoio)
            h_a = cs.altura(OBJ["texto"], PAR["texto"], cs.linhas(txt, OBJ["texto"], PAR["texto"], W))
            sid = self._story_casa(txt, PAR["texto"])
            moldura_apoio = self._moldura_casa(sid, OBJ["texto"], L, topo_corpo, W, h_a, txt)
            topo_corpo += h_a
        # --- tabela do NXtab -> tabela do InDesign
        tabela = self._tabela(corpo_f, corpo_t, L, W)
        miolo = []
        if tabela:
            xml_tab, h_tab, usados = tabela
            corpo_f = [x for x in corpo_f if id(x) not in usados]
            corpo_t = [x for x in corpo_t if id(x) not in usados]
            sid = self.doc.uid("st")
            self.doc._add_story(self.doc._wrap_story(sid, xml_tab), sid)
            _, _, b_in, _ = cs.inset(OBJ["texto"])
            h_fr = h_tab + b_in + 1.0
            miolo.append(self._moldura_casa(sid, OBJ["texto"], L, topo_corpo, W, h_fr, "Tabela"))
            fim_corpo = topo_corpo + h_fr
            dy = (topo_corpo + h_tab) - self._tabela_fim       # o que sobrar abaixo da tabela (nota) acompanha
            for x in corpo_f:
                fim_corpo = max(fim_corpo, x["bbox"][3] + dy + b_in)
            for r in corpo_t:
                fim_corpo = max(fim_corpo, r["py"] + 0.22 * r["size"] + dy + b_in)
        else:
            tops = [x["bbox"][1] for x in corpo_f] + [self._topo_texto(r) for r in corpo_t]
            bots = [x["bbox"][3] for x in corpo_f] + [r["py"] + 0.22 * r["size"] for r in corpo_t]
            if not tops:
                return None
            dy = topo_corpo - min(tops)
            _, _, b_in, _ = cs.inset(OBJ["texto"])
            fim_corpo = max(bots) + dy + b_in
        if W < 62 * MM_CASA and len(corpo_t) > 10:
            self.avisos.append(f"{self.nome}: peça com {len(corpo_t)} rótulos e números numa coluna só; com o corpo da "
                               "casa ela fica apertada. Prefira a vaga dupla (duas colunas).")
        # --- números e rótulos do gráfico
        tam_num = sorted(r["size"] for r in corpo_t if self.NUM.match(r["texto"].strip()) and self._tom(r["rgb"])
                         and r["size"] <= 16)
        mediana = tam_num[len(tam_num) // 2] if tam_num else 0
        for rec in corpo_t:
            miolo.append(self._texto_corpo(rec, dy, mediana))
        for x in corpo_f:
            miolo.append(x["xml"].replace("@@XF@@", self._xf(dy)))
        # --- box com o estilo da casa, do topo até o fim do miolo
        box_h = fim_corpo - T
        a = {"Self": self.doc.uid("v"), "Name": "Box", "ItemLayer": self.doc._lid(self.layer), "ContentType": "Unassigned",
             "AppliedObjectStyle": OBJ["box"], "ItemTransform": self._xf(), "FillColor": card["fill"]}
        if card["gf"]:
            gx0, gy0 = (float(v) for v in card["gf"]["start"].split())
            esc = box_h / max(B - T, 1)
            ang = float(card["gf"]["angle"])
            vertical = abs(abs(ang) - 90) < 1
            a.update(GradientFillStart=card["gf"]["start"], GradientFillAngle=card["gf"]["angle"],
                     GradientFillLength=f(float(card["gf"]["length"]) * (esc if vertical else 1)))
        saida.append(f'<Rectangle {attrs(a)}>{self.doc._path(L, T, W, box_h)}</Rectangle>')
        for x in fundo:
            saida.append(x["xml"].replace("@@XF@@", self._xf()))
        for x in aba:      # barrinha na amostra da casa (Destinos Rosa 2026, como no exemplo de 26/11/2026)
            xml = x["xml"].replace("@@XF@@", self._xf())
            if x["fill"] and cs.tem("Color/Destinos Rosa 2026"):
                xml = xml.replace(f'FillColor="{x["fill"]}"', 'FillColor="Color/Destinos Rosa 2026"', 1)
            saida.append(xml)
        saida += [moldura_tit] + ([moldura_apoio] if moldura_apoio else []) + miolo
        # --- fonte, logo abaixo do box
        fim = T + box_h
        if fonte:
            txt = " ".join(r["texto"] for r in fonte)
            h_f = cs.altura(OBJ["creditos"], PAR["creditos"], cs.linhas(txt, OBJ["creditos"], PAR["creditos"], W))
            sid = self._story_casa(txt, PAR["creditos"])
            saida.append(self._moldura_casa(sid, OBJ["creditos"], L, fim, W, h_f, txt))
            fim += h_f
        orig = max([x["bbox"][3] for x in it if x["k"] != "texto"] + [r["py"] + 0.25 * r["size"] for r in textos])
        dif = (fim - orig) / MM_CASA
        if abs(dif) > 1.5:
            self.avisos.append(f"{self.nome}: no padrão da casa a peça ficou {abs(dif):.1f} mm "
                               f"{'mais alta' if dif > 0 else 'mais baixa'} que na prova; confira o texto em volta.")
        return saida

    def _story_casa(self, texto, ps) -> str:
        sid = self.doc.uid("st")
        inner = (f'<ParagraphStyleRange AppliedParagraphStyle="{ps}"><CharacterStyleRange '
                 f'AppliedCharacterStyle="CharacterStyle/$ID/[No character style]"><Content>{escape(texto)}</Content>'
                 f'</CharacterStyleRange></ParagraphStyleRange>')
        self.doc._add_story(self.doc._wrap_story(sid, inner), sid)
        return sid

    def _texto_corpo(self, rec, dy, mediana) -> str:
        """Número ou rótulo do gráfico em moldura com o estilo de objeto da casa, no mesmo ponto da prova."""
        cs = self.casa
        txt = rec["texto"].strip()
        numero = bool(self.NUM.match(txt))
        tom = self._tom(rec["rgb"])
        ps = None
        if numero and tom and rec["size"] <= 16:          # número de destaque grande (centro da rosca): corpo da prova
            grande = mediana and rec["size"] > mediana * 1.2
            ps = PAR[f"{tom}_grande" if grande else tom]
        obj = OBJ["numeros"] if numero else OBJ["legenda_grafico"]
        t_in, l_in, b_in, r_in = cs.inset(obj)
        if ps:
            p = cs.par(ps)
            size, cap = p["size"], p["cap"]
            larg = cs.largura(txt, ps) + 2
            sid = self._story(rec, ps=ps, limpo=True)
            centro = {"LeftAlign": rec["px"] + larg / 2, "RightAlign": rec["px"] - larg / 2}.get(rec["just"], rec["px"])
            fw = larg + l_in + r_in
            fx = centro - fw / 2
        else:
            # rótulos, eixos, legendas e números neutros: estilos da casa em Roboto Condensed (títulos só em
            # Inter), variando só o corpo, que segue o da prova (26/11/2026)
            # corpo sempre o do estilo da casa (Mário Fernando: sem variação de tamanho de letra; a peça ganha
            # espaço na vaga dupla em vez de encolher a letra, 26/11/2026)
            ps = self._estilo_rotulo(rec, numero, tom)
            p = cs.par(ps)
            size = p["size"]
            cap = p["cap"]
            larg = cs.largura(txt, ps) + 2
            sid = self._story_tamanho(rec, ps)
            centro = {"LeftAlign": rec["px"] + larg / 2, "RightAlign": rec["px"] - larg / 2}.get(rec["just"], rec["px"])
            fw = larg + l_in + r_in
            if p["just"] == "LeftAlign":
                fx = centro - larg / 2 - l_in
            else:
                fx = centro - fw / 2
        fy = rec["py"] - cap - t_in
        fh = t_in + cap + 0.3 * size + b_in
        return self._moldura_casa(sid, obj, fx, fy, fw, fh, txt, dy)

    def _estilo_rotulo(self, rec, numero, tom) -> str:
        rgb = rec["rgb"] or (0, 0, 0)
        if min(rgb) > 225:
            return PAR["tab_topo"]                     # texto branco sobre cor (meses da linha do tempo)
        if numero and tom:
            return PAR[f"{tom}_grande"]                # número enorme de destaque (centro da rosca)
        if tom == "rosa":
            return PAR["rosa"]
        if rec["peso"] >= 600:
            return PAR["tab_primeira"]                 # rótulo em negrito: Roboto Condensed Bold, azul da casa
        return PAR["tab_normal"]

    def _story_tamanho(self, rec, ps) -> str:
        """História só com o estilo da casa, no corpo do estilo."""
        crs = []
        for r in rec["runs"]:     # só o estilo: nem corpo nem deslocamento locais (o "%" sobrescrito volta à linha)
            ca = {"AppliedCharacterStyle": "CharacterStyle/$ID/[No character style]"}
            crs.append(f"<CharacterStyleRange {attrs(ca)}><Content>{escape(r['t'])}</Content></CharacterStyleRange>")
        sid = self.doc.uid("st")
        self.doc._add_story(self.doc._wrap_story(sid, f'<ParagraphStyleRange AppliedParagraphStyle="{ps}">{"".join(crs)}'
                                                      f'</ParagraphStyleRange>'), sid)
        return sid

    def _tabela(self, formas, textos, L, W):
        """Tabela do NXtab (t-retro) -> XML de uma tabela do InDesign no padrão da casa. Devolve
        (xml da história, altura da tabela, ids dos itens usados) ou None."""
        self._tabela_fim = None
        rects = [x for x in formas if x["k"] == "forma" and x["tag"] in ("rect", "path") and x["fill"]
                 and (x["bbox"][2] - x["bbox"][0]) > W * 0.6]
        cab = next((x for x in rects if self._escuro(x["rgb"])), None)
        if cab is None:
            return None
        cx0, cy0, cx1, cy1 = cab["bbox"]
        linhas_r = sorted([x for x in rects if x is not cab and abs(x["bbox"][0] - cx0) < 1 and abs(x["bbox"][2] - cx1) < 1
                           and x["bbox"][1] >= cy1 - 1], key=lambda x: x["bbox"][1])
        if not linhas_r:
            return None
        fundo_tab = linhas_r[-1]["bbox"][3]
        vert = sorted({round((x["bbox"][0] + x["bbox"][2]) / 2, 1) for x in formas
                       if x["k"] == "forma" and x.get("vertical") and cx0 + 2 < x["bbox"][0] < cx1 - 2
                       and cy0 - 1 <= x["bbox"][1] <= fundo_tab})
        cols = [cx0] + [v for i, v in enumerate(vert) if i == 0 or v - vert[i - 1] > 2] + [cx1]
        faixas = [(cy0, cy1)] + [(x["bbox"][1], x["bbox"][3]) for x in linhas_r]
        grade = [["" for _ in range(len(cols) - 1)] for _ in faixas]
        estilo = [[None for _ in range(len(cols) - 1)] for _ in faixas]
        usados = {id(cab)} | {id(x) for x in linhas_r}
        usados |= {id(x) for x in formas if x["k"] == "forma" and (x.get("vertical") or x.get("horizontal"))
                   and cx0 - 1 <= x["bbox"][0] <= cx1 + 1 and cy0 - 1 <= x["bbox"][1] <= fundo_tab + 1}
        tam = sorted(r["size"] for r in textos if cy1 <= r["py"] <= fundo_tab)
        normal = tam[len(tam) // 2] if tam else 0
        for r in textos:
            ri = next((i for i, (a, b) in enumerate(faixas) if a - 0.5 <= r["py"] <= b + 0.5), None)
            if ri is None:
                continue
            cxr = r["px"] if r["just"] == "CenterAlign" else (r["px"] + r["w"] / 2 if r["just"] == "LeftAlign" else r["px"] - r["w"] / 2)
            ci = next((i for i in range(len(cols) - 1) if cols[i] - 0.5 <= cxr <= cols[i + 1] + 0.5), None)
            if ci is None:
                continue
            grade[ri][ci] = (grade[ri][ci] + " " + r["texto"]).strip()
            tom = self._tom(r["rgb"])
            if ri > 0 and ci > 0 and tom == "rosa":
                estilo[ri][ci] = "rosa"
            elif ri > 0 and ci > 0 and tom == "azul" and (r["peso"] >= 800 or r["size"] > normal * 1.1):
                estilo[ri][ci] = "azul"
            usados.add(id(r))
        self._tabela_fim = fundo_tab
        n_lin, n_col = len(faixas), len(cols) - 1
        _, l_in, _, r_in = self.casa.inset(OBJ["texto"])
        larg = W - l_in - r_in
        tot_svg = cols[-1] - cols[0]
        larguras = [(cols[i + 1] - cols[i]) / tot_svg * larg for i in range(n_col)]
        h_cab, h_lin = 19.625, 17.625
        tid = self.doc.uid("tb")
        ins = 'TextTopInset="4" TextLeftInset="4" TextBottomInset="4" TextRightInset="4" ClipContentToTextCell="false"'
        partes = [f'<Table Self="{tid}" HeaderRowCount="1" FooterRowCount="0" NumHeaderColumns="0" '
                  f'HeaderColumnsPosition="HeaderColumnsLeft" {ins} BodyRowCount="{n_lin - 1}" ColumnCount="{n_col}" '
                  f'AppliedTableStyle="TableStyle/$ID/[No table style]" TableDirection="LeftToRightDirection">']
        for i in range(n_lin):
            h = h_cab if i == 0 else h_lin
            partes.append(f'<Row Self="{tid}Row{i}" Name="{i}" {ins} SingleRowHeight="{f(h)}" MinimumHeight="{f(h)}"/>')
        for c in range(n_col):
            partes.append(f'<Column Self="{tid}Column{c}" Name="{c}" ColumnType="BodyColumn" {ins} SingleColumnWidth="{f(larguras[c])}"/>')
        total = grade[-1][0].lower().startswith("total")
        n = 0
        for c in range(n_col):
            for r in range(n_lin):
                if r == 0:
                    ps, fill = PAR["tab_topo"], COR["navy"]
                    bordas = dict(L=(0 if c == 0 else 0.5), R=(0 if c == n_col - 1 else 0.5), T=0, B=0.75)
                else:
                    fill = COR["linha_a"] if r % 2 == 1 else COR["linha_b"]
                    if c == 0:
                        ps = PAR["tab_primeira"]
                    elif estilo[r][c]:
                        ps = PAR[estilo[r][c]]
                    elif total and r == n_lin - 1:
                        ps = PAR["tab_total"]
                    else:
                        ps = PAR["tab_normal"]
                    bordas = dict(L=(0 if c == 0 else 0.75), R=(0 if c == n_col - 1 else 0.75), T=0.75,
                                  B=(0 if r == n_lin - 1 else 0.75))
                cor_b = {k: (COR["branco"] if v else "Color/Black") for k, v in bordas.items()}
                a = {"Self": f"{tid}i{n}", "Name": f"{c}:{r}", "RowSpan": 1, "ColumnSpan": 1, "ColumnType": "BodyColumn",
                     "CellType": "TextTypeCell", "AppliedCellStyle": "CellStyle/$ID/[None]", "AppliedCellStylePriority": 0,
                     "FillColor": fill, "LeftEdgeStrokeWeight": f(bordas["L"]), "RightEdgeStrokeWeight": f(bordas["R"]),
                     "TopEdgeStrokeWeight": f(bordas["T"]), "BottomEdgeStrokeWeight": f(bordas["B"]),
                     "LeftEdgeStrokeColor": cor_b["L"], "RightEdgeStrokeColor": cor_b["R"], "TopEdgeStrokeColor": cor_b["T"],
                     "BottomEdgeStrokeColor": cor_b["B"], "VerticalJustification": "CenterAlign"}
                partes.append(f'<Cell {attrs(a)} {ins}><ParagraphStyleRange AppliedParagraphStyle="{ps}"><CharacterStyleRange '
                              f'AppliedCharacterStyle="CharacterStyle/$ID/[No character style]"><Content>{escape(grade[r][c])}'
                              f'</Content></CharacterStyleRange></ParagraphStyleRange></Cell>')
                n += 1
        partes.append("</Table>")
        xml = (f'<ParagraphStyleRange AppliedParagraphStyle="{PAR["texto"]}"><CharacterStyleRange '
               f'AppliedCharacterStyle="CharacterStyle/$ID/[No character style]">{"".join(partes)}</CharacterStyleRange>'
               f'</ParagraphStyleRange>')
        return xml, h_cab + (n_lin - 1) * h_lin, usados

    # ------------------------------------------------------------------ percurso
    def percorre(self, el, ctm: Matrix, herdado: dict, opac: float, em_use=False):
        tag = _tag(el)
        if tag in ("defs", "title", "desc", "metadata", "clipPath", "mask", "linearGradient", "radialGradient",
                   "symbol", "style", "filter", "pattern", "marker"):
            return
        st = {k: v for k, v in herdado.items() if k in HERDADOS}
        proprio = _estilo(el)
        st.update({k: v for k, v in proprio.items() if k in HERDADOS})
        if proprio.get("display") == "none" or st.get("visibility") == "hidden":
            return
        if proprio.get("transform"):
            ctm = Matrix(proprio["transform"]) * ctm
        opac = opac * _num(proprio.get("opacity"), 1.0)
        clip = None
        m = URL.match(proprio.get("clip-path") or "")
        if m:
            clip = self.ids.get(m.group(1))
        if tag in ("svg", "g", "a", "switch") and not (tag == "svg" and em_use):
            for c in el:
                self.percorre(c, ctm, st, opac)
        elif tag == "use":
            ref = (el.get("href") or el.get(XLINK) or "")[1:]
            alvo = self.ids.get(ref)
            if alvo is None:
                return
            ctm2 = Matrix(f"translate({_num(el.get('x'))},{_num(el.get('y'))})") * ctm
            if _tag(alvo) == "image":
                self.imagem(alvo, st, ctm2, opac, clip)
            else:
                self.percorre(alvo, ctm2, st, opac, em_use=True)
        elif tag == "image":
            self.imagem(el, st, ctm, opac, clip)
        elif tag == "text":
            self.texto(el, st, ctm, opac)
        elif tag in ("path", "rect", "circle", "ellipse", "line", "polyline", "polygon"):
            self.forma(el, tag, st, ctm, opac)

    def converter(self, svg: str, x: float, y: float, w: float, h: float, grupo: str):
        raiz = ET.fromstring(svg)
        for el in raiz.iter():
            if el.get("id"):
                self.ids[el.get("id")] = el
        vb = [float(v) for v in re.split(r"[\s,]+", (raiz.get("viewBox") or "").strip()) if v] or \
             [0, 0, _num(raiz.get("width"), w), _num(raiz.get("height"), h)]
        vx, vy, vw, vh = vb
        self.vb = vb
        s = min(w / vw, h / vh)
        ox, oy = x + (w - vw * s) / 2, y + (h - vh * s) / 2
        ctm = Matrix(f"translate({-vx},{-vy})") * Matrix(f"scale({s})") * Matrix(f"translate({ox},{oy})")
        for c in raiz:
            self.percorre(c, ctm, {}, 1.0)
        if not self.itens:
            return None
        saida = None
        if self.casa is not None:
            try:
                saida = self._arranjo_casa()
            except Exception as e:  # noqa: BLE001
                self.avisos.append(f"{self.nome}: não consegui montar a peça nos estilos da casa ({e.__class__.__name__}: {e}); "
                                   "saiu como no NXtab.")
                saida = None
        if saida is None:
            saida = [self._texto_simples(it) if it["k"] == "texto" else it["xml"].replace("@@XF@@", self._xf())
                     for it in self.itens]
        a = {"Self": self.doc.uid("gr"), "Name": grupo, "ItemLayer": self.doc._lid(self.layer), "Visible": "true",
             "AppliedObjectStyle": "ObjectStyle/$ID/[None]", "ItemTransform": "1 0 0 1 0 0"}
        self.doc.pages[self.page].append(f"<Group {attrs(a)}>{''.join(saida)}</Group>")
        return len(saida)


def desenhar_svg(doc, page, svg, x, y, w, h, cor, fonte, salvar_imagem=None, larguras=None, layer=None,
                 nome="Gráfico", avisos=None, casa=None):
    """Desenha a peça SVG como objetos nativos na página. (x, y, w, h) em pontos da página: a caixa
    que a peça ocupa na prova. Devolve o número de objetos criados (ou None)."""
    cv = Conversor(doc, page, cor, fonte, salvar_imagem, larguras, layer, nome, avisos, casa)
    return cv.converter(svg, x, y, w, h, nome)


# Medição dos textos no Chromium: comprimento de cada <text>, na ordem do documento, em unidades do SVG.
JS_MEDIR = """() => Array.from(document.querySelectorAll('svg text')).map(t => {
  try { return t.getComputedTextLength(); } catch (e) { return null; } })"""
