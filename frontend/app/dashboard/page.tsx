"use client";
import { useEffect, useState } from "react";
import { api } from "../../services/api";

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null);
  useEffect(() => { api.get("/api/system/status").then(setStatus); }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-2xl text-lexi-accent font-mono">SYSTEM DASHBOARD</h1>
      <pre className="glass p-4 rounded-lg text-sm">{JSON.stringify(status, null, 2)}</pre>
    </div>
  );
}
