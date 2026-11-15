import { useState } from "react";
import { checkJob } from "../api.js";

const LABEL = { verified: "Verified", unverified: "Unverified", high_risk: "High risk" };

export default function CheckJob() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    try { setResult(await checkJob({ message })); } catch (err) { setError("Could not verify right now. Please try again."); }
  }

  return (
    <section>
      <h2>Check a job</h2>
      <form onSubmit={submit}>
        <textarea rows="6" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Paste the job message here" />
        <button type="submit">Check</button>
      </form>
      {error && <p className="err">{error}</p>}
      {result && (
        <div className={`result ${result.rating}`}>
          <h3>{LABEL[result.rating]}</h3>
          <p>{result.explanation}</p>
          <ul>{result.reasons.map((r) => <li key={r.id}>{r.text}</li>)}</ul>
          {result.trafficking_alert && <p className="err">Overseas offers can be trafficking lures. Do not pay or travel.</p>}
          <h4>What to do</h4>
          <ul>{result.advice.map((a) => <li key={a}>{a}</li>)}</ul>
          <small>{result.disclaimer}</small>
        </div>
      )}
    </section>
  );
}
