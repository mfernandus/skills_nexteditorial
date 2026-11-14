---
name: "estilo-diario-esbrasil"
description: "Rodada diária de Estilo da ES Brasil: 1 matéria por subcategoria (7 por dia), com apuração, SEO e imagem, publicada direto. Única rotina de Estilo; use quando pedirem a rodada."
---

# Rodada diária de Estilo — ES Brasil

Objetivo: manter vivas as subcategorias de **Vida Capixaba › Estilo** no site da **ES Brasil**, com **uma matéria por dia para cada subcategoria** (7 por rodada). Roda uma vez por dia, de manhã. **É a única rotina que produz Estilo**: o turno noturno não mexe nessas subcategorias.

**Antes de tudo, carregue a skill `padrao-publicacao-next`** e siga-a: publicação direta, cuidados do NX Feed, duplicidade, fontes, direitos autorais, SEO, imagem (inclusive por IA), avisos e economia do plano (seção 11) estão lá. Aqui fica só o que é de Estilo. Se a skill-base não estiver disponível, não publique nada: deixe as matérias em rascunho e avise que a skill-base faltou.

## Subcategorias (portal ES Brasil = 1; categoria-mãe Estilo = 3971)

| Subcategoria | id | slug | Linha editorial |
|---|---|---|---|
| Casa e decoração | 42112 | casa-e-decoracao | arquitetura, design de interiores, mostras (CASACOR ES), cores e materiais do ano, escritórios e profissionais capixabas |
| Em Casa | 14737 | em-casa | vida doméstica: economia na casa (energia, água, gás), organização, plantas, cozinha, casa inteligente, manutenção |
| Esportes Vip | 42111 | esportes-vip | esportes de alto padrão do público AB: pesca oceânica, vela, golfe, tênis, beach tennis, padel, hipismo, kitesurf, triathlon, corrida, ciclismo. NUNCA futebol, F1 ou vôlei (são da rotina de esporte) |
| Essas Mulheres | 103 | essas-mulheres | perfis e conquistas de mulheres capixabas: empreendedoras, lideranças, profissionais, prêmios |
| Meu pet | 42110 | meu-pet | saúde e comportamento animal, campanhas veterinárias, políticas públicas para animais no ES, eventos pet |
| Moda e Vestuário | 87 | moda-e-vestuario | tendências, semanas de moda, moda capixaba (ES Fashion, polos de confecção), consultoria de imagem |
| Saúde e estética | 42109 | saude-e-estetica | dermatologia, cabelo, skincare, procedimentos estéticos, bem-estar, campanhas de saúde com ângulo de autoestima |

Grave sempre `[{portal: "ES Brasil", ids: [<id da sub>, 3971]}]`. Nunca Destaques.

## Fluxo da rodada

1. **Lista de tarefas** com as 7 subcategorias e a conferência final.
2. **O que já saiu** em cada subcategoria: `listar_materias` (portal=1, categoria=<id>, últimos 30 dias, formato compacto), uma listagem por subcategoria, uma vez na rodada. Para o tema escolhido, busque também `site:esbrasil.com.br <tema>`: não repita assunto publicado nos últimos 12 meses sem fato novo.
3. **Pauta**, com WebSearch (modo standard) usando a data de hoje. Prioridade: (a) gancho capixaba atual; (b) gancho de calendário da semana (evento, campanha, data comemorativa); (c) serviço com dado novo. Abra a fonte com WebFetch antes de escrever; prefira fonte primária (órgão oficial, release, site do evento).
4. **Redigir** no padrão abaixo.
5. **Imagem destacada**, pela skill-base, com esta ordem de busca: `buscar_imagens` NX Fotos (termo) → editoriais (termo) → recomendadas (materia_id) → divulgação oficial com crédito → imagem por IA. Estilo não fica sem foto.
6. **Criar** com `criar_materia` (autor "Redação", categorias acima) e ajustar a nota SEO pela skill-base.
7. **Publicar tudo**: imediatamente antes de cada publicação, faça a reconferência leve da skill-base (seção 4): `listar_publicacoes` do portal 1 desde a primeira conferência e `listar_materias` com `busca` pelo tema (todos os estados); se a casa publicou o mesmo assunto nesse meio-tempo, troque a pauta. As listagens por subcategoria e o WebSearch do passo 2 não se repetem. Publique no portal ES Brasil: a primeira matéria sai "agora" e as seguintes são agendadas de 15 em 15 minutos.
8. **Resumo** (passo final).

## Padrão da matéria de Estilo

- **Tamanho:** 450 a 650 palavras. **8 a 10 tags.**
- Intertítulos em `<h4>`; listas em `<ul>`; destaques em `<strong>`.
- Depois do 2º parágrafo: `[sc name="leia_mais" categoria="<slug>" num_posts="2" ][/sc]`.
- Ângulo capixaba sempre que existir (personagem, serviço, dado ou evento no ES).
- Evento ainda não confirmado aparece como "costuma acontecer" ou "ainda a confirmar".
- O resto do padrão (título, lide, link, rodapé, SEO) está na skill-base.

## Resumo

Avisos da skill-base, com uma diferença: o resumo e a notificação de Estilo saem **em toda rodada**. Título do resumo: **"Estilo ES Brasil · DD/MM"**.

No resumo: tabela com subcategoria, título, link no ar, nota SEO, imagem (real / ilustrativa / IA / sem imagem) e observações; fontes usadas; erros técnicos.