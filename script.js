// scroll progress bar
var prog = document.getElementById('progress');
if (prog) {
  var updateProgress = function() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    prog.style.width = max > 0 ? (window.scrollY / max * 100) + '%' : '0%';
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
}

// reveal-on-scroll
var io = new IntersectionObserver(function(entries) {
  entries.forEach(function(e) {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });
document.querySelectorAll('.reveal').forEach(function(el) { io.observe(el); });

// mousemove spotlight on cards
document.querySelectorAll('.item, .project-card, .post-item').forEach(function(card) {
  card.addEventListener('mousemove', function(e) {
    var r = card.getBoundingClientRect();
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});
