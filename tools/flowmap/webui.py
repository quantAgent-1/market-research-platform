"""webui.py — flowmap dashboard renderer (single self-contained HTML file).

Follows the dataviz reference method: role-based CSS custom properties (light +
dark selected, not flipped), thin marks with rounded data-ends, 2px lines, surface
gaps/rings, hairline solid grid, per-mark tooltips + crosshair, a legend for >=2
series, and a table view under every chart. Status colors are reserved for state
chips; series colors are the fixed categorical order (never cycled).
"""
from __future__ import annotations

import json


def render_dashboard(state: dict) -> str:
    from flowmap import jsonify
    blob = json.dumps(jsonify(state), ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.replace("__DATA__", blob)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>flowmap — the five-question flow read</title>
<style>
:root{
  --surface-1:#fcfcfb; --plane:#f9f9f7; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#1baf7a; --s3:#eda100; --s5:#4a3aa7; --s6:#e34948; --s7:#e87ba4; --s8:#eb6834;
  --seq-250:#86b6ef;
  --good:#0ca30c; --warn:#fab219; --serious:#ec835a; --critical:#d03b3b;
  --pos:#e34948; --neg:#2a78d6;
}
@media (prefers-color-scheme: dark){ :root{
  --surface-1:#1a1a19; --plane:#0d0d0d; --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
  --s1:#3987e5; --s2:#199e70; --s3:#c98500; --s5:#9085e9; --s6:#e66767; --s7:#d55181; --s8:#d95926;
  --seq-250:#1c5cab; --pos:#e66767; --neg:#3987e5;
}}
:root[data-theme="light"]{
  --surface-1:#fcfcfb; --plane:#f9f9f7; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#1baf7a; --s3:#eda100; --s5:#4a3aa7; --s6:#e34948; --s7:#e87ba4; --s8:#eb6834;
  --seq-250:#86b6ef; --pos:#e34948; --neg:#2a78d6;
}
:root[data-theme="dark"]{
  --surface-1:#1a1a19; --plane:#0d0d0d; --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
  --s1:#3987e5; --s2:#199e70; --s3:#c98500; --s5:#9085e9; --s6:#e66767; --s7:#d55181; --s8:#d95926;
  --seq-250:#1c5cab; --pos:#e66767; --neg:#3987e5;
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
  font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:16px 18px 60px}
header{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin:6px 0 2px}
h1{font-size:19px;margin:0;font-weight:650}
h1 small{color:var(--muted);font-weight:400;font-size:12.5px;margin-left:8px}
.gen{color:var(--muted);font-size:12px;margin-left:auto}
#themeBtn{background:var(--surface-1);border:1px solid var(--ring);color:var(--ink-2);
  border-radius:8px;padding:3px 10px;cursor:pointer;font-size:12px}
.contract{color:var(--ink-2);font-size:12.2px;background:var(--surface-1);border:1px solid var(--ring);
  border-radius:10px;padding:8px 12px;margin:10px 0}
.freshrow{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px}
.fresh{font-size:11px;color:var(--ink-2);background:var(--surface-1);border:1px solid var(--ring);
  border-radius:999px;padding:2px 9px;display:inline-flex;gap:5px;align-items:center}
.fresh .dot{width:7px;height:7px;border-radius:50%}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 12px;position:sticky;top:0;z-index:5;
  background:var(--plane);padding:8px 0}
.tab{border:1px solid var(--ring);background:var(--surface-1);color:var(--ink-2);border-radius:9px;
  padding:6px 13px;cursor:pointer;font-size:13px}
.tab[aria-selected="true"]{color:var(--ink);border-color:var(--s1);box-shadow:inset 0 0 0 1px var(--s1);font-weight:600}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.card{background:var(--surface-1);border:1px solid var(--ring);border-radius:12px;padding:13px 15px}
.card.wide{grid-column:1/-1}
.card h2{font-size:13px;margin:0 0 2px;color:var(--muted);font-weight:600;letter-spacing:.2px;text-transform:uppercase}
.card h3{font-size:14.5px;margin:2px 0 8px;font-weight:600}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
.tiles{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0 2px}
.tile{background:var(--surface-1);border:1px solid var(--ring);border-radius:11px;padding:9px 13px;min-width:118px}
.tile .lb{font-size:11px;color:var(--muted)}
.tile .v{font-size:20px;font-weight:650;margin-top:1px}
.tile .d{font-size:11.5px;margin-top:1px}
.up{color:var(--good)} .dn{color:var(--critical)}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0 4px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:12px;border-radius:999px;
  padding:4px 11px;border:1px solid var(--ring);background:var(--surface-1);color:var(--ink-2);cursor:pointer}
.chip b{color:var(--ink);font-weight:600}
.chip .ic{font-size:11px}
.chip.good .ic{color:var(--good)} .chip.warn .ic{color:var(--warn)}
.chip.serious .ic{color:var(--serious)} .chip.critical .ic{color:var(--critical)}
.chip.info .ic{color:var(--s1)} .chip.neutral .ic{color:var(--muted)}
.conf{font-size:10px;color:var(--muted);border:1px solid var(--ring);border-radius:5px;padding:0 4px}
.ev{margin:6px 0 0;padding-left:18px;color:var(--ink-2);font-size:12.6px}
.ev li{margin:2px 0}
.hyp{font-size:12.6px;color:var(--ink-2);margin:7px 0 0}
.hyp b{color:var(--ink)}
.fals{font-size:11.8px;color:var(--muted);margin:4px 0 0}
.fals::before{content:"falsifier — ";color:var(--muted)}
svg{display:block}
.tt{position:fixed;pointer-events:none;background:var(--surface-1);border:1px solid var(--ring);
  border-radius:9px;padding:7px 10px;font-size:12px;box-shadow:0 4px 14px rgba(0,0,0,.14);z-index:50;display:none;max-width:340px}
.tt .h{color:var(--muted);font-size:11px;margin-bottom:3px}
.tt .r{display:flex;align-items:center;gap:7px;margin:1.5px 0}
.tt .k{width:14px;height:3px;border-radius:2px;flex:none}
.tt .v{font-weight:650;margin-left:auto;padding-left:12px}
.legend{display:flex;flex-wrap:wrap;gap:12px;margin:2px 0 6px;font-size:11.5px;color:var(--ink-2)}
.legend .it{display:inline-flex;align-items:center;gap:5px}
.legend .sw{width:14px;height:8px;border-radius:2px}
.legend .ln{width:14px;height:3px;border-radius:2px}
details.tbl{margin-top:8px;font-size:12px}
details.tbl summary{cursor:pointer;color:var(--muted);font-size:11.5px}
table{border-collapse:collapse;margin-top:6px;width:100%}
th,td{text-align:right;padding:3px 8px;border-bottom:1px solid var(--grid);font-variant-numeric:tabular-nums}
th:first-child,td:first-child{text-align:left}
th{color:var(--muted);font-weight:600;font-size:11px}
.note{font-size:11.5px;color:var(--muted);margin-top:6px}
input[type=range]{width:100%;accent-color:var(--s1)}
.mocR{color:var(--ink-2)}
.flag{border-left:3px solid var(--warn);padding:5px 10px;background:var(--surface-1);
  border-radius:0 9px 9px 0;margin:5px 0;font-size:12.5px}
.flag .rl{color:var(--muted);font-size:11px}
.zrow{display:grid;grid-template-columns:190px 1fr 120px;align-items:center;gap:8px;margin:3px 0;font-size:12.3px}
.zrow .lb{color:var(--ink-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zrow .vv{color:var(--ink);text-align:right;font-variant-numeric:tabular-nums}
.zrow .vv small{color:var(--muted)}
.sect{margin:16px 0 8px;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.stale{color:var(--warn)}
a{color:var(--s1)}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>flowmap<small>the five-question flow read - semis complex</small></h1>
  <span class="gen" id="gen"></span>
  <button id="themeBtn" type="button">theme</button>
</header>
<div class="contract" id="contract"></div>
<div class="freshrow" id="fresh"></div>
<nav class="tabs" id="tabs" role="tablist"></nav>
<main id="view"></main>
</div>
<div class="tt" id="tt"></div>
<script id="data" type="application/json">__DATA__</script>
<script>
"use strict";
const D = JSON.parse(document.getElementById('data').textContent);
const themeQ = (new URLSearchParams(location.search)).get('theme');
if(themeQ==='dark'||themeQ==='light') document.documentElement.dataset.theme = themeQ;
const $ = (s, el) => (el||document).querySelector(s);
const esc = s => String(s??'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const fmtPct = (x, dp=1, signed=true) => x==null ? 'n/a' : ((signed&&x>=0?'+':'')+(100*x).toFixed(dp)+'%');
const fmtUsd = (x, signed=false) => {
  if(x==null) return 'n/a'; const s = x<0?'-':(signed?'+':''); const a = Math.abs(x);
  for(const [d,u] of [[1e12,'T'],[1e9,'B'],[1e6,'M'],[1e3,'K']]) if(a>=d) return s+'$'+(a/d).toFixed(2)+u;
  return s+'$'+a.toFixed(0);
};
const fmtKrw = (x, signed=true) => {
  if(x==null) return 'n/a'; const s = x<0?'-':(signed?'+':''); const a = Math.abs(x);
  return a>=1e12 ? s+(a/1e12).toFixed(2)+'T KRW' : s+(a/1e9).toFixed(1)+'B KRW';
};
const fmtSh = x => x==null?'n/a':((x>=0?'+':'')+(x/1e6).toFixed(2)+'M sh');
const fmtAmt = (x, unit) => unit==='KRW' ? fmtKrw(x) : fmtSh(x);
const CHIP_IC = {good:'●', warn:'▲', serious:'▲', critical:'■', info:'●', neutral:'○'};
const MKT = {US:'--s1', KR:'--s2', TW:'--s3', EU:'--s5', BOTH:'--s7'};
const COH = {foreign_net:'--s1', inst_net:'--s2', trust_net:'--s2', retail_net:'--s3', dealer_net:'--s3'};

// ---------- theme
const btn = $('#themeBtn');
btn.onclick = () => {
  const cur = document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.dataset.theme = cur === 'dark' ? 'light' : 'dark';
  render(current);
};

// ---------- tooltip
const tt = $('#tt');
function showTT(x, y, head, rows){
  tt.innerHTML = '';
  if(head){ const h = document.createElement('div'); h.className='h'; h.textContent = head; tt.appendChild(h); }
  for(const r of rows){
    const div = document.createElement('div'); div.className='r';
    if(r.color){ const k = document.createElement('span'); k.className='k'; k.style.background=r.color; div.appendChild(k); }
    const lb = document.createElement('span'); lb.textContent = r.label; lb.style.color='var(--ink-2)'; div.appendChild(lb);
    const v = document.createElement('span'); v.className='v'; v.textContent = r.value; div.appendChild(v);
    tt.appendChild(div);
  }
  tt.style.display='block';
  const w = tt.offsetWidth, h = tt.offsetHeight;
  tt.style.left = Math.min(x+14, innerWidth-w-10)+'px';
  tt.style.top  = Math.max(6, Math.min(y+14, innerHeight-h-10))+'px';
}
const hideTT = () => tt.style.display='none';
addEventListener('scroll', hideTT, true);

// ---------- svg helpers
const NS = 'http://www.w3.org/2000/svg';
function svgEl(tag, attrs){ const e = document.createElementNS(NS, tag);
  for(const k in attrs) e.setAttribute(k, attrs[k]); return e; }
function barPath(x, y0, w, h, up){
  // rounded 4px at the data end, square at the baseline
  const r = Math.min(4, w/2, Math.abs(h));
  if(Math.abs(h) < 0.5) return `M${x},${y0-0.5}h${w}v1h${-w}Z`;
  if(up) return `M${x},${y0}v${-(h-r)}q0,${-r} ${r},${-r}h${w-2*r}q${r},0 ${r},${r}v${h-r}Z`;
  return `M${x},${y0}v${h-r}q0,${r} ${r},${r}h${w-2*r}q${r},0 ${r},${-r}v${-(h-r)}Z`;
}

// mini bar chart: one series, up/down from zero baseline
function barChart(parent, dates, vals, colorVar, fmt, label){
  const W = Math.min(parent.clientWidth||520, 640), H = 88, padL = 6, padR = 6;
  const svg = svgEl('svg', {width:'100%', viewBox:`0 0 ${W} ${H}`});
  const n = vals.length, span = (W-padL-padR)/Math.max(n,1);
  const bw = Math.min(24, Math.max(3, span-2));           // 2px surface gap
  const mx = Math.max(...vals.map(Math.abs), 1e-9);
  const y0 = H/2, scale = (H/2-15)/mx;                    // 15px label band each side
  svg.appendChild(svgEl('line', {x1:padL, x2:W-padR, y1:y0, y2:y0, stroke:css('--axis'), 'stroke-width':1}));
  const color = css(colorVar);
  let exI = 0; vals.forEach((v,i)=>{ if(Math.abs(v)>Math.abs(vals[exI])) exI=i; });
  vals.forEach((v,i)=>{
    const x = padL + i*span + (span-bw)/2, h = Math.abs(v)*scale;
    const p = svgEl('path', {d: barPath(x, y0, bw, Math.max(h,1), v>=0), fill: color});
    const hit = svgEl('rect', {x: padL+i*span, y:0, width:span, height:H, fill:'transparent'});
    hit.addEventListener('pointermove', e=>{ p.style.opacity=.75;
      showTT(e.clientX, e.clientY, dates[i], [{color, label, value: fmt(v)}]); });
    hit.addEventListener('pointerleave', ()=>{ p.style.opacity=1; hideTT(); });
    svg.appendChild(p); svg.appendChild(hit);
    if(i===exI && Math.abs(v)>0){
      const ly = Math.max(10, Math.min(H-3, v>=0? y0-h-4 : y0+h+11));
      const t = svgEl('text', {x: Math.max(30, Math.min(W-30, x+bw/2)), y: ly,
        'text-anchor':'middle', 'font-size':10, fill:css('--ink-2')});
      t.textContent = fmt(v); svg.appendChild(t);
    }
  });
  parent.appendChild(svg);
}

// multi-series line chart with crosshair tooltip (every series at the hovered X)
function lineChart(parent, dates, series, fmt){
  const W = Math.min(parent.clientWidth||520, 640), H = 120, padL=8, padR=52, padT=8, padB=16;
  const svg = svgEl('svg', {width:'100%', viewBox:`0 0 ${W} ${H}`});
  const all = series.flatMap(s=>s.values);
  const lo = Math.min(...all), hi = Math.max(...all), rng = (hi-lo)||1e-9;
  const X = i => padL + i*(W-padL-padR)/Math.max(dates.length-1,1);
  const Y = v => padT + (hi-v)*(H-padT-padB)/rng;
  for(const g of [hi, (hi+lo)/2, lo]){
    svg.appendChild(svgEl('line',{x1:padL,x2:W-padR,y1:Y(g),y2:Y(g),stroke:css('--grid'),'stroke-width':1}));
    const t = svgEl('text',{x:W-padR+4,y:Y(g)+3,'font-size':9,fill:css('--muted')});
    t.textContent = fmt(g); svg.appendChild(t);
  }
  series.forEach(s=>{
    const d = s.values.map((v,i)=>(i?'L':'M')+X(i).toFixed(1)+','+Y(v).toFixed(1)).join('');
    svg.appendChild(svgEl('path',{d,fill:'none',stroke:css(s.color),'stroke-width':2,
      'stroke-linejoin':'round','stroke-linecap':'round'}));
    const le = s.values[s.values.length-1];
    svg.appendChild(svgEl('circle',{cx:X(s.values.length-1),cy:Y(le),r:4,fill:css(s.color),
      stroke:css('--surface-1'),'stroke-width':2}));
    const t = svgEl('text',{x:X(s.values.length-1)+7,y:Y(le)+3,'font-size':10,fill:css('--ink-2')});
    t.textContent = s.label; svg.appendChild(t);
  });
  const cross = svgEl('line',{y1:padT,y2:H-padB,stroke:css('--axis'),'stroke-width':1,opacity:0});
  svg.appendChild(cross);
  const hit = svgEl('rect',{x:0,y:0,width:W,height:H,fill:'transparent'});
  hit.addEventListener('pointermove', e=>{
    const r = svg.getBoundingClientRect();
    const fx = (e.clientX-r.left)*(W/r.width);
    const i = Math.max(0, Math.min(dates.length-1, Math.round((fx-padL)/((W-padL-padR)/Math.max(dates.length-1,1)))));
    cross.setAttribute('x1',X(i)); cross.setAttribute('x2',X(i)); cross.setAttribute('opacity',.8);
    showTT(e.clientX,e.clientY,dates[i], series.map(s=>({color:css(s.color),label:s.label,value:fmt(s.values[i])})));
  });
  hit.addEventListener('pointerleave', ()=>{ cross.setAttribute('opacity',0); hideTT(); });
  svg.appendChild(hit);
  parent.appendChild(svg);
}

function spark(vals, w=88, h=26, colorVar='--muted'){
  if(!vals || vals.length<2) return '';
  const lo=Math.min(...vals), hi=Math.max(...vals), rng=(hi-lo)||1e-9;
  const pts = vals.map((v,i)=>((i*(w-6)/(vals.length-1))+2).toFixed(1)+','+(h-3-(v-lo)*(h-8)/rng).toFixed(1));
  const last = pts[pts.length-1].split(',');
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline points="${pts.join(' ')}"
    fill="none" stroke="${css(colorVar)}" stroke-width="1.5"/><circle cx="${last[0]}" cy="${last[1]}" r="3"
    fill="${css('--s1')}" stroke="${css('--surface-1')}" stroke-width="2"/></svg>`;
}

// horizontal diverging z-bars (+ = crowded/warm pole, - = washed-out/cool pole)
function zBars(parent, rows){
  const wrap = document.createElement('div');
  const MAXZ = Math.max(2.5, ...rows.map(r=>Math.abs(r.z??0)));
  for(const r of rows){
    const row = document.createElement('div'); row.className='zrow';
    const lb = document.createElement('div'); lb.className='lb';
    lb.textContent = r.label; lb.title = (r.note||'') + (r.asof? (' as of '+r.asof):'');
    const mid = document.createElement('div');
    const W=100, H=16;
    if(r.z!=null){
      const frac = Math.min(Math.abs(r.z)/MAXZ, 1)*46;
      const x0 = 50, x1 = r.z>=0 ? 50 : 50-frac, wpct = frac;
      mid.innerHTML = `<svg width="100%" height="${H}" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
        <line x1="50" x2="50" y1="1" y2="${H-1}" stroke="${css('--axis')}" stroke-width="1"/>
        <rect x="${x1}" y="3" width="${Math.max(wpct,0.8)}" height="${H-6}" rx="2"
          fill="${css(r.z>=0?'--pos':'--neg')}"/></svg>`;
    } else {
      mid.innerHTML = `<svg width="100%" height="${H}" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
        <line x1="50" x2="50" y1="1" y2="${H-1}" stroke="${css('--axis')}" stroke-width="1"/>
        <circle cx="50" cy="${H/2}" r="2.5" fill="${css('--muted')}"/></svg>`;
    }
    const vv = document.createElement('div'); vv.className='vv';
    vv.innerHTML = `${esc(r.value)} <small>${r.z!=null? 'z '+(r.z>=0?'+':'')+r.z.toFixed(1) : (r.note? esc(r.note):'level')}</small>`;
    row.appendChild(lb); row.appendChild(mid); row.appendChild(vv);
    wrap.appendChild(row);
  }
  parent.appendChild(wrap);
}

// ---------- header / freshness / tabs
$('#gen').textContent = 'generated ' + D.generated + ' - as of ' + D.asof;
$('#contract').textContent = D.contract + '  [evidence groups armed: ' + D.armed_groups.length + '/' + D.groups_total + ' - ' + D.armed_groups.join(', ') + ']';
(function(){
  const el = $('#fresh'); const today = D.asof;
  const staleDays = a => a ? Math.round((new Date(today) - new Date(a))/864e5) : null;
  const seen = new Set();
  for(const f of D.feeds){
    const key = f.name.split(':')[0];
    if(seen.has(key)) continue; seen.add(key);
    const div = document.createElement('span'); div.className='fresh';
    const dot = document.createElement('span'); dot.className='dot';
    const sd = staleDays(f.asof);
    dot.style.background = !f.ok ? css('--critical') : (sd!=null && sd>4 ? css('--warn') : css('--good'));
    div.appendChild(dot);
    div.appendChild(document.createTextNode(key + ' ' + (f.asof || (f.ok?'ok':'FAIL'))));
    div.title = f.note || '';
    el.appendChild(div);
  }
})();

const TABS = [{id:'COMPLEX', label:'Complex'}].concat(D.names_order.map(id=>({id, label: id})));
const want = (new URLSearchParams(location.search)).get('tab') || location.hash.replace('#','');
let current = TABS.some(t=>t.id===want) ? want : 'COMPLEX';
const tabsEl = $('#tabs');
for(const t of TABS){
  const b = document.createElement('button'); b.className='tab'; b.role='tab'; b.id='tab-'+t.id;
  b.textContent = D.names[t.id] ? D.names[t.id].label : t.label;
  b.onclick = ()=>{ current = t.id; location.hash = t.id; render(t.id); };
  tabsEl.appendChild(b);
}

// ---------- building blocks
function chipRow(verdicts, order){
  let h = '<div class="chips">';
  for(const q of order){
    const v = verdicts[q]; if(!v) continue;
    h += `<span class="chip ${esc(v.chip)}" title="${esc(v.headline)}">
      <span class="ic">${CHIP_IC[v.chip]||'○'}</span>
      <span>${q.toUpperCase()}</span><b>${esc(v.verdict)}</b>
      <span class="conf">${esc(v.confidence)}</span></span>`;
  }
  return h + '</div>';
}
function verdictBlock(v){
  let h = `<h3>${esc(v.headline)}</h3>`;
  if(v.evidence && v.evidence.length) h += '<ul class="ev">'+v.evidence.map(e=>`<li>${esc(e)}</li>`).join('')+'</ul>';
  if(v.hypothesis) h += `<div class="hyp"><b>hypothesis</b> — ${esc(v.hypothesis)}</div>`;
  if(v.falsifier) h += `<div class="fals">${esc(v.falsifier)}</div>`;
  return h;
}
function tblView(headers, rows){
  let h = '<details class="tbl"><summary>table</summary><table><tr>';
  h += headers.map(x=>`<th>${esc(x)}</th>`).join('') + '</tr>';
  for(const r of rows) h += '<tr>'+r.map(x=>`<td>${esc(x)}</td>`).join('')+'</tr>';
  return h + '</table></details>';
}
function tiles(st, tag){
  const p = st.px||{}; const us = st.kind==='us';
  const px = p.last==null?'n/a':(us? '$'+p.last.toLocaleString(undefined,{maximumFractionDigits:2}) : p.last.toLocaleString());
  const cls = x => x==null?'':(x>=0?'up':'dn');
  let live = '';
  if(st.live && st.live.ret!=null)
    live = `<div class="tile"><div class="lb">${st.live.is_live?'live session':'last session'}</div>
      <div class="v ${cls(st.live.ret)}">${fmtPct(st.live.ret)}</div><div class="d">${st.live.is_live?'intraday, ~15min delay possible':'completed'}</div></div>`;
  let extra = '';
  if(st.foreign_hold && st.foreign_hold.last!=null)
    extra = `<div class="tile"><div class="lb">foreign ownership</div><div class="v">${st.foreign_hold.last.toFixed(2)}%</div>
      <div class="d">${st.foreign_hold.d20!=null? (st.foreign_hold.d20>=0?'+':'')+st.foreign_hold.d20.toFixed(2)+'pp / 20d':''}</div></div>`;
  return `<div class="tiles">
    <div class="tile"><div class="lb">${tag?esc(tag)+' — ':''}last close (${esc(p.date||'')})</div><div class="v">${px}</div>
      <div class="d ${cls(p.ret1)}">${fmtPct(p.ret1)} 1d</div></div>
    <div class="tile"><div class="lb">5 days</div><div class="v ${cls(p.ret5)}">${fmtPct(p.ret5)}</div>
      <div class="d">z ${p.ret5_z==null?'n/a':(p.ret5_z>=0?'+':'')+p.ret5_z.toFixed(1)}</div></div>
    <div class="tile"><div class="lb">20 days</div><div class="v ${cls(p.ret20)}">${fmtPct(p.ret20)}</div>
      <div class="d">${spark(p.closes20||[])}</div></div>
    ${live}${extra}</div>`;
}

function mocCard(st, host){
  const d3 = st.q3data||{}; const rows = d3.moc_rows||[];
  const card = document.createElement('div'); card.className='card wide';
  card.innerHTML = `<h2>Q3 - who is forced to trade next</h2>` + verdictBlock(st.verdicts.q3);
  if(rows.length){
    const div = document.createElement('div');
    const label = document.createElement('div'); label.className='note';
    div.appendChild(label);
    const slider = document.createElement('input');
    slider.type='range'; slider.min=-3; slider.max=3; slider.step=0.05;
    const start = rows[0].ref_ret!=null? Math.max(-3, Math.min(3, rows[0].ref_ret*100)) : 0;
    slider.value = start.toFixed(2);
    let uniform = false;  // initial table = actual per-row returns (matches the headline)
    const tbl = document.createElement('div');
    const recompute = ()=>{
      const r = parseFloat(slider.value)/100;
      label.textContent = uniform
        ? `scenario: uniform day return ${(r*100).toFixed(2)}% applied to every row (drag)`
        : `at actual ${esc(d3.ref_label||'last')} returns per row — drag the slider to run a uniform what-if`;
      let h = '<table><tr><th>fund</th><th>L</th><th>(L²-L)</th><th>AUM</th><th>day ret</th><th>MOC $</th></tr>';
      let tot = 0;
      for(const row of rows){
        const rr = uniform ? r : (row.ref_ret!=null? row.ref_ret : r);
        const dol = row.k*row.aum*rr; tot += dol;
        h += `<tr class="mocR"><td>${esc(row.etf)}</td><td>${row.L>0?'+':''}${row.L}x</td><td>${row.k}</td>
          <td>${fmtUsd(row.aum)}</td><td>${fmtPct(rr)}</td><td>${fmtUsd(dol,true)}</td></tr>`;
      }
      h += `<tr><td><b>total</b></td><td></td><td></td><td></td><td></td><td><b>${fmtUsd(tot,true)}</b></td></tr></table>`;
      tbl.innerHTML = h;
    };
    slider.oninput = ()=>{ uniform = true; recompute(); }; recompute();
    div.appendChild(slider); div.appendChild(tbl);
    const note = document.createElement('div'); note.className='note';
    note.textContent = 'Rebalance $ = (L²-L) x AUM x day return, same sign as the move, executed into the close (~15:50-16:00 ET). The one flow knowable before it trades. Scenario applies one return to all rows - single-stock funds really track their own name.';
    div.appendChild(note);
    card.appendChild(div);
  }
  if(st.opt && st.opt.gex_per_pct!=null){
    const g = document.createElement('div'); g.className='note';
    const sgn = st.opt.gex_per_pct>0? 'LONG gamma - hedging dampens' : 'SHORT gamma - hedging amplifies';
    g.textContent = `dealer gamma (naive +call/-put convention, LOW confidence): ${sgn}; est ${fmtUsd(st.opt.gex_per_pct,true)}/1% move` +
      (st.opt.gex_flip? `, flip ~${st.opt.gex_flip.toFixed(0)}`:'');
    card.appendChild(g);
  }
  host.appendChild(card);
}

function calendarCard(host){
  const card = document.createElement('div'); card.className='card wide';
  card.innerHTML = '<h2>forced-flow calendar - next ' + D.calendar.length + ' days (ffcal, KST)</h2>';
  const W = 1080, H = 96, colW = W/Math.max(D.calendar.length,1);
  const svg = svgEl('svg',{width:'100%',viewBox:`0 0 ${W} ${H}`});
  const R = {S:3, M:4.5, L:6, XL:8};
  D.calendar.forEach((d,i)=>{
    const x0 = i*colW;
    if(i) svg.appendChild(svgEl('line',{x1:x0,x2:x0,y1:4,y2:H-24,stroke:css('--grid'),'stroke-width':1}));
    const lab = svgEl('text',{x:x0+colW/2,y:H-11,'text-anchor':'middle','font-size':10,fill:css('--ink-2')});
    lab.textContent = d.date.slice(5)+' '+d.dow; svg.appendChild(lab);
    const dn = svgEl('text',{x:x0+colW/2,y:H-1,'text-anchor':'middle','font-size':9,fill:css('--muted')});
    dn.textContent = 'density '+d.density; svg.appendChild(dn);
    const evs = d.events.filter(e=>!e.span);
    const spans = d.events.filter(e=>e.span);
    evs.slice(0,9).forEach((e,j)=>{
      const cx = x0 + 14 + (j%4)*((colW-26)/3.2), cy = 14 + Math.floor(j/4)*20;
      const c = svgEl('circle',{cx,cy,r:R[e.size]||3, fill:css(MKT[e.market]||'--s5'),
        stroke:css('--surface-1'),'stroke-width':2});
      svg.appendChild(c);
    });
    if(spans.length){
      svg.appendChild(svgEl('rect',{x:x0+8,y:H-30,width:colW-16,height:3,rx:1.5,fill:css('--grid')}));
    }
    const hit = svgEl('rect',{x:x0,y:0,width:colW,height:H,fill:'transparent'});
    hit.addEventListener('pointermove', ev=>{
      const rows = d.events.slice(0,10).map(e=>({color:css(MKT[e.market]||'--s5'),
        label:`[${e.size}${e.conf==='deterministic'?'#':e.conf==='confirmed'?' ok':'~'}] ${e.label}`,
        value:e.time||''}));
      showTT(ev.clientX, ev.clientY, d.date+' '+d.dow+' - density '+d.density,
        rows.length? rows : [{label:'no events', value:''}]);
    });
    hit.addEventListener('pointerleave', hideTT);
    svg.appendChild(hit);
  });
  card.appendChild(svg);
  card.insertAdjacentHTML('beforeend', `<div class="legend">
    <span class="it"><span class="sw" style="background:${css('--s1')}"></span>US</span>
    <span class="it"><span class="sw" style="background:${css('--s2')}"></span>KR</span>
    <span class="it"><span class="sw" style="background:${css('--s3')}"></span>TW</span>
    <span class="it"><span class="sw" style="background:${css('--s5')}"></span>EU</span>
    <span class="it"><span class="sw" style="background:${css('--s7')}"></span>both</span>
    <span class="it">dot size = event size S/M/L/XL; band = multi-day window</span></div>`);
  const rows = [];
  for(const d of D.calendar) for(const e of d.events.filter(e=>!e.span))
    rows.push([d.date, e.time||'', e.market, e.size, e.label]);
  card.insertAdjacentHTML('beforeend', tblView(['date','KST','tape','size','event'], rows));
  host.appendChild(card);
}

function flagsCard(host, nameId){
  const fl = D.flags.filter(f=>!nameId || f.name===nameId);
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = '<h2>anomaly flags</h2>';
  if(!fl.length){
    card.insertAdjacentHTML('beforeend',
      `<div class="note">none fired - rules: single |z|>=3 - dual-group |z|>=2 - divergence tells. ` +
      `${D.armed_groups.length}/${D.groups_total} evidence groups armed; more arm as archives accumulate.</div>`);
  } else {
    for(const f of fl){
      card.insertAdjacentHTML('beforeend',
        `<div class="flag">${esc(f.text)}<div class="rl">rule: ${esc(f.rule)} - group: ${esc(f.group)}</div></div>`);
    }
  }
  host.appendChild(card);
}

// ---------- views
function render(id){
  for(const t of TABS) $('#tab-'+t.id).setAttribute('aria-selected', String(t.id===id));
  const host = $('#view'); host.innerHTML = '';
  if(id==='COMPLEX') return renderComplex(host);
  renderName(host, D.names[id]);
}

function renderComplex(host){
  const c = D.complex;
  host.insertAdjacentHTML('beforeend', tiles({px:c.px, kind:'us'}, 'SMH (complex proxy)'));
  host.insertAdjacentHTML('beforeend', chipRow(c.verdicts, ['q3','q4']));
  const grid = document.createElement('div'); grid.className='grid';

  // Asia anchors summary (the measured layer)
  const an = document.createElement('div'); an.className='card wide';
  an.innerHTML = '<h2>Asia measured anchors - the direct cohort layer (leads US by ~12h)</h2>';
  let ah = '<table><tr><th>anchor</th><th>5d</th><th>Q1 attribution (measured)</th><th>Q2 tape</th></tr>';
  for(const a of c.anchors||[])
    ah += `<tr><td>${esc(a.label)}</td><td>${fmtPct(a.ret5)}</td><td style="text-align:left">${esc(a.q1)}</td><td>${esc(a.q2)}</td></tr>`;
  an.insertAdjacentHTML('beforeend', ah+'</table>');
  grid.appendChild(an);

  mocCard(c, grid);
  calendarCard(grid);

  // breadth table
  const br = document.createElement('div'); br.className='card';
  br.innerHTML = `<h2>breadth test</h2><h3>complex-wide vs idiosyncratic (rule: |ret5 - SMH| >= 3%)</h3>`;
  let bh = '<table><tr><th>name</th><th>tape</th><th>5d</th><th>20d</th><th>resid vs SMH</th></tr>';
  for(const r of c.breadth||[])
    bh += `<tr><td>${esc(r.name)}</td><td>${esc(r.tape)}</td><td>${fmtPct(r.ret5)}</td><td>${fmtPct(r.ret20)}</td>
      <td>${r.resid5==null?'n/a':fmtPct(r.resid5)}${r.resid5!=null&&Math.abs(r.resid5)>=0.03?' ⚠':''}</td></tr>`;
  br.insertAdjacentHTML('beforeend', bh+'</table><div class="note">⚠ = idiosyncratic candidate vs SMH - dig. Many ⚠ on one tape = a REGIONAL divergence (e.g. a Korea cascade while the US bounces), which is shared flow on that tape, not single-name information. Largest mover ≠ informed.</div>');
  grid.appendChild(br);

  // crowd card
  const q4 = document.createElement('div'); q4.className='card';
  q4.innerHTML = '<h2>Q4 - where is the crowd</h2>' + verdictBlock(c.verdicts.q4);
  zBars(q4, (c.q4data&&c.q4data.rows)||[]);
  q4.insertAdjacentHTML('beforeend', '<div class="note">+z (warm) = crowded-long direction, -z (cool) = washed-out; equal-weight pre-registered score.</div>');
  grid.appendChild(q4);

  // KR margin chart
  if(c.margin && c.margin.series){
    const mg = document.createElement('div'); mg.className='card';
    mg.innerHTML = `<h2>KR margin balance (KOFIA, market-level)</h2>
      <h3>${fmtKrw(c.margin.level,false)} - z ${(c.margin.z==null?'n/a':(c.margin.z>=0?'+':'')+c.margin.z.toFixed(1))} - as of ${esc(c.margin.asof)}</h3>`;
    const div = document.createElement('div');
    lineChart(div, c.margin.series.dates, [{label:'margin', color:'--s1', values:c.margin.series.total}],
      v=>fmtKrw(v,false));
    mg.appendChild(div);
    mg.insertAdjacentHTML('beforeend','<div class="note">The margin clock: elevated balance + a hard down day arms the 09:00-10:00 KST forced-supply window (ffcal F13 semantics).</div>');
    grid.appendChild(mg);
  }
  flagsCard(grid, null);
  host.appendChild(grid);
}

function renderName(host, st){
  if(!st){ host.textContent = 'no data'; return; }
  host.insertAdjacentHTML('beforeend', tiles(st));
  host.insertAdjacentHTML('beforeend', chipRow(st.verdicts, ['q1','q2','q3','q4','q5']));
  const grid = document.createElement('div'); grid.className='grid';

  // Q1
  const q1 = document.createElement('div'); q1.className='card wide';
  q1.innerHTML = '<h2>Q1 - who owned the recent move</h2>' + verdictBlock(st.verdicts.q1);
  const coh = st.q1data && st.q1data.cohort;
  if(coh){
    q1.insertAdjacentHTML('beforeend', `<div class="legend">` + coh.cohorts.map(c=>
      `<span class="it"><span class="sw" style="background:${css(COH[c.key]||'--s5')}"></span>${esc(c.label)}</span>`).join('') +
      `<span class="it">daily net-buy, last 20 sessions (${esc(coh.unit)})</span></div>`);
    for(const c of coh.cohorts){
      const lab = document.createElement('div'); lab.className='note';
      lab.textContent = `${c.label} - 5d ${fmtAmt(c.cum5, coh.unit)}, 20d ${fmtAmt(c.cum20, coh.unit)}` +
        (c.z5!=null? `, z ${(c.z5>=0?'+':'')+c.z5.toFixed(1)}`:'') + `, streak ${c.streak>0?'+':''}${c.streak}d`;
      q1.appendChild(lab);
      const div = document.createElement('div');
      barChart(div, coh.dates, c.daily20, COH[c.key]||'--s5', v=>fmtAmt(v, coh.unit), c.label);
      q1.appendChild(div);
    }
    q1.insertAdjacentHTML('beforeend', tblView(['date'].concat(coh.cohorts.map(c=>c.label)),
      coh.dates.map((d,i)=>[d].concat(coh.cohorts.map(c=>fmtAmt(c.daily20[i], coh.unit))))));
  }
  if(st.px && st.px.on20 && st.kind==='us'){
    q1.insertAdjacentHTML('beforeend','<div class="sect">overnight vs intraday - cumulative 20d (clientele diagnostic)</div>' +
      `<div class="legend"><span class="it"><span class="ln" style="background:${css('--s1')}"></span>overnight (gap: global/institutional hours)</span>` +
      `<span class="it"><span class="ln" style="background:${css('--s8')}"></span>intraday (US session flow)</span></div>`);
    const cum = a => a.reduce((acc,v)=>{acc.push((acc.length?acc[acc.length-1]:0)+v);return acc;},[]);
    const div = document.createElement('div');
    lineChart(div, st.px.dates20, [
      {label:'overnight', color:'--s1', values:cum(st.px.on20)},
      {label:'intraday', color:'--s8', values:cum(st.px.id20)}], v=>fmtPct(v));
    q1.appendChild(div);
    q1.insertAdjacentHTML('beforeend', tblView(['date','overnight','intraday'],
      st.px.dates20.map((d,i)=>[d, fmtPct(st.px.on20[i]), fmtPct(st.px.id20[i])])));
  }
  const svr = st.q1data && st.q1data.svr;
  if(svr){
    q1.insertAdjacentHTML('beforeend', `<div class="sect">FINRA short-volume ratio (30d)</div>
      <div class="tiles"><div class="tile"><div class="lb">latest ratio</div>
      <div class="v">${(svr.ratio[svr.ratio.length-1]*100).toFixed(0)}%</div>
      <div class="d">z ${svr.z==null?'n/a':(svr.z>=0?'+':'')+svr.z.toFixed(1)} - liquidity-provision mix, weak cohort signal</div></div>
      <div class="tile"><div class="lb">30d path</div><div class="v">${spark(svr.ratio)}</div></div></div>`);
  }
  grid.appendChild(q1);

  // Q2
  const q2 = document.createElement('div'); q2.className='card';
  q2.innerHTML = '<h2>Q2 - whose shares am I buying</h2>' + verdictBlock(st.verdicts.q2);
  q2.insertAdjacentHTML('beforeend','<div class="note">forced seller (cascade, margin clock) = favorable - informed distributor (selling strength into retail absorption) = adverse.</div>');
  grid.appendChild(q2);

  // Q4
  const q4 = document.createElement('div'); q4.className='card';
  q4.innerHTML = '<h2>Q4 - where is the crowd</h2>' + verdictBlock(st.verdicts.q4);
  zBars(q4, (st.q4data&&st.q4data.rows)||[]);
  grid.appendChild(q4);

  // Q3
  mocCard(st, grid);

  // Q5
  const q5 = document.createElement('div'); q5.className='card wide';
  q5.innerHTML = '<h2>Q5 - what is already priced</h2>' + verdictBlock(st.verdicts.q5);
  const d5 = st.q5data||{};
  let t5 = '<div class="tiles">';
  if(d5.earnings && d5.earnings.date)
    t5 += `<div class="tile"><div class="lb">next earnings</div><div class="v">${d5.earnings.days}d</div>
      <div class="d">${esc(d5.earnings.date)}</div></div>`;
  if(d5.implied)
    t5 += `<div class="tile"><div class="lb">straddle-implied (${esc(d5.implied.expiry)})</div>
      <div class="v">${fmtPct(d5.implied.move,1,false)}</div><div class="d">${d5.implied.days}d window, ATM ${d5.implied.strike}</div></div>`;
  if(d5.realized)
    t5 += `<div class="tile"><div class="lb">realized reaction avg (${d5.realized.n})</div>
      <div class="v">${fmtPct(d5.realized.avg_abs,1,false)}</div><div class="d">|close-to-close| after print</div></div>`;
  if(d5.runup && d5.runup.ret20!=null)
    t5 += `<div class="tile"><div class="lb">run-up 20d</div><div class="v">${fmtPct(d5.runup.ret20)}</div>
      <div class="d">${d5.runup.resid20==null?'':fmtPct(d5.runup.resid20)+' vs SMH'}</div></div>`;
  t5 += '</div>';
  q5.insertAdjacentHTML('beforeend', t5);
  if(d5.implied && d5.realized){
    const W=520,H=64;
    const mx = Math.max(d5.implied.move, d5.realized.avg_abs)*1.25;
    const bw = 18, x0=150;
    const len = v => (W-x0-70)*v/mx;
    q5.insertAdjacentHTML('beforeend', `<div class="legend">
      <span class="it"><span class="sw" style="background:${css('--s1')}"></span>implied (event straddle)</span>
      <span class="it"><span class="sw" style="background:${css('--seq-250')}"></span>realized avg |move|</span></div>
      <svg width="100%" viewBox="0 0 ${W} ${H}">
      <line x1="${x0}" x2="${x0}" y1="4" y2="${H-4}" stroke="${css('--axis')}" stroke-width="1"/>
      <text x="${x0-8}" y="22" text-anchor="end" font-size="11" fill="${css('--ink-2')}">implied</text>
      <path d="${barPathH(x0, 12, len(d5.implied.move), bw)}" fill="${css('--s1')}"/>
      <text x="${x0+len(d5.implied.move)+6}" y="25" font-size="11" fill="${css('--ink-2')}">${fmtPct(d5.implied.move,1,false)}</text>
      <text x="${x0-8}" y="48" text-anchor="end" font-size="11" fill="${css('--ink-2')}">realized</text>
      <path d="${barPathH(x0, 38, len(d5.realized.avg_abs), bw)}" fill="${css('--seq-250')}"/>
      <text x="${x0+len(d5.realized.avg_abs)+6}" y="51" font-size="11" fill="${css('--ink-2')}">${fmtPct(d5.realized.avg_abs,1,false)}</text>
      </svg>
      <div class="note">implied includes ambient drift over the window - a fair comparison needs the event-isolated move; treat gaps below ~1.3x as noise.</div>`);
  }
  if(d5.rev30 && Object.keys(d5.rev30).length){
    const rows = Object.entries(d5.rev30).map(([k,v])=>[k, fmtPct(v,1)]);
    q5.insertAdjacentHTML('beforeend', '<div class="sect">EPS estimate drift, 30 days</div>'+
      tblView(['period','change'], rows));
  }
  grid.appendChild(q5);

  flagsCard(grid, st.id);
  host.appendChild(grid);
}

function barPathH(x, y, w, h){
  const r = Math.min(4, h/2, Math.max(w,1));
  if(w<=1) return `M${x},${y}h1v${h}h-1Z`;
  return `M${x},${y}h${w-r}q${r},0 ${r},${r}v${h-2*r}q0,${r} ${-r},${r}h${-(w-r)}Z`;
}

render(current);
</script>
</body>
</html>
"""
