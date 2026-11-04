'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.join(__dirname, '..');
const privacy = require('../assets/consult-privacy.js');
const html = fs.readFileSync(path.join(root, 'consult/index.html'), 'utf8');
const script = fs.readFileSync(path.join(root, 'assets/consult.js'), 'utf8');

// Synthetic test values only; these are not customer records.
test('redacts national/old/new residence ID shapes, case, spacing, fullwidth and zero-width', () => {
  for (const id of ['A123456789','b223456789','AB12345678','A812345678','a-1 2 3 4 5 6 7 8 9','Ａ１２３４５６７８９','A\u200b123456789','A—123—456—789']) {
    const result = privacy.redact(`備註：${id}，請聯絡`);
    assert.equal(result.removed, true, id);
    assert.equal(result.text, '備註:〔已移除疑似證件號碼〕,請聯絡');
    assert.equal(privacy.redact(result.text).text, result.text);
  }
});
test('removes long account/card candidates but preserves contact and assessment', () => {
  assert.equal(privacy.redact('卡號 4111 1111 1111 1111').removed, true);
  assert.equal(privacy.redact('帳號 12345678901234').removed, true);
  const normal = '手機:0912345678\n車型:Toyota 2020\n金額:10 萬元\n收入:3 萬至未滿 5 萬元';
  assert.equal(privacy.redact(normal).text, normal);
});
test('optional mobile validation accepts common Taiwan formats and rejects ID strings', () => {
  for (const v of ['', '0912-345-678', '+886 912345678','０９１２３４５６７８']) assert.equal(privacy.mobile(v).valid, true);
  assert.equal(privacy.mobile('+886912345678').text, '0912345678');
  for (const v of ['A123456789','abc','09123','1234567890123456']) assert.equal(privacy.mobile(v).valid, false);
});

function setup({clipboard, fallback = true, query = ''} = {}) {
  const nodes = new Map();
  const fields = {};
  const handlers = {};
  let selectionCount = 0, fallbackCount = 0;
  for (const match of html.matchAll(/<(input|select|textarea)\b([^>]+)>/g)) {
    const attrs = match[2];
    const id = /\bid="([^"]+)"/.exec(attrs)?.[1];
    if (!id) continue;
    const name = /\bname="([^"]+)"/.exec(attrs)?.[1];
    if (name) fields[name] = id;
  }
  const node = id => {
    if (!nodes.has(id)) nodes.set(id, {
      value:'', checked:false, disabled:false, hidden:false, validity:'', textContent:'',
      addEventListener(type, fn) { (handlers[id+':'+type] ??= []).push(fn); },
      setCustomValidity(text) { this.validity=text; },
      focus(){},scrollIntoView(){},select(){selectionCount++;},setSelectionRange(){},
    });
    return nodes.get(id);
  };
  for(const id of [...Object.values(fields),'summary-text','consult-form','service-type','review-summary','copy-summary','consult-summary','form-status','copy-status','generate-summary','summary-heading','clear-after-copy'])node(id);
  const fire = async (id,type,event={}) => {
    for(const fn of handlers[id+':'+type]??[])await fn({preventDefault(){},...event});
  };
  const form = node('consult-form');
  form.reportValidity = () => ![...nodes.values()].some(n=>n.validity) && Boolean(node('consult-name').value && node('service-type').value);
  form.reset = () => {
    for(const fn of handlers['consult-form:reset']??[])fn({});
    for(const id of Object.values(fields))node(id).value='';
  };
  const win = {ConsultPrivacy:privacy, location:{search:query}, isSecureContext:true, matchMedia:()=>({matches:true}),addEventListener:(type,fn)=>{handlers['window:'+type]=[fn];}};
  const blocked = () => {throw new Error('Unexpected network/storage access');};
  const document = {querySelector:s=>node(s.slice(1)),execCommand:()=>{fallbackCount++;return fallback;}};
  const context = {window:win,document,navigator:{clipboard,sendBeacon:blocked},URLSearchParams,Intl,
    FormData:class {constructor(){this.data=Object.fromEntries(Object.entries(fields).map(([n,id])=>[n,node(id).value]));}get(n){return this.data[n]??null;}},
    fetch:blocked,XMLHttpRequest:blocked,WebSocket:blocked,localStorage:new Proxy({}, {get:blocked,set:blocked}),sessionStorage:new Proxy({}, {get:blocked,set:blocked}),indexedDB:new Proxy({}, {get:blocked})};
  vm.runInNewContext(script,context);
  const fill = (name,value) => {node(fields[name]).value=value;};
  const generate = async (extra={}) => {fill('name','測試暱稱');fill('service','car');for(const [n,v]of Object.entries(extra))fill(n,v);await fire('consult-form','submit');};
  const review = async () => {node('review-summary').checked=true;await fire('review-summary','change');};
  return {node,fill,fire,generate,review,fields,counts:()=>({selectionCount,fallbackCount})};
}

test('minimal inquiry works without phone; omits optional and removed fields', async () => {
  const h=setup();await h.generate();const s=h.node('summary-text').value;
  assert.match(s,/測試暱稱/);assert.match(s,/汽車借款/);assert.match(s,/LINE 對話聯絡/);
  assert.doesNotMatch(s,/未填寫|生日|身分證|戶籍|公司|警示|銀行貸款|每月收入/);
  assert.equal(h.node('copy-summary').disabled,true);
});
test('retains optional amount, phone, collateral and broad assessment', async () => {
  const h=setup();await h.generate({phone:'+886912345678',amount:'10.5',collateral:'Toyota 2020',incomeRange:'3 萬至未滿 5 萬元',repaymentRange:'未滿 1 萬元'});
  const s=h.node('summary-text').value;
  for(const expected of ['0912345678','10.5 萬元','Toyota 2020','每月收入區間','每月現有還款總額區間'])assert.ok(s.includes(expected));
});
test('all retained free text is sanitized; legacy injected fields are ignored', async () => {
  const h=setup();h.fields.idNumber='legacy-id';h.node('legacy-id').value='A123456789';
  await h.generate({collateral:'AB12345678',notes:'Ｂ２２３４５６７８９'});
  assert.doesNotMatch(h.node('summary-text').value,/A123456789|AB12345678|B223456789/);
  assert.match(h.node('copy-status').textContent,/移除/);
});
test('whitespace nickname and invalid phone cannot generate', async () => {
  const h=setup();await h.generate({phone:'A123456789'});assert.equal(h.node('consult-summary').hidden,true);
  await h.fire('consult-form','input');await h.generate({phone:'',name:'   '});assert.equal(h.node('consult-summary').hidden,true);
});
test('clipboard requires review and receives exactly the redacted preview', async () => {
  const writes=[];const h=setup({clipboard:{writeText:async s=>writes.push(s)}});
  await h.generate({notes:'證號 A123456789'});await h.fire('copy-summary','click');assert.equal(writes.length,0);
  await h.review();await h.fire('copy-summary','click');assert.deepEqual(writes,[h.node('summary-text').value]);assert.match(h.node('copy-status').textContent,/尚未送出/);
});
test('copy boundary re-redacts a tampered summary and requires a new review', async () => {
  const writes=[];const h=setup({clipboard:{writeText:async s=>writes.push(s)}});await h.generate();await h.review();
  h.node('summary-text').value+=' A123456789';await h.fire('copy-summary','click');assert.equal(writes.length,0);assert.equal(h.node('review-summary').checked,false);assert.doesNotMatch(h.node('summary-text').value,/A123456789/);
});
test('input and change invalidate old summaries and review state',async()=>{
  const h=setup();await h.generate();await h.review();await h.fire('consult-form','input');
  assert.equal(h.node('summary-text').value,'');assert.equal(h.node('consult-summary').hidden,true);assert.equal(h.node('copy-summary').disabled,true);assert.equal(h.node('review-summary').checked,false);
});
test('clipboard denied falls back; full failure selects text and explains manual copy',async()=>{
  for(const fallback of [true,false]){
    const h=setup({clipboard:{writeText:async()=>{throw new Error('denied');}},fallback});await h.generate();await h.review();await h.fire('copy-summary','click');
    assert.equal(h.counts().fallbackCount,1);assert.equal(h.counts().selectionCount,1);assert.match(h.node('copy-status').textContent,fallback?/已複製/:/長按/);
  }
});
test('pending copy cannot trigger fallback after reset or overwrite a new state',async()=>{
  let reject;const h=setup({clipboard:{writeText:()=>new Promise((_,r)=>reject=r)}});await h.generate();await h.review();
  const pending=h.fire('copy-summary','click');h.node('consult-form').reset();reject(new Error('denied'));await pending;
  assert.equal(h.counts().fallbackCount,0);assert.equal(h.node('summary-text').value,'');assert.equal(h.node('copy-summary').disabled,true);assert.match(h.node('form-status').textContent,/剪貼簿/);
});
test('clear and back-forward restoration remove entered values and retain only service hint',async()=>{
  const h=setup({query:'?type=gold&name=DO_NOT_IMPORT&phone=0912345678'});assert.equal(h.node('service-type').value,'gold');assert.equal(h.node('consult-name').value,'');
  await h.generate();await h.fire('clear-after-copy','click');assert.equal(h.node('consult-name').value,'');assert.equal(h.node('summary-text').value,'');
  await h.generate();await h.fire('window','pagehide');await h.fire('window','pageshow',{persisted:true});assert.equal(h.node('consult-name').value,'');assert.equal(h.node('service-type').value,'gold');
});
test('HTML prohibits form/network submission, has only intended controls and fixed LINE destinations',()=>{
  assert.match(html,/connect-src 'none'/);assert.match(html,/form-action 'none'/);assert.match(html,/name="referrer" content="no-referrer"/);
  assert.doesNotMatch(html,/onsubmit=|include-full-id|name="idNumber"|type="file"|type="password"|name="birthDate"|name="registeredAddress"|name="bankLoans"/);
  const names=[...html.matchAll(/<(?:input|select|textarea)\b[^>]*\bname="([^"]+)"/g)].map(m=>m[1]).sort();
  assert.deepEqual(names,['name','phone','region','contactTime','service','amount','purpose','collateral','financing','notes','incomeRange','repaymentRange'].sort());
  const required=[...html.matchAll(/<(?:input|select|textarea)\b[^>]*\brequired\b[^>]*>/g)];assert.equal(required.length,2);
  for(const m of html.matchAll(/href="(https:\/\/line.me[^\"]+)"/g))assert.equal(m[1],'https://line.me/R/ti/p/@104faknx');
  for(const file of ['consult.js','consult-privacy.js','tm.js'])assert.doesNotMatch(fs.readFileSync(path.join(root,'assets',file),'utf8'),/fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket|localStorage|sessionStorage|indexedDB|document\.cookie/);
});
