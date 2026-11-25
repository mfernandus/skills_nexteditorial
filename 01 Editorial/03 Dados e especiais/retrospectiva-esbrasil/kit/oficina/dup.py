import asyncio, sys
from playwright.async_api import async_playwright
from pathlib import Path
async def main():
    src=Path(sys.argv[1]).resolve()
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':940,'height':1300})
        await pg.goto(src.as_uri(),wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(2500)
        r=await pg.evaluate('''()=>{const norm=t=>t.replace(/[\\u00ad\\u00a0\\s-]+/g,'');
          const tpl=norm([...document.getElementById('texto').content.children].map(n=>n.textContent).join(''));
          const fl=norm([...document.querySelectorAll('.flow')].sort((a,b)=>a.dataset.flow-b.dataset.flow).map(f=>f.textContent).join(''));
          return [tpl.length,fl.length,tpl===fl]}''')
        print('modelo',r[0],'nas paginas',r[1],'identico' if r[2] else 'DIFERENTE')
        await b.close()
asyncio.run(main())
