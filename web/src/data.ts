import { useEffect, useState } from "react";

export type Sheet = {
  name: string;
  maxRow: number;
  maxCol: number;
  letters: string[];
  headerRow: number | null;
  statusCol: number | null;
  cells: string[][];
  merges: { r1: number; c1: number; r2: number; c2: number }[];
  rowStatus: Record<string, string>;
  notes: Record<string, string>;
};

export type Contract = {
  workbook: string;
  title: string;
  partner: string;
  version: string;
  signed: string;
  totals: { rules: number; ACTIVE: number; PLANNED: number; DEPRECATED: number; BREAKING: number };
  sheets: Sheet[];
};

export type DiffLine = { kind: string; text: string; old?: number | null; new?: number | null };
export type PR = {
  branch: string;
  base: string;
  commits: { sha: string; subject: string }[];
  files: { path: string; added: number; removed: number; hunks: { header: string; lines: DiffLine[] }[] }[];
};

export type CitedRow = {
  sheet: string;
  letters: string[];
  headers: string[];
  cells: string[];
  row: number;
  hit: number;
} | null;

export type Finding = {
  id: string;
  cell: string;
  related_cells?: string[];
  rule?: string;
  contract_says: string;
  code_does: string;
  evidence: { file: string; line?: number };
  reasoning: string;
  test: string;
  decision: "pending" | "fix_code" | "record_breaking" | "reject";
  decided_by?: string;
  fix_commit?: string;
  workbook_edit?: { cells?: Record<string, string>; changelog_row?: number } | null;
  row: CitedRow;
  related: CitedRow[];
  diff: { kind: string; text: string }[];
  before?: string | null;
  after?: string | null;
};

export type Skipped = {
  cell: string;
  change?: string;
  why: string;
  evidence?: { file: string; line?: number };
  row: CitedRow;
  diff: { kind: string; text: string }[];
};

export type Run = {
  doc: { branch: string; base: string; workbook: string; workbook_version?: string };
  findings: Finding[];
  skipped: Skipped[];
  counts: { breaks: number; skipped: number; red_before: number; green_after: number; recorded: number; cells_changed: number };
  problems: string[];
  changes: { cell: string; old: string; new: string }[] | null;
  head: string | null;
  generated: string;
};

export type Site = { exportedAt: string; head: string; hasRun: boolean; hasDossier: boolean; repo: string };

type State<T> = { data: T | null; missing: boolean; error: string | null };

const cache = new Map<string, Promise<unknown>>();

function load(path: string): Promise<unknown> {
  if (!cache.has(path)) {
    cache.set(
      path,
      fetch(`/data/${path}`).then((r) => {
        if (r.status === 404) return null;
        if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`);
        const type = r.headers.get("content-type") || "";
        return type.includes("json") ? r.json() : null; // SPA fallback returns HTML for missing files
      }),
    );
  }
  return cache.get(path)!;
}

export function useData<T>(path: string | null): State<T> & { loading: boolean } {
  const [state, setState] = useState<State<T> & { loading: boolean }>({ data: null, missing: false, error: null, loading: path !== null });
  useEffect(() => {
    if (path === null) {
      setState({ data: null, missing: true, error: null, loading: false });
      return;
    }
    let live = true;
    load(path)
      .then((d) => live && setState({ data: d as T | null, missing: d === null, error: null, loading: false }))
      .catch((e: Error) => live && setState({ data: null, missing: false, error: e.message, loading: false }));
    return () => {
      live = false;
    };
  }, [path]);
  return state;
}

export function useRun() {
  const site = useData<Site>("site.json");
  const run = useData<Run>(site.data?.hasRun ? "run.json" : null);
  const loading = site.loading || (site.data?.hasRun ? run.loading : false);
  return { site: site.data, run: site.data?.hasRun ? run.data : null, loading };
}
