/* Deck engine shared by the three pitch concepts in judges/pitch/a5/: a fixed 1280×720 stage scaled to the
   window, keyboard navigation, a 3-minute timer, the script drawer and live numbers from race-data.js.
   Keys: → / space next · ← back · 1-7 jump · S script · T restart the timer. Add ?present to start with the script hidden. */
(() => {
  const stage = document.querySelector('.stage');
  const secs = [...stage.querySelectorAll(':scope > section')];
  const R = window.RACE;
  const LIMIT = 180;
  let cur = -1, t0 = null, drawerOpen = !/[?&]present\b/.test(location.search);

  // Live numbers: a [data-live] span keeps its static text unless race-data.js is loaded.
  const L = {};
  if (R && R.latest) {
    const rows = R.latest.rows, us = rows.find(r => r[0] === 't05'), top = rows[0];
    Object.assign(L, {
      tick: R.latest.tick, teams: rows.length, rank: rows.indexOf(us) + 1,
      score: us[1].toFixed(2), neg: us[2].toFixed(2), mkt: us[3].toFixed(2),
      negrank: [...rows].sort((a, b) => b[2] - a[2]).indexOf(us) + 1,
      leader: 'Team ' + Number(top[0].slice(1)), leadscore: top[1].toFixed(2), leadmkt: top[3].toFixed(2),
      gap: (top[1] - us[1]).toFixed(2), mktgap: (top[3] - us[3]).toFixed(2),
      first: R.us.rank.filter(r => r === 1).length, snaps: R.ticks.length,
    });
  }
  document.querySelectorAll('[data-live]').forEach(n => { if (L[n.dataset.live] != null) n.textContent = L[n.dataset.live]; });

  const style = document.createElement('style');
  style.textContent = `
  html,body{margin:0;height:100%;overflow:hidden}
  .viewport{position:fixed;inset:0 0 34px 0;overflow:hidden}
  body.drawer .viewport{right:380px}
  .stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;overflow:hidden;transform:translate(-50%,-50%) scale(var(--k,1))}
  .stage>section{position:absolute;inset:0;visibility:hidden;opacity:0;transition:opacity .3s}
  .stage>section.on{visibility:visible;opacity:1}
  .say{display:none}
  .hud{position:fixed;left:0;right:0;bottom:0;height:34px;display:flex;align-items:center;gap:14px;padding:0 14px;box-sizing:border-box;
    font:12px/1 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--hud-bg,#0b0b0b);color:var(--hud-fg,#fff);z-index:10}
  .hud button{all:unset;cursor:pointer;padding:6px 9px;border-radius:5px;font-size:14px}
  .hud button:hover{background:rgba(255,255,255,.14)}
  .hud .dots{display:flex;gap:6px}
  .hud .dots i{width:22px;height:4px;border-radius:2px;background:rgba(255,255,255,.25);cursor:pointer}
  .hud .dots i.on{background:var(--hud-accent,#3987e5)}
  .hud .where{opacity:.85}
  .hud .timer{margin-left:auto;font-variant-numeric:tabular-nums}
  .hud .timer.over b{color:#e66767}
  .hud .keys{opacity:.55}
  .drawer{position:fixed;top:0;right:0;bottom:34px;width:380px;box-sizing:border-box;overflow:auto;display:none;padding:18px 20px 30px;
    font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;background:#161615;color:#e9e8e3;border-left:1px solid rgba(255,255,255,.1);z-index:9}
  body.drawer .drawer{display:block}
  .drawer h3{margin:0 0 2px;font-size:15px}
  .drawer .meta{color:#898781;font-size:12px;margin-bottom:14px}
  .drawer ol{list-style:none;margin:0;padding:0}
  .drawer li{padding:10px 12px;margin:0 -12px 6px;border-radius:8px;cursor:pointer;opacity:.5}
  .drawer li.on{opacity:1;background:rgba(255,255,255,.07)}
  .drawer li h4{margin:0 0 4px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#c3c2b7;display:flex;justify-content:space-between}
  .drawer li p{margin:0}
  .drawer details{margin-top:14px;color:#c3c2b7;font-size:12px}
  .drawer table{border-collapse:collapse;margin-top:8px;font-variant-numeric:tabular-nums}
  .drawer td,.drawer th{padding:2px 10px 2px 0;text-align:right}`;
  document.head.append(style);

  const fmt = s => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  const says = secs.map(s => s.querySelector('.say'));
  const budget = says.map(s => Number(s?.dataset.secs || 0));
  const words = says.reduce((n, s) => n + (s ? s.textContent.trim().split(/\s+/).length : 0), 0);

  const drawer = document.createElement('aside');
  drawer.className = 'drawer';
  drawer.innerHTML = `<h3>Script</h3><div class="meta">${fmt(budget.reduce((a, b) => a + b, 0))} planned · ${words} words · click a block to jump</div><ol>` +
    secs.map((s, i) => `<li data-i="${i}"><h4><span>${i + 1} · ${s.dataset.title || ''}</span><span>${fmt(budget[i])}</span></h4><p>${says[i] ? says[i].innerHTML : ''}</p></li>`).join('') + '</ol>' +
    (R ? `<details><summary>Race data as a table (Team 5, every snapshot; source ${R.source})</summary><table><tr><th>tick</th><th>score</th><th>rank</th><th>negotiating</th><th>market</th></tr>` +
      R.ticks.map((t, k) => `<tr><td>${t}</td><td>${R.score.t05[k].toFixed(2)}</td><td>#${R.us.rank[k]}</td><td>${R.us.negotiating[k].toFixed(2)}</td><td>${R.us.market[k].toFixed(2)}</td></tr>`).join('') + '</table></details>' : '');
  drawer.addEventListener('click', e => { const li = e.target.closest('li'); if (li) show(Number(li.dataset.i)); });

  const hud = document.createElement('footer');
  hud.className = 'hud';
  hud.innerHTML = `<button data-go="-1" aria-label="Back">‹</button><span class="dots">${secs.map(() => '<i></i>').join('')}</span><button data-go="1" aria-label="Next">›</button>
    <span class="where"></span><span class="timer"></span><span class="keys">← → · S script · T timer</span>`;
  hud.addEventListener('click', e => {
    const b = e.target.closest('button'); if (b) return show(cur + Number(b.dataset.go));
    const d = e.target.closest('.dots i'); if (d) show([...d.parentNode.children].indexOf(d));
  });
  document.body.append(drawer, hud);

  function fit() {
    document.body.classList.toggle('drawer', drawerOpen);
    const w = innerWidth - (drawerOpen ? 380 : 0), h = innerHeight - 34;
    stage.style.setProperty('--k', Math.min(w / 1280, h / 720));
  }
  function tick() {
    const el = t0 ? (Date.now() - t0) / 1000 : 0, target = budget.slice(0, cur + 1).reduce((a, b) => a + b, 0);
    const t = hud.querySelector('.timer');
    t.classList.toggle('over', el > LIMIT);
    t.innerHTML = `<b>${fmt(el)}</b> / ${fmt(LIMIT)} · this screen ends at ${fmt(target)}`;
  }
  function show(i) {
    i = Math.max(0, Math.min(secs.length - 1, i));
    if (i === cur) return;
    if (i > 0 && !t0) t0 = Date.now();
    cur = i;
    secs.forEach((s, k) => s.classList.toggle('on', k === i));
    hud.querySelectorAll('.dots i').forEach((d, k) => d.classList.toggle('on', k <= i));
    hud.querySelector('.where').textContent = `${i + 1} / ${secs.length} · ${secs[i].dataset.title || ''}`;
    drawer.querySelectorAll('li').forEach((li, k) => { li.classList.toggle('on', k === i); if (k === i) li.scrollIntoView({block: 'nearest'}); });
    history.replaceState(null, '', '#' + (i + 1));
    tick();
    document.dispatchEvent(new CustomEvent('deck:show', {detail: {i, section: secs[i]}}));
  }
  addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); show(cur + 1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(cur - 1); }
    else if (/^[1-9]$/.test(e.key)) show(Number(e.key) - 1);
    else if (e.key === 's' || e.key === 'S') { drawerOpen = !drawerOpen; fit(); }
    else if (e.key === 't' || e.key === 'T') { t0 = Date.now(); tick(); }
  });
  addEventListener('resize', fit);
  setInterval(tick, 500);
  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
