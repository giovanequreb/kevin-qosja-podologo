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

/* Highlight today's row in the opening hours */
document.querySelectorAll('.hours tbody').forEach((body) => {
  const rows = body.querySelectorAll('tr');
  if (rows.length === 7) rows[(new Date().getDay() + 6) % 7].classList.add('is-today');
});

/* Plantar pressure map: an illustrative footprint drawn as a heat field */
const ASPECT = 1.5;
// x, y, radius (in canvas widths), moment of the step when it carries the load
const BLOBS = [
  [.50, .84, .17, 0],
  [.60, .62, .095, .18],
  [.62, .49, .09, .28],
  [.36, .31, .14, .45],
  [.54, .28, .13, .45],
  [.69, .33, .10, .42],
  [.29, .10, .07, .62],
  [.45, .065, .048, .64],
  [.56, .075, .043, .65],
  [.66, .105, .04, .66],
  [.745, .15, .036, .67],
];
const STOPS = [[0, [30, 48, 110]], [.3, [61, 119, 245]], [.55, [140, 180, 255]], [.8, [214, 229, 255]], [1, [255, 255, 255]]];
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
  LUT[i * 4 + 3] = edge * edge * (3 - 2 * edge) * 240;
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
    BLOBS.forEach(([, , , phase], i) => {
      let d = Math.abs(t - phase);
      d = Math.min(d, 1 - d);
      weights[i] = .3 + .7 * Math.exp(-(d * d) / .065);
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

  new ResizeObserver(() => { resize(); draw(reduceMotion ? 2340 : last); }).observe(canvas);
  if (!reduceMotion) {
    new IntersectionObserver(([e]) => {
      const was = visible;
      visible = e.isIntersecting;
      if (visible && !was) requestAnimationFrame(loop);
    }).observe(canvas);
  }
}

document.querySelectorAll('canvas[data-foot]').forEach(pressureMap);
