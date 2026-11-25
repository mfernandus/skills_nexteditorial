"""Confere o alinhamento das colunas: topo da 1ª linha de cada coluna, topo das peças da lateral e respiro abaixo das fotos.
Uso: python3 ../alinha.py capitulo.html"""
import asyncio, sys, json
from playwright.async_api import async_playwright
from pathlib import Path
JS = r'''()=>[...document.querySelectorAll('article.page')].map((a,pi)=>{
  const res={page:a.querySelector('.pn')?.textContent, colunas:[], lateral:[], fotos:[]};
  a.querySelectorAll('.flow').forEach(f=>{const n=+getComputedStyle(f).columnCount||1;const R=f.getBoundingClientRect();
    const gap=parseFloat(getComputedStyle(f).columnGap)||0;const cw=(R.width-(n-1)*gap)/n;const tops=Array(n).fill(null),bots=Array(n).fill(null);
    const rg=document.createRange();rg.selectNodeContents(f);
    for(const q of rg.getClientRects()){if(q.width<2||q.height<5)continue;const c=Math.min(n-1,Math.max(0,Math.floor((q.left-R.left+2)/(cw+gap))));
      if(tops[c]===null||q.top<tops[c])tops[c]=q.top; if(bots[c]===null||q.bottom>bots[c])bots[c]=q.bottom;}
    tops.forEach((t,c)=>res.colunas.push({flow:f.dataset.flow,col:c+1,topo:t&&Math.round(t),pe:bots[c]&&Math.round(bots[c]),caixa_topo:Math.round(R.top),caixa_pe:Math.round(R.bottom)}));});
  a.querySelectorAll('aside.side > *').forEach(k=>{const r=k.getBoundingClientRect();res.lateral.push({el:k.className,topo:Math.round(r.top),pe:Math.round(r.bottom)})});
  a.querySelectorAll('figure.ph').forEach(ph=>{if(ph.classList.contains('opener'))return;const r=ph.getBoundingClientRect();
    let prox=null;a.querySelectorAll('.flow, aside.side > *, figure.nxtab').forEach(k=>{const q=k.getBoundingClientRect();if(q.top>=r.bottom-1&&q.left<r.right&&q.right>r.left){if(prox===null||q.top<prox)prox=q.top}});
    res.fotos.push({cls:ph.className,altura:Math.round(r.height),respiro_abaixo:prox===null?null:Math.round(prox-r.bottom)})});
  return res;})'''
async def main():
    src=Path(sys.argv[1]).resolve()
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':940,'height':1300})
        await pg.goto(src.as_uri(),wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(2500)
        for r in await pg.evaluate(JS):
            print('== pág', r['page'])
            for c in r['colunas']: print('  col', c)
            for l in r['lateral']: print('  lat', l)
            for f in r['fotos']: print('  foto', f)
        await b.close()
asyncio.run(main())
