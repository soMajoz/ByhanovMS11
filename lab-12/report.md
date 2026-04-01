# Отчет по лабораторной работе №12
# Часть 1: Нативная Android-разработка с Jetpack Compose

**Семестр:** 2 курс 2 полугодие (4 семестр)  
**Дисциплина:** Технологии программирования  
**Студент:** Быханов Михаил Сергеевич  

---

## Цель работы

Получить практические навыки создания нативного Android-приложения на Kotlin с использованием современного декларативного подхода Jetpack Compose, архитектурных компонентов Jetpack (ViewModel, StateFlow) и локальной базы данных Room.

---

## Теоретическая часть

### Изученные концепции

#### 1. **Jetpack Compose**
- Современный декларативный UI-фреймворк для Android.
- Позволяет описывать интерфейс функциями-компонентами (`@Composable`), которые автоматически перерисовываются при изменении состояния (State).
- Вместо разметки XML, код пользовательского интерфейса создается в Kotlin, что объединяет логику и внешний вид.

#### 2. **Архитектура MVVM и ViewModel**
- **Model-View-ViewModel (MVVM)** — шаблон проектирования, разделяющий бизнес-логику и данные от пользовательского интерфейса.
- `ViewModel` сохраняет UI-состояние и выживает при конфигурационных изменениях (например, поворот экрана).
- Для передачи состояния от `ViewModel` к `View` (Compose) используются реактивные компоненты — `StateFlow` из корутин.

#### 3. **База данных Room**
- Абстракция над SQLite-базой данных в Android.
- Состоит из сущностей (`@Entity`), объектов доступа к данным (`@Dao`), и базы данных (`@Database`).
- Метод запросов DAO поддерживает корутины (`suspend` функции для разовых действий и `Flow` для постоянного отслеживания изменений данных).

---

## Практическая часть

### Структура проекта

```
NotesApp/
├── app/
│   ├── src/main/java/com/example/notesapp/
│   │   ├── data/
│   │   │   ├── Note.kt                 # Модель (Entity)
│   │   │   ├── NoteDao.kt              # Интерфейс работы с БД
│   │   │   ├── NoteDatabase.kt         # Класс базы данных
│   │   │   └── NoteRepository.kt       # Репозиторий
│   │   ├── ui/
│   │   │   ├── AddEditNoteScreen.kt    # Экран создания/редактирования (Compose)
│   │   │   ├── NotesScreen.kt          # Главный экран списка (Compose)
│   │   │   ├── NotesViewModel.kt       # Логика и состояние (ViewModel)
│   │   │   └── NotesViewModelFactory.kt# Фабрика ViewModel
│   │   ├── ui/theme/
│   │   │   └── Theme.kt                # Базовая тема
│   │   └── MainActivity.kt             # Navigation Host, старт приложения
```

### Выполненные задачи

- [x] **Настройка проекта:** Инициализация файлов ViewModel, Repository, Room Database и Jetpack Compose UI.
- [x] **Удаление заметок (DAO):** Реализация `@Delete suspend fun deleteNote(note: Note)` в `NoteDao`.
- [x] **Удаление заметок (Repository, ViewModel):** Добавление методов проброса запроса удаления к DAO и вызов их из `viewModelScope.launch`.
- [x] **Удаление заметок (UI):** Иконка на `NoteItem`, вызов лямбды `onDeleteClick`.
- [x] **Добавление метки времени (createdAt):** Реализовано добавление `Long` timestamp в сущность `Note.kt`, генерация времени `System.currentTimeMillis()` в `NotesViewModel.kt`, и его отображение в карточке заметки (`NotesScreen.kt`) с помощью SimpleDateFormat.
- [x] **Обработка редактирования:** Обработка навигационного маршрута `add_edit_note/{noteId}` с извлечением аргументов в `MainActivity`, метод `updateNote()` и подзагрузка данных в `NotesViewModel`.

---

## Ключевые фрагменты кода

### 1. Добавление поля Timestamp в Note

**`Note.kt`**:
```kotlin
@Entity(tableName = "notes")
data class Note(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val content: String,
    val createdAt: Long = System.currentTimeMillis() // Реализовано требование
)
```

### 2. Поддержка удаления

**`NoteDao.kt`**:
```kotlin
@Delete
suspend fun deleteNote(note: Note)
```
**`NotesViewModel.kt`**:
```kotlin
fun deleteNote(note: Note) {
    viewModelScope.launch {
        repository.deleteNote(note)
    }
}
```

### 3. Редактирование заметок

**`NotesViewModel.kt`**:
```kotlin
fun updateNote(id: Int, title: String, content: String) {
    viewModelScope.launch {
        val noteToUpdate = repository.getNoteById(id)
        if (noteToUpdate != null) {
            val updatedNote = noteToUpdate.copy(title = title, content = content)
            repository.updateNote(updatedNote)
        }
    }
}

fun loadNoteById(id: Int) {
    viewModelScope.launch {
        val note = repository.getNoteById(id)
        _currentNote.value = note
    }
}
```

**`MainActivity.kt` (фрагмент навигации)**:
```kotlin
composable("add_edit_note/{noteId}") { backStackEntry ->
    val noteId = backStackEntry.arguments?.getString("noteId")?.toInt() ?: 0
    LaunchedEffect(noteId) {
        viewModel.loadNoteById(noteId)
    }
    val currentNote by viewModel.currentNote.collectAsState()
    
    if (currentNote != null && currentNote?.id == noteId) {
        AddEditNoteScreen(
            initialTitle = currentNote!!.title,
            initialContent = currentNote!!.content,
            onSaveClick = { title, content ->
                viewModel.updateNote(noteId, title, content)
            },
            onNavigateBack = { navController.popBackStack() }
        )
    }
}
```

---

## Ответы на контрольные вопросы

#### 1. В чем преимущество использования Flow и StateFlow перед обычными списками?
**Ответ:** Flow является реактивным потоком данных. Подписавшись на него (`collectAsState()` в Jetpack Compose), пользовательский интерфейс автоматически узнаёт об изменениях. Ему не нужно дополнительно поллить (запрашивать) БД или вызывать принудительно методы перерисовки UI — если в базе Room обновилась строчка, запрос, возвращающий `Flow`, излучает новую обновленную коллекцию, и StateFlow реактивно перерисовывает все `@Composable` функции, которые от него зависят.

#### 2. Почему ViewModel не уничтожается при повороте экрана и как это влияет на UX?
**Ответ:** Жизненный цикл ViewModel управляется классом `ViewModelStoreOwner` (как правило, Activity или фрагментом), но ViewModelStore выживает во время конфигурационных изменений среды (изменение ориентации, темы, локали). Это улучшает UX: пользователь не теряет набранный, но не сохраненный текст (если он хранится во ViewModel), и не видит моргания / повторной загрузки данных с диска или сети при простом повороте телефона.

#### 3. Какие преимущества дает использование Room по сравнению с прямым использованием SQLite?
**Ответ:** 
- Огромное сокращение шаблонного (многословного) кода — не нужно строить курсоры и прописывать сырые SQL-запросы для простейших операций (есть аннотации `@Insert`, `@Update`).
- Безопасность на этапе компиляции — Room заранее проверяет валидность написанных запросов (`@Query`) и сразу выкидает ошибку компиляции, если запрос неверен, оберегая от падений приложения в рантайме.
- Поддержка корутин из коробки: можно просто сделать `suspend fun` или вернуть `Flow<List<T>>` и функция сама корректно асинхронно уйдет в выполнение вне UI-потока.

---

# Часть 2: Кроссплатформенная разработка на React Native

## Теоретическая часть

React Native — это фреймворк для создания мобильных приложений с использованием JavaScript и React. В отличие от гибридных приложений, React Native рендерит реальные нативные компоненты.

### Ключевые технологии:
1.  **Redux Toolkit**: Современный подход к управлению состоянием, упрощающий работу с Redux (reducers, actions, thunks).
2.  **SQLite (expo-sqlite)**: Локальное хранилище для структурированных данных.
3.  **Expo SDK**: Набор инструментов и библиотек, предоставляющих доступ к нативным функциям устройства (камера, геолокация) через единый API.

## Практическая часть

Реализовано приложение **GeoNotes** для создания заметок с привязкой к местоположению и фотографией.

### Выполненные задачи:
- [x] **Инициализация БД:** Создание таблицы `notes` при запуске приложения.
- [x] **CRUD операции:** Реализация методов `fetchNotes`, `addNote`, `deleteNote` в `database.ts`.
- [x] **Redux Slice:** Создание `notesSlice` с асинхронными `createAsyncThunk` для работы с БД.
- [x] **Геолокация и Камера:** Использование `expo-location` для получения адреса и `expo-image-picker` для снимков.

### Ключевой код (Redux Thunk):
```typescript
export const saveNote = createAsyncThunk(
    'notes/saveNote',
    async (note: GeoNote) => {
        await database.addNote(note);
        return note;
    }
);
```

## Ответы на контрольные вопросы

1. **В чем разница между "мостиком" (Bridge) и новой архитектурой (JSI) в React Native?**
   *Ответ:* Мостик использует асинхронную передачу JSON-сообщений между JS и нативным потоком. JSI (JavaScript Interface) позволяет JS-потоку напрямую вызывать нативные методы, что значительно ускоряет работу.

2. **Зачем нужен Redux Toolkit, если есть обычный Redux?**
   *Ответ:* RTK сокращает количество "шаблонного" кода (boilerplate), включает в себя полезные утилиты (напр. Immer для мутаций) и стандартные настройки стора.

---

# Часть 3: Кроссплатформенная разработка на Flutter

## Теоретическая часть

Flutter — это UI-фреймворк от Google, использующий язык Dart и собственный движок отрисовки (Skia/Impeller), что обеспечивает высокую производительность и идентичный вид на всех платформах.

### Ключевые концепции:
1.  **Provider**: Легковесное управление состоянием на основе `InheritedWidget`.
2.  **Sensors**: Доступ к акселерометру и шагомеру для отслеживания активности.
3.  **SQLite (sqflite)**: Плагин для работы с локальной базой данных.

## Практическая часть

Реализовано приложение **Activity Tracker** для отслеживания физической активности.

### Выполненные задачи:
- [x] **Модель данных:** Реализация `ActivityRecord` с методами `toMap` и `fromMap`.
- [x] **Provider:** Создание `ActivityProvider` для управления списком тренировок и `SensorProvider` для данных с сенсоров.
- [x] **Сенсоры:** Интеграция `accelerometerEvents` для подсчета шагов в реальном времени.

### Ключевой код (Расчет шагов):
```dart
_accelSub = accelerometerEvents.listen((AccelerometerEvent event) {
  _accelerometerMagnitude = sqrt(event.x*event.x + event.y*event.y + event.z*event.z);
  if (_accelerometerMagnitude > 12.0) _stepCount++; // Простой алгоритм детекции шага
});
```

## Ответы на контрольные вопросы

1. **Что такое Hot Reload во Flutter и как он работает?**
   *Ответ:* Hot Reload вставляет обновленный исходный код в работающую VM Dart, сохраняя текущее состояние приложения, что позволяет видеть изменения мгновенно.

2. **В чем различие между StatelessWidget и StatefulWidget?**
   *Ответ:* Stateless не меняет свое состояние после создания. Stateful имеет связанный объект `State`, который может вызывать `setState()` для перерисовки виджета.

---

# Часть 4: Kotlin Multiplatform Mobile (KMM)

## Теоретическая часть

KMM позволяет использовать один и тот же код на Kotlin для бизнес-логики Android и iOS приложений, оставляя интерфейс полностью нативным.

### Ключевые механизмы:
1.  **Expect/Actual**: Механизм для вызова платформенно-зависимого кода из общего модуля.
2.  **SQLDelight**: Библиотека для генерации типобезопасного Kotlin-кода из SQL-запросов.

## Практическая часть

Реализована общая логика для приложения **Expense Tracker**.

### Выполненные задачи:
- [x] **Shared Logic:** Создание моделей `Expense`, `Category`, `Budget` в `commonMain`.
- [x] **Database Driver:** Реализация `expect class DatabaseDriverFactory` и её `actual` версий для Android и iOS.
- [x] **ViewModel:** Реализация `ExpensesViewModel` на чистом Kotlin с использованием Coroutines и StateFlow.

### Ключевой код (Expect/Actual):
```kotlin
// commonMain
expect class DatabaseDriverFactory {
    fun createDriver(): SqlDriver
}

// androidMain
actual class DatabaseDriverFactory(private val context: Context) {
    actual fun createDriver(): SqlDriver = AndroidSqliteDriver(ExpenseDatabase.Schema, context, "expense.db")
}
```

## Ответы на контрольные вопросы

1. **Чем KMM отличается от Flutter или React Native?**
   *Ответ:* KMM не навязывает UI-фреймворк. Вы разделяете только логику данных и расчетов, а интерфейс пишете на нативных Compose/SwiftUI.

2. **Зачем нужен SQLDelight в KMM?**
   *Ответ:* Он генерирует Kotlin-интерфейсы из SQL, обеспечивая проверку запросов на этапе компиляции для всех платформ одновременно.

---

# Часть 5: Progressive Web App (PWA)

## Теоретическая часть

PWA — это технология, превращающая веб-сайт в приложение, которое можно установить на смартфон, и которое работает офлайн.

### Компоненты:
1.  **Service Worker**: Прокси-сервер в браузере, кэширующий ресурсы и обрабатывающий сетевые запросы.
2.  **Manifest.json**: Описание приложения (иконки, ориентация, полноэкранный режим).
3.  **IndexedDB**: Клиентская БД для хранения больших объемов данных.

## Практическая часть

Реализован **News Aggregator** с поддержкой офлайн-режима.

### Выполненные задачи:
- [x] **Service Worker:** Кэширование статических ресурсов и перехват `fetch`.
- [x] **Offline Storage:** Сохранение статей в IndexedDB при успешном запросе к API.
- [x] **Sync:** Автоматическое переключение на локальные данные при отсутствии сети.

### Ключевой код (Service Worker Fetch):
```javascript
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(response => {
      return response || fetch(e.request); // Сначала кэш, потом сеть
    })
  );
});
```

## Ответы на контрольные вопросы

1. **В чем главное ограничение PWA по сравнению с нативными приложениями?**
   *Ответ:* Ограниченный доступ к некоторым сенсорам, отсутствие глубокой интеграции с системными API (напр. Bluetooth или NFC в некоторых браузерах), зависимость от возможностей браузерного движка.

2. **Для чего нужен жизненный цикл 'install' у Service Worker?**
   *Ответ:* Для предварительного кэширования критически важных ресурсов приложения (App Shell), необходимых для запуска в офлайн-режиме.

---

## Заключение

В рамках лабораторной работы №12 были изучены и применены на практике пять современных подходов к разработке мобильных и веб-приложений. Каждая технология имеет свои преимущества: нативная разработка дает максимальную производительность, React Native и Flutter ускоряют выпуск кроссплатформенных продуктов, KMM позволяет элегантно разделять бизнес-логику, а PWA делает веб-контент доступным без необходимости установки через магазины приложений.
