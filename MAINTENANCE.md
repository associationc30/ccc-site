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
│   ├── css/custom.css        # ⭐ 自訂樣式入口（目前僅註解）
│   └── images/               # logo、favicon、og-image、hero-books 等圖檔
│       └── hero-books.png    # ⭐ 首頁主視覺（書島插畫，底色 #FCFBF9）
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
4. **自訂 CSS**：`assets/css/custom.css`（目前只有註解，日後新增樣式寫這裡）
5. **CMS 後台**：`static/admin/` 整套自建
6. **資料內容**：`content/` 與 `data/` 全部為協會自有內容
7. **baseURL 策略**：`hugo.toml` 放預設值，兩個部署平台各自用 `HUGO_BASEURL` 覆蓋（見下節）
8. **首頁 hero 版型**：`layouts/index.html`——改為兩欄式（圖左文右），行動裝置上下堆疊且文字在前。
   圖片主視覺為 `assets/images/hero-books.png`（書島插畫，底色已重繪為 `#FCFBF9` 以與頁面背景無縫接合）。
   ⚠️ 圖片最大寬度是套在外層 `div`（`max-w-[620px]`），**不是**套在 `<img>` 上——主題的 `.img { max-width:100% }`
   屬於未分層 CSS，權重高於 Tailwind utility，直接寫在 `<img>` 的 `max-w-*` 不會生效。

---

## 6. 部署（雙站備援）

| | 主站 Netlify | 備用站 GitHub Pages |
|---|---|---|
| 網址 | `https://ccc-site.netlify.app/` | `https://associationc30.github.io/ccc-site/` |
| 設定檔 | `netlify.toml` | `.github/workflows/main.yml` |
| baseURL | `HUGO_BASEURL` in netlify.toml | `HUGO_BASEURL` in workflow env |
| 觸發 | push main 自動 build | push main 自動跑 workflow |

注意事項：
- 兩站 `baseURL` 刻意不同，改網址時各改各的環境變數
- GitHub Pages 需在 repo Settings → Pages 設為「GitHub Actions」
- 詳細說明見 `DEPLOY.md`
- 其他平台設定檔（amplify/gitlab/vercel）已移除，勿再新增

---

## 7. 日常維護流程速查

1. **改內容**：優先用 `/admin` CMS；改版面/設定才動程式碼
2. **本地預覽**：`npm run dev`，確認無誤
   > 若改用靜態預覽（`hugo -d` 產出一份後再起伺服器），請用 `scripts/preview-server.py` 而不是 `python3 -m http.server`。
   > Hugo 的檔名帶 fingerprint，每次重建都會變；plain http.server 不送快取標頭，瀏覽器會繼續用舊 HTML 去抓已被刪除的 CSS，畫面就變成沒有樣式的裸 HTML。
   > ```bash
   > hugo --baseURL http://127.0.0.1:1319/ -d "$TMPDIR/preview" --quiet
   > python3 scripts/preview-server.py 1319 "$TMPDIR/preview"
   > ```
3. **提交**：`git add -A && git commit && git push origin main`
4. **確認**：等 Netlify build 完成，檢查主站；備用站看 Actions 跑完
5. **改主題色/字體**：改 `data/theme.json`（不動程式碼）
6. **新增活動**：CMS 新增或 `hugo new events/xxx.md`，記得填 status / featured / google_form_url
