## Frontend Infrastructure

The frontend is containerized and included in the repository-level Docker Compose stack.

## Environment

Create `web/.env` from `web/.env.example` when you need to override defaults locally.

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

## Docker Run

From the repository root:

```bash
docker compose up --build web
```

The frontend is exposed on `http://localhost:3000`.

## Docker Dev Run

For hot reload inside Docker:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build web
```
