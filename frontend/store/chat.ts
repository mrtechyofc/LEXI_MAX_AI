"use client";
import { create } from "zustand";
import { openChatSocket } from "../services/ws";

type Msg = { role: "user" | "assistant"; content: string };
type State = {
  messages: Msg[];
  send: (text: string) => Promise<void>;
};

export const useChatStore = create<State>((set, get) => ({
  messages: [],
  send: async (text) => {
    set({ messages: [...get().messages, { role: "user", content: text }] });
    return new Promise((resolve) => {
      let buffer = "";
      const ws = openChatSocket((ev) => {
        if (ev.type === "token") {
          buffer += ev.value;
          set((s) => {
            const last = s.messages[s.messages.length - 1];
            if (last?.role === "assistant") {
              return { messages: [...s.messages.slice(0, -1), { ...last, content: buffer }] };
            }
            return { messages: [...s.messages, { role: "assistant", content: buffer }] };
          });
        }
        if (ev.type === "done") { ws.close(); resolve(); }
      });
      ws.onopen = () => ws.send(JSON.stringify({ user_id: "anonymous", message: text }));
    });
  },
}));
