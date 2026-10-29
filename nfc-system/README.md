# 台茂 NFC 電子名片 v1

第一個實例為台茂當舖・羅經理。純靜態、零 npm 外部依賴，可部署 GitHub Pages 子目錄或一般靜態主機。

- 名片：https://gucci3364-spec.github.io/neihupawnshop/nfc/c/taimao/luo/
- 設定工具：https://gucci3364-spec.github.io/neihupawnshop/nfc/studio.html
- 完整操作與 NFC 寫卡教學：https://gucci3364-spec.github.io/neihupawnshop/nfc/guide.html
- 原始碼：本目錄的 build.mjs、lib/、src/、tenants/、tests/、package.json。

## 本機開發與建置

需求 Node.js 20 以上；不需要 npm install。

```sh
npm test
npm run build
python3 -m http.server 8080 --directory dist
```

瀏覽 http://localhost:8080/（請使用 HTTP 伺服器，不要直接雙擊 file:// HTML，否則模組與 JSON 可能被阻擋）。

正式修改：在設定工具匯出 taimao.json，放入 tenants/taimao.json，再執行 npm test 與 npm run build。dist 是可部署產物；不要僅改 dist，否則下次建置會覆蓋。

設定工具只儲存目前瀏覽器的草稿，下載 JSON 不等於已發布。未設電話、LINE、社群、Email、地址與官方 Logo 為刻意保留，不會補入猜測資料。已知官網由使用者提供；服務項目來自本次工作已提供的台茂背景。

## 資料與路徑

每家公司一個 tenants/<companyId>.json。各名片由 cards[] 分別設定，發布後為 c/<companyId>/<cardId>/。設定 schema 為版本 1，請以現有 taimao.json 或設定工具輸出為範本。companyId / cardId 僅接受小寫英數與連字號，同公司不得有重複 cardId。

建置產生每張名片獨立 profile.json、index.html、contact.vcf；卡片不載入全公司總表。不存在的網址沒有 fallback 到另一家公司。data/<companyId>/company.json 是設定工具載入的公開公司設定；其中所有資訊均為公開。build-info.json 不含公司名單或密鑰。

公司隔離是公開檔案與 URL 的分隔，不是伺服器授權隔離。此版本沒有登入、帳號、資料庫、寫入 API 或自動發布。所有部署由有 GitHub / 主機權限的管理者執行。若讓公司登入編輯，需增設後端驗證身份與 tenant_id、資料庫存取權限、操作紀錄及備份，不能只使用前端公司參數。

Logo 可使用 HTTPS 圖片網址或不超過 1 MB 的 PNG/JPEG/WebP（設定工具將圖片內嵌到 JSON）。不得放密鑰、未公開個資或借款客戶資料。電話空白時 vCard 不產生 TEL；不會把網址當作電話。

## 部署至現有 GitHub Pages

本次目標 repository 為 gucci3364-spec/neihupawnshop。公開產物在 nfc/，原始碼在 nfc-system/，根目錄官網保持原狀。

```sh
cd nfc-system
npm test
npm run build
# 核對輸出後，將 dist 的內容同步到同 repository 的 ../nfc/
# 僅同步 nfc 子目錄；不要覆蓋官網根目錄。
```

建議檢查 git diff，只提交 nfc-system 與 nfc。沿用 main 的既有 Pages 發布流程。更新後以 GitHub Actions 顯示 pages build and deployment 成功與實際網址回應為驗證。

對不同主機或 repository 建置：

```sh
CARD_BASE_URL=https://your-domain.example/cards/ npm run build
```

Windows PowerShell：

```powershell
$env:CARD_BASE_URL = 'https://your-domain.example/cards/'
npm run build
```

CARD_BASE_URL 以 / 結尾。其內容用於 canonical、分享網址與 vCard 備註；頁面素材使用相對路徑，所以 GitHub Pages 的 /repo/nfc/ 子目錄可以正常載入。改網域後需重新建置。404.html 在某些主機的子目錄不會自動用作錯誤頁，仍會顯示主機 404，且不會顯示其他公司的名片。

GitHub Pages 技術上適合此靜態測試版；官方限制免費託管商業 SaaS、主要促成商業交易與敏感交易等用途。若擴充為提供其他公司付費登入的平台，請改用適合商業應用的主機及後端，不把這個靜態試作視為完整 SaaS。

## NFC 卡寫入

在已確認公開網址能無登入開啟後，用 NFC Tools（wakdev）依序 Write → Add a record → URL/URI → 貼上完整 HTTPS 名片網址 → Validate → Write → 卡片靠近手機感應區。只寫入一個網址紀錄，勿寫 JSON 或 studio.html。測試階段不要永久鎖卡。

接收者不需專用 App。iPhone XS 及後續機型通常在螢幕亮起時讀取，點網站通知後開啟；不是保證碰觸後無操作自動跳頁。Android 需支援並開啟 NFC，感應位置與開啟方式依機型。開啟網頁需要網路。

此交付不代表實體卡已寫入或完成實機 NFC 測試。詳細步驟、問題排查與官方來源見 src/guide.html。

## 安全與驗證

- HTTPS 連結驗證、拒絕 javascript/data HTML URL；文字以 textContent 或 HTML escaping 顯示。
- .vcf 使用 CRLF，轉義分隔符與換行，依 UTF-8 75 bytes 摺行。
- 生成前驗證全部公司，避免不合法資料破壞上一個 dist。
- 設定檔匯入／Logo 大小限制；本機草稿鍵以公司與名片分開。
- 所有連結資料均為公開，不收集訪客表單，不讀取通訊錄。
- 測試涵蓋多公司輸出隔離、子目錄資源、路徑穿越、重複識別碼、URL 注入與聯絡人格式。
- 無外部 CDN、字型服務或第三方追蹤；設定外部 Logo 時瀏覽器仍會向該網址抓圖。
- 頁面標記 noindex 供第一版測試；noindex 不是防止外部存取的安全機制。

參考網站此次無法公開讀取，介面為原創設計，沒有宣稱還原其未查證功能。
