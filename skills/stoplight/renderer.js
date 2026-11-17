function render(data, root) {
  const el = (t, cls, txt) => { const e = document.createElement(t); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const NAME = { F: 'Fatto', I: 'Interpretazione', S: 'Supposizione' };
  const MEAN = { F: 'la fonte lo dice per intero', I: 'in parte dalla fonte', S: 'manca nella fonte' };
  const BY = { ai: 'IA', user: 'utente' };
  const claims = Object.fromEntries(data.claims.map(c => [c.id, c]));

  root.append(el('h2', null, 'Mappa dei ragionamenti'));
  const lg = el('div', 'sl-legend');
  for (const t of ['F', 'I', 'S']) lg.append(el('span', 'chip ' + t, NAME[t] + ' · ' + MEAN[t]));
  root.append(lg);

  const depth = {}, busy = new Set();
  const dep = id => {
    if (depth[id] !== undefined) return depth[id];
    if (busy.has(id)) return 0;
    busy.add(id);
    const ps = data.reasonings.filter(r => r.to === id).flatMap(r => r.from);
    depth[id] = ps.length ? Math.max(...ps.map(dep)) + 1 : 0;
    busy.delete(id);
    return depth[id];
  };
  data.claims.forEach(c => dep(c.id));
  const cols = [];
  data.claims.forEach(c => (cols[depth[c.id]] ||= []).push(c));

  const graph = el('div', 'sl-graph');
  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg'); svg.setAttribute('class', 'sl-svg');
  graph.append(svg);
  const nodes = {};
  for (const col of cols.filter(Boolean)) {
    const ce = el('div', 'sl-col');
    for (const c of col) {
      const d = el('div', 'sl-card ' + c.type);
      const id = el('div', 'id', c.id); id.append(el('span', null, NAME[c.type] + (c.by ? ' · ' + BY[c.by] : '')));
      d.append(id, el('p', null, c.text));
      if (c.cite) d.append(el('div', 'cite', c.cite));
      if (c.basis && c.basis !== 'none') d.append(el('div', 'cite', 'Base: ' + c.basis));
      nodes[c.id] = d; ce.append(d);
    }
    graph.append(ce);
  }
  root.append(graph);

  const edges = data.reasonings.flatMap(r => r.from.map(f => ({ r: r.id, from: f, to: r.to, t: r.type || 'F' })));
  const related = id => {
    const out = new Set([id]);
    const up = x => edges.filter(e => e.to === x).forEach(e => { if (!out.has(e.from)) { out.add(e.from); up(e.from); } });
    const down = x => edges.filter(e => e.from === x).forEach(e => { if (!out.has(e.to)) { out.add(e.to); down(e.to); } });
    up(id); down(id); return out;
  };
  const rs = Object.fromEntries(data.reasonings.map(r => [r.id, r]));
  const tip = el('div', 'sl-tip'); document.body.append(tip);
  const tagOf = id => { const s = el('span', 't ' + claims[id].type, id); return s; };
  const showTip = (x, y, ids) => {
    tip.replaceChildren();
    for (const id of ids) {
      const r = rs[id], h = el('div', 'h'); h.append(el('b', null, r.id + '  '));
      r.from.forEach((f, i) => { if (i) h.append(document.createTextNode(' + ')); h.append(tagOf(f)); });
      h.append(document.createTextNode(' → '), tagOf(r.to));
      h.append(el('span', 'm', '  ' + NAME[r.type || 'F'] + (r.by ? ' · ' + BY[r.by] : '')));
      tip.append(h, el('div', 'x', r.text));
      const src = r.cite || (r.basis && r.basis !== 'none' ? 'Base: ' + r.basis : '');
      if (src) tip.append(el('div', 'src', src));
    }
    tip.classList.add('on');
    const w = tip.offsetWidth, hh = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(x + 14, innerWidth - w - 8)) + 'px';
    tip.style.top = Math.max(8, Math.min(y + 14, innerHeight - hh - 8)) + 'px';
  };
  const hideTip = () => tip.classList.remove('on');
  const paths = [];
  const draw = () => {
    svg.innerHTML = ''; paths.length = 0;
    const g = graph.getBoundingClientRect();
    svg.setAttribute('width', graph.scrollWidth); svg.setAttribute('height', graph.scrollHeight);
    for (const e of edges) {
      const a = nodes[e.from].getBoundingClientRect(), b = nodes[e.to].getBoundingClientRect();
      const x1 = a.right - g.left + graph.scrollLeft, y1 = a.top + a.height / 2 - g.top;
      const x2 = b.left - g.left + graph.scrollLeft, y2 = b.top + b.height / 2 - g.top, m = (x1 + x2) / 2;
      const p = document.createElementNS(svgNS, 'path'); p.setAttribute('class', 'arc ' + e.t);
      p.setAttribute('d', `M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}`);
      const hit = document.createElementNS(svgNS, 'path'); hit.setAttribute('d', p.getAttribute('d')); hit.setAttribute('class', 'hit');
      hit.addEventListener('mousemove', ev => showTip(ev.clientX, ev.clientY, [e.r]));
      hit.addEventListener('mouseleave', hideTip);
      svg.append(p, hit); paths.push({ p, e });
      const lab = document.createElementNS(svgNS, 'text');
      lab.setAttribute('x', m); lab.setAttribute('y', (y1 + y2) / 2 + 3); lab.setAttribute('text-anchor', 'middle'); lab.textContent = e.r;
      lab.setAttribute('class', 'lab');
      lab.addEventListener('mousemove', ev => showTip(ev.clientX, ev.clientY, [e.r]));
      lab.addEventListener('mouseleave', hideTip);
      svg.append(lab);
    }
  };
  requestAnimationFrame(draw); addEventListener('resize', draw);
  for (const [id, d] of Object.entries(nodes)) {
    d.addEventListener('mousemove', ev => {
      const ids = data.reasonings.filter(r => r.to === id).map(r => r.id);
      if (ids.length) showTip(ev.clientX, ev.clientY, ids); else hideTip();
    });
    d.addEventListener('mouseenter', () => {
      const rel = related(id); graph.classList.add('focus');
      Object.entries(nodes).forEach(([k, n]) => n.classList.toggle('rel', rel.has(k)));
      paths.forEach(({ p, e }) => { const hot = rel.has(e.from) && rel.has(e.to); p.classList.toggle('hot', hot); p.classList.toggle('dim', !hot); });
    });
    d.addEventListener('mouseleave', () => {
      hideTip(); graph.classList.remove('focus');
      Object.values(nodes).forEach(n => n.classList.remove('rel'));
      paths.forEach(({ p }) => p.classList.remove('hot', 'dim'));
    });
  }

}
