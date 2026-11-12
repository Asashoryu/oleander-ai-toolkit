function render(data, root) {
  const el = (t, cls, txt) => { const e = document.createElement(t); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const NAME = { F: 'Fatto', I: 'Interpretazione', S: 'Supposizione' };
  const MEAN = { F: 'la fonte lo sostiene', I: 'rielaborazione dell\'utente', S: 'forte per l\'utente, debole nella fonte' };
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
      const id = el('div', 'id', c.id); id.append(el('span', null, NAME[c.type]));
      d.append(id, el('p', null, c.text));
      if (c.cite) d.append(el('div', 'cite', c.cite));
      nodes[c.id] = d; ce.append(d);
    }
    graph.append(ce);
  }
  root.append(graph);

  const edges = data.reasonings.flatMap(r => r.from.map(f => ({ r: r.id, from: f, to: r.to })));
  const related = id => {
    const out = new Set([id]);
    const up = x => edges.filter(e => e.to === x).forEach(e => { if (!out.has(e.from)) { out.add(e.from); up(e.from); } });
    const down = x => edges.filter(e => e.from === x).forEach(e => { if (!out.has(e.to)) { out.add(e.to); down(e.to); } });
    up(id); down(id); return out;
  };
  const paths = [];
  const draw = () => {
    svg.innerHTML = ''; paths.length = 0;
    const g = graph.getBoundingClientRect();
    svg.setAttribute('width', graph.scrollWidth); svg.setAttribute('height', graph.scrollHeight);
    for (const e of edges) {
      const a = nodes[e.from].getBoundingClientRect(), b = nodes[e.to].getBoundingClientRect();
      const x1 = a.right - g.left + graph.scrollLeft, y1 = a.top + a.height / 2 - g.top;
      const x2 = b.left - g.left + graph.scrollLeft, y2 = b.top + b.height / 2 - g.top, m = (x1 + x2) / 2;
      const p = document.createElementNS(svgNS, 'path');
      p.setAttribute('d', `M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}`);
      svg.append(p); paths.push({ p, e });
      const lab = document.createElementNS(svgNS, 'text');
      lab.setAttribute('x', m); lab.setAttribute('y', (y1 + y2) / 2 + 3); lab.setAttribute('text-anchor', 'middle'); lab.textContent = e.r;
      svg.append(lab);
    }
  };
  requestAnimationFrame(draw); addEventListener('resize', draw);
  for (const [id, d] of Object.entries(nodes)) {
    d.addEventListener('mouseenter', () => {
      const rel = related(id); graph.classList.add('focus');
      Object.entries(nodes).forEach(([k, n]) => n.classList.toggle('rel', rel.has(k)));
      paths.forEach(({ p, e }) => { const hot = rel.has(e.from) && rel.has(e.to); p.classList.toggle('hot', hot); p.classList.toggle('dim', !hot); });
    });
    d.addEventListener('mouseleave', () => {
      graph.classList.remove('focus');
      Object.values(nodes).forEach(n => n.classList.remove('rel'));
      paths.forEach(({ p }) => p.classList.remove('hot', 'dim'));
    });
  }

  root.append(el('h2', null, 'Ragionamenti'));
  const ul = el('ul', 'sl-r');
  const tag = id => { const s = el('span', 't ' + claims[id].type, id); return s; };
  for (const r of data.reasonings) {
    const li = el('li'); li.append(el('b', null, r.id + '  '));
    r.from.forEach((f, i) => { if (i) li.append(document.createTextNode(' + ')); li.append(tag(f)); });
    li.append(document.createTextNode(' → '), tag(r.to), document.createTextNode('  ' + r.text));
    ul.append(li);
  }
  root.append(ul);
}
