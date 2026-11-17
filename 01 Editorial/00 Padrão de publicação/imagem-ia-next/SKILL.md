---
name: "imagem-ia-next"
description: "Apoio da padrao-publicacao-next (9.1 e 9.2): imagem por IA na Krea e legenda-fato. Carregar só quando nenhuma foto real com direito de uso servir para a matéria."
---

# Imagem por IA — apoio do padrão Next

Estas são as seções 9.1 e 9.2 da skill `padrao-publicacao-next`, separadas em 17/11/2026 para economizar o plano (decisão do Mário Fernando): só são carregadas quando nenhuma foto real com direito de uso serviu, depois de seguir a ordem de busca e a conferência das seções 9 e 9.3 do padrão. Valem para todas as rotinas, como se estivessem no padrão.

### 9.1 Imagem por IA (último recurso; autorizada em 26/10/2026 para todas as rotinas)

Só quando nenhuma foto real com direito de uso servir:

- Krea: `mcp__Krea_AI__generate_image` (carregue com ToolSearch), modelo `krea/krea-2/large`, `aspect_ratio` 16:9, `resolution` 1K, `sync` = true.
- Prompt em inglês, com uma cena **genérica e ilustrativa** do tema, terminando com: "photorealistic editorial photo, natural light, no text, no logos, no recognizable faces".
- **Proibido gerar:** pessoa real ou identificável; rosto de personagem da matéria; criança em contexto sensível; marca, logotipo, fachada, produto ou coleção de empresa real; escudo, uniforme ou patrocinador de clube real; símbolo ou templo de denominação específica; lugar reconhecível como se fosse foto real; recriar o próprio fato (gol, ataque, acidente, discurso, evento noticiado) como se fosse foto; procedimento, remédio ou dose; animal em sofrimento.
- Olhe a imagem antes de gravar. Com defeito visível (mãos, rostos, objetos deformados, texto), gere de novo **uma** vez.
- Grave com `definir_imagem_destacada`: fonte "Imagem gerada por IA"; autor "Krea AI / ES Brasil" (só Comunhão: "Krea AI / Comunhão"); título curto com o assunto da matéria; **descrição = a legenda-fato (9.2)**; legenda (alt) com até 125 caracteres dizendo o que a ilustração mostra, terminando com "(imagem ilustrativa gerada por IA)".
- Se a Krea falhar (saldo ou erro), publique sem imagem e avise.
- Toda imagem de IA entra no resumo, na seção "Imagens de IA para validar", com a legenda-fato. É validação, não aprovação: não espere resposta.

### 9.2 Legenda-fato da imagem por IA (decisão do Mário Fernando, 26/10/2026)

A descrição é o texto que aparece embaixo da imagem no site, seguido do crédito "Foto: Imagem gerada por IA/Krea AI / …", que já avisa que é ilustração. Por isso ela **não descreve a imagem**: entrega ao leitor um dado a mais sobre o assunto da matéria.

1. **Assunto, não cena.** Fala do tema da matéria, nunca do que a ilustração mostra. Nada de "na imagem", "na foto", "ilustração de".
2. **Fato novo.** Não está no título, na linha fina nem no texto: dado, número, data, regra, histórico ou serviço. Antes de gravar, confira que os números e os termos-chave da frase não aparecem no texto.
3. **Conferido e atribuído.** Vem de fonte oficial aberta com WebFetch e leva a atribuição na frase ("segundo o IBGE", "de acordo com a Anvisa"). Nunca de memória, nunca inventado.
4. **Coerente.** Não contradiz o texto nem muda o foco da matéria.
5. **Uma frase de 100 a 220 caracteres**, informativa: sem pergunta, chamada, exclamação ou adjetivo de propaganda.
6. **Saúde e pet:** sem dose nem prescrição. **Política:** dado oficial e neutro.
7. **Sem fato novo** conferido depois de duas buscas extras: use o dado de serviço mais útil da própria matéria (data, local, horário, prazo, canal de atendimento) e marque "legenda sem fato novo" no resumo.

Exemplos (matéria sobre apreensão de lote falsificado de toxina botulínica):
- Errado (descreve a imagem): "Sala de clínica de estética vazia, com cadeira reclinável branca e janela com cortinas claras."
- Errado (repete a matéria): "Anvisa manda apreender novo lote falsificado de toxina botulínica."
- Certo (forma): "<fato que o texto não traz, com número ou data>, segundo <fonte oficial>." Por exemplo: "O Espírito Santo tem N estabelecimentos de estética licenciados pela Vigilância Sanitária, segundo a Sesa." O número e a fonte vêm sempre da apuração do dia.