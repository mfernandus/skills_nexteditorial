---
name: "materia-igrejas-abertas-comunhao"
description: "Matéria mensal da Comunhão sobre CNPJs de igrejas evangélicas abertos e baixados, com os números do Evangélicos em Números, logo depois da carga mensal do CNPJ."
---

# Matéria mensal: igrejas evangélicas abertas no mês (Comunhão)

Roda logo depois da skill `atualizacao-cnpj-templos`, e só quando ela carregou uma base nova da Receita. Se não houve base nova, termine com "Sem fato novo nesta rodada".

**Antes de tudo, carregue a skill `padrao-publicacao-next`.** As regras comuns valem: publicação direta, pautas proibidas, matéria agendada, feed do Instagram só manual, duplicidade, fontes, direitos, texto, SEO, imagem, avisos e economia do plano. Nada em caixa alta.

## Dados (só do banco do Evangélicos em Números)

Projeto Lovable `bd496ff6-6711-470b-aef0-fc1c2b6a611e`, ferramenta `query_database`, só leitura.

1. **Termômetro do Brasil, 36 meses:**
   ```sql
   select templos_termometro(null, null, 36);
   ```
   Cada mês traz aberturas e baixas evangélicas, o total de todas as religiões e a marca `parcial`.
2. **Janela de 12 meses:** os 12 meses mais recentes da série, os mesmos do site (os mais novos podem vir como parciais). Some aberturas e baixas e compare com os 12 meses anteriores.
3. **Mês consolidado:** o mês mais recente com `parcial` = false. Compare as aberturas dele com o mesmo mês do ano anterior.
4. **Estados nos 12 meses:**
   ```sql
   select codigo_uf, sum(abertas) from mv_cnpj_aberturas_mes where religiao = 'evangelica' and mes >= '<início da janela>' group by 1 order by 2 desc;
   ```
   Dê as 5 maiores e o Espírito Santo (32).
5. **Denominações das aberturas nos 12 meses:**
   ```sql
   select denominacao_slug, sum(abertas) from mv_cnpj_aberturas_mes where religiao = 'evangelica' and mes >= '<início>' group by 1 order by 2 desc;
   ```
   Use os rótulos da casa: assembleia-de-deus = Assembleia de Deus, vazio = sem denominação identificada, outras-pentecostais = outras pentecostais, e assim por diante.
6. **Contexto:** total de CNPJs evangélicos ativos.
   ```sql
   select sum(ativos) from mv_templos_municipio where origem = 'cnpj' and religiao = 'evangelica';
   ```

## Regras de redação desta pauta

- **O que o número mede:** nunca escreva "templos novos" ou "igrejas novas". O dado é "CNPJs de organizações religiosas evangélicas abertos". Uma igreja pode funcionar sem CNPJ próprio, e um CNPJ pode registrar uma congregação que já existia; diga isso em uma frase.
- **Meses recentes:** diga que os meses mais novos ainda podem subir na próxima atualização da Receita, porque a data de início de atividade pode ser retroativa.
- **Comparações:** compare só janelas iguais, 12 meses com 12 meses e mês consolidado com o mesmo mês do ano anterior. Variação em % com uma casa decimal.
- **Classificação por nome:** a denominação vem do nome da organização e é estimativa. Diga isso ao citar igrejas.
- **Sem juízo de valor:** sem "explosão", "boom" ou "crise". Os números falam.
- **Fontes e links:**
  - fonte oficial: Receita Federal, dados abertos do CNPJ, base AAAA-MM. Link externo: https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK
  - link para o portal, que é da casa: https://evangelicosbr.lovable.app/templos
- **Rodapé:** `<p><em>Com informações da Receita Federal e do Evangélicos em Números, da Revista Comunhão</em></p>`
- **Texto:** 350 a 550 palavras, dois ou três intertítulos (h2), uma peça do NXtab no lugar da tabela simples, com os 5 estados e o Espírito Santo (decisão do Mário Fernando, 23/11/2026; `c-barras`, marca `com`, ES em destaque, subtítulo com a janela de 12 meses e fonte "Receita Federal, CNPJ, base AAAA-MM; Evangélicos em Números."), autor "Redação". Segunda leitura: rode de novo a consulta do item 4 dos Dados e monte o `conferencia.json` a partir desse segundo resultado (url https://evangelicosbr.lovable.app/templos); confira pela seção 12 da `dados-e-graficos-next`.
- **Título:** até 60 caracteres, com o número do Brasil nos 12 meses. Exemplo de forma: "Brasil abriu 6,1 mil CNPJs de igrejas evangélicas em 12 meses".
- **Palavra-chave SEO:** "igrejas evangélicas abertas".
- **Duplicidade:** se a equipe já publicou o mesmo levantamento no mês, não publique e registre "coberto pela equipe".

## Publicação

- Portal Comunhão (4), categoria Igreja e Missões › Igreja (id 6060). Se o id for recusado, siga a regra da seção 3 do padrão.
- Agende para as 9h do mesmo dia (horário de Brasília). A matéria agendada segue a seção 2.2 do padrão: nada de redes até ela ir ao ar.
- **Imagem:** NX Fotos primeiro, com foto real de culto, fachada genérica de igreja ou fiéis sem rosto identificável de menor, e conferência e tratamento da seção 9.3. Na falta, imagem por IA da seção 9.1, sem símbolo nem templo de denominação específica.

## Resumo

Título do resumo: "Matéria mensal: igrejas abertas". Siga a seção 10 do padrão e acrescente uma linha com o total dos 12 meses, o mês consolidado e a variação.

## Modelo recomendado
- Nível: Sonnet
- Nota: 7/12 (raciocínio 1, fontes 1, texto 1, números 2, fluxo 1, risco 1)
- Motivo: uma base fixa e consultas prontas, mas com janelas e variações a calcular; publica direto, o que barra o Haiku.
- Teste: não testado, primeira execução monitorada na próxima carga mensal.
- Subir para Opus se: comparação de janelas ou variação errada for ao ar.