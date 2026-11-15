const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export const checkJob = (body) => request("/v1/check", { method: "POST", body: JSON.stringify(body) });
export const getPassport = (id) => request(`/v1/passport/${encodeURIComponent(id)}`);
export const reportScam = (body) => request("/v1/report", { method: "POST", body: JSON.stringify(body) });
export const createVacancy = (apiKey, body) =>
  request("/v1/employer/vacancies", { method: "POST", headers: { "X-API-Key": apiKey }, body: JSON.stringify(body) });
