# Отчет по лабораторной работе №17

## Часть 1. Деплой веб-приложения

Цель части: подготовить фронтенд, backend API, Docker-образ и облачный деплой.

В `fullstack-app/frontend` адаптирован Next.js проект из лабораторной 10.2. Главная страница читает `NEXT_PUBLIC_API_URL` и показывает статус `/health` backend API. Добавлены `.env.production.example` и `vercel.json`.

В `fullstack-app/backend` адаптирован FastAPI проект из лабораторной 11.1. Сохранены endpoints библиотеки книг, OpenAPI доступен по `/docs`, healthcheck доступен по `/health`. Добавлены:

- `config.py` для `DATABASE_URL`, `ALLOWED_ORIGINS`, `ENVIRONMENT`;
- `Dockerfile` и `.dockerignore`;
- зависимости `sqlalchemy` и `psycopg[binary]` для production PostgreSQL-конфигурации.

Локальная проверка фронтенда:

```text
npm run build
Compiled successfully
Generating static pages (10/10)
```

После запуска Docker Desktop backend image собран командой `docker build -t lab17-book-api .`. Контейнерный запуск проверен на порту `18000`, endpoint `/health` вернул:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-26",
  "environment": "development",
  "database_configured": true
}
```

## Часть 2. CI/CD

Цель части: подготовить автоматизацию сборки, тестирования, инфраструктуры и деплоя.

В `fullstack-app/.github/workflows` добавлены:

- `pr-checks.yml`: сборка frontend и compile-проверка backend;
- `deploy.yml`: деплой frontend в Vercel и backend Docker image в Yandex Cloud;
- `terraform.yml`: `terraform fmt`, `init`, `validate`.

В `fullstack-app/infrastructure/terraform` добавлены `main.tf`, `variables.tf`, `terraform.tfvars.example` для service account, Container Registry и Managed PostgreSQL. В `scripts/` добавлены PowerShell-скрипты локального тестирования и ручного деплоя.

## Верификация

Backend прошел `python -m compileall .`, `docker build -t lab17-book-api .` и контейнерную проверку `/health`. Frontend прошел `npm run build`. Terraform CLI не установлен на локальной машине, поэтому `terraform validate` не запускался локально. Реальный деплой Vercel/Yandex Cloud требует заполненных GitHub Actions Secrets и локальных/облачных учетных данных.
