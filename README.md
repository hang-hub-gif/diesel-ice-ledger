# 柴油冰塊記帳

每天記錄柴油（買、用、剩下）、衛生冰與普通冰（做、賣、剩下）、賣了多少錢、實收現金、應收帳款與總共剩多少錢，並自動找出帳本異常。
繁體中文，iPhone / Android / Windows 都能用，資料只存在各自裝置的瀏覽器（localStorage），不會上傳。

- 線上使用：開 GitHub Pages 網址，手機用「加入主畫面」就像 App 一樣，沒網路也能開。
- 離線單檔：`柴油冰塊記帳.html`，直接用瀏覽器開。
- 記得定期在「設定」頁下載備份檔。

## 修改

1. 改 `src/app.html`
2. 執行 `python build.py`，會產生 `柴油冰塊記帳.html` 和 `docs/index.html`
3. 改了 `docs/` 裡的檔案後，把 `docs/sw.js` 的 `CACHE` 版本號加一，手機才會換成新版

圖示用 `python make_icons.py` 產生。

## 授權

介面使用 [Framework7](https://github.com/framework7io/framework7) 9.3.0（MIT 授權，見 `vendor/LICENSE`）。
