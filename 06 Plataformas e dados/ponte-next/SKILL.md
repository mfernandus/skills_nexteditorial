---
name: ponte-next
description: "Inventaria projetos corporativos, consulta o Manifesto Canônico da Ponte Next no Google Drive, consolida decisões e conclusões com fontes e prepara sincronização auditável entre Claude e ChatGPT. Use quando o usuário pedir Ponte Next, sincronização de projetos, memória compartilhada, estado atual, inventário, auditoria de conhecimentos ou cadastro de projeto novo."
---

# Ponte Next — memória corporativa compartilhada

## Missão
Permitir que o usuário encontre conhecimento corporativo autorizado, decisões, conclusões, documentos e pendências em Claude e ChatGPT usando o Google Drive como repositório canônico. **Nunca afirmar que conversas ou projetos nativos estão sincronizados automaticamente sem integração e teste comprovados.**

## Fontes canônicas
- Manifesto vivo: https://drive.google.com/file/d/14bDOiiKgTi4I5e7w0h4aRldExD4uvp3c/view
- Pasta: https://drive.google.com/drive/folders/1sU_MusGgt9vx3LGQOm1wNwVlFOBEql6U
- Planilha: https://docs.google.com/spreadsheets/d/1NDdB-PG_X0dsKAkWtPIjnnMol4IWdFT5KsCIfpRBLY4/edit
- Abas: Controle, Projetos, Alterações
- Pareamento de projetos (fonte da verdade do cadastro, editável pelo Claude): https://docs.google.com/spreadsheets/d/1046G8WbOgQlKog0aLQrzL-tsYumO1kDvN0Fx_cyviWY/edit — abas Projetos (um projeto nativo por linha, com ID da ponte, documento oficial e situação) e Execuções (log da rotina).
- Mapa geral, anexado em todo projeto nativo: "00 — Mapa de projetos | ChatGPT e Claude" (id 1sgY-QkYUerlurXhsyn0eu9ar9W6GaLvvM_Kp_QoFM_w).
- O manifesto JSON e a planilha "Índice e Auditoria" pertencem ao script de monitoramento: ler, não editar.
- Cópia do manifesto na Skill: `references/manifesto-63-snapshot.json` — **referência histórica, não substitui a fonte viva**.

## Primeiro uso: inventário do Claude
1. Verifique se há conexão autorizada ao Google Drive e ferramentas para listar projetos do Claude. Declare as capacidades efetivamente disponíveis.
2. Leia o manifesto vivo e a planilha. Identifique 63 documentos cadastrados, 22 monitorados pelo script anterior e 41 adicionais (conforme baseline; confirme estado atual antes de reportar).
3. Liste projetos do Claude **somente se ferramentas autorizadas permitirem enumerá-los**. Não presuma que o assistente consegue ver todos os projetos da conta. Se não puder, peça ao usuário uma exportação/lista ou acesso suportado.
4. Cruze por identificador, título, área e conteúdo. Classifique: correspondência confirmada, provável, não encontrado, não acessível, fora do escopo.
5. Não tratar documentos como prova de que o projeto nativo do Claude existe ou está atualizado.
6. Produza relatório de cobertura e lacunas. Nunca declarar 100% sem prova de cobertura integral.

## Em cada trabalho com projeto
1. Identifique projeto e documento canônico pelo manifesto; confira ID/URL no Drive.
2. Leia a versão atual e busque fontes adicionais autorizadas quando necessárias.
3. Diferencie rigorosamente: **FATO**, **DECISÃO CONFIRMADA**, **CONCLUSÃO FUNDAMENTADA**, **HIPÓTESE**, **PROPOSTA**, **PENDÊNCIA** e **CONFLITO**.
4. Preserve a redação original, datas, valores e fontes; não transforme recomendações do assistente em decisões do usuário.
5. Gere síntese segundo `templates/estado-atual.md`, citando links e versões.
6. Se o usuário autorizar publicação, confira permissões e versão atual antes de escrever. Nunca sobrescreva conteúdo anterior; acrescente registro datado ou nova versão, preserve histórico. Em caso de conflito, peça resolução.
7. Se a escrita não estiver disponível, apresente o conteúdo pronto para publicação e informe que **não foi sincronizado**.

## Cadastro de projeto novo
Vale quando o usuário pedir ("Ponte Next: cadastrar o projeto X") e na tarefa agendada "Ponte Next: cadastro diário de projetos novos" (dias úteis, 16h50, modo cadastrar e avisar).
1. Liste os projetos do Claude (claude.ai/projects) e do ChatGPT (barra lateral: Fixados com ícone de pasta e Projetos, até o fim de "Mostrar mais"). Compare com a aba Projetos do pareamento, primeiro pelo link e depois pelo nome sem diferença de maiúsculas, acentos e espaços.
2. Projeto pessoal fica fora: nome que comece com "Minha", "Meu", "Minhas" ou "Meus", ou que tenha "pessoal". Não abra, não cadastre e não escreva o nome dele em lugar nenhum.
3. Se já houver a mesma frente na outra plataforma, reuse o ID da ponte e o documento oficial. Na dúvida, crie registro novo e anote "possível correspondência com <ID>".
4. Registro novo na pasta da ponte (1sU_MusGgt9vx3LGQOm1wNwVlFOBEql6U), título "PONTE | <nome> | Registro canônico", com identificador, projeto nativo e link, referência, diretriz de registro e histórico. Confira antes se o título já existe.
5. Anexe o registro e o mapa geral no projeto nativo: no Claude, Contexto → Adicionar → Google Drive (deve aparecer "Fonte sincronizada"); no ChatGPT, Fontes → Adicionar fontes → Google Drive (deve aparecer "Última sincronização"). Não crie projeto na outra plataforma.
6. Acrescente a linha no pareamento e registre a execução na aba Execuções. Nunca apague, renomeie, mova ou arquive projeto, arquivo ou linha.
7. A fonte do Drive no ChatGPT não atualiza na hora: em 21/11/2026, três minutos depois de uma gravação, ela ainda estava na versão anterior e só atualizou com "Sincronizar novamente". Antes de trabalhar ou testar pelo ChatGPT, confira a data de "Última sincronização".

## Captura de conversas
- Não alegue acesso a chats nativos do Claude/ChatGPT, históricos, mensagens ou memórias pessoais sem exportação ou API autorizada.
- Em conversas em que esta Skill for acionada, é possível **preparar** registro do que estiver acessível no contexto atual. A publicação no Drive depende de permissão e ferramenta real.
- Para captura contínua de todos os projetos e chats, requer-se integração externa autorizada, mecanismos de exportação e testes; a Skill por si só não é um serviço de background.
- Dois projetos pessoais estão excluídos do repositório corporativo. Não inventarie, exporte ou publique dados pessoais desses projetos.

## Sincronização e auditoria
- Fonte de verdade: documentos do Drive, com IDs estáveis e metadados de origem.
- Eventos devem conter: event_id, project_id, origem, documento_id, versao_anterior, versao_nova, timestamp_BRT, tipo, status, link, evidência.
- Deduplicar por documento+versão/evento; não criar loop de atualizações entre sistemas.
- Mudança de `modified_time` significa apenas mudança de metadados; não alegar alteração textual sem diff.
- Não criar nem modificar arquivos em tarefas **somente de monitoramento**.
- Auditoria anterior >45 minutos: reportar somente se confirmado. O script antigo monitora 22; a versão 63 preparada não deve ser tratada como instalada.
- Se for autorizada uma sincronização de escrita, usar operação idempotente, backup/versão, verificação pós-escrita e log.
- Não declarar sincronização bidirecional até testar publicação e leitura de nova versão nos dois sentidos.

## Resposta-padrão
Entregue: (a) cobertura verificada; (b) conclusões e decisões com fontes; (c) lacunas; (d) próximo passo. Seja conciso e não use emojis.

## Testes de aceitação
- Inventário real do Claude comparado ao manifesto.
- Cada projeto corporativo possui documento canônico e fonte identificável.
- Uma decisão nova é registrada com evidência e encontrada no outro ambiente.
- Uma atualização originada no outro ambiente é recuperada no Claude.
- Conflitos, falhas e duplicações são detectados e reportados.
- Exclusões pessoais são respeitadas.