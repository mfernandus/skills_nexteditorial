// Captura quadros 1080p de um vídeo do próprio canal, direto do player do YouTube no Chrome.
// Use quando o original ainda não foi baixado ou só para escolher a foto da capa.
// 1) Abra https://www.youtube.com/watch?v=ID no Chrome, espere ~4 s.
// 2) Rode este trecho (javascript_tool). Ele salva N quadros em Downloads como quadro_ID_PP.jpg
//    e, ao terminar, põe "CAPDONE" no início do título da aba.
// 3) Rode a verificação até o título começar com CAPDONE (cada quadro leva ~3 s; não espere tudo
//    numa chamada só, o navegador corta em ~45 s):
//    for(let i=0;i<40&&!document.title.startsWith('CAPDONE');i++)await new Promise(r=>setTimeout(r,1000));document.title
// Uma chamada por vídeo. Depois: mover para Downloads/<pasta>/, esperar ~50 s (o Mac cria
// hardlinks temporários em arquivos novos) e só então trazer para o ambiente de trabalho.
const N = 12, INI = 0.06, PASSO = 0.08;             // 12 quadros entre 6% e 94% do vídeo
const p = document.getElementById('movie_player'), v = document.querySelector('video');
v.muted = true; try { p.setPlaybackQualityRange('hd1080', 'hd1080'); } catch (e) {}
p.pauseVideo && p.pauseVideo();
(async () => {
  await new Promise(r => setTimeout(r, 1500));
  const id = new URL(location.href).searchParams.get('v');
  for (let k = 0; k < N; k++) {
    const f = INI + k * PASSO; v.currentTime = v.duration * f;
    await new Promise(r => v.addEventListener('seeked', r, { once: true }));
    await new Promise(r => setTimeout(r, 2200));      // tempo para carregar o quadro em 1080p
    const c = document.createElement('canvas'); c.width = v.videoWidth; c.height = v.videoHeight;
    c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
    const b = await new Promise(r => c.toBlob(r, 'image/jpeg', 0.95));
    const a = document.createElement('a'); a.href = URL.createObjectURL(b);
    a.download = 'quadro_' + id + '_' + String(Math.round(f * 100)).padStart(2, '0') + '.jpg';
    document.body.appendChild(a); a.click(); a.remove();
    await new Promise(r => setTimeout(r, 500));
  }
  document.title = 'CAPDONE ' + document.title;
})(); 'iniciado';
