# PostgreSQL verification

Planned command:

```powershell
docker compose up -d
docker compose exec postgres psql -U lab_user -d shop_analytics -f /work/schema.sql
docker compose exec postgres psql -U lab_user -d shop_analytics -f /work/queries.sql
docker compose exec postgres psql -U lab_user -d shop_analytics -f /work/index_analysis.sql
```

Actual local environment status on 2026-04-26:

- `docker compose up -d` was attempted.
- Docker Desktop daemon was not running.
- Error: `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`.
- `psql` is not installed on the host, so direct host execution was unavailable.

