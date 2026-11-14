"""Recorta os Shorts de uma entrevista Comunhão (vertical 1080x1920).
Uso: python3 cortar_shorts.py video_original.mp4 shorts.json pasta_saida [legendas.srt]

shorts.json:
{"centro_x": 0.62,            # posição horizontal do rosto no vídeo (0 = esquerda, 1 = direita)
 "convidado": "Danielle Nazário",   # nome que aparece abaixo do título (1 linha)
 "shorts": [{"id": "s1", "inicio": "15:13", "fim": "16:12",
             "gancho": "A Bíblia que nunca me deixou"}, ...]}   # gancho: até 30 caracteres

O que cada Short recebe:
- Convidado preenchendo a área livre de 1260 px (y 344 a 1604), recorte centrado no rosto (centro_x).
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
        h, m, r = s.split(":"); s2, ms = r.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s2) + int(ms) / 1000
    def fmt(v):
        v = max(0, v); h = int(v // 3600); m = int(v % 3600 // 60); s = v % 60
        return f"{h:02}:{m:02}:{int(s):02},{int((s % 1) * 1000):03}"
    blocos, n = [], 1
    for b in re.split(r"\n\s*\n", open(srt, encoding="utf-8").read().strip()):
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
        vf = (f"color=c=black:s={W}x{H}:r=30[bg];"
              f"[0:v]crop=ih*{W}/{FG_H}:ih:max(0\\,min(iw-ih*{W}/{FG_H}\\,iw*{cx}-ih*{W}/{2*FG_H})):0,"
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
               "-i", str(ov), "-filter_complex", vf, "-map", last, "-map", "0:a?",
               "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
        print(f"{out}  ({fim - ini:.0f}s)")

if __name__ == "__main__":
    main()
