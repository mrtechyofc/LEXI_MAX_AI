"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Cpu, MessageSquare, Database, Wrench, Settings, ScrollText, Mic } from "lucide-react";

const items = [
  { href: "/",          label: "Chat",      icon: MessageSquare },
  { href: "/dashboard", label: "Dashboard", icon: Cpu },
  { href: "/memory",    label: "Memory",    icon: Database },
  { href: "/tools",     label: "Tools",     icon: Wrench },
  { href: "/voice",     label: "Voice",     icon: Mic },
  { href: "/logs",      label: "Logs",      icon: ScrollText },
  { href: "/settings",  label: "Settings",  icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-56 glass border-r border-white/5 p-4 flex flex-col gap-2">
      <div className="text-2xl font-mono text-lexi-accent mb-4 tracking-wider">L · E · X · I</div>
      {items.map((it) => {
        const Icon = it.icon;
        const active = pathname === it.href;
        return (
          <Link key={it.href} href={it.href}
                className={`flex items-center gap-3 px-3 py-2 rounded transition ${
                  active ? "bg-lexi-accent/10 text-lexi-accent" : "text-lexi-muted hover:text-white"
                }`}>
            <Icon size={16} /> <span>{it.label}</span>
          </Link>
        );
      })}
    </aside>
  );
}
