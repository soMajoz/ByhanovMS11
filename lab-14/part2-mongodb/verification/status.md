# MongoDB verification

Planned command:

```powershell
docker compose up -d
docker compose exec mongodb mongosh /work/init.js
docker compose exec mongodb mongosh /work/queries.js
docker compose exec mongodb mongosh /work/comparison.js
docker compose exec mongodb mongosh /work/indexes.js
```

Actual local environment status on 2026-04-26:

- MongoDB JavaScript files passed syntax check with `node --check`.
- Docker Desktop daemon was not running, so MongoDB container execution could not be started.
- `mongosh` is not installed on the host.

