// ---- Countdown ----
(function () {
  var target = new Date(document.body.dataset.weddingDatetime).getTime();
  var d = document.getElementById('cd-days');
  var h = document.getElementById('cd-hours');
  var m = document.getElementById('cd-mins');
  var s = document.getElementById('cd-secs');
  if (!d) return;

  function tick() {
    var now = Date.now();
    var diff = Math.max(0, target - now);
    var days = Math.floor(diff / 86400000);
    var hours = Math.floor((diff % 86400000) / 3600000);
    var mins = Math.floor((diff % 3600000) / 60000);
    var secs = Math.floor((diff % 60000) / 1000);
    d.textContent = String(days).padStart(2, '0');
    h.textContent = String(hours).padStart(2, '0');
    m.textContent = String(mins).padStart(2, '0');
    s.textContent = String(secs).padStart(2, '0');
  }
  tick();
  setInterval(tick, 1000);
})();

// ---- Nav solid-on-scroll ----
(function () {
  var nav = document.querySelector('.nav');
  if (!nav) return;
  function onScroll() {
    if (window.scrollY > 60) nav.classList.add('solid');
    else nav.classList.remove('solid');
  }
  onScroll();
  window.addEventListener('scroll', onScroll);
})();

// ---- Highlight the section currently in view ----
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a'));
  if (!links.length || !('IntersectionObserver' in window)) return;

  var pairs = links
    .map(function (link) {
      return { link: link, section: document.querySelector(link.getAttribute('href')) };
    })
    .filter(function (pair) { return pair.section; });
  if (!pairs.length) return;

  function setActive(id) {
    pairs.forEach(function (pair) {
      pair.link.classList.toggle('active', pair.section.id === id);
    });
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) setActive(entry.target.id);
    });
  }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

  pairs.forEach(function (pair) { observer.observe(pair.section); });
})();

// ---- Mobile menu ----
(function () {
  var openBtn = document.querySelector('.menu-btn');
  var closeBtn = document.querySelector('.menu-close');
  var panel = document.querySelector('.menu-panel');
  if (!openBtn || !panel) return;
  openBtn.addEventListener('click', function () { panel.classList.add('open'); });
  closeBtn.addEventListener('click', function () { panel.classList.remove('open'); });
  panel.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { panel.classList.remove('open'); });
  });
})();

// ---- RSVP form (static site: opens email client with details pre-filled) ----
(function () {
  var form = document.getElementById('rsvp-form');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.name.value.trim();
    var side = form.side.value;
    var attending = form.attending.value;
    var guests = form.guests.value.trim();
    var kids = form.kids.value;
    var message = form.message.value.trim();

    var subject = 'RSVP - ' + name + ' (' + side + ', ' + attending + ')';
    var body =
      'Name: ' + name + '\n' +
      'Guest of: ' + side + '\n' +
      'Attending: ' + attending + '\n' +
      'Number of guests: ' + guests + '\n' +
      'Coming with kids: ' + kids + '\n' +
      'Message: ' + message;

    var mailto = 'mailto:' + form.dataset.rsvpEmail +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);

    window.location.href = mailto;
  });
})();
