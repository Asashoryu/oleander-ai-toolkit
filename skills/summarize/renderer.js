function render(data, root, rep) {
  const h = (t, txt) => Object.assign(document.createElement(t), { textContent: txt });
  const refs = [];
  const sup = ids => {
    const s = document.createElement('sup');
    ids.forEach((id, k) => {
      const place = rep.atoms[id].place;
      let n = refs.indexOf(place) + 1;
      if (!n) n = refs.push(place);
      const a = h('a', n); a.href = '#ref-' + n;
      if (k) s.append(document.createTextNode(','));
      s.append(a);
    });
    return s;
  };
  const section = (sec, depth) => {
    root.append(h(['h2', 'h3', 'h4'][Math.min(depth, 2)], sec.title));
    for (const p of sec.paragraphs || []) {
      const e = document.createElement('p');
      e.append(document.createTextNode(p.text), sup(p.atoms));
      root.append(e);
    }
    (sec.sections || []).forEach(s => section(s, depth + 1));
  };
  data.sections.forEach(s => section(s, 0));
  root.append(h('h2', 'Riferimenti'));
  const ol = h('ol', ''); ol.className = 'refs';
  refs.forEach((r, i) => { const li = h('li', r); li.id = 'ref-' + (i + 1); ol.append(li); });
  root.append(ol);
}
