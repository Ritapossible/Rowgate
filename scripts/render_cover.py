"""Render the 1200x630 cover card for the lablab submission and social previews.

Usage: python scripts/render_cover.py   (CHROME_PATH=... if Playwright cannot find a browser)
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
LOGO = (ROOT / "web" / "public" / "logo.svg").read_text(encoding="utf-8")

HTML = """
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1200px; height:630px; background:#0f1611; color:#e8dcb8; overflow:hidden;
         font-family:"DejaVu Sans",sans-serif; position:relative; }
  .grid { position:absolute; inset:0;
    background-image:linear-gradient(#263128 1px,transparent 1px),
                     linear-gradient(90deg,#263128 1px,transparent 1px);
    background-size:60px 60px; opacity:.3; }
  .glow { position:absolute; right:-160px; top:-160px; width:620px; height:620px; border-radius:50%;
          background:radial-gradient(circle, rgba(227,182,79,.16), transparent 68%); }
  .pad { position:relative; padding:56px 64px; height:100%; display:flex; flex-direction:column; }
  .top { display:flex; align-items:center; gap:18px; }
  .logo { width:56px; height:56px; }
  .name { font-family:Georgia,"DejaVu Serif",serif; font-size:44px; }
  .badge { margin-left:auto; border:1px solid #2f3d33; border-radius:999px; padding:10px 22px;
           font-size:17px; color:#9a9a88; letter-spacing:.08em; }
  h1 { font-family:Georgia,"DejaVu Serif",serif; font-weight:400; font-size:66px; line-height:1.07;
       margin-top:40px; }
  em { color:#e3b64f; font-style:italic; }
  .sub { font-size:23px; color:#9a9a88; margin-top:20px; }
  .stats { margin-top:auto; display:flex; gap:14px; }
  .s { flex:1; background:#151e18; border:1px solid #263128; border-radius:16px; padding:20px 24px; }
  .s.hit { border-color:#e3b64f; }
  .s b { display:block; font-family:Georgia,"DejaVu Serif",serif; font-size:40px; font-weight:400; }
  .s.hit b { color:#e3b64f; }
  .s span { font-size:16px; color:#9a9a88; line-height:1.3; display:block; margin-top:6px; }
  .cell { position:absolute; right:64px; top:196px; font-family:"DejaVu Sans Mono",monospace;
          font-size:21px; color:#e3b64f; border:1px solid #e3b64f; border-radius:12px;
          padding:12px 20px; background:rgba(15,22,17,.9); }
</style>
<div class="grid"></div><div class="glow"></div>
<div class="pad">
  <div class="top">__LOGO__<span class="name">Rowgate</span>
    <span class="badge">BUILT WITH IBM BOB</span></div>
  <h1>The contract they signed<br>is <em>not</em> in your diff.</h1>
  <p class="sub">Reads the signed API spreadsheet &middot; cites the broken cell &middot; writes the test that proves it</p>
  <div class="cell">Orders!C14</div>
  <div class="stats">
    <div class="s hit"><b>4 / 4</b><span>signed cells broken, all found</span></div>
    <div class="s"><b>4 / 4</b><span>proved by a failing test</span></div>
    <div class="s"><b>0</b><span>false alarms &middot; 2 lookalikes skipped</span></div>
    <div class="s"><b>6.1</b><span>Bobcoins, then free in CI</span></div>
  </div>
</div>
""".replace("__LOGO__", LOGO.replace('viewBox="0 0 64 64"', 'viewBox="0 0 64 64" class="logo"'))

with sync_playwright() as pw:
    chrome = os.environ.get("CHROME_PATH")
    b = pw.chromium.launch(executable_path=chrome) if chrome else pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(HTML)
    out = ROOT / "submission" / "cover.png"
    pg.screenshot(path=str(out))
    b.close()
    print(out, out.stat().st_size // 1024, "KB")
