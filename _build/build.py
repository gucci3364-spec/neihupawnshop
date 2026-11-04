#!/usr/bin/env python3
"""台茂當舖官網建置腳本。

用法：python3 _build/build.py
- 重新產生 index.html、services/、about/、sitemap.xml、llms.txt、robots.txt
- 套用新外觀到 faq/、updates/、consult/（保留原本內文與表單邏輯）
- 保留自動發文用的 <!--LATEST--> / <!--POSTS--> 標記
改網址（例如日後換成自有網域）只要改下面的 BASE，再執行一次即可。
"""
import html, json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://gucci3364-spec.github.io/neihupawnshop/"     # ← 換網域時只改這行
OLD_BASE = "https://gucci3364-spec.github.io/neihupawnshop/"
LINE = "https://line.me/R/ti/p/@104faknx"
TEL, TEL_HREF = "02-8792-1111", "tel:0287921111"
ADDR = "台北市內湖區成功路三段88號"
PLACE_ID = "ChIJi1I1J46tQjQRYBXHGyKJFkM"
MAP_Q = "%E5%8F%B0%E8%8C%82%E7%95%B6%E8%88%96%20%E5%8F%B0%E5%8C%97%E5%B8%82%E5%85%A7%E6%B9%96%E5%8D%80%E6%88%90%E5%8A%9F%E8%B7%AF%E4%B8%89%E6%AE%B588%E8%99%9F"
MAP_VIEW = f"https://www.google.com/maps/search/?api=1&query={MAP_Q}&query_place_id={PLACE_ID}"
MAP_DIR = f"https://www.google.com/maps/dir/?api=1&destination={MAP_Q}&destination_place_id={PLACE_ID}"
MAP_REVIEW = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"
FB = "https://www.facebook.com/61584792693374"
TODAY = datetime.date.today().isoformat()
OG = BASE + "assets/og-taimao.jpg"

def w(path, s):
    if path.endswith(".html"):
        s = clean_headings(s)
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def r(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()

def e(s):
    return html.escape(s, quote=True)

def nopunct_text(t):
    """標題不放逗號、句號：句尾的拿掉，句中的逗號換成空格。"""
    t = t.replace("。", "").replace("，", " ")
    return re.sub(r" {2,}", " ", t).strip() if t.strip() != t else re.sub(r" {2,}", " ", t)

def clean_headings(h):
    def fix(m):
        inner = re.sub(r"[，。]\s*(?=<br)", "", m.group(3))
        parts = re.split(r"(<[^>]*>)", inner)
        inner = "".join(x if x.startswith("<") else nopunct_text(x) for x in parts)
        return f"<{m.group(1)}{m.group(2)}>{inner}</{m.group(1)}>"
    return re.sub(r"<(h[1-3])([^>]*)>(.*?)</\1>", fix, h, flags=re.S)

# ── 圖示（Lucide，ISC 授權） ─────────────────────────────
def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')
IC = {
 "car": '<path d="m21 8-2 2-1.5-3.7A2 2 0 0 0 15.646 5H8.4a2 2 0 0 0-1.903 1.257L5 10 3 8"/><path d="M7 14h.01"/><path d="M17 14h.01"/><rect width="18" height="8" x="3" y="10" rx="2"/><path d="M5 18v2"/><path d="M19 18v2"/>',
 "bike": '<circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/>',
 "gem": '<path d="M10.5 3 8 9l4 13 4-13-2.5-6"/><path d="M17 3a2 2 0 0 1 1.6.8l3 4a2 2 0 0 1 .013 2.382l-7.99 10.986a2 2 0 0 1-3.247 0l-7.99-10.986A2 2 0 0 1 2.4 7.8l2.998-3.997A2 2 0 0 1 7 3z"/><path d="M2 9h20"/>',
 "watch": '<path d="M12 10v2.2l1.6 1"/><path d="m16.13 7.66-.81-4.05a2 2 0 0 0-2-1.61h-2.68a2 2 0 0 0-2 1.61l-.78 4.05"/><path d="m7.88 16.36.8 4a2 2 0 0 0 2 1.61h2.72a2 2 0 0 0 2-1.61l.81-4.05"/><circle cx="12" cy="12" r="6"/>',
 "bag": '<path d="M16 10a4 4 0 0 1-8 0"/><path d="M3.103 6.034h17.794"/><path d="M3.4 5.467a2 2 0 0 0-.4 1.2V20a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6.667a2 2 0 0 0-.4-1.2l-2-2.667A2 2 0 0 0 17 2H7a2 2 0 0 0-1.6.8z"/>',
 "phone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
 "tel": '<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>',
 "chat": '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/>',
 "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
}

SERVICES = [  # id, icon, 名稱, 一句話, 標籤, 諮詢參數, 延伸
 ("car", "car", "汽車借款", "汽車借款先了解車況與需求。原車、分期車皆可先洽詢評估。", ["原車評估", "分期車可洽詢", "條件說明"], "car", "faq/car-loan-outstanding/", "車貸尚未繳完的常見問題"),
 ("motorcycle", "bike", "機車借款", "機車借款先了解車況、權利狀態與資金需求，再說明評估結果及辦理條件。", ["機車・重機", "小額周轉"], "motorcycle", "faq/motorcycle-pawn/", "機車借款的準備資料"),
 ("gold", "gem", "黃金・珠寶", "珍惜物品，也看見它的價值。依重量、成色與品項現場鑑定。", ["金飾・金條", "鑽石・珠寶"], "gold", "faq/gold-valuation/", "黃金典當如何估價"),
 ("watch", "watch", "名錶典當", "從品牌、型號到保存狀態，仔細了解每一只腕錶的條件。", ["名錶評估", "附件一併提供"], "watch", "https://gucci3364-spec.github.io/WATCH/", "查看既有名錶專區"),
 ("bags", "bag", "精品包款", "讓收藏多一種運用方式。品牌、款式與保存情形都是評估重點。", ["精品皮件", "專人洽詢"], "bags", "https://gucci3364-spec.github.io/BAGS/", "查看既有精品包專區"),
 ("devices", "phone", "3C 數位產品", "手機、平板、筆電與相機，先提供型號與使用狀況了解收當條件。", ["手機・筆電", "相機・平板"], "devices", "https://gucci3364-spec.github.io/3c/", "查看既有 3C 專區"),
]
SERVICE_TIPS = {
 "car": ["先說明品牌、車款、年份與大約里程。", "有車貸或設定時，可先整理目前繳款與剩餘貸款狀況。", "實際評估與準備文件，由專人依車籍和個案說明。"],
 "motorcycle": ["先提供品牌、車型、出廠年份與使用狀況。", "說明車輛是否本人名下，以及是否仍有分期。", "先詢問應備資料，再安排後續評估與到店。"],
 "gold": ["可先說明是金飾、金條、金幣或其他珠寶。", "知道重量、純度或有購買證明時，可一併告知。", "實際重量與材質仍需確認，再由專人說明估價。"],
 "watch": ["先提供品牌、型號與大約購入年份。", "說明是否有盒單、保卡、附件及維修紀錄。", "外觀、機芯狀況與附件，需實際檢視後再評估。"],
 "bags": ["先說明品牌、款式、尺寸與使用情形。", "如有購買證明、盒袋或附件，可先告知。", "實際品況與附件會影響後續評估方式。"],
 "devices": ["先提供產品品牌、完整型號與規格。", "說明機況、外觀、配件與是否仍有分期。", "先確認收當條件，再依專人說明準備相關資料。"],
}

HOME_FAQ = [
 ("內湖當鋪台茂當舖在哪裡？電話是多少？",
  f"台茂當舖位於{ADDR}，電話 {TEL}，官方 LINE ID 為 @104faknx。到店前建議先以電話或 LINE 確認受理時間與準備事項。"),
 ("台茂當舖的營業時間是幾點？",
  f"台茂當舖 24 小時營業。到店前仍建議先以電話 {TEL} 或 LINE 聯繫，確認受理項目與要準備的文件。"),
 ("台茂當舖可以諮詢哪些物品？",
  "汽車、機車（含重機）、黃金珠寶、名錶、精品包與 3C 數位產品都可以先諮詢。實際收當品項、額度與費用，依個案評估及契約約定。"),
 ("第一次去當舖要準備什麼？",
  "通常需要本人身分證及第二證件；汽機車可先備妥行照，精品、黃金或名錶如有購買證明與附件，也請一併提供。實際文件由專人依案件說明。"),
 ("當舖利息與費用有法定上限嗎？",
  "有。依《當舖業法》第 11 條，營業場所揭示的年利率最高不得超過 30%；依第 20 條，除利息與倉棧費外不得收取其他費用，倉棧費最高不得超過收當金額的 5%。以上是法律上限，不代表台茂的實際報價，辦理前請逐項確認並核對當票。"),
 ("怎麼判斷內湖當鋪是否合法、值得信任？",
  "合法當舖應在營業場所明顯處揭示許可證、利率、利息計算方式與營業時間。到店前可先核對店名、地址與聯絡方式是否一致；簽約前核對當票內容，不清楚的項目請對方用文字寫清楚，不要空白簽名。"),
 ("汽車、機車還有貸款，可以先詢問嗎？",
  "可以先洽詢。專人會了解車款、年份、車況、權利狀態與目前貸款情形，再說明評估結果、費用及辦理方式，確認條件後再決定是否辦理。網頁介紹不代表核准額度或報價。"),
 ("可以先用 LINE 問，不用直接到店嗎？",
  "可以。先提供物品種類、型號與狀況，讓專人了解需求，再安排後續評估。請勿在公開留言區或初次聯絡時提供身分證字號、帳號或完整證件照片。"),
 ("物品典當之後還可以贖回嗎？",
  "典當與直接出售不同。贖回時間、應繳金額與相關程序，依當票及契約約定辦理；如需續當或調整安排，請提早聯繫專人確認。"),
]

HOME_FAQ = [(nopunct_text(q), a) for q, a in HOME_FAQ]

NAV = [("服務項目", "services/"), ("辦理流程", "#process"), ("常見問題", "#faq"), ("金融知識", "faq/"), ("最新消息", "updates/"), ("關於台茂", "about/"), ("諮詢表單", "consult/")]

def nav_links(R, active=""):
    out = []
    for name, href in NAV:
        cur = ' aria-current="page"' if active and href.strip("/") == active else ""
        out.append(f'<a href="{R}{href}"{cur}>{name}</a>')
    return "".join(out)

def header(R, active=""):
    links = nav_links(R, active)
    return f'''<a class="skip-link" href="#main">跳至主要內容</a>
<header class="tm-header"><div class="wrap tm-head-row">
<a class="brand" href="{R or './'}" aria-label="台茂當舖首頁"><span class="brand-mark" aria-hidden="true">當</span><span class="brand-text"><strong>台茂當舖</strong><small>TAIMAO PAWN SHOP</small></span></a>
<nav class="tm-nav" aria-label="主選單">{links}</nav>
<a class="btn btn-gold tm-head-cta" href="{LINE}" target="_blank" rel="noopener noreferrer">LINE 諮詢</a>
<button class="menu-btn" type="button" aria-controls="tm-panel" aria-expanded="false" aria-label="開啟選單"><span></span><span></span><span></span></button>
</div>
<nav class="tm-panel" id="tm-panel" aria-label="手機選單">{links}<a class="btn btn-gold" href="{LINE}" target="_blank" rel="noopener noreferrer">LINE 專人諮詢</a><a class="panel-tel" href="{TEL_HREF}">電話 {TEL}</a></nav>
</header>'''

def footer(R):
    return f'''<footer class="tm-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="{R or './'}"><span class="brand-mark" aria-hidden="true">當</span><span class="brand-text"><strong>台茂當舖</strong><small>TAIMAO PAWN SHOP</small></span></a><p>內湖在地當舖。汽機車、黃金珠寶、名錶、精品包與 3C，先說明流程與條件，再決定是否辦理。</p></div>
<div><h2 class="foot-h">店家資料</h2><address>台茂當舖（台茂當鋪）<br>{ADDR}<br>電話 <a href="{TEL_HREF}">{TEL}</a><br>LINE <a href="{LINE}" target="_blank" rel="noopener noreferrer">@104faknx</a><br>營業時間 24 小時</address></div>
<div><h2 class="foot-h">網站導覽</h2><ul><li><a href="{R}services/">服務項目</a></li><li><a href="{R}faq/">金融知識（{FAQ_TOTAL} 篇）</a></li><li><a href="{R}updates/">最新消息</a></li><li><a href="{R}about/">關於台茂</a></li><li><a href="{R}consult/">諮詢表單</a></li><li><a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook 粉絲專頁</a></li></ul></div>
<div><h2 class="foot-h">服務專區</h2><ul><li><a href="https://gucci3364-spec.github.io/taimaopawnshop/" target="_blank" rel="noopener noreferrer">汽車借款專區</a></li><li><a href="https://gucci3364-spec.github.io/motorcycle/" target="_blank" rel="noopener noreferrer">機車借款專區</a></li><li><a href="https://gucci3364-spec.github.io/gold/" target="_blank" rel="noopener noreferrer">黃金珠寶專區</a></li><li><a href="https://gucci3364-spec.github.io/WATCH/" target="_blank" rel="noopener noreferrer">名錶專區</a></li><li><a href="https://gucci3364-spec.github.io/BAGS/" target="_blank" rel="noopener noreferrer">精品包專區</a></li><li><a href="https://gucci3364-spec.github.io/3c/" target="_blank" rel="noopener noreferrer">3C 專區</a></li></ul></div>
</div>
<p class="foot-note">網頁介紹不代表核准額度或報價；實際收當品項、額度、費用與辦理方式，依個案評估及契約約定。借款前請衡量還款能力。<br>© 2026 台茂當舖 TAIMAO. All rights reserved.</p>
</div></footer>
<nav class="dock" aria-label="快速聯絡"><a href="{TEL_HREF}">{svg(IC["tel"])}撥打電話</a><a href="{LINE}" target="_blank" rel="noopener noreferrer">{svg(IC["chat"])}LINE 諮詢</a><a href="{MAP_DIR}" target="_blank" rel="noopener noreferrer">{svg(IC["pin"])}導航</a></nav>'''

FAVICON = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2064%2064%22%3E%3Crect%20width%3D%2264%22%20height%3D%2264%22%20rx%3D%2212%22%20fill%3D%22%230f1a16%22/%3E%3Ccircle%20cx%3D%2232%22%20cy%3D%2232%22%20r%3D%2225%22%20fill%3D%22none%22%20stroke%3D%22%23c9ad77%22%20stroke-width%3D%222%22/%3E%3Ctext%20x%3D%2232%22%20y%3D%2243%22%20text-anchor%3D%22middle%22%20fill%3D%22%23c9ad77%22%20font-family%3D%22serif%22%20font-size%3D%2233%22%3E%E7%95%B6%3C/text%3E%3C/svg%3E"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@500;700;900&display=swap">'

def head(title, desc, path, R, jsonld=None, og_type="website", extra=""):
    url = BASE + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in (jsonld or []))
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#0f1a16"><link rel="canonical" href="{url}"><meta name="geo.region" content="TW-TPE"><meta name="geo.placename" content="台北市內湖區"><meta name="geo.position" content="25.078598;121.5892963"><meta name="ICBM" content="25.078598, 121.5892963"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="台茂當舖"><meta property="og:locale" content="zh_TW"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{OG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="台茂當舖・內湖當舖"><meta name="twitter:card" content="summary_large_image">{extra}{FONTS}<link rel="stylesheet" href="{R}assets/tm.css?v=3"><link rel="icon" href="{FAVICON}">{ld}'''

def page(title, desc, path, R, body, active="", jsonld=None, og_type="website", extra="", body_class=""):
    return f'''<!doctype html>
<html lang="zh-Hant-TW"><head>{head(title, desc, path, R, jsonld, og_type, extra)}</head><body{(' class="%s"' % body_class) if body_class else ""}>
{header(R, active)}
{body}
{footer(R)}
<script src="{R}assets/tm.js?v=3" defer></script>
</body></html>
'''

# ── 結構化資料 ───────────────────────────────────────
BIZ = BASE + "#business"
def business_node():
    return {
     "@type": ["PawnShop", "LocalBusiness"], "@id": BIZ,
     "name": "台茂當舖", "alternateName": ["台茂當鋪", "台茂當舖 內湖", "Taimao Pawn Shop"],
     "url": BASE, "logo": BASE + "assets/og-taimao.jpg", "image": OG,
     "description": f"{ADDR}的台茂當舖，提供汽車、機車、黃金珠寶、名錶、精品包及 3C 典當諮詢與評估，24 小時營業，專人說明流程、費用與條件。",
     "telephone": "+886-2-8792-1111",
     "address": {"@type": "PostalAddress", "streetAddress": "成功路三段88號", "addressLocality": "內湖區", "addressRegion": "台北市", "postalCode": "114", "addressCountry": "TW"},
     "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
     "geo": {"@type": "GeoCoordinates", "latitude": 25.078598, "longitude": 121.5892963},
     "hasMap": MAP_VIEW,
     "areaServed": {"@type": "AdministrativeArea", "name": "台北市內湖區"},
     "sameAs": [FB, LINE, f"https://www.google.com/maps/place/?q=place_id:{PLACE_ID}"],
     "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": "+886-2-8792-1111", "availableLanguage": ["zh-TW"], "url": LINE}],
     "knowsAbout": ["內湖當舖", "汽車借款", "機車借款", "黃金典當", "名錶典當", "精品包典當", "3C 典當", "當舖業法"],
     "employee": {"@type": "Person", "name": "羅經理", "jobTitle": "經理", "worksFor": {"@id": BIZ}},
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "台茂當舖諮詢項目", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d, "url": BASE + "services/#" + i}} for i, _, n, d, *_ in SERVICES]},
    }

def website_node():
    return {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "台茂當舖", "inLanguage": "zh-Hant-TW", "publisher": {"@id": BIZ}}

def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def faq_node(qa):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

# ── 最新消息卡片（與自動發文 connectors/website.py 的輸出結構相同） ──────
def card(p, prefix, heading="h2"):
    img = f'{prefix}updates/img/{p["date"]}.jpg'
    pts = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    more = ""
    link = p.get("link") or ""
    if link.startswith(OLD_BASE):
        link = prefix + link[len(OLD_BASE):]
    if link:
        ext = ' target="_blank" rel="noopener noreferrer"' if link.startswith("http") else ""
        more = f'<a class="update-more" href="{e(link)}"{ext}>延伸閱讀 →</a>'
    return (f'<article class="update-card" id="d{p["date"]}">'
            f'<img src="{e(img)}" alt="{e(p["title"])}" width="540" height="675" loading="lazy">'
            f'<div class="update-body"><time datetime="{p["date"]}">{p["date"].replace("-", ".")}</time>'
            f'<{heading}>{e(p["title"])}</{heading}><p>{e(p["caption"])}</p><ul>{pts}</ul>{more}</div></article>')

def posts():
    return json.load(open(os.path.join(ROOT, "updates", "posts.json"), encoding="utf-8"))


# ═════════════ 首頁 ═════════════
def facts_dl():
    return f'''<dl class="facts">
<div><dt>店名</dt><dd><strong>台茂當舖</strong>（亦寫作「台茂當鋪」）</dd></div>
<div><dt>地址</dt><dd><strong>{ADDR}</strong></dd></div>
<div><dt>電話</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div>
<div><dt>LINE</dt><dd><a href="{LINE}" target="_blank" rel="noopener noreferrer">@104faknx</a>（官方帳號）</dd></div>
<div><dt>受理項目</dt><dd>汽車、機車・重機、黃金珠寶、名錶、精品包、3C 數位產品</dd></div>
<div><dt>營業時間</dt><dd><strong>24 小時營業</strong>（到店前歡迎先電話或 LINE 聯繫）</dd></div>
<div><dt>諮詢窗口</dt><dd>羅經理（專人評估與說明）</dd></div>
</dl>'''

def home():
    pl = posts()
    latest = "".join(card(p, "", "h3") for p in pl[:3])
    svc = "".join(
        f'<a class="svc" href="services/#{i}">{svg(IC[ic])}<div><h3>{n}</h3><p>{d}</p><div class="tags">{"".join(f"<span>{t}</span>" for t in tags)}</div></div><span class="go" aria-hidden="true">↗</span></a>'
        for i, ic, n, d, tags, *_ in SERVICES)
    faq = "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in HOME_FAQ)
    belt_items = "".join(f"<span>{t}</span>" for t in ["汽車借款", "機車・重機", "黃金珠寶", "名錶", "精品包", "3C 數位產品", "24 小時營業", "成功路三段 88 號"])
    body = f'''<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<h1>內湖當舖，<br>台茂當舖。</h1>
<p class="hero-sub">從了解您的需求開始</p>
<p class="hero-desc">位於台北市內湖區成功路三段88號。汽機車、黃金珠寶、名錶、精品包與 3C，先把流程與條件說清楚，同意了才辦理。</p>
<div class="hero-actions"><a class="btn btn-gold" href="{LINE}" target="_blank" rel="noopener noreferrer">{svg(IC["chat"])}LINE 專人諮詢</a><a class="btn btn-line" href="{TEL_HREF}">{svg(IC["tel"])}撥打 {TEL}</a></div>
</div>
<div class="hero-visual">
<img src="assets/hero-valuable-things.webp" alt="腕錶與黃金飾品的品牌情境示意" width="1536" height="1024" fetchpriority="high">
<div class="slip-wrap"><aside class="slip" aria-label="台茂當舖店家資料">
<div class="slip-top"><div class="slip-title">諮詢單<small>台茂當舖・內湖</small></div><div class="seal" aria-hidden="true">當</div></div>
<dl class="slip-rows">
<div><dt>地址</dt><dd style="--i:0">內湖區成功路三段88號</dd></div>
<div><dt>電話</dt><dd style="--i:1"><a href="{TEL_HREF}">{TEL}</a></dd></div>
<div><dt>LINE</dt><dd style="--i:2">@104faknx</dd></div>
<div><dt>時間</dt><dd style="--i:3">24 小時營業</dd></div>
<div><dt>想問</dt><dd style="--i:4"><span class="typer" data-words="汽車借款|機車借款|黃金珠寶|名錶|精品包|3C 產品">汽車借款</span></dd></div>
</dl>
<p class="slip-foot">專人評估・條件說明・重視隱私</p>
</aside></div>
</div>
</div></section>
<div class="belt" aria-hidden="true"><div class="belt-track">{belt_items}{belt_items}</div></div>

<section class="sec" id="info"><div class="wrap cols two">
<div>
<div class="sec-head"><h2>在內湖找當舖，<br>先確認地址與服務。</h2></div>
<p class="answer">想找<strong>內湖當鋪</strong>的實體店面？<strong>台茂當舖</strong>位於台北市內湖區成功路三段88號，<strong>24 小時營業</strong>，提供汽車、機車、黃金珠寶、名錶、精品包與 3C 的典當諮詢與評估。</p>
<p class="answer-more">到店前可先用電話或 LINE 說明物品，確認受理時間與要準備的文件。挑選當舖時，也請核對營業許可、利率揭示與當票內容，可先閱讀<a href="faq/neihu-pawnshop/">內湖當舖選擇與到店準備</a>。</p>
</div>
<div>
{facts_dl()}
<div class="fact-actions"><a class="btn btn-dark" href="{MAP_DIR}" target="_blank" rel="noopener noreferrer">{svg(IC["pin"])}Google 地圖導航</a><a class="btn btn-ghost" href="about/">更多店家資料</a></div>
</div>
</div></section>

<section class="sec dark" id="services"><div class="wrap">
<div class="sec-head"><h2>不同的資產，<br>都有值得了解的可能。</h2><p>依照您的物品與實際需求，一起評估合適的周轉方式。不確定適不適合，先問問我們。</p></div>
<div class="svc-list">{svc}</div>
<p class="sec-note">實際收當品項、額度、費用與辦理方式，依個案評估及契約約定。</p>
</div></section>

<section class="sec mist approach" id="approach"><span class="mark-bg" aria-hidden="true">當</span><div class="wrap cols approach-cols">
<div><h2>有些珍貴，<br>不必急著割捨。</h2><p class="lead">可能是陪您工作的車，也可能是一份捨不得出售的紀念。我們先聽您的故事，再談合適的方式。</p></div>
<div class="pledges">
<article><h3>尊重每一份託付</h3><p>仔細了解物品狀況與您的需求，讓評估有依據，讓溝通有溫度。</p></article>
<article><h3>先把條件說清楚</h3><p>借款金額、適用費用與還款安排，辦理前逐項了解，再做決定。</p></article>
<article><h3>有人可以好好商量</h3><p>從初次詢問到後續聯繫，由專人協助。關於您的疑問，歡迎直接提出。</p></article>
</div></div></section>

<section class="sec white" id="process"><div class="wrap">
<div class="sec-head"><h2>把流程說明白，<br>每一步都更踏實。</h2><p>第一次來也不用擔心。從一通電話或一則訊息開始。</p></div>
<ol class="steps">
<li><h3>聊聊需求</h3><p>透過電話或 LINE，說明需求與物品資訊。</p></li>
<li><h3>準備資料</h3><p>依專人說明，備妥本人證件及相關物品資料。</p></li>
<li><h3>評估與說明</h3><p>確認物品狀況，了解額度、費用及還款條件。</p></li>
<li><h3>確認後辦理</h3><p>確認同意條件後，依約完成手續與撥款。</p></li>
</ol></div></section>

<section class="sec" id="faq"><div class="wrap cols two">
<div class="sec-head"><h2>您的疑問，<br>我們先回答。</h2><p>以下是到內湖找當舖的人最常問的問題。還有其他想了解的，歡迎直接與台茂聯繫。</p><div class="fact-actions"><a class="btn btn-dark" href="{LINE}" target="_blank" rel="noopener noreferrer">{svg(IC["chat"])}LINE 詢問</a></div></div>
<div class="faq-list">{faq}</div>
</div></section>

<section class="sec white" id="updates"><div class="wrap">
<div class="sec-head"><h2>台茂每日小知識，<br>周轉前先看懂。</h2><p>每天一則典當與借款小知識，同步發布於 Facebook 與 Threads。<a class="link" href="updates/">看全部最新消息</a></p></div>
<div class="updates-grid"><!--LATEST-->{latest}<!--/LATEST--></div>
</div></section>

<section class="sec mist" id="knowledge"><div class="wrap cols two">
<div class="sec-head"><h2>常見借款問題，<br>先看羅經理的解答。</h2><p>在台北、內湖尋找當舖時，先了解物品評估、所需文件、費用與取贖方式。整理{ZH_NUM[FAQ_TOTAL]}篇常見問答，方便諮詢前閱讀。</p><div class="fact-actions"><a class="btn btn-dark" href="faq/">瀏覽 {FAQ_TOTAL} 篇金融知識</a></div></div>
<nav class="arrow-rows" aria-label="精選典當問答"><a href="faq/neihu-pawnshop/">內湖當鋪：地址與到店準備</a><a href="faq/neihu-24-hour-pawnshop/">內湖24小時當舖：營業時間與夜間到店</a><a href="faq/pawn-interest-fees/">當舖利息怎麼算？年利率與倉棧費</a><a href="faq/pawn-vs-bank-loan/">當舖和銀行信貸差在哪？</a><a href="faq/pawn-document-checklist/">第一次到當舖要帶什麼？</a></nav>
</div></section>

<section class="sec dark" id="consult"><div class="wrap callout">
<div><h2>先把需求整理好，<br>再和羅經理聊聊。</h2><p>選擇想了解的服務、填寫大致需求，產生一份可複製的諮詢摘要，再貼到台茂官方 LINE。內容由您確認後自行傳送，本站不會自動送出資料。</p></div>
<div class="fact-actions" style="margin:0"><a class="btn btn-gold" href="consult/">整理諮詢內容</a><a class="btn btn-line" href="services/">查看服務指南</a></div>
</div></section>

<section class="sec ink contact" id="contact"><div class="wrap contact-grid">
<div>
<h2 class="h2">周轉的事，<br>來台茂聊聊。</h2>
<a class="phone" href="{TEL_HREF}">{TEL}</a>
<p class="addr">{ADDR}<br>到店前歡迎先聯繫，我們說明準備事項。</p>
<div class="contact-actions"><a class="btn btn-gold" href="{LINE}" target="_blank" rel="noopener noreferrer">{svg(IC["chat"])}LINE 專人諮詢</a><a class="btn btn-line" href="{MAP_DIR}" target="_blank" rel="noopener noreferrer">{svg(IC["pin"])}開啟地圖導航</a></div>
<p class="addr" style="margin-top:16px;font-size:14px">官方 LINE ID：@104faknx</p>
</div>
<div class="map-panel"><iframe title="台茂當舖位置：{ADDR}" src="https://www.google.com/maps?q={MAP_Q}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
<div class="map-links"><a href="{MAP_VIEW}" target="_blank" rel="noopener noreferrer">成功路三段 88 號・Google 地圖</a><a href="{MAP_REVIEW}" target="_blank" rel="noopener noreferrer">在 Google 留下評論</a></div></div>
</div></section>
</main>'''
    title = "內湖當舖｜台北台茂當舖・汽機車、黃金與精品典當"
    desc = "台北內湖當舖諮詢：台茂當舖位於成功路三段88號，24小時營業，提供汽機車、黃金、名錶、精品與3C典當評估；電話02-8792-1111。"
    ld = [{"@context": "https://schema.org", "@graph": [
        business_node(), website_node(),
        {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": title, "description": desc, "inLanguage": "zh-Hant-TW",
         "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BIZ}, "mainEntity": {"@id": BIZ}, "dateModified": TODAY,
         "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "assets/hero-valuable-things.webp"}},
        faq_node(HOME_FAQ)]}]
    preload = f'<link rel="preload" as="image" href="assets/hero-valuable-things.webp" type="image/webp" fetchpriority="high">'
    return page(title, desc, "", "", body, jsonld=ld, extra=preload, body_class="home")

# ═════════════ 服務指南 ═════════════
def services():
    nav = "".join(f'<a href="#{i}">{n}</a>' for i, _, n, *_ in SERVICES)
    arts = ""
    for i, ic, n, d, tags, q, href, label in SERVICES:
        ext = href.startswith("http")
        link = f'<a class="link" href="{"" if ext else "../"}{href}"{" target=_blank rel=noopener" if ext else ""}>{label}</a>'
        lis = "".join(f"<li>{t}</li>" for t in SERVICE_TIPS[i])
        arts += (f'<article class="svc-detail" id="{i}">{svg(IC[ic])}<div class="col-l"><h2>{n}</h2><p class="desc">{d}</p></div>'
                 f'<div class="col-r"><h3>諮詢前，可先整理</h3><ul>{lis}</ul><div class="detail-links"><a class="btn btn-dark" href="../consult/?type={q}">諮詢這項服務</a>{link}</div></div></article>')
    body = f'''<section class="pagehead"><div class="wrap"><nav class="breadcrumbs" aria-label="麵包屑"><a href="../">台茂首頁</a> / 服務指南</nav>
<h1>先了解服務，<br>再準備合適的資料。</h1>
<p class="lead">汽機車、黃金、名錶、精品與 3C，各有不同的評估重點。選一個服務，先把想問的事情整理好，再和羅經理討論。台茂當舖位於台北市內湖區成功路三段88號，電話 {TEL}。</p></div></section>
<main class="wrap" id="main"><nav class="svc-nav" aria-label="服務分類">{nav}</nav>{arts}
<section class="widecta"><div><h2>還不確定是哪一項需求？</h2><p>選擇「其他需求」，先描述想詢問的事情。實際收當品項、額度及費用，依個案評估與契約約定。</p></div><a class="cta" href="../consult/?type=other">整理我的需求</a></section></main>
<div style="height:70px"></div>'''
    title = "台北內湖當舖服務指南｜汽機車、黃金與精品評估｜台茂當舖"
    desc = f"台茂當舖服務指南：了解汽車、機車、黃金珠寶、名錶、精品包與3C典當諮詢的準備事項。位於台北市內湖區成功路三段88號，歡迎先以電話{TEL}或官方LINE詢問。"
    ld = [{"@context": "https://schema.org", "@graph": [
        business_node(), website_node(),
        {"@type": "WebPage", "@id": BASE + "services/#webpage", "url": BASE + "services/", "name": title, "description": desc, "inLanguage": "zh-Hant-TW",
         "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BIZ}, "publisher": {"@id": BIZ}, "dateModified": TODAY},
        {"@type": "ItemList", "name": "台茂當舖服務項目", "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "name": n, "url": BASE + "services/#" + i} for k, (i, _, n, *_x) in enumerate(SERVICES)]},
        breadcrumb([("台茂當舖首頁", BASE), ("服務指南", BASE + "services/")])]}]
    return page(title, desc, "services/", "../", body, active="services", jsonld=ld, body_class="sub")

# ═════════════ 關於台茂 ═════════════
def about():
    body = f'''<section class="pagehead"><div class="wrap"><nav class="breadcrumbs" aria-label="麵包屑"><a href="../">台茂首頁</a> / 關於台茂</nav>
<h1>關於台茂當舖</h1>
<p class="lead">台茂當舖是位於台北市內湖區成功路三段的當舖，提供汽車、機車、黃金珠寶、名錶、精品包與 3C 的典當諮詢。</p></div></section>
<main class="wrap layout" id="main"><article class="article prose">
<h2>台茂當舖是什麼樣的店？</h2>
<p>台茂當舖（亦寫作「台茂當鋪」）位於{ADDR}。我們受理汽車、機車（含重機）、黃金珠寶、名錶、精品包與 3C 數位產品的典當諮詢，由羅經理與專人先了解您的需求，再說明評估結果、費用與辦理條件。</p>
<p>我們的做法很簡單：先說清楚，再決定。額度、利息、倉棧費與還款安排，辦理前逐項確認；網頁介紹不代表核准額度或報價。</p>
<h2>店家資料</h2>
{facts_dl()}
<h2>在內湖挑當舖，可以核對這些事</h2>
<ul class="checklist">
<li>營業場所明顯處是否揭示許可證、利率、利息計算方式與營業時間。</li>
<li>店名、地址與聯絡方式，是否與網路上的資料一致。</li>
<li>年利率是否在《當舖業法》上限內（第 11 條：年利率最高 30%），並確認倉棧費（第 20 條：最高為收當金額的 5%）及是否有其他不明費用。</li>
<li>當票與契約上的本金、利率、起算日、屆滿日與取贖方式，是否都看得懂、寫得清楚。</li>
<li>不空白簽名，不交付不必要的帳號密碼，初次聯絡不提供身分證字號。</li>
</ul>
<p>想看完整說明，可以閱讀<a href="../faq/neihu-pawnshop/">內湖當鋪怎麼選？台茂當舖服務與到店準備</a>與<a href="../faq/pawn-interest-fees/">當舖利息怎麼算？</a>。</p>
<h2>羅經理的金融知識中心</h2>
<p>本站整理{ZH_NUM[FAQ_TOTAL]}篇典當與借款常見問題，涵蓋準備文件、汽機車評估、黃金估價、利息費用與取贖。內容為一般資訊，非個別法律或財務意見，也不是核准借款的承諾。</p>
<p><a class="link" href="../faq/">瀏覽 {FAQ_TOTAL} 篇金融知識</a></p>
<div class="hint"><strong>提醒：</strong>借款前請衡量還款能力。實際承作項目與條件，以依法說明及書面契約為準。</div>
</article>
<aside class="sidebar"><div class="sidecard"><h2>想先了解自己的情況？</h2><p>先說明需求，再確認適用的方案與費用。</p><a class="cta" href="{LINE}" target="_blank" rel="noopener noreferrer">加入官方 LINE 諮詢</a><small>{ADDR}<br>電話：{TEL}</small></div>
<div class="related"><h2>接著看</h2><a href="../services/">服務項目與諮詢前準備 →</a><a href="../faq/pawn-document-checklist/">第一次到當舖要帶什麼？ →</a><a href="../consult/">整理諮詢內容 →</a><a href="../updates/">最新消息 →</a></div></aside></main>'''
    title = "關於台茂當舖｜內湖成功路三段88號｜店家資料與選擇指南"
    desc = f"台茂當舖店家資料：{ADDR}，24小時營業，電話{TEL}，官方LINE @104faknx。受理汽車、機車、黃金珠寶、名錶、精品包與3C典當諮詢；附內湖當舖挑選檢核清單。"
    ld = [{"@context": "https://schema.org", "@graph": [
        business_node(), website_node(),
        {"@type": "AboutPage", "@id": BASE + "about/#webpage", "url": BASE + "about/", "name": title, "description": desc, "inLanguage": "zh-Hant-TW",
         "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BIZ}, "mainEntity": {"@id": BIZ}, "dateModified": TODAY},
        breadcrumb([("台茂當舖首頁", BASE), ("關於台茂", BASE + "about/")])]}]
    return page(title, desc, "about/", "../", body, active="about", jsonld=ld, body_class="sub")

# ═════════════ 套用新外觀到既有內頁 ═════════════
def add_assets(h, R, extra_after=""):
    """把舊樣式連結換成新樣式＋字體＋圖示（保留 canonical / og / JSON-LD）。"""
    h = re.sub(r'<link rel="stylesheet" href="[^"]*(?:faq/)?style\.css[^"]*">', "", h)
    h = re.sub(r'<link rel="stylesheet" href="[^"]*assets/updates\.css[^"]*">', "", h)
    tag = f'{FONTS}<link rel="stylesheet" href="{R}assets/tm.css?v=3"><link rel="icon" href="{FAVICON}">'
    if "assets/tm.css" not in h:
        h = h.replace("</head>", tag + "</head>", 1)
    return h

def restyle_faq(path, R, active="faq"):
    h = r(path)
    h = add_assets(h, R)
    h = re.sub(r'(?:<a class="skip-link"[^>]*>[^<]*</a>\s*)?<header class="(?:sitehead|tm-header|inner-header)">.*?</header>', lambda m: header(R, active), h, flags=re.S)
    h = re.sub(r'<footer class="(?:footer|tm-footer|inner-footer)">.*?</footer>(?:\s*<nav class="dock".*?</nav>)?(?:<script src="[^"]*tm\.js[^"]*" defer></script>)?', lambda m: footer(R) + f'<script src="{R}assets/tm.js?v=3" defer></script>', h, flags=re.S)
    h = h.replace('<section class="hero">', '<section class="pagehead">')
    h = re.sub(r'<p class="kicker">TAIMAO KNOWLEDGE / (\d+)</p>', lambda m: f'<p class="kicker">金融知識・第 {int(m.group(1))} 篇</p>', h)
    h = h.replace('<p class="kicker">KNOWLEDGE CENTER / 羅經理專業解答</p>', '<p class="kicker">羅經理專業解答</p>')
    h = h.replace('<p class="kicker">DAILY NOTES / 每日小知識</p>', '<p class="kicker">每日小知識</p>')
    h = re.sub(r'<main class="', '<main id="main" class="', h, count=1)
    if "<footer" not in h:   # 最新消息頁原本沒有頁尾
        h = h.replace("</body>", footer(R) + f'<script src="{R}assets/tm.js?v=3" defer></script></body>', 1)
    # 麵包屑：舊版用「 / 」文字分隔，沿用即可
    h = h.replace("</title>", "</title><meta name=\"robots\" content=\"index,follow,max-image-preview:large,max-snippet:-1\">", 1) if 'name="robots"' not in h else h
    h = h.replace("<body>", "<body class=\"sub\">", 1)
    w(path, h)

def restyle_consult():
    path = "consult/index.html"
    h = r(path)
    R = "../"
    # 諮詢頁有嚴格的 CSP（不連外部網站），所以不載入 Google 字體與 data: 圖示，字體用系統字體
    tag = f'<link rel="stylesheet" href="{R}assets/tm.css?v=3">'
    if "assets/tm.css" not in h:
        h = h.replace("</head>", tag + "</head>", 1)
    h = re.sub(r'(?:<a class="skip-link"[^>]*>[^<]*</a>\s*)?<header class="(?:sitehead|tm-header|inner-header)">.*?</header>', lambda m: header(R, "consult"), h, flags=re.S)
    h = re.sub(r'<footer class="(?:footer|tm-footer|inner-footer)">.*?</footer>(?:\s*<nav class="dock".*?</nav>)?(?:<script src="[^"]*tm\.js[^"]*" defer></script>)?', lambda m: footer(R), h, flags=re.S)
    # 頁首改成與其他頁相同的深色頁首區（表單本體不動）
    m_bc = re.search(r'<nav class="breadcrumbs".*?</nav>', h, re.S)
    m_ph = re.search(r'<section class="page-heading">(.*?)</section>', h, re.S)
    if m_bc and m_ph and 'class="pagehead"' not in h:
        inner = re.sub(r'<p class="page-kicker">[^<]*</p>', '<p class="kicker">先把需求整理好</p>', m_ph.group(1))
        h = h.replace(m_bc.group(0), "", 1).replace(m_ph.group(0), "", 1)
        h = h.replace('<main class="page-shell" id="main">', f'<section class="pagehead"><div class="wrap">{m_bc.group(0)}{inner}</div></section><main class="page-shell" id="main">', 1)
    h = h.replace('（全部選填，點此展開）', '（全部選填 點此展開）')
    h = h.replace('<script src="../assets/common.js" defer></script>', f'<script src="{R}assets/tm.js?v=3" defer></script>')
    if "assets/tm.js" not in h:
        h = h.replace("</body>", f'<script src="{R}assets/tm.js?v=3" defer></script></body>', 1)
    w(path, h)

def restyle_updates():
    restyle_faq("updates/index.html", "../", active="updates")

# ═════════════ sitemap / llms.txt / robots.txt ═════════════
FAQ_PAGES = ["neihu-pawnshop", "car-loan-outstanding", "car-no-retention", "motorcycle-pawn", "pawn-interest-fees",
             "credit-issues", "debt-consolidation", "gold-valuation", "car-loan-limit", "pawn-document-checklist"]

def sitemap():
    pl = posts()
    global FAQ_PAGES
    urls = [("", TODAY, ""), ("services/", TODAY, ""), ("about/", TODAY, ""), ("consult/", TODAY, ""), ("faq/", TODAY, "")]
    urls += [(f"faq/{s}/", TODAY, "") for s in FAQ_PAGES + [a["slug"] for a in ARTICLES]]
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, _ in urls:
        out.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod></url>")
    out.append(f"<url><loc>{BASE}updates/</loc><lastmod>{pl[0]['date'] if pl else TODAY}</lastmod><changefreq>daily</changefreq></url>")
    out.append(f"<url><loc>{BASE}go/</loc><lastmod>{TODAY}</lastmod></url>")
    out.append("</urlset>")
    w("sitemap.xml", "\n".join(out) + "\n")

def faq_index_entries():
    h = r("faq/index.html")
    return re.findall(r'<a class="qcard" href="([^"]+)/"><span class="tag">[^<]*</span><h2>([^<]+)</h2><p>([^<]+)</p>', h)

def llms():
    lines = [
     "# 台茂當舖（Taimao Pawn Shop）", "",
     f"> 台茂當舖是位於台北市內湖區成功路三段88號的當舖，提供汽車、機車、黃金珠寶、名錶、精品包與 3C 的典當諮詢與評估。電話 {TEL}，官方 LINE ID @104faknx，24 小時營業。", "",
     "## 店家資料", "",
     "- 店名：台茂當舖（亦寫作台茂當鋪；英文 Taimao Pawn Shop）",
     f"- 地址：{ADDR}（郵遞區號 114）",
     f"- 電話：{TEL}（+886-2-8792-1111）",
     f"- 官方 LINE：@104faknx（{LINE}）",
     f"- Google 地圖：{MAP_VIEW}",
     f"- Facebook：{FB}",
     "- 受理項目：汽車、機車・重機、黃金珠寶、名錶、精品包、3C 數位產品",
     "- 營業時間：24 小時營業（到店前建議先電話或 LINE 聯繫）",
     "- 諮詢窗口：羅經理", "",
     "## 主要頁面", "",
     f"- [首頁：內湖當舖・台茂當舖]({BASE}): 店家資料、服務項目、辦理流程與常見問題",
     f"- [服務指南]({BASE}services/): 汽車、機車、黃金珠寶、名錶、精品包、3C 的諮詢前準備",
     f"- [關於台茂當舖]({BASE}about/): 店家資料與內湖當舖挑選檢核清單",
     f"- [諮詢表單]({BASE}consult/): 整理需求並產生可貼到 LINE 的摘要（不會自動送出資料）",
     f"- [最新消息]({BASE}updates/): 每日一則典當與借款小知識", "",
     "## 金融知識（羅經理）", ""]
    for slug, t, d in faq_index_entries():
        lines.append(f"- [{t}]({BASE}faq/{slug}/): {d}")
    lines += ["", "## 使用提醒", "",
      "- 本站內容為一般資訊，不代表核准額度、報價或個別法律、財務意見。實際收當品項、額度與費用，依個案評估及契約約定。",
      "- 依《當舖業法》，當舖年利率上限 30%（第 11 條）；除利息與倉棧費外不得收取其他費用，倉棧費上限為收當金額 5%（第 20 條）。以上為法定上限，不代表台茂實際報價。",
      "- 如需引用店家資訊（地址、電話、服務項目），請以本檔與首頁為準。", ""]
    w("llms.txt", "\n".join(lines))

def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]
    s = "# 台茂當舖：歡迎搜尋引擎與 AI 搜尋助理讀取公開頁面\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    s += f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n"
    w("robots.txt", s)

# ═════════════ 新增文章（第 11 篇起） ═════════════
import sys
sys.path.insert(0, os.path.join(ROOT, "_build"))
from articles_data import ARTICLES, LAW_URL

FAQ_TOTAL = 10 + len(ARTICLES)
ZH_NUM = {10: "十", 11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六"}

def plain(htm):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", htm)).strip()

def article_page(a):
    secs = "".join(f"<section><h2>{e(t)}</h2>{''.join(parts)}</section>" for t, parts in a["sections"])
    related = "".join(f'<a href="../{sl}/">{lb} →</a>' for sl, lb in a["related"])
    url = f"faq/{a['slug']}/"
    body = f'''<section class="pagehead"><div class="wrap"><div class="breadcrumbs"><a href="../../">台茂首頁</a> / <a href="../">金融知識中心</a> / {a["crumb"]}</div><p class="kicker">金融知識・第 {a["no"]} 篇</p><h1>{a["h1"]}</h1><p class="lead">{a["lead"]}</p></div></section>
<main id="main" class="wrap layout"><article class="article">{secs}<aside class="hint"><strong>羅經理提醒：</strong>本文為一般資訊，非核准借款承諾或個別法律、財務意見。借款前請衡量還款能力，實際承作項目與條件以依法說明及書面契約為準。</aside><div class="references"><strong>延伸參考：</strong><a href="{LAW_URL}" target="_blank" rel="noopener noreferrer">《當舖業法》（全國法規資料庫）</a><p>本頁資訊校訂日期：{TODAY.replace("-0", "-").replace("-", " 年 ", 1).replace("-", " 月 ")} 日。法令以主管機關最新公布版本為準。</p></div></article>
<aside class="sidebar"><div class="sidecard"><h2>想先了解自己的情況？</h2><p>台茂當舖｜羅經理專業諮詢。先說明需求，再確認適用的合法方案與費用。</p><a class="cta" href="{LINE}" target="_blank" rel="noopener noreferrer">加入官方 LINE 諮詢</a><small>{ADDR}<br>電話：{TEL}<br>營業時間：24 小時</small></div><div class="related service-bridge"><h2>相關台茂服務</h2><a href="../../services/">服務項目與諮詢前準備 →</a><a href="../../about/">關於台茂與店家資料 →</a></div><div class="related"><h2>你可能也想了解</h2>{related}<a href="../">瀏覽全部常見問題 →</a></div></aside></main>'''
    qa = [(t, " ".join(plain(x) for x in parts)) for t, parts in a["sections"] if t.endswith("？")]
    graph = [
        {"@type": "Article", "@id": BASE + url + "#article", "headline": a["title"], "description": a["desc"],
         "mainEntityOfPage": BASE + url, "inLanguage": "zh-Hant-TW", "datePublished": TODAY, "dateModified": TODAY,
         "author": {"@type": "Organization", "name": "台茂當舖", "@id": BIZ}, "publisher": {"@id": BIZ}, "about": {"@id": BIZ},
         "isPartOf": {"@id": BASE + "#website"}, "image": OG},
        breadcrumb([("台茂當舖首頁", BASE), ("金融知識中心", BASE + "faq/"), (a["crumb"], BASE + url)]),
    ]
    if qa:
        graph.append(faq_node(qa))
    ld = [{"@context": "https://schema.org", "@graph": graph}]
    return page(a["title"] + "｜台茂當舖 羅經理", a["desc"], url, "../../", body, active="faq", jsonld=ld, og_type="article", body_class="sub")

def patch_faq_index():
    path = "faq/index.html"
    h = r(path)
    cards = ""
    for a in ARTICLES:
        if f'href="{a["slug"]}/"' in h:
            continue
        cards += (f'<a class="qcard" href="{a["slug"]}/"><span class="tag">{a["tag"]} / {a["no"]:02d}</span>'
                  f'<h2>{a["title"]}</h2><p>{a["short"]}</p><span class="arrow">閱讀羅經理解答 →</span></a>\n')
    if cards:
        h = h.replace('</a></div><section class="widecta">', "</a>\n" + cards + '</div><section class="widecta">', 1)
    h = h.replace("台茂整理十篇常見問答", f"台茂整理{ZH_NUM[FAQ_TOTAL]}篇常見問答")
    # ItemList 補上新文章
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    if m:
        j = json.loads(m.group(1))
        for node in j["@graph"]:
            if node.get("mainEntity", {}).get("@type") == "ItemList":
                items = node["mainEntity"]["itemListElement"]
                have = {i["url"] for i in items}
                for a in ARTICLES:
                    u = BASE + f"faq/{a['slug']}/"
                    if u not in have:
                        items.append({"@type": "ListItem", "position": len(items) + 1, "url": u, "name": a["title"]})
        h = h.replace(m.group(1), json.dumps(j, ensure_ascii=False, separators=(",", ":")), 1)
    w(path, h)

def main():
    w("index.html", home())
    w("services/index.html", services())
    w("about/index.html", about())
    for s in FAQ_PAGES:
        restyle_faq(f"faq/{s}/index.html", "../../")
    for a in ARTICLES:
        w(f"faq/{a['slug']}/index.html", article_page(a))
    patch_faq_index()
    restyle_faq("faq/index.html", "../")
    restyle_consult()
    restyle_updates()
    sitemap(); llms(); robots()
    print("built OK")

if __name__ == "__main__":
    main()
