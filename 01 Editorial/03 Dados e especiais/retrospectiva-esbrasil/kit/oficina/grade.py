"""Aplica a regra de alinhamento de 23/11/2026 num capítulo (ou no base-tail.html):
- todas as colunas da grade e a lateral começam na mesma altura (a sobra menor que uma linha sai da foto de cima, que cresce, ou vira respiro acima da grade);
- na lateral, a sobra fica entre a peça e o texto, e o texto cai por baixo, alinhado ao pé das outras colunas;
- respiro de ~20 px abaixo das fotos e da tabela do alto; intertítulo com respiro antes do texto (0,6 linha acima, 0,4 abaixo: soma 1 linha, a grade de linhas fica igual).
Uso: python3 grade.py arquivo.html"""
POST_OLD = "window.__prob=()=>"
POST = "boxes.forEach(bx=>{const R=bx.getBoundingClientRect();const pt=parseFloat(getComputedStyle(bx).paddingTop)||0;bx.querySelectorAll('h4').forEach(h=>{h.classList.remove('topo');const r=h.getClientRects()[0];if(r&&r.top-(R.top+pt)<4)h.classList.add('topo')})});window.__prob=()=>"
import sys
OLD = "boxes.forEach(bx=>{const lin=parseFloat(getComputedStyle(bx).lineHeight)||18.585;bx.style.paddingTop='0px';const h=bx.getBoundingClientRect().height-(parseFloat(getComputedStyle(bx).paddingBottom)||0);const rem=h-Math.floor(h/lin+0.001)*lin;bx.style.paddingTop=Math.max(0,rem-0.3).toFixed(2)+'px';});"
NEW = ("const _lin0=b=>parseFloat(getComputedStyle(b).lineHeight)||18.585;"
 "const _rem=b=>{const lin=_lin0(b);const cs=getComputedStyle(b);const h=b.getBoundingClientRect().height-(parseFloat(cs.paddingTop)||0)-(parseFloat(cs.paddingBottom)||0);return h-Math.floor(h/lin+0.001)*lin;};"
 "boxes.forEach(bx=>{bx.style.paddingTop='0px'});"
 "boxes.filter(bx=>!bx.closest('aside')).forEach(bx=>{const grid=bx.closest('.grid');const rem=_rem(bx);"
 "if(!grid){bx.style.paddingTop=Math.max(0,rem-0.3).toFixed(2)+'px';return;}"
 "if(rem<0.5)return;let prev=grid.previousElementSibling;while(prev&&prev.matches('p.src'))prev=prev.previousElementSibling;"
 "if(prev&&prev.matches('figure.ph:not(.opener)')){prev.style.height=(prev.getBoundingClientRect().height+rem-0.3).toFixed(2)+'px';}"
 "else{grid.style.marginTop=((parseFloat(grid.style.marginTop)||0)+rem-0.3).toFixed(2)+'px';}});"
 "boxes.filter(bx=>bx.closest('aside')).forEach(bx=>{bx.style.paddingTop=Math.max(0,_rem(bx)-0.3).toFixed(2)+'px';});")
NEW1 = NEW
NEW = NEW.replace("boxes.filter(bx=>bx.closest('aside')).forEach", "boxes.filter(bx=>!bx.closest('aside')).forEach(bx=>{const grid=bx.closest('.grid');if(!grid)return;const as=grid.querySelector('aside');if(!as)return;const g=parseFloat(getComputedStyle(as).rowGap)||0;let tot=g*Math.max(0,as.children.length-1);for(const k of as.children){if(k.matches('.flow'))continue;const cs=getComputedStyle(k);tot+=k.getBoundingClientRect().height+(parseFloat(cs.marginTop)||0)+(parseFloat(cs.marginBottom)||0);}const over=tot-as.getBoundingClientRect().height;if(over>0.5){let prev=grid.previousElementSibling;while(prev&&prev.matches('p.src'))prev=prev.previousElementSibling;if(prev&&prev.matches('figure.ph:not(.opener)')){const L=_lin0(bx);prev.style.height=(prev.getBoundingClientRect().height-Math.ceil(over/L)*L).toFixed(2)+'px';}}});boxes.filter(bx=>bx.closest('aside')).forEach",1)
CSS = ('<style id="grade-2311">.page>figure.ph:not(.opener){margin-bottom:8px!important}'
       '.page>figure.nxtab[data-vaga="tabela"]{margin-bottom:6px!important}'
       '.page .flow h4{margin:var(--lin) 0 0!important;position:relative;top:calc(var(--lin)*-.35)}.page .flow>h4:first-child{margin-top:0!important}.page .flow h4.topo{top:0}</style>')
# texto que abre a lateral (sem peça acima) fica alinhado ao alto das outras colunas; a sobra vai para o pé, antes do box
FIRST = "const _abre=b=>{const a=b.closest('aside');return !!a&&a.firstElementChild===b;};"
L106_OLD = "if(ult&&(+getComputedStyle(ult).columnCount||1)<2){"
L106_NEW = "if(ult&&(+getComputedStyle(ult).columnCount||1)<2&&!_abre(ult)){"
STEP2_OLD = "boxes.filter(bx=>bx.closest('aside')).forEach(bx=>{bx.style.paddingTop="
STEP2_NEW = "boxes.filter(bx=>bx.closest('aside')&&!_abre(bx)).forEach(bx=>{bx.style.paddingTop="

f = sys.argv[1]; s = open(f).read()
if NEW1 in s and NEW not in s:
    s = s.replace(NEW1, NEW)
if NEW not in s:
    assert s.count(OLD) == 1, 'trecho do alinhamento não encontrado'
    s = s.replace(OLD, NEW)
s = s.replace(s[s.find('<style id="grade-2311">'):s.find('</style>', s.find('<style id="grade-2311">'))+8], '') if '<style id="grade-2311">' in s else s
if '</head>' in s:
    s = s.replace('</head>', CSS + '</head>', 1)
if POST not in s:
    assert s.count(POST_OLD) == 1
    s = s.replace(POST_OLD, POST)
if L106_NEW not in s:
    assert s.count(L106_OLD) == 1; s = s.replace(L106_OLD, L106_NEW)
if STEP2_NEW not in s:
    assert s.count(STEP2_OLD) == 1; s = s.replace(STEP2_OLD, STEP2_NEW)
if FIRST not in s:
    s = s.replace("const _lin0=", FIRST + "const _lin0=", 1)
open(f, 'w').write(s); print('ok', f)
