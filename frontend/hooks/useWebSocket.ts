"use client";
import { useEffect, useRef } from "react";
export function useWebSocket(url: string, onMessage: (e: any) => void) {
  const ref = useRef<WebSocket | null>(null);
  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (m) => { try { onMessage(JSON.parse(m.data)); } catch {} };
    ref.current = ws;
    return () => ws.close();
  }, [url]);
  return ref;
}
