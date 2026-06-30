"use client";
import { useState, useRef } from "react";

export default function VoiceConsole() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const mediaRecRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);

  const toggle = async () => {
    if (recording) {
      mediaRecRef.current?.stop();
      setRecording(false);
      return;
    }
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    chunksRef.current = [];
    rec.ondataavailable = (e) => chunksRef.current.push(e.data);
    rec.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      const form = new FormData(); form.append("file", blob, "audio.webm");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/voice/turn`, { method: "POST", body: form });
      const data = await res.json();
      setTranscript(`YOU: ${data.transcript}\nLEXI: ${data.response_text}`);
    };
    rec.start();
    mediaRecRef.current = rec;
    setRecording(true);
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl text-lexi-accent font-mono">VOICE CONSOLE</h1>
      <button onClick={toggle}
              className={`px-6 py-3 rounded ${recording ? "bg-lexi-danger" : "bg-lexi-accent text-black"}`}>
        {recording ? "Stop" : "Record"}
      </button>
      <pre className="glass p-4 rounded whitespace-pre-wrap">{transcript}</pre>
    </div>
  );
}
