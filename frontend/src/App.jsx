import { useState } from "react";
import CheckJob from "./pages/CheckJob.jsx";
import VerifyPassport from "./pages/VerifyPassport.jsx";
import EmployerPortal from "./pages/EmployerPortal.jsx";

const TABS = [
  ["check", "Check a job"],
  ["passport", "Verify a passport"],
  ["employer", "Employers"],
];

export default function App() {
  const [tab, setTab] = useState("check");
  // Passport links look like /verify/<id>
  const linkedId = window.location.pathname.startsWith("/verify/") ? window.location.pathname.split("/")[2] : "";
  return (
    <main className="wrap">
      <header>
        <h1>JobShield</h1>
        <p className="tag">Apply with proof. Real jobs never charge you.</p>
        <nav>
          {TABS.map(([id, label]) => (
            <button key={id} className={tab === id ? "on" : ""} onClick={() => setTab(id)}>{label}</button>
          ))}
        </nav>
      </header>
      {tab === "check" && <CheckJob />}
      {tab === "passport" && <VerifyPassport initialId={linkedId} />}
      {tab === "employer" && <EmployerPortal />}
      <footer>Evidence-backed verification and risk rating. JobShield never guarantees that a job is genuine. Prototype data is simulated.</footer>
    </main>
  );
}
