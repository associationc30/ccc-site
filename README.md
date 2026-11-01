# 台灣鍾肇政文學推廣協會 官方網站

以 Hugo + Tailwind CSS v4 建置的靜態網站（基於 Hugoplate 主題客製）。

## 快速開始

```bash
npm run project-setup   # 首次設定（只需一次）
npm install
npm run dev             # 本地開發
npm run build           # 建置到 public/
```

## 部署

採雙站備援：**Netlify 為主站、GitHub Pages 為備用站**，細節見 `DEPLOY.md`。
內容編輯走 `/admin`（Decap CMS，僅主站可用）。

## 文件

- `MAINTENANCE.md` — 技術架構與維護者須知
- `EDITOR-GUIDE.md` — 內容編輯者操作手冊
- `DEPLOY.md` — 雙站部署說明

## 授權

網頁內容採 [創用 CC 姓名標示-非商業性-相同方式分享 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh_TW) 釋出；程式碼為 MIT License（繼承自 Hugoplate）。
