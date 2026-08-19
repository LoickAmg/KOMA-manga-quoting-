// Copie la citation dans le presse-papiers. Dégrade proprement si l'API
// Clipboard n'est pas disponible (contexte non sécurisé, vieux navigateur).
document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("copy-btn");
  if (!button) return;

  const defaultLabel = button.textContent;

  button.addEventListener("click", async () => {
    // Copie la version actuellement affichée (FR ou VO), pas systématiquement
    // l'anglais — dépend du toggle de langue posé sur <html data-quote-lang>.
    const lang = document.documentElement.dataset.quoteLang === "en" ? "en" : "fr";
    const text = (lang === "fr" && button.dataset.textFr) || button.dataset.text || "";
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const helper = document.createElement("textarea");
        helper.value = text;
        helper.style.position = "fixed";
        helper.style.opacity = "0";
        document.body.appendChild(helper);
        helper.select();
        document.execCommand("copy");
        helper.remove();
      }
      button.textContent = "Copié ✓";
    } catch {
      button.textContent = "Échec de la copie";
    }
    setTimeout(() => {
      button.textContent = defaultLabel;
    }, 1800);
  });
});
