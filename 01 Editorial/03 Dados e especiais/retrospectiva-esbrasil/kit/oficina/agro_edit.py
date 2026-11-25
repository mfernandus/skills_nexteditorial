import re, sys, json, pyphen
"""Troca trechos do texto do Agronegócio. Uso, dentro da pasta agronegocio: python3 ../agro_edit.py trocas.json [capitulo-prova.html]
trocas.json = [["trecho antigo","trecho novo"], ...]; reaplica a hifenização (pip install pyphen)."""
P=sys.argv[2] if len(sys.argv)>2 else 'capitulo-prova.html'
s=open(P,encoding='utf8').read()
k=s.index('<template id="texto">'); e=s.index('</template>',k)
tx=s[k:e].replace('­','')
for a,b in json.load(open(sys.argv[1],encoding='utf8')):
    assert tx.count(a)==1,(a,tx.count(a)); tx=tx.replace(a,b)
h=pyphen.Pyphen(lang='pt_BR',left=2,right=3)
hif=lambda tr: re.sub(r'(?<![-\w])[A-Za-zÀ-ÿ][a-zà-ÿ]{6,}(?![-\w])',lambda w:h.inserted(w.group(0),hyphen='­'),tr)
tx=re.sub(r'>([^<]+)<',lambda m:'>'+hif(m.group(1))+'<',tx)
tx=re.sub(r'<h4>.*?</h4>',lambda m:m.group(0).replace('­',''),tx,flags=re.S)
s=s[:k]+tx+s[e:]
open(P,'w',encoding='utf8').write(s); print('ok')
