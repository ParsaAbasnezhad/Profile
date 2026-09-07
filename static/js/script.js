document.documentElement.classList.add('js');

/* ---------------- Page loader ---------------- */
function hideLoader() {
  const loader = document.getElementById('loader');
  if (loader) {
    loader.classList.add('hidden');
  }
}

window.addEventListener('DOMContentLoaded', () => {
  setTimeout(hideLoader, 400);
});
window.setTimeout(hideLoader, 2000);

/* ---------------- Scroll progress bar ---------------- */
const scrollProgress = document.getElementById('scrollProgress');
function updateScrollProgress() {
  if (!scrollProgress) return;
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  scrollProgress.style.width = pct + '%';
}
window.addEventListener('scroll', updateScrollProgress);
updateScrollProgress();

/* ---------------- Mobile nav toggle ---------------- */
const burgerBtn = document.getElementById('burgerBtn');
const nav = document.querySelector('.nav');
if (burgerBtn && nav) {
  burgerBtn.addEventListener('click', () => {
    nav.classList.toggle('open');
    burgerBtn.classList.toggle('open');
  });
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      burgerBtn.classList.remove('open');
    });
  });
}

/* ---------------- Active nav link on scroll ---------------- */
const sections = document.querySelectorAll('main section[id], header[id]');
const navLinks = document.querySelectorAll('.nav-link');
function setActiveLink() {
  let current = sections[0]?.id;
  const scrollPos = window.scrollY + 140;
  sections.forEach(section => {
    if (section.offsetTop <= scrollPos) current = section.id;
  });
  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
}
window.addEventListener('scroll', setActiveLink);
setActiveLink();

/* ---------------- Language switcher ---------------- */
const langBtn = document.getElementById('langBtn');
const langDropdown = document.getElementById('langDropdown');
const langLabel = document.getElementById('langLabel');
if (langBtn && langDropdown && langLabel) {
  langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('open');
  });
  langDropdown.querySelectorAll('p').forEach(option => {
    option.addEventListener('click', () => {
      langLabel.textContent = option.dataset.lang;
      langDropdown.classList.remove('open');
    });
  });
  document.addEventListener('click', () => langDropdown.classList.remove('open'));
}

/* ---------------- Reveal on scroll (Intersection Observer) ---------------- */
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
revealEls.forEach(el => revealObserver.observe(el));

/* ---------------- Typewriter effect ---------------- */
const words = ['front-end developer', 'UI craftsman', 'problem solver', 'lifelong learner'];
const typewriterEl = document.getElementById('typewriter');
let wordIndex = 0, charIndex = 0, deleting = false;

function typeLoop() {
  const currentWord = words[wordIndex];
  if (!deleting) {
    charIndex++;
    typewriterEl.textContent = currentWord.slice(0, charIndex);
    if (charIndex === currentWord.length) {
      deleting = true;
      setTimeout(typeLoop, 1600);
      return;
    }
  } else {
    charIndex--;
    typewriterEl.textContent = currentWord.slice(0, charIndex);
    if (charIndex === 0) {
      deleting = false;
      wordIndex = (wordIndex + 1) % words.length;
    }
  }
  setTimeout(typeLoop, deleting ? 40 : 80);
}
if (typewriterEl) typeLoop();

/* ---------------- Animated stat counters ---------------- */
const statEls = document.querySelectorAll('.stat-number');
function animateCount(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1200;
  const start = performance.now();
  function step(now) {
    const progress = Math.min((now - start) / duration, 1);
    el.textContent = Math.floor(progress * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  }
  requestAnimationFrame(step);
}
const statObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCount(entry.target);
      statObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });
statEls.forEach(el => statObserver.observe(el));

/* ---------------- Animated skill bars ---------------- */
const skillBars = document.querySelectorAll('.skill-bar i');
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      skillObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.4 });
skillBars.forEach(bar => skillObserver.observe(bar));

/* ---------------- Back to top button ---------------- */
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  if (!backToTop) return;
  backToTop.classList.toggle('visible', window.scrollY > 500);
});
if (backToTop) {
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
