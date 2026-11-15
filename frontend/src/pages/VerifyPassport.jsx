import { useEffect, useState } from "react";
import { getPassport } from "../api.js";

export default function VerifyPassport({ initialId = "" }) {
  const [id, setId] = useState(initialId);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  async function verify(pid = id) {
    setError("");
    try { setData(await getPassport(pid)); } catch { setError("Could not verify right now."); }
  }
  useEffect(() => { if (initialId) verify(initialId); }, []);

  return (
    <section>
      <h2>Verify a passport</h2>
      <input value={id} onChange={(e) => setId(e.target.value)} placeholder="Passport ID (or scan the QR code)" />
      <button onClick={() => verify()}>Verify</button>
      {error && <p className="err">{error}</p>}
      {data && (
        <div className={`result ${data.status === "valid" ? "verified" : "high_risk"}`}>
          <h3>{data.status === "valid" ? "Verified Vacancy Passport" : `Passport ${data.status}`}</h3>
          {data.employer && <p>Employer: {data.employer}</p>}
          {data.recruiter && <p>Recruiter: {data.recruiter}</p>}
          {data.vacancy && <p>Vacancy: {data.vacancy}</p>}
          {data.expires_at && <p>Expires: {new Date(data.expires_at).toLocaleDateString()}</p>}
          <small>Checked {new Date(data.checked_at).toLocaleString()}</small>
        </div>
      )}
    </section>
  );
}
