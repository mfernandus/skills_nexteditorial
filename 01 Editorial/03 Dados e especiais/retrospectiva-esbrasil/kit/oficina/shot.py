"""Confere o capítulo: ocupação do texto, sobras nas caixas e captura de cada página.
Uso: python3 ../shot.py capitulo.html [prefixo]"""
import asyncio, sys
from playwright.async_api import async_playwright
from pathlib import Path

async def main():
    src = Path(sys.argv[1]).resolve(); pre = sys.argv[2] if len(sys.argv) > 2 else 'shot'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 940, 'height': 1300})
        await pg.goto(src.as_uri(), wait_until='networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(2500)
        print('ocupacao:', await pg.inner_text('#ocupacao'))
        info = await pg.evaluate('''()=>[...document.querySelectorAll('.flow')].map(f=>{const r=f.getBoundingClientRect();
           const kids=[...f.children]; let last=0; for(const k of kids){const kr=k.getClientRects(); for(const q of kr){ if(q.bottom>last) last=q.bottom; }}
           return {flow:f.dataset.flow, h:Math.round(r.height), cols:getComputedStyle(f).columnCount, livre: kids.length? Math.round(r.bottom-last):Math.round(r.height), nfilhos:kids.length}})''')
        for i in info: print(i)
        # buracos no pé das colunas de cada caixa (coluna que termina antes do fundo, sem ser a última)
        bur = await pg.evaluate('''()=>{const out=[];document.querySelectorAll('.flow').forEach(f=>{const n=+getComputedStyle(f).columnCount||1; if(n<2) return;
           const r=f.getBoundingClientRect(), cw=r.width/n, lim=Array(n).fill(r.top);
           for(const k of f.children){for(const q of k.getClientRects()){const c=Math.min(n-1,Math.max(0,Math.floor((q.left-r.left+2)/cw))); if(q.bottom>lim[c]) lim[c]=q.bottom;}}
           const fim=!!f.querySelector('.fim');lim.forEach((b,c)=>{const gap=Math.round(r.bottom-b); if(gap>3 && (c<n-1||!fim)) out.push({flow:f.dataset.flow,coluna:c+1,buraco_px:gap});});});return out}''')
        for bb in bur: print("buraco", bb)
        tip = await pg.evaluate('''()=>{const out=[];
          document.querySelectorAll('.flow').forEach(f=>{const n=+getComputedStyle(f).columnCount||1;const R=f.getBoundingClientRect();const cw=(R.width-(n-1)*17.56)/n;
            const linhas=el=>{const r=document.createRange();r.selectNodeContents(el);const fm=el.querySelector('.fim');if(fm)r.setEndBefore(fm);const tops={};for(const q of r.getClientRects()){if(q.width<1)continue;const k=Math.round(q.top)+'|'+Math.floor((q.left-R.left+2)/(cw+17.56));const a=tops[k]||{l:q.left,r:q.right,top:q.top,col:Math.floor((q.left-R.left+2)/(cw+17.56))};a.l=Math.min(a.l,q.left);a.r=Math.max(a.r,q.right);tops[k]=a;}return Object.values(tops).sort((a,b)=>a.col-b.col||a.top-b.top)};
            [...f.children].forEach((el,idx)=>{if(el.tagName==='P'&&!el.classList.contains('corte')&&!el.classList.contains('vaga-aspa')){const L=linhas(el);if(L.length>1){const u=L[L.length-1];if((u.r-u.l)<cw*0.33)out.push({tipo:'viuva',flow:f.dataset.flow,txt:el.textContent.slice(-40)})}}
              if(el.tagName==='H4'){const nx=el.nextElementSibling;if(nx){const L=linhas(nx);const c0=L.length?L[0].col:-1;const nc=L.filter(x=>x.col===c0).length;const hcol=linhas(el)[0];if(hcol&&c0===hcol.col&&nc<2&&L.length>1)out.push({tipo:'orfa',flow:f.dataset.flow,txt:el.textContent})}}});
            // linha sozinha no alto da coluna (fim de parágrafo vindo da coluna anterior)
            [...f.children].forEach(el=>{if(el.tagName!=='P')return;const L=linhas(el);const cols=[...new Set(L.map(x=>x.col))];if(cols.length>1){const ult=cols[cols.length-1];if(L.filter(x=>x.col===ult).length===1)out.push({tipo:'linha-sozinha-no-alto',flow:f.dataset.flow,txt:el.textContent.slice(-40)});const pri=cols[0];if(L.filter(x=>x.col===pri).length===1)out.push({tipo:'linha-sozinha-no-pe',flow:f.dataset.flow,txt:el.textContent.slice(0,40)})}});
          });return out}''')
        for t in tip: print(t['tipo'], t)
        # lateral: espaço livre no pé de cada aside
        sides = await pg.evaluate('''()=>[...document.querySelectorAll('aside.side')].map(a=>{const r=a.getBoundingClientRect(); let last=r.top;
           for(const k of a.children){const q=k.getBoundingClientRect(); if(q.bottom>last) last=q.bottom;}
           const pgn=a.closest('.page').className; return {page:pgn, livre:Math.round(r.bottom-last), h:Math.round(r.height)}})''')
        for s in sides: print('aside', s)
        n = await pg.locator('.pagebox').count()
        for i in range(n):
            await pg.locator('.pagebox').nth(i).screenshot(path=f'{pre}-{i+1}.png')
        await b.close()

asyncio.run(main())
