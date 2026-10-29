import {validateTenant} from './model.mjs';
const q=s=>document.querySelector(s);
let timer;
function toast(text){const t=q('#toast');t.textContent=text;t.hidden=false;clearTimeout(timer);timer=setTimeout(()=>t.hidden=true,4200);}
const icons={phone:'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 20 20 0 0 1-8.7-3.1 20 20 0 0 1-6.2-6.2A20 20 0 0 1 1.8 4a2 2 0 0 1 2-2.2h3a2 2 0 0 1 2 1.7l.5 3a2 2 0 0 1-.6 2.1L7.4 9.9a16 16 0 0 0 6.2 6.2l1.3-1.3a2 2 0 0 1 2.1-.6l3 .5a2 2 0 0 1 2 2.2z"/>',line:'<path d="M21 10c0 4.4-4.1 8-9 8l-4 3 1-3.5C5 16.5 3 13.5 3 10c0-4.4 4-7 9-7s9 2.6 9 7z"/><path d="M8 9v3h2m3-3v3m3-3v3"/>'};
function contactAction(id,href,kind,label){const old=q(id);const el=document.createElement(href?'a':'button');el.id=old.id;el.className=old.className;if(href){el.href=href;if(kind==='line'){el.target='_blank';el.rel='noopener noreferrer';}}else{el.disabled=true;}el.innerHTML=`<svg viewBox="0 0 24 24" aria-hidden="true">${icons[kind]}</svg><span></span>`;el.lastChild.textContent=label;if(!href){const sub=document.createElement('small');sub.className='sub';sub.textContent='待確認後開放';el.lastChild.append(sub);}old.replaceWith(el);}
function linkRow(id,url){const el=q(id);if(url){el.href=url;el.hidden=false;const hint=el.querySelector('small');if(hint)hint.textContent=new URL(url).hostname;}else el.hidden=true;}
export function renderProfile(company,card,{preview=false}={}){
 document.title=`${card.name}｜${company.companyName}電子名片`;
 q('#company-name').textContent=company.companyName;q('#person-name').textContent=card.name;q('#person-title').textContent=card.title;q('#intro').textContent=card.intro;q('#profile-note').textContent=card.note;
 document.documentElement.style.setProperty('--accent',company.accent);
 const avatar=q('#avatar');avatar.replaceChildren();if(company.logo){const img=document.createElement('img');img.src=company.logo;img.alt=company.companyName+' Logo';img.addEventListener('error',()=>{avatar.textContent=card.name.slice(0,1);},{once:true});avatar.append(img);}else avatar.textContent=card.name.slice(0,1);
 contactAction('#phone-action',card.phone?'tel:'+card.phone.replace(/[ ()-]/g,''):'','phone','電話聯繫');contactAction('#line-action',card.line,'line','加入 LINE');
 linkRow('#website-link',card.website);
 const mail=q('#email-link');mail.hidden=!card.email;mail.href=card.email?'mailto:'+card.email:'#';q('#email-text').textContent=card.email;
 const addr=q('#address-row');addr.hidden=!card.address;q('#address-text').textContent=card.address;
 const socials=q('#socials');socials.replaceChildren();for(const [f,label] of [['facebook','Facebook'],['instagram','Instagram'],['threads','Threads']]){if(card[f]){const a=document.createElement('a');a.textContent=label+' ↗';a.href=card[f];a.target='_blank';a.rel='noopener noreferrer';socials.append(a);}}
 const tags=q('#tags');tags.replaceChildren();for(const tag of card.services){const el=document.createElement('span');el.className='tag';el.textContent=tag;tags.append(el);}q('#services-section').hidden=!card.services.length;
 q('#save-contact').setAttribute('download',`${company.companyId}-${card.cardId}.vcf`);
 if(preview){q('#save-contact').removeAttribute('href');q('#save-contact').setAttribute('aria-disabled','true');q('#save-contact').onclick=e=>{e.preventDefault();toast('這是本機預覽；請先匯出設定並由管理者發布。');};q('#share-button').disabled=true;document.querySelector('.topbar').hidden=true;}
}
async function boot(){try{const src=document.body.dataset.profile;if(!src)return;const response=await fetch(src,{cache:'no-cache'});if(!response.ok)throw new Error('名片資料讀取失敗');const t=validateTenant(await response.json());const c=t.cards[0];renderProfile(t,c);q('#save-contact').href=document.body.dataset.vcard;q('#save-contact').addEventListener('click',()=>toast('開啟 .vcf 後，請選擇「建立新聯絡人」；若下載檔案，請從檔案開啟。'));}catch(error){q('#load-error').hidden=false;q('#load-error').textContent='暫時無法載入名片資料，請重新整理。';}}
q('#share-button')?.addEventListener('click',()=>{const url=q('link[rel="canonical"]')?.href||location.href;q('#share-url').value=url;q('#share-dialog').showModal();});
q('#close-dialog')?.addEventListener('click',()=>q('#share-dialog').close());
q('#share-dialog')?.addEventListener('click',e=>{if(e.target===q('#share-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
q('#copy-url')?.addEventListener('click',async()=>{const input=q('#share-url');try{await navigator.clipboard.writeText(input.value);toast('名片網址已複製');}catch{input.focus();input.select();toast('請長按或使用複製指令，複製選取的網址');}});
q('#native-share')?.addEventListener('click',async()=>{if(!navigator.share){toast('此瀏覽器請使用「複製名片網址」');return;}try{await navigator.share({title:document.title,url:q('#share-url').value});}catch(e){if(e.name!=='AbortError')toast('分享未完成，請複製網址。');}});
if(document.body.dataset.preview==='true'){
 window.addEventListener('message',e=>{if(e.origin!==location.origin||e.source!==parent||e.data?.type!=='card-preview')return;try{const t=validateTenant(e.data.tenant);const c=t.cards.find(c=>c.cardId===e.data.cardId);if(c)renderProfile(t,c,{preview:true});}catch{}});
 parent.postMessage({type:'preview-ready'},location.origin);
}else boot();
