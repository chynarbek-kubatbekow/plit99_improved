document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.nav');
  const scrollTopBtn = document.querySelector('.scroll-top');

  const onScroll = () => {
    nav?.classList.toggle('scrolled', window.scrollY > 20);
    scrollTopBtn?.classList.toggle('visible', window.scrollY > 400);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const burger = document.getElementById('nav-burger') || document.querySelector('.nav-burger');
  const mobileNav = document.getElementById('nav-mobile') || document.querySelector('.nav-mobile');
  const spans = burger?.querySelectorAll('span');

  function closeMobileNav() {
    mobileNav?.classList.remove('open');
    burger?.setAttribute('aria-expanded', 'false');
    if (spans) {
      spans[0].style.transform = '';
      spans[1].style.opacity = '';
      spans[2].style.transform = '';
    }
    document.body.style.overflow = '';
  }

  burger?.addEventListener('click', () => {
    const open = mobileNav?.classList.toggle('open');
    burger?.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (spans) {
      spans[0].style.transform = open ? 'rotate(45deg) translate(5px,5px)' : '';
      spans[1].style.opacity = open ? '0' : '';
      spans[2].style.transform = open ? 'rotate(-45deg) translate(5px,-5px)' : '';
    }
    document.body.style.overflow = open ? 'hidden' : '';
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-burger') && !e.target.closest('.nav-mobile') &&
        !e.target.closest('#nav-burger') && !e.target.closest('#nav-mobile')) {
      closeMobileNav();
    }
  });

  mobileNav?.querySelectorAll('.nav-link, .nav-mobile-cta').forEach(link => {
    link.addEventListener('click', () => closeMobileNav());
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeMobileNav();
    }
  });

  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  document.querySelectorAll('[data-aos]').forEach(el => revealObs.observe(el));

  function animateCounter(el) {
    const target = parseFloat(el.dataset.counter);
    const isFloat = el.dataset.counter.includes('.');
    const duration = target > 100 ? 1600 : 1200;
    const start = performance.now();
    const run = now => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      const value = target * ease;
      el.textContent = isFloat ? value.toFixed(1) : Math.floor(value);
      if (progress < 1) requestAnimationFrame(run);
    };
    requestAnimationFrame(run);
  }

  const counterObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('[data-counter]').forEach(animateCounter);
        counterObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.25 });
  document.querySelectorAll('.hero-stats, .stat-strip-grid, .hero-premium-stats').forEach(el => counterObs.observe(el));

  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  document.querySelectorAll('.gallery-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.gallery-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  document.querySelectorAll('.tag[data-filter]').forEach(tag => {
    tag.addEventListener('click', () => {
      const group = tag.closest('[data-tag-group]');
      group?.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
      tag.classList.add('active');
    });
  });

  scrollTopBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  const directionModalTriggers = document.querySelectorAll('.dir-detail-trigger[data-modal-target]');
  const directionModals = document.querySelectorAll('.dir-modal');
  let activeDirectionModal = null;
  let lastFocusedTrigger = null;

  function closeDirectionModal(modal) {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    if (modal.__closeTimer) {
      window.clearTimeout(modal.__closeTimer);
    }
    modal.__closeTimer = window.setTimeout(() => {
      modal.hidden = true;
      modal.__closeTimer = null;
    }, 280);
    if (activeDirectionModal === modal) {
      document.body.style.overflow = '';
      activeDirectionModal = null;
    }
  }

  function openDirectionModal(modal, trigger) {
    if (!modal) return;
    if (activeDirectionModal && activeDirectionModal !== modal) {
      closeDirectionModal(activeDirectionModal);
    }
    if (modal.__closeTimer) {
      window.clearTimeout(modal.__closeTimer);
      modal.__closeTimer = null;
    }
    lastFocusedTrigger = trigger || document.activeElement;
    modal.hidden = false;
    modal.scrollTop = 0;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    activeDirectionModal = modal;
    const closeButton = modal.querySelector('.dir-modal-close');
    window.requestAnimationFrame(() => closeButton?.focus());
  }

  directionModalTriggers.forEach(trigger => {
    trigger.setAttribute('aria-haspopup', 'dialog');
    const targetId = trigger.dataset.modalTarget;
    const modal = targetId ? document.getElementById(targetId) : null;
    if (!modal) return;
    trigger.setAttribute('aria-controls', modal.id);
    trigger.addEventListener('click', e => {
      e.preventDefault();
      openDirectionModal(modal, trigger);
    });
  });

  directionModals.forEach(modal => {
    modal.querySelector('.dir-modal-backdrop')?.addEventListener('click', e => {
      e.preventDefault();
      closeDirectionModal(modal);
      lastFocusedTrigger?.focus();
    });

    modal.querySelector('.dir-modal-close')?.addEventListener('click', e => {
      e.preventDefault();
      closeDirectionModal(modal);
      lastFocusedTrigger?.focus();
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = target.getBoundingClientRect().top + window.scrollY - 88;
        window.scrollTo({ top: offset, behavior: 'smooth' });
      }
    });
  });

  const parallaxNodes = [...document.querySelectorAll('[data-parallax]')];
  const heroParallax = document.querySelector('[data-hero-parallax]');
  if (
    (parallaxNodes.length || heroParallax) &&
    window.matchMedia('(min-width: 1024px)').matches &&
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ) {
    let ticking = false;
    const onParallax = () => {
      const viewportHalf = window.innerHeight / 2;
      if (heroParallax) {
        const heroRect = heroParallax.getBoundingClientRect();
        const heroShift = Math.max(-36, Math.min(36, heroRect.top * -0.08));
        heroParallax.style.setProperty('--hero-parallax-y', `${heroShift.toFixed(2)}px`);
      }
      parallaxNodes.forEach(node => {
        const rect = node.getBoundingClientRect();
        const speed = parseFloat(node.dataset.speed || '0.08');
        const centerOffset = viewportHalf - (rect.top + rect.height / 2);
        const translateY = Math.max(-28, Math.min(28, centerOffset * speed * 0.18));
        node.style.transform = `translate3d(0, ${translateY.toFixed(2)}px, 0)`;
      });
      ticking = false;
    };

    const requestParallax = () => {
      if (!ticking) {
        window.requestAnimationFrame(onParallax);
        ticking = true;
      }
    };

    window.addEventListener('scroll', requestParallax, { passive: true });
    window.addEventListener('resize', requestParallax, { passive: true });
    requestParallax();
  }

  window.addEventListener('keydown', e => {
    if (e.key === 'Escape' && activeDirectionModal) {
      closeDirectionModal(activeDirectionModal);
      lastFocusedTrigger?.focus();
    }
  });

});
