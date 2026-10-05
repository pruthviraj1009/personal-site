// Loaded synchronously in <head>: flag JS support before first paint so
// .reveal content only starts hidden when we know this script can reveal it.
document.documentElement.classList.add('js');

var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

document.addEventListener('DOMContentLoaded', function() {

  // scroll progress bar
  var prog = document.getElementById('progress');
  if (prog) {
    var updateProgress = function() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
  }

  // reveal-on-scroll
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });
    reveals.forEach(function(el) { io.observe(el); });
  } else {
    reveals.forEach(function(el) { el.classList.add('visible'); });
  }

  // mousemove spotlight on cards
  document.querySelectorAll('.project-card, .post-item').forEach(function(card) {
    card.addEventListener('mousemove', function(e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // homepage tagline typewriter (text is already in the HTML; skip when motion is reduced)
  var tagline = document.getElementById('tagline-text');
  if (tagline && !reducedMotion) {
    var full = tagline.textContent;
    var charIdx = 0;
    var typeStep = function() {
      tagline.textContent = full.slice(0, charIdx);
      charIdx++;
      if (charIdx <= full.length) {
        setTimeout(typeStep, charIdx === 1 ? 800 : 36 + Math.random() * 20);
      }
    };
    typeStep();
  }

  // 404: echo the requested path
  var errorPath = document.getElementById('error-path');
  if (errorPath) errorPath.textContent = window.location.pathname;
});
