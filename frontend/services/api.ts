const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function call(method: string, path: string, body?: any) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`${method} ${path} failed: ${res.status}`);
  return res.json();
}

export const api = {
  get:  (p: string)        => call("GET", p),
  post: (p: string, b: any) => call("POST", p, b),
};
