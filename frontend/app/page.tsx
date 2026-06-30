"use client";
import ChatPanel from "../components/ChatPanel";
import AgentMonitor from "../components/AgentMonitor";

export default function Home() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
      <div className="lg:col-span-2"><ChatPanel /></div>
      <div className="lg:col-span-1"><AgentMonitor /></div>
    </div>
  );
}
