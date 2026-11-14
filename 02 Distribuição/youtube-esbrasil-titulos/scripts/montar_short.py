"""Monta um Short 1080x1920 do canal Revista ES Brasil: vídeo na área livre + moldura por cima.
Uso: python3 montar_short.py video.mp4 INICIO FIM moldura.png saida.mp4 [centro_x=0.5] [legendas.srt]

  INICIO e FIM   tempos do trecho no vídeo original (MM:SS ou HH:MM:SS ou segundos)
  moldura.png    gerada por gerar_short_esbrasil.py moldura ... (1080x1920, com título e nome)
  centro_x       posição horizontal do rosto no vídeo (0 = esquerda, 1 = direita)
  legendas.srt   opcional; tempos do VÍDEO INTEIRO (o script desloca para o trecho)

Layout (medidas do design): o vídeo ocupa a área livre de 1080x1260, de y=352 a y=1612;
a moldura (faixa do título em cima, ES BRASIL play embaixo) vai por cima.
Legendas queimadas: Inter ExtraBold, ~80 px, brancas com contorno escuro, dentro da área do vídeo.
Saída: H.264 + AAC, 30 fps. Requer ffmpeg com libass.
"""
import pathlib, re, subprocess, sys, tempfile

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
W, H = 1080, 1920
AREA_Y, AREA_H = 352, 1260
RODAPE = H - (AREA_Y + AREA_H)        # 308 px

def area_da_moldura(path):
    """Lê a janela transparente da moldura (ES Brasil: y=352..1612; Café com Moqueca: y~413..1595, com borda inclinada)."""
    from PIL import Image
    a = Image.open(path).getchannel("A")
    rows = [y for y in range(a.height) if min(a.getpixel((x, y)) for x in (2, 540, 1077)) < 250]
    if not rows:
        return 352, 1260
    y0, y1 = rows[0] - 4, rows[-1] + 4
    y0 -= y0 % 2; h = (y1 - y0) + ((y1 - y0) % 2)
    return y0, h

def seg(t):
    p = [float(x) for x in str(t).split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))

def srt_trecho(srt, ini, fim, out):
    """Copia do .srt só as falas do trecho, com os tempos deslocados para começar em 0."""
    def ts(s):
        h, m, r = s.split(":"); s2, ms = r.replace(".", ",").split(",")
        return int(h) * 3600 + int(m) * 60 + int(s2) + int(ms) / 1000
    def fmt(v):
        v = max(0, v); h = int(v // 3600); m = int(v % 3600 // 60); s = v % 60
        return f"{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)):03}"
    blocos, n = [], 1
    for b in re.split(r"\n\s*\n", open(srt, encoding="utf-8").read().strip()):
        ls = b.splitlines()
        if len(ls) < 3 or "-->" not in ls[1]:
            continue
        a, z = [ts(x.strip()) for x in ls[1].split("-->")]
        if z < ini or a > fim:
            continue
        blocos.append(f"{n}\n{fmt(max(a, ini) - ini)} --> {fmt(min(z, fim) - ini)}\n" + "\n".join(ls[2:]))
        n += 1
    open(out, "w", encoding="utf-8").write("\n\n".join(blocos) + "\n")
    return len(blocos)

def main():
    video, ini, fim, moldura, saida = sys.argv[1], seg(sys.argv[2]), seg(sys.argv[3]), sys.argv[4], sys.argv[5]
    cx = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
    srt = sys.argv[7] if len(sys.argv) > 7 else None
    dur = fim - ini
    global AREA_Y, AREA_H, RODAPE
    AREA_Y, AREA_H = area_da_moldura(moldura)
    RODAPE = H - (AREA_Y + AREA_H)
    vf = (f"[0:v]scale=-2:{AREA_H}:flags=lanczos,"
          f"crop={W}:{AREA_H}:max(0\\,min(iw-{W}\\,iw*{cx}-{W // 2})):0,setsar=1[v];"
          f"color=c=black:s={W}x{H}:r=30:d={dur:.3f}[bg];[bg][v]overlay=0:{AREA_Y}:shortest=1[c0]")
    last = "[c0]"
    if srt:
        tmp = pathlib.Path(tempfile.mkdtemp()) / "trecho.srt"
        if srt_trecho(srt, ini, fim, tmp):
            # o filtro 'subtitles' usa 288 de altura de referência: 1 unidade = 1920/288 = 6,67 px
            estilo = (f"FontName=Inter ExtraBold,FontSize=12,Bold=0,PrimaryColour=&H00FFFFFF,OutlineColour=&H00201000,"
                      f"BorderStyle=1,Outline=1.6,Shadow=0,Alignment=2,MarginV={int((RODAPE + 60) / (H / 288))}")
            vf += f";{last}subtitles='{tmp}':fontsdir='{ASSETS / 'fonts'}':force_style='{estilo}'[c1]"
            last = "[c1]"
    vf += f";{last}[1:v]overlay=0:0[out]"
    fade = f"afade=t=in:st=0:d=0.15,afade=t=out:st={max(0, dur - 0.3):.3f}:d=0.3"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ini), "-to", str(fim), "-i", video, "-i", moldura,
           "-filter_complex", vf, "-map", "[out]", "-map", "0:a?", "-af", fade, "-r", "30",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{dur:.3f}", saida]
    subprocess.run(cmd, check=True)
    print(f"{saida}  ({dur:.0f}s)")

if __name__ == "__main__":
    main()
