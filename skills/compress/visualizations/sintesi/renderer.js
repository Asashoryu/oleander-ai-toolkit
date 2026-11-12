function render(data, root) {
  const h = (t, txt) => Object.assign(document.createElement(t), { textContent: txt });
  const refs = [];
  const sup = source => {
    let n = refs.indexOf(source) + 1;
    if (!n) n = refs.push(source);
    const s = document.createElement('sup'), a = h('a', n);
    a.href = '#ref-' + n; s.append(a); return s;
  };
  const section = (sec, depth) => {
    root.append(h(['h2', 'h3', 'h4'][Math.min(depth, 2)], sec.title));
    if (sec.timeline) {
      const ol = h('ol', ''); ol.className = 'timeline';
      for (const e of sec.timeline) {
        const li = document.createElement('li');
        li.append(h('time', e.when), document.createTextNode(e.text), sup(e.source));
        ol.append(li);
      }
      root.append(ol);
    }
    if (sec.points && sec.points.length) {
      const ul = document.createElement('ul');
      for (const p of sec.points) {
        const li = document.createElement('li');
        li.append(document.createTextNode(p.text), sup(p.source));
        ul.append(li);
      }
      root.append(ul);
    }
    if (sec.quote) {
      const b = h('blockquote', sec.quote.text);
      b.append(h('cite', sec.quote.by), sup(sec.quote.source));
      root.append(b);
    }
    (sec.sections || []).forEach(s => section(s, depth + 1));
  };
  data.sections.forEach(s => section(s, 0));
  root.append(h('h2', 'Riferimenti'));
  const ol = h('ol', ''); ol.className = 'refs';
  refs.forEach((r, i) => { const li = h('li', r); li.id = 'ref-' + (i + 1); ol.append(li); });
  root.append(ol);
}
