"""把 src/app.html 和 vendor/ 裡的 Framework7 合併成單一檔案「柴油冰塊記帳.html」，
並複製一份到 docs/index.html 給 GitHub Pages 用。

用法：python build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "柴油冰塊記帳.html"


def main() -> None:
    page = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
    css = (ROOT / "vendor" / "framework7-bundle.min.css").read_text(encoding="utf-8")
    js = (ROOT / "vendor" / "framework7-bundle.min.js").read_text(encoding="utf-8")

    for name, text, closing in (("CSS", css, "</style"), ("JS", js, "</script")):
        if closing in text.lower():
            raise SystemExit(f"Framework7 {name} 內含 {closing}，不能直接內嵌")

    for marker in ("/*F7_CSS*/", "/*F7_JS*/"):
        if page.count(marker) != 1:
            raise SystemExit(f"範本裡的 {marker} 必須剛好出現一次")

    page = page.replace("/*F7_CSS*/", css).replace("/*F7_JS*/", js)
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"已輸出 {OUT.name}（{OUT.stat().st_size / 1024:.0f} KB）")

    # GitHub Pages 網站（docs/）用同一份
    site = ROOT / "docs" / "index.html"
    site.parent.mkdir(exist_ok=True)
    site.write_text(page, encoding="utf-8", newline="\n")
    print("已輸出 docs/index.html")


if __name__ == "__main__":
    main()
