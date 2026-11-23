# registra um resultado de busca do NX Fotos (arquivo salvo) sob um rótulo e mostra um resumo curto
import json,sys,collections,os
DB='buscas.json'
def load(f):
    t=open(f).read()
    j=json.loads(t[t.index('{'):]) if not t.lstrip().startswith('[') else json.loads(json.loads(t)[0]['text'])
    return j
db=json.load(open(DB)) if os.path.exists(DB) else {}
for arg in sys.argv[1:]:
    label,f=arg.split('=',1)
    j=load(f)
    db[label]={'file':f,'total':j.get('total'),'etapa':j.get('etapa'),'itens':j.get('itens',[])}
    its=j.get('itens',[])
    aut=collections.Counter(i.get('author') for i in its)
    print(f"{label}: total {j.get('total')} etapa {j.get('etapa')} | {len(its)} itens | autores {dict(aut.most_common(4))}")
    words=collections.Counter()
    for i in its:
        for w in (i.get('title','')+' '+i.get('description','')).lower().replace(',',' ').split(): 
            if len(w)>4: words[w]+=1
    print('   ',' '.join(w for w,_ in words.most_common(18)))
json.dump(db,open(DB,'w'),ensure_ascii=False)
