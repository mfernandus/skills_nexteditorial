---
name: "verificacao-es-em-numeros"
description: "Audita o site ES em Números (esemnumeros.esbrasil.com.br): erros, coletores e rotinas quebradas, o que o radar de fontes gravou, dados vencidos e fotos novas do NX Fotos. Use para a rodada semanal ou mensal."
---

# Verificação do ES em Números

Rodada de auditoria da plataforma ES em Números (ecossistema **ES Brasil**). A skill SÓ PROPÕE: nunca grava nada na base sem o ok explícito de Mário Fernando. A única exceção é acrescentar ou corrigir linhas no radar de fontes (`lake_sync.radar_fontes`), que é cadastro e não dado publicado. Responder sempre em português do Brasil; negrito em **ES Brasil** e **revista ES Brasil**.

## Divisão de trabalho (desde 25/11/2026)

- **Coletores do banco** (cron do Supabase, cerca de 30 jobs): trazem sozinhos as fontes com API (IBGE/SIDRA, Banco Central, Comex Stat, Caged, Siconfi, ANP etc.).
- **Radar de fontes** (tarefa agendada "ES em Números · radar de fontes oficiais", todo dia às 17h58): lê `lake_sync.radar_fontes`, abre o documento oficial das fontes em PDF ou página (IJSN, Fecomércio-ES, Findes, Santander, LCA, Sinduscon-ES, Conab, Sesp-ES etc.) e GRAVA sozinho período novo, revisão e projeção, registrando em `data_fix_log` (run_label `radar-fontes <data>`).
- **Esta skill**: audita os dois. Não busca número novo para gravar (isso é do radar); confere o que entrou, acha erros, buracos e fontes que o radar não cobre, e propõe correções. É a segunda leitura, feita por quem não gravou.

## Onde estão os dados

- O site é um app Lovable que monta tudo no navegador: WebFetch não mostra números. Ler direto do banco.
- Projeto Lovable "ES EM NUMEROS V3" (workspace rcolnago2), project_id `3a80f07a-fc2d-4f99-b63f-a748a3268680`. Usar `mcp__Lovable__query_database` só com SELECT.
- Tabelas: `themes` (featured_image, alternative_images), `indicators` (current_value, previous_value, variation, updated_at_data, unit, frequency, source, is_featured, is_active), `indicator_time_series` (date, value, is_preliminary, source_reference, partial_months, partial_kind), `municipios` (imagem_url), `hero_slides`, `sync_logs` (task_name, status, error_message, metadata, created_at), `site_settings`, `ipca_grande_vitoria`, `ipca15_grande_vitoria` (period_date), `fatos_municipais`, `fatos_rochas_es`, `concessoes_es`.
- Considerar público só tema e indicador com is_active = true. Observa Vix e Desenvolvimento Social são temas ocultos.
- NUNCA copiar para relatório ou chat o conteúdo de `site_settings.ai_settings` (contém chaves de API).

## Passos

1. **Coletores e rotinas**:
   - Funções de borda: `select task_name, (array_agg(status order by created_at desc))[1] ultimo, max(created_at), max(created_at) filter (where status='success') ultimo_ok, count(*) filter (where status='error') erros from sync_logs where created_at > now() - interval '30 days' group by 1`. Listar rotinas com último status error/partial e o efeito (que indicador deixou de entrar). Ler `metadata.results` dos parciais: o próprio coletor marca "série a revisar".
   - Jobs do banco: `select j.jobname, d.status, d.return_message, d.start_time from cron.job_run_details d join cron.job j using (jobid) where d.start_time > now() - interval '8 days' and d.status <> 'succeeded' order by d.start_time desc`.
   - Publicação dos dados municipais: `select ultima_sincronia, ultimo_resultado from lake_sync.config`. Se `ultima_sincronia` tiver mais de 26 horas, a publicação diária (`lake_sync.publicar()`, 8h17) parou: achar a causa e propor a correção.
   - Radar: `select fonte, publicacao, proxima_divulgacao, ultima_checagem, ultimo_achado from lake_sync.radar_fontes where ativo order by ultima_checagem nulls first`. Apontar fonte nunca checada, checagem com mais de 8 dias, `ultimo_achado` com falha (bloqueio, login, fora do ar) e `proxima_divulgacao` vencida há mais de 15 dias sem número novo.
2. **Dados vencidos**: comparar a última data de cada indicador ativo (em destaque primeiro) com o calendário de divulgação (IBGE: IPCA ~dia 10, IPCA-15 ~dia 25, PIM-PF regional início do mês, PNAD trimestral por UF meados de fev/mai/ago/nov, Contas Regionais em novembro, estimativa de população em 28/08; MTE Novo Caged fim do mês seguinte; Comex Stat início do mês; Conab café fev/mai/set/dez; Sesp balanço no 1º dia útil do mês; ANP boletim mensal; IJSN PIB trimestral mar/jun/set/dez e PIB estadual em novembro). Para cada indicador vencido, dizer quem deveria ter trazido o dado: um coletor do banco (então o coletor falhou) ou o radar (então ver a linha dele). Indicador vencido de fonte sem API que não aparece em nenhuma linha do radar: acrescentar a fonte em `lake_sync.radar_fontes` (fonte, publicacao, url, tipo consolidado/estimativa/projecao, periodicidade, proxima_divulgacao, indicadores) e dizer isso no relatório.
3. **Conferência do que o radar gravou**: `select ran_at, indicator_slug, field, old_value, new_value, source_url, note from data_fix_log where run_label like 'radar-fontes%' and ran_at > now() - interval '8 days' order by ran_at`. Para cada linha, abrir o `source_url` e conferir valor, unidade, período, tipo (acumulado no ano, anual, 4 trimestres) e se ficou como preliminar ou parcial quando devia. Conferir também se os indicadores calculados (per capita, participação no Brasil, taxa de crescimento) foram refeitos quando o insumo mudou. Dizer o que está certo e listar o que está errado com a correção proposta. Número novo que o radar não pegou vai como item do relatório, com fonte, período e link, para a correção do radar (não gravar).
4. **Testes de consistência** (SQL + leitura):
   - parte maior que o total (ex.: mortes de motociclistas x mortes no trânsito; conilon + arábica = total);
   - variação percentual calculada sobre taxa ou saldo negativo (deveria ser p.p.);
   - mesmo conceito com valores diferentes (concessões, PPPs, empresas exportadoras, população, participação da indústria);
   - séries de 6 pontos 2020–2025 e séries todas inteiras (carga estimada): `count(*)=6 and min(date)='2020-01-01'`;
   - fonte do card que não bate com `source_reference` do último ponto (ex.: estimativa IJSN rotulada como IBGE);
   - updated_at_data nulo, previous_value nulo, frequency fora do padrão (mensal/trimestral/anual), unidade divergente na mesma família, nomes com espaço no fim, slugs técnicos (ibge-XXXX-YYY) expostos;
   - soma de participações acima de 100% ou muito abaixo;
   - projeção gravada dentro de série de dado realizado (projeção vai em indicador próprio, `projecao-<o-que>-es-<fonte>`), e estimativa por cima de número consolidado do mesmo período;
   - série que mistura bases (ex.: PIB de um ano já revisado pelo IBGE e o ano seguinte ainda na base antiga do IJSN), com o efeito visível (participação ou per capita que cai sem motivo) e a nota a pôr no card até a fonte reajustar;
   - em `fatos_municipais`, a mesma chave (município, indicador, ano, mês) vinda de carga avulsa e do coletor (`source_reference` diferente de 'procidade-lake'): o coletor prevalece desde 25/11/2026; listar o que sobrar.
5. **Fotos (NX Fotos)**: ver `themes.featured_image`, `alternative_images`, `hero_slides` e `municipios.imagem_url` (contar vazios e banco de imagem genérico, como unsplash). Buscar com `mcp__NXFOTOS__buscar` (orientacao h, tipo foto, ano_de recente, até 6 por busca) usando o mapa abaixo. Na rodada semanal, priorizar o que entrou desde a última rodada. Conferir as melhores com `mcp__NXFOTOS__mostrar_imagens`. Preferir autores da casa (Sidney Pagotto, Willian Girelli, Gleiton Mendes, Claudio Alves); divulgação só com crédito. Evitar fotos com contexto negativo para capa (ex.: greve da PM de 2017). Listar lacunas do acervo como pauta fotográfica. Foto proposta para o site passa antes pela skill `tratamento-fotos-next` (`--marca esbrasil --origem nxfotos --largura 1600 --sufixo`). Foto que já tem a marca da casa (inclusive a invisível) ou foi tratada pelo fotógrafo entra como está (decisão do Mário Fernando de 25/11/2026).

### Mapa de busca por tema

| Tema | Termos |
| --- | --- |
| Capa / Macroeconomia | Terceira Ponte vista aérea; Vitória vista aérea |
| Turismo | Convento da Penha; praia Guarapari; Pedra Azul |
| Agropecuária | café conilon; lavoura; pimenta-do-reino |
| Rochas Naturais | rochas ornamentais; mármore; granito; Cachoeiro |
| Comércio Exterior | Porto de Vitória; Portocel; contêiner |
| Indústria | ArcelorMittal; usina; fábrica; Suzano |
| Energia | FPSO; plataforma de petróleo; energia solar |
| Emprego e Renda / Comércio e Serviços | calçadão; comércio rua; trabalhadores |
| Educação | sala de aula; escola |
| Saúde | hospital; atendimento |
| Infraestrutura | aeroporto de Vitória; rodovia; Terceira Ponte |
| Meio Ambiente | Reserva Natural Vale; Mata Atlântica |
| Economia Criativa | paneleiras; artesanato |
| Cooperativismo | cooperativa |
| Segurança Pública | polícia militar; viatura |
| Democracia | Assembleia Legislativa ES |
| Municípios | nome da cidade |

## Saída

- **Semanal**: resposta curta só com o que mudou desde a última rodada (coletores, dados novos, erros novos, até 3 fotos por tema), cada item com link da fonte e a ação proposta.
- **Mensal (ou primeira rodada do mês)**: documento no tipo Docs, título "ES em Números — Verificação #N", com as seções: Resumo (o que resolver primeiro), Erros visíveis no site (tabela indicador · no site · problema · correção), Problemas estruturais, Números novos para atualizar (tabela com fonte), Próximas divulgações, Fotos (tabela tema · sugestão com link do NX Fotos · autor e ano + lacunas), Fontes.
- Antes de entregar, reconferir cada número contra a base e a fonte; contagens vêm de SQL, não de estimativa.
- Se Mário aprovar correções, aplicar pela base do projeto Lovable apenas o que ele aprovou, com SELECT antes e depois, e registrar o que mudou.

## Referência — 1ª rodada (24/10/2026)

330 indicadores públicos em 21 temas; 154 séries no padrão estimado; 14 erros visíveis; coletores IPCA/IPCA-15 (IBGE timeout desde 23/10), Conab e CUB com falhas; chaves de API em texto puro em site_settings (recomendado mover para secrets e rotacionar). Usar como linha de base para dizer o que foi corrigido.

## Referência — 25/11/2026

PIB do ES 2024 oficial (R$ 233,6 bi, +2,5%) e 2025 pelo IJSN (R$ 248,4 bi, base anterior à revisão); 2026 só como acumulado no ano (+4,8% jan–jun). O IJSN não publica projeção anual do PIB: projeções de 2026 no site são de Fecomércio-ES, Santander e LCA. `lake_sync.publicar()` corrigida (parada de 24 a 25/11 por 40 colisões de carga avulsa do Siconfi). Radar de fontes criado com 17 fontes.