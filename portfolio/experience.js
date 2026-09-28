(() => {
  'use strict';
  document.fonts.load('16px Canopee').then(fonts => {
    if (fonts.length) document.documentElement.classList.add('has-display-font');
  }).catch(() => { /* The bundled fallback remains available offline. */ });
  const viewport = document.querySelector('.experience-viewport');
  const cards = [...document.querySelectorAll('.experience-card')];
  const buttons = cards.map(card => card.querySelector('.experience-spine'));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const count = document.querySelector('.experience-count');
  let current = 0, hoverTimer, revealTimer, drag = null, dragged = false;
  const menu = document.querySelector('.experience-menu');
  const menuButton = document.querySelector('.rail-menu');

  function reveal(index) {
    const card = cards[index];
    const left = card.offsetLeft;
    const right = left + card.offsetWidth;
    let to = viewport.scrollLeft;
    if (left < to) to = left;
    else if (right > to + viewport.clientWidth) to = right - viewport.clientWidth;
    viewport.scrollTo({left: Math.max(0, to), behavior: reduced.matches ? 'instant' : 'smooth'});
  }
  function updateControls() {
    count.textContent = `${String(current + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
    document.querySelector('[data-step="-1"]').disabled = current === 0;
    document.querySelector('[data-step="1"]').disabled = current === cards.length - 1;
  }
  function activate(index, focus = false) {
    clearTimeout(hoverTimer);
    clearTimeout(revealTimer);
    current = Math.max(0, Math.min(cards.length - 1, index));
    cards.forEach((card, i) => {
      card.classList.toggle('is-active', i === current);
      buttons[i].setAttribute('aria-expanded', String(i === current));
      card.querySelector('.experience-panel').inert = i !== current;
    });
    updateControls();
    if (focus) buttons[current].focus({preventScroll: true});
    revealTimer = setTimeout(() => reveal(current), reduced.matches ? 0 : 850);
  }
  buttons.forEach((button, i) => {
    button.addEventListener('click', () => { if (!dragged) activate(i); });
    button.addEventListener('pointerenter', e => {
      if (e.pointerType === 'mouse' && !drag && i !== current) {
        hoverTimer = setTimeout(() => activate(i), 160);
      }
    });
    button.addEventListener('pointerleave', () => clearTimeout(hoverTimer));
  });
  viewport.addEventListener('keydown', e => {
    let next;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = current + 1;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = current - 1;
    if (e.key === 'Home') next = 0;
    if (e.key === 'End') next = cards.length - 1;
    if (next !== undefined) { e.preventDefault(); activate(next, true); }
  });
  document.querySelectorAll('[data-step]').forEach(button => {
    button.addEventListener('click', () => activate(current + Number(button.dataset.step)));
  });
  viewport.addEventListener('wheel', e => {
    // Preserve native horizontal trackpad gestures; map a mouse wheel sideways.
    if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    e.preventDefault();
    clearTimeout(hoverTimer);
    clearTimeout(revealTimer);
    viewport.scrollLeft += e.deltaY * (e.deltaMode === 1 ? 20 : e.deltaMode === 2 ? viewport.clientWidth : 1);
  }, {passive: false});
  viewport.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    clearTimeout(revealTimer);
    dragged = false;
    drag = {x: e.clientX, left: viewport.scrollLeft, id: e.pointerId};
  });
  viewport.addEventListener('pointermove', e => {
    if (!drag) return;
    const delta = e.clientX - drag.x;
    if (Math.abs(delta) > 5) {
      dragged = true;
      clearTimeout(hoverTimer);
      viewport.setPointerCapture(e.pointerId);
      viewport.classList.add('is-dragging');
      viewport.scrollLeft = drag.left - delta;
    }
  });
  function endDrag() {
    if (drag && viewport.hasPointerCapture(drag.id)) viewport.releasePointerCapture(drag.id);
    drag = null;
    viewport.classList.remove('is-dragging');
    setTimeout(() => { dragged = false; }, 0);
  }
  window.addEventListener('pointerup', endDrag);
  viewport.addEventListener('pointercancel', endDrag);
  function setMenu(open) {
    menu.hidden = !open;
    menu.inert = !open;
    viewport.inert = open;
    document.querySelector('.experience-controls').inert = open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (open) menu.querySelector('a').focus();
    else menuButton.focus();
  }
  menuButton.addEventListener('click', () => setMenu(menu.hidden));
  document.addEventListener('keydown', e => {
    if (menu.hidden) return;
    if (e.key === 'Escape') setMenu(false);
    if (e.key === 'Tab') {
      const stops = [menuButton, ...menu.querySelectorAll('a')];
      const index = stops.indexOf(document.activeElement);
      e.preventDefault();
      stops[(index + (e.shiftKey ? -1 : 1) + stops.length) % stops.length].focus();
    }
  });
  window.addEventListener('resize', () => { clearTimeout(revealTimer); revealTimer = setTimeout(() => reveal(current), 150); });
  updateControls();
})();
