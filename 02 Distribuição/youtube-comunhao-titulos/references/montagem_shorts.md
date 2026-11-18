# Montagem dos Shorts no corte limpo — comandos ffmpeg

Comandos do Passo 13, item 7, da skill `youtube-comunhao-titulos`. As regras (selos, enquadramento, legenda, áreas livres) estão no SKILL.md; aqui ficam só os comandos. Rode a partir da pasta da skill, para o `fontsdir=assets/fonts` achar as fontes do kit.

## Comando base (estúdio, sem gráficos do canal no corte)

Gere as legendas do trecho em `.ass` (tempos por palavra do item 6) com `PlayResX: 1080`, `PlayResY: 1920` e este estilo:
```
Style: Legenda,Inter ExtraBold,96,&H00D8F6FF,&H00D8F6FF,&H00000000,&H64000000,0,-1,0,0,100,100,0,0,1,6,2,2,120,120,470,1
```
e monte o Short com a camada de selos (CX = `centro_x`; DURACAO = FIM − INICIO, em segundos; SELOS = `selos_[programa].png` ou `selos_so_marca.png`):
```
ffmpeg -ss INICIO -to FIM -i original.mp4 -i SELOS.png \
  -filter_complex "[0:v]crop=w='ih*9/16':h=ih:x='min(max(iw*CX-ih*9/32,0),iw-ih*9/16)':y=0,scale=1080:1920:flags=lanczos,setsar=1[v];[v][1:v]overlay=0:0,subtitles=legendas.ass:fontsdir=assets/fonts[out]" \
  -map "[out]" -map 0:a \
  -af "afade=t=in:d=0.15,afade=t=out:st=DURACAO-0.3:d=0.3" \
  -r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart short_01.mp4
```
Comando e estilo testados em 18/11/2026 (o `fontsdir` aponta para as fontes do kit). Os scripts antigos (`legado/cortar_shorts.py`) aplicam a moldura antiga: não use para montar.

## Variante com gráficos do canal

Estúdio com #revistacomunhao, @oficialcomunhao ou "inscreva-se" no corte. Troque só o `-filter_complex` do comando base; o resto é igual:
```
-filter_complex "[0:v]split[base][rec];[rec]crop=480:120:60:35,format=yuva420p,lumakey=threshold=0.92:tolerance=0.1:softness=0.08[letras];color=c=0xC6BDCC:s=480x120,format=yuva420p[parede];[parede][letras]overlay=shortest=1[remendo];[base][remendo]overlay=60:35,delogo=x=60:y=35:w=390:h=118,crop=w='ih*9/16':h=ih:x='min(max(iw*CX-ih*9/32,0),iw-ih*9/16)':y=0,scale=1080:1920:flags=lanczos,setsar=1[v];[v][1:v]overlay=0:0,subtitles=legendas.ass:fontsdir=assets/fonts[out]"
```
Os números do `crop` do remendo e do `overlay=60:35` são os da `marca_branca` (largura:altura:x:y); os do `delogo`, os do `delogo`. Para outro cenário, meça os dois num quadro do original.

## Variante webcam

Entrevista por webcam em 720p (CX = centro do rosto, de 0 a 1). Também troca só o `-filter_complex`:
```
-filter_complex "[0:v]crop=w='iw*446/1280':h='ih*520/720':x='max(0,min(iw-iw*446/1280,iw*CX-iw*223/1280))':y=0,split[r1][r2];[r2]scale=1080:1920,boxblur=30:3,eq=brightness=-0.15[fundo];[r1]scale=1080:-2:flags=lanczos[frente];[fundo][frente]overlay=0:'(H-h)/2',setsar=1[v];[v][1:v]overlay=0:0,subtitles=legendas.ass:fontsdir=assets/fonts[out]"
```
O vídeo fica entre y≈330 e y≈1590, com os selos sobre o fundo desfocado e a legenda sobre o vídeo. Se a webcam tiver o gráfico do canal no alto, junte o trecho `marca_branca` + `delogo` da variante anterior antes do `crop`, medido no quadro de 1280×720. As duas variantes foram testadas em 18/11/2026 com vídeo de teste (gera 1080×1920, H.264 + AAC, legenda na fonte do kit); falta conferir com um original de verdade.
