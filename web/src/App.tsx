import { useEffect } from "react";
import { Footer, Nav } from "./components/Chrome";
import { useData, useRun, type Contract, type PR } from "./data";
import ContractPage from "./pages/Contract";
import Docs from "./pages/Docs";
import Home from "./pages/Home";
import RunPage from "./pages/Run";
import { Link, useLocation } from "./router";

const TITLES: Record<string, string> = {
  "/": "Rowgate · the signed contract, as a release gate",
  "/run": "Run · Rowgate",
  "/contract": "Contract · Rowgate",
  "/docs": "Docs · Rowgate",
};

export default function App() {
  const { path } = useLocation();
  const contract = useData<Contract>("contract.json").data;
  const pr = useData<PR>("pr.json").data;
  const { site, run, loading } = useRun();

  useEffect(() => {
    document.title = TITLES[path] ?? "Rowgate";
  }, [path]);

  useEffect(() => {
    if (!loading && window.location.hash) document.getElementById(window.location.hash.slice(1))?.scrollIntoView({ block: "start" });
  }, [loading, path]);

  let page;
  if (path === "/") page = <Home contract={contract} pr={pr} run={run} />;
  else if (path === "/run") page = <RunPage run={run} pr={pr} loading={loading} hasDossier={!!site?.hasDossier} />;
  else if (path === "/contract") page = <ContractPage contract={contract} run={run} />;
  else if (path === "/docs") page = <Docs />;
  else
    page = (
      <main className="wrap page-head">
        <h1 className="display">Not here.</h1>
        <p className="lede">That page does not exist. <Link className="text-link" href="/">Back to the overview</Link>.</p>
      </main>
    );

  return (
    <>
      <Nav />
      {page}
      <Footer exportedAt={site?.exportedAt} />
    </>
  );
}
