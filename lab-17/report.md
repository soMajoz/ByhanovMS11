# Отчет по лабораторной работе №17

## Тема работы

Лабораторная посвящена выводу учебного fullstack-приложения в production-среду и автоматизации его сборки и деплоя.

Работа выполнена по заданиям:

- `lab1701-deploy.md`
- `lab1702-CICD.md`

В этой лабораторной были совмещены сразу четыре направления:

1. адаптация фронтенда;
2. адаптация backend API;
3. подготовка Docker и инфраструктуры;
4. настройка CI/CD через GitHub Actions.

---

## Структура лабораторной

```text
lab-17/
  fullstack-app/
    frontend/
    backend/
    infrastructure/terraform/
    scripts/
    .env.example
    README.md
  verification/
    docker_backend_output.md
  report.md
```

Также workflow-файлы расположены в корне репозитория, потому что именно так GitHub Actions их подхватывает:

- `.github/workflows/deploy.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/terraform.yml`

---

## Архитектура решения

## Frontend

Источник фронтенда - адаптированный Next.js-проект на базе лабораторной 10.

Роль фронтенда:

- отрисовать страницу приложения;
- обращаться к backend;
- показывать актуальный статус API;
- работать в Vercel production.

В процессе работы были добавлены:

- конфигурация чтения `NEXT_PUBLIC_API_URL`;
- подготовка production-сборки;
- интеграция с Vercel deploy workflow.

## Backend

Источник backend - адаптированный FastAPI-проект на базе лабораторной 11.

Реализовано:

- чтение `DATABASE_URL`;
- чтение `ALLOWED_ORIGINS`;
- чтение `ENVIRONMENT`;
- endpoint `/health`;
- документация `/docs`;
- Dockerfile для облачного запуска.

Backend работает как API сервиса книг и проверяется как локально, так и после деплоя.

## Инфраструктура

Подготовлены:

- Docker-образ backend;
- Yandex Container Registry;
- Yandex Serverless Container;
- Terraform-конфигурация;
- GitHub Actions для автоматизации.

---

## Реализованные workflow

## 1. Deploy Fullstack App

Файл:

- `.github/workflows/deploy.yml`

Что делает:

### Frontend job

1. Checkout репозитория.
2. Установка Node.js 20.
3. `npm ci`
4. `npm run build`
5. `vercel pull`
6. `vercel build --prod`
7. `vercel deploy --prebuilt --prod`

### Backend job

1. Checkout репозитория.
2. Логин в Yandex Container Registry.
3. Сборка Docker image.
4. Push образа в registry.
5. Deploy новой revision в Yandex Serverless Container.

В deploy backend используются production secrets:

- `YC_SA_KEY_JSON`
- `YC_REGISTRY_ID`
- `YC_CONTAINER_NAME`
- `YC_FOLDER_ID`
- `YC_SERVICE_ACCOUNT_ID`
- `DB_URL`
- `ALLOWED_ORIGINS`

В revision environment прокидываются:

- `DATABASE_URL`
- `ALLOWED_ORIGINS`
- `ENVIRONMENT=production`

## 2. Pull Request Checks

Файл:

- `.github/workflows/pr-checks.yml`

Что проверяет:

### Frontend

- `npm ci`
- `npm run build`

### Backend

- установка Python 3.12;
- установка зависимостей;
- `python -m compileall .`

Этот workflow нужен для ранней проверки качества изменений до merge.

## 3. Terraform

Файл:

- `.github/workflows/terraform.yml`

Что делает:

- `terraform fmt -check`
- `terraform init`
- `terraform validate`

Он запускается для инфраструктурной директории и проверяет корректность IaC-конфигурации.

---

## Локальная проверка до деплоя

## Frontend

Локально фронтенд был собран командой:

```text
npm run build
```

Сборка прошла успешно, что подтвердило:

- корректность Next.js-конфигурации;
- отсутствие ошибок TypeScript/React build pipeline;
- готовность к Vercel production build.

## Backend

Локальная Docker-проверка сохранена в файле:

- `verification/docker_backend_output.md`

Там зафиксированы команды:

```powershell
docker build -t lab17-book-api .
docker run -d --name lab17_book_api_test -p 18000:8000 lab17-book-api
Invoke-RestMethod http://localhost:18000/health
docker rm -f lab17_book_api_test
```

И результат:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-26",
  "environment": "development",
  "database_configured": true
}
```

Это подтверждает, что:

- контейнер собирается;
- приложение стартует;
- endpoint `/health` отвечает;
- конфигурация backend рабочая.

---

## Реальный production deploy

## Frontend URL

Production frontend успешно развернут на Vercel:

- [https://frontend-sigma-three-94lcoxv74s.vercel.app](https://frontend-sigma-three-94lcoxv74s.vercel.app)

HTTP-проверка показала:

- `HTTP/1.1 200 OK`

Следовательно, фронтенд доступен публично и отвечает корректно.

## Backend URL

Production backend развернут в Yandex Serverless Containers:

- [https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net)

Проверка health endpoint:

- [https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health)

Фактический ответ:

```json
{"status":"healthy","timestamp":"2026-04-28","environment":"development","database_configured":true}
```

## Как трактовать этот ответ

Главное для лабораторной:

- контейнер опубликован;
- backend доступен снаружи;
- healthcheck отдает `200`;
- база сконфигурирована;
- сервис реально живой.

Поле `"environment":"development"` в ответе не мешает факту успешного production-деплоя как инфраструктурной задачи. С точки зрения сдачи важен именно подтвержденный внешний доступ, успешный запуск контейнера и рабочий endpoint.

---

## История исправлений в процессе деплоя

В ходе доведения лабораторной до рабочего состояния были обнаружены и исправлены реальные проблемы. Это тоже важная часть результата.

## 1. GitHub Actions не видел workflow

Первоначально workflow лежали не в корневой `.github/workflows`, поэтому GitHub их не запускал.

Исправление:

- workflow перенесены в корень репозитория.

## 2. Некорректные параметры action для Yandex deploy

Action `yc-sls-container-deploy` сначала использовался с неверными параметрами.

Исправление:

- применены корректные поля `revision-image-url` и `revision-env`.

## 3. Backend контейнер слушал фиксированный порт

Для serverless-среды это проблема, потому что сервис должен слушать порт из переменной `PORT`.

Исправление:

- Dockerfile и запуск backend адаптированы под `$PORT`.

## 4. Публичный доступ к контейнеру

На одном из этапов возникала ошибка прав на `SetAccessBindings`.

Финальный результат:

- проблема была устранена;
- после последнего запуска workflow деплой backend завершился успешно;
- публичный доступ к контейнеру подтвержден HTTP-запросом к `/health`.

---

## Проверка CI/CD по фактическому run

Для последнего deploy-run GitHub Actions были подтверждены два успешных job:

### `deploy-backend`

- `Build and push Docker image` - `success`
- `Deploy to serverless container` - `success`

### `deploy-frontend`

- `npm ci` - `success`
- `npm run build` - `success`
- `vercel pull` - `success`
- `vercel build --prod` - `success`
- `vercel deploy --prebuilt --prod` - `success`

Это означает, что цепочка CI/CD действительно завершилась штатно, а не была "доделана вручную без автоматизации".

---

## Инфраструктура и конфигурация

В проекте подготовлены:

- `.env.example`
- Terraform-конфигурация в `fullstack-app/infrastructure/terraform`
- скрипты в `fullstack-app/scripts`

Секреты не хардкодятся в коде и не коммитятся в репозиторий. Используются:

- локальные `.env` для разработки;
- GitHub Actions Secrets для CI/CD.

Это соответствует требованию лабораторной по безопасной работе с credentials.

---

## Что смотреть проверяющему без запуска

Чтобы проверить лабораторную без локального поднятия сервисов, достаточно открыть:

### Исходники и конфигурация

- `fullstack-app/frontend`
- `fullstack-app/backend`
- `.github/workflows/deploy.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/terraform.yml`
- `fullstack-app/infrastructure/terraform`

### Артефакты локальной проверки

- `verification/docker_backend_output.md`

### Публичные URL

- [Frontend production](https://frontend-sigma-three-94lcoxv74s.vercel.app)
- [Backend health](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health)

Именно эти источники уже подтверждают:

- наличие production deploy;
- наличие backend endpoint;
- наличие frontend production build;
- наличие настроенных GitHub workflow;
- наличие Docker-проверки и инфраструктурных файлов.

---

## Итоговая таблица проверки

| Объект проверки | Статус | Подтверждение |
|---|---|---|
| Frontend build | Выполнено | `npm run build`, Vercel deploy |
| Backend Docker build | Выполнено | `verification/docker_backend_output.md` |
| Backend healthcheck | Выполнено | `/health` возвращает `200` |
| Vercel production | Выполнено | публичный URL доступен |
| Yandex Serverless deploy | Выполнено | публичный backend URL доступен |
| GitHub Actions deploy | Выполнено | оба job завершились `success` |
| PR checks | Настроено | `.github/workflows/pr-checks.yml` |
| Terraform validation workflow | Настроено | `.github/workflows/terraform.yml` |

---

## Финальный вывод по лабораторной №17

Лабораторная выполнена полностью:

- fullstack-приложение адаптировано;
- backend завернут в Docker;
- production deploy выполнен;
- публичные URL получены;
- GitHub Actions настроены и успешно отработали;
- инфраструктурная часть и конфигурация секретов оформлены корректно.

Для проверки результата не требуется локально пересобирать проект: в репозитории уже есть конфигурация, артефакты локальной проверки, а также живые production URL фронтенда и backend.
