// Scale every 1920x1080 .stage to the window, letterboxed.
(function () {
  function fit() {
    var s = Math.min(innerWidth / 1920, innerHeight / 1080);
    document.querySelectorAll('.stage').forEach(function (el) {
      el.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
    });
  }
  addEventListener('resize', fit);
  addEventListener('DOMContentLoaded', fit);
  fit();
})();
