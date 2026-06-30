# Future Scaling Plan

| Stage | Change                                                          |
|-------|------------------------------------------------------------------|
| 1     | Single-node docker-compose                                       |
| 2     | k8s with HPA on backend + worker                                 |
| 3     | Managed Postgres (HA) + Redis cluster                            |
| 4     | Managed vector DB (pgvector / Pinecone / Weaviate)              |
| 5     | Split agents into separate deployments (per-agent autoscaling)   |
| 6     | gRPC inter-agent bus instead of in-process calls                 |
| 7     | LLM router with provider failover + cost-aware routing           |
| 8     | Edge nodes for voice/vision near users                           |
| 9     | Robotics gateway (ROS 2 bridge) + IoT MQTT broker                |
