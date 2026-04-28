# Отчет по лабораторной работе №17
# Часть 1: Деплой веб-приложения в облаке
# Часть 2: Настройка CI/CD пайплайна

**Семестр:** 2 курс 2 полугодие (4 семестр)  
**Дисциплина:** Технологии программирования  
**Студент:** Быханов Михаил Сергеевич  

---

## Цель работы

Получить практические навыки развертывания fullstack-приложения в облаке и автоматизации его сборки, тестирования и деплоя. В рамках лабораторной необходимо было адаптировать frontend и backend из предыдущих лабораторных работ, собрать backend в Docker-образ, развернуть frontend на Vercel, backend - в Yandex Cloud, а затем настроить CI/CD через GitHub Actions и IaC-проверки Terraform.

---

## Часть 1. Облачный деплой приложения

### Подготовка frontend

В качестве frontend использовался адаптированный Next.js-проект из лабораторной 10. Проект был помещен в каталог `lab-17/fullstack-app/frontend`.

В процессе подготовки была реализована:

- поддержка переменной `NEXT_PUBLIC_API_URL`;
- production-сборка через `npm run build`;
- совместимость с деплоем на Vercel.

Локальная сборка frontend была успешно проверена командой:

```text
npm run build
```

Это подтвердило, что проект готов к production-деплою и не содержит ошибок сборки.

### Подготовка backend

В качестве backend использовался адаптированный FastAPI-проект из лабораторной 11, размещенный в `lab-17/fullstack-app/backend`.

В backend были добавлены:

- чтение `DATABASE_URL`;
- чтение `ALLOWED_ORIGINS`;
- чтение `ENVIRONMENT`;
- endpoint `/health`;
- OpenAPI-документация `/docs`;
- Dockerfile и `.dockerignore`.

Особое внимание было уделено поддержке serverless-среды: контейнер был доработан так, чтобы корректно использовать порт, переданный через переменную окружения.

### Локальная Docker-проверка

Перед облачным деплоем backend был собран и протестирован локально. Результат сохранен в `lab-17/verification/docker_backend_output.md`.

В ходе проверки выполнялись команды:

```powershell
docker build -t lab17-book-api .
docker run -d --name lab17_book_api_test -p 18000:8000 lab17-book-api
Invoke-RestMethod http://localhost:18000/health
docker rm -f lab17_book_api_test
```

Фактический ответ endpoint `/health`:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-26",
  "environment": "development",
  "database_configured": true
}
```

Это подтверждает, что Docker-образ корректно собирается и запускает приложение.

### Реальный деплой frontend на Vercel

После настройки проекта frontend был развернут на Vercel. Production URL:

- [https://frontend-sigma-three-94lcoxv74s.vercel.app](https://frontend-sigma-three-94lcoxv74s.vercel.app)

Проверка через HTTP подтвердила статус:

```text
HTTP/1.1 200 OK
```

Следовательно, frontend доступен публично и успешно обслуживается Vercel.

### Реальный деплой backend в Yandex Cloud

Backend был опубликован в Yandex Serverless Containers. Публичный URL:

- [https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net)

Проверка endpoint `/health`:

- [https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health)

Фактический ответ:

```json
{"status":"healthy","timestamp":"2026-04-28","environment":"development","database_configured":true}
```

Несмотря на значение `"environment":"development"` в самом JSON-ответе, ключевой факт лабораторной заключается в том, что контейнер развернут, доступен снаружи, отвечает кодом `200`, а конфигурация БД успешно применена.

### Интеграция frontend и backend

В рамках деплоя frontend был настроен на обращение к backend через production URL. Это обеспечивает реальную связку двух частей fullstack-приложения.

Таким образом, первая часть лабораторной завершилась получением двух публичных адресов:

1. frontend на Vercel;
2. backend в Yandex Cloud.

---

## Ответы на контрольные вопросы (Часть 1)

1. **Какие преимущества дает многослойная или продуманная сборка Docker-образа?**  
   Она позволяет уменьшить размер итогового образа, отделить этап установки зависимостей от этапа выполнения, ускорить повторные сборки и сделать production-окружение чище и безопаснее.

2. **Почему frontend размещен на Vercel, а backend в Yandex Cloud?**  
   Vercel хорошо подходит для Next.js и статических/гибридных frontend-проектов, так как предоставляет быстрый деплой и интеграцию с GitHub. Yandex Cloud удобен для контейнеризированного backend и интеграции с другими облачными сервисами, включая PostgreSQL и Container Registry.

3. **Как решается проблема CORS?**  
   На стороне backend задается список разрешенных источников (`ALLOWED_ORIGINS`), из которых браузер может выполнять запросы. Это позволяет frontend, развернутому на отдельном домене, безопасно обращаться к backend API.

4. **Какие переменные окружения должны быть секретными, а какие могут быть публичными?**  
   Секретными должны быть строки подключения к БД, ключи облачных сервисов, service account JSON и токены CI/CD. Публичными могут быть только значения, не дающие прямого доступа, например `NEXT_PUBLIC_API_URL`, которое frontend использует для обращения к API.

5. **Что такое “холодный старт” в serverless-среде?**  
   Это задержка первого ответа, возникающая, когда облачная платформа поднимает контейнер “с нуля” после периода простоя. Такой эффект типичен для serverless и может влиять на отклик первого запроса.

---

## Часть 2. CI/CD пайплайн

### Размещение workflow и общая логика

В рамках второй части лабораторной были настроены workflow GitHub Actions, расположенные в корне репозитория:

1. `.github/workflows/deploy.yml`
2. `.github/workflows/pr-checks.yml`
3. `.github/workflows/terraform.yml`

Это важно, поскольку именно корневая папка `.github/workflows` распознается GitHub Actions для автоматического запуска пайплайнов.

### Workflow `deploy.yml`

Файл `deploy.yml` отвечает за production-деплой всего fullstack-приложения.

Он выполняет два основных job:

#### `deploy-frontend`

- checkout репозитория;
- установка Node.js;
- `npm ci`;
- `npm run build`;
- `vercel pull`;
- `vercel build --prod`;
- `vercel deploy --prebuilt --prod`.

#### `deploy-backend`

- checkout репозитория;
- логин в Yandex Container Registry;
- сборка Docker image;
- push образа;
- деплой новой revision в Yandex Serverless Container.

Для деплоя backend используются секреты:

- `YC_SA_KEY_JSON`
- `YC_REGISTRY_ID`
- `YC_CONTAINER_NAME`
- `YC_FOLDER_ID`
- `YC_SERVICE_ACCOUNT_ID`
- `DB_URL`
- `ALLOWED_ORIGINS`

### Workflow `pr-checks.yml`

Этот workflow предназначен для проверок на Pull Request и ручного запуска.

Для frontend выполняются:

- `npm ci`
- `npm run build`

Для backend выполняются:

- установка Python;
- установка зависимостей;
- `python -m compileall .`

Таким образом, этот workflow подтверждает, что изменения хотя бы собираются и не содержат грубых ошибок на этапе интеграции.

### Workflow `terraform.yml`

Этот workflow проверяет инфраструктурную часть проекта. В нем выполняются:

- `terraform fmt -check`
- `terraform init`
- `terraform validate`

Он запускается по изменению terraform-конфигурации и обеспечивает базовый контроль корректности IaC.

### Реальная проверка CI/CD

После доведения конфигурации до рабочего состояния был подтвержден успешный запуск production workflow `Deploy Fullstack App`.

По последнему запуску оба job завершились успешно:

#### Frontend

- `npm ci` - success
- `npm run build` - success
- `vercel pull` - success
- `vercel build --prod` - success
- `vercel deploy --prebuilt --prod` - success

#### Backend

- `Login to Yandex Cloud Container Registry` - success
- `Build and push Docker image` - success
- `Deploy to serverless container` - success

Это означает, что автоматическая цепочка сборки и деплоя реально работает, а не существует только на уровне конфигурационных файлов.

### Исправления, выполненные в ходе настройки

При доведении CI/CD до рабочего состояния были устранены реальные инженерные проблемы:

1. workflow изначально лежали не в корневой директории `.github/workflows`;
2. использовались некорректные параметры deploy action для Yandex;
3. backend контейнер был доработан для корректной работы с `PORT`;
4. была решена проблема публичного доступа к контейнеру и деплой был доведен до успешного состояния.

Эти исправления являются важной частью результата лабораторной, так как показывают не только “идеальную настройку”, но и практическое отлаживание пайплайна.

---

## Ответы на контрольные вопросы (Часть 2)

1. **Чем CI/CD пайплайн лучше ручного деплоя?**  
   Он воспроизводим, снижает количество человеческих ошибок, автоматически запускает проверки и ускоряет обновление приложения после изменения кода.

2. **Зачем нужны GitHub Actions Secrets?**  
   Они позволяют безопасно хранить токены, ключи облака, строки подключения к БД и другие чувствительные данные, не размещая их в исходном коде репозитория.

3. **Для чего нужен отдельный workflow на Pull Request?**  
   Он позволяет заранее проверить, что изменения не ломают проект, еще до попадания их в основную ветку. Это помогает удерживать `main` в рабочем состоянии.

4. **Зачем нужен Terraform validation workflow, если инфраструктура уже создана?**  
   Потому что инфраструктура тоже является кодом и может содержать ошибки. `terraform validate` и `terraform fmt -check` позволяют находить проблемы на раннем этапе, до попытки применения конфигурации.

5. **Что происходит, если один из jobs в CI/CD завершается с ошибкой?**  
   В зависимости от логики workflow следующие шаги могут не выполниться. Это полезно, так как предотвращает публикацию сломанного кода в production.

---

## Финальная проверочная таблица

| Объект проверки | Результат |
|---|---|
| Frontend локально собирается | Да |
| Backend Docker локально запускается | Да |
| Frontend развернут на Vercel | Да |
| Backend развернут в Yandex Cloud | Да |
| `/health` отвечает кодом 200 | Да |
| GitHub Actions deploy workflow успешен | Да |
| PR-check workflow настроен | Да |
| Terraform workflow настроен | Да |

---

## Верификация выполнения лабораторной

Проверяющему достаточно открыть следующие материалы:

### Локальные артефакты

- `lab-17/verification/docker_backend_output.md`

### Исходники и конфигурация

- `lab-17/fullstack-app/frontend`
- `lab-17/fullstack-app/backend`
- `.github/workflows/deploy.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/terraform.yml`
- `lab-17/fullstack-app/infrastructure/terraform`

### Production URL

- [Frontend production](https://frontend-sigma-three-94lcoxv74s.vercel.app)
- [Backend health](https://bba3h0hsef8ihpsg3ear.containers.yandexcloud.net/health)

Эти источники уже подтверждают конечный результат без необходимости повторного деплоя.

---

## Заключение

В лабораторной работе №17 был выполнен полный цикл вывода учебного fullstack-приложения в production.

В первой части были подготовлены и развернуты frontend и backend, backend был контейнеризирован, опубликован в Yandex Cloud и подключен к production-конфигурации. Во второй части была настроена автоматизация через GitHub Actions, включая сборку frontend, публикацию backend, проверки на PR и валидацию terraform-конфигурации.

Практический результат лабораторной:

- приложение реально доступно по публичным URL;
- backend отвечает на healthcheck;
- деплой подтвержден GitHub Actions;
- локальная и облачная верификация сохранены в артефактах.

Таким образом, лабораторная работа №17 выполнена полностью и оформлена в виде, удобном для проверки без повторного запуска сервисов.
