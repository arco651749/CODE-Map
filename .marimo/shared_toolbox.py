import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Project Shared Toolbox")


@app.cell
def _():
    import marimo as mo
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📦 專案共用工具箱 (Shared Toolbox)
    > **跨會話活文檔 (Cross-Session Living Documentation)**
    >
    > 本筆記本為專案層級的共用資產庫，跨越所有對話視窗永久留存：
    > - 各會話中驗證成熟、高重用價值的核心 Python 工具與踩坑紀錄 (Gotchas) 可沉澱於此。
    > - 檔案路徑：`.marimo/shared_toolbox.py`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 模組：檔案雜湊與大小快速檢測器 (`inspect_text_digest`)
    * **最後修訂**：2026-10-16
    * **踩坑紀錄 (Gotchas)**：
      1. Windows 環境預設編碼可能為 `cp950`，計算雜湊與 byte 大小時必須明確指定 `.encode("utf-8")` 以確保跨平台一致性。
      2. 行數計算須兼顧 CRLF (`\r\n`) 與 LF (`\n`)，使用 `splitlines()` 處理空字串與多行文本最為穩健。
      3. `hashlib` 於 `@app.function` 內部載入，保持純函式獨立可匯出性。
    * **修改原因**：新增跨會話通用的文字內容 SHA-256 雜湊、UTF-8 位元組大小與行數快速檢測工具。
    """)
    return


@app.function
def inspect_text_digest(text: str) -> dict:
    """輸入任意文字或內容，計算 SHA-256 雜湊、UTF-8 byte 大小與行數。"""
    import hashlib

    raw_bytes = text.encode("utf-8")
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    line_count = len(text.splitlines()) if text else 0
    return {
        "sha256": sha256_hex,
        "utf8_bytes": len(raw_bytes),
        "line_count": line_count,
        "char_count": len(text),
    }


@app.cell
def _(mo):
    digest_text_inp = mo.ui.text_area(
        value="Hello Antigravity Marimo!\n跨會話共用工具箱測試內容。",
        label="輸入要檢測的文字或檔案內容",
        rows=4,
    )
    digest_run_btn = mo.ui.run_button(label="⚡ 計算 SHA-256 與大小")
    return digest_run_btn, digest_text_inp


@app.cell
def _(digest_run_btn, digest_text_inp, mo):
    _res = inspect_text_digest(digest_text_inp.value) if digest_run_btn.value else None
    mo.vstack([
        mo.md("### 🎛️ 檔案雜湊與大小檢測操作台"),
        digest_text_inp,
        digest_run_btn,
        mo.ui.json(_res) if _res else mo.md("_請點擊上方按鈕計算 SHA-256 雜湊、UTF-8 Bytes 與行數_"),
    ])
    return


if __name__ == "__main__":
    app.run()
