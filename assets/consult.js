"use strict";
(() => {
  const form = document.querySelector("#consult-form");
  const typeSelect = document.querySelector("#service-type");
  const summaryCard = document.querySelector("#consult-summary");
  const summaryText = document.querySelector("#summary-text");
  const summaryHeading = document.querySelector("#summary-heading");
  const copyButton = document.querySelector("#copy-summary");
  const status = document.querySelector("#copy-status");
  const generateButton = document.querySelector("#generate-summary");
  if (!form || !typeSelect || !summaryCard || !summaryText || !copyButton || !status) return;
  const types = {
    car: "汽車借款", motorcycle: "機車借款", gold: "黃金・珠寶",
    watch: "名錶典當", bags: "精品包款", devices: "3C 數位產品", other: "其他需求"
  };
  const queryType = new URLSearchParams(window.location.search).get("type");
  if (Object.prototype.hasOwnProperty.call(types, queryType)) typeSelect.value = queryType;
  const clean = (value) => String(value ?? "").replace(/\r/g, "").trim();
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const amount = clean(data.get("amount"));
    const name = clean(data.get("name"));
    const place = clean(data.get("region"));
    const notes = clean(data.get("notes"));
    const service = types[data.get("service")] || "其他需求";
    summaryText.value = [
      "羅經理您好，我想先諮詢台茂當舖的服務：", "",
      `諮詢項目：${service}`,
      `怎麼稱呼：${name || "尚未填寫"}`,
      `所在地區：${place || "尚未填寫"}`,
      `預計資金需求：${amount ? `${Number(amount).toLocaleString("zh-TW", {maximumFractionDigits: 2})} 萬元` : "想先了解，尚未確定"}`,
      `物品與需求說明：${notes || "想先了解準備事項與辦理流程。"}`, "",
      "想請您協助確認評估方式與需要準備的資料，謝謝。"
    ].join("\n");
    summaryCard.hidden = false;
    status.textContent = "內容已整理在下方，尚未送出。";
    copyButton.textContent = "複製諮詢內容";
    summaryCard.scrollIntoView({behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start"});
    if (summaryHeading) summaryHeading.focus({preventScroll:true});
  });
  const fallbackCopy = () => {
    summaryText.focus();
    summaryText.select();
    summaryText.setSelectionRange(0, summaryText.value.length);
    try { return Boolean(document.execCommand("copy")); } catch (_) { return false; }
  };
  copyButton.addEventListener("click", async () => {
    if (!summaryText.value) return;
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(summaryText.value); copied = true;
      } else copied = fallbackCopy();
    } catch (_) { copied = fallbackCopy(); }
    copyButton.textContent = copied ? "已複製" : "請長按複製";
    status.textContent = copied ? "已複製。請開啟官方 LINE，自行貼上後送出；本頁尚未傳送資料。" : "瀏覽器無法直接複製，請長按上方文字選取並複製，再貼至官方 LINE。";
  });
  form.addEventListener("reset", () => {
    summaryCard.hidden = true;
    summaryText.value = "";
    status.textContent = "";
    copyButton.textContent = "複製諮詢內容";
  });
  if (generateButton) generateButton.disabled = false;
})();
