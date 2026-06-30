"use client";
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useChatStore } from "../store/chat";

export default function ChatPanel() {
  const { messages, send } = useChatStore();
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const onSend = async () => {
    if (!input.trim()) return;
    const msg = input; setInput("");
    await send(msg);
  };

  return (
    <div className="glass rounded-lg h-full flex flex-col">
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3 scanline">
        <AnimatePresence>
          {messages.map((m, i) => (
            <motion.div key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`max-w-[80%] p-3 rounded ${
                m.role === "user" ? "ml-auto bg-lexi-accent/10" : "bg-white/5"
              }`}>
              <div className="text-xs text-lexi-muted mb-1">{m.role.toUpperCase()}</div>
              <div className="whitespace-pre-wrap">{m.content}</div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <div className="border-t border-white/5 p-3 flex gap-2">
        <input className="flex-1 bg-lexi-panel rounded px-3 py-2"
               placeholder="Talk to LEXI…"
               value={input}
               onKeyDown={(e) => e.key === "Enter" && onSend()}
               onChange={(e) => setInput(e.target.value)} />
        <button onClick={onSend} className="px-4 py-2 bg-lexi-accent text-black rounded">Send</button>
      </div>
    </div>
  );
}
