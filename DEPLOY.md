# 部署設定（雙站備援）

本專案採 **Netlify 為主、GitHub Pages 為備用站** 的雙平台部署。

## 主站：Netlify

- 網址：`https://ccc-site.netlify.app/`
- 設定檔：`netlify.toml`
- baseURL 由 `netlify.toml` 的 `HUGO_BASEURL` 控制
- 推送 `main` 時 Netlify 自動 build & deploy

## 備用站：GitHub Pages

- 網址：`https://associationc30.github.io/ccc-site/`
- 設定檔：`.github/workflows/main.yml`
- baseURL 由 workflow 內的 `HUGO_BASEURL` 控制（與 Netlify 分開，互不影響）
- 需確認 repo Settings → Pages → Source 設為 **GitHub Actions**

## 注意事項

1. 兩站的 `baseURL`刻意不同，請勿把 `hugo.toml` 的 `baseURL` 拿來當某一站的唯一來源——兩個平台都用環境變數 `HUGO_BASEURL` 覆蓋。
2. `hugo.toml` 內的 `baseURL` 只是本地開發用的預設值。
3. 若未來只保留單站，刪除對應平台的設定檔即可，另一站不受影響。
