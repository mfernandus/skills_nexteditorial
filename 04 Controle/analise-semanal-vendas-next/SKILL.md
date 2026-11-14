---
name: analise-semanal-vendas-next
description: Gera a Análise Semanal de Vendas da Next Editorial — performance individual dos executivos (propostas geradas, aprovadas, pendentes) espelhada com a meta, análise do time no gráfico, e leitura imediata de fechamento da semana. Analisa por produto, por produto editorial e por projeto, com dados do NextorCRM. Acione sempre que o usuário pedir "análise de vendas", "relatório de performance", "como está o time", "fechamento da semana", "análise por executivo", ou quando a tarefa agendada das 18:30 disparar. Também é a skill canônica do painel comercial diário/semanal da casa.
---

# Análise Semanal de Vendas — Next Editorial

Skill para produzir o painel de gestão comercial da Next Editorial a partir do **NextorCRM**: performance individual por executivo, consolidado do time em gráficos, e leitura imediata de fechamento da semana — sempre espelhado com a **meta do plano comercial** e quebrado por **produto, produto editorial e projeto**.

Executivos do plano: **Mário Fernando Souza, Claudio Janssen, Magno Araújo, Leticia Lima**. Pré-venda: **Rayenne Fagundes** (propostas atribuídas ao executivo dono da conta).

## Quando usar
- Tarefa agendada diária às 18:30 (leitura do dia sobre a semana/mês).
- Pedidos de "análise de vendas / performance / como está o time / fechamento da semana".
- Análise individual de um executivo.

## 1. Coleta de dados (NextorCRM — MCP `nextor`)
Puxe SEMPRE dados ao vivo (nunca de memória):

1. **Metas do plano** — `get_comercial_metas` (meta por executivo e por produto; ritmo diário/semanal de contatos, propostas, visitas). Meta consolidada de referência: **R$ 1.210.000/mês**, distribuída: Mário 467.500 (38,6%), Claudio/Magno/Leticia 247.500 cada (20,5%). Por produto: Comunhão 150k, ES Brasil 300k (prioridade 25%), Livro 100 Praias 300k, ES Brasil Site 120k, Site Comunhão 100k, PróCidade 240k.
2. **Propostas** — `search_proposals`:
   - **Aprovadas** (`status="Aprovado"`, `sort="recent"`, `limit=100`) → realizado. Competência = **mês de aprovação** (`last_update` no mês corrente).
   - **Enviadas** (`status="Enviado"`) e **Pendentes** (`status="Pendente"`) → pipeline aberto ("propostas geradas / a fechar").
   - **Geradas** = propostas criadas no período (`proposal_date` na semana/mês).
3. **Responsável de cada proposta** — `get_proposal_details` traz `created_by` (executivo). Para propostas da pré-venda (Rayenne), atribua ao **executivo dono da conta**: confira `get_comercial_carteira` (admin: `executivo_id` 2=Mário, 25=Claudio, 26=Magno, 3160=Leticia).
4. **Pipeline por executivo/estágio** — `get_comercial_kanban` (Prospect, Para Hoje, Agendamento, Proposta, Enviado/Pendente) e `get_comercial_carteira`.

Mapeamento **projeto → produto do plano**:
- `ES Brasil Especial Rochas… / Mercado Imobiliário / Retrospectiva / Agro / Anuário Verde` → **ES Brasil** (print)
- `Portal ES Brasil` → **ES Brasil Site** · `Portal Comunhão` → **Site Comunhão**
- `Comunhão …` (edições) → **Comunhão** · `Projeto Destinos ES / 100 praias` → **Livro 100 Praias**
- `Procidades` → **PróCidade** · `Serenatas de Natal` → **Next/Projetos (fora do plano)** — soma ao consolidado em linha própria.

## 2. Cálculos
Por **executivo** (individual): nº e R$ de propostas **geradas**, **aprovadas**, **pendentes/enviadas**; **realizado × meta** (atingimento %, gap R$, R$/dia p/ meta); **conversão** (aprovadas ÷ geradas). Por **produto / produto editorial / projeto**: realizado, pipeline, gap, cobertura (pipeline÷gap). **Time**: consolidado + gráficos (barras meta×realizado por executivo; rosca de atingimento global; barras pipeline×gap por produto).

**Projeção e ritmo** (gestão de faturamento): `run_rate = realizado ÷ dias decorridos`; `projeção = run_rate × dias do mês`; `ritmo necessário = gap ÷ dias restantes`. Sinalize semáforo (verde ≥80% do proporcional, amarelo ≥40%, vermelho <40%).

**Fechamento da semana (leitura imediata)** — com base nas **aprovadas** da semana corrente vs. o proporcional da meta semanal; liste as **top oportunidades em aberto** (maiores Enviado/Pendente) que podem fechar até sexta e o **valor necessário** para bater a semana.

## 3. Estrutura do relatório (A4, padrão Next Editorial)
1. **Painel executivo** — KPIs (meta, realizado, gap, projeção, ritmo necessário) + tabela por produto (meta/realizado/gap/pipeline/cobertura/semáforo) + tabela por executivo.
2. **Fechamento da semana** — aprovadas da semana × meta semanal, projeção do sábado, top oportunidades a fechar, valor que falta.
3. **Análise individual por executivo** — 1 bloco por executivo: geradas/aprovadas/pendentes (nº e R$), atingimento, conversão, contas prioritárias, foco da semana.
4. **Time em gráficos** — barras meta×realizado por executivo, rosca global, pipeline×gap por produto.
5. **Por produto editorial e projeto** — quebra fina (edição/projeto) com realizado e pipeline.
6. **Plano de ação & alertas** — quem está fora do ritmo, produtos parados com pipeline, propostas paradas (aging), foco por executivo.

## 4. Branding & build
- Fonte **Inter** (embutida no `assets/report.css`), tracking **-0,5px**, paleta navy `#001C43` / vermelho `#B11A27`, formato **A4** com margens estreitas.
- Cabeçalho: logo `assets/next_logo.png` (embutir em base64) + faixa Período · Snapshot · Fonte · Status.
- Reaproveite o CSS de `assets/report.css` e siga o **`reference/exemplo_build.py`** como modelo (gera HTML A4, componentes de KPI, tabelas, gráficos em CSS/SVG). Renderize para **PDF** via headless Chromium (Playwright, `format:'A4', printBackground:true`), conferindo que cada página fecha em ~1123px (A4 @96dpi).

## 5. Entrega
Entregue **PDF + HTML** ao usuário (SendUserFile). Cabeçalho "Snapshot: DD/MM/AAAA · HH:MM". Termine com 3–5 bullets de leitura executiva e o **foco da semana** por executivo.

## Notas de governança
- Realizado = status **Aprovado**, competência do mês. Valores em **bruto**, salvo indicação (Serra e demais vendas via agência: mostrar **líquido a faturar** = bruto − 20%).
- Serenatas de Natal e outros Next/Projetos entram **fora do plano**, em linha própria, mas somam ao consolidado.
- Dados são **vivos** (propostas mudam ao longo do dia) — este é um **snapshot**; use o horário de corte fixo (18:30).
