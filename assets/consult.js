"use strict";
(() => {
  const form = document.querySelector("#consult-form");
  const typeSelect = document.querySelector("#service-type");
  const summaryCard = document.querySelector("#consult-summary");
  const summaryText = document.querySelector("#summary-text");
  const summaryHeading = document.querySelector("#summary-heading");
  const copyButton = document.querySelector("#copy-summary");
  const copyStatus = document.querySelector("#copy-status");
  const formStatus = document.querySelector("#form-status");
  const generateButton = document.querySelector("#generate-summary");
  const birthday = document.querySelector("#consult-birthday");
  const ageInput = document.querySelector("#consult-age");
  const idInput = document.querySelector("#consult-id-number");
  const idToggle = document.querySelector("#toggle-id-visibility");
  const includeFullId = document.querySelector("#include-full-id");
  if (!form || !typeSelect || !summaryCard || !summaryText || !copyButton || !copyStatus) return;

  const types = {
    car: "汽車借款", motorcycle: "機車借款", gold: "黃金・珠寶",
    watch: "名錶典當", bags: "精品包款", devices: "3C 數位產品", other: "其他需求"
  };
  const queryType = new URLSearchParams(window.location.search).get("type");
  if (Object.prototype.hasOwnProperty.call(types, queryType)) typeSelect.value = queryType;

  const clean = value => String(value ?? "").replace(/\r/g, "").trim();
  const filled = value => clean(value) || "未填寫";
  const numberFormat = new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 2 });
  let summaryVersion = 0;
  let copying = false;

  function todayInTaipei() {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Taipei", year: "numeric", month: "2-digit", day: "2-digit"
    }).formatToParts(new Date());
    const part = type => parts.find(item => item.type === type).value;
    return `${part("year")}-${part("month")}-${part("day")}`;
  }

  function dateParts(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
    const date = new Date(`${value}T00:00:00.000Z`);
    if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== value) return null;
    return value.split("-").map(Number);
  }

  function syncBirthday() {
    if (!birthday) return;
    const today = todayInTaipei();
    birthday.max = today;
    birthday.setCustomValidity("");
    const value = clean(birthday.value);
    if (ageInput) ageInput.readOnly = Boolean(value);
    if (!value) return;
    const birth = dateParts(value);
    if (!birth || value > today) {
      birthday.setCustomValidity(birth ? "出生日期不能晚於今天。" : "請填寫有效的出生日期。");
      if (ageInput) ageInput.value = "";
      return;
    }
    const current = dateParts(today);
    let age = current[0] - birth[0];
    // For a February 29 birth, the month/day anniversary falls on March 1 in a non-leap year.
    if (current[1] < birth[1] || (current[1] === birth[1] && current[2] < birth[2])) age -= 1;
    if (ageInput) ageInput.value = String(age);
  }

  function setIdVisible(visible) {
    if (idInput) idInput.type = visible ? "text" : "password";
    if (idToggle) {
      idToggle.setAttribute("aria-pressed", String(visible));
      idToggle.setAttribute("aria-label", visible ? "隱藏身分證字號" : "顯示身分證字號");
      idToggle.textContent = visible ? "隱藏" : "顯示";
    }
  }

  function maskId(value) {
    const characters = Array.from(clean(value));
    if (!characters.length) return "未填寫";
    if (characters.length < 8) return "*".repeat(characters.length);
    return characters[0] + "*".repeat(characters.length - 4) + characters.slice(-3).join("");
  }

  function amountWithUnit(value, unit) {
    const text = clean(value);
    if (!text) return "未填寫";
    const number = Number(text.replace(/,/g, ""));
    return `${Number.isFinite(number) ? numberFormat.format(number) : text} ${unit}`;
  }

  function clearSummary(notice = "") {
    summaryVersion += 1;
    summaryCard.hidden = true;
    summaryText.value = "";
    copyStatus.textContent = "";
    copyButton.textContent = "複製諮詢內容";
    copyButton.disabled = true;
    if (formStatus && notice) formStatus.textContent = notice;
  }

  function formChanged(event) {
    // An edited summary is intentional; source-form edits require a fresh summary.
    if (event.target === summaryText) return;
    if (event.target === birthday) syncBirthday();
    const hadSummary = !summaryCard.hidden || Boolean(summaryText.value);
    clearSummary(hadSummary ? "資料已變更，請重新產生諮詢內容。" : "");
  }
  form.addEventListener("input", formChanged);
  form.addEventListener("change", formChanged);

  form.addEventListener("submit", event => {
    event.preventDefault();
    syncBirthday();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const value = name => clean(data.get(name));
    const line = (label, name) => `${label}：${filled(data.get(name))}`;
    const id = value("idNumber");
    const showFullId = Boolean(includeFullId && includeFullId.checked && data.has("includeFullId"));
    const idSummary = showFullId ? filled(id) : maskId(id);
    const service = Object.prototype.hasOwnProperty.call(types, value("service")) ? types[value("service")] : "未填寫";
    summaryVersion += 1;
    summaryText.value = [
      "羅經理您好，以下是我的借款諮詢資料：", "",
      "【基本資料】",
      line("姓名", "name"),
      line("手機號碼", "phone"),
      line("生日", "birthDate"),
      `年齡：${value("age") ? `${value("age")} 歲` : "未填寫"}`,
      `身分證字號：${idSummary}${id && !showFullId ? "（已遮罩）" : ""}`,
      line("目前居住地", "residenceAddress"),
      line("居住地持有人", "residenceOwner"),
      line("戶籍地", "registeredAddress"),
      line("戶籍地持有人", "registeredOwner"), "",
      "【工作與資產】",
      line("職業／工作內容", "occupation"),
      line("公司名稱", "company"),
      line("在職年資", "tenure"),
      `月收入：${amountWithUnit(data.get("monthlyIncome"), "元")}`,
      line("薪轉／勞保", "payrollInsurance"),
      line("有無房屋、土地", "realEstate"),
      line("有無汽車、機車", "vehicles"),
      line("是否有汽車駕照", "driverLicense"), "",
      "【負債與信用】",
      line("銀行貸款（銀行／金額／月繳／期數）", "bankLoans"),
      line("信用卡狀況", "creditCards"),
      line("融資公司貸款", "financeLoans"),
      line("民間借款", "privateLoans"),
      line("有無債務協商或法扣", "negotiationDeduction"),
      line("警示帳戶", "flaggedAccount"),
      line("支付命令", "paymentOrder"),
      line("未繳罰單", "unpaidFines"),
      line("有無銀行或融資呆帳", "badDebt"),
      line("有無銀行或融資遲繳", "latePayments"),
      line("近 3 個月有無送貸款申請", "recentApplications"), "",
      "【本次借款需求】",
      `諮詢項目：${service}`,
      `此次想貸額度：${amountWithUnit(data.get("amount"), "萬元")}`,
      line("資金用途", "purpose"),
      line("目前是否還在其他代辦詢問", "otherAgent"),
      line("其他補充說明", "notes"), "",
      "請協助說明後續所需資料與評估流程，謝謝。"
    ].join("\n");
    summaryCard.hidden = false;
    if (formStatus) formStatus.textContent = "";
    copyStatus.textContent = "內容已整理在下方，尚未送出。";
    copyButton.textContent = copying ? "正在複製…" : "複製諮詢內容";
    copyButton.disabled = copying;
    summaryCard.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    if (summaryHeading) summaryHeading.focus({ preventScroll: true });
  });

  const fallbackCopy = () => {
    summaryText.focus();
    summaryText.select();
    summaryText.setSelectionRange(0, summaryText.value.length);
    try { return Boolean(document.execCommand("copy")); } catch (_) { return false; }
  };

  summaryText.addEventListener("input", () => {
    summaryVersion += 1;
    copyButton.textContent = copying ? "正在複製…" : "複製諮詢內容";
    copyButton.disabled = copying || !clean(summaryText.value);
    copyStatus.textContent = summaryText.value ? "內容已修改，請確認後重新複製。" : "";
  });

  copyButton.addEventListener("click", async () => {
    if (copying || summaryCard.hidden || !clean(summaryText.value)) return;
    const version = summaryVersion;
    const text = summaryText.value;
    const stillCurrent = () => version === summaryVersion && !summaryCard.hidden && summaryText.value === text;
    copying = true;
    copyButton.disabled = true;
    copyButton.textContent = "正在複製…";
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        copied = true;
      } else copied = fallbackCopy();
    } catch (_) {
      // A rejected older copy must never select or copy an already-invalidated summary.
      if (stillCurrent()) copied = fallbackCopy();
    } finally {
      copying = false;
      copyButton.disabled = summaryCard.hidden || !clean(summaryText.value);
      if (!stillCurrent()) {
        copyButton.textContent = "複製諮詢內容";
      } else {
        copyButton.textContent = copied ? "已複製" : "請長按複製";
        copyStatus.textContent = copied
          ? "已複製。請開啟官方 LINE，自行貼上後送出；本頁尚未傳送資料。"
          : "瀏覽器無法直接複製，請長按上方文字選取並複製，再貼至官方 LINE。";
      }
    }
  });

  if (idToggle) idToggle.addEventListener("click", event => {
    event.preventDefault();
    setIdVisible(idInput ? idInput.type === "password" : false);
  });

  form.addEventListener("reset", () => {
    clearSummary();
    if (formStatus) formStatus.textContent = "";
    setIdVisible(false);
    if (includeFullId) includeFullId.checked = false;
    if (birthday) {
      birthday.setCustomValidity("");
      birthday.max = todayInTaipei();
    }
    if (ageInput) ageInput.readOnly = false;
    // Do not read the old birthday here: the browser resets native values after this event.
  });

  clearSummary();
  setIdVisible(false);
  if (includeFullId) includeFullId.checked = false;
  syncBirthday();
  if (generateButton) generateButton.disabled = false;
})();
