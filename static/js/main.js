document.addEventListener('DOMContentLoaded', function() {
  // Sticky navbar
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // Mobile menu
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  const overlay = document.querySelector('.mobile-overlay');
  if (hamburger && mobileNav) {
    const toggle = () => {
      hamburger.classList.toggle('active');
      mobileNav.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
      document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
    };
    hamburger.addEventListener('click', toggle);
    if (overlay) overlay.addEventListener('click', toggle);
    mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      if (mobileNav.classList.contains('open')) toggle();
    }));
  }

  // Active nav link
  const path = window.location.pathname;
  document.querySelectorAll('.nav-menu a, .mobile-nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (href !== '/' && path.startsWith(href))) {
      a.classList.add('active');
    }
  });

  // Fade-up animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  // Animated counters
  const counters = document.querySelectorAll('[data-count]');
  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const el = e.target;
        const target = el.getAttribute('data-count');
        const num = parseInt(target.replace(/[^0-9]/g, '')) || 0;
        const suffix = target.replace(/[0-9,]/g, '');
        let current = 0;
        const step = Math.max(1, Math.floor(num / 40));
        const timer = setInterval(() => {
          current += step;
          if (current >= num) { current = num; clearInterval(timer); }
          el.textContent = current.toLocaleString() + suffix;
        }, 30);
        counterObs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => counterObs.observe(c));

  // Testimonial slider
  const track = document.querySelector('.testimonial-track');
  if (track) {
    const slides = track.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.slider-dots button');
    const prevBtn = document.querySelector('.slider-prev');
    const nextBtn = document.querySelector('.slider-next');
    let current = 0;
    let autoTimer;

    const goTo = (i) => {
      current = (i + slides.length) % slides.length;
      track.style.transform = `translateX(-${current * 100}%)`;
      dots.forEach((d, di) => d.classList.toggle('active', di === current));
    };
    const next = () => goTo(current + 1);
    const prev = () => goTo(current - 1);
    const startAuto = () => { autoTimer = setInterval(next, 5000); };
    const stopAuto = () => clearInterval(autoTimer);

    if (nextBtn) nextBtn.addEventListener('click', () => { next(); stopAuto(); startAuto(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prev(); stopAuto(); startAuto(); });
    dots.forEach((d, i) => d.addEventListener('click', () => { goTo(i); stopAuto(); startAuto(); }));
    track.addEventListener('mouseenter', stopAuto);
    track.addEventListener('mouseleave', startAuto);
    startAuto();
  }

  // Flash messages auto-dismiss
  document.querySelectorAll('.flash').forEach(f => {
    setTimeout(() => { f.style.opacity = '0'; setTimeout(() => f.remove(), 300); }, 5000);
    const close = f.querySelector('.close-flash');
    if (close) close.addEventListener('click', () => f.remove());
  });
});
