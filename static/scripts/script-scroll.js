/* en el móvil, para esconder la barra de navegación al hacer scroll hacia abajo */
var prevScrollpos = window.scrollY;
window.onscroll = function() {
  var currentScrollPos = window.scrollY;
  var topnav = document.getElementById("topnav") || document.querySelector("header");
  if (topnav) {
    if (prevScrollpos > currentScrollPos || window.scrollY < (window.innerHeight)*0.08) {
      topnav.style.top = "0";
    } else {
      topnav.style.top = "-8vh";
    }
  }
  prevScrollpos = currentScrollPos;
}