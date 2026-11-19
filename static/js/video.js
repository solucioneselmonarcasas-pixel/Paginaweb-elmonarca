// Video de la herramienta: YouTube se carga solo cuando la persona toca reproducir (página más liviana y sin
// cookies de YouTube antes de ese momento). Sin JavaScript, el enlace abre el video en YouTube.
document.querySelectorAll("a.video[data-video]").forEach(function (enlace) {
  enlace.addEventListener("click", function (evento) {
    var id = enlace.getAttribute("data-video");
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    evento.preventDefault();
    var marco = document.createElement("iframe");
    marco.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0&playsinline=1";
    marco.title = "Video de la herramienta de El Monarca";
    marco.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    marco.allowFullscreen = true;
    marco.className = "video video--reproduciendo";
    enlace.replaceWith(marco);
    marco.focus();
  });
});
