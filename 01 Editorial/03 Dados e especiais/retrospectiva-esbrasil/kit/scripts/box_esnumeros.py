"""Box "Quer saber mais sobre os números do [editoria]?" do ES em Números, no fim de todo capítulo da Retrospectiva.

Desenho enviado por Mário Fernando em 22/11/2026: cartão navy, sem números, com a marca do ES em Números à direita,
filete rosa e o endereço esemnumeros.esbrasil.com.br na faixa de baixo. Vai como último elemento da última página,
no pé da coluna lateral (uma coluna, 246 px na prova). Sai em SVG (vínculo no InDesign) e no <figure> da prova.

Uso: python3 box_esnumeros.py "Agro" graficos/  (ou "dos Supermercados", ou linhas com "|")   -> graficos/esn-box.svg e graficos/esn-box.html
     No corpo do capítulo, use {{esn-box}} no fim da lateral da última página.
"""
import base64
import sys
from pathlib import Path

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo-es-em-numeros-h.png"   # recorte da referência; trocar pelo vetor no InDesign


def box(editoria: str) -> str:
    b64 = base64.b64encode(LOGO.read_bytes()).decode()
    W, TOP, BAR, BOT = 330, 124, 6, 48
    H = TOP + BAR + BOT
    # editoria com artigo ("dos Supermercados") ou em linhas prontas, separadas por "|"
    # ("Quer saber mais|sobre os números|dos Serviços|Financeiros?"); sem artigo, usa "do" (ex.: "Agro").
    if "|" in editoria:
        linhas = editoria.split("|")
    else:
        art, _, nome = editoria.partition(" ")
        if art not in ("do", "da", "dos", "das") or not nome:
            art, nome = "do", editoria
        linhas = ["Quer saber", "mais sobre os", f"números {art}", f"{nome}?"]
    rotulo = " ".join(linhas)
    fs, lh = 17.2, 19.2
    y0 = (TOP - lh * len(linhas)) / 2 + fs - 1
    txt = "".join(f'<text x="18" y="{y0 + i * lh:.1f}">{l}</text>' for i, l in enumerate(linhas))
    lw = 146; lhh = lw * 96 / 300
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{rotulo} esemnumeros.esbrasil.com.br">'
            f'<defs><clipPath id="esnbox-clip"><rect width="{W}" height="{H}" rx="13"/></clipPath></defs>'
            f'<g clip-path="url(#esnbox-clip)"><rect width="{W}" height="{TOP}" fill="#073269"/>'
            f'<rect y="{TOP}" width="{W}" height="{BAR}" fill="#D8165D"/><rect y="{TOP + BAR}" width="{W}" height="{BOT}" fill="#031534"/></g>'
            f'<g font-family="Inter,Arial,sans-serif" font-weight="800" font-size="{fs}" fill="#FFFFFF" letter-spacing="-0.4">{txt}</g>'
            f'<image x="{W - 18 - lw:.1f}" y="{(TOP - lhh) / 2:.1f}" width="{lw}" height="{lhh:.1f}" preserveAspectRatio="xMidYMid meet" '
            f'xlink:href="data:image/png;base64,{b64}"/>'
            f'<text x="{W / 2}" y="{TOP + BAR + BOT / 2 + 5.2:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" '
            f'font-size="15" fill="#FFFFFF" letter-spacing="-0.2">esemnumeros.esbrasil.com.br</text></svg>')


if __name__ == "__main__":
    editoria, saida = sys.argv[1], Path(sys.argv[2] if len(sys.argv) > 2 else "graficos")
    saida.mkdir(parents=True, exist_ok=True)
    svg = box(editoria)
    (saida / "esn-box.svg").write_text(svg, encoding="utf-8")
    (saida / "esn-box.html").write_text(f'<figure class="nxtab esnbox" data-vaga="lateral" style="width:246px">{svg}</figure>', encoding="utf-8")
    print(saida / "esn-box.svg")
