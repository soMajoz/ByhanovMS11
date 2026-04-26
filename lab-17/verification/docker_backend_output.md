# Backend Docker verification

Date: 2026-04-26

Commands:

```powershell
docker build -t lab17-book-api .
docker run -d --name lab17_book_api_test -p 18000:8000 lab17-book-api
Invoke-RestMethod http://localhost:18000/health
docker rm -f lab17_book_api_test
```

Result:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-26",
  "environment": "development",
  "database_configured": true
}
```

