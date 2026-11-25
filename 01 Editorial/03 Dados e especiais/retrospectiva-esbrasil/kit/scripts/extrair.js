// Extrai a geometria e o conteúdo das páginas aprovadas (article.page) para o exportador IDML.
// Roda dentro do Chromium (Playwright). Devolve JSON com, por página, a lista de itens na ordem de pintura.
(() => {
  const PAGES = [...document.querySelectorAll('article.page')];
  const isNone = c => !c || c === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(c);
  const px = v => parseFloat(v) || 0;
  const vis = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden' && px(cs.opacity) > 0.01; };

  // 1. Pseudo-elementos com conteúdo viram elementos reais (barras, pontos, filetes).
  const style = document.createElement('style');
  style.textContent = '.__nops::before,.__nops::after{content:none!important;display:none!important}';
  document.head.appendChild(style);
  for (const page of PAGES) {
    for (const el of [page, ...page.querySelectorAll('*')]) {
      if (el.closest('svg')) continue;
      const add = [];
      for (const pse of ['::before', '::after']) {
        const cs = getComputedStyle(el, pse);
        if (!cs || cs.content === 'none' || cs.content === 'normal' || cs.display === 'none') continue;
        const n = document.createElement('i');
        n.className = '__pseudo';
        for (const prop of cs) n.style.setProperty(prop, cs.getPropertyValue(prop));
        const m = cs.content.match(/^"(.*)"$/);
        n.textContent = m ? m[1] : '';
        add.push([pse, n]);
      }
      if (add.length) {
        el.classList.add('__nops');
        for (const [pse, n] of add) pse === '::before' ? el.prepend(n) : el.append(n);
      }
    }
  }

  // 2. Texto solto dentro de caixas de layout ganha um span próprio.
  const layoutDisplay = d => /^(flex|grid|inline-flex|inline-grid)$/.test(d);
  for (const page of PAGES) {
    for (const el of [page, ...page.querySelectorAll('*')]) {
      if (el.closest('svg') || el.closest('table') || el.classList.contains('flow') || el.closest('.flow')) continue;
      const kids = [...el.childNodes];
      const hasEl = kids.some(k => k.nodeType === 1);
      const loose = kids.filter(k => k.nodeType === 3 && k.textContent.trim());
      if (!hasEl || !loose.length) continue;
      const cs = getComputedStyle(el);
      const blocky = kids.some(k => k.nodeType === 1 && !/^inline/.test(getComputedStyle(k).display));
      if (layoutDisplay(cs.display) || blocky) {
        for (const t of loose) { const s = document.createElement('span'); s.className = '__anon'; t.replaceWith(s); s.appendChild(t); }
      }
    }
  }

  const hasBox = cs => !isNone(cs.backgroundColor) || ['Top', 'Right', 'Bottom', 'Left'].some(s => px(cs['border' + s + 'Width']) > 0 && !isNone(cs['border' + s + 'Color']) && cs['border' + s + 'Style'] !== 'none');
  const isLayoutBox = el => {
    if (/^(IMG|svg|TABLE|CANVAS|VIDEO)$/.test(el.tagName)) return true;
    const cs = getComputedStyle(el);
    if (cs.position === 'absolute' || cs.position === 'fixed' || cs.float !== 'none') return true;
    if (hasBox(cs)) return true;
    if (/^(flex|grid|inline-flex|inline-grid|inline-block|table)$/.test(cs.display)) return true;
    return false;
  };
  const isTextBlock = el => {
    if (!el.textContent.trim()) return false;
    const cs = getComputedStyle(el);
    if (layoutDisplay(cs.display) && [...el.children].filter(vis).length > 1) return false;
    for (const d of el.querySelectorAll('*')) if (vis(d) && isLayoutBox(d)) return false;
    return true;
  };

  const rectOf = (el, origin) => { const r = el.getBoundingClientRect(); return { x: r.left - origin.left, y: r.top - origin.top, w: r.width, h: r.height }; };
  const clipRect = (el, page) => {
    const pr = page.getBoundingClientRect();
    let r = el.getBoundingClientRect(); let L = r.left, T = r.top, R = r.right, B = r.bottom;
    for (let a = el.parentElement; a && a !== page.parentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.overflow !== 'visible' || a === page) {
        const q = a.getBoundingClientRect();
        L = Math.max(L, q.left); T = Math.max(T, q.top); R = Math.min(R, q.right); B = Math.min(B, q.bottom);
      }
    }
    return { x: L - pr.left, y: T - pr.top, w: Math.max(0, R - L), h: Math.max(0, B - T) };
  };
  const radiusOf = el => {
    let r = px(getComputedStyle(el).borderTopLeftRadius);
    const p = el.parentElement;
    if (p && getComputedStyle(p).overflow !== 'visible') {
      const a = el.getBoundingClientRect(), b = p.getBoundingClientRect();
      if (Math.abs(a.width - b.width) < 2 && Math.abs(a.height - b.height) < 2) r = Math.max(r, px(getComputedStyle(p).borderTopLeftRadius));
    }
    return r;
  };
  const fontOf = cs => ({
    family: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
    weight: parseInt(cs.fontWeight) || 400, italic: cs.fontStyle === 'italic',
    size: px(cs.fontSize), color: cs.color, ls: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
    lh: cs.lineHeight === 'normal' ? null : px(cs.lineHeight)
  });
  const roleOf = el => {
    const tests = [
      ['h1', 'Título'], ['.fina', 'Linha fina'], ['.by', 'Assinatura'], ['.tag, .tag *', 'Cartola'],
      ['.legenda', 'Legenda'], ['.ph .leg', 'Legenda sobre foto'], ['.cr', 'Crédito da foto'], ['.qr span', 'QR Code'],
      ['.busca b', 'Prova · Buscar original (rótulo)'], ['.busca, .busca *', 'Prova · Buscar original'],
      ['.esn-top h3', 'Box · título'], ['.esn-top span, .esn-top div', 'Box · subtítulo'], ['.esn .n i', 'Box · etiqueta'],
      ['.esn .n b', 'Box · número'], ['.esn .n span', 'Box · texto'], ['.esn-qr, .esn-qr *', 'Box · QR Code'], ['.esn-src', 'Box · fontes'],
      ['.tempo figcaption, .tempo figcaption *', 'Linha do tempo · título'], ['.tempo .e', 'Linha do tempo · escopo'],
      ['.tempo .m', 'Linha do tempo · mês'], ['.tempo li b', 'Linha do tempo · marco'], ['.tempo .x', 'Linha do tempo · detalhe'],
      ['.tempo .src', 'Linha do tempo · fontes'],
      ['.kpis b', 'Gráfico · número'], ['.kpis span, .kpis > div', 'Gráfico · rótulo'],
      ['.tabela h3', 'Tabela · título'], ['.panel h3', 'Gráfico · título'], ['.panel figcaption p', 'Gráfico · subtítulo'], ['.src, .src *', 'Gráfico · fonte'],
      ['.foot, .foot *', 'Rodapé'], ['.aspa, .aspa *', 'Box · aspa'],
      ['.__pseudo', 'Detalhe'], ['.panel.tabela', 'Painel da tabela'], ['.panel', 'Painel de gráfico'],
      ['.esn-top', 'Box · faixa do logo'], ['.esn-qr', 'Box · faixa do QR Code'], ['.esn', 'Box 2026 em Números'], ['.tempo', 'Linha do tempo']
    ];
    for (const [sel, name] of tests) if (el.matches(sel)) return name;
    const c = [...el.classList].filter(c => !c.startsWith('__'))[0];
    return 'Outros · ' + el.tagName.toLowerCase() + (c ? '.' + c : '');
  };

  // Probe de linha de base: span inline-block de altura zero alinhado na linha de base.
  const probeAt = (node, atEnd) => {
    const s = document.createElement('span');
    s.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline;padding:0;margin:0;border:0';
    if (node.nodeType === 3) { atEnd ? node.after(s) : node.before(s); }
    else { atEnd ? node.append(s) : node.prepend(s); }
    const y = s.getBoundingClientRect().top; s.remove(); return y;
  };

  // Parágrafos e trechos de um bloco de texto.
  const blockOf = (n, root) => { let e = n.parentElement; while (e && e !== root && /^inline/.test(getComputedStyle(e).display)) e = e.parentElement; return e || root; };
  const roleEl = e => (e && e.classList.contains('__anon') ? e.parentElement : e);
  function paragraphs(root, origin) {
    const paras = []; let cur = null, brk = true;
    const walk = n => {
      if (n.nodeType === 3) {
        const pe = n.parentElement; if (!vis(pe)) return;
        const t = n.textContent.replace(/\s+/g, ' ');
        if (!t.trim() && (brk || !cur)) return;
        if (!cur || brk) {
          const b = blockOf(n, root);
          cur = { runs: [], first: n, last: n, block: b, role: roleOf(roleEl(b)) }; paras.push(cur); brk = false;
        }
        cur.runs.push({ text: t, ...fontOf(getComputedStyle(pe)), cls: [...pe.classList].join(' ') });
        cur.last = n;
      } else if (n.nodeType === 1) {
        if (!vis(n) || n.classList.contains('__pseudo')) return;
        if (n.tagName === 'BR') { if (cur) cur.runs.push({ text: '\n', ...fontOf(getComputedStyle(n.parentElement)), cls: '' }); return; }
        const block = !/^inline/.test(getComputedStyle(n).display);
        if (block) brk = true;
        for (const k of n.childNodes) walk(k);
        if (block) brk = true;
      }
    };
    for (const k of root.childNodes) walk(k);
    for (const p of paras) {
      // apara espaços nas pontas
      while (p.runs.length && !p.runs[0].text.trim() && p.runs[0].text !== '\n') p.runs.shift();
      if (p.runs.length) p.runs[0].text = p.runs[0].text.replace(/^\s+/, '');
      if (p.runs.length) p.runs[p.runs.length - 1].text = p.runs[p.runs.length - 1].text.replace(/\s+$/, '');
      const bcs = getComputedStyle(p.block);
      p.align = bcs.textAlign; p.lh = bcs.lineHeight === 'normal' ? null : px(bcs.lineHeight);
      p.base0 = probeAt(p.first, false) - origin.top; p.base1 = probeAt(p.last, true) - origin.top;
      delete p.first; delete p.last; delete p.block; delete p.closed;
    }
    return paras.filter(p => p.runs.some(r => r.text.trim()));
  }

  const svgString = svg => {
    const clone = svg.cloneNode(true);
    const src = [svg, ...svg.querySelectorAll('*')], dst = [clone, ...clone.querySelectorAll('*')];
    const props = ['fill', 'fill-opacity', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-dasharray', 'opacity', 'font-family', 'font-size', 'font-weight', 'font-style', 'text-anchor', 'dominant-baseline', 'letter-spacing'];
    src.forEach((s, i) => { const cs = getComputedStyle(s); const st = props.map(p => `${p}:${cs.getPropertyValue(p)}`).join(';'); dst[i].setAttribute('style', st); dst[i].removeAttribute('class'); });
    const r = svg.getBoundingClientRect();
    clone.setAttribute('width', r.width); clone.setAttribute('height', r.height);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    return clone.outerHTML;
  };

  const out = { pages: [], width: PAGES[0] ? PAGES[0].getBoundingClientRect().width : 900, height: PAGES[0] ? PAGES[0].getBoundingClientRect().height : 1207 };
  PAGES.forEach((page, pi) => {
    const origin = page.getBoundingClientRect();
    const items = [];
    const boxItems = (el, cs, layer) => {
      const r = rectOf(el, origin);
      if (!isNone(cs.backgroundColor)) items.push({ type: 'rect', ...r, fill: cs.backgroundColor, radius: radiusOf(el), layer, name: roleOf(el) });
      const sides = { Top: [r.x, r.y, r.w, px(cs.borderTopWidth)], Bottom: [r.x, r.y + r.h - px(cs.borderBottomWidth), r.w, px(cs.borderBottomWidth)],
        Left: [r.x, r.y, px(cs.borderLeftWidth), r.h], Right: [r.x + r.w - px(cs.borderRightWidth), r.y, px(cs.borderRightWidth), r.h] };
      const all = ['Top', 'Right', 'Bottom', 'Left'].every(s => px(cs['border' + s + 'Width']) > 0 && cs['border' + s + 'Color'] === cs.borderTopColor);
      if (all && !isNone(cs.borderTopColor) && cs.borderTopStyle !== 'none') {
        items.push({ type: 'rect', ...r, stroke: cs.borderTopColor, strokeW: px(cs.borderTopWidth), radius: radiusOf(el), layer, name: 'Contorno' });
      } else for (const [s, [x, y, w, h]] of Object.entries(sides)) {
        if (h > 0 && w > 0 && px(cs['border' + s + 'Width']) > 0 && !isNone(cs['border' + s + 'Color']) && cs['border' + s + 'Style'] !== 'none')
          items.push({ type: 'rect', x, y, w, h, fill: cs['border' + s + 'Color'], layer, name: 'Filete' });
      }
    };
    const visit = (el, layer) => {
      if (!vis(el)) return;
      if (el.classList.contains('busca') || el.classList.contains('manual')) layer = 'prova';
      const cs = getComputedStyle(el);
      if (el.classList.contains('flow')) {
        const r = rectOf(el, origin);
        const fp = el.querySelector('p,h4');
        items.push({ type: 'flow', ...r, order: +el.dataset.flow || 0, columns: parseInt(cs.columnCount) || 1, gap: px(cs.columnGap),
          base0: fp ? probeAt(fp.firstChild || fp, false) - origin.top - r.y : null });
        return;
      }
      if (el.tagName === 'IMG') {
        const r = rectOf(el, origin);
        items.push({ type: 'image', ...r, clip: clipRect(el, page), src: el.currentSrc || el.src, nw: el.naturalWidth, nh: el.naturalHeight,
          fit: cs.objectFit, pos: cs.objectPosition, radius: radiusOf(el), alt: el.alt || '', inPhoto: !!el.closest('.ph'),
          busca: (el.closest('figure') && el.closest('figure').querySelector('.busca')) ? [...el.closest('figure').querySelector('.busca').childNodes].map(n => n.textContent.replace(/\s+/g, ' ').trim()).filter(Boolean).join(': ') : '',
          credito: (el.closest('figure') && el.closest('figure').querySelector('.cr')) ? el.closest('figure').querySelector('.cr').textContent.replace(/\s+/g, ' ').trim() : '',
          cls: [...el.classList].join(' '), layer });
        return;
      }
      if (el.tagName.toLowerCase() === 'svg') {
        const r = rectOf(el, origin);
        const fig = el.closest('figure');
        const title = fig && fig.querySelector('h3') ? fig.querySelector('h3').textContent.trim() : (el.getAttribute('aria-label') || 'grafico');
        items.push({ type: 'svg', ...r, clip: clipRect(el, page), svg: svgString(el), title, layer });
        return;
      }
      if (el.tagName === 'TABLE') {
        boxItems(el, cs, layer);
        const r = rectOf(el, origin);
        const rows = [...el.rows].map(tr => {
          const tr_r = tr.getBoundingClientRect();
          return { h: tr_r.height, cls: tr.className, cells: [...tr.cells].map(td => {
            const c = getComputedStyle(td); const cr = td.getBoundingClientRect();
            let bg = c.backgroundColor; if (isNone(bg)) bg = getComputedStyle(tr).backgroundColor; if (isNone(bg)) bg = getComputedStyle(el).backgroundColor;
            return { w: cr.width, bg, pad: [px(c.paddingTop), px(c.paddingLeft), px(c.paddingBottom), px(c.paddingRight)],
              bb: px(c.borderBottomWidth) > 0 && !isNone(c.borderBottomColor) ? [c.borderBottomColor, px(c.borderBottomWidth)] : null,
              valign: c.verticalAlign, header: td.tagName === 'TH' || tr.parentElement.tagName === 'THEAD',
              paras: paragraphs(td, origin), total: tr.classList.contains('tot') };
          }) };
        });
        items.push({ type: 'table', ...r, rows, header: el.tHead ? el.tHead.rows.length : 0, layer });
        return;
      }
      if (el !== page && hasBox(cs)) boxItems(el, cs, layer);
      if (el !== page && isTextBlock(el)) {
        const r = rectOf(el, origin);
        const content = { x: r.x + px(cs.paddingLeft) + px(cs.borderLeftWidth), y: r.y + px(cs.paddingTop) + px(cs.borderTopWidth) };
        content.w = r.w - px(cs.paddingLeft) - px(cs.paddingRight) - px(cs.borderLeftWidth) - px(cs.borderRightWidth);
        content.h = r.h - px(cs.paddingTop) - px(cs.paddingBottom) - px(cs.borderTopWidth) - px(cs.borderBottomWidth);
        const paras = paragraphs(el, origin);
        const rot = /^vertical/.test(cs.writingMode) ? 90 : 0;   // crédito na vertical, de cima para baixo
        if (paras.length) items.push({ type: 'text', ...content, paras, role: roleOf(el), layer, rot });
        return;
      }
      for (const k of el.children) visit(k, layer);
    };
    visit(page, 'base');
    const lado = page.dataset.lado || (page.classList.contains('dir') ? 'dir' : page.classList.contains('esq') ? 'esq' : null);
    out.pages.push({ items, lado });
  });

  // Texto corrido completo (template#texto) — fonte da história encadeada.
  const tpl = document.getElementById('texto');
  const story = [];
  const runsOf = (node, acc, cls) => {
    for (const k of node.childNodes) {
      if (k.nodeType === 3) { const t = k.textContent.replace(/\s+/g, ' '); if (t) acc.push({ text: t, cls }); }
      else if (k.nodeType === 1) {
        if (k.classList.contains('fim')) { acc.push({ text: '■', cls: 'fim' }); continue; }
        if (k.tagName === 'BR') { acc.push({ text: '\n', cls }); continue; }
        const c = [cls, k.className, ['B', 'STRONG'].includes(k.tagName) ? 'negrito' : '', ['I', 'EM'].includes(k.tagName) ? 'italico' : ''].filter(Boolean).join(' ');
        runsOf(k, acc, c);
      }
    }
    return acc;
  };
  if (tpl) {
    for (const el of tpl.content.children) {
      const runs = runsOf(el, [], '');
      if (runs.length) { runs[0].text = runs[0].text.replace(/^\s+/, ''); runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/\s+$/, ''); }
      story.push({ tag: el.tagName.toLowerCase(), cls: el.className, runs });
    }
  } else {
    for (const box of [...document.querySelectorAll('.flow')].sort((a, b) => a.dataset.flow - b.dataset.flow)) {
      for (const el of box.children) {
        const runs = runsOf(el, [], '');
        if (el.classList.contains('cont') && story.length) { const last = story[story.length - 1]; last.runs.push({ text: ' ', cls: '' }, ...runs); }
        else story.push({ tag: el.tagName.toLowerCase(), cls: el.className, runs });
      }
    }
  }
  out.story = story;
  // Estilo computado do corpo e do intertítulo dentro do fluxo (para os estilos de parágrafo).
  const fb = document.querySelector('.flow p:not(.cap)'), fh = document.querySelector('.flow h4');
  if (fb) { const cs = getComputedStyle(fb); out.body = { ...fontOf(cs), indent: px(cs.textIndent), align: cs.textAlign }; }
  if (fh) { const cs = getComputedStyle(fh); out.inter = { ...fontOf(cs), mt: px(cs.marginTop), mb: px(cs.marginBottom) }; }
  const cap = document.querySelector('.flow p.cap');
  if (cap) { const cs = getComputedStyle(cap, '::first-letter'); out.cap = { ...fontOf(cs) }; }
  out.title = document.title;
  const banco = document.querySelector('.banco table');
  out.banco = banco ? [...banco.rows].map(r => [...r.cells].map(c => c.textContent.replace(/\s+/g, ' ').trim())) : [];
  out.bancoLinks = banco ? [...banco.rows].map(r => { const a = r.querySelector('a'); return a ? a.href : ''; }) : [];
  out.fechamento = [...document.querySelectorAll('.apur li')].map(li => li.textContent.replace(/\s+/g, ' ').trim());
  const info = document.getElementById('ocupacao'); out.ocupacao = info ? info.textContent : '';
  return out;
})();
