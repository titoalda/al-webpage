/* en el móvil, para esconder la barra de navegación al hacer scroll hacia abajo */
var prevScrollpos = window.scrollY;
window.onscroll = function() {
var currentScrollPos = window.scrollY;
console.log(currentScrollPos);
  if (prevScrollpos > currentScrollPos ||  window.scrollY < (window.innerHeight)*0.08) {
    document.getElementById("topnav").style.top = "0";
  } else {
    document.getElementById("topnav").style.top = "-8vh";
  }
  prevScrollpos = currentScrollPos;
}