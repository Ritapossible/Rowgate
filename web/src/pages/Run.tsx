import type { PR, Run } from "../data";
import { Excerpt, FileDiff, Outcome, RowTable } from "../components/Evidence";
import { Link } from "../router";

function Decision({ f }: { f: Run["findings"][number] }) {
  const pill =
    f.decision === "fix_code" ? <span className="pill green">code fixed</span>
    : f.decision === "record_breaking" ? <span className="pill amber">breaking change recorded</span>
    : f.decision === "reject" ? <span className="pill">finding rejected</span>
    : <span className="pill">waiting for a human</span>;
  return (
    <div className="decision">
      <span className="label" style={{ margin: 0 }}>Decision</span>
      {pill}
      {f.decided_by && <span className="muted">by {f.decided_by}</span>}
      {f.fix_commit && <code>{f.fix_commit}</code>}
      {Object.entries(f.workbook_edit?.cells ?? {}).map(([cell, v]) => (
        <Link key={cell} href={`/contract?cell=${encodeURIComponent(cell)}`} className="pill amber mono" style={{ textDecoration: "none" }}>
          {cell} = {v}
        </Link>
      ))}
      {f.workbook_edit?.changelog_row && (
        <Link href={`/contract?cell=Changelog!A${f.workbook_edit.changelog_row}`} className="pill amber mono" style={{ textDecoration: "none" }}>
          Changelog!A{f.workbook_edit.changelog_row}
        </Link>
      )}
    </div>
  );
}

function PullRequest({ pr, openFirst }: { pr: PR | null; openFirst?: boolean }) {
  if (!pr) return null;
  return (
    <>
      <div className="section-title">
        <h2>The pull request under review</h2>
        <span className="pill mono">{pr.base} ← {pr.branch}</span>
      </div>
      <ul className="commit-list">
        {pr.commits.map((c) => (
          <li key={c.sha}><code>{c.sha}</code><span>{c.subject}</span></li>
        ))}
      </ul>
      {pr.files.map((f, i) => <FileDiff key={f.path} {...f} open={openFirst && i === 0} />)}
    </>
  );
}

export default function RunPage({ run, pr, loading, hasDossier }: { run: Run | null; pr: PR | null; loading: boolean; hasDossier: boolean }) {
  if (loading) return <main className="wrap page-head muted">Loading…</main>;

  if (!run) {
    return (
      <main className="wrap fade-in">
        <div className="page-head">
          <span className="eyebrow">Run</span>
          <h1 className="display" style={{ marginTop: 14 }}>No run published yet.</h1>
          <p className="lede">
            The branch below is waiting for Rowgate. When a run finishes inside IBM Bob, its measured results are exported here:
            the broken cells, the failing tests, and what a human decided.
          </p>
        </div>
        <div className="card-night empty">
          <span className="eyebrow">Publish a run</span>
          <pre className="codeblock" style={{ background: "var(--night-2)", border: "1px solid var(--night-line)" }}>
            <span className="c"># in IBM Bob, Contract Gate mode</span>{"\n"}
            /rowgate {pr?.branch ?? "feature/fast-checkout"}{"\n\n"}
            <span className="c"># then, no model involved</span>{"\n"}
            python scripts/export_site.py
          </pre>
        </div>
        <PullRequest pr={pr} openFirst />
      </main>
    );
  }

  const c = run.counts;
  return (
    <main className="wrap fade-in">
      <div className="page-head">
        <span className="eyebrow">Run · {run.generated}</span>
        <h1 className="display" style={{ marginTop: 14 }}>
          {c.breaks} signed {c.breaks === 1 ? "cell" : "cells"} broken.
        </h1>
        <p className="lede">
          <span className="mono">{run.doc.branch}</span> checked against <b>{run.doc.workbook}</b>
          {run.doc.workbook_version ? ` (${run.doc.workbook_version})` : ""}. Code comes from the diff, pass and fail from pytest,
          workbook edits from comparing the file with git.
        </p>
        <div className="meta-row">
          <span className="pill mono">base {run.doc.base}</span>
          {run.head && <span className="pill mono">head {run.head}</span>}
          {hasDossier && <a className="pill forest" href="/dossier.html" style={{ textDecoration: "none" }}>Single-file dossier ↗</a>}
        </div>
      </div>

      {run.problems.length > 0 && (
        <div className="problems" role="alert">
          <b>This run has {run.problems.length} problem{run.problems.length === 1 ? "" : "s"}:</b>
          <ul>{run.problems.map((p) => <li key={p}>{p}</li>)}</ul>
        </div>
      )}

      <div className="stats">
        <div className="stat dark"><b>{c.breaks}</b><span>contract cells broken</span></div>
        <div className="stat"><b>{c.red_before}/{c.breaks}</b><span>tests red on the branch</span></div>
        <div className="stat"><b>{c.green_after}/{c.fixed ?? c.breaks}</b><span>green after approved fixes</span></div>
        <div className="stat"><b>{c.recorded}</b><span>breaking changes recorded</span></div>
        <div className="stat"><b>{c.skipped}</b><span>lookalikes skipped</span></div>
      </div>

      <div className="section-title"><h2>Broken contract cells</h2></div>
      {run.findings.map((f) => (
        <article className="panel finding" key={f.id} id={f.id}>
          <div className="finding-head">
            <span className="cell-ref">{f.cell}</span>
            {f.rule && <span className="pill forest">{f.rule}</span>}
            {f.related_cells?.map((r) => <span key={r} className="pill mono">{r}</span>)}
            <span className="pill red"><span className="dot" />BREAK</span>
            <span style={{ flex: 1 }} />
            <Link className="text-link" href={`/contract?cell=${encodeURIComponent(f.cell)}`}>Open in contract →</Link>
          </div>
          <div className="says">
            <div className="contract"><span className="label">Contract says</span><p>{f.contract_says}</p></div>
            <div className="code"><span className="label">Branch does</span><p>{f.code_does}</p></div>
          </div>
          <div>
            <span className="label">Signed row · {f.row?.sheet}</span>
            <RowTable row={f.row} />
          </div>
          {f.related.map((r, i) => r && (
            <div key={i}><span className="label">Referenced row · {r.sheet}</span><RowTable row={r} /></div>
          ))}
          <div>
            <span className="label">Diff · {f.evidence.file}{f.evidence.line ? `:${f.evidence.line}` : ""}</span>
            <Excerpt lines={f.diff} />
          </div>
          <p className="reason">{f.reasoning}</p>
          <div className="test-row">
            <span className="label" style={{ margin: 0 }}>Test</span>
            <code>{f.test}</code>
            <Outcome value={f.before} /><span className="arrow">→</span><Outcome value={f.after} />
          </div>
          <Decision f={f} />
        </article>
      ))}

      <div className="section-title"><h2>Checked and skipped</h2></div>
      {run.skipped.length === 0 && <p className="muted">Nothing skipped.</p>}
      {run.skipped.map((s) => (
        <article className="panel finding" key={s.cell} style={{ borderStyle: "dashed" }}>
          <div className="finding-head">
            <span className="cell-ref">{s.cell}</span>
            <span className="pill green"><span className="dot" />holds</span>
            <span style={{ flex: 1 }} />
            <Link className="text-link" href={`/contract?cell=${encodeURIComponent(s.cell)}`}>Open in contract →</Link>
          </div>
          {s.change && <div><span className="label">Looks like</span>{s.change}</div>}
          <RowTable row={s.row} />
          <div><span className="label">Why it is not a break</span>{s.why}</div>
          <Excerpt lines={s.diff} />
        </article>
      ))}

      <div className="section-title">
        <h2>Workbook edits</h2>
        <span className="muted">measured against {run.doc.base}:{run.doc.workbook}</span>
      </div>
      {run.changes === null ? (
        <p className="muted">Could not read the base copy of the workbook from git.</p>
      ) : run.changes.length === 0 ? (
        <p className="muted">No cells changed. The signed workbook is untouched.</p>
      ) : (
        <div className="scroll" style={{ background: "var(--surface)" }}>
          <table className="rowt edits">
            <thead><tr><th>Cell</th><th>Before</th><th>After</th></tr></thead>
            <tbody>
              {run.changes.map((ch) => (
                <tr key={ch.cell}>
                  <td><Link className="text-link mono" href={`/contract?cell=${encodeURIComponent(ch.cell)}`}>{ch.cell}</Link></td>
                  <td className="old">{ch.old}</td>
                  <td className="new">{ch.new}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <PullRequest pr={pr} />
    </main>
  );
}
