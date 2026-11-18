"""Recorta os Shorts de uma entrevista Comunhão (vertical 1080x1920).
Uso: python3 cortar_shorts.py video_original.mp4 shorts.json pasta_saida [legendas.srt]

shorts.json:
{"centro_x": 0.62,            # posição horizontal do rosto no vídeo (0 = esquerda, 1 = direita)
 "modo": "webcam",            # "webcam" (padrão, recorte do alto do quadro) ou "cheio" (estúdio)
 "delogo": [60, 35, 360, 120], # opcional: apaga gráfico do vídeo original nessa área (x, y, w, h)
 "convidado": "Danielle Nazário",   # nome que aparece abaixo do título (1 linha)
 "shorts": [{"id": "s1", "inicio": "15:13", "fim": "16:12",
             "gancho": "A Bíblia que nunca me deixou",
             "centro_x": 0.45}, ...]}   # gancho: até 30 caracteres; centro_x por Short é opcional

O que cada Short recebe:
- Convidado na área livre de 1260 px (y 344 a 1604), recorte centrado no rosto (centro_x).
  Modo webcam: alto do quadro ampliado, 90 px abaixo, fundo desfocado. Áudio com fade de 0,15 s / 0,3 s.
- Faixa laranja inclinada no topo com o título (Inter, corpo 22, entrelinha 22, tracking -35,
  até 30 caracteres em 2 linhas) e o nome (corpo 11, tracking -35) — ver gerar_visual_short.py.
- Rodapé vermelho com o logo Comunhão ▶ play.
- Legendas queimadas se for passado um .srt (tempos do vídeo inteiro; o script desloca para cada corte).
Exporta H.264 + AAC, pronto para subir como Short (privado).
"""
import json, subprocess, sys, pathlib, re, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
W, H = 1080, 1920
FG_Y, FG_H = 344, 1260   # área livre do vídeo: 1260 px (y 344 a 1604), largura total

def seg(t):
    p = [float(x) for x in str(t).split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))

def overlay(gancho, nome, out):
    """Moldura do Short no padrão Comunhão play (faixa laranja com título e nome, rodapé vermelho
    com logo), gerada por gerar_visual_short.py: PNG com janela transparente para o vídeo."""
    import gerar_visual_short as gv
    gv.render("moldura", {"titulo": gancho, "nome": nome}, str(out))

def srt_trecho(srt, ini, fim, out):
    """Copia do .srt só as falas do trecho, com tempos deslocados para começar em 0."""
    def ts(s):
        h, m, r = s.split(":"); s2, ms = r.replace(".", ",").split(",")
        return int(h) * 3600 + int(m) * 60 + int(s2) + int(ms) / 1000
    def fmt(v):
        v = max(0, v); h = int(v // 3600); m = int(v % 3600 // 60); s = v % 60
        return f"{h:02}:{m:02}:{int(s):02},{int((s % 1) * 1000):03}"
    blocos, n = [], 1
    for b in re.split(r"\n\s*\n", open(srt, encoding="utf-8-sig").read().replace("\r\n", "\n").strip()):
        ls = b.splitlines()
        if len(ls) < 3 or "-->" not in ls[1]:
            continue
        a, z = [ts(x.strip()) for x in ls[1].split("-->")]
        if z < ini or a > fim:
            continue
        blocos.append(f"{n}\n{fmt(a - ini)} --> {fmt(min(z, fim) - ini)}\n" + "\n".join(ls[2:]))
        n += 1
    open(out, "w", encoding="utf-8").write("\n\n".join(blocos) + "\n")
    return len(blocos)

def main():
    video, cfg_p, outdir = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    srt = sys.argv[4] if len(sys.argv) > 4 else None
    cfg = json.load(open(cfg_p)); outdir.mkdir(parents=True, exist_ok=True)
    cx = cfg.get("centro_x", 0.5)
    tmp = pathlib.Path(tempfile.mkdtemp())
    for s in cfg["shorts"]:
        ini, fim = seg(s["inicio"]), seg(s["fim"])
        nome = s.get("nome") or cfg.get("convidado")
        assert nome, "informe o nome do convidado (\"convidado\" no json ou \"nome\" no Short)"
        ov = tmp / f"{s['id']}_ov.png"; overlay(s["gancho"], nome, ov)
        # layout: vídeo do convidado preenchendo a área livre (1080x1260, recorte no rosto) a partir
        # de y=344; por cima, a moldura (faixa de título no topo, rodapé com logo). Fundo preto
        # nunca aparece: faixa e rodapé são opacos e cobrem o resto da tela.
        c = s.get("centro_x", cx)
        # "delogo": [x, y, w, h] no quadro original apaga selos/gráficos do vídeo (ex.: #revistacomunhao)
        dl = s.get("delogo", cfg.get("delogo"))
        # "marca_branca": [x, y, w, h, "0xRRGGBB"] troca os pixels brancos (texto/ícone do vídeo) pela cor
        # da parede nessa área; use junto com "delogo" para limpar a sombra onde não há cabelo/rosto.
        mb = s.get("marca_branca", cfg.get("marca_branca"))
        pre = ""
        if mb:
            pre = (f"[0:v]split[mbm][mbr];[mbr]crop={mb[2]}:{mb[3]}:{mb[0]}:{mb[1]},format=yuva420p,"
                   f"lumakey=threshold=0.92:tolerance=0.1:softness=0.08[mbk];"
                   f"color=c={mb[4]}:s={mb[2]}x{mb[3]},format=yuva420p[mbw];[mbw][mbk]overlay=shortest=1[mbp];"
                   f"[mbm][mbp]overlay={mb[0]}:{mb[1]}[src0];")
        base = "[src0]" if mb else "[0:v]"
        src = pre + (f"{base}delogo=x={dl[0]}:y={dl[1]}:w={dl[2]}:h={dl[3]}," if dl else (f"{base}null," if mb else "[0:v]"))
        if s.get("modo", cfg.get("modo", "webcam")) == "webcam":
            # entrevista por webcam: recorta só a parte de cima do quadro (446x520 em 1280x720,
            # proporcional em outras resoluções), deixando de fora a tarja de nome (embaixo à
            # esquerda) e o selo do canto. Vídeo 90 px abaixo do topo da área livre; fundo é uma
            # cópia desfocada e escurecida do mesmo recorte.
            crop = (f"crop=iw*446/1280:ih*520/720:"
                    f"max(0\\,min(iw-iw*446/1280\\,iw*{c}-iw*223/1280)):0")
            vf = (f"color=c=black:s={W}x{H}:r=30[bg];"
                  f"{src}{crop},scale={W}:{FG_H}:flags=lanczos,setsar=1,split[fg][fb];"
                  f"[fb]boxblur=30:3,eq=brightness=-0.15[blur];"
                  f"[bg][blur]overlay=0:{FG_Y}:shortest=1[b1];[b1][fg]overlay=0:{FG_Y+90}[v0];"
                  f"[v0][1:v]overlay=0:0[v1]")
        else:
            # "cheio": quadro inteiro na altura, recorte vertical centrado no rosto
            vf = (f"color=c=black:s={W}x{H}:r=30[bg];"
                  f"{src}crop=ih*{W}/{FG_H}:ih:max(0\\,min(iw-ih*{W}/{FG_H}\\,iw*{c}-ih*{W}/{2*FG_H})):0,"
                  f"scale={W}:{FG_H}:flags=lanczos,setsar=1[fg];"
                  f"[bg][fg]overlay=0:{FG_Y}:shortest=1[v0];[v0][1:v]overlay=0:0[v1]")
        last = "[v1]"
        st = tmp / f"{s['id']}.srt"
        if srt and srt_trecho(srt, ini, fim, st):
            style = ("FontName=Inter ExtraBold,FontSize=12,Bold=0,Italic=1,PrimaryColour=&H00DCF4FF,"
                     "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=69,Alignment=2")
            vf += f";[v1]subtitles='{st}':fontsdir='{ASSETS / 'fonts'}':force_style='{style}'[v2]"
            last = "[v2]"
        out = outdir / f"{s['id']}.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ini), "-to", str(fim), "-i", video,
               "-i", str(ov), "-filter_complex", vf, "-map", last, "-map", "0:a?", "-af", f"afade=t=in:d=0.15,afade=t=out:st={fim-ini-0.3:.2f}:d=0.3",
               "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
        print(f"{out}  ({fim - ini:.0f}s)")

if __name__ == "__main__":
    main()
