// Scale every 1920x1080 .stage to the window, letterboxed.
(function () {
  function fit() {
    var s = Math.min(innerWidth / 1920, innerHeight / 1080);
    document.querySelectorAll('.stage').forEach(function (el) {
      el.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
    });
  }
  // inside the deck: ?lvl=2/6 turns the footer into the organisers' LVL counter
  addEventListener('DOMContentLoaded', function () {
    var m = /lvl=(\d+)\/(\d+)/.exec(location.search); if (!m) return;
    var l = document.querySelector('.foot .lvl'), b = document.querySelector('.foot .bar i');
    if (l) l.textContent = m[1] === '0' ? 'BACKUP' : 'LVL ' + ('0' + m[1]).slice(-2) + '/' + ('0' + m[2]).slice(-2);
    if (b) b.style.width = (100 * m[1] / m[2]) + '%';
  });
  addEventListener('resize', fit);
  addEventListener('DOMContentLoaded', fit);
  fit();
})();
