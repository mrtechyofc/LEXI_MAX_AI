# LEXI Deployment Guide

## Local (docker-compose)
```bash
cp .env.example .env  # add OPENAI_API_KEY etc.
docker compose up --build
```
Services: backend (8000), frontend (3000), postgres, redis, chroma, prometheus, grafana, celery worker/beat/flower.

## Kubernetes
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
cp kubernetes/secrets.example.yaml kubernetes/secrets.yaml   # fill in real secrets
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/worker-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## Production checklist
- [ ] Replace `LEXI_SECRET_KEY` with a 64-byte random string.
- [ ] Pin LLM provider keys in your secret manager (Vault, AWS SM, GCP SM).
- [ ] Configure managed Postgres + Redis (e.g. RDS, ElastiCache).
- [ ] Use a managed vector store at scale (Pinecone, Weaviate, pgvector).
- [ ] TLS via cert-manager + Let's Encrypt.
- [ ] Enable OTEL exporter (`OTEL_EXPORTER_OTLP_ENDPOINT`).
- [ ] Restrict CORS to your real frontend host.
- [ ] Move terminal/code tools to a hardened sandbox (Firecracker / gVisor).
