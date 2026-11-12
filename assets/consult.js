"use strict";
(() => {
  const form = document.querySelector("#consult-form");
  const typeSelect = document.querySelector("#service-type");
  const nameInput = document.querySelector("#consult-name");
  const phoneInput = document.querySelector("#consult-phone");
  const summaryCard = document.querySelector("#consult-summary");
  const summaryText = document.querySelector("#summary-text");
  const summaryHeading = document.querySelector("#summary-heading");
  const review = document.querySelector("#review-summary");
  const copyButton = document.querySelector("#copy-summary");
  const copyStatus = document.querySelector("#copy-status");
  const formStatus = document.querySelector("#form-status");
  const generateButton = document.querySelector("#generate-summary");
  const privacy = window.ConsultPrivacy;
  if (!form || !typeSelect || !nameInput || !phoneInput || !summaryCard || !summaryText || !review || !copyButton || !copyStatus || !privacy) return;
  const { clean, redact, mobile } = privacy;
  const types = {
    car: "汽車借款", motorcycle: "機車借款", gold: "黃金・珠寶",
    watch: "名錶典當", bags: "精品包款", devices: "3C 數位產品", other: "其他需求"
  };
  const queryType = new URLSearchParams(window.location.search).get("type");
  const setService = () => {
    if (Object.prototype.hasOwnProperty.call(types, queryType)) typeSelect.value = queryType;
  };
  let summaryVersion = 0;
  let copying = false;
  let copyAttempted = false;
  const canCopy = () => !copying && !summaryCard.hidden && review.checked && Boolean(clean(summaryText.value));
  function clearSummary(notice = "") {
    summaryVersion += 1;
    summaryCard.hidden = true;
    summaryText.value = "";
    review.checked = false;
    copyButton.disabled = true;
    copyButton.textContent = "複製諮詢摘要";
    copyStatus.textContent = "";
    formStatus.textContent = notice;
  }
  function formChanged() {
    nameInput.setCustomValidity("");
    phoneInput.setCustomValidity("");
    clearSummary(!summaryCard.hidden ? "資料已變更，請重新產生並核對摘要；已複製的舊內容不會自動更新。" : "");
  }
  form.addEventListener("input", formChanged);
  form.addEventListener("change", formChanged);
  form.addEventListener("submit", event => {
    event.preventDefault();
    nameInput.setCustomValidity(clean(nameInput.value) ? "" : "請填寫稱呼或暱稱。");
    const phone = mobile(phoneInput.value);
    phoneInput.setCustomValidity(phone.valid ? "" : "請填寫 09 開頭的 10 碼手機，或 +8869 開頭的號碼；也可留白改以 LINE 聯絡。");
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const value = key => clean(data.get(key));
    const service = types[value("service")];
    if (!Object.prototype.hasOwnProperty.call(types, value("service"))) return;
    // Explicit allowlist: removed/legacy fields are never serialized.
    const lines = ["羅經理您好，以下是我的初次借款諮詢：", "", `稱呼：${value("name")}`, `諮詢項目：${service}`];
    lines.push(phone.text ? `手機號碼：${phone.text}` : "聯絡方式：請先以本 LINE 對話聯絡");
    const add = (label, key) => { if (value(key)) lines.push(`${label}：${value(key)}`); };
    add("所在縣市", "region");
    add("方便聯絡時段", "contactTime");
    if (value("amount")) lines.push(`希望借款金額：${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 1 }).format(Number(value("amount")))} 萬元`);
    add("資金用途", "purpose");
    add("物品概況", "collateral");
    add("物品貸款／分期", "financing");
    add("每月收入區間", "incomeRange");
    add("每月現有還款總額區間", "repaymentRange");
    add("其他需求補充", "notes");
    lines.push("", "請協助說明後續評估流程與所需資料，謝謝。");
    const result = redact(lines.join("\n"));
    summaryVersion += 1;
    summaryText.value = result.text;
    summaryText.readOnly = true;
    summaryCard.hidden = false;
    review.checked = false;
    copyButton.disabled = true;
    copyButton.textContent = "複製諮詢摘要";
    formStatus.textContent = "";
    copyStatus.textContent = result.removed
      ? "已從摘要移除疑似證件或帳號／卡號。請再檢查是否有其他個資，勾選確認後即可複製；尚未送出。"
      : "摘要已整理，尚未送出。請核對內容並勾選確認後複製。";
    summaryCard.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    summaryHeading.focus({ preventScroll: true });
  });
  review.addEventListener("change", () => {
    summaryVersion += 1;
    copyButton.disabled = !canCopy();
    copyButton.textContent = "複製諮詢摘要";
  });
  function fallbackCopy() {
    summaryText.focus();
    summaryText.select();
    summaryText.setSelectionRange(0, summaryText.value.length);
    try { return Boolean(document.execCommand("copy")); } catch (_) { return false; }
  }
  copyButton.addEventListener("click", async () => {
    if (!canCopy()) return;
    const result = redact(summaryText.value);
    // Re-check at the clipboard boundary, even if the DOM was altered.
    if (result.text !== summaryText.value) {
      summaryText.value = result.text;
      review.checked = false;
      summaryVersion += 1;
      copyButton.disabled = true;
      copyStatus.textContent = "摘要已重新移除疑似敏感資料，請再次核對並勾選確認後複製。";
      return;
    }
    const version = summaryVersion;
    const text = result.text;
    const stillCurrent = () => version === summaryVersion && !summaryCard.hidden && review.checked && summaryText.value === text;
    copying = true;
    copyAttempted = true;
    copyButton.disabled = true;
    copyButton.textContent = "正在複製…";
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        copied = true;
      } else copied = fallbackCopy();
    } catch (_) {
      if (stillCurrent()) copied = fallbackCopy();
    } finally {
      copying = false;
      copyButton.disabled = !canCopy();
      if (!stillCurrent()) {
        copyButton.textContent = "複製諮詢摘要";
        formStatus.textContent = "資料已變更或清空；先前的複製作業可能已將舊摘要寫入剪貼簿，貼上前請重新核對。";
      } else {
        copyButton.textContent = copied ? "已複製" : "請長按摘要複製";
        copyStatus.textContent = copied
          ? "已複製，尚未送出。請開啟官方 LINE（@104faknx），自行貼上、核對後送出。"
          : "瀏覽器未能自動複製。已選取摘要，請長按文字選擇「複製」，再貼至官方 LINE；尚未送出。";
      }
    }
  });
  form.addEventListener("reset", () => {
    clearSummary(copyAttempted ? "已清空本頁資料；裝置剪貼簿及已傳送的 LINE 訊息不會一起刪除。" : "已清空本頁資料。若曾手動複製，剪貼簿內容需另外清除。");
    nameInput.setCustomValidity("");
    phoneInput.setCustomValidity("");
  });
  document.querySelector("#clear-after-copy").addEventListener("click", () => {
    form.reset();
    generateButton.focus();
  });
  // Browser history restoration must not revive another visitor's filled form.
  window.addEventListener("pagehide", () => form.reset());
  window.addEventListener("pageshow", event => {
    if (event.persisted) { form.reset(); setService(); }
  });
  form.reset();
  clearSummary();
  setService();
  generateButton.disabled = false;
})();

