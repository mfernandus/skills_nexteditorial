"""Gerador mínimo de IDML (InDesign Markup Language) para a Retrospectiva ES Brasil.

Monta um pacote .idml válido com páginas, retângulos, molduras de texto (encadeadas ou
soltas), tabelas nativas, imagens e PDFs vinculados, cores, estilos de parágrafo e de
caractere. Unidades em pontos; coordenadas relativas ao canto superior esquerdo da página.
"""
from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass, field
from xml.sax.saxutils import escape, quoteattr

DOM = "13.0"
NS = 'xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"'
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
NONE = "Swatch/None"
LANG = "$ID/Portuguese: Brazilian"


def f(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def attrs(d: dict) -> str:
    return " ".join(f"{k}={quoteattr(str(v))}" for k, v in d.items() if v is not None)


def safe_name(s: str) -> str:
    return re.sub(r"[^\w\- .áéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ/]", "_", s).strip() or "estilo"


@dataclass
class Run:
    text: str
    char_style: str | None = None      # nome do estilo de caractere
    font: str | None = None            # família
    style: str | None = None           # FontStyle (Regular, Bold...)
    size: float | None = None
    color: str | None = None           # nome da cor (swatch)
    tracking: float | None = None
    leading: float | None = None


@dataclass
class Para:
    runs: list[Run]
    style: str = "$ID/NormalParagraphStyle"
    overrides: dict = field(default_factory=dict)  # atributos locais de parágrafo
    leading: float | None = None


class IDML:
    def __init__(self, width: float, height: float, bleed: float = 8.5039, lang: str = LANG,
                 facing: bool = False, primeira: str = "esq"):
        self.W, self.H, self.bleed, self.lang = width, height, bleed, lang
        self.facing, self.primeira = facing, primeira
        self.sides: list[str | None] = []
        self._n = 0
        self.colors: dict[str, tuple] = {}
        self.para_styles: dict[str, dict] = {}
        self.char_styles: dict[str, dict] = {}
        self.pages: list[list[str]] = []      # xml dos itens por página
        self.stories: dict[str, str] = {}     # id -> xml
        self.story_order: list[str] = []
        self.layers: dict[str, tuple] = {"base": ("ul", "Diagramação", True)}
        self.layers_existentes: set[str] = set()

    def layer(self, key: str, name: str, printable: bool = True) -> str:
        if key not in self.layers:
            self.layers[key] = (f"ul{len(self.layers) + 1}", name, printable)
        return key

    def layer_existente(self, key: str, lid: str, name: str) -> str:
        """Usa uma camada que já existe no documento-base (por exemplo, TEXTOS ou FUNDOS E IMAGENS)."""
        self.layers[key] = (lid, name, True)
        self.layers_existentes.add(key)
        return key

    def _lid(self, key: str | None) -> str:
        return self.layers.get(key or "base", self.layers["base"])[0]

    # ------------------------------------------------------------------ ids
    def uid(self, p: str = "nx") -> str:
        # Prefixo próprio: os ids da base da revista começam com "u" seguido de hexadecimal (ub9, uba...)
        # e não podem se repetir no documento.
        self._n += 1
        return f"{p}{self._n:x}"

    # ------------------------------------------------------------------ cores
    def color(self, rgb: tuple[int, int, int], name: str | None = None) -> str:
        r, g, b = (max(0, min(255, int(round(c)))) for c in rgb[:3])
        if (r, g, b) == (0, 0, 0) and not name:
            return "Color/Black"
        if (r, g, b) == (255, 255, 255) and not name:
            return "Color/Paper"
        for nm, val in self.colors.items():
            if val == (r, g, b):
                return f"Color/{nm}"
        nm = name or f"R={r} G={g} B={b}"
        self.colors[nm] = (r, g, b)
        return f"Color/{nm}"

    # ------------------------------------------------------------------ estilos
    def para_style(self, name: str, **a) -> str:
        name = safe_name(name)
        if name not in self.para_styles:
            self.para_styles[name] = a
        return f"ParagraphStyle/{name}"

    def char_style(self, name: str, **a) -> str:
        name = safe_name(name)
        if name not in self.char_styles:
            self.char_styles[name] = a
        return f"CharacterStyle/{name}"

    # ------------------------------------------------------------------ páginas
    def add_page(self) -> int:
        self.pages.append([])
        i = len(self.pages) - 1
        if self.facing:
            outro = "dir" if self.primeira == "esq" else "esq"
            self.sides.append(self.primeira if i % 2 == 0 else outro)
        else:
            self.sides.append(None)
        return i

    def _off(self, page: int | None = None) -> tuple[float, float]:
        """Deslocamento da página no espelho: esquerda em -W, direita em 0; página solta centrada."""
        if page is None or not self.facing:
            return -self.W / 2, -self.H / 2
        return (-self.W if self.sides[page] == "esq" else 0.0), -self.H / 2

    def _xf(self, page: int | None = None) -> str:
        ox, oy = self._off(page)
        return f"1 0 0 1 {f(ox)} {f(oy)}"

    @staticmethod
    def _path(x: float, y: float, w: float, h: float) -> str:
        pts = [(x, y), (x, y + h), (x + w, y + h), (x + w, y)]
        pp = "".join(
            f'<PathPointType Anchor="{f(px)} {f(py)}" LeftDirection="{f(px)} {f(py)}" RightDirection="{f(px)} {f(py)}"/>'
            for px, py in pts)
        return (f'<Properties><PathGeometry><GeometryPathType PathOpen="false"><PathPointArray>{pp}'
                f'</PathPointArray></GeometryPathType></PathGeometry></Properties>')

    @staticmethod
    def _corner(r: float) -> dict:
        if not r or r < 0.5:
            return {}
        d = {}
        for c in ("TopLeft", "TopRight", "BottomLeft", "BottomRight"):
            d[f"{c}CornerOption"] = "RoundedCorner"
            d[f"{c}CornerRadius"] = f(r)
        return d

    @staticmethod
    def _opacity(o: float | None) -> str:
        if o is None or o >= 0.999:
            return ""
        return f'<TransparencySetting><BlendingSetting Opacity="{f(o * 100)}"/></TransparencySetting>'

    def rect(self, page: int, x, y, w, h, fill: str | None = None, stroke: str | None = None,
             stroke_w: float = 0, radius: float = 0, opacity: float | None = None, name: str | None = None,
             layer: str | None = None):
        a = {"Self": self.uid(), "Name": name, "ItemLayer": self._lid(layer), "ContentType": "Unassigned", "StoryTitle": "$ID/",
             "FillColor": fill or NONE, "StrokeColor": stroke or NONE, "StrokeWeight": f(stroke_w),
             "AppliedObjectStyle": "ObjectStyle/$ID/[None]", "ItemTransform": self._xf(page), **self._corner(radius)}
        self.pages[page].append(f"<Rectangle {attrs(a)}>{self._path(x, y, w, h)}{self._opacity(opacity)}</Rectangle>")

    # ------------------------------------------------------------------ histórias
    def _story_xml(self, sid: str, paras: list[Para]) -> str:
        out = []
        for i, p in enumerate(paras):
            pa = {"AppliedParagraphStyle": p.style if p.style.startswith("ParagraphStyle/") else f"ParagraphStyle/{p.style}"}
            pa.update(p.overrides)
            props = f'<Properties><Leading type="unit">{f(p.leading)}</Leading></Properties>' if p.leading else ""
            body = []
            runs = p.runs or [Run("")]
            for j, r in enumerate(runs):
                ca = {"AppliedCharacterStyle": f"CharacterStyle/{r.char_style}" if r.char_style else "CharacterStyle/$ID/[No character style]",
                      "FontStyle": r.style, "PointSize": f(r.size) if r.size else None,
                      "FillColor": r.color, "Tracking": f(r.tracking) if r.tracking is not None else None}
                cprops = []
                if r.font:
                    cprops.append(f'<AppliedFont type="string">{escape(r.font)}</AppliedFont>')
                if r.leading:
                    cprops.append(f'<Leading type="unit">{f(r.leading)}</Leading>')
                cp = f"<Properties>{''.join(cprops)}</Properties>" if cprops else ""
                content = self._content(r.text)
                br = "<Br/>" if (j == len(runs) - 1 and i < len(paras) - 1) else ""
                body.append(f"<CharacterStyleRange {attrs(ca)}>{cp}{content}{br}</CharacterStyleRange>")
            out.append(f"<ParagraphStyleRange {attrs(pa)}>{props}{''.join(body)}</ParagraphStyleRange>")
        return self._wrap_story(sid, "".join(out))

    @staticmethod
    def _content(text: str) -> str:
        if text is None or text == "":
            return ""
        parts = text.split("\n")
        xml = []
        for k, part in enumerate(parts):
            if part:
                xml.append(f"<Content>{escape(part)}</Content>")
            if k < len(parts) - 1:
                xml.append("<Content> </Content>")
        return "".join(xml)

    @staticmethod
    def _wrap_story(sid: str, inner: str) -> str:
        return (f'{HDR}<idPkg:Story {NS} DOMVersion="{DOM}"><Story Self="{sid}" AppliedTOCStyle="n" '
                f'TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">'
                f'<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" FrameType="TextFrameType" '
                f'StoryOrientation="Horizontal" StoryDirection="LeftToRightDirection"/>'
                f'<InCopyExportOption IncludeGraphicProxies="true" IncludeAllResources="false"/>'
                f'{inner}</Story></idPkg:Story>')

    def _add_story(self, xml: str, sid: str):
        self.stories[sid] = xml
        self.story_order.append(sid)

    def text_frame(self, page: int, x, y, w, h, paras: list[Para], columns: int = 1, gutter: float = 12,
                   valign: str = "TopAlign", autosize: bool = False, name: str | None = None,
                   fill: str | None = None, inset: tuple | None = None, layer: str | None = None,
                   baseline: float | None = None, rot: int = 0, object_style: str | None = None):
        sid = self.uid("st")
        self._add_story(self._story_xml(sid, paras), sid)
        self._frame(page, sid, x, y, w, h, columns, gutter, valign, autosize, name, fill, inset,
                    layer=layer, baseline=baseline, rot=rot, object_style=object_style)
        return sid

    def _frame(self, page, sid, x, y, w, h, columns=1, gutter=12, valign="TopAlign", autosize=False,
               name=None, fill=None, inset=None, prev="n", nxt="n", fid=None, layer=None, baseline=None,
               rot=0, object_style=None):
        fid = fid or self.uid("tf")
        xf = self._xf(page)
        if rot == 90:   # texto de cima para baixo: a moldura gira 90 graus; (x, y, w, h) é a caixa já girada
            ox, oy = self._off(page)
            xf = f"0 1 -1 0 {f(ox + x + w)} {f(oy + y)}"
            x, y, w, h = 0, 0, h, w
        a = {"Self": fid, "Name": name, "ItemLayer": self._lid(layer), "ParentStory": sid, "PreviousTextFrame": prev, "NextTextFrame": nxt,
             "ContentType": "TextType", "FillColor": fill or NONE, "StrokeColor": NONE, "StrokeWeight": "0",
             "AppliedObjectStyle": object_style or "ObjectStyle/$ID/[None]", "ItemTransform": xf}
        tp = {"TextColumnCount": columns, "TextColumnGutter": f(gutter),
              "FirstBaselineOffset": "FixedHeight" if baseline else "AscentOffset",
              "MinimumFirstBaselineOffset": f(baseline) if baseline else None,
              "VerticalJustification": valign, "IgnoreWrap": "false", "UseFixedColumnWidth": "false"}
        if autosize:
            tp.update({"AutoSizingType": "HeightOnly", "AutoSizingReferencePoint": "TopCenterPoint",
                       "UseNoLineBreaksForAutoSizing": "false"})
        ins = ""
        if inset:
            ins = ("<Properties><InsetSpacing type=\"list\">" +
                   "".join(f'<ListItem type="unit">{f(v)}</ListItem>' for v in inset) +
                   "</InsetSpacing></Properties>")
        self.pages[page].append(
            f"<TextFrame {attrs(a)}>{self._path(x, y, w, h)}<TextFramePreference {attrs(tp)}>{ins}</TextFramePreference></TextFrame>")
        return fid

    def threaded_story(self, frames: list[dict], paras: list[Para], name: str = "Texto corrido"):
        """frames: [{page,x,y,w,h,columns,gutter}] na ordem do fluxo."""
        sid = self.uid("st")
        self._add_story(self._story_xml(sid, paras), sid)
        ids = [self.uid("tf") for _ in frames]
        for i, fr in enumerate(frames):
            self._frame(fr["page"], sid, fr["x"], fr["y"], fr["w"], fr["h"], fr.get("columns", 1),
                        fr.get("gutter", 12), name=f"{name} {i + 1}", baseline=fr.get("baseline"),
                        prev=ids[i - 1] if i else "n", nxt=ids[i + 1] if i < len(ids) - 1 else "n", fid=ids[i])
        return sid

    # ------------------------------------------------------------------ tabela
    def table_frame(self, page: int, x, y, w, h, rows: list[dict], col_widths: list[float],
                    header_rows: int = 1, name: str | None = None, layer: str | None = None):
        """rows: [{height, cells:[{paras, fill, insets(t,l,b,r), stroke_bottom:(color,w), valign}]}]"""
        sid = self.uid("st")
        tid = self.uid("tb")
        nrows, ncols = len(rows), len(col_widths)
        parts = [f'<Table {attrs({"Self": tid, "HeaderRowCount": header_rows, "FooterRowCount": 0, "BodyRowCount": nrows - header_rows, "ColumnCount": ncols, "AppliedTableStyle": "TableStyle/$ID/[Basic Table]", "TableDirection": "LeftToRightDirection"})}>']
        for ri, r in enumerate(rows):
            parts.append(f'<Row Self="{tid}Row{ri}" Name="{ri}" SingleRowHeight="{f(r.get("height", 14))}" MinimumHeight="{f(min(r.get("height", 14), 6))}" AutoGrow="true"/>')
        for ci, cw in enumerate(col_widths):
            parts.append(f'<Column Self="{tid}Column{ci}" Name="{ci}" SingleColumnWidth="{f(cw)}"/>')
        for ri, r in enumerate(rows):
            for ci, c in enumerate(r["cells"]):
                t, l, b, rr = c.get("insets", (2, 4, 2, 4))
                sb = c.get("stroke_bottom")
                ca = {"Self": f"{tid}i{ci}i{ri}", "Name": f"{ci}:{ri}", "RowSpan": 1, "ColumnSpan": 1,
                      "AppliedCellStyle": "CellStyle/$ID/[None]", "AppliedCellStylePriority": 0,
                      "FillColor": c.get("fill") or NONE, "FillTint": 100 if c.get("fill") else None,
                      "TopInset": f(t), "LeftInset": f(l), "BottomInset": f(b), "RightInset": f(rr),
                      "VerticalJustification": c.get("valign", "CenterAlign"),
                      "TopEdgeStrokeWeight": "0", "LeftEdgeStrokeWeight": "0", "RightEdgeStrokeWeight": "0",
                      "BottomEdgeStrokeWeight": f(sb[1]) if sb else "0",
                      "BottomEdgeStrokeColor": sb[0] if sb else None}
                inner = self._story_xml("tmp", c["paras"])
                inner = inner.split('IncludeAllResources="false"/>', 1)[1].rsplit("</Story>", 1)[0]
                parts.append(f"<Cell {attrs(ca)}>{inner}</Cell>")
        parts.append("</Table>")
        inner = ('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle">'
                 '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]">'
                 + "".join(parts) + "</CharacterStyleRange></ParagraphStyleRange>")
        self._add_story(self._wrap_story(sid, inner), sid)
        self._frame(page, sid, x, y, w, h, name=name, layer=layer)
        return sid

    # ------------------------------------------------------------------ imagens e PDF
    def placed(self, page: int, x, y, w, h, link_uri: str, kind: str, gw: float, gh: float,
               sx: float, sy: float, tx: float, ty: float, radius: float = 0, name: str | None = None,
               layer: str | None = None):
        """kind: 'jpg' | 'png' | 'pdf'. (gw, gh) = tamanho do gráfico em pt; (sx,sy,tx,ty) posiciona
        o gráfico dentro da moldura (coordenadas de página)."""
        rid, gid, lid = self.uid(), self.uid("g"), self.uid("l")
        a = {"Self": rid, "Name": name, "ItemLayer": self._lid(layer), "ContentType": "GraphicType", "StoryTitle": "$ID/", "FillColor": NONE,
             "StrokeColor": NONE, "StrokeWeight": "0", "AppliedObjectStyle": "ObjectStyle/$ID/[None]",
             "ItemTransform": self._xf(page), **self._corner(radius)}
        fmt = {"jpg": "$ID/JPEG", "png": "$ID/Portable Network Graphics (PNG)",
               "pdf": "$ID/Adobe Portable Document Format (PDF)"}[kind]
        link = (f'<Link {attrs({"Self": lid, "AssetURL": "$ID/", "AssetID": "$ID/", "LinkResourceURI": link_uri, "LinkResourceFormat": fmt, "StoredState": "Normal", "LinkClassID": 35906, "LinkClientID": 257, "LinkResourceModified": "false", "LinkObjectModified": "false", "ShowInUI": "true", "CanEmbed": "true", "CanUnembed": "true", "CanPackage": "true", "ImportPolicy": "NoAutoImport", "ExportPolicy": "NoAutoExport"})}/>')
        gb = f'<GraphicBounds Left="0" Top="0" Right="{f(gw)}" Bottom="{f(gh)}"/>'
        xf = f"{f(sx)} 0 0 {f(sy)} {f(tx)} {f(ty)}"
        if kind == "pdf":
            g = (f'<PDF Self="{gid}" ItemTransform="{xf}"><Properties>{gb}</Properties>'
                 f'<PDFAttribute PageNumber="1" PDFCrop="CropMedia" TransparentBackground="true"/>{link}</PDF>')
        else:
            g = (f'<Image Self="{gid}" ItemTransform="{xf}" ImageTypeName="{fmt}"><Properties>'
                 f'<Profile type="string">$ID/Embedded</Profile>{gb}</Properties>{link}</Image>')
        fit = '<FrameFittingOption AutoFit="false"/>'
        self.pages[page].append(f"<Rectangle {attrs(a)}>{self._path(x, y, w, h)}{fit}{g}</Rectangle>")

    # ------------------------------------------------------------------ saída
    def _graphic_xml(self) -> str:
        base = (
            '<Color Self="Color/Black" Model="Process" Space="CMYK" ColorValue="0 0 0 100" ColorOverride="Specialblack" AlternateSpace="NoAlternateColor" AlternateColorValue="" Name="Black" ColorEditable="false" ColorRemovable="false" Visible="true" SwatchCreatorID="7937"/>'
            '<Color Self="Color/Paper" Model="Process" Space="CMYK" ColorValue="0 0 0 0" ColorOverride="Specialpaper" AlternateSpace="NoAlternateColor" AlternateColorValue="" Name="Paper" ColorEditable="true" ColorRemovable="false" Visible="true" SwatchCreatorID="7937"/>'
            '<Color Self="Color/Registration" Model="Registration" Space="CMYK" ColorValue="100 100 100 100" ColorOverride="Specialregistration" AlternateSpace="NoAlternateColor" AlternateColorValue="" Name="Registration" ColorEditable="false" ColorRemovable="false" Visible="true" SwatchCreatorID="7937"/>')
        cols = "".join(
            f'<Color {attrs({"Self": f"Color/{n}", "Model": "Process", "Space": "RGB", "ColorValue": f"{r} {g} {b}", "ColorOverride": "Normal", "AlternateSpace": "NoAlternateColor", "AlternateColorValue": "", "Name": n, "ColorEditable": "true", "ColorRemovable": "true", "Visible": "true", "SwatchCreatorID": "7937"})}/>'
            for n, (r, g, b) in self.colors.items())
        return (f'{HDR}<idPkg:Graphic {NS} DOMVersion="{DOM}">{base}{cols}'
                '<Swatch Self="Swatch/None" Name="None" ColorEditable="false" ColorRemovable="false" Visible="true" SwatchCreatorID="7937"/>'
                '<StrokeStyle Self="StrokeStyle/$ID/Solid" Name="$ID/Solid"/>'
                '</idPkg:Graphic>')

    def _style_el(self, kind: str, name: str, a: dict) -> str:
        a = dict(a)
        props = []
        font = a.pop("font", None)
        leading = a.pop("leading", None)
        based = a.pop("based_on", None)
        ucolor = a.pop("UnderlineColor", None)
        if based and based.startswith("$ID/"):
            props.append(f'<BasedOn type="string">{escape(based)}</BasedOn>')
        elif based:
            props.append(f'<BasedOn type="object">{kind}/{escape(safe_name(based))}</BasedOn>')
        elif kind == "ParagraphStyle":
            props.append('<BasedOn type="string">$ID/NormalParagraphStyle</BasedOn>')
        else:
            props.append('<BasedOn type="string">$ID/[No character style]</BasedOn>')
        if font:
            props.append(f'<AppliedFont type="string">{escape(font)}</AppliedFont>')
        if leading:
            props.append(f'<Leading type="unit">{f(leading)}</Leading>')
        if ucolor:
            props.append(f'<UnderlineColor type="object">{escape(ucolor)}</UnderlineColor>')
        attr = {"Self": f"{kind}/{name}", "Name": name, "Imported": "false"}
        if kind == "ParagraphStyle":
            attr["NextStyle"] = f"ParagraphStyle/{name}"
        for k, v in a.items():
            attr[k] = f(v) if isinstance(v, float) else v
        return f"<{kind} {attrs(attr)}><Properties>{''.join(props)}</Properties></{kind}>"

    def _styles_xml(self) -> str:
        cs = "".join(self._style_el("CharacterStyle", n, a) for n, a in self.char_styles.items())
        ps = "".join(self._style_el("ParagraphStyle", n, a) for n, a in self.para_styles.items())
        return (
            f'{HDR}<idPkg:Styles {NS} DOMVersion="{DOM}">'
            f'<RootCharacterStyleGroup Self="{self.uid()}">'
            '<CharacterStyle Self="CharacterStyle/$ID/[No character style]" Imported="false" Name="$ID/[No character style]"/>'
            f'{cs}</RootCharacterStyleGroup>'
            f'<RootParagraphStyleGroup Self="{self.uid()}">'
            f'<ParagraphStyle Self="ParagraphStyle/$ID/[No paragraph style]" Name="$ID/[No paragraph style]" Imported="false" FillColor="Color/Black" FontStyle="Regular" PointSize="12" Justification="LeftAlign" AppliedLanguage="{self.lang}" Hyphenation="true"><Properties><Leading type="enumeration">Auto</Leading><AppliedFont type="string">Inter</AppliedFont></Properties></ParagraphStyle>'
            '<ParagraphStyle Self="ParagraphStyle/$ID/NormalParagraphStyle" Name="$ID/NormalParagraphStyle" Imported="false" NextStyle="ParagraphStyle/$ID/NormalParagraphStyle"><Properties><BasedOn type="string">$ID/[No paragraph style]</BasedOn></Properties></ParagraphStyle>'
            f'{ps}</RootParagraphStyleGroup>'
            '<TOCStyle Self="TOCStyle/$ID/DefaultTOCStyleName" Name="$ID/DefaultTOCStyleName" TitleStyle="ParagraphStyle/$ID/[No paragraph style]" Title="Contents"/>'
            f'<RootCellStyleGroup Self="{self.uid()}"><CellStyle Self="CellStyle/$ID/[None]" Name="$ID/[None]" AppliedParagraphStyle="ParagraphStyle/$ID/[No paragraph style]"/></RootCellStyleGroup>'
            f'<RootTableStyleGroup Self="{self.uid()}"><TableStyle Self="TableStyle/$ID/[No table style]" Name="$ID/[No table style]"/>'
            '<TableStyle Self="TableStyle/$ID/[Basic Table]" Name="$ID/[Basic Table]"><Properties><BasedOn type="string">$ID/[No table style]</BasedOn></Properties></TableStyle></RootTableStyleGroup>'
            f'<RootObjectStyleGroup Self="{self.uid()}">'
            '<ObjectStyle Self="ObjectStyle/$ID/[None]" Name="$ID/[None]" FillColor="Swatch/None" StrokeColor="Swatch/None" StrokeWeight="0"/>'
            '<ObjectStyle Self="ObjectStyle/$ID/[Normal Graphics Frame]" Name="$ID/[Normal Graphics Frame]"><Properties><BasedOn type="string">$ID/[None]</BasedOn></Properties></ObjectStyle>'
            '<ObjectStyle Self="ObjectStyle/$ID/[Normal Text Frame]" Name="$ID/[Normal Text Frame]"><Properties><BasedOn type="string">$ID/[None]</BasedOn></Properties></ObjectStyle>'
            '</RootObjectStyleGroup>'
            '</idPkg:Styles>')

    def _prefs_xml(self) -> str:
        b = f(self.bleed)
        return (f'{HDR}<idPkg:Preferences {NS} DOMVersion="{DOM}">'
                f'<DocumentPreference PageHeight="{f(self.H)}" PageWidth="{f(self.W)}" PagesPerDocument="1" '
                f'FacingPages="false" DocumentBleedTopOffset="{b}" DocumentBleedBottomOffset="{b}" '
                f'DocumentBleedInsideOrLeftOffset="{b}" DocumentBleedOutsideOrRightOffset="{b}" DocumentBleedUniformSize="true" '
                f'AllowPageShuffle="true" PageBinding="LeftToRight" Intent="PrintIntent" ColumnDirection="Horizontal"/>'
                f'<MarginPreference ColumnCount="1" ColumnGutter="12" Top="0" Bottom="0" Left="0" Right="0" ColumnDirection="Horizontal" ColumnsPositions="0 {f(self.W)}"/>'
                f'<ViewPreference HorizontalMeasurementUnits="Millimeters" VerticalMeasurementUnits="Millimeters" RulerOrigin="PageOrigin"/>'
                f'</idPkg:Preferences>')

    def _page_el(self, pid, name, master=True):
        am = 'AppliedMaster="um" ' if master else ""
        return (f'<Page Self="{pid}" {am}GeometricBounds="0 0 {f(self.H)} {f(self.W)}" ItemTransform="{self._xf()}" '
                f'Name="{name}" OverrideList="" MasterPageTransform="1 0 0 1 0 0" TabOrder="" GridStartingPoint="TopOutside" UseMasterGrid="true">'
                f'<Properties><PageColor type="enumeration">UseMasterColor</PageColor></Properties>'
                f'<MarginPreference ColumnCount="1" ColumnGutter="12" Top="0" Bottom="0" Left="0" Right="0" ColumnDirection="Horizontal" ColumnsPositions="0 {f(self.W)}"/></Page>')

    def _layers_xml(self) -> str:
        cores = ["LightBlue", "Red", "Green", "Blue", "Yellow"]
        out = []
        for i, (lid, name, printable) in enumerate(self.layers.values()):
            out.append(f'<Layer {attrs({"Self": lid, "Name": name, "Visible": "true", "Locked": "false", "IgnoreWrap": "false", "ShowGuides": "true", "LockGuides": "false", "UI": "true", "Expendable": "true", "Printable": "true" if printable else "false"})}>'
                       f'<Properties><LayerColor type="enumeration">{cores[i % len(cores)]}</LayerColor></Properties></Layer>')
        return "".join(out)

    def save(self, path: str, title: str = "Retrospectiva"):
        files: dict[str, str] = {}
        files["MasterSpreads/MasterSpread_um.xml"] = (
            f'{HDR}<idPkg:MasterSpread {NS} DOMVersion="{DOM}"><MasterSpread Self="um" ItemTransform="1 0 0 1 0 0" '
            f'OverriddenPageItemProps="" Name="A-Mestre" NamePrefix="A" BaseName="Mestre" ShowMasterItems="true" PageCount="1" PageColor="UseMasterColor">'
            f'{self._page_el("ump", "A", master=False)}</MasterSpread></idPkg:MasterSpread>')
        spread_refs = []
        for i, items in enumerate(self.pages):
            sid = f"sp{i + 1}"
            files[f"Spreads/Spread_{sid}.xml"] = (
                f'{HDR}<idPkg:Spread {NS} DOMVersion="{DOM}"><Spread Self="{sid}" PageCount="1" BindingLocation="0" '
                f'AllowPageShuffle="true" ItemTransform="1 0 0 1 0 0" ShowMasterItems="true" PageTransitionType="None">'
                f'{self._page_el(f"pg{i + 1}", str(i + 1))}{"".join(items)}</Spread></idPkg:Spread>')
            spread_refs.append(f'<idPkg:Spread src="Spreads/Spread_{sid}.xml"/>')
        for sid in self.story_order:
            files[f"Stories/Story_{sid}.xml"] = self.stories[sid]
        files["Resources/Graphic.xml"] = self._graphic_xml()
        files["Resources/Fonts.xml"] = f'{HDR}<idPkg:Fonts {NS} DOMVersion="{DOM}"/>'
        files["Resources/Styles.xml"] = self._styles_xml()
        files["Resources/Preferences.xml"] = self._prefs_xml()
        files["XML/Tags.xml"] = (f'{HDR}<idPkg:Tags {NS} DOMVersion="{DOM}"><XMLTag Self="XMLTag/Root" Name="Root">'
                                 f'<Properties><TagColor type="enumeration">LightBlue</TagColor></Properties></XMLTag></idPkg:Tags>')
        files["XML/BackingStory.xml"] = (
            f'{HDR}<idPkg:BackingStory {NS} DOMVersion="{DOM}"><XmlStory Self="ubs" AppliedTOCStyle="n" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">'
            '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle"><CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]"/></ParagraphStyleRange>'
            '</XmlStory></idPkg:BackingStory>')
        story_refs = "".join(f'<idPkg:Story src="Stories/Story_{s}.xml"/>' for s in self.story_order)
        designmap = (
            f'{HDR}<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="{DOM}(0)" ?>\n'
            f'<Document {NS} DOMVersion="{DOM}" Self="d" StoryList="{" ".join(self.story_order)}" Name={quoteattr(title)} '
            f'ZeroPoint="0 0" ActiveLayer="ul" CMYKProfile="Coated FOGRA39 (ISO 12647-2:2004)" RGBProfile="sRGB IEC61966-2.1" '
            f'SolidColorIntent="UseColorSettings" AfterBlendingIntent="UseColorSettings" DefaultImageIntent="UseColorSettings" '
            f'RGBPolicy="PreserveEmbeddedProfiles" CMYKPolicy="CombinationOfPreserveAndSafeCmyk" AccurateLABSpots="false">'
            '<idPkg:Graphic src="Resources/Graphic.xml"/><idPkg:Fonts src="Resources/Fonts.xml"/>'
            '<idPkg:Styles src="Resources/Styles.xml"/><idPkg:Preferences src="Resources/Preferences.xml"/>'
            '<idPkg:Tags src="XML/Tags.xml"/>'
            f'{self._layers_xml()}'
            '<idPkg:MasterSpread src="MasterSpreads/MasterSpread_um.xml"/>'
            f'{"".join(spread_refs)}'
            f'<Section Self="usec" Length="{len(self.pages)}" Name="" ContinueNumbering="true" IncludeSectionPrefix="false" Marker="" PageStart="pg1" SectionPrefix=""><Properties><PageNumberStyle type="enumeration">Arabic</PageNumberStyle></Properties></Section>'
            '<idPkg:BackingStory src="XML/BackingStory.xml"/>'
            f'{story_refs}</Document>')
        container = (f'{HDR}<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                     '<rootfiles><rootfile full-path="designmap.xml" media-type="text/xml"/></rootfiles></container>')
        with zipfile.ZipFile(path, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), "application/vnd.adobe.indesign-idml-package",
                       compress_type=zipfile.ZIP_STORED)
            z.writestr("designmap.xml", designmap, compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
            for name, data in files.items():
                z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)

    # ------------------------------------------------------------------ saída sobre a base da revista
    def save_on_base(self, base: str, path: str, title: str = "Retrospectiva", page_start: int | None = None,
                     mestre_origem: str | None = None, mestre_nome: tuple[str, str] = ("R", "Retrospectiva 2026"),
                     retranca: str | None = None):
        """Grava o documento dentro do arquivo-base da revista (IDML): mantém cores, fontes, estilos,
        preferências (página, sangria, margens, linha de base), camadas e páginas-mestre da casa, tira as
        páginas de exemplo e cria a página-mestre do capítulo a partir de `mestre_origem`, só com o
        paginador (rodapé). Estilos e cores do capítulo que não existem na base entram ao lado dos da casa."""
        import xml.etree.ElementTree as ET
        zin = zipfile.ZipFile(base)
        files = {n: zin.read(n) for n in zin.namelist()}
        txt = lambda n: files[n].decode("utf-8")
        dm = txt("designmap.xml")
        dom = re.search(r'DOMVersion="([^"]+)"', dm).group(1)
        fixdom = lambda x: x.replace(f'DOMVersion="{DOM}"', f'DOMVersion="{dom}"')

        # --- página-mestre do capítulo
        # Base da Retrospectiva (V5 em diante): as mestres já trazem fundo, retranca "retrospectiva 2026", selo,
        # logo da ES Brasil, abas de cor e paginador. A mestre do capítulo é a cópia inteira da "A-Master", com a
        # retranca da página direita trocada pela editoria. Bases antigas (sem a retranca "retrospectiva 2026" na
        # mestre): cópia da mestre de 3 colunas só com o rodapé, como antes.
        mfiles = [n for n in files if n.startswith("MasterSpreads/")]
        retro = any("retrospectiva 2026" in txt(n).lower() for n in files if n.startswith("Stories/"))
        if mestre_origem is None:
            mestre_origem = "A-Master" if retro else "B-Parent"
        inteira = retro
        origem = next(n for n in mfiles if f'Name="{mestre_origem}"' in txt(n))
        ET.register_namespace("idPkg", "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging")
        root = ET.fromstring(files[origem])
        ms = root.find("MasterSpread")
        itens = [e for e in list(ms) if e.tag in ("TextFrame", "Rectangle", "Group", "GraphicLine", "Polygon", "Oval")]

        def topo(e):
            pts = [tuple(map(float, p.get("Anchor").split())) for p in e.iter("PathPointType")]
            a, b, c, d, tx, ty = map(float, (e.get("ItemTransform") or "1 0 0 1 0 0").split())
            return min(b * x + d * y + ty for x, y in pts) if pts else 0
        if not inteira:
            for e in itens:
                if topo(e) < 300:          # cabeçalho da mestre (retranca e logos): o capítulo traz o seu
                    ms.remove(e)
        mapa = {}
        for e in ms.iter():
            if e.get("Self"):
                mapa[e.get("Self")] = "r" + e.get("Self")
        historias = {e.get("ParentStory") for e in ms.iter() if e.get("ParentStory") not in (None, "n")}
        novas_hist = {}
        for sid in historias:
            sx = txt(f"Stories/Story_{sid}.xml")
            for oid in re.findall(r'Self="([^"]+)"', sx):
                mapa.setdefault(oid, "r" + oid)
            novas_hist[sid] = sx
        def renomeia(v):
            return " ".join(mapa.get(t, t) for t in v.split(" "))
        for e in ms.iter():
            for k, v in list(e.attrib.items()):
                if k in ("Self", "ParentStory", "PreviousTextFrame", "NextTextFrame", "OverrideList") or v in mapa:
                    e.set(k, renomeia(v))
        mid = ms.get("Self")
        ms.set("Name", f"{mestre_nome[0]}-{mestre_nome[1]}")
        ms.set("NamePrefix", mestre_nome[0])
        ms.set("BaseName", mestre_nome[1])
        mestre_xml = HDR + ET.tostring(root, encoding="unicode")
        mestre_arq = f"MasterSpreads/MasterSpread_{mid}.xml"
        # retranca da editoria: a história de "Retranca 2026" da página direita que não é "retrospectiva 2026"
        # vira o nome da editoria, alinhada à direita e terminando a 10 mm do refile (espelho da retranca da esquerda)
        if inteira and retranca:
            MM = 72 / 25.4
            for sid, sx in list(novas_hist.items()):
                conteudo = " ".join(re.findall(r"<Content>([^<]*)</Content>", sx)).strip().lower()
                if "ParagraphStyle/Retranca 2026" in sx and conteudo and conteudo != "retrospectiva 2026":
                    sx = re.sub(r"<Content>[^<]*</Content>", f"<Content>{escape(retranca)}</Content>", sx, count=1)
                    sx = sx.replace('AppliedParagraphStyle="ParagraphStyle/Retranca 2026"',
                                    'AppliedParagraphStyle="ParagraphStyle/Retranca 2026" Justification="RightAlign"', 1)
                    novas_hist[sid] = sx
                    for fr in ms.iter("TextFrame"):
                        if fr.get("ParentStory") == mapa.get(sid):
                            a, b, c, d, tx, ty = map(float, (fr.get("ItemTransform") or "1 0 0 1 0 0").split())
                            pts = list(fr.iter("PathPointType"))
                            xs = [float(p.get("Anchor").split()[0]) for p in pts]
                            if not xs or min(xs) + tx < 0:      # só a da página direita
                                continue
                            direita = self.W - 10 * MM - tx
                            esquerda = direita - 90 * MM
                            x0, x1 = min(xs), max(xs)
                            for p in pts:
                                for k in ("Anchor", "LeftDirection", "RightDirection"):
                                    vx, vy = p.get(k).split()
                                    nx = esquerda if abs(float(vx) - x0) < abs(float(vx) - x1) else direita
                                    p.set(k, f"{f(nx)} {vy}")
            mestre_xml = HDR + ET.tostring(root, encoding="unicode")
            # alternância das retrancas (regra do Mário Fernando, 22/11/2026): a página esquerda leva a editoria
            # e a direita, ao lado do logo da ES Brasil, leva "RETROSPECTIVA 2026" (só o texto troca; posição e
            # alinhamento de cada retranca continuam os da mestre)
            esq = [sid for sid, sx in novas_hist.items() if "ParagraphStyle/Retranca 2026" in sx and
                   " ".join(re.findall(r"<Content>([^<]*)</Content>", sx)).strip().lower() == "retrospectiva 2026"]
            dir_ = [sid for sid, sx in novas_hist.items() if "ParagraphStyle/Retranca 2026" in sx and
                    " ".join(re.findall(r"<Content>([^<]*)</Content>", sx)).strip() == escape(retranca)]
            if esq and dir_:
                txt_retro = re.findall(r"<Content>([^<]*)</Content>", novas_hist[esq[0]])[0]
                novas_hist[esq[0]] = re.sub(r"<Content>[^<]*</Content>", f"<Content>{escape(retranca)}</Content>", novas_hist[esq[0]], count=1)
                novas_hist[dir_[0]] = re.sub(r"<Content>[^<]*</Content>", f"<Content>{txt_retro}</Content>", novas_hist[dir_[0]], count=1)
        for sid, sx in novas_hist.items():
            for oid in set(re.findall(r'Self="([^"]+)"', sx)):
                sx = sx.replace(f'"{oid}"', f'"{mapa[oid]}"')
            files[f"Stories/Story_{mapa[sid]}.xml"] = sx.encode("utf-8")
        files[mestre_arq] = mestre_xml.encode("utf-8")
        margens = re.search(r"<MarginPreference [^>]*/>", mestre_xml).group(0)

        # --- tira as páginas de exemplo e as histórias que só elas usavam
        hist_mestres = set()
        for n in mfiles + [mestre_arq]:
            hist_mestres |= set(re.findall(r'ParentStory="([^"]+)"', files[n].decode("utf-8")))
        for n in [n for n in files if n.startswith("Spreads/")]:
            del files[n]
        for n in [n for n in files if n.startswith("Stories/")]:
            sid = n[len("Stories/Story_"):-4]
            if sid not in hist_mestres:
                del files[n]

        # --- estilos e cores do capítulo ao lado dos da casa
        st = txt("Resources/Styles.xml")
        existentes = set(re.findall(r'Self="((?:Paragraph|Character)Style/[^"]+)"', st))
        ps = "".join(self._style_el("ParagraphStyle", n, a) for n, a in self.para_styles.items()
                     if f"ParagraphStyle/{n}" not in existentes)
        cs = "".join(self._style_el("CharacterStyle", n, a) for n, a in self.char_styles.items()
                     if f"CharacterStyle/{n}" not in existentes)
        st = st.replace("</RootParagraphStyleGroup>", ps + "</RootParagraphStyleGroup>", 1)
        st = st.replace("</RootCharacterStyleGroup>", cs + "</RootCharacterStyleGroup>", 1)
        files["Resources/Styles.xml"] = st.encode("utf-8")
        gr = txt("Resources/Graphic.xml")
        cores = "".join(
            f'<Color {attrs({"Self": f"Color/{n}", "Model": "Process", "Space": "RGB", "ColorValue": f"{r} {g} {b}", "ColorOverride": "Normal", "AlternateSpace": "NoAlternateColor", "AlternateColorValue": "", "Name": n, "ColorEditable": "true", "ColorRemovable": "true", "Visible": "true", "SwatchCreatorID": "7937"})}/>'
            for n, (r, g, b) in self.colors.items() if f'Self="Color/{n}"' not in gr)
        files["Resources/Graphic.xml"] = gr.replace("</idPkg:Graphic>", cores + "</idPkg:Graphic>", 1).encode("utf-8")

        # --- espelhos do capítulo
        spread_refs, n_pag, pid_primeira = [], len(self.pages), None
        grupos, i = [], 0
        while i < n_pag:
            if self.sides[i] == "esq" and i + 1 < n_pag:
                grupos.append([i, i + 1]); i += 2
            else:
                grupos.append([i]); i += 1
        inicio = page_start if page_start is not None else (2 if self.sides and self.sides[0] == "esq" else 1)
        for gi, grp in enumerate(grupos):
            sid = f"sp{gi + 1}"
            pags = []
            for pi in grp:
                pid = f"pg{pi + 1}"
                pid_primeira = pid_primeira or pid
                pags.append(
                    f'<Page Self="{pid}" GeometricBounds="0 0 {f(self.H)} {f(self.W)}" ItemTransform="{self._xf(pi)}" '
                    f'Name="{inicio + pi}" AppliedTrapPreset="TrapPreset/$ID/kDefaultTrapStyleName" OverrideList="" '
                    f'AppliedMaster="{mid}" MasterPageTransform="1 0 0 1 0 0" TabOrder="" GridStartingPoint="TopOutside" UseMasterGrid="true">'
                    f'<Properties><PageColor type="enumeration">UseMasterColor</PageColor></Properties>{margens}</Page>')
            ligacao = "0" if (len(grp) == 1 and self.sides[grp[0]] == "dir") else "1"
            itens_xml = "".join("".join(self.pages[pi]) for pi in grp)
            files[f"Spreads/Spread_{sid}.xml"] = fixdom(
                f'{HDR}<idPkg:Spread {NS} DOMVersion="{DOM}"><Spread Self="{sid}" FlattenerOverride="Default" SpreadHidden="false" '
                f'AllowPageShuffle="true" ItemTransform="1 0 0 1 0 0" ShowMasterItems="true" PageCount="{len(grp)}" '
                f'BindingLocation="{ligacao}" PageTransitionType="None" PageTransitionDirection="NotApplicable" PageTransitionDuration="Medium">'
                f'{"".join(pags)}{itens_xml}</Spread></idPkg:Spread>').encode("utf-8")
            spread_refs.append(f'<idPkg:Spread src="Spreads/Spread_{sid}.xml"/>')
        for sid in self.story_order:
            files[f"Stories/Story_{sid}.xml"] = fixdom(self.stories[sid]).encode("utf-8")

        # --- mapa do documento
        hist_base = set(re.findall(r'<idPkg:Story src="Stories/Story_([^"]+)\.xml"', dm))
        dm = re.sub(r"\s*<idPkg:Spread src=\"[^\"]+\"\s*/>", "", dm)
        dm = re.sub(r"\s*<idPkg:Story src=\"[^\"]+\"\s*/>", "", dm)
        hist_todas = sorted(n[len("Stories/Story_"):-4] for n in files if n.startswith("Stories/"))
        lista = re.search(r'StoryList="([^"]*)"', dm).group(1).split()
        lista = [t for t in lista if t not in hist_base or t in hist_todas]
        lista += [t for t in hist_todas if t not in lista]
        dm = re.sub(r'StoryList="[^"]*"', f'StoryList="{" ".join(lista)}"', dm, count=1)
        dm = re.sub(r'(<Document [^>]*?)Name="[^"]*"', lambda m: m.group(1) + f"Name={quoteattr(title + '.indd')}", dm, count=1)
        ultima_mestre = list(re.finditer(r"<idPkg:MasterSpread src=\"[^\"]+\"\s*/>", dm))[-1]
        dm = (dm[:ultima_mestre.end()] + f'<idPkg:MasterSpread src="{mestre_arq}"/>' + "".join(spread_refs) + dm[ultima_mestre.end():])
        secao = (f'<Section Self="usecR" Length="{n_pag}" Name="" ContinueNumbering="false" IncludeSectionPrefix="false" '
                 f'PageNumberStart="{inicio}" Marker="" PageStart="{pid_primeira}" SectionPrefix=""><Properties>'
                 f'<PageNumberStyle type="enumeration">Arabic</PageNumberStyle></Properties></Section>')
        dm = re.sub(r"<Section .*?</Section>", secao, dm, count=1, flags=re.S)
        # hiperlinks: os das páginas de exemplo saem; os do paginador ganham cópia para a mestre nova
        itens_vivos = set()
        for n in files:
            if n.startswith(("MasterSpreads/", "Spreads/")):
                itens_vivos |= set(re.findall(r'Self="([^"]+)"', files[n].decode("utf-8")))
        fontes_mortas, novas = set(), []
        for m in re.finditer(r'<HyperlinkPageItemSource Self="([^"]+)"[^>]*SourcePageItem="([^"]+)"[^>]*/>', dm):
            fsid, item = m.group(1), m.group(2)
            if item not in itens_vivos:
                fontes_mortas.add(fsid)
            elif item in mapa:
                novas.append((m.group(0), fsid, item))
        for fsid in fontes_mortas:
            dm = re.sub(rf'\s*<HyperlinkPageItemSource Self="{fsid}"[^>]*/>', "", dm)
            dm = re.sub(rf'\s*<Hyperlink Self="[^"]+"[^>]*Source="{fsid}".*?</Hyperlink>', "", dm, flags=re.S)
        for el, fsid, item in novas:
            dm = dm.replace(el, el + el.replace(f'Self="{fsid}"', f'Self="r{fsid}"').replace(f'SourcePageItem="{item}"', f'SourcePageItem="{mapa[item]}"')
                            .replace('Name="', 'Name="R ', 1), 1)
            hl = re.search(rf'<Hyperlink Self="([^"]+)"[^>]*Source="{fsid}".*?</Hyperlink>', dm, flags=re.S)
            if hl:
                copia = hl.group(0).replace(f'Self="{hl.group(1)}"', f'Self="r{hl.group(1)}"', 1).replace(f'Source="{fsid}"', f'Source="r{fsid}"', 1).replace('Name="', 'Name="R ', 1)
                dm = dm.replace(hl.group(0), hl.group(0) + copia, 1)
        # camadas novas do capítulo (a de prova não imprime)
        novas_camadas = "".join(
            f'<Layer {attrs({"Self": lid, "Name": name, "Visible": "true", "Locked": "false", "IgnoreWrap": "false", "ShowGuides": "true", "LockGuides": "false", "UI": "true", "Expendable": "true", "Printable": "true" if printable else "false"})}>'
            f'<Properties><LayerColor type="enumeration">Magenta</LayerColor></Properties></Layer>'
            for k, (lid, name, printable) in self.layers.items() if k not in self.layers_existentes and k != "base")
        ultima_camada = list(re.finditer(r"<Layer [^>]*>.*?</Layer>", dm, flags=re.S))[-1]
        dm = dm[:ultima_camada.end()] + novas_camadas + dm[ultima_camada.end():]
        story_refs = "".join(f'<idPkg:Story src="Stories/Story_{s}.xml"/>' for s in hist_todas)
        bs = re.search(r"<idPkg:BackingStory [^>]*/>", dm)
        dm = dm[:bs.end()] + story_refs + dm[bs.end():] if bs else dm.replace("</Document>", story_refs + "</Document>")
        files["designmap.xml"] = dm.encode("utf-8")

        with zipfile.ZipFile(path, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), "application/vnd.adobe.indesign-idml-package", compress_type=zipfile.ZIP_STORED)
            for name, data in files.items():
                if name != "mimetype":
                    z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
        return {"mestre": f"{mestre_nome[0]}-{mestre_nome[1]}", "espelhos": len(grupos), "pagina_inicial": inicio,
                "mestre_inteira": inteira, "retranca": retranca if inteira else None}
