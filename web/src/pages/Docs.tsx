import { useEffect, useState, type MouseEvent, type ReactNode } from "react";
import { REPO } from "../components/Chrome";
import { Link } from "../router";

function Code({ children, lang = "bash" }: { children: string; lang?: string }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(children.trim());
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard unavailable */
    }
  };
  return (
    <div className="doc-code">
      <div className="doc-code-bar">
        <span>{lang}</span>
        <button onClick={copy}>{copied ? "Copied" : "Copy"}</button>
      </div>
      <pre>{children.trim()}</pre>
    </div>
  );
}

function Note({ kind = "info", title, children }: { kind?: "info" | "warn"; title: string; children: ReactNode }) {
  return (
    <aside className={`doc-note ${kind}`}>
      <b>{title}</b>
      <div>{children}</div>
    </aside>
  );
}

type Section = { id: string; group: string; title: string; body: ReactNode };

const SECTIONS: Section[] = [
  {
    id: "introduction",
    group: "Getting started",
    title: "Introduction",
    body: (
      <>
        <p>
          Rowgate checks a release branch against the <b>signed API contract spreadsheet</b> and writes the contract test that
          fails when a row breaks. Every finding cites one cell, such as <code>Orders!C14</code>, and a human decides what
          happens next: fix the code, or record a breaking change in the workbook.
        </p>
        <p>
          It runs inside IBM Bob as a <b>Contract Gate mode</b> and a <b>Rowgate Skill</b>, started with <code>/rowgate</code>.
          Everything deterministic (the diff, the test runs, the report) is a plain script that costs no tokens.
        </p>
        <ul>
          <li><b>Input:</b> a branch and a contract workbook (<code>.xlsx</code>).</li>
          <li><b>Output:</b> a cited cell, a failing test named after it, a decision, and a dossier that proves each one.</li>
          <li><b>After the run:</b> the tests stay in the repo, so CI checks every later pull request with no model involved.</li>
        </ul>
      </>
    ),
  },
  {
    id: "quickstart",
    group: "Getting started",
    title: "Quickstart",
    body: (
      <>
        <p>Requirements: Python 3.11+, Git, and Node 20+ for the web app.</p>
        <Code>{`
git clone ${REPO}.git && cd Rowgate
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                 # smoke + renderer tests
`}</Code>
        <p>Put the repo in the demo's starting state and check it:</p>
        <Code>{`
scripts/reset_demo.sh --force       # branch feature/fast-checkout at demo/start
`}</Code>
        <p>
          It ends with <code>Ready.</code> when all seven checks pass: the right branch, tooling identical to <code>main</code>,
          only <code>app/</code> changed, no contract tests yet, the workbook untouched, <code>out/</code> empty, and the existing
          tests green.
        </p>
      </>
    ),
  },
  {
    id: "demo",
    group: "Getting started",
    title: "The demo repository",
    body: (
      <>
        <p>
          <code>app/</code> is the <b>Kora Partner API</b>, a small FastAPI service with orders, billing and auth. On{" "}
          <code>main</code> it meets every ACTIVE row of the contract. The branch <code>feature/fast-checkout</code> is a
          plausible pull request (three commits, five files) whose existing tests still pass.
        </p>
        <p>
          The branch <code>demo/start</code> marks the untouched pull request; <code>reset_demo.sh --force</code> returns to it.
          Never commit to <code>demo/start</code>.
        </p>
        <Note title="Fictional material">The Kora partner, its API and its contract are invented for the demo.</Note>
      </>
    ),
  },
  {
    id: "how-it-works",
    group: "Concepts",
    title: "How a run works",
    body: (
      <>
        <ol className="doc-steps">
          <li><b>Collect the diff</b> <span className="pill">script</span> <code>scripts/collect_diff.sh</code> writes <code>out/diff.patch</code> and <code>out/changed_files.txt</code>.</li>
          <li><b>Read the workbook</b> <span className="pill forest">Bob</span> with <code>office_read</code>.</li>
          <li><b>Plan</b> <span className="pill forest">Plan mode</span> which rows the diff can touch. You approve the plan before anything is written.</li>
          <li><b>Check in parallel</b> <span className="pill forest">subagents</span> one per resource, each with its own context.</li>
          <li><b>Write the failing tests</b> <span className="pill forest">Agent mode</span> one per broken cell, then <code>run_contract_tests.sh before</code>.</li>
          <li><b>Decide</b> <span className="pill amber">human</span> fix the code, record a breaking change, or reject the finding.</li>
          <li><b>Measure and publish</b> <span className="pill">script</span> <code>run_contract_tests.sh after</code>, <code>render_dossier.py</code>, <code>export_site.py</code>.</li>
        </ol>
        <Note title="Where the Bob pieces live">
          The Rowgate Skill is <code>.bob/skills/rowgate/SKILL.md</code>, with a contract-test template beside it. The Contract
          Gate mode and the <code>/rowgate</code> command are defined in <code>rowgate/bob/</code>. <code>RUNBOOK.md</code> lists
          every step of a run, what to approve, and the expected result.
        </Note>
      </>
    ),
  },
  {
    id: "workbook",
    group: "Concepts",
    title: "The contract workbook",
    body: (
      <>
        <p>
          <code>contract/api-contract.xlsx</code> is generated by <code>scripts/build_contract.py</code>. It is deliberately
          untidy, like a real signed contract. Browse it on the <Link className="text-link" href="/contract">Contract page</Link>.
        </p>
        <div className="scroll">
          <table className="rowt">
            <thead><tr><th>Sheet</th><th>Holds</th></tr></thead>
            <tbody>
              <tr><td>Cover</td><td>Partner, version, signature block, change rule</td></tr>
              <tr><td>Orders</td><td>Create and read orders. Field rows inherit their status code from <code>ORD-011</code></td></tr>
              <tr><td>Billing</td><td>Invoices. One merged HTTP status cell covers rows 3 to 9</td></tr>
              <tr><td>Auth</td><td>Token endpoint and its error codes</td></tr>
              <tr><td>Errors</td><td>The shared error envelope every error must use</td></tr>
              <tr><td>Changelog</td><td>Every change to an ACTIVE row, with decision and approver</td></tr>
            </tbody>
          </table>
        </div>
        <h3>Conventions</h3>
        <ul>
          <li><b>ACTIVE</b> rows are enforced. <b>PLANNED</b> and <b>DEPRECATED</b> rows are informational and must never be flagged.</li>
          <li><code>↳ ORD-011</code> means the value is inherited from that rule.</li>
          <li>A breaking change is recorded by setting the row's Contract status to <code>BREAKING</code> and adding a Changelog row.</li>
        </ul>
      </>
    ),
  },
  {
    id: "findings",
    group: "Concepts",
    title: "Findings format",
    body: (
      <>
        <p>
          Bob's only structured output is <code>out/findings.json</code>, validated against{" "}
          <code>rowgate/findings.schema.json</code>. Bob cites a file and a line; the code excerpt is cut from the diff by the
          renderer, never quoted by the model.
        </p>
        <Code lang="json">{`
{
  "branch": "feature/fast-checkout",
  "base": "main",
  "workbook": "contract/api-contract.xlsx",
  "findings": [{
    "id": "F1",
    "cell": "Orders!C14",
    "rule": "ORD-011",
    "contract_says": "POST /orders returns 201",
    "code_does": "returns 202",
    "evidence": { "file": "app/orders.py", "line": 22 },
    "verdict": "BREAK",
    "reasoning": "One or two sentences.",
    "test": "tests/contract/test_orders_C14_create_returns_201.py",
    "decision": "pending"
  }],
  "skipped": [
    {
      "cell": "Orders!D11",
      "why": "...",
      "evidence": { "file": "app/models.py", "line": 15 }
    }
  ]
}
`}</Code>
        <div className="scroll">
          <table className="rowt">
            <thead><tr><th>Field</th><th>Rule</th></tr></thead>
            <tbody>
              <tr><td><code>cell</code></td><td><code>Sheet!A1</code> form; the primary cell the branch violates</td></tr>
              <tr><td><code>related_cells</code></td><td>Optional; referenced rows, such as the shared error envelope</td></tr>
              <tr><td><code>evidence</code></td><td>File and line in the branch version; a quoted hunk must match the diff</td></tr>
              <tr><td><code>test</code></td><td>Must be <code>tests/contract/test_&lt;sheet&gt;_&lt;cell&gt;_&lt;what&gt;.py</code> and exist</td></tr>
              <tr><td><code>decision</code></td><td><code>pending</code>, <code>fix_code</code>, <code>record_breaking</code> or <code>reject</code></td></tr>
              <tr><td><code>workbook_edit</code></td><td>Claimed cell edits; checked against the file itself</td></tr>
              <tr><td><code>skipped</code></td><td>Lookalikes checked and found to hold, each with a reason</td></tr>
            </tbody>
          </table>
        </div>
      </>
    ),
  },
  {
    id: "tests",
    group: "Concepts",
    title: "Contract tests and CI",
    body: (
      <>
        <p>
          Each broken cell gets one test in <code>tests/contract/</code>, named after the cell. The name is the citation: if it
          points at the wrong cell, the dossier flags it.
        </p>
        <Code>{`
scripts/run_contract_tests.sh before   # on the untouched branch: expected red
scripts/run_contract_tests.sh after    # after the approved changes
`}</Code>
        <p>
          Results are saved as pytest JSON reports in <code>out/</code>; red and green in the dossier come from those files, not
          from the model. <code>.github/workflows/tests.yml</code> runs the whole suite on every push and pull request, so once the
          tests exist a PR that breaks a signed row fails CI.
        </p>
      </>
    ),
  },
  {
    id: "evidence",
    group: "Concepts",
    title: "Evidence and the dossier",
    body: (
      <>
        <p>Nothing in the dossier is taken on Bob's word:</p>
        <div className="scroll">
          <table className="rowt">
            <thead><tr><th>Evidence</th><th>Source</th></tr></thead>
            <tbody>
              <tr><td>Code excerpt</td><td>Cut from <code>out/diff.patch</code> by file and line; the cited line is marked</td></tr>
              <tr><td>Red → green</td><td>pytest JSON reports from <code>run_contract_tests.sh</code></td></tr>
              <tr><td>Workbook edits</td><td>Every cell that differs from <code>main:contract/api-contract.xlsx</code> in git</td></tr>
              <tr><td>Cited rows</td><td>Read from the workbook, with the cell highlighted</td></tr>
            </tbody>
          </table>
        </div>
        <p>
          Any mismatch (a missing test, a hunk that is not in the diff, a claimed edit that is not in the file) is listed in a red
          box at the top of the dossier and makes <code>render_dossier.py</code> exit with status 1.
        </p>
      </>
    ),
  },
  {
    id: "scripts",
    group: "Reference",
    title: "Scripts",
    body: (
      <>
        <p>All scripts run from the repository root and use no model.</p>
        <div className="scroll">
          <table className="rowt">
            <thead><tr><th>Script</th><th>What it does</th></tr></thead>
            <tbody>
              <tr><td><code>scripts/collect_diff.sh [branch] [base]</code></td><td>Writes <code>out/diff.patch</code> and <code>out/changed_files.txt</code></td></tr>
              <tr><td><code>scripts/run_contract_tests.sh [before|after]</code></td><td>Runs <code>tests/contract</code>, saves <code>out/test_results.&lt;label&gt;.json</code></td></tr>
              <tr><td><code>python scripts/render_dossier.py</code></td><td>Renders <code>out/dossier.html</code> from <code>out/findings.json</code>; exits 1 on problems</td></tr>
              <tr><td><code>python scripts/export_site.py</code></td><td>Writes <code>web/public/data/*.json</code> and copies the dossier for the web app</td></tr>
              <tr><td><code>scripts/reset_demo.sh [--force]</code></td><td>Restores and checks the demo's starting state</td></tr>
              <tr><td><code>python scripts/build_contract.py</code></td><td>Regenerates the workbook and asserts the cells the demo depends on</td></tr>
            </tbody>
          </table>
        </div>
        <p>
          <code>run_contract_tests.sh</code> and <code>reset_demo.sh</code> call <code>$PYTHON</code> (default{" "}
          <code>python</code>), for example <code>PYTHON=.venv/bin/python scripts/run_contract_tests.sh before</code>.
        </p>
      </>
    ),
  },
  {
    id: "publish",
    group: "Reference",
    title: "Publishing a run",
    body: (
      <>
        <p>After a run, publish its measured results to this site:</p>
        <Code>{`
python scripts/render_dossier.py
python scripts/export_site.py
git add web/public/data web/public/dossier.html
git commit -m "Publish Rowgate run"
git push
`}</Code>
        <p>
          The <Link className="text-link" href="/run">Run page</Link> fills in from <code>run.json</code>, and the single-file
          dossier is linked from it.
        </p>
      </>
    ),
  },
  {
    id: "deploy",
    group: "Reference",
    title: "Deploying the web app",
    body: (
      <>
        <p>
          <code>web/</code> is a static Vite + React site. It reads JSON from <code>web/public/data/</code>, so hosting needs no
          Python and no server.
        </p>
        <ol>
          <li>On Vercel, <b>Add New → Project</b> and import the repository.</li>
          <li>Set <b>Root Directory</b> to <code>web</code>. The preset becomes <b>Vite</b>.</li>
          <li>Deploy. Every push to <code>main</code> redeploys.</li>
        </ol>
        <Code>{`
cd web && npm install && npm run dev   # http://localhost:5173
`}</Code>
      </>
    ),
  },
  {
    id: "faq",
    group: "Reference",
    title: "FAQ",
    body: (
      <>
        <h3>Why not OpenAPI, Pact or Schemathesis?</h3>
        <p>
          Those need a machine-readable spec. Partner integrations in banking, telco and insurance are often signed as
          spreadsheets that never become OpenAPI. Rowgate starts from that document.
        </p>
        <h3>Does the site or CI call a model?</h3>
        <p>No. Bob reads the workbook once, during a run. The tests it writes run in plain pytest from then on.</p>
        <h3>What if Bob cites the wrong cell?</h3>
        <p>The test is named after the cell and must fail on the branch. A wrong citation shows up as a test that does not fail, or as a problem in the dossier.</p>
        <h3>Will Rowgate change product code on its own?</h3>
        <p>No. Code changes only for findings where a human chose <code>fix_code</code>.</p>
      </>
    ),
  },
];

const GROUPS = [...new Set(SECTIONS.map((s) => s.group))];

const RESOURCES: [string, string][] = [
  ["README", "README.md"],
  ["Architecture", "ARCHITECTURE.md"],
  ["Findings schema", "rowgate/findings.schema.json"],
  ["Build plan", "PLAN.md"],
  ["Decisions and facts", "MEMORY.md"],
];

export default function Docs() {
  const [active, setActive] = useState(SECTIONS[0].id);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    // the active section is the last one whose top has scrolled past the header
    let frame = 0;
    const update = () => {
      frame = 0;
      const line = window.innerWidth < 760 ? 140 : 110;
      let current = SECTIONS[0].id;
      for (const s of SECTIONS) {
        const el = document.getElementById(s.id);
        if (el && el.getBoundingClientRect().top <= line) current = s.id;
      }
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = SECTIONS[SECTIONS.length - 1].id;
      setActive(current);
    };
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (frame) cancelAnimationFrame(frame);
    };
  }, []);

  const go = (id: string) => (e: MouseEvent) => {
    e.preventDefault();
    setMenuOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
    window.history.replaceState(null, "", `/docs#${id}`);
  };

  const current = SECTIONS.find((s) => s.id === active);
  const nav = (
    <nav aria-label="Documentation">
      {GROUPS.map((g) => (
        <div key={g} className="docs-group">
          <span className="docs-group-title">{g}</span>
          {SECTIONS.filter((s) => s.group === g).map((s) => (
            <a key={s.id} href={`/docs#${s.id}`} onClick={go(s.id)} aria-current={active === s.id ? "true" : undefined}>
              {s.title}
            </a>
          ))}
        </div>
      ))}
    </nav>
  );

  return (
    <main className="wrap docs fade-in">
      <aside className="docs-side">{nav}</aside>

      <div className="docs-mobile">
        <button className="docs-mobile-btn" onClick={() => setMenuOpen((o) => !o)} aria-expanded={menuOpen}>
          <span className="muted">Docs /</span> {current?.title}
          <span className="docs-caret" aria-hidden="true">{menuOpen ? "▴" : "▾"}</span>
        </button>
        {menuOpen && <div className="docs-mobile-menu">{nav}</div>}
      </div>

      <article className="docs-body">
        <header className="docs-head">
          <span className="eyebrow">Documentation</span>
          <h1 className="display">Rowgate docs</h1>
          <p className="lede">Run the demo, read the contract conventions, and see exactly what each script and file does.</p>
        </header>
        {SECTIONS.map((s) => (
          <section key={s.id} id={s.id} className="docs-section">
            <h2>
              <a href={`/docs#${s.id}`} onClick={go(s.id)} className="docs-anchor">{s.title}</a>
            </h2>
            {s.body}
          </section>
        ))}
        <p className="muted docs-edit">
          Found something out of date? <a className="text-link" href={`${REPO}/blob/main/web/src/pages/Docs.tsx`} target="_blank" rel="noreferrer">Edit this page on GitHub</a>.
        </p>
      </article>

      <aside className="docs-toc">
        <span className="docs-group-title">Resources</span>
        {RESOURCES.map(([label, path]) => (
          <a key={path} href={`${REPO}/blob/main/${path}`} target="_blank" rel="noreferrer">
            {label} <span aria-hidden="true">↗</span>
          </a>
        ))}
        <a href="#top" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Back to top ↑</a>
      </aside>
    </main>
  );
}
