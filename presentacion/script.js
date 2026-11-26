const slides = [...document.querySelectorAll('.slide')];
const previousButton = document.querySelector('#prev');
const nextButton = document.querySelector('#next');
const fullscreenButton = document.querySelector('#fullscreen');
const counter = document.querySelector('#counter');
const progressBar = document.querySelector('#progress-bar');

let current = Math.max(0, Math.min(slides.length - 1, Number(location.hash.slice(1)) - 1 || 0));

function showSlide(index, updateHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, position) => {
    const active = position === current;
    slide.classList.toggle('active', active);
    slide.setAttribute('aria-hidden', String(!active));
  });
  counter.textContent = `${current + 1} / ${slides.length}`;
  progressBar.style.width = `${((current + 1) / slides.length) * 100}%`;
  previousButton.disabled = current === 0;
  nextButton.disabled = current === slides.length - 1;
  document.title = `${slides[current].dataset.title} · Desigualdades`;
  if (updateHash) history.replaceState(null, '', `#${current + 1}`);
}

previousButton.addEventListener('click', () => showSlide(current - 1));
nextButton.addEventListener('click', () => showSlide(current + 1));
fullscreenButton.addEventListener('click', async () => {
  if (document.fullscreenElement) await document.exitFullscreen();
  else await document.documentElement.requestFullscreen();
});

document.addEventListener('keydown', (event) => {
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) {
    event.preventDefault();
    showSlide(current + 1);
  }
  if (['ArrowLeft', 'PageUp'].includes(event.key)) {
    event.preventDefault();
    showSlide(current - 1);
  }
  if (event.key === 'Home') showSlide(0);
  if (event.key === 'End') showSlide(slides.length - 1);
  if (event.key.toLowerCase() === 'f') fullscreenButton.click();
});

window.addEventListener('hashchange', () => showSlide(Number(location.hash.slice(1)) - 1, false));
showSlide(current);
