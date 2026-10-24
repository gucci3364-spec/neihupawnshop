"use strict";
(() => {
  const button = document.querySelector(".mobile-menu");
  const panel = document.querySelector(".mobile-nav-panel");
  if (!button || !panel) return;
  const close = () => { panel.classList.remove("open"); button.setAttribute("aria-expanded", "false"); };
  button.addEventListener("click", () => { const open = panel.classList.toggle("open"); button.setAttribute("aria-expanded", String(open)); });
  panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && panel.classList.contains("open")) { close(); button.focus(); } });
  document.addEventListener("click", (e) => { if (!panel.contains(e.target) && !button.contains(e.target)) close(); });
})();
