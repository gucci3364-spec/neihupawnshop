"use strict";
(() => {
  const button = document.querySelector(".inner-menu");
  const nav = document.querySelector(".inner-nav");
  if (!button || !nav) return;
  const close = () => { nav.classList.remove("open"); button.setAttribute("aria-expanded", "false"); };
  button.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    button.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", close));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && nav.classList.contains("open")) { close(); button.focus(); }
  });
  document.addEventListener("click", (event) => {
    if (!nav.contains(event.target) && !button.contains(event.target)) close();
  });
})();
