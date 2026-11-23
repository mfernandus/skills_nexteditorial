---
name: "formula-1"
description: "Fórmula 1 na ES Brasil em todo fim de semana de GP (sexta a domingo, 7h20, 13h20 e 19h20): ficha do GP refeita toda semana nas fontes oficiais, volume reduzido e fotos oficiais. Substitui a f1-gp-eua-2026."
---

# Fórmula 1 — ES Brasil

Rotina de Fórmula 1 do site da **ES Brasil** (portal 1 no NX Feed) em todo fim de semana de Grande Prêmio. Substitui a skill temporária `f1-gp-eua-2026` (GP dos EUA, 22 a 25/10/2026). Responda em português do Brasil; escreva **ES Brasil** em negrito. Execução automática: não faça perguntas; na dúvida, a decisão mais conservadora, registrada no resumo.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, pautas proibidas (2.1) e matéria agendada (2.2), NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem e avisos. Se ela não carregar, não publique nada e avise. Aqui fica só o que é da F1.

## 1. Atualização semanal (ficha do GP)

A skill não guarda calendário nem classificação: tudo é refeito **toda semana** nas fontes oficiais, porque muda de um GP para o outro.

- **Primeira execução da semana de GP** (sexta, 7h20, ou a primeira que rodar no fim de semana): monte a ficha do GP a partir de formula1.com (calendário e horários da temporada atual) e fia.com:
  - nome do GP, circuito, cidade e país;
  - se tem sprint;
  - horário de cada sessão em Brasília (TL, sprint, classificação, corrida), convertido e conferido no calendário;
  - classificação do Mundial de Pilotos (top 5 e Gabriel Bortoleto) e de Construtores (top 3 e a Audi), com pontos;
  - situação da briga pelo título (o que cada um precisa) quando o campeonato estiver na reta final;
  - o que mudou desde o GP anterior (punições, troca de piloto, regulamento em vigor).
- Guarde a ficha no resumo da primeira execução ("Ficha do GP") e use-a no fim de semana inteiro. Classificação do campeonato e resultado de sessão são **sempre conferidos de novo na hora** de escrever, na fonte oficial.
- **Não tem GP neste fim de semana** (calendário oficial): responda só "Sem GP neste fim de semana" e pare, sem notificação.

## 2. Volume reduzido (decisão do Mário Fernando, 27/10/2026)

- No máximo **1 matéria por execução**.
- **Teto do fim de semana:** 3 matérias de F1 na **ES Brasil** (4 em fim de semana com sprint), contando todas as matérias de F1 da casa desde sexta 00h (`listar_materias` portal=1, estado publicado, categoria 21861, data_de = sexta do fim de semana), inclusive as da equipe e de outras rotinas.
- O que entra, nesta ordem: (a) resultado da corrida (sempre); (b) classificação e grid; (c) resultado da sprint, só em fim de semana com sprint; (d) fato muito relevante: título decidido, brasileiro (Gabriel Bortoleto) no pódio ou na pole, acidente grave, punição que muda o resultado. Repercussão e falas entram como atualização da matéria do resultado, não como matéria nova.
- **Peça do Mundial** (decisão do Mário Fernando, 23/11/2026). A matéria do resultado da corrida, e a da sprint quando houver, leva o Mundial de Pilotos atualizado numa peça do NXtab: `c-barras`, marca `esb`, rótulo com posição e piloto juntos ("1º Nome do Piloto"), top 5 e Gabriel Bortoleto em destaque, com pontos. Quando couber, uma segunda peça com o Mundial de Construtores (top 3 e a Audi). Os pontos são relidos em formula1.com depois do resultado oficial e passam pela conferência reforçada da seção 12 da `dados-e-graficos-next`. A peça vai dentro da matéria do resultado: não é "matéria de números" e não conta no teto.
- Não entra: boletim de treino livre, guia da pista, cenários, números, histórico, clima, pneus, bastidor ou pauta para preencher. Sexta-feira só publica com fato muito relevante.
- Execução sem sessão encerrada nem fato muito relevante desde a anterior: responda "Sem movimentação nova na F1" e pare, sem notificação.
- Nos dias do fim de semana de GP, a F1 é só desta rotina: a rotina de esporte (`esporte-noturno-next`) não escreve sobre F1 de sexta a domingo.

## 3. Linha editorial

A briga pelo título e os líderes; Gabriel Bortoleto (posição, comparação com o companheiro de equipe, fala oficial); no GP de São Paulo (Interlagos), o ângulo brasileiro com mais peso, dentro do mesmo teto.

## 4. Fontes

NX Feed `feed_nacional` primeiro (Estadão Conteúdo – Esportes e Agência Brasil, aproveitáveis com crédito no rodapé); oficiais (formula1.com, fia.com, comunicados das equipes); apoio só para conferir (Grande Prêmio, ge, Motorsport.com, The Race), sem crédito nem link. Resultado de sessão: sempre o oficial da F1/FIA mais uma fonte. Texto com palavras próprias.

## 5. Fotos

- Prefira serviço de imprensa oficial com crédito: Audi Media Center (arquivo `_web_1440`; fonte "Audi Media Center", autor "Audi AG/Divulgação"), site da equipe Audi, Mercedes, Ferrari Media Centre, Red Bull Content Pool, McLaren Media Centre, Pirelli, FIA, organizador do GP, perfis oficiais no X ("Divulgação/<perfil>"); depois os acervos do NX Feed.
- Proibido: Reuters, AFP, AP, Getty, Estadão/Zimel, foto de jornal ou portal, print de transmissão.
- Foto de outro GP: "(foto de arquivo)" na descrição. Varie: não repita a imagem destacada da matéria anterior.
- Imagem por IA só em último caso, pela regra da skill-base, nunca recriando carro, piloto ou lance.
- A matéria do **resultado da corrida** leva galeria de 4 a 8 fotos no fim, antes do rodapé, sob `<h3>Galeria: ...</h3>`, uma `<figure class="wp-block-image size-large"><img src="URL" alt="o que a foto mostra"/><figcaption>Legenda curta. Foto: Crédito</figcaption></figure>` por foto. Sem fotos liberadas suficientes, publique sem galeria e diga no resumo.

## 6. Formato

Chapéu "FÓRMULA 1"; autor "Redação"; categoria **ES Brasil** 21861 (nunca 63); 400 a 700 palavras; intertítulos `<h3>`; top 10 em `<ol>` no resultado e no grid. Só a **ES Brasil**, salvo título mundial decidido (aí também na Comunhão, categoria 116634). **Destaques:** esta rotina nunca marca nem tira Destaques; quem decide é a rotina de Destaques (o fim de semana é janela de esporte). Ao editar uma matéria que já está em Destaques, mantenha a categoria.

## 7. Duplicidade e atualização

Buscas "F1", "Fórmula 1", o nome do GP, "Bortoleto" e o piloto principal, data_de = sexta do fim de semana, todos os estados. Fato já publicado: não publique; com dado novo, atualize a matéria existente (`editar_materia` com `<p><strong>Atualização (DD/MM, HHhMM):</strong> o que mudou.</p>` no topo → `atualizar_no_wordpress`).

## 8. Resumo

`SendUserMessage`, curto, para celular, título "F1 – <GP> – <dia> <hora>": publicada (título, link no ar, crédito da foto), quantas matérias de F1 a casa já tem no fim de semana e quanto falta do teto, próxima sessão (horário de Brasília). Na primeira execução da semana, acrescente a "Ficha do GP". Notificação só com matéria nova ou problema. Na matéria do resultado, diga se a peça do Mundial entrou ou o motivo de ter ficado fora.

## Modelo recomendado
- Nível: Sonnet
- Nota: 6/12 (raciocínio 1, fontes 1, texto 1, números 1, fluxo 1, risco 1)
- Motivo: fontes oficiais fixas, teto e pauta definidos por regra; publica direto, o que barra o Haiku.
- Teste: não testado, primeira execução monitorada no próximo fim de semana de GP.
- Subir para Opus se: resultado ou pontuação errados forem ao ar por falha de leitura.