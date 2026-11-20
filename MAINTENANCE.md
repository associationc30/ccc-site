# 台灣鍾肇政文學推廣協會網站 — 維護文件

> 本文件記錄本專案的技術架構、自訂內容結構與部署流程，供日後維護更新時快速上手。
> 最後整理日期：2026-11-01

---

## 1. 技術架構總覽

| 項目 | 技術 | 版本 |
|---|---|---|
| 靜態網站生成器 | [Hugo Extended](https://gohugo.io/) | 0.162.1 |
| CSS 框架 | Tailwind CSS | v4（`@tailwindcss/cli`） |
| 主題 | Hugoplate（`themes/hugoplate`，本地修改版） | — |
| 內容管理後台 | Decap CMS（原 Netlify CMS），見 `static/admin/` | 靜態檔 |
| 套件管理 | pnpm / npm | Node 22+、Go 1.25 |
| 版控 | Git（GitHub: `associationc30/ccc-site`） | branch: `main` |

### 重要指令

```bash
npm run project-setup   # 首次：把主題內容搬進專案根目錄（只需跑一次）
npm install             # 安裝依賴
npm run dev             # 本地開發伺服器（含 themeGenerator watch）
npm run build           # 產生 public/（Hugo --minify）
npm run format          # Prettier 格式化
```

> `hugo_stats.json` 是 Hugo build 自動產生的統計檔，已列入 `.gitignore`，勿提交。
> ⚠️ **但 Tailwind 是靠它決定要產生哪些 utility class**（`main.css` 的 `@source "hugo_stats.json"`）。
> 檔案不存在時，第一次 build 產生的 CSS 會缺少所有 utility（`flex`、`max-w-*` 等），版面會壞掉。
> 因此 `package.json` 的 `dev`／`build`／`preview` 都先跑一次 `hugo --renderToMemory --quiet` 產生統計檔，再進行正式建置。
> **不要移除這個前置步驟**，否則 CI 首次建置會產出殘缺的 CSS。

---

## 2. 專案目錄結構（自訂部分）

```
ccc-site/
├── hugo.toml                 # 主設定：baseURL、模組掛載、外掛、output formats
├── config/_default/
│   ├── menus.toml            # 主選單（首頁/關於協會/鍾肇政/活動與計畫/.../聯絡我們）
│   ├── params.toml           # 全站參數：logo、favicon、深淺色主題、聯絡表單 action
│   └── module.toml           # Hugo modules（gethugothemes 外掛模組）
├── content/                  # ⭐ 所有頁面內容（Markdown + front matter）
│   ├── about/                # 關於協會
│   ├── chung-chao-cheng/    # 鍾肇政介紹頁
│   ├── blog/                 # 文學專文與報導（cms_type: post）
│   ├── events/               # 活動與計畫（cms_type: event）
│   ├── contact/              # 聯絡頁
│   └── sections/             # 首頁區塊元件（call-to-action、testimonial）
├── data/                     # ⭐ 結構化資料（由 Decap CMS 編輯，網頁直接讀取）
│   ├── about.json            # 協會歷史、歷任理事長、組織架構
│   ├── chronology.json       # 鍾肇政著作出版年表
│   ├── bibliography.json     # 研究書目資料庫
│   ├── letters.json          # 書信文物資料庫
│   ├── manuscripts.json      # 手稿與文物資料庫
│   ├── social.json           # 社群連結
│   └── theme.json            # ⭐ 顏色與字體主題（primary #0B9396 等）
├── layouts/                  # 覆寫主題的版型
│   ├── contact.html          # ⭐ 自訂：聯絡頁（已隱藏會址/開放時間/交通指引）
│   └── _partials/essentials/ # header、footer、head、style、script
├── assets/
│   ├── css/custom.css        # ⭐ 自訂樣式入口（主視覺圖版版面的全部樣式都在這裡，前綴 .kv-）
│   └── images/               # logo、favicon、og-image 等圖檔
│       ├── hero-books-pen.png # ⭐ 首頁主視覺素材：書島白描線稿（透明底 RGBA，2396×729）
│       └── hero-books.png    # 舊主視覺插畫（已停用，保留以便還原）
├── static/admin/             # ⭐ Decap CMS 後台（/admin 路徑）
│   ├── index.html            # 含 Netlify Identity 登入
│   └── config.yml            # CMS 集合定義（見第 4 節）
├── archetypes/               # `hugo new` 用的文章模板（events.md、blog.md 會自動帶 cms_type）
├── netlify.toml              # ⭐ Netlify 建置設定（主站）
├── .github/workflows/main.yml# ⭐ GitHub Actions 部署（備用站）
├── DEPLOY.md                 # 雙站部署說明
└── public/                   # build 輸出（.gitignore）
```

---

## 3. 內容模式（Content Model）

### 3.1 一般頁面（content/*.md）
直接編輯 Markdown，或用 CMS。活动/專文必須帶 `cms_type` 才會出現在 CMS 清單：

- 活動：`cms_type: event`，欄位見 `static/admin/config.yml` 第 5 集合
  （status 控制徽章與首頁收錄、featured 控制精選區、google_form_url 控制報名按鈕）
- 專文：`cms_type: post`
- 新增檔案請用 `hugo new events/<名>.md` / `hugo new blog/<名>.md`（archetype 會自動帶 cms_type）

### 3.2 資料驅動頁面（data/*.json）
`data/` 底下的 JSON 是網站的「資料庫」，由 Decap CMS 編輯，版型直接讀取：

| 檔案 | 用途 | 主要欄位 |
|---|---|---|
| `about.json` | 協會沿革、歷任理事長、組織架構 | past_presidents, org_structure, history[] |
| `chronology.json` | 著作年表 | id, title, category, year, decade, publisher, summary, keywords, image |
| `bibliography.json` | 研究書目 | id, title, category, year, author, publisher, summary |
| `letters.json` | 書信文物 | id, sender, recipient, date, language, summary, location, image |
| `manuscripts.json` | 手稿與文物 | id, title, category, year, medium, summary, location, image |

⚠️ **編輯 data/*.json 時欄位順序要和現有檔案一致**（CMS config 有特別註解說明），避免存檔時鍵值被重排造成 diff 混亂。

---

## 4. Decap CMS 後台（/admin）

- 入口：網站的 `/admin`（`static/admin/index.html`），用 Netlify Identity 登入（backend: github, repo: associationc30/ccc-site, branch: main）
- `config.yml` 定義 7 個集合：書信、手稿、書目、年表、活動、專文、區塊首頁文案
- 圖片上傳路徑：`static/images/uploads/`（media_folder 設定）
- 集合用 `filter: {field: cms_type, value: ...}` 排除 `_index.md`，區塊首頁文案另外收在「🗂️ 區塊首頁文案」
- ⚠️ 手動新增活動/專文 md 檔若漏填 `cms_type`，網站正常但不會出現在 CMS 清單

---

## 5. 自訂修改清單（相對主題原版）

1. **主題色與字體**：`data/theme.json`（primary `#0B9396`、body 背景 `#FCFBF9` 等，字體 Heebo）
2. **選單**：`config/_default/menus.toml`（中文選單，含聯絡我們）
3. **聯絡頁**：`layouts/contact.html`——標題改為「聯絡資訊」，會址/開放時間/交通指引區塊以 `{{/* */}}` 註解隱藏（內容保留，日後可還原）
4. **自訂 CSS**：`assets/css/custom.css`（主視覺的圖版樣式都寫在這裡，class 前綴 `.kv-`；
   檔尾的 `@import "custom.css"` 在主題 `main.css`，會被 Tailwind 內嵌，不需另加 `<link>`）
5. **CMS 後台**：`static/admin/` 整套自建
6. **資料內容**：`content/` 與 `data/` 全部為協會自有內容
7. **baseURL 策略**：`hugo.toml` 放預設值，兩個部署平台各自用 `HUGO_BASEURL` 覆蓋（見下節）
8. **首頁 hero 版型**：`layouts/index.html`——「圖右字左」主視覺：米白紙底，左欄是直排標題（`.kv-title`）
   ＋朱紅落款印（`.kv-seal`）＋提要（英文全名、協會全名、標語、說明段），右側是書島**線稿**（透明底 PNG），
   圖寬 `118%` 向右出血出畫面。文案欄位見 `content/_index.md` 的 `banner:`。
   - 圖下方沒有圖說也沒有細線（`caption`／`credit` 欄位都已移除），首頁只留線稿本身。
   - 桌機給圖 `margin-top: clamp(1rem, 7vw, 6rem)`，讓圖說與左欄提要落在同一水平帶。
   - 窄螢幕（< 1023px）：`.kv-grid` 改 flex、`.kv-col` 設 `display: contents` 解體，
     再用 `order` 排成「標題＋印 → 圖 → 圖說 → 提要」；直排標題轉橫排、圖寬回到 100%。
   - 紙色用站上 token `--color-light`（`#F5F2EC`）；要改回設計稿色只需改 `.kv-hero` 的 `--kv-paper`。
   - 字體：`jf蘭陽明體1.1`（本機才有）→ `Noto Serif TC`（Google Fonts）→ `Noto Serif CJK TC` 逐級退。
     **主題在 `h1` 上直接指定了 `--font-secondary`（Signika 無襯線），繼承贏不過元素選擇器**，
     所以 `.kv-hero h1 / p / span / figcaption` 都必須明寫 `font-family`，只設在父層沒用。
   - 圖片用 Hugo 影像處理（`.Resize … webp q95`）產生 900／1400／2000／2396 四種寬度，
     `banner.image` 寫 `images/xxx.png`（相對 `assets/`、不帶開頭斜線）。線稿細線怕壓縮，webp 品質用 95。
   - 線稿怎麼來的：照片 → 降到 70% → Canny 抓結構線（門檻 36/88）→ 濾掉 <260px 碎線 → 低頻位移做手抖
     → 套島形遮罩只留書上的線 → 再清掉去背後透明區裡的殘線與碎點。腳本與排版提案見
     `ccc-site_待處理素材/主視覺提案/`。
   - 前一版「字在島內」（標題落在島的中央留白、需要量測洞的位置）在 commit `82ecc98`，可整段還原。
