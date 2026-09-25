import type { CitedRow, DiffLine } from "../data";

export function Outcome({ value }: { value?: string | null }) {
  if (value === "failed") return <span className="pill red">red</span>;
  if (value === "passed") return <span className="pill green">green</span>;
  if (value) return <span className="pill amber">{value}</span>;
  return <span className="pill">not run</span>;
}

export function RowTable({ row }: { row: CitedRow }) {
  if (!row) return null;
  const heads = row.headers.length ? row.headers : row.letters.map(() => "");
  return (
    <div className="scroll">
      <table className="rowt">
        <thead>
          <tr>
            <th />
            {heads.map((h, i) => (
              <th key={i}>
                <small>{row.letters[i]}</small>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="n">{row.row}</td>
            {row.cells.map((c, i) => (
              <td key={i} className={i === row.hit ? "hit" : undefined}>
                {c}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export function Excerpt({ lines }: { lines: { kind: string; text: string }[] }) {
  if (!lines.length) return null;
  return (
    <pre className="diff">
      {lines.map((l, i) => (
        <span key={i} className={`ln ${l.kind}`}>
          {l.text}
        </span>
      ))}
    </pre>
  );
}

export function FileDiff({ path, added, removed, hunks, open }: {
  path: string; added: number; removed: number; hunks: { header: string; lines: DiffLine[] }[]; open?: boolean;
}) {
  return (
    <details className="file" open={open}>
      <summary>
        <span>{path}</span>
        <span className="spacer" />
        <span className="add">+{added}</span>
        <span className="del">−{removed}</span>
      </summary>
      <pre className="diff">
        {hunks.map((h, i) => (
          <span key={i}>
            <span className="ln at">{h.header}</span>
            {h.lines.map((l, j) => (
              <span key={j} className={`ln ${l.kind}`}>
                <span className="no">{l.new ?? l.old ?? ""}</span>
                {l.kind === "add" ? "+" : l.kind === "del" ? "−" : " "}
                {l.text}
              </span>
            ))}
          </span>
        ))}
      </pre>
    </details>
  );
}
