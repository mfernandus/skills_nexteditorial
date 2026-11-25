"""Monta o capítulo da Retrospectiva sobre o molde do capítulo de Agro (versão 10, 22/11/2026).
Uso, na pasta do capítulo: python3 ../montar.py
Lê titulo.txt, nota.html, corpo.html (com {{id}} das peças do NXtab, {{SELO}} e {{LOGO}}), secoes.html e texto.html;
grava capitulo.html (imagens por caminho relativo) para conferir, e depois embutir com embutir_imagens.py."""
import re
from pathlib import Path

B = Path(__file__).resolve().parent
head = (B / 'base-head.html').read_text(encoding='utf8')
tail = (B / 'base-tail.html').read_text(encoding='utf8')
selo = (B / 'base-selo.txt').read_text().strip()
logo = (B / 'base-logo.txt').read_text().strip()

titulo = Path('titulo.txt').read_text(encoding='utf8').strip()
head = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', head, count=1)
extra = Path('estilo.css').read_text(encoding='utf8') if Path('estilo.css').exists() else ''
# Coluna cheia até o pé (regra do editor, 22/11/2026): sem viúva/órfã de 2 linhas empurrando o texto para a coluna seguinte;
# a lateral empilha as peças no alto e o resto da coluna é texto (sem espaço distribuído entre as peças).
extra = '.p1 .opener h1{line-height:45.6px!important}\n.page.esq .top .tag{left:52.68px!important}\n.page.esq .top .selo{left:auto!important;right:74.63px!important}\n.page.dir .top .logo-esb{left:74.63px!important}\n.page.dir .top .tag{right:52.68px!important}\n.flow p{orphans:1;widows:1;text-wrap:pretty}\n.flow p.corte{text-align-last:justify}\n.flow p.vaga-aspa{margin:0!important;min-height:0!important;height:calc(var(--lin)*5)!important;overflow:hidden;border-width:1px!important}\n.flow p.vaga-aspa span{font-size:10.5px!important;line-height:12.5px!important}\n.flow p.vaga-aspa{padding:1px 5px!important}\n.side:not(.side-fecho){justify-content:flex-start!important}\n' + extra
# Texto corrido em Minion Pro Cond 11/12 pt, tracking -15 (a fonte da revista, enviada pelo editor em 23/11/2026 e
# guardada em kit/assets/fonts): na prova, 17,04 px sobre a entrelinha de 18,585 px, embutida no HTML.
import base64
_F = B / 'kit' / 'assets' / 'fonts'
_faces = ''
for _arq, _peso, _estilo in (('MinionPro-Cn.otf', 400, 'normal'), ('MinionPro-CnIt.otf', 400, 'italic'),
                             ('MinionPro-SemiboldCn.otf', 600, 'normal'), ('MinionPro-BoldCn.otf', 700, 'normal')):
    if (_F / _arq).exists():
        _b64 = base64.b64encode((_F / _arq).read_bytes()).decode()
        _faces += ('@font-face{font-family:"Minion Pro Cond";src:url(data:font/otf;base64,' + _b64 +
                   ') format("opentype");font-weight:' + str(_peso) + ';font-style:' + _estilo + '}\n')
if _faces:
    extra = _faces + '.flow{font-family:"Minion Pro Cond","Crimson Pro",Georgia,serif!important;font-size:17.04px!important;letter-spacing:-.015em}\n' + extra
# Fotos internas (todas menos a de abertura) com cantos arredondados no mesmo raio das tabelas do NXtab
# (12 unidades do desenho, 9,66 px na prova, cerca de 2,2 mm), pedido do editor em 23/11/2026.
# Intertítulo sem palavra sozinha na última linha (text-wrap: balance, mais espaço inseparável entre as duas últimas palavras).
extra = '.ph:not(.opener)>img{border-radius:9.66px!important}\n.flow h4{text-wrap:balance}\n.page>figure.ph:not(.opener){margin-bottom:8px!important}\n.page>figure.nxtab[data-vaga="tabela"]{margin-bottom:6px!important}\n.page .flow h4{margin:var(--lin) 0 0!important;position:relative;top:calc(var(--lin)*-.35)}\n.page .flow>h4:first-child{margin-top:0!important}\n.page .flow h4.topo{top:0}\n' + extra
if extra:
    head = head.replace('</style></head>', extra + '\n</style></head>', 1)

corpo = Path('corpo.html').read_text(encoding='utf8')
corpo = corpo.replace('{{SELO}}', selo).replace('{{LOGO}}', logo)


def peca(m):
    sobre, nome = m.group(1), m.group(2)
    f = Path('graficos') / f'{nome}.html'
    if not f.exists():
        raise SystemExit(f'peça não encontrada: {f}')
    h = f.read_text(encoding='utf8')
    if sobre:   # peça ligeiramente sobre a foto de abertura, alinhada à última coluna da direita
        h = h.replace('class="nxtab"', 'class="nxtab sobre"', 1)
    return h


corpo = re.sub(r'\{\{(sobre:)?([a-z0-9\-]+)\}\}', peca, corpo)
nota = Path('nota.html').read_text(encoding='utf8').strip()
secoes = Path('secoes.html').read_text(encoding='utf8')
texto = Path('texto.html').read_text(encoding='utf8').strip()
# Hifenização em português (o Chromium não traz dicionário pt-BR): hífens discricionários (U+00AD), que o InDesign
# também lê como hífen opcional, como na hifenização dos estilos da base V5.
import pyphen
_hif = pyphen.Pyphen(lang='pt_BR', left=2, right=3)
def _hifeniza(trecho):
    return re.sub(r'(?<![-\w])[A-Za-zÀ-ÿ][a-zà-ÿ]{6,}(?![-\w])', lambda w: _hif.inserted(w.group(0), hyphen='\u00ad'), trecho)
texto = re.sub(r'>([^<]+)<', lambda mm: '>' + _hifeniza(mm.group(1)) + '<', texto)
texto = re.sub(r'<h4>.*?</h4>', lambda mm: mm.group(0).replace('\u00ad',''), texto, flags=re.S)
texto = re.sub(r'(<h4>[^<]*?) (\S+</h4>)', lambda mm: mm.group(1) + '\u00a0' + mm.group(2), texto)
html = head + '<div class="wrap" lang="pt-BR">' + nota + '\n' + corpo + '\n' + secoes + '</div>\n' + texto + tail
Path('capitulo.html').write_text(html, encoding='utf8')
print('capitulo.html', len(html))
