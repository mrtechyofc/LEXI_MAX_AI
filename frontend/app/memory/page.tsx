"use client";
import { useState } from "react";
import { api } from "../../services/api";

export default function MemoryPage() {
  const [q, setQ] = useState(""); const [hits, setHits] = useState<any[]>([]);
  const search = async () => setHits(await api.post("/api/memory/search", { query: q, k: 10 }));
  return (
    <div className="space-y-4">
      <h1 className="text-2xl text-lexi-accent font-mono">MEMORY</h1>
      <div className="flex gap-2">
        <input className="bg-lexi-panel rounded px-3 py-2 flex-1"
               placeholder="search semantic memory…"
               value={q} onChange={(e) => setQ(e.target.value)} />
        <button onClick={search} className="px-4 py-2 bg-lexi-accent text-black rounded">Search</button>
      </div>
      <div className="space-y-2">
        {hits.map((h) => (
          <div key={h.id} className="glass p-3 rounded">
            <div className="text-xs text-lexi-muted">score {h.score.toFixed(3)}</div>
            <div>{h.text}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
