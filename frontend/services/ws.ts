export function openChatSocket(onEvent: (e: any) => void) {
  const url = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";
  const ws = new WebSocket(`${url}/chat`);
  ws.onmessage = (m) => { try { onEvent(JSON.parse(m.data)); } catch {} };
  return ws;
}
