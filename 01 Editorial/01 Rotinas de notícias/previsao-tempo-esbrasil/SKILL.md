---
name: "previsao-tempo-esbrasil"
description: "Rotina diária da previsão do tempo da ES Brasil: às 19h prepara o Post A (dia seguinte + 3 dias), o Post B (2 dias) e o stories animado, e agenda tudo no NX Feed para 00h01."
---

# Previsão do tempo — **ES Brasil**

Use quando pedirem a previsão do tempo da **ES Brasil** (rodar agora, refazer um dia, conferir a rotina) ou quando a tarefa agendada das 19h disparar.

## Onde está tudo

O pacote completo (scripts do gerador, mapa do ES, logos, as 6 trilhas, o manual `SKILL.md` com as seções 0 a 16, `INSTALAR.md` e `TAREFA.md`) fica no artefato **eb3abec1-a4d4-40b4-8722-9d9160b207f5** ("Previsão do tempo · ES Brasil — rotina das 19h"), no arquivo `pacote.b64.txt` (o .zip em base64, porque o artefato não serve .zip).

## Como rodar

1. Carregue `mcp__claude-artifacts__read_file` (ToolSearch) e chame só com `slug` e `paths: ["pacote.b64.txt"]`. O arquivo volta salvo no disco: `mkdir -p /tmp/prev && base64 -d 'CAMINHO' > /tmp/prev/pacote.zip && cd /tmp/prev && unzip -o -q pacote.zip`.
2. Leia inteiro `/tmp/prev/previsao-tempo-esbrasil/SKILL.md` e siga a seção 0.
3. Na rodada das 19h, o dia alvo é amanhã: Post A às 00h01, Post B às 00h06, stories animado às 00h01, e os posts da véspera vão para a lixeira.
4. Se a pessoa pedir para rodar fora do horário, pergunte o dia alvo e se publica agora, agenda ou manda como rascunho.

## Redes: só stories, jamais feed

- Nunca criar post de feed, carrossel ou reels da previsão, nem como rascunho ou para revisão (decisão de Mário Fernando, 2/11/2026).
- Ao publicar ou agendar uma matéria, a automação do painel do NX Feed cria sozinha um stories genérico dela, e o NX Feed não aceita um segundo stories da mesma matéria. Por isso: crie o animado ligado ao Post A, cancele só o agendamento do stories automático do Post A (`cancelar_agendamento_instagram`; ele fica guardado no Studio) e agende o animado às 00h01. O Post B fica com o automático do painel.
- Se o automático já tiver saído (matéria publicada na hora), o animado só sai sem vínculo: reenvie o vídeo ao Studio sem `materia_id` e crie o stories com essa mídia (o vínculo é herdado da mídia).

## Regras que não mudam

- Fonte: Incaper primeiro, Climatempo depois. Nunca estimar número.
- Fotos só do NX Fotos, sempre tratadas e coerentes com o tempo. Fatos da dica só de destinoses.com, esbrasil.com.br ou NX Fotos; nunca A Gazeta, Tribuna Online, Folha Vitória e afins.
- Gravar no NX Feed o `out/texto_*.html` exatamente como o gerador entregou: os `<div style="display:contents">` protegem o quadro do wpautop do WordPress. Sem eles, o banner do meio do texto entra dentro do quadro.
- Trava de duplicidade: se a rotina já fez A ou B do dia alvo, não criar nada.
- Rotinas publicam direto, sem esperar o "sim" (decisão de Mário Fernando, 26 e 27/10/2026); a confirmação dupla do NX Feed vale só para agendar A e B, o stories animado, o cancelamento do automático do Post A e a lixeira da véspera.

## Outra conta

Para outra pessoa da equipe ter a própria rotina (ex.: Elisângela), ela recebe o .zip e pede ao Claude dela para instalá-la seguindo o `INSTALAR.md`: ele publica o pacote num artefato da conta dela e cria a tarefa das 19h com o texto do `TAREFA.md` e o slug novo.