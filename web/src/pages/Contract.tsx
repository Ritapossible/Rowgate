import { useEffect, useMemo, useRef, useState } from "react";
import type { Contract, Run, Sheet } from "../data";
import { Link, navigate, useLocation } from "../router";

const REF = /^([A-Za-z]+)!([A-Z]+)(\d+)$/;

function parseRef(ref: string | null) {
  const m = ref ? REF.exec(ref) : null;
  return m ? { sheet: m[1], col: m[2], row: Number(m[3]) } : null;
}

function layout(sheet: Sheet) {
  // top-left cell of a merge → span; every other cell in it → hidden
  const span = new Map<string, { rowSpan: number; colSpan: number }>();
  const hidden = new Set<string>();
  for (const m of sheet.merges) {
    span.set(`${m.r1}:${m.c1}`, { rowSpan: m.r2 - m.r1 + 1, colSpan: m.c2 - m.c1 + 1 });
    for (let r = m.r1; r <= m.r2; r++) for (let c = m.c1; c <= m.c2; c++) if (r !== m.r1 || c !== m.c1) hidden.add(`${r}:${c}`);
  }
  return { span, hidden };
}

function ruleCount(sheet: Sheet) {
  return Object.keys(sheet.rowStatus).length;
}

export default function ContractPage({ contract, run }: { contract: Contract | null; run: Run | null }) {
  const { search } = useLocation();
  const target = parseRef(search.get("cell"));
  const [sheetName, setSheetName] = useState(target?.sheet ?? "Orders");
  const [selected, setSelected] = useState<string | null>(target ? `${target.sheet}!${target.col}${target.row}` : null);
  const [copied, setCopied] = useState(false);
  const flashRef = useRef<HTMLTableCellElement | null>(null);
  const wrapRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!target) return;
    setSheetName(target.sheet);
    setSelected(`${target.sheet}!${target.col}${target.row}`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search.get("cell")]);

  useEffect(() => {
    const cell = flashRef.current;
    const wrap = wrapRef.current;
    if (!cell || !wrap) return;
    // bring the sheet under the nav, then centre the cell inside the sheet's own scroll area
    wrap.scrollIntoView({ block: "start", behavior: "smooth" });
    wrap.scrollTo({
      top: cell.offsetTop - wrap.clientHeight / 2 + cell.offsetHeight / 2,
      left: cell.offsetLeft - wrap.clientWidth / 2 + cell.offsetWidth / 2,
      behavior: "smooth",
    });
  }, [sheetName, contract]);

  const cited = useMemo(() => {
    const map = new Map<string, string>();
    run?.findings.forEach((f) => {
      map.set(f.cell, `${f.id} · BREAK`);
      f.related_cells?.forEach((r) => map.set(r, `${f.id} · referenced`));
    });
    run?.skipped.forEach((s) => map.set(s.cell, "skipped · holds"));
    return map;
  }, [run]);
  const changed = useMemo(() => new Set(run?.changes?.map((c) => c.cell) ?? []), [run]);

  if (!contract) return <main className="wrap page-head muted">Loading the workbook…</main>;
  const sheet = contract.sheets.find((s) => s.name === sheetName) ?? contract.sheets[1];
  const { span, hidden } = layout(sheet);
  const sel = parseRef(selected);
  const selRow = sel && sel.sheet === sheet.name ? sel.row : null;
  const selCol = sel && sel.sheet === sheet.name ? sheet.letters.indexOf(sel.col) : -1;
  const selValue = selRow && selCol >= 0 ? sheet.cells[selRow - 1]?.[selCol] ?? "" : "";
  const selRule = selRow ? sheet.cells[selRow - 1]?.[0] : "";
  const selStatus = selRow ? sheet.rowStatus[String(selRow)] : undefined;
  const selNote = selected ? sheet.notes[selected.split("!")[1]] : undefined;
  const selFinding = selected ? cited.get(selected) : undefined;
  const t = contract.totals;

  const pick = (addr: string) => {
    setSelected(addr);
    setCopied(false);
    window.history.replaceState(null, "", `/contract?cell=${encodeURIComponent(addr)}`);
  };
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(`${window.location.origin}/contract?cell=${encodeURIComponent(selected!)}`);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };

  return (
    <main className="wrap fade-in">
      <div className="page-head">
        <span className="eyebrow">Contract · {contract.workbook}</span>
        <h1 className="display" style={{ marginTop: 14 }}>The signed workbook.</h1>
        <p className="lede">
          {contract.partner}. Version {contract.version}, signed {contract.signed}. Read exactly as Bob reads it: every sheet,
          merged cells, notes and all. Click any cell to get a link to it.
        </p>
        <div className="meta-row">
          <span className="pill">{t.rules} rules</span>
          <span className="pill green"><span className="dot" />{t.ACTIVE} active</span>
          <span className="pill">{t.PLANNED} planned</span>
          <span className="pill">{t.DEPRECATED} deprecated</span>
          {t.BREAKING > 0 && <span className="pill amber">{t.BREAKING} breaking</span>}
        </div>
      </div>

      <div className="contract-bar">
        <div className="tabs" role="tablist" aria-label="Sheets">
          {contract.sheets.map((s) => (
            <button
              key={s.name}
              role="tab"
              className="tab"
              aria-selected={s.name === sheet.name}
              onClick={() => {
                setSheetName(s.name);
                navigate(`/contract`);
                setSelected(null);
              }}
            >
              {s.name}
              {ruleCount(s) > 0 && <span className="count">{ruleCount(s)}</span>}
            </button>
          ))}
        </div>
        <div className="legend">
          {cited.size > 0 && <span className="pill amber">cited by the run</span>}
          {changed.size > 0 && <span className="pill amber mono">edited</span>}
          <span className="pill">▨ planned / deprecated</span>
        </div>
      </div>

      <div className="sheet-wrap" ref={wrapRef} role="region" aria-label={`${sheet.name} sheet`} tabIndex={0}>
        <table className="sheet">
          <thead>
            <tr>
              <th className="rn" />
              {sheet.letters.map((l) => <th key={l}>{l}</th>)}
            </tr>
          </thead>
          <tbody>
            {sheet.cells.map((row, ri) => {
              const r = ri + 1;
              const status = sheet.rowStatus[String(r)];
              const cls = r === 1 ? "title" : sheet.headerRow && r <= sheet.headerRow ? "header" : status === "PLANNED" || status === "DEPRECATED" ? "dim" : "";
              return (
                <tr key={r} className={cls || undefined}>
                  <th className="rn">{r}</th>
                  {row.map((value, ci) => {
                    const key = `${r}:${ci + 1}`;
                    if (hidden.has(key)) return null;
                    const addr = `${sheet.name}!${sheet.letters[ci]}${r}`;
                    const classes = [
                      sheet.statusCol === ci + 1 && status ? `status-${value}` : "",
                      cited.has(addr) ? "cited" : "",
                      changed.has(addr) ? "changed" : "",
                      selected === addr ? "selected" : "",
                      sheet.notes[`${sheet.letters[ci]}${r}`] ? "note" : "",
                      target && addr === `${target.sheet}!${target.col}${target.row}` ? "flash" : "",
                      value.length <= 16 ? "short" : "",
                    ].filter(Boolean).join(" ");
                    const isTarget = target && addr === `${target.sheet}!${target.col}${target.row}`;
                    return (
                      <td
                        key={key}
                        {...span.get(key)}
                        className={classes || undefined}
                        ref={isTarget ? flashRef : undefined}
                        title={cited.get(addr) ?? sheet.notes[`${sheet.letters[ci]}${r}`]}
                        onClick={() => pick(addr)}
                      >
                        {value}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {selected && (
        <div className="inspector" aria-live="polite">
          <span className="addr">{selected}</span>
          {selRule && /^[A-Z]{3}-\d{3}$/.test(selRule) && <span className="pill forest">{selRule}</span>}
          {selStatus && <span className="pill">{selStatus}</span>}
          <span className="val">{selValue || <span style={{ color: "var(--night-muted)" }}>empty</span>}{selNote ? ` · note: ${selNote}` : ""}</span>
          {selFinding && <Link href={`/run#${selFinding.split(" ")[0]}`}>{selFinding} →</Link>}
          <button onClick={copy}>{copied ? "Copied" : "Copy link"}</button>
        </div>
      )}
    </main>
  );
}
