/* ------------------------------------------------------------------
   app.js — interaction layer for the Paper Portfolio pages.

   Mirrors the behaviour of the reference build:
     · Locomotive Scroll (smooth virtual scroll) with a native fallback
     · GSAP timeline reveals
     · Sticky, auto-hiding navigation
     · Paper-fold menu overlay (Index / Work / About)
     · Butter-style inertial horizontal slider for the work list
     · Infinite marquee
     · Procedural paper grain + column grid overlay
   ------------------------------------------------------------------ */
(function () {
  'use strict';

  var INK = '#1D1D1B';
  var PAPER = '#E8E3DA';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ----------------------------------------------------------------
     1. Paper grain
     A cheap tiled noise texture painted once into a canvas and used
     as a repeating background. Keeps the pages light while matching
     the fibrous paper look of the design.
     ---------------------------------------------------------------- */
  function paperGrain() {
    var size = 180;
    var c = document.createElement('canvas');
    c.width = c.height = size;
    var x = c.getContext('2d');
    var img = x.createImageData(size, size);
    var d = img.data;
    for (var i = 0; i < d.length; i += 4) {
      // Fibrous vertical bias + fine speckle.
      var n = 236 + Math.random() * 19;
      var speck = Math.random() < 0.006 ? 40 : 0;
      d[i] = n - speck;
      d[i + 1] = n - speck;
      d[i + 2] = n - speck - 3;
      d[i + 3] = 26 + Math.random() * 26;
    }
    x.putImageData(img, 0, 0);
    return c.toDataURL('image/png');
  }

  function applyPaper() {
    var url = paperGrain();
    $$('.paper-background, body').forEach(function (el) {
      el.style.backgroundImage = 'url(' + url + ')';
    });
    document.documentElement.style.setProperty('--paper-grain', 'url(' + url + ')');
  }

  /* ----------------------------------------------------------------
     2. Smooth scroll
     ---------------------------------------------------------------- */
  var scroller = null;
  var hasLoco = false;

  function initScroll() {
    if (reduce || !window.locomotiveScroll) return;
    $$('[data-scroll]').forEach(function (el) { el.removeAttribute('data-scroll'); });
    $$('[data-scroll-sticky]').forEach(function (el) { el.removeAttribute('data-scroll-sticky'); });
    try {
      scroller = new window.locomotiveScroll({
        el: document.querySelector('[data-scroll-container]') || document.querySelector('#app'),
        smooth: true,
        lerp: 0.09,
        multiplier: 1,
        smartphone: { smooth: false },
        tablet: { smooth: false }
      });
      hasLoco = true;
    } catch (e) {
      scroller = null;
    }
  }

  function scrollTo(y) {
    if (hasLoco) scroller.scrollTo(y, { duration: 900, disableLerp: true });
    else window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
  }

  /* ----------------------------------------------------------------
     3. Navigation — sticky, hides on scroll down, returns on up
     ---------------------------------------------------------------- */
  function initNav() {
    var nav = $('.nav');
    if (!nav) return;
    var last = 0;
    var hide = function (y, dir) {
      if ($('.nav').classList.contains('menu-open')) return;
      var showing = dir === 'up' || y < 40;
      nav.classList.toggle('is-hidden', !showing);
    };
    if (hasLoco) {
      scroller.on('scroll', function (e) {
        var y = e.scroll.y;
        var dir = y > last ? 'down' : 'up';
        if (Math.abs(y - last) > 4) hide(y, dir);
        last = y;
      });
    } else {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          var y = window.pageYOffset;
          hide(y, y > last ? 'down' : 'up');
          last = y;
          ticking = false;
        });
      }, { passive: true });
    }
  }

  /* ----------------------------------------------------------------
     4. Paper-fold menu
     ---------------------------------------------------------------- */
  function initMenu() {
    var nav = $('.nav');
    var menu = $('.menu');
    var trigger = $('.nav-link');
    if (!nav || !menu || !trigger) return;
    var open = false;

    var setOpen = function (next) {
      if (open === next) return;
      open = next;
      nav.classList.toggle('menu-open', open);
      if (open) {
        menu.style.display = 'flex';
        requestAnimationFrame(function () { menu.classList.add('is-open'); });
        // Stagger the three menu titles in.
        $$('.menu-title', menu).forEach(function (t, i) {
          t.style.transitionDelay = (0.06 + i * 0.07) + 's';
        });
      } else {
        menu.classList.remove('is-open');
        $$('.menu-title', menu).forEach(function (t) { t.style.transitionDelay = '0s'; });
        setTimeout(function () { if (!open) menu.style.display = 'none'; }, 520);
      }
      if (typeof window.locomotiveScroll !== 'undefined' && hasLoco) scroller.stop();
      else document.body.classList.toggle('no-scroll', open);
    };

    trigger.addEventListener('click', function () { setOpen(!open); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });

    $$('.menu-link', menu).forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var href = a.getAttribute('href');
        if (!href) return;
        var move = function () { window.location.href = href; };
        if (hasLoco && !reduce) { scroller.stop(); setTimeout(move, 420); }
        else move();
      });
    });

    // If the viewport grows past the mobile breakpoint, never trap scroll.
    window.addEventListener('resize', function () {
      if (open && window.innerWidth > 991) setOpen(false);
    });
  }

  /* ----------------------------------------------------------------
     5. Inertial horizontal slider (Butter-compatible)
     Falls back to a self-contained pointer-inertia implementation when
     the butter-slider bundle is unavailable.
     ---------------------------------------------------------------- */
  function initSlider() {
    var container = $('[data-butter-container]');
    var slidable = $('[data-butter-slidable]');
    if (!container || !slidable) return;

    if (window.Butter && typeof window.Butter === 'function') {
      try {
        var opts = (container.getAttribute('data-butter-butter-options') || '')
          .split(',').reduce(function (acc, pair) {
            var kv = pair.split(':');
            if (kv.length === 2) acc[kv[0].trim()] = isNaN(+kv[1]) ? kv[1].trim() : +kv[1];
            return acc;
          }, {});
        new window.Butter({
          container: container,
          slidable: slidable,
          inertia: true,
          inertiaMultiplier: opts.dragSpeed || 2.5,
          swipeable: true,
          resistance: 300 / (opts.smoothAmount || 0.15)
        });
        return;
      } catch (e) { /* fall through to the native implementation */ }
    }

    // Native fallback: pointer drag with inertial glide.
    var max = function () { return Math.max(0, slidable.scrollWidth - container.clientWidth); };
    var x = 0, target = 0, dragging = false, startX = 0, startT = 0, v = 0;
    var ease = function () {
      x += (target - x) * (reduce ? 1 : 0.12);
      if (Math.abs(target - x) < 0.4 && !dragging) {
        x = target;
        v = 0;
        slidable.style.transform = '';
        return;
      }
      if (v) { target += v; v *= 0.94; }
      slidable.style.transform = 'translate3d(' + (-x) + 'px,0,0)';
      requestAnimationFrame(ease);
    };
    ease();

    container.addEventListener('pointerdown', function (e) {
      dragging = true; startX = e.clientX; startT = Date.now(); v = 0;
      target = x;
      container.setPointerCapture(e.pointerId);
    });
    container.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var now = Date.now();
      var dx = e.clientX - startX;
      var m = max();
      var next = x - dx;
      if (next < 0) next /= 3; else if (next > m) m + (next - m) / 3;
      v = (x - next) / Math.max(1, now - startT) * 16;
      x = next;
      startX = e.clientX; startT = now;
    });
    var end = function () {
      if (!dragging) return;
      dragging = false;
      v = -v * 0.6;
      target = Math.min(max(), Math.max(0, x));
    };
    container.addEventListener('pointerup', end);
    container.addEventListener('pointercancel', end);
    container.addEventListener('pointerleave', end);
  }

  /* ----------------------------------------------------------------
     6. Marquee
     ---------------------------------------------------------------- */
  function initMarquee() {
    var inner = $('.marquee--inner');
    var track = $('.marquee', $('.footer') || document);
    if (!inner || !track || reduce) return;
    var x = 0;
    var one = inner.getBoundingClientRect().width / 3;
    if (!one) return;
    var tick = function () {
      x -= 0.6;
      if (x <= -one) x += one;
      inner.style.transform = 'translate3d(' + x + 'px,0,0)';
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ----------------------------------------------------------------
     7. Reveal + parallax
     ---------------------------------------------------------------- */
  function initReveals() {
    if (!window.gsap) return;
    var gsap = window.gsap;

    // Per-word rise for the large editorial headings.
    $$('[data-words]').forEach(function (el) {
      var words = el.textContent.trim().split(/\s+/);
      el.innerHTML = words.map(function (w) {
        return '<span class="w-words" style="display:inline-block;overflow:hidden;vertical-align:top">' +
               '<span style="display:inline-block;transform:translateY(105%)">' + w + '</span>' +
               '</span>';
      }).join(' ');
      gsap.fromTo(el.querySelectorAll('.w-words > span'),
        { yPercent: 105 },
        { yPercent: 0, duration: 1.1, ease: 'power4.out', stagger: 0.035, delay: 0.15 });
    });

    // Fade/rise as blocks enter the viewport, driven by whichever
    // scroll implementation ended up active.
    var items = $$('[data-reveal]');
    if (!items.length) return;

    var show = function (el) {
      if (el.__shown) return;
      el.__shown = true;
      gsap.to(el, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' });
    };

    if (hasLoco) {
      gsap.set(items, { opacity: 0, y: 40 });
      scroller.on('scroll', function (e) {
        items.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight * 0.9 && r.bottom > 0) show(el);
        });
        void e;
      });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } });
      }, { rootMargin: '0px 0px -12% 0px' });
      items.forEach(function (el) { io.observe(el); });
    }

    // Slow drift on the oversized project artwork.
    if (!reduce) {
      $$('[data-drift]').forEach(function (el) {
        var amt = parseFloat(el.getAttribute('data-drift')) || 8;
        gsap.to(el, { yPercent: amt, ease: 'none' });
      });
    }
  }

  /* ----------------------------------------------------------------
     8. Grid overlay
     ---------------------------------------------------------------- */
  function initGrid() {
    var grid = $('.grid');
    if (!grid) return;
    var show = false;
    document.addEventListener('keydown', function (e) {
      if (e.key === 'g' || e.key === 'G') { show = !show; grid.style.opacity = show ? '1' : '0'; }
    });
  }

  /* ----------------------------------------------------------------
     9. Case-page gallery
     ---------------------------------------------------------------- */
  function initGallery() {
    var overlay = $('.gallery-overlay');
    if (!overlay) return;
    var close = function () { overlay.classList.remove('is-open'); };
    $$('[data-gallery-item]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var src = btn.getAttribute('data-gallery-item');
        var cap = btn.getAttribute('data-gallery-caption') || '';
        var img = $('img', overlay);
        if (img) { img.src = src; img.alt = cap; }
        var c = $('.gallery-cap', overlay);
        if (c) c.textContent = cap;
        overlay.classList.add('is-open');
      });
    });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.closest('.gallery-close')) close();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  /* ----------------------------------------------------------------
     10. Next-project paging
     ---------------------------------------------------------------- */
  function initPaging() {
    $$('[data-next]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        if (hasLoco && !reduce) {
          scroller.scrollTo(0, { duration: 700, disableLerp: true });
          setTimeout(function () { window.location.href = a.getAttribute('href'); }, 480);
        } else {
          window.location.href = a.getAttribute('href');
        }
      });
    });
  }

  /* ----------------------------------------------------------------
     Boot
     ---------------------------------------------------------------- */
  function boot() {
    applyPaper();
    initScroll();
    initNav();
    initMenu();
    initSlider();
    initMarquee();
    initReveals();
    initGrid();
    initGallery();
    initPaging();
    document.documentElement.classList.add('is-ready');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
