"use client";
import { useEffect, useState } from "react";
import { api } from "../../services/api";

export default function ToolsPage() {
  const [tools, setTools] = useState<any[]>([]);
  useEffect(() => { api.get("/api/tools").then(setTools); }, []);
  return (
    <div>
      <h1 className="text-2xl text-lexi-accent font-mono mb-4">TOOLS</h1>
      <ul className="grid gap-2 md:grid-cols-2">
        {tools.map((t) => (
          <li key={t.name} className="glass p-4 rounded">
            <div className="font-mono text-lexi-accent2">{t.name}</div>
            <div className="text-sm text-lexi-muted">{t.description}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
