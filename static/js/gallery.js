document.addEventListener('DOMContentLoaded', function() {
  const items = document.querySelectorAll('.gallery-item[data-src]');
  if (!items.length) return;

  let currentIdx = 0;
  const sources = Array.from(items).map(i => ({
    src: i.dataset.src || i.querySelector('img')?.src,
    title: i.dataset.title || ''
  }));

  // Create lightbox
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = `
    <span class="lightbox-close" aria-label="Close">&times;</span>
    <span class="lightbox-nav lightbox-prev" aria-label="Previous">&#10094;</span>
    <img src="" alt="">
    <span class="lightbox-nav lightbox-next" aria-label="Next">&#10095;</span>
    <div class="lightbox-caption"></div>
  `;
  document.body.appendChild(lb);

  const lbImg = lb.querySelector('img');
  const lbCaption = lb.querySelector('.lightbox-caption');
  const show = (i) => {
    currentIdx = (i + sources.length) % sources.length;
    lbImg.src = sources[currentIdx].src;
    lbCaption.textContent = sources[currentIdx].title;
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const hide = () => {
    lb.classList.remove('open');
    document.body.style.overflow = '';
  };

  items.forEach((item, i) => item.addEventListener('click', () => show(i)));
  lb.querySelector('.lightbox-close').addEventListener('click', hide);
  lb.querySelector('.lightbox-prev').addEventListener('click', () => show(currentIdx - 1));
  lb.querySelector('.lightbox-next').addEventListener('click', () => show(currentIdx + 1));
  lb.addEventListener('click', e => { if (e.target === lb) hide(); });
  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') hide();
    if (e.key === 'ArrowLeft') show(currentIdx - 1);
    if (e.key === 'ArrowRight') show(currentIdx + 1);
  });
});
