"""Medidas da base da casa, lidas do próprio .idml: espaçamento interno (Inset Spacing) de cada estilo de
objeto e fonte, corpo e entrelinha de cada estilo de parágrafo. O exportador usa essas medidas para montar as
molduras no padrão da casa: cada moldura encosta na vizinha e o espaçamento entre elas vem só do estilo de
objeto (pedido de 26/11/2026). Mudar o Inset Spacing no estilo de objeto passa a mudar o espaçamento.
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

MM = 72 / 25.4
_LARG = json.loads((Path(__file__).with_name("larguras_fontes.json")).read_text(encoding="utf-8"))


def largura(texto: str, fonte: str, estilo: str, corpo: float, tracking: float = 0.0) -> float:
    """Largura do texto em pt, pelas larguras reais da fonte (Inter e Roboto Condensed; o resto, pela Roboto)."""
    tab = _LARG.get(f"{fonte}|{estilo}") or _LARG.get(f"{fonte}|Regular") or _LARG["Roboto Condensed|Regular"]
    w = sum(tab.get(ch, 0.55) for ch in texto)
    return (w + tracking / 1000 * max(len(texto) - 1, 0)) * corpo


def quebrar(texto: str, fonte: str, estilo: str, corpo: float, tracking: float, util: float) -> int:
    """Número de linhas com quebra por palavra numa largura útil (em pt)."""
    linhas, atual = 1, ""
    for palavra in texto.split():
        tenta = (atual + " " + palavra).strip()
        if atual and largura(tenta, fonte, estilo, corpo, tracking) > util:
            linhas += 1
            atual = palavra
        else:
            atual = tenta
    return linhas

# altura das maiúsculas (em fração do corpo): é o que o InDesign usa com "Primeira linha de base: Altura das maiúsculas"
CAP = {"Inter": 0.727, "Roboto Condensed": 0.711, "Arial Narrow": 0.716, "Minion Pro": 0.651, "Myriad Pro": 0.674}

# estilos de objeto e de parágrafo das peças (base V6, "GRAFICOS E TABELAS 1 - RETROSPECTIVA 2026 - ESB V1")
OBJ = {
    "box": "ObjectStyle/Frame Box 2026",
    "titulo": "ObjectStyle/Frame Título de box 2026",
    "texto": "ObjectStyle/Frame texto de box 2026",
    "creditos": "ObjectStyle/Frame Créditos 2026",
    "numeros": "ObjectStyle/Frame números de gráficos 2026",
    "legenda_grafico": "ObjectStyle/Frame legenda de gráficos 2026",
    "legenda_fora": "ObjectStyle/Frame Legenda fora da foto 2026",
    "legenda_dentro": "ObjectStyle/Frame Legenda dentro foto 2026",
}
PAR = {
    "titulo": "ParagraphStyle/Título de box 2026",
    "texto": "ParagraphStyle/Texto de box 2026",
    "creditos": "ParagraphStyle/Créditos 2026",
    "tab_topo": "ParagraphStyle/Texto topo de tabela 2026",
    "tab_primeira": "ParagraphStyle/Texto de tabela primeira coluna 2026",
    "tab_normal": "ParagraphStyle/Texto de tabela normal 2026",
    "tab_total": "ParagraphStyle/Texto de tabela destaque de total 2026",
    "azul": "ParagraphStyle/Texto de tabela e gráficos destaque azul 2026",
    "rosa": "ParagraphStyle/Texto de tabela e gráficos destaque rosa 2026",
    "azul_grande": "ParagraphStyle/Texto de tabela e gráficos destaque grande azul 2026",
    "rosa_grande": "ParagraphStyle/Texto de tabela e gráficos destaque grande rosa 2026",
}
COR = {"navy": "Color/Destinos Navy 2026", "linha_a": "Color/C=20 M=0 Y=0 K=0", "linha_b": "Color/C=10 M=0 Y=0 K=0",
       "branco": "Color/Paper"}


def cmyk_para_rgb(c, m, y, k):
    """Aproximação simples (só para comparar cores; a impressão usa o CMYK da amostra)."""
    return tuple(255 * (1 - v / 100) * (1 - k / 100) for v in (c, m, y))


def rgb_para_cmyk(rgb):
    r, g, b = (v / 255 for v in rgb[:3])
    k = 1 - max(r, g, b)
    if k >= 0.999:
        return 0, 0, 0, 100
    return tuple(int(round(v)) for v in ((1 - r - k) / (1 - k) * 100, (1 - g - k) / (1 - k) * 100,
                                          (1 - b - k) / (1 - k) * 100, k * 100))


def _lab(rgb):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    fx, fy, fz = (t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116 for t in (x, y, z))
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


# amostras da paleta impressa da casa que podem receber as cores do NXtab e da prova (26/11/2026: o .idml é
# para impressão, tudo em CMYK da paleta enviada pelo Mário Fernando, nada de amostra RGB)
PALETA_CASA = re.compile(r"(2026$|^Preto \d+%25\s*$|^C=10 M=0 Y=0 K=0$|^C=20 M=0 Y=0 K=0$|^Paper$|^Black$)")


class Casa:
    """Medidas da base. inset(estilo) -> (topo, esquerda, baixo, direita) em pt; par(estilo) -> dict."""

    def __init__(self, base: Path):
        with zipfile.ZipFile(base) as z:
            st = z.read("Resources/Styles.xml").decode("utf-8")
        from idml import ajustar_estilos_casa   # os ajustes da casa valem também para as medidas lidas aqui
        self._st = ajustar_estilos_casa(st)
        self._ins: dict[str, tuple] = {}
        self._par: dict[str, dict] = {}
        with zipfile.ZipFile(base) as z:
            gr = z.read("Resources/Graphic.xml").decode("utf-8")
        self._gr = gr
        self.paleta = []          # (Self, lab) das amostras CMYK da paleta da casa
        for m in re.finditer(r'<Color Self="Color/([^"]+)"([^>]*)>', gr):
            nome, a = m.group(1), dict(re.findall(r'(\w+)="([^"]*)"', m.group(2)))
            if a.get("Space") != "CMYK" or a.get("Visible") != "true" or a.get("Model") != "Process":
                continue
            if not PALETA_CASA.search(nome):
                continue
            v = [float(x) for x in a.get("ColorValue", "0 0 0 0").split()]
            self.paleta.append((f"Color/{nome}", _lab(cmyk_para_rgb(*v))))
        self._cache: dict = {}

    def amostra(self, rgb, limite: float = 28.0):
        """Amostra CMYK da paleta da casa mais próxima da cor (diferença Delta E até o limite) ou None."""
        rgb = tuple(int(v) for v in rgb[:3])
        if rgb not in self._cache:
            lab = _lab(rgb)
            melhor = min(self.paleta, key=lambda p: sum((a - b) ** 2 for a, b in zip(p[1], lab)), default=None)
            d = sum((a - b) ** 2 for a, b in zip(melhor[1], lab)) ** 0.5 if melhor else 999
            self._cache[rgb] = melhor[0] if melhor and d <= limite else None
        return self._cache[rgb]

    def tem(self, self_id: str) -> bool:
        return f'Self="{self_id}"' in self._st or f'Self="{self_id}"' in self._gr

    def _bloco(self, self_id: str, tag: str) -> tuple[str, str] | None:
        i = self._st.find(f'<{tag} Self="{self_id}"')
        if i < 0:
            return None
        cab = self._st[i:self._st.index(">", i)]
        j = self._st.find(f"</{tag}>", i)
        corpo = "" if cab.endswith("/") or j < 0 else self._st[i:j]
        return cab, corpo

    def inset(self, self_id: str) -> tuple[float, float, float, float]:
        if self_id not in self._ins:
            b = self._bloco(self_id, "ObjectStyle")
            v = (0.0, 0.0, 0.0, 0.0)
            if b:
                m = re.search(r"<InsetSpacing type=\"list\">(.*?)</InsetSpacing>", b[1], re.S)
                if m:
                    nums = [float(x) for x in re.findall(r">\s*(-?[\d.]+)\s*<", m.group(1))]
                    if len(nums) == 4:
                        v = tuple(nums)
            self._ins[self_id] = v
        return self._ins[self_id]

    def par(self, self_id: str) -> dict:
        if self_id in self._par:
            return self._par[self_id]
        d: dict = {}
        cadeia, atual = [], self_id
        while atual and len(cadeia) < 8:
            b = self._bloco(atual, "ParagraphStyle")
            if not b:
                break
            cab, corpo = b
            a = dict(re.findall(r'(\w+)="([^"]*)"', cab))
            p = dict(re.findall(r'<(\w+) type="[^"]*">([^<]*)<', corpo))
            for k, v in list(a.items()) + list(p.items()):
                d.setdefault(k, v)
            base = p.get("BasedOn", "")
            atual = None if not base or "No paragraph style" in base else (base if base.startswith("ParagraphStyle/") else "ParagraphStyle/" + base)
            cadeia.append(atual)
        size = float(d.get("PointSize", 12))
        lead = d.get("Leading", "Auto")
        lead = size * 1.2 if lead in ("Auto", "") else float(lead)
        fonte = d.get("AppliedFont", "Minion Pro")
        r = {"size": size, "leading": lead, "font": fonte, "style": d.get("FontStyle", "Regular"),
             "cap": CAP.get(fonte, 0.7) * size, "just": d.get("Justification", "LeftAlign"),
             "tracking": float(d.get("Tracking", 0) or 0)}
        self._par[self_id] = r
        return r

    def linhas(self, texto: str, obj: str, par: str, largura_moldura: float) -> int:
        _, l, _, r = self.inset(obj)
        p = self.par(par)
        return quebrar(texto, p["font"], p["style"], p["size"], p["tracking"], (largura_moldura - l - r) * 0.98)

    def largura(self, texto: str, par: str) -> float:
        p = self.par(par)
        return largura(texto, p["font"], p["style"], p["size"], p["tracking"])

    def altura(self, obj: str, par: str, linhas: int = 1) -> float:
        """Altura da moldura no padrão da casa: espaço de cima + altura das maiúsculas + (linhas - 1) entrelinhas
        + espaço de baixo (a linha de base fica na borda do espaço de baixo, como no exemplo da casa)."""
        t, _, b, _ = self.inset(obj)
        p = self.par(par)
        return t + p["cap"] + max(0, linhas - 1) * p["leading"] + b
