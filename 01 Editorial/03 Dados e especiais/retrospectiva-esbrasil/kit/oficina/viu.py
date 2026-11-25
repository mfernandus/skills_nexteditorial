import asyncio, sys
from playwright.async_api import async_playwright
from pathlib import Path
async def main():
    src=Path(sys.argv[1]).resolve()
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':940,'height':1300})
        await pg.goto(src.as_uri(),wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(2500)
        r=await pg.evaluate('''()=>{const out=[];document.querySelectorAll('.flow p').forEach(el=>{if(el.classList.contains('corte')||el.classList.contains('vaga-aspa'))return;
          // última linha: palavras cujo retângulo está na mesma altura do último
          const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let nodes=[];while(w.nextNode())nodes.push(w.currentNode);
          const r=document.createRange();let last=null,txt='';const rects=[];
          for(const n of nodes){for(let i=0;i<n.length;i++){r.setStart(n,i);r.setEnd(n,i+1);const q=r.getClientRects()[0];if(q&&q.width>0)rects.push([q.top,q.left,q.right,n.textContent[i]]);}}
          if(!rects.length)return;if(el.classList.contains('cont')&&new Set(rects.map(x=>Math.round(x[0]))).size<2)out.push({fragmento:el.textContent.replace(/\u00ad/g,'').slice(0,40),flow:el.closest('.flow').dataset.flow});const lt=rects[rects.length-1][0];const ll=rects.filter(x=>Math.abs(x[0]-lt)<3&&Math.abs(x[1]-rects[rects.length-1][1])<400);
          const tops=new Set(rects.map(x=>Math.round(x[0])+'|'+Math.round(x[1]/150)));if(tops.size<2)return;
          const wid=Math.max(...ll.map(x=>x[2]))-Math.min(...ll.map(x=>x[1]));const cw=el.getBoundingClientRect().width;const cwc=el.closest('.flow');
          const n=+getComputedStyle(cwc).columnCount||1;const cww=(cwc.clientWidth-(n-1)*17.56)/n;
          // linhas frouxas: espaço médio entre palavras muito largo
          const porLinha={};for(const x of rects){const FL=cwc.getBoundingClientRect().left;const k=Math.round(x[0])+'|'+Math.floor((x[1]-FL+2)/(cww+17.56));(porLinha[k]=porLinha[k]||[]).push(x);}
          const ks=Object.keys(porLinha);ks.forEach((k,ix)=>{const L=porLinha[k];if(L===porLinha[ks[ks.length-1]])return;const esp=L.filter(x=>x[3]===' '||x[3]==='\u00a0');if(!esp.length)return;
            const larg=Math.max(...L.map(x=>x[2]))-Math.min(...L.map(x=>x[1]));const letras=L.filter(x=>x[3]!==' '&&x[3]!=='\u00a0').reduce((a,x)=>a+(x[2]-x[1]),0);const g=(larg-letras)/esp.length;
            if(g>10)out.push({flow:cwc.dataset.flow,frouxa:g.toFixed(1),linha:L.map(x=>x[3]).join('').replace(/\u00ad/g,'')});});
          if(wid<cww*0.37)out.push({flow:cwc.dataset.flow,ratio:(wid/cww).toFixed(2),ultima:ll.map(x=>x[3]).join('').replace(/\\u00ad/g,''),inicio:el.textContent.replace(/\\u00ad/g,'').slice(0,60)})});return out}''')
        for x in r: print(x)
        await b.close()
asyncio.run(main())
