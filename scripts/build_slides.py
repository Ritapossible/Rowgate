"""Render submission/SLIDES.md as a 7-slide deck: PNGs, a PDF and a .pptx.

The deck is drawn as HTML in the site's palette and screenshotted at 1920x1080, so the slides
match rowgate.vercel.app rather than looking like a different project. Numbers come from the
run of record; change them in one place here and re-run.

Usage: python scripts/build_slides.py     (CHROME_PATH=... if Playwright cannot find a browser)
"""

import os
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "slides"
LOGO = (ROOT / "web" / "public" / "logo.svg").read_text(encoding="utf-8")

CSS = """
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1920px; height:1080px; background:#0f1611; color:#e8dcb8; overflow:hidden;
         font-family:"DejaVu Sans",sans-serif; display:flex; align-items:center; }
  .grid { position:fixed; inset:0;
    background-image:linear-gradient(#263128 1px,transparent 1px),
                     linear-gradient(90deg,#263128 1px,transparent 1px);
    background-size:64px 64px; opacity:.26; }
  .wrap { position:relative; width:100%; padding:0 120px; }
  .eyebrow { font-size:21px; letter-spacing:.22em; text-transform:uppercase; color:#9a9a88; }
  h1 { font-family:Georgia,"DejaVu Serif",serif; font-weight:400; font-size:82px;
       line-height:1.06; margin-top:24px; }
  h1.big { font-size:104px; }
  em { color:#e3b64f; font-style:italic; }
  .mono { font-family:"DejaVu Sans Mono",monospace; }
  ul { list-style:none; margin-top:46px; }
  li { font-size:31px; line-height:1.5; color:#cfc8b0; margin-bottom:26px; padding-left:34px;
       position:relative; }
  li:before { content:""; position:absolute; left:0; top:15px; width:14px; height:14px;
              border-radius:3px; background:#e3b64f; opacity:.85; }
  b.n { color:#e3b64f; font-weight:400; }
  .cols { display:flex; gap:40px; margin-top:52px; }
  .card { flex:1; background:#151e18; border:1px solid #263128; border-radius:20px; padding:38px 40px; }
  .card.amber { border-color:#e3b64f; }
  .card h3 { font-size:22px; letter-spacing:.16em; text-transform:uppercase; color:#9a9a88;
             font-weight:400; margin-bottom:24px; }
  .card .k { font-family:Georgia,"DejaVu Serif",serif; font-size:64px; color:#e8dcb8; }
  .card .k small { font-size:27px; color:#9a9a88; font-family:"DejaVu Sans",sans-serif; }
  .card p { font-size:26px; color:#cfc8b0; line-height:1.45; margin-top:16px; }
  .foot { position:absolute; left:120px; right:120px; bottom:56px; display:flex;
          justify-content:space-between; font-size:22px; color:#6f7a6f; }
</style>
<div class="grid"></div>
"""

S1 = CSS + """
<style>
  body { justify-content:center; text-align:center; }
  .wrap { width:1500px; }
  .logo { width:150px; height:150px; }
  h1 { font-size:150px; margin-top:30px; }
  .tag { font-family:Georgia,"DejaVu Serif",serif; font-size:48px; color:#e3b64f;
         font-style:italic; margin-top:22px; }
  .one { font-size:30px; color:#cfc8b0; margin-top:40px; }
  .links { margin-top:56px; display:flex; gap:20px; justify-content:center; flex-wrap:wrap;
           font-family:"DejaVu Sans Mono",monospace; font-size:26px; }
  .links span { border:1px solid #263128; border-radius:999px; padding:14px 28px; }
  .links span.a { border-color:#e3b64f; color:#e3b64f; }
  .who { margin-top:46px; font-size:24px; color:#6f7a6f; }
</style>
<div class="wrap">
  <div style="display:flex;justify-content:center">__LOGO__</div>
  <h1>Rowgate</h1>
  <div class="tag">The contract they signed is not in your diff.</div>
  <div class="one">Cites the broken cell &middot; writes the failing test &middot; built with IBM Bob</div>
  <div class="links">
    <span class="a">rowgate.vercel.app</span>
    <span>github.com/Ritapossible/Rowgate</span>
  </div>
  <div class="who">Ritapossible &middot; IBM Bob 2.0 Hackathon 2026</div>
</div>
""".replace("__LOGO__", LOGO.replace('viewBox="0 0 64 64"', 'viewBox="0 0 64 64" class="logo"'))

S2 = CSS + """
<div class="wrap">
  <span class="eyebrow">The gap &middot; business value</span>
  <h1>Review reads the diff.<br>The partner signed a <em>spreadsheet</em>.</h1>
  <div class="cols">
    <div class="card">
      <h3>What the reviewer sees</h3>
      <div class="k">5 <small>files changed</small></div>
      <div class="k" style="font-size:44px;margin-top:10px">
        <span style="color:#7fb98a">+21</span> <span style="color:#c98a7a">&minus;9</span>
        <small>lines &middot; existing tests green</small></div>
      <p>Looks mergeable.</p>
    </div>
    <div class="card amber">
      <h3>What the partner signed</h3>
      <div class="k">41 <small>rules across 6 sheets</small></div>
      <div class="k" style="font-size:44px;margin-top:10px">0 <small>of them in the diff</small></div>
      <p>Status codes, required fields, error bodies &mdash; never in code review.</p>
    </div>
  </div>
  <ul style="margin-top:44px">
    <li>Partner integrations in banking, telco and insurance are signed as spreadsheets and never become OpenAPI.</li>
    <li>The cost lands after release: failed checkouts, rejected invoices, support tickets.</li>
  </ul>
</div>
"""

S3 = CSS + """
<style>
  .finding { margin-top:44px; background:#151e18; border:1px solid #263128; border-radius:20px;
             padding:34px 40px; }
  .fh { display:flex; align-items:center; gap:18px; flex-wrap:wrap; }
  .cell { font-family:"DejaVu Sans Mono",monospace; font-size:40px; color:#e3b64f; }
  .pill { border:1px solid #3a4a3d; border-radius:999px; padding:9px 20px; font-size:22px; color:#cfc8b0; }
  .pill.red { border-color:#c9705f; color:#e0917f; }
  .says { display:flex; gap:40px; margin-top:28px; }
  .says div { flex:1; }
  .lbl { font-size:19px; letter-spacing:.16em; text-transform:uppercase; color:#9a9a88; }
  .says p { font-size:27px; color:#e8dcb8; margin-top:10px; line-height:1.4; }
  .test { margin-top:26px; display:flex; align-items:center; gap:16px; flex-wrap:wrap;
          font-family:"DejaVu Sans Mono",monospace; font-size:23px; color:#cfc8b0; }
  .red { color:#e0917f; } .green { color:#8fc79a; }
</style>
<div class="wrap">
  <span class="eyebrow">What it returns &middot; originality</span>
  <h1>A cell. A failing test. A <em>decision</em>.</h1>
  <div class="finding">
    <div class="fh"><span class="cell">Orders!C14</span>
      <span class="pill">ORD-011</span><span class="pill red">BREAK</span></div>
    <div class="says">
      <div><span class="lbl">Contract says</span><p>POST /orders returns 201 Created</p></div>
      <div><span class="lbl">Branch does</span><p>returns 202 Accepted</p></div>
    </div>
    <div class="test"><span class="lbl" style="letter-spacing:.16em">Test</span>
      test_orders_C14_create_returns_201.py
      <span class="red">&#10007; failed</span> &rarr; <span class="green">&#10003; passed</span></div>
  </div>
  <ul style="margin-top:38px">
    <li>Every finding cites one cell &mdash; not a paragraph of opinion.</li>
    <li>The test is named after the cell and <b class="n">must fail on the branch</b>. A wrong citation shows up as a test that doesn't fail.</li>
    <li>The human chooses: fix the code, or record a breaking change <b class="n">in the workbook itself</b>.</li>
  </ul>
</div>
"""

S4 = CSS + """
<style>
  .flow { display:flex; flex-wrap:nowrap; gap:14px; align-items:center; margin-top:44px; }
  .step { border-radius:14px; padding:20px 26px; font-size:24px; line-height:1.2; white-space:nowrap; }
  .bob { background:#e8dcb8; color:#12211a; font-weight:bold; }
  .scr { background:#1b231d; border:1px solid #2f3d33; color:#9a9a88;
         font-family:"DejaVu Sans Mono",monospace; font-size:22px; }
  .gate { background:#e3b64f; color:#2b2008; font-weight:bold; }
  .arr { color:#4c5a4f; font-size:30px; }
  .key { display:flex; gap:34px; margin-top:44px; font-size:23px; color:#9a9a88; }
  .sw { display:inline-block; width:20px; height:20px; border-radius:5px; vertical-align:-3px; margin-right:10px; }
</style>
<div class="wrap">
  <span class="eyebrow">Inside IBM Bob &middot; application of technology</span>
  <h1>Bob does the judgment.<br>Scripts do the <em>mechanics</em>.</h1>
  <div class="flow">
    <span class="step scr">collect_diff.sh</span><span class="arr">&rarr;</span>
    <span class="step bob">office_read the workbook</span><span class="arr">&rarr;</span>
    <span class="step gate">Plan mode &middot; you approve</span>
  </div>
  <div class="flow" style="margin-top:16px">
    <span class="arr" style="font-size:26px">&#8627;</span>
    <span class="step bob">3 parallel subagents: orders, billing, auth</span><span class="arr">&rarr;</span>
    <span class="step bob">Agent mode writes a test per cell</span><span class="arr">&rarr;</span>
    <span class="step scr">run_contract_tests.sh</span>
  </div>
  <div class="flow" style="margin-top:16px">
    <span class="arr" style="font-size:26px">&#8627;</span>
    <span class="step gate">human decision</span><span class="arr">&rarr;</span>
    <span class="step bob">office_edit the workbook</span><span class="arr">&rarr;</span>
    <span class="step scr">render_dossier.py</span>
  </div>
  <div class="key">
    <span><i class="sw" style="background:#e8dcb8"></i>IBM Bob</span>
    <span><i class="sw" style="background:#e3b64f"></i>human gate</span>
    <span><i class="sw" style="background:#1b231d;border:1px solid #2f3d33"></i>script, no tokens</span>
  </div>
  <ul style="margin-top:34px">
    <li>Contract Gate <b class="n">custom mode</b> + Rowgate <b class="n">Skill</b> + <span class="mono">/rowgate</span> &mdash; not a workflow.</li>
    <li>Document understanding: merged cells, inherited rules, a shared Errors sheet, PLANNED rows it must ignore.</li>
  </ul>
</div>
"""

S5 = CSS + """
<style>
  table { width:100%; border-collapse:collapse; margin-top:50px; }
  th,td { padding:24px 18px; border-bottom:1px solid #263128; font-size:32px; text-align:left; }
  thead th { font-size:21px; letter-spacing:.14em; text-transform:uppercase; color:#9a9a88;
             border-bottom:2px solid #3a4a3d; font-weight:normal; }
  td.lbl2 { color:#9a9a88; width:40%; } td.them { color:#c9c4ae; width:30%; }
  td.us { color:#e8dcb8; width:30%; } b { font-size:44px; font-weight:400; } .win { color:#e3b64f; }
  .note { margin-top:34px; font-size:25px; color:#9a9a88; line-height:1.5; }
</style>
<div class="wrap">
  <span class="eyebrow">Proof &middot; measured, not claimed</span>
  <h1 class="big">Four broken cells.<br><em>Zero</em> false alarms.</h1>
  <table>
    <thead><tr><th></th><th>Reading the diff</th><th>Rowgate</th></tr></thead>
    <tbody>
      <tr><td class="lbl2">Broken cells found</td><td class="them"><b>2</b> of 4</td><td class="us"><b class="win">4</b> of 4</td></tr>
      <tr><td class="lbl2">Proven by a failing test</td><td class="them">none</td><td class="us"><b class="win">4/4</b> red</td></tr>
      <tr><td class="lbl2">False alarms</td><td class="them">&mdash;</td><td class="us"><b class="win">0</b> &middot; 2 lookalikes skipped</td></tr>
      <tr><td class="lbl2">Effort</td><td class="them">12 min, knowing the answers</td><td class="us">one Bob run &middot; <span class="mono">6.1</span> coins</td></tr>
    </tbody>
  </table>
  <p class="note">The 12 minutes are the author's own, already knowing where the breaks were &mdash; and still half were missed.
  Four cells, three edits: the auth change moved both the status code and the error envelope.</p>
</div>
"""

S6 = CSS + """
<style>
  .cols { margin-top:50px; }
  .big2 { font-family:Georgia,"DejaVu Serif",serif; font-size:86px; color:#e3b64f; }
</style>
<div class="wrap">
  <span class="eyebrow">After the run &middot; business value</span>
  <h1>The model reads the sheet once.<br>The <em>tests stay</em>.</h1>
  <div class="cols">
    <div class="card"><h3>Cost of the run</h3><div class="big2">6.1</div>
      <p>Bobcoins, once. The contract tests then run in CI on every later pull request &mdash; plain pytest, no model, no tokens.</p></div>
    <div class="card amber"><h3>The gate, today</h3><div class="big2">1 &#10007;</div>
      <p>The pull request is red on <span class="mono">test_billing_E9</span>, the row a human recorded as a breaking change. A signed cell is holding the release.</p></div>
    <div class="card"><h3>Every number</h3><div class="big2">measured</div>
      <p>Code from the diff, pass and fail from pytest, workbook edits compared against git. Nothing on this slide is asserted by a model.</p></div>
  </div>
</div>
"""

S7 = CSS + """
<style>
  body { justify-content:center; text-align:center; }
  .wrap { width:1500px; }
  .logo { width:120px; height:120px; }
  h1 { font-size:88px; margin-top:26px; }
  .links { margin-top:48px; display:flex; gap:18px; justify-content:center; flex-wrap:wrap;
           font-family:"DejaVu Sans Mono",monospace; font-size:25px; }
  .links span { border:1px solid #263128; border-radius:999px; padding:14px 26px; }
  .links span.a { border-color:#e3b64f; color:#e3b64f; }
  .next { margin-top:46px; font-size:29px; color:#cfc8b0; line-height:1.5; }
</style>
<div class="wrap">
  <div style="display:flex;justify-content:center">__LOGO__</div>
  <h1>The signed contract,<br>as a <em>release gate</em>.</h1>
  <div class="links">
    <span class="a">rowgate.vercel.app</span>
    <span>github.com/Ritapossible/Rowgate &middot; MIT</span>
    <span>bob_sessions/</span>
  </div>
  <p class="next">Next: any spreadsheet contract &mdash; API mappings, data contracts, SLA tables &mdash; becomes tests.</p>
</div>
""".replace("__LOGO__", LOGO.replace('viewBox="0 0 64 64"', 'viewBox="0 0 64 64" class="logo"'))

SLIDES = [S1, S2, S3, S4, S5, S6, S7]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as pw:
        chrome = os.environ.get("CHROME_PATH")
        b = pw.chromium.launch(executable_path=chrome) if chrome else pw.chromium.launch()
        for i, html in enumerate(SLIDES, 1):
            pg = b.new_page(viewport={"width": 1920, "height": 1080})
            pg.set_content(html)
            p = OUT / f"slide-{i}.png"
            pg.screenshot(path=str(p))
            pg.close()
            paths.append(p)
            print(f"slide-{i}.png")
        b.close()

    imgs = [Image.open(p).convert("RGB") for p in paths]
    pdf = ROOT / "submission" / "rowgate-slides.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=96.0)
    print(f"{pdf.name}  {pdf.stat().st_size // 1024} KB")

    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    for p in paths:
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(str(p), 0, 0, width=prs.slide_width, height=prs.slide_height)
    ppt = ROOT / "submission" / "rowgate-slides.pptx"
    prs.save(ppt)
    print(f"{ppt.name}  {ppt.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
