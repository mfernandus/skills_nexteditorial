"""Recomprime Shorts para o envio pelo navegador (limite de 10 MB por arquivo).
Uso: python3 comprimir_envio.py pasta_dos_shorts [alvo_mb=9.2]
Grava as versões em pasta_dos_shorts/envio/ (H.264 2 passagens, 1080x1920, AAC 128k).
Taxa de vídeo = alvo_mb × 8 ÷ duração − 130 kbps. Guarde a versão cheia; suba a de envio/.
"""
import json, pathlib, subprocess, sys, tempfile
pasta = pathlib.Path(sys.argv[1]); alvo = float(sys.argv[2]) if len(sys.argv) > 2 else 9.2
(pasta / "envio").mkdir(exist_ok=True)
for f in sorted(pasta.glob("*.mp4")):
    dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "json", str(f)], capture_output=True, text=True).stdout)["format"]["duration"])
    kbps = max(800, int(alvo * 8192 / dur - 130))
    out = pasta / "envio" / f.name; log = str(pathlib.Path(tempfile.gettempdir()) / "pass2log")
    base = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(f), "-c:v", "libx264", "-b:v", f"{kbps}k",
            "-preset", "slow", "-pix_fmt", "yuv420p", "-passlogfile", log]
    subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", "/dev/null"], check=True)
    subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    print(f"{out}  {out.stat().st_size / 1e6:.1f} MB  ({kbps} kbps, {dur:.0f}s)")
