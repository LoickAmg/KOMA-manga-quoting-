(function () {
  "use strict";

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "mode clair" : "mode sombre";
  }

  function applyLang(lang) {
    document.documentElement.dataset.quoteLang = lang;
    var btn = document.getElementById("lang-toggle");
    if (btn) btn.textContent = lang === "fr" ? "afficher en VO" : "afficher en FR";
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(document.documentElement.dataset.theme || "light");
    applyLang(document.documentElement.dataset.quoteLang || "fr");

    var themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        var next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        try {
          localStorage.setItem("koma-theme", next);
        } catch (err) {
          /* stockage indisponible (navigation privée, quota…) — le thème
             reste appliqué pour cette page, juste pas mémorisé. */
        }
        applyTheme(next);
      });
    }

    var langBtn = document.getElementById("lang-toggle");
    if (langBtn) {
      langBtn.addEventListener("click", function () {
        var next = document.documentElement.dataset.quoteLang === "fr" ? "en" : "fr";
        try {
          localStorage.setItem("koma-lang", next);
        } catch (err) {
          /* idem : dégradation silencieuse si le stockage échoue. */
        }
        applyLang(next);
      });
    }
  });
})();
