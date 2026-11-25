"""PDF vetorial no tamanho da revista (205 x 275 mm). Uso: python3 ../pdf.py capitulo-prova.html saida.pdf"""
import asyncio, os, sys
from playwright.async_api import async_playwright
CSS='''@page{size:205mm 275mm;margin:0}
html,body{background:#fff!important;margin:0!important}
.note,.pg,.apur,.banco,.atual,.dossie{display:none!important}
.wrap{padding:0!important;margin:0!important;max-width:none!important;gap:0!important;display:block!important}
.pagebox{width:900px!important;height:1207px!important;overflow:hidden!important;break-after:page;page-break-after:always;position:relative}
.page{transform:none!important;box-shadow:none!important}'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':940,'height':1300})
        await pg.goto('file://'+os.path.abspath(sys.argv[1])); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(3000)
        await pg.add_style_tag(content=CSS); await pg.wait_for_timeout(500)
        await pg.pdf(path=sys.argv[2],width='205mm',height='275mm',scale=round(205/25.4*96/900,4),print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
asyncio.run(main())
