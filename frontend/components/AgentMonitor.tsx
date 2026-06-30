"use client";
import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function AgentMonitor() {
  const [agents, setAgents] = useState<any[]>([]);
  useEffect(() => { api.get("/api/agents").then(setAgents); }, []);
  return (
    <div className="glass rounded-lg p-4 h-full">
      <h2 className="text-lexi-accent font-mono mb-3">AGENTS</h2>
      <ul className="space-y-2 text-sm">
        {agents.map((a) => (
          <li key={a.name} className="flex justify-between border-b border-white/5 py-1">
            <span className="font-mono text-lexi-accent2">{a.name}</span>
            <span className="text-lexi-muted text-right max-w-[60%]">{a.description}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
