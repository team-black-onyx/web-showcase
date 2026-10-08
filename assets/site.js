(() => {
  const root = document.documentElement;
  root.classList.add('js');
  const toggle = document.querySelector('.theme-toggle');
  const icon = document.querySelector('.theme-icon');
  const syncTheme = () => {
    const light = root.dataset.theme === 'light';
    toggle?.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
    if (icon) icon.textContent = light ? '☾' : '☼';
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', light ? '#F6F7F8' : '#0B0D0F');
  };
  syncTheme();
  toggle?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('layercraft-theme', root.dataset.theme); } catch (_) {}
    syncTheme();
  });
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    nav?.classList.toggle('open', open);
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    menu?.setAttribute('aria-expanded', 'false');
    menu?.setAttribute('aria-label', 'Open navigation');
  }));
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  } else document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
})();
