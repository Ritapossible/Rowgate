import { useEffect, useState } from "react";
import { Link, useLocation } from "../router";

/** A gate made of an arch and a spreadsheet row; the amber cell is the one a release breaks. */
export function Logo({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true">
      <rect width="64" height="64" rx="16" fill="var(--logo-tile)" />
      <path d="M17 51V29a15 15 0 0 1 30 0v22" fill="none" stroke="var(--logo-ink)" strokeWidth="6" strokeLinecap="round" />
      <rect x="17" y="34" width="30" height="8" fill="var(--logo-ink)" opacity="0.38" />
      <rect x="27" y="31" width="10" height="14" rx="2" fill="var(--logo-cell)" />
    </svg>
  );
}

type Theme = "light" | "dark";

function systemTheme(): Theme {
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => (document.documentElement.dataset.theme as Theme) || systemTheme());
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);
  const next: Theme = theme === "dark" ? "light" : "dark";
  const toggle = () => {
    setTheme(next);
    try {
      localStorage.setItem("rowgate-theme", next);
    } catch {
      /* storage unavailable: theme still switches for this visit */
    }
  };
  return (
    <button className="icon-btn" onClick={toggle} aria-label={`Switch to ${next} theme`} title={`Switch to ${next} theme`}>
      {theme === "dark" ? (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
          <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" />
        </svg>
      ) : (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
          <circle cx="12" cy="12" r="4.2" fill="currentColor" />
          <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4" />
        </svg>
      )}
    </button>
  );
}

export function GitHubIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.1-1.46-1.1-1.46-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.08.63-1.33-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2Z" />
    </svg>
  );
}

export const REPO = "https://github.com/Ritapossible/Rowgate";

export function Nav() {
  const { path } = useLocation();
  const links = [
    ["/", "Overview"],
    ["/run", "Run"],
    ["/contract", "Contract"],
  ];
  return (
    <header className="nav">
      <div className="wrap nav-inner">
        <Link href="/" className="brand" aria-label="Rowgate home">
          <Logo />
          <span className="brand-name">Rowgate</span>
        </Link>
        <nav className="nav-links" aria-label="Main">
          {links.map(([href, label]) => (
            <Link key={href} href={href} className="nav-link" aria-current={path === href ? "page" : undefined}>
              {label}
            </Link>
          ))}
        </nav>
        <ThemeToggle />
        <a className="icon-btn hide-sm" href={REPO} target="_blank" rel="noreferrer" aria-label="Source on GitHub">
          <GitHubIcon />
        </a>
      </div>
    </header>
  );
}

export function Footer({ exportedAt }: { exportedAt?: string }) {
  return (
    <footer className="footer">
      <div className="wrap footer-inner">
        <div>
          <b style={{ color: "var(--forest)" }}>Rowgate</b> · built with IBM Bob for the IBM Bob 2.0 Hackathon (lablab.ai). MIT licensed.
          <br />
          Independent project, not affiliated with IBM. The Kora partner, API and contract are fictional demo material.
        </div>
        <div>
          <a href={REPO} target="_blank" rel="noreferrer">
            Source on GitHub
          </a>
          {exportedAt && <span> · data exported {exportedAt}</span>}
        </div>
      </div>
    </footer>
  );
}
