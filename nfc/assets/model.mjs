export const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const URL_FIELDS = ['line','website','facebook','instagram','threads'];
function str(v, name, max=500, required=false) {
  if (typeof v !== 'string' || v.length > max || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(v) || (required && !v.trim())) throw new Error(`${name} 格式不正確`);
  return v.trim();
}
export function httpsUrl(v, name='網址') {
  if (!v) return '';
  let u; try { u = new URL(v); } catch { throw new Error(`${name} 請填寫完整 HTTPS 網址`); }
  if (u.protocol !== 'https:' || !u.hostname || u.username || u.password || /[\r\n]/.test(v)) throw new Error(`${name} 只接受 HTTPS 網址`);
  return u.href;
}
export function validateTenant(input) {
  if (!input || typeof input !== 'object' || input.schemaVersion !== 1) throw new Error('不支援的設定檔版本');
  const companyId = str(input.companyId,'公司代碼',48,true);
  if (!SLUG.test(companyId)) throw new Error('公司代碼限小寫英數與連字號');
  const companyName = str(input.companyName,'公司名稱',80,true);
  let logo=str(input.logo??'','Logo',1500000);
  if(logo && !/^data:image\/(png|jpeg|webp);base64,[a-zA-Z0-9+/=]+$/.test(logo)) logo=httpsUrl(logo,'Logo');
  const accent=str(input.accent??'#a65d43','主色',7);
  if(!/^#[a-fA-F0-9]{6}$/.test(accent)) throw new Error('主色格式不正確');
  if(!Array.isArray(input.cards) || input.cards.length<1 || input.cards.length>100) throw new Error('每個設定檔需有 1–100 張名片');
  const ids=new Set();
  const cards=input.cards.map(c=>{
    if(!c||typeof c!=='object') throw new Error('名片格式不正確');
    const cardId=str(c.cardId,'名片代碼',48,true);
    if(!SLUG.test(cardId)||ids.has(cardId)) throw new Error('名片代碼格式錯誤或重複');
    ids.add(cardId);
    const o={cardId,name:str(c.name,'姓名',80,true),title:str(c.title??'','職稱',100),intro:str(c.intro??'','介紹',600)};
    o.phone=str(c.phone??'','電話',40);
    if(o.phone&&!/^\+?[0-9 ()-]{5,30}$/.test(o.phone)) throw new Error('電話格式不正確');
    o.email=str(c.email??'','Email',160);
    if(o.email&&!/^[^\s@;,]+@[^\s@;,]+\.[^\s@;,]+$/.test(o.email)) throw new Error('Email 格式不正確');
    for(const f of URL_FIELDS) o[f]=httpsUrl(str(c[f]??'',f,600),f);
    o.address=str(c.address??'','地址',200);
    o.note=str(c.note??'','備註',300);
    if(!Array.isArray(c.services)||c.services.length>12) throw new Error('服務項目最多 12 項');
    o.services=c.services.map(s=>str(s,'服務項目',30,true));
    return o;
  });
  return {schemaVersion:1,companyId,companyName,logo,accent,cards};
}
export function escapeHtml(s) { return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function vc(s) { return String(s).replace(/\\/g,'\\\\').replace(/\r\n|\n|\r/g,'\\n').replace(/;/g,'\\;').replace(/,/g,'\\,'); }
export function foldLine(line) {
  const rows=[]; let row='',bytes=0;
  for(const c of line){const n=new TextEncoder().encode(c).length;if(bytes+n>75){rows.push(row);row=' ';bytes=1;}row+=c;bytes+=n;}
  rows.push(row);return rows.join('\r\n');
}
export function vcard(company, card, cardUrl) {
  const lines=['BEGIN:VCARD','VERSION:3.0',`N:${vc(card.name)};;;;`,`FN:${vc(card.name)}`,`ORG:${vc(company.companyName)}`,`TITLE:${vc(card.title)}`];
  if(card.phone) lines.push(`TEL;TYPE=WORK,VOICE:${card.phone.replace(/[ ()-]/g,'')}`);
  if(card.email) lines.push(`EMAIL;TYPE=INTERNET,WORK:${vc(card.email)}`);
  if(card.website) lines.push(`URL:${vc(card.website)}`);
  if(card.address) lines.push(`ADR;TYPE=WORK:;;${vc(card.address)};;;;`);
  const notes=[card.intro,card.line?`LINE: ${card.line}`:'',card.facebook?`Facebook: ${card.facebook}`:'',card.instagram?`Instagram: ${card.instagram}`:'',card.threads?`Threads: ${card.threads}`:'',cardUrl?`電子名片: ${cardUrl}`:''].filter(Boolean).join('\n');
  if(notes) lines.push(`NOTE:${vc(notes)}`);
  lines.push('END:VCARD'); return lines.map(foldLine).join('\r\n')+'\r\n';
}
