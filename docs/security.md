# Security Best Practices

1. **Sandboxed tool execution** — the `terminal` tool runs only an allow-list of binaries; the `code_runner` executes in `python -I` with a strict timeout. Replace with Firecracker/gVisor for prod.
2. **Permission flags** on every tool (`network`, `filesystem_read/write`, `shell`) — agents must check before invocation in regulated environments.
3. **JWT** auth with HS256 (rotate `LEXI_SECRET_KEY`); upgrade to RS256 + JWKS for multi-service.
4. **Rate limiting** middleware caps abusive clients (60 req/s default).
5. **Encrypted secrets** — never bake into images. Use `lexi-secrets` (k8s) or Vault.
6. **Input validation** — Pydantic models gate every request.
7. **Path traversal protection** — `tools/files/reader.py` enforces a DATA_ROOT root.
8. **Audit logging** — every tool call is structured-logged with request_id.
9. **PII redaction** — extend `services/observability.py` with a redaction processor.
10. **Prompt-injection awareness** — Critic agent + memory provenance flags suspicious content.
