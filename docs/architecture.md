# LEXI Architecture

## High-Level Flow

```
User → API/WebSocket → Brain → ThinkingEngine → AgentRouter
                                                ├── PlannerAgent
                                                ├── ResearchAgent
                                                ├── ReasoningAgent
                                                ├── CodingAgent
                                                ├── VisionAgent
                                                ├── VoiceAgent
                                                ├── MemoryAgent
                                                ├── TaskExecutionAgent
                                                ├── CriticAgent
                                                └── ReflectionAgent

                              ▼
                       Tool Registry (sandboxed)
                              ▼
                    Memory Layer (STM + LTM + Vector)
                              ▼
                      PostgreSQL · Redis · Chroma/FAISS
```

## Hidden Chain-of-Thought Pipeline
Every user turn flows through the Brain in this order:

1. **Intent analysis** — `ThinkingEngine.plan()`
2. **Context building** — `ContextManager.build()` (short-term + profile)
3. **Memory recall** — `MemoryRouter.recall()` (vector + scoring)
4. **Routing** — `AgentRouter.route()` picks the minimal agent subset
5. **Execution** — agents run sequentially, sharing the running context
6. **Reflection** — `ThinkingEngine.reflect()` critiques the trace
7. **Personality** — `PersonalityEngine.style()` tones the final text
8. **Persistence** — meaningful turns are written to LTM

Internal thoughts are **never** exposed to the user; they are stored in
`BrainResponse.thoughts` for the AgentMonitor UI and structured logs only.

## Memory Model
- **Short-term**: rolling deque per (user, session), mirrored in Redis.
- **Long-term**:
  - structured profile/facts → PostgreSQL (`user_profiles`, `memory_facts`)
  - semantic recall → vector store (ChromaDB primary, FAISS fallback)
- **Compression**: Celery beat task `summarize_sessions` rolls up old turns.
- **Pruning**: nightly Celery task drops low-score memories.

## Voice Pipeline
`Mic → Whisper STT → Brain.think() → TTS (Coqui / ElevenLabs / OpenAI) → speaker`.
Wake-word can be Porcupine (when an access key is set) or a Whisper-text matcher.

## Vision Pipeline
`Screenshot/Webcam → OCR + Multimodal LLM → ScreenParser fusion → Brain context`.
