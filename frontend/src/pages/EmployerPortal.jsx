import { useState } from "react";
import { createVacancy } from "../api.js";

// Prototype only. TODO: real employer sign-in with multi-factor authentication.
export default function EmployerPortal() {
  const [apiKey, setApiKey] = useState("");
  const [title, setTitle] = useState("");
  const [applyUrl, setApplyUrl] = useState("");
  const [out, setOut] = useState(null);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    try { setOut(await createVacancy(apiKey, { title, apply_url: applyUrl })); } catch { setError("Could not create the vacancy. Check your key."); }
  }

  return (
    <section>
      <h2>Employer portal</h2>
      <form onSubmit={submit}>
        <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="Employer API key (demo)" />
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Vacancy title" />
        <input value={applyUrl} onChange={(e) => setApplyUrl(e.target.value)} placeholder="Official application link" />
        <button type="submit">Approve vacancy and issue passport</button>
      </form>
      {error && <p className="err">{error}</p>}
      {out && <div className="result verified"><h3>Passport issued</h3><p>Passport ID: {out.passport_id}</p><p>Verify link: {out.verify_url}</p></div>}
    </section>
  );
}
