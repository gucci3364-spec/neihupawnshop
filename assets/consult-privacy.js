"use strict";
((root) => {
  const clean = value => String(value ?? "").normalize("NFKC")
    .replace(/[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]/g, "")
    .replace(/\r/g, "").trim();
  // Conservative aid, not a guarantee. No checksum requirement: typos also redact.
  function redact(value) {
    let removed = false;
    const replace = () => { removed = true; return "〔已移除疑似證件號碼〕"; };
    const text = clean(value)
      .replace(/[A-Z][\s.\-－–—]*[A-Z](?:[\s.\-－–—]*\d){8}|[A-Z](?:[\s.\-－–—]*\d){9}/gi, replace)
      .replace(/\d(?:[ \t.\-－–—]*\d){11,}/g, () => {
        removed = true;
        return "〔已移除疑似帳號或卡號〕";
      });
    return { text, removed };
  }
  function mobile(value) {
    const text = clean(value).replace(/[\s()\-]/g, "");
    if (!text) return { valid: true, text: "" };
    if (/^09\d{8}$/.test(text)) return { valid: true, text };
    if (/^\+8869\d{8}$/.test(text)) return { valid: true, text: "0" + text.slice(4) };
    return { valid: false, text: "" };
  }
  const api = Object.freeze({ clean, redact, mobile });
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ConsultPrivacy = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
