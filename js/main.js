const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Menu */
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav');

if (burger && nav) {
  const setOpen = (open) => {
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  };
  burger.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      setOpen(false);
      burger.focus();
    }
  });
}

/* Header gets out of the way while reading, comes back on scroll up */
const header = document.querySelector('.header');
const dock = document.querySelector('.dock');
let lastY = scrollY;
addEventListener('scroll', () => {
  const y = scrollY;
  const menuOpen = nav && nav.classList.contains('is-open');
  header.classList.toggle('is-hidden', y > lastY && y > 400 && !menuOpen);
  if (dock) dock.classList.toggle('is-visible', y > 380);
  lastY = y;
}, { passive: true });

const year = document.querySelector('[data-year]');
if (year) year.textContent = new Date().getFullYear();

/* Scroll reveal */
const revealer = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      revealer.unobserve(e.target);
    }
  }
}, { rootMargin: '0px 0px 12% 0px' });
document.querySelectorAll('[data-reveal]').forEach((el) => revealer.observe(el));

/* Pointer spotlight on cards */
document.querySelectorAll('.card').forEach((card) => {
  card.addEventListener('pointermove', (e) => {
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', `${e.clientX - r.left}px`);
    card.style.setProperty('--my', `${e.clientY - r.top}px`);
  });
});

/* Highlight today's row in the opening hours */
const rows = document.querySelectorAll('.hours tbody tr');
if (rows.length === 7) rows[(new Date().getDay() + 6) % 7].classList.add('is-today');

/* Plantar pressure map: an illustrative footprint drawn as a heat field */
const ASPECT = 1.5;
// x, y, radius (in canvas widths), zone, moment of the step when it carries the load
const BLOBS = [
  [.50, .84, .17, 'tallone', 0],
  [.60, .62, .095, 'arco', .18],
  [.62, .49, .09, 'arco', .28],
  [.36, .31, .14, 'avampiede', .45],
  [.54, .28, .13, 'avampiede', .45],
  [.69, .33, .10, 'avampiede', .42],
  [.29, .10, .07, 'dita', .62],
  [.45, .065, .048, 'dita', .64],
  [.56, .075, .043, 'dita', .65],
  [.66, .105, .04, 'dita', .66],
  [.745, .15, .036, 'dita', .67],
];
const STOPS = [[0, [10, 40, 36]], [.3, [20, 150, 128]], [.55, [200, 255, 77]], [.8, [255, 244, 170]], [1, [255, 255, 255]]];
// Posterised into bands, like the printout of a real pressure platform
const BANDS = 9;
const LUT = new Uint8ClampedArray(256 * 4);
for (let i = 0; i < 256; i++) {
  const raw = i / 255;
  const step = Math.min(1, ((raw * BANDS) % 1) / .12);
  const v = Math.min(1, (Math.floor(raw * BANDS) + step * step * (3 - 2 * step)) / BANDS);
  let s = 0;
  while (s < STOPS.length - 2 && v > STOPS[s + 1][0]) s++;
  const [a, ca] = STOPS[s];
  const [b, cb] = STOPS[s + 1];
  const k = Math.min(1, Math.max(0, (v - a) / (b - a)));
  const edge = Math.min(1, Math.max(0, (raw - .06) / .12));
  for (let c = 0; c < 3; c++) LUT[i * 4 + c] = ca[c] + (cb[c] - ca[c]) * k;
  LUT[i * 4 + 3] = edge * edge * (3 - 2 * edge) * 235;
}

function pressureMap(canvas) {
  const small = matchMedia('(max-width: 700px)').matches;
  const W = small ? 110 : 180;
  const H = W * ASPECT;
  const buf = document.createElement('canvas');
  buf.width = W;
  buf.height = H;
  const bctx = buf.getContext('2d');
  const img = bctx.createImageData(W, H);
  const ctx = canvas.getContext('2d');
  const weights = new Float32Array(BLOBS.length);
  let zone = null;
  let touch = null;
  let visible = false;
  let last = 0;

  const resize = () => {
    const r = canvas.getBoundingClientRect();
    const d = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(r.width * d);
    canvas.height = Math.round(r.height * d);
  };

  const draw = (ms) => {
    const t = (ms / 5200) % 1;
    BLOBS.forEach(([, , , z, phase], i) => {
      if (zone) {
        weights[i] = z === zone ? .85 + .15 * Math.sin(ms / 350) : .2;
      } else {
        let d = Math.abs(t - phase);
        d = Math.min(d, 1 - d);
        weights[i] = .3 + .7 * Math.exp(-(d * d) / .065);
      }
    });
    if (touch) touch.life *= .95;

    for (let y = 0, p = 0; y < H; y++) {
      const py = (y + .5) / W;
      for (let x = 0; x < W; x++, p += 4) {
        const px = (x + .5) / W;
        let v = 0;
        for (let i = 0; i < BLOBS.length; i++) {
          const b = BLOBS[i];
          const dx = px - b[0];
          const dy = py - b[1] * ASPECT;
          const d2 = dx * dx + dy * dy;
          const r2 = b[2] * b[2];
          if (d2 < r2 * 8) v += weights[i] * Math.exp(-d2 / r2);
        }
        if (touch) {
          const dx = px - touch.x;
          const dy = py - touch.y;
          v += touch.life * .8 * Math.exp(-(dx * dx + dy * dy) / .008);
        }
        const o = Math.min(255, (v * 210) | 0) * 4;
        img.data[p] = LUT[o];
        img.data[p + 1] = LUT[o + 1];
        img.data[p + 2] = LUT[o + 2];
        img.data[p + 3] = LUT[o + 3];
      }
    }
    bctx.putImageData(img, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(buf, 0, 0, canvas.width, canvas.height);
  };

  const loop = (ms) => {
    if (!visible) return;
    requestAnimationFrame(loop);
    if (ms - last < (small ? 50 : 33)) return;
    last = ms;
    draw(ms);
  };

  canvas.addEventListener('pointermove', (e) => {
    const r = canvas.getBoundingClientRect();
    touch = { x: (e.clientX - r.left) / r.width, y: ((e.clientY - r.top) / r.height) * ASPECT, life: 1 };
  });

  // Tapping the print picks the nearest zone
  canvas.addEventListener('click', (e) => {
    const r = canvas.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = ((e.clientY - r.top) / r.height) * ASPECT;
    let best = null;
    let bestD = 2.2;
    for (const b of BLOBS) {
      const d = Math.hypot(x - b[0], y - b[1] * ASPECT) / b[2];
      if (d < bestD) { bestD = d; best = b[3]; }
    }
    if (best) canvas.dispatchEvent(new CustomEvent('zone', { detail: best }));
  });

  new ResizeObserver(() => { resize(); draw(reduceMotion ? 2340 : last); }).observe(canvas);
  if (!reduceMotion) {
    new IntersectionObserver(([e]) => {
      const was = visible;
      visible = e.isIntersecting;
      if (visible && !was) requestAnimationFrame(loop);
    }).observe(canvas);
  }

  return {
    setZone(z) {
      zone = z;
      if (reduceMotion) draw(2340);
    },
  };
}

const maps = new Map();
document.querySelectorAll('canvas[data-foot]').forEach((c) => maps.set(c, pressureMap(c)));

/* "Dove senti fastidio?" finder */
const finder = document.querySelector('[data-finder]');
if (finder) {
  const chips = finder.querySelectorAll('.chip');
  const panels = finder.querySelectorAll('[data-panel]');
  const footCanvas = finder.querySelector('canvas[data-foot]');
  const map = maps.get(footCanvas);
  footCanvas.addEventListener('zone', (e) => {
    const chip = finder.querySelector(`.chip[data-zone="${e.detail}"]`);
    if (chip && chip.getAttribute('aria-pressed') !== 'true') chip.click();
  });
  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const on = chip.getAttribute('aria-pressed') !== 'true';
      chips.forEach((c) => c.setAttribute('aria-pressed', String(on && c === chip)));
      panels.forEach((p) => { p.hidden = p.dataset.panel !== (on ? chip.dataset.zone : 'intro'); });
      if (map) map.setZone(on ? chip.dataset.blob : null);
    });
  });
}

/* Service filter, animated with same-document view transitions */
const filter = document.querySelector('[data-filter]');
if (filter) {
  const chips = filter.querySelectorAll('.chip');
  const items = document.querySelectorAll('.card[data-cat]');
  const root = document.documentElement;
  items.forEach((el, i) => { el.style.viewTransitionName = `svc-${i}`; });
  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const cat = chip.dataset.show;
      const apply = () => {
        chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
        items.forEach((el) => {
          el.classList.add('in');
          el.hidden = cat !== 'tutti' && !el.dataset.cat.split(' ').includes(cat);
        });
      };
      if (document.startViewTransition && !reduceMotion) {
        root.classList.add('filtering');
        const vt = document.startViewTransition(apply);
        // a skipped transition (hidden tab, rapid clicks) still applies the filter
        vt.ready.catch(() => {});
        vt.finished.catch(() => {}).finally(() => root.classList.remove('filtering'));
      } else {
        apply();
      }
    });
  });
}
