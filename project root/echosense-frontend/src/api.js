// echosense-frontend/src/api.js
export const BACKEND_BASE = "http://127.0.0.1:8000";

export async function processYoutube(url) {
  const res = await fetch(`${BACKEND_BASE}/youtube/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt);
  }
  return res.json();
}
