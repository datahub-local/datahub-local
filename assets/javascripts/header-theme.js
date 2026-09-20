(function () {
  "use strict";

  var hero = document.querySelector(".hero-band");
  if (!hero) {
    return;
  }

  var root = document.documentElement;
  var header = document.querySelector(".md-header");

  function update() {
    // .md-tabs lives inside .md-header, so its height is already included.
    var offset = header ? header.offsetHeight : 0;
    var past = hero.getBoundingClientRect().bottom <= offset;
    root.classList.toggle("hero-scrolled", past);
  }

  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
})();
