// Grava no mapas.nx.tv.br (Destinos ES) as fotos escolhidas no NX Fotos.
// Roda no console de uma aba do painel do mapas com sessão logada (nunca digitar senha).
// O CDN do NX Fotos não libera leitura direta pelo mapas (CORS), então:
//   1) nesta aba do mapas: instalar o ouvinte e abrir uma aba do CDN com window.open;
//   2) na aba do CDN: baixar cada foto (mesma origem) e mandar o arquivo para esta aba com postMessage;
//   3) nesta aba: tratar no canvas (receita da casa, só nas fotos cruas), subir e anexar ao local.
// Cada item do plano: [id_do_local, id_nxfotos, autoria, legenda, alt, k_do_tratamento, principal(1/0)]

// ---------- passo 1 (aba do mapas) ----------
window.__blobs = {};
window.addEventListener('message', e => {
  if (e.origin !== 'https://cdn.nxfotos.com.br') return;
  const d = e.data; if (d && d.key !== undefined && d.blob) window.__blobs[d.key] = d.blob;
});
window.__cdn = window.open('https://cdn.nxfotos.com.br/<qualquer foto>@w400.webp', '_blank');

// ---------- passo 2 (aba do CDN) ----------
// const lista = [[0, 'https://cdn.nxfotos.com.br/pub/...@w1600.webp'], ...];
// for (const [k, u] of lista) {
//   const r = await fetch(u.replace('https://cdn.nxfotos.com.br', ''));
//   window.opener.postMessage({key: k, blob: await r.blob()}, 'https://mapas.nx.tv.br');
// }

// ---------- passo 3 (aba do mapas) ----------
window.api = async function api(path, {method = 'GET', body, form} = {}) {
  if (method !== 'GET' && !window.__csrf) { await fetch('/api/csrf-cookie', {credentials: 'include'}); window.__csrf = true; }
  const xsrf = decodeURIComponent((document.cookie.match(/XSRF-TOKEN=([^;]+)/) || [])[1] || '');
  const headers = {Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest', ...(xsrf ? {'X-XSRF-TOKEN': xsrf} : {})};
  if (!form) headers['Content-Type'] = 'application/json';
  const r = await fetch('/api' + path, {method, credentials: 'include', headers, body: form ? form : (body ? JSON.stringify(body) : undefined)});
  if (r.status === 429) { await new Promise(z => setTimeout(z, (+(r.headers.get('retry-after') || 30)) * 1000 + 500)); return api(path, {method, body, form}); }
  const j = await r.json().catch(() => null);
  if (!r.ok) throw new Error(r.status + ' ' + JSON.stringify(j).slice(0, 300));
  return j;
};

// Receita de tratamento da casa (11/11/2026): k = 0 (foto já viva, não mexe), 0,6 ou 0,8 (foto crua).
window.tratar = async function (blob, k) {
  const bmp = await createImageBitmap(blob);
  const c = document.createElement('canvas'); c.width = bmp.width; c.height = bmp.height;
  const x = c.getContext('2d'); x.drawImage(bmp, 0, 0);
  if (k > 0) {
    const im = x.getImageData(0, 0, c.width, c.height), d = im.data;
    const ct = 1 + 0.09 * k, gR = 1 + 0.04 * k, gG = 1 + 0.022 * k, gB = 1 - 0.012 * k, gam = 1 - 0.05 * k;
    for (let i = 0; i < d.length; i += 4) {
      let r = d[i] / 255, g = d[i + 1] / 255, b = d[i + 2] / 255;
      r = (r - 0.5) * ct + 0.5; g = (g - 0.5) * ct + 0.5; b = (b - 0.5) * ct + 0.5;      // contraste
      const mx = Math.max(r, g, b), mn = Math.min(r, g, b), s = mx > 0 ? (mx - mn) / mx : 0, m = (r + g + b) / 3;
      const v = 1 + 0.55 * k * (1 - s); r = m + (r - m) * v; g = m + (g - m) * v; b = m + (b - m) * v;  // vivacidade
      r *= gR; g *= gG; b *= gB;                                                       // mais quente e cítrica
      const dd = b - r; if (dd > 0) { g += 0.05 * k * dd; b -= 0.01 * k * dd; }        // azuis puxando para o turquesa
      r = Math.pow(Math.min(Math.max(r, 0), 1), gam); g = Math.pow(Math.min(Math.max(g, 0), 1), gam); b = Math.pow(Math.min(Math.max(b, 0), 1), gam);
      d[i] = r * 255; d[i + 1] = g * 255; d[i + 2] = b * 255;
    }
    x.putImageData(im, 0, 0);
  }
  const out = await new Promise(z => c.toBlob(z, 'image/jpeg', 0.9));
  return {out, w: c.width, h: c.height};
};

window.gravar = async function (idx) {
  const [tid, pid, autoria, legenda, alt, k, main] = window.__plano[idx];
  const blob = window.__blobs[idx]; if (!blob) throw new Error('sem arquivo ' + idx);
  const {out, w, h} = await tratar(blob, k);
  const fd = new FormData(); fd.append('image', out, 'nxfotos-' + pid + '.jpg');
  const up = await api('/upload-image', {method: 'POST', form: fd});
  const url = up.url || (up.data && (up.data.url || up.data.path)) || up.path;
  const img = await api('/mapa/' + tid + '/images', {method: 'POST', body: {
    url, source: 'upload', autoria, legenda: legenda.split('. ')[0], alt_text: alt,
    is_main: false, file_name: 'nxfotos-' + pid + '.jpg', width: w, height: h}});
  const imgId = (img.data && img.data.id) || img.id;
  if (main && imgId) await api('/mapa/' + tid + '/images/' + imgId + '/set-main', {method: 'POST'});
  return {idx, tid, imgId, url, k, principal: !!main};
};

// window.__plano = [...]  (gerado pelo selecionar.py + escolha visual)
// window.__res = {}; window.__erros = {};
// for (let i = 0; i < __plano.length; i++) { try { __res[i] = await gravar(i); } catch (e) { __erros[i] = e.message; } await new Promise(z => setTimeout(z, 1500)); }
