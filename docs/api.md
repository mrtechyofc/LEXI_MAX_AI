# LEXI API Reference

All endpoints are served from `/api/...` and require a Bearer JWT *except*
`/api/auth/register` and `/api/auth/login`. In development the token can be
omitted; requests will be attributed to the `anonymous` user.

| Method | Path                       | Purpose                                  |
|--------|----------------------------|------------------------------------------|
| POST   | /api/auth/register         | Create user + return JWT                 |
| POST   | /api/auth/login            | Authenticate + return JWT                |
| GET    | /api/auth/me               | Inspect current user                     |
| POST   | /api/chat                  | One-shot chat (REST)                     |
| WS     | /ws/chat                   | Streaming chat (tokens + thoughts)       |
| GET    | /api/agents                | List available agents                    |
| GET    | /api/tools                 | List registered tools                    |
| POST   | /api/tools/{name}/invoke   | Direct tool invocation                   |
| POST   | /api/memory/search         | Semantic recall                          |
| POST   | /api/memory/write          | Manually add a memory                    |
| POST   | /api/voice/transcribe      | Audio file → text                        |
| POST   | /api/voice/synthesize      | Text → WAV/MP3                           |
| POST   | /api/voice/turn            | Audio in → audio out                     |
| POST   | /api/vision/describe       | Image → description                      |
| POST   | /api/vision/ocr            | Image → text                             |
| GET    | /api/vision/screen         | Screenshot + OCR + LLM description       |
| POST   | /api/tasks                 | Plan & execute a goal                    |
| GET    | /api/system/status         | Service status + introspection           |

See `/docs` (Swagger) for full schemas.
