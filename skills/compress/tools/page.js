const rep = JSON.parse(document.getElementById('report').textContent);
const $ = (t, cls, txt) => { const e = document.createElement(t); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
const root = document.documentElement;
root.dataset.theme = localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light');
const app = document.getElementById('app');

const hero = $('header', 'hero');
hero.append($('div', 'kicker', 'Condensato · ' + rep.date), $('h1', null, rep.title),
  $('div', 'sub', rep.sources.map(s => s.name).join(' · ')));
const tg = $('button', null, root.dataset.theme === 'dark' ? '☀ Chiaro' : '☾ Scuro'); tg.id = 'theme';
tg.onclick = () => { root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark'; localStorage.setItem('theme', root.dataset.theme); tg.textContent = root.dataset.theme === 'dark' ? '☀ Chiaro' : '☾ Scuro'; };
hero.append(tg);

const toc = $('nav'); toc.id = 'toc';
const main = $('main'); main.id = 'content';
const side = $('aside'); side.id = 'scheda';
const layout = $('div', 'layout'); layout.append(toc, main, side);
app.append(hero, layout);

render(rep.data, main);

const card = (title, ...kids) => { const c = $('div', 'card'); c.append($('h5', null, title), ...kids); return c; };
if (rep.data.scheda && rep.data.scheda.length) {
  const dl = $('dl');
  rep.data.scheda.forEach(f => dl.append($('dt', null, f.label), $('dd', null, f.value)));
  side.append(card('Scheda', dl));
}
const st = rep.stats, pct = st.report_words && st.source_words ? Math.min(100, 100 * st.report_words / st.source_words) : 0;
const big = $('div', 'big', '×' + st.ratio); big.append($('small', null, 'compressione'));
const bar = $('div', 'bar'); const fill = $('i'); fill.style.width = pct.toFixed(1) + '%'; bar.append(fill);
side.append(card('Compressione', big, bar, $('div', 'muted', st.source_words + ' parole → ' + st.report_words)));
const pend = $('div');
if (rep.not_treated.length) { const ul = $('ul'); rep.not_treated.forEach(t => ul.append($('li', null, t))); pend.append(ul); }
else pend.append($('span', 'muted', 'Tutto trattato.'));
side.append(card('Non trattato', pend));
const out = (title, items, fmt) => { const d = $('details'); d.append($('summary', null, title + ' (' + items.length + ')')); if (items.length) { const ul = $('ul'); items.forEach(i => ul.append($('li', null, fmt(i)))); d.append(ul); } return d; };
const cd = $('div'); cd.append(out('Rumore', rep.noise, n => n.text + ' — ' + n.reason), out('Perso', rep.lost, n => n.text));
side.append(card('Scarti', cd));

const heads = [...main.querySelectorAll('h2,h3')];
toc.append($('b', null, 'Indice'));
const links = heads.map((h, i) => { h.id = h.id || 's' + i; const a = $('a', h.tagName === 'H3' ? 'l3' : '', h.textContent); a.href = '#' + h.id; toc.append(a); return a; });
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { links.forEach(l => l.classList.remove('on')); links[heads.indexOf(e.target)].classList.add('on'); } }), { rootMargin: '0px 0px -75% 0px' });
  heads.forEach(h => io.observe(h));
}
