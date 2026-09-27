"""Render the video's non-footage frames at 1920x1080 in the site's palette."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "cards"
OUT.mkdir(parents=True, exist_ok=True)

LOGO = (ROOT / "web" / "public" / "logo.svg").read_text(encoding="utf-8")

BASE = """
<style>
  @page { size: 1920px 1080px; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1920px; height:1080px; background:#0f1611; color:#e8dcb8;
         font-family: Georgia, "DejaVu Serif", serif; display:flex;
         align-items:center; justify-content:center; overflow:hidden; }
  .grid { position:fixed; inset:0;
    background-image:linear-gradient(#263128 1px, transparent 1px),
                     linear-gradient(90deg, #263128 1px, transparent 1px);
    background-size:64px 64px; opacity:.28; }
  .wrap { position:relative; width:1500px; }
  .eyebrow { font-family:"DejaVu Sans",sans-serif; font-size:22px; letter-spacing:.22em;
             text-transform:uppercase; color:#9a9a88; }
  h1 { font-size:96px; line-height:1.04; margin-top:26px; font-weight:400; }
  em { color:#e3b64f; font-style:italic; }
  .mono { font-family:"DejaVu Sans Mono",monospace; }
</style>
<div class="grid"></div>
"""

NUMBERS = BASE + """
<style>
  table { width:100%; border-collapse:collapse; margin-top:56px;
          font-family:"DejaVu Sans",sans-serif; }
  th, td { padding:26px 20px; border-bottom:1px solid #263128; font-size:34px; text-align:left; }
  thead th { font-size:22px; letter-spacing:.14em; text-transform:uppercase; color:#9a9a88;
             border-bottom:2px solid #3a4a3d; }
  td.lbl { color:#9a9a88; width:40%; }
  td.them { color:#c9c4ae; width:30%; }
  td.us { color:#e8dcb8; width:30%; }
  b { font-size:46px; font-weight:400; }
  .win { color:#e3b64f; }
</style>
<div class="wrap">
  <span class="eyebrow">Measured, not claimed</span>
  <h1>Four broken cells.<br><em>Zero</em> false alarms.</h1>
  <table>
    <thead><tr><th></th><th>Reading the diff</th><th>Rowgate</th></tr></thead>
    <tbody>
      <tr><td class="lbl">Broken cells found</td><td class="them"><b>2</b> of 4</td><td class="us"><b class="win">4</b> of 4</td></tr>
      <tr><td class="lbl">Proven by a failing test</td><td class="them">none</td><td class="us"><b class="win">4/4</b> red</td></tr>
      <tr><td class="lbl">False alarms</td><td class="them">&mdash;</td><td class="us"><b class="win">0</b></td></tr>
      <tr style="border:0"><td class="lbl">Effort</td><td class="them">12 min, knowing the answers</td><td class="us">one Bob run &middot; <span class="mono">6.1</span> Bobcoins</td></tr>
    </tbody>
  </table>
</div>
"""

END = BASE + """
<style>
  body { flex-direction:column; gap:0; }
  .logo { width:132px; height:132px; }
  .wrap { text-align:center; width:1400px; }
  h1 { font-size:104px; margin-top:34px; }
  p { font-family:"DejaVu Sans",sans-serif; font-size:32px; color:#9a9a88; margin-top:30px; line-height:1.5; }
  .links { margin-top:52px; display:flex; gap:22px; justify-content:center; flex-wrap:wrap;
           font-family:"DejaVu Sans Mono",monospace; font-size:27px; }
  .links span { border:1px solid #263128; border-radius:999px; padding:15px 30px; color:#e8dcb8; }
  .links span.amber { border-color:#e3b64f; color:#e3b64f; }
</style>
<div class="wrap">
  <div style="display:flex;justify-content:center">__LOGO__</div>
  <h1>Rowgate</h1>
  <p>The signed contract, as a release gate.<br>Built with IBM Bob &mdash; Contract Gate mode and the Rowgate Skill.</p>
  <div class="links">
    <span class="amber">rowgate.vercel.app</span>
    <span>github.com/Ritapossible/Rowgate</span>
    <span>bob_sessions/</span>
  </div>
</div>
""".replace("__LOGO__", LOGO.replace('viewBox="0 0 64 64"', 'viewBox="0 0 64 64" class="logo"'))

CAPTION = """
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:900px; height:170px; background:transparent; display:flex;
         align-items:center; padding-left:10px; }
  .chip { display:inline-flex; align-items:center; gap:18px;
          background:rgba(15,22,17,.94); border:2px solid #e3b64f; border-radius:16px;
          padding:22px 34px; }
  .cell { font-family:"DejaVu Sans Mono",monospace; font-size:44px; color:#e3b64f; }
  .what { font-family:"DejaVu Sans",sans-serif; font-size:30px; color:#e8dcb8; }
</style>
<div class="chip"><span class="cell">__CELL__</span><span class="what">__WHAT__</span></div>
"""

CAPTIONS = [
    ("caption-orders-C14", "Orders!C14", "must return 201 Created"),
    ("caption-billing-E9", "Billing!E9", "invoice must carry currency"),
    ("caption-auth-E5", "Auth!E5", "bad secret must return 401"),
    ("caption-errors-D6", "Errors!D6", "shared error envelope"),
    ("caption-orders-D11", "Orders!D11", "holds — wire name unchanged"),
]


def main() -> int:
    with sync_playwright() as pw:
        chrome = os.environ.get("CHROME_PATH")  # set when Playwright cannot find a browser
        b = pw.chromium.launch(executable_path=chrome) if chrome else pw.chromium.launch()
        for name, html, size in (("numbers-card", NUMBERS, (1920, 1080)),
                                 ("end-card", END, (1920, 1080))):
            pg = b.new_page(viewport={"width": size[0], "height": size[1]})
            pg.set_content(html)
            pg.screenshot(path=str(OUT / f"{name}.png"))
            pg.close()
            print(f"{name}.png  {size[0]}x{size[1]}")
        for name, cell, what in CAPTIONS:
            pg = b.new_page(viewport={"width": 900, "height": 170})
            pg.set_content(CAPTION.replace("__CELL__", cell).replace("__WHAT__", what))
            pg.screenshot(path=str(OUT / f"{name}.png"), omit_background=True)
            pg.close()
            print(f"{name}.png  transparent")
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
