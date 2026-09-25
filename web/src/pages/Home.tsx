import type { Contract, PR, Run } from "../data";
import { Link } from "../router";

const STEPS: { n: string; title: string; body: string; who: [string, string][] }[] = [
  { n: "01", title: "Collect the diff", body: "git diff of the branch against main. Captured by a script, not read by a model.", who: [["Script", "pill"], ["No tokens", "pill"]] },
  { n: "02", title: "Read the signed workbook", body: "Bob opens the .xlsx directly: merged headers, inherited rules, the shared error sheet, the rows that are only PLANNED.", who: [["IBM Bob", "pill forest"], ["office_read", "pill mono"]] },
  { n: "03", title: "Plan which rows the diff can touch", body: "Bob maps changed files to contract rows and proposes the checks. Nothing is written until you approve the plan.", who: [["Plan mode", "pill forest"], ["Human gate", "pill amber"]] },
  { n: "04", title: "Check each resource in parallel", body: "One subagent per resource (orders, billing, auth) with its own clean context. Each returns a verdict per row.", who: [["Subagents", "pill forest"], ["Parallel", "pill"]] },
  { n: "05", title: "Write the failing test", body: "One contract test per broken cell, named after the cell. It must fail on the branch, or the finding does not stand.", who: [["Agent mode", "pill forest"]] },
  { n: "06", title: "Decide", body: "Per finding: fix the code, or record a breaking change. Recording writes the Status cell and a Changelog row back into the workbook.", who: [["Human gate", "pill amber"], ["office_edit", "pill mono"]] },
  { n: "07", title: "Measure and publish", body: "pytest runs before and after; the dossier is rendered from the diff, the test reports and the workbook itself.", who: [["Script", "pill"], ["No tokens", "pill"]] },
];

function HeroSheet({ contract }: { contract: Contract | null }) {
  const orders = contract?.sheets.find((s) => s.name === "Orders");
  if (!orders) return null;
  const rows = [11, 12, 13, 14];
  const cols = [0, 1, 2];
  return (
    <figure className="sheet-preview" style={{ margin: 0 }} aria-label="Excerpt of the Orders sheet">
      <div className="sheet-preview-top">
        {contract!.sheets.slice(1, 5).map((s) => (
          <span key={s.name} className={s.name === "Orders" ? "on" : undefined}>{s.name}</span>
        ))}
      </div>
      <table>
        <tbody>
          {rows.map((r) => (
            <tr key={r}>
              <td className="n">{r}</td>
              {cols.map((c) => (
                <td key={c} className={r === 14 && c === 2 ? "hit" : undefined}>
                  {orders.cells[r - 1][c]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <figcaption style={{ padding: "10px 12px", borderTop: "1px solid var(--night-line)", color: "var(--night-muted)", fontFamily: "var(--sans)", fontSize: 13 }}>
        Orders!C14 · signed {contract!.signed} · not in any diff
      </figcaption>
    </figure>
  );
}

export default function Home({ contract, pr, run }: { contract: Contract | null; pr: PR | null; run: Run | null }) {
  const t = contract?.totals;
  const added = pr?.files.reduce((a, f) => a + f.added, 0) ?? 0;
  const removed = pr?.files.reduce((a, f) => a + f.removed, 0) ?? 0;

  return (
    <main className="fade-in">
      <section className="hero">
        <div className="wrap">
          <div className="card-night">
            <div className="grid-lines" />
            <div className="hero-grid">
              <div>
                <span className="eyebrow">Release gate · built with IBM Bob</span>
                <h1 className="display" style={{ marginTop: 18 }}>
                  The contract they signed is <em>not</em> in your diff.
                </h1>
                <p className="lede">
                  Rowgate reads the signed API spreadsheet, cites the cell a release branch breaks, and writes the contract test that
                  proves it. A human decides what ships.
                </p>
                <div className="btn-row">
                  <Link href="/run" className="btn btn-cream">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="4" y="3" width="16" height="18" rx="2" /><path d="M8 8h8M8 12h8M8 16h5" /></svg>
                    See the run
                  </Link>
                  <Link href="/contract" className="btn btn-dark">Browse the contract</Link>
                </div>
              </div>
              <HeroSheet contract={contract} />
            </div>
            <div className="big-stats">
              {run ? (
                <>
                  <div className="big-stat"><b>{run.counts.breaks}</b><span>signed cells broken on {run.doc.branch}</span></div>
                  <div className="big-stat"><b>{run.counts.red_before}<small>/ {run.counts.breaks}</small></b><span>proved by a failing test</span></div>
                  <div className="big-stat"><b>{run.counts.skipped}</b><span>lookalike checked and skipped</span></div>
                </>
              ) : (
                <>
                  <div className="big-stat"><b>{t?.rules ?? "–"}</b><span>signed rules in one .xlsx</span></div>
                  <div className="big-stat"><b>{t?.ACTIVE ?? "–"}</b><span>enforced on every release</span></div>
                  <div className="big-stat"><b>0</b><span>of them visible in the pull request</span></div>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <span className="eyebrow">The gap</span>
          <h2 className="h2" style={{ marginTop: 14 }}>Review reads the diff. The partner signed a spreadsheet.</h2>
          <p className="lede">
            A status code or a required field changes, the tests stay green, and the pull request looks mergeable. The document that
            says otherwise never enters the review.
          </p>
          <div className="gap-grid">
            <div className="panel gap-card">
              <span className="label">What the reviewer sees · {pr?.branch}</span>
              <div className="kpi-row">
                <div className="kpi"><b>{pr?.files.length ?? "–"}</b><span>files changed</span></div>
                <div className="kpi"><b><span className="add">+{added}</span> <span className="del">−{removed}</span></b><span>lines</span></div>
                <div className="kpi"><b>{pr?.commits.length ?? "–"}</b><span>commits</span></div>
              </div>
              <ul className="file-list">
                {pr?.files.map((f) => (
                  <li key={f.path}><span>{f.path}</span><span><span className="add">+{f.added}</span> <span className="del">−{f.removed}</span></span></li>
                ))}
              </ul>
              <p className="muted" style={{ margin: 0 }}>The existing test suite passes on the branch.</p>
            </div>
            <div className="card-cream gap-card" style={{ padding: "clamp(18px, 3vw, 28px)" }}>
              <span className="label" style={{ color: "var(--cream-muted)" }}>What the partner signed · {contract?.workbook}</span>
              <div className="kpi-row">
                <div className="kpi"><b style={{ color: "var(--cream-ink)" }}>{t?.rules ?? "–"}</b><span style={{ color: "var(--cream-muted)" }}>rules</span></div>
                <div className="kpi"><b style={{ color: "var(--cream-ink)" }}>{contract?.sheets.length ?? "–"}</b><span style={{ color: "var(--cream-muted)" }}>sheets</span></div>
                <div className="kpi"><b style={{ color: "var(--cream-ink)" }}>{contract?.version ?? "–"}</b><span style={{ color: "var(--cream-muted)" }}>signed {contract?.signed}</span></div>
              </div>
              <p style={{ margin: 0 }}>
                {contract?.partner?.split(" (")[0] ?? "The partner"} signed off on status codes, required fields and the exact error envelope. Merged headers, rules that inherit from other rules,
                a shared Errors sheet, and {t ? t.PLANNED + t.DEPRECATED : "–"} rows that are planned or deprecated and must not be enforced.
              </p>
              <div>
                <Link href="/contract" className="btn btn-ink">Open the workbook</Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="wrap">
        <div className="card-cream">
          <span className="eyebrow" style={{ color: "var(--cream-muted)" }}>What a run gives you</span>
          <h2 className="h2" style={{ marginTop: 14 }}>
            A cell, a failing test, <em>and</em> a decision.
          </h2>
          <div className="feature-list">
            <div className="feature">
              <span className="feature-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M3 10h18M9 4v16" /></svg></span>
              <div><h3 className="h3">The cell, not an opinion</h3><p>Every finding cites one address, like Orders!C14, and shows the signed row next to the line of code that breaks it.</p></div>
            </div>
            <div className="feature">
              <span className="feature-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3" /></svg></span>
              <div><h3 className="h3">A test that fails</h3><p>The test is named after the cell. Red on the branch, green after the approved fix. If the citation is wrong, the test says so.</p></div>
            </div>
            <div className="feature">
              <span className="feature-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M20 6 9 17l-5-5" /></svg></span>
              <div><h3 className="h3">A human decision</h3><p>Fix the code, or record a breaking change in the workbook itself. Product code is never rewritten without that choice.</p></div>
            </div>
          </div>
          <div className="btn-row">
            <Link href="/run" className="btn btn-ink">See the run</Link>
            <a href="https://github.com/Ritapossible/Rowgate" className="btn btn-ghost" target="_blank" rel="noreferrer">Read the source</a>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <span className="eyebrow">How it runs</span>
          <h2 className="h2" style={{ marginTop: 14 }}>Bob does the judgment. Scripts do the mechanics.</h2>
          <p className="lede">
            Rowgate is a Contract Gate mode and a Rowgate Skill for IBM Bob, started with <code>/rowgate</code>. Anything
            deterministic runs as a script and costs no tokens.
          </p>
          <ol className="steps">
            {STEPS.map((s) => (
              <li className="step" key={s.n}>
                <span className="step-n">{s.n}</span>
                <div className="step-who">{s.who.map(([label, cls]) => <span key={label} className={cls}>{label}</span>)}</div>
                <div className="step-body"><h4>{s.title}</h4><p>{s.body}</p></div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="wrap">
        <span className="eyebrow">Why this, not another review bot</span>
        <div className="compare">
          <div className="panel"><h4>Findings you can falsify</h4><p>Review bots emit paragraphs. Rowgate emits a cell address and a test; a wrong citation fails in front of you.</p></div>
          <div className="panel"><h4>Evidence it can't invent</h4><p>Code excerpts are cut from the diff, pass and fail come from pytest, and workbook edits are measured against git.</p></div>
          <div className="panel"><h4>The contract nobody converted</h4><p>Partner integrations in banking, telco and insurance are signed as spreadsheets and never become OpenAPI. That is the input here.</p></div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="card-night">
            <div className="hero-grid">
              <div>
                <span className="eyebrow">After the run</span>
                <h2 className="h2" style={{ marginTop: 14, color: "var(--night-ink)" }}>The model reads the sheet once. The tests stay.</h2>
                <p className="lede">
                  Every later pull request is checked by the contract tests in CI, with no model in the loop and no tokens spent.
                </p>
              </div>
              <pre className="codeblock" style={{ background: "var(--night-2)", border: "1px solid var(--night-line)" }}>
                <span className="c"># every push and pull request</span>{"\n"}
                python -m pytest tests/contract -q{"\n\n"}
                <span className="c"># tests/contract/</span>
                {run?.findings.length
                  ? run.findings.map((f) => "\n" + f.test.replace("tests/contract/", ""))
                  : "\ntest_<sheet>_<cell>_<what>.py"}
              </pre>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
