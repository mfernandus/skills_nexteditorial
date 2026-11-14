# -*- coding: utf-8 -*-
CSS = open("_css.txt").read()
LOGO = open("_logo.txt").read()
EMISS = "14/08/2026 · 10:00"

# ---------- component styles (appended) ----------
CSS += """
  .sub2{font-size:9pt;color:var(--muted);margin-top:5px;font-weight:500}
  .callout{border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:#fff}
  .callout.warn{border-left:4px solid var(--red)}
  .callout .cl-h{font-size:7pt;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
  .callout .cl-v{font-size:17pt;font-weight:900;color:var(--navy);line-height:1;margin-top:4px}
  .callout .cl-v.red{color:var(--red)} .callout .cl-v.green{color:var(--green)}
  .callout .cl-f{font-size:6.8pt;color:var(--muted);margin-top:4px;line-height:1.35}
  .cov{position:relative;background:var(--soft2);border-radius:4px;height:16px;overflow:hidden}
  .cov > i{position:absolute;top:0;left:0;height:100%;border-radius:4px}
  .cov .cvv{position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:6.2pt;font-weight:800;color:var(--navy);z-index:2}
  .acard{border:1px solid var(--line);border-left:4px solid var(--navy);border-radius:0 6px 6px 0;padding:9px 12px;background:#fff;margin-bottom:8px}
  .acard.r{border-left-color:var(--red)} .acard.y{border-left-color:#f59e0b} .acard.g{border-left-color:var(--green)}
  .acard .ah{font-size:8pt;font-weight:900;color:var(--navy)}
  .acard .as{font-size:7.2pt;color:#4b5563;line-height:1.45;margin-top:3px}
  .acard .as b{color:var(--navy)}
  .sem{display:inline-block;width:8px;height:8px;border-radius:50%;vertical-align:middle;margin-right:4px}
  .sem.g{background:var(--green)} .sem.y{background:#f59e0b} .sem.r{background:#ef4444}
  .wk{display:flex;align-items:flex-end;gap:14px;height:120px;border-bottom:1.5px solid var(--navy);padding:0 8px}
  .wkc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
  .wkbar{width:60%;background:linear-gradient(180deg,#0a3163,var(--navy));border-radius:3px 3px 0 0;position:relative;min-height:2px}
  .wkbar.ideal{background:repeating-linear-gradient(45deg,#dde4ee,#dde4ee 5px,#eef2f7 5px,#eef2f7 10px)}
  .wkbar .wv{position:absolute;top:-13px;left:50%;transform:translateX(-50%);font-size:5.8pt;font-weight:700;color:#374151;white-space:nowrap}
  .wklab{display:flex;justify-content:space-around;padding:6px 8px 0}
  .wklab div{flex:1;text-align:center;font-size:6.6pt;font-weight:700;color:var(--navy)}
"""

def br(v):
    s = f"{v:,.0f}".replace(",", ".")
    return s

def mast():
    return ('<div class="masthead"><div class="brand">'
      '<img class="brand-lockup" src="'+LOGO+'" alt="Next Editorial">'
      '<div class="kicker">Relatório de Vendas · Gestão & Performance</div></div>'
      '<div class="meta-top">'
      '<div class="mt-col"><span class="l">Período</span><span class="v">01–31/08/2026</span></div>'
      '<div class="mt-col"><span class="l">Snapshot</span><span class="v">'+EMISS+'</span></div>'
      '<div class="mt-col"><span class="l">Fonte</span><span class="v">NextorCRM</span></div>'
      '<div class="mt-col status"><span class="l">Status</span><span class="v">Ciclo em curso</span></div>'
      '</div></div>')

def foot(n):
    return ('<div class="footer"><span>Next Editorial · Relatório de Vendas · Agosto 2026</span>'
      '<span>NextorCRM · '+EMISS+' · página '+n+'</span></div>')

H = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
     '<title>Relatório de Vendas — Gestão · Agosto 2026</title>'
     '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'
     '<style>'+CSS+'</style></head><body>')

# ============ DADOS ============
META = 1210000
# realizado por produto (dentro do relatório)
prod = [
 # nome, sub, meta, realizado, pipeline, stale_note
 ("Comunhão","Comunhão — 329",150000,0,120000,"pipeline só de edição jun/26 (revisar)"),
 ("ES Brasil","Especial Rochas · Merc. Imob · Retrospectiva",300000,166624.50,400905,""),
 ("Livro 100 Praias","Projeto Destinos ES 26",300000,0,235000,""),
 ("ES Brasil Site","Portal ES Brasil",120000,28624.69,18000,""),
 ("Site Comunhão","Portal Comunhão",100000,6000.49,0,"sem pipeline — originar"),
 ("PróCidade","Procidades 2026",240000,0,348800,""),
]
REAL_TOTAL = 241249.68           # inclui Serenatas 40k (fora do plano)
REAL_PLANO = sum(p[3] for p in prod)   # dentro do plano
PIPE_PLANO = sum(p[4] for p in prod)
GAP_TOTAL = META - REAL_TOTAL    # a realizar (consistente com o relatório)
PIPE_SEREN = 180000
PIPE_TOTAL = PIPE_PLANO + PIPE_SEREN
# projeção
DIAS = 31; DECOR = 14; REST = DIAS-DECOR
run_rate = REAL_TOTAL/DECOR
proj = run_rate*DIAS
proj_pct = proj/META*100
need_day = GAP_TOTAL/REST
ratio = need_day/run_rate
# execs
execs = [
 ("Mário Fernando Souza",467500,176675.18),
 ("Claudio Janssen",247500,24574.50),
 ("Magno Araújo",247500,40000.00),
 ("Leticia Lima",247500,0.0),
]

def sem_for(pct):
    return "g" if pct>=80 else ("y" if pct>=40 else "r")

# ===================== PAGE 1 — PAINEL EXECUTIVO =====================
p1 = '<div class="page">' + mast()
p1 += ('<div class="titlewrap"><div class="eyebrow">Painel Executivo · Gestão de Faturamento</div>'
  '<h1>Relatório de Vendas — Agosto 2026</h1>'
  '<div class="sub2">Performance da equipe · projeção de fechamento · recuperação de produtividade</div></div>')
# KPIs faturamento
p1 += '<div class="kpis">'
p1 += '<div class="kpi dark"><div class="lbl">Meta consolidada</div><div class="val">R$ 1,21 mi</div><div class="foot">plano do mês</div></div>'
p1 += '<div class="kpi accent"><div class="lbl">Realizado (aprovado)</div><div class="val">R$ 241 mil</div><div class="foot">R$ '+br(REAL_TOTAL)+' · 19,9%</div></div>'
p1 += '<div class="kpi"><div class="lbl">Gap para a meta</div><div class="val" style="color:var(--red)">R$ 969 mil</div><div class="foot">falta para bater</div></div>'
p1 += '<div class="kpi"><div class="lbl">Projeção fim do mês</div><div class="val">'+f"{proj_pct:.0f}".replace('.',',')+'%</div><div class="foot">no ritmo atual ≈ R$ '+br(proj)+'</div></div>'
p1 += '<div class="kpi"><div class="lbl">Ritmo necessário</div><div class="val">R$ 57 mil<span style="font-size:8pt">/dia</span></div><div class="foot">'+f"{ratio:.1f}".replace('.',',')+'× o ritmo atual</div></div>'
p1 += '</div>'
# alerta de ritmo
p1 += ('<div class="srcbar" style="border-left-color:var(--red)"><b>Leitura de faturamento:</b> no dia '+str(DECOR)+' de '+str(DIAS)+
  ' ('+f"{DECOR/DIAS*100:.1f}".replace('.',',')+'% do ciclo), o realizado é <b>R$ '+br(REAL_TOTAL)+'</b> (19,9%). '
  'No ritmo atual (R$ '+br(run_rate)+'/dia) o mês fecha em <b>~'+f"{proj_pct:.0f}".replace('.',',')+'%</b>. '
  'Para bater a meta são necessários <b>R$ '+br(need_day)+'/dia</b> nos '+str(REST)+' dias restantes — '+f"{ratio:.1f}".replace('.',',')+'× o atual. '
  'O <b>pipeline aberto (R$ '+br(PIPE_TOTAL)+')</b> cobre '+f"{PIPE_TOTAL/GAP_TOTAL:.2f}".replace('.',',')+'× o gap: o desafio é <b>conversão</b>, não originação.</div>')
# tabela produto: meta / realizado / gap / pipeline / cobertura / semáforo
p1 += ('<div class="sec"><div class="sec-h"><h2>Faturamento por produto — meta · realizado · gap · pipeline</h2>'
  '<span class="note">valores em R$ · cobertura = pipeline ÷ gap</span></div>')
p1 += ('<table><thead><tr><th style="width:9px"></th><th>Produto</th><th>Meta</th><th>Realizado</th><th>Atg.</th>'
  '<th>Gap</th><th>Pipeline aberto</th><th>Cobertura</th></tr></thead><tbody>')
for nome,sub,meta,real,pipe,note in prod:
    atg = real/meta*100 if meta else 0
    gap = meta-real
    cov = pipe/gap if gap>0 else 0
    covtxt = (f"{cov:.1f}".replace('.',',')+"×") if gap>0 else "—"
    atgtxt = f"{atg:.1f}".replace('.',',')+"%"
    subh = '<span class="sub-line">'+sub+(' · '+note if note else '')+'</span>'
    p1 += ('<tr><td><span class="sem '+sem_for(atg)+'"></span></td>'
      '<td style="text-align:left">'+nome+subh+'</td><td>'+br(meta)+'</td><td class="realz">'+br(real)+'</td>'
      '<td><span class="pct '+('ok' if atg>=40 else 'low')+'">'+atgtxt+'</span></td>'
      '<td>'+br(gap)+'</td><td style="font-weight:700;color:var(--blue)">'+br(pipe)+'</td>'
      '<td style="font-weight:800">'+covtxt+'</td></tr>')
p1 += ('</tbody><tfoot><tr><td></td><td style="text-align:left">Total (plano)</td><td>'+br(META)+'</td><td>'+br(REAL_PLANO)+'</td>'
  '<td>'+f"{REAL_PLANO/META*100:.1f}".replace('.',',')+'%</td><td>'+br(META-REAL_PLANO)+'</td>'
  '<td>'+br(PIPE_PLANO)+'</td><td>'+f"{PIPE_PLANO/(META-REAL_PLANO):.1f}".replace('.',',')+'×</td></tr></tfoot></table>'
  '<div style="font-size:6.6pt;color:var(--muted);margin-top:4px">Serenatas de Natal (fora do plano): realizado R$ 40.000 · pipeline R$ 180.000. Total realizado consolidado R$ '+br(REAL_TOTAL)+'.</div></div>')
# por executivo (resumo)
p1 += ('<div class="sec"><div class="sec-h"><h2>Faturamento por executivo</h2>'
  '<span class="note">realizado × meta · gap individual</span></div>')
p1 += ('<table><thead><tr><th style="width:9px"></th><th>Executivo</th><th>Meta</th><th>Realizado</th><th>Atg.</th><th>Gap</th><th>R$/dia p/ meta</th></tr></thead><tbody>')
for nome,meta,real in execs:
    atg=real/meta*100; gap=meta-real; nd=gap/REST
    p1 += ('<tr><td><span class="sem '+sem_for(atg)+'"></span></td><td style="text-align:left">'+nome+'</td>'
      '<td>R$ '+br(meta)+'</td><td class="realz">R$ '+br(real)+'</td>'
      '<td><span class="pct '+('ok' if atg>=30 else 'low')+'">'+f"{atg:.1f}".replace('.',',')+'%</span></td>'
      '<td>R$ '+br(gap)+'</td><td style="font-weight:700">R$ '+br(nd)+'</td></tr>')
p1 += ('</tbody><tfoot><tr><td></td><td style="text-align:left">Consolidado</td><td>R$ '+br(META)+'</td><td>R$ '+br(REAL_TOTAL)+'</td>'
  '<td>19,9%</td><td>R$ '+br(GAP_TOTAL)+'</td><td>R$ '+br(need_day)+'</td></tr></tfoot></table></div>')
p1 += foot("1/5") + '</div>'

# ===================== PAGE 2 — RITMO & PROJEÇÃO =====================
p2 = '<div class="page">' + mast()
p2 += ('<div class="sec" style="margin-top:16px"><div class="sec-h"><h2>Ritmo & Projeção de fechamento</h2>'
  '<span class="note">curva do ciclo · projeção · ritmo necessário</span></div>')
p2 += '<div class="charts" style="grid-template-columns:1fr 1fr">'
# callouts
p2 += ('<div class="chart-card"><div class="chart-title">Onde o mês fecha no ritmo atual</div>'
  '<div class="chart-sub">projeção linear com base no realizado até o dia '+str(DECOR)+'</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
  '<div class="callout"><div class="cl-h">Ritmo atual</div><div class="cl-v">R$ '+br(run_rate)+'<span style="font-size:8pt">/dia</span></div><div class="cl-f">realizado ÷ '+str(DECOR)+' dias</div></div>'
  '<div class="callout warn"><div class="cl-h">Projeção fim do mês</div><div class="cl-v red">R$ '+br(proj)+'</div><div class="cl-f">'+f"{proj_pct:.0f}".replace('.',',')+'% da meta · gap projetado R$ '+br(META-proj)+'</div></div>'
  '<div class="callout"><div class="cl-h">Dias restantes</div><div class="cl-v">'+str(REST)+'</div><div class="cl-f">de '+str(DIAS)+' dias do ciclo</div></div>'
  '<div class="callout warn"><div class="cl-h">Ritmo p/ bater a meta</div><div class="cl-v red">R$ '+br(need_day)+'<span style="font-size:8pt">/dia</span></div><div class="cl-f">'+f"{ratio:.1f}".replace('.',',')+'× o ritmo atual</div></div>'
  '</div></div>')
# weekly bars
sem1=80000.0; sem2=REAL_TOTAL-sem1; ideal_wk=META/4.43
mx=max(sem1,sem2,ideal_wk)
def wkbar(v,lbl,ideal=False):
    h=max(2,v/mx*108)
    cls="wkbar ideal" if ideal else "wkbar"
    return ('<div class="wkc"><div class="'+cls+'" style="height:'+f"{h:.0f}"+'px"><span class="wv">'+('R$ '+br(v))+'</span></div></div>')
p2 += ('<div class="chart-card"><div class="chart-title">Realizado por semana × ritmo ideal</div>'
  '<div class="chart-sub">ideal ≈ R$ '+br(ideal_wk)+'/semana para bater a meta</div>'
  '<div class="wk">'+wkbar(sem1,"SEM 1")+wkbar(sem2,"SEM 2")+wkbar(ideal_wk,"Ideal",True)+'</div>'
  '<div class="wklab"><div>SEM 1<br><small style="color:var(--muted)">01–07/08</small></div>'
  '<div>SEM 2<br><small style="color:var(--muted)">08–14/08</small></div>'
  '<div>Ideal<br><small style="color:var(--muted)">por semana</small></div></div>'
  '<div style="font-size:6.8pt;color:#4b5563;margin-top:8px;line-height:1.4">A SEM 2 acelerou (R$ '+br(sem2)+', puxada pela pré-venda), mas ambas ainda ficam <b>abaixo do ritmo ideal</b> de R$ '+br(ideal_wk)+'/semana. Faltam 2 semanas fortes para recuperar.</div></div>')
p2 += '</div></div>'
# ritmo por executivo
p2 += ('<div class="sec"><div class="sec-h"><h2>Ritmo necessário por executivo</h2>'
  '<span class="note">quanto cada um precisa produzir nos '+str(REST)+' dias restantes</span></div>')
p2 += ('<table><thead><tr><th>Executivo</th><th>Gap</th><th>R$/dia necessário</th><th>Propostas equivalentes</th><th>Leitura</th></tr></thead><tbody>')
tickets={"Mário Fernando Souza":14000,"Claudio Janssen":9000,"Magno Araújo":8000,"Leticia Lima":8000}
for nome,meta,real in execs:
    gap=meta-real; nd=gap/REST; nprop=gap/tickets[nome]
    leitura = ("Ritmo forte, manter foco em fechamento" if real/meta>=0.3 else
               ("Precisa acelerar conversão do funil" if real>0 else "Sem realizado — ativação urgente"))
    p2 += ('<tr><td>'+nome+'</td><td>R$ '+br(gap)+'</td><td style="font-weight:700">R$ '+br(nd)+'</td>'
      '<td>~'+f"{nprop:.0f}"+' propostas</td><td style="text-align:left;font-size:7pt;color:#4b5563">'+leitura+'</td></tr>')
p2 += '</tbody></table></div>'
p2 += foot("2/5") + '</div>'

# ===================== PAGE 3 — FUNIL & CONVERSÃO =====================
p3 = '<div class="page">' + mast()
p3 += ('<div class="sec" style="margin-top:16px"><div class="sec-h"><h2>Funil & Conversão — pipeline aberto</h2>'
  '<span class="note">onde está o dinheiro que falta · Enviado + Pendente</span></div>')
# pipeline por estágio (cards)
p3 += ('<div class="kpis" style="grid-template-columns:repeat(4,1fr)">'
  '<div class="kpi"><div class="lbl">Pipeline total aberto</div><div class="val" style="color:var(--blue)">R$ '+br(PIPE_TOTAL)+'</div><div class="foot">Enviado + Pendente</div></div>'
  '<div class="kpi"><div class="lbl">Cobertura do gap</div><div class="val">'+f"{PIPE_TOTAL/GAP_TOTAL:.2f}".replace('.',',')+'×</div><div class="foot">pipeline ÷ gap (R$ 969 mil)</div></div>'
  '<div class="kpi"><div class="lbl">Enviado (aguarda cliente)</div><div class="val">R$ 733 mil</div><div class="foot">19 propostas</div></div>'
  '<div class="kpi"><div class="lbl">Pendente (interno)</div><div class="val">R$ 415 mil</div><div class="foot">17 propostas</div></div>'
  '</div>')
p3 += '</div>'
# cobertura por produto (bars)
p3 += ('<div class="sec"><div class="sec-h"><h2>Pipeline × gap por produto</h2>'
  '<span class="note">barra = pipeline aberto · marcador = gap do produto</span></div>')
p3 += '<div class="hbars">'
maxv=max(max(p[4],p[2]-p[3]) for p in prod)
for nome,sub,meta,real,pipe,note in sorted(prod,key=lambda x:-x[4]):
    gap=meta-real; cov=pipe/gap if gap>0 else 0
    pw=pipe/maxv*100; gw=gap/maxv*100
    cvtxt = 'pipe R$ '+br(pipe)+' · gap R$ '+br(gap)+' · '+(f"{cov:.1f}".replace('.',',')+'×' if gap>0 else '—')
    p3 += ('<div class="hrow"><div class="hl">'+nome+'</div>'
      '<div class="htrack" style="height:20px"><div class="hmeta" style="width:'+f"{gw:.0f}"+'%"></div>'
      '<div class="hreal" style="width:'+f"{pw:.0f}"+'%;background:linear-gradient(90deg,#2f6fb0,var(--blue))"></div>'
      '<span class="hval" style="color:#111">'+cvtxt+'</span></div></div>')
p3 += '</div></div>'
# top oportunidades + aging
p3 += '<div class="charts" style="grid-template-columns:1fr 1fr;margin-top:14px">'
tops=[("Conceição da Barra","PróCidade","120.000","Enviado"),
 ("Vargem Alta","PróCidade","119.000","Pendente"),
 ("Santa Teresa","PróCidade","109.800","Pendente"),
 ("Sesc","Livro 100 Praias","95.000","Enviado"),
 ("Serra","Livro 100 Praias","80.000","Enviado"),
 ("Serra","Retrospectiva","70.000","Enviado"),
 ("Vila Velha","Livro 100 Praias","60.000","Enviado")]
th='<div class="chart-card"><div class="chart-title">Top oportunidades em aberto</div><div class="chart-sub">fechar as 7 maiores ≈ R$ 653 mil (67% do gap)</div><table style="font-size:7pt"><tbody>'
for cli,prd,val,st in tops:
    th+='<tr><td style="font-weight:700;color:var(--navy)">'+cli+'</td><td style="color:var(--muted)">'+prd+'</td><td style="text-align:right;color:var(--muted)">'+st+'</td><td style="text-align:right;font-weight:700">R$ '+val+'</td></tr>'
th+='</tbody></table></div>'
p3+=th
ag='<div class="chart-card"><div class="chart-title">Propostas paradas (aging)</div><div class="chart-sub">enviadas há muito tempo — revisar/reativar ou descartar</div><table style="font-size:7pt"><tbody>'
aging=[("Samarco · Retrospectiva","55.000","jun · vencida"),
 ("Banestes · Comunhão","50.000","jun/26"),
 ("Serra · Comunhão","40.000","jun/26"),
 ("Cofril · Anuário Verde","20.000","mai/26"),
 ("Cariacica · Comunhão","20.000","jun/26"),
 ("Multivix · Comunhão","10.000","jun/26")]
for cli,val,dt in aging:
    ag+='<tr><td style="font-weight:700;color:var(--navy)">'+cli+'</td><td style="text-align:right;color:var(--red);font-weight:700">'+dt+'</td><td style="text-align:right;font-weight:700">R$ '+val+'</td></tr>'
ag+='</tbody></table></div>'
p3+=ag
p3+='</div>'
p3 += foot("3/5") + '</div>'

# ===================== PAGE 4 — PLANO DE AÇÃO =====================
p4 = '<div class="page">' + mast()
p4 += ('<div class="sec" style="margin-top:16px"><div class="sec-h"><h2>Recuperação de produtividade — plano de ação</h2>'
  '<span class="note">alertas · foco da semana por executivo</span></div>')
# alertas
p4 += '<div class="two" style="grid-template-columns:1fr 1fr;margin-bottom:10px">'
p4 += ('<div><div style="font-size:7.5pt;font-weight:800;color:var(--red);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Alertas críticos</div>'
  '<div class="acard r"><div class="ah">Leticia Lima · 0% da meta</div><div class="as">Sem realizado e sem propostas no ciclo. <b>Ação:</b> plano de ativação — mínimo de contatos P1/dia e 2 primeiras propostas nesta semana.</div></div>'
  '<div class="acard r"><div class="ah">Site Comunhão · gap R$ 94 mil, pipeline R$ 0</div><div class="as">Único produto sem nenhuma proposta aberta. <b>Ação:</b> originar — prospecção dirigida de anunciantes do portal Comunhão.</div></div>'
  '<div class="acard y"><div class="ah">Projeção 44% · ritmo 3,3× abaixo</div><div class="as">No passo atual o mês fecha em ~44%. <b>Ação:</b> mutirão de fechamento nas 7 top oportunidades (R$ 653 mil).</div></div></div>')
p4 += ('<div><div style="font-size:7.5pt;font-weight:800;color:#b45309;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Oportunidades de destrave</div>'
  '<div class="acard g"><div class="ah">PróCidade · pipeline R$ 349 mil (0 realizado)</div><div class="as">3 prefeituras grandes (Conceição, Vargem Alta, Santa Teresa). <b>Fechar 1–2 já destrava</b> o produto e ~1/3 do gap.</div></div>'
  '<div class="acard g"><div class="ah">Livro 100 Praias · pipeline R$ 235 mil (0 realizado)</div><div class="as">Sesc (95k), Serra (80k), Vila Velha (60k) enviados. <b>Ação:</b> reunião de fechamento nesta semana.</div></div>'
  '<div class="acard y"><div class="ah">Mercado Imobiliário · 14 propostas pendentes (~R$ 130 mil)</div><div class="as">Muitas imobiliárias em ticket 6–10k. <b>Ação:</b> força-tarefa de conversão em lote (follow-up + prazo).</div></div></div>')
p4 += '</div>'
# foco por executivo
p4 += ('<div class="sec-h" style="margin-top:6px"><h2 style="font-size:9.5pt">Foco da semana por executivo</h2></div>')
foco=[("Mário Fernando Souza","g","Líder em realizado (37,8%). <b>Foco:</b> fechar PróCidade (Conceição/Vargem Alta/Santa Teresa) e Livro 100 Praias (Sesc/Serra) — as maiores alavancas do mês."),
 ("Claudio Janssen","y","9,9% da meta. <b>Foco:</b> converter carteira de agências/imobiliárias e o restante da Especial Rochas; priorizar as pendentes com maior ticket."),
 ("Magno Araújo","y","16,2% da meta, boa produção na Rochas. <b>Foco:</b> transformar propostas enviadas em fechamento e originar 2 novas contas peso 1."),
 ("Leticia Lima","r","0% — sem produção. <b>Foco (ativação):</b> cadência mínima de contatos P1 e emitir as 2 primeiras propostas até sexta; acompanhamento diário.")]
for nome,c,txt in foco:
    p4 += '<div class="acard '+c+'"><div class="ah">'+nome+'</div><div class="as">'+txt+'</div></div>'
p4 += '</div>'
p4 += foot("4/5") + '</div>'

# ===================== PAGE 5 — GOVERNANÇA =====================
p5 = '<div class="page">' + mast()
p5 += ('<div class="sec" style="margin-top:16px"><div class="sec-h"><h2>Base de cálculo & governança</h2>'
  '<span class="note">como ler os números</span></div>')
p5 += ('<div class="notes"><ol>'
  '<li><b>Realizado</b> = propostas com status <b>Aprovado</b> na competência ago/2026 (NextorCRM): <b>21 propostas, R$ 241.249,68</b> (bruto, salvo indicação). Snapshot de '+EMISS+'.</li>'
  '<li><b>Pipeline aberto</b> = propostas <b>Enviado + Pendente</b> por produto: total <b>R$ '+br(PIPE_TOTAL)+'</b> (cobre '+f"{PIPE_TOTAL/GAP_TOTAL:.2f}".replace('.',',')+'× o gap). O gargalo do mês é <b>conversão</b>, não originação.</li>'
  '<li><b>Projeção</b> = ritmo linear (realizado ÷ dias decorridos × 31). Ritmo necessário = gap ÷ dias restantes. Referência: dia '+str(DECOR)+' de '+str(DIAS)+'.</li>'
  '<li><b>Serra (#807)</b> exibida pelo valor a faturar <b>R$ 32.000</b> (líquido, −20% agência); demais valores em bruto. Recomenda-se padronizar em <b>líquido a faturar</b> nas próximas versões.</li>'
  '<li><b>Serenatas de Natal</b> (Next/Projetos) está <b>fora dos 6 produtos do plano</b>: realizado R$ 40.000 somado ao consolidado, exibido em linha própria.</li>'
  '<li><b>Atividade (leading)</b>: contatos válidos e visitas realizadas aparecem <b>zerados</b> no CRM no ciclo. Registrar essas atividades é pré-requisito para diagnosticar topo de funil × conversão.</li>'
  '<li><b>Dados vivos</b>: propostas são editadas ao longo do dia (valores mudam). Este relatório é um <b>snapshot</b>; recomenda-se um horário fixo de corte para leitura oficial.</li>'
  '</ol></div>')
p5 += foot("5/5") + '</div>'

open("relatorio_gestao_ago26.html","w").write(H+p1+p2+p3+p4+p5+'</body></html>')
print("OK realizado_plano=",REAL_PLANO,"pipe_plano=",PIPE_PLANO,"proj_pct=",round(proj_pct,1),"need_day=",round(need_day))
