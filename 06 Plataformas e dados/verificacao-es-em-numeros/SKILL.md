---
name: "verificacao-es-em-numeros"
description: "Verifica o site ES em Números (esemnumeros.esbrasil.com.br): erros, números novos nas fontes oficiais, coletores quebrados e fotos novas do NX Fotos. Use para a rodada semanal ou mensal."
---

# Verificação do ES em Números

Rodada de auditoria da plataforma ES em Números (ecossistema **ES Brasil**). A skill SÓ PROPÕE: nunca grava nada na base sem o ok explícito de Mário Fernando. Responder sempre em português do Brasil; negrito em **ES Brasil** e **revista ES Brasil**.

## Onde estão os dados

- O site é um app Lovable que monta tudo no navegador: WebFetch não mostra números. Ler direto do banco.
- Projeto Lovable "ES EM NUMEROS V3" (workspace rcolnago2), project_id `3a80f07a-fc2d-4f99-b63f-a748a3268680`. Usar `mcp__Lovable__query_database` só com SELECT.
- Tabelas: `themes` (featured_image, alternative_images), `indicators` (current_value, previous_value, variation, updated_at_data, unit, frequency, source, is_featured, is_active), `indicator_time_series` (date, value, is_preliminary, source_reference, partial_months, partial_kind), `municipios` (imagem_url), `hero_slides`, `sync_logs` (task_name, status, error_message, metadata, created_at), `site_settings`, `ipca_grande_vitoria`, `ipca15_grande_vitoria` (period_date), `fatos_municipais`, `fatos_rochas_es`, `concessoes_es`.
- Considerar público só tema e indicador com is_active = true. Observa Vix e Desenvolvimento Social são temas ocultos.
- NUNCA copiar para relatório ou chat o conteúdo de `site_settings.ai_settings` (contém chaves de API).

## Passos

1. **Coletores**: `select task_name, (array_agg(status order by created_at desc))[1] ultimo, max(created_at), max(created_at) filter (where status='success') ultimo_ok, count(*) filter (where status='error') erros from sync_logs where created_at > now() - interval '30 days' group by 1`. Listar rotinas com último status error/partial e o efeito (que indicador deixou de entrar). Ler `metadata.results` dos parciais: o próprio coletor marca "série a revisar".
2. **Dados vencidos**: comparar a última data de cada indicador ativo (em destaque primeiro) com o calendário de divulgação (IBGE: IPCA ~dia 10, IPCA-15 ~dia 25, PIM-PF regional início do mês, PNAD trimestral por UF meados de fev/mai/ago/nov, Contas Regionais em novembro, estimativa de população em 28/08; MTE Novo Caged fim do mês seguinte; Comex Stat início do mês; Conab café fev/mai/set/dez; Sesp balanço no 1º dia útil do mês; ANP boletim mensal).
3. **Números novos**: para cada indicador vencido ou em destaque, buscar o dado na fonte oficial (WebSearch em modo standard, várias buscas no mesmo turno) e registrar valor, período e link. Conferir também os que estão certos e dizer isso.
4. **Testes de consistência** (SQL + leitura):
   - parte maior que o total (ex.: mortes de motociclistas x mortes no trânsito; conilon + arábica = total);
   - variação percentual calculada sobre taxa ou saldo negativo (deveria ser p.p.);
   - mesmo conceito com valores diferentes (concessões, PPPs, empresas exportadoras, população, participação da indústria);
   - séries de 6 pontos 2020–2025 e séries todas inteiras (carga estimada): `count(*)=6 and min(date)='2020-01-01'`;
   - fonte do card que não bate com `source_reference` do último ponto (ex.: estimativa IJSN rotulada como IBGE);
   - updated_at_data nulo, previous_value nulo, frequency fora do padrão (mensal/trimestral/anual), unidade divergente na mesma família, nomes com espaço no fim, slugs técnicos (ibge-XXXX-YYY) expostos;
   - soma de participações acima de 100% ou muito abaixo.
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