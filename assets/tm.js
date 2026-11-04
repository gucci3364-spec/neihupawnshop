"use strict";
(() => {
  /* 手機選單 */
  const btn = document.querySelector(".menu-btn");
  const panel = document.getElementById("tm-panel");
  if (btn && panel) {
    const close = () => { panel.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; };
    btn.addEventListener("click", () => {
      const open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && panel.classList.contains("open")) { close(); btn.focus(); } });
    window.matchMedia("(min-width:980px)").addEventListener("change", close);
  }

  /* 諮詢單「想問」欄：依序打出各項服務（減少動態時不輪播） */
  const typer = document.querySelector(".typer");
  if (typer && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const words = (typer.dataset.words || "").split("|").filter(Boolean);
    if (words.length > 1) {
      let i = 0;
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      (async () => {
        await sleep(4200);
        for (;;) {
          while (typer.textContent.length) { typer.textContent = typer.textContent.slice(0, -1); await sleep(55); }
          i = (i + 1) % words.length;
          for (const ch of words[i]) { typer.textContent += ch; await sleep(110); }
          await sleep(2200);
        }
      })();
    }
  }
})();
