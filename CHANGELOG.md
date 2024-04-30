# CHANGELOG

## [1.33.0] - 2024-04-29
- При поиске значения слова добавляются нормальные формы всех значений этого слова

## [1.32.2] - 2024-04-14
- При изменении текста через TipTap обновляется updated_at у текста и проекта

## [1.31.1] - 2024-04-14
- Удаление текстов из TipTap

## [1.30.0] - 2024-04-14
- Убран resample из определения bpm
- CI/CD дополнен тестами

## [1.29.1] - 2024-04-13
- Лимит custom_bpm установлен в 999

## [1.29.0] - 2024-04-13
- Исправлена настройка линтеров, исправлены недочеты в файлах

## [1.28.0] - 2024-04-13
- Тесты TipTap, включены в pre-commit

## [1.27.0] - 2024-04-12
- Тесты музыки, фикс прав на ручки музыки

## [1.26.0] - 2024-04-08
- Тесты грантов, get_user, healthcheck. Фикс leave_project.

## [1.25.0] - 2024-04-07
- Mongodb

## [1.24.0] - 2024-04-07
- Удален endpoint TipTap, который выдавал токен на все тексты
- Ускорен вход через Яндекс
- Добавлены интеграционные тесты (получение токена по почте+коду, автодополнение)

## [1.23.0] - 2024-03-27
- Ручка leave_project для самобана

## [1.22.0] - 2024-03-27
- grant_level добавлен к проекту

## [1.21.2] - 2024-03-27
- Фикс delete_project по части удаления не владельцем

## [1.21.1] - 2024-03-27
- Фикс revoke_project_access по части 500

## [1.21.0] - 2024-03-27
- revoke_project_access теперь возвращает ProjectGrant вместо null

## [1.20.3] - 2024-03-27
- При разбане выбор последнего, а не случайного кода активации

## [1.20.2] - 2024-03-27
- Фикс разбана

## [1.20.1] - 2024-03-27
- update_project_access разблокирует доступ пользователя

## [1.20.0] - 2024-03-27
- В ProjectGrant добавлено поле grant_code_id

## [1.19.0] - 2024-03-27
- В ProjectGrant добавлено поле is_active

## [1.18.3] - 2024-03-26
- Фикс 500 (user_id uuid pydantic)

## [1.18.2] - 2024-03-26
- Фикс 500 (user_id uuid pydantic)

## [1.18.1] - 2024-03-25
- Фикс 500 (user_id uuid pydantic)

## [1.18.0] - 2024-03-25
- get_user: Получить информацию о пользователе

## [1.17.0] - 2024-03-25
- В JWT добавлен user_id

## [1.16.0] - 2024-03-25
- В схему проекта добавлено поле bool is_owner

## [1.15.4] - 2024-03-25
- Фикс: аутентификация через яндекс

## [1.15.3] - 2024-03-25
- Фикс: аутентификация через яндекс

## [1.15.2] - 2024-03-25
- Фикс: аутентификация через яндекс

## [1.15.1] - 2024-03-25
- Фикс: аутентификация через яндекс

## [1.15.0] - 2024-03-25
- Добавлен атрибут owner_user_id в ProjectOut

## [1.14.3] - 2024-03-24
- В create_completion, когда completion_input.text="", не производится обращение в openai. Возвращается [].

## [1.14.2] - 2024-03-24
- Исправлен промпт автокомплита. Новый промпт: "Продолжи текст песни. Добавь перенос строки, если не продолжаешь текущую строку, а начинаешь новую. В ответ пришли текст, который нужно добавить. учитывай регистр, старайся рифмовать."

## [1.14.1] - 2024-03-24
- Удаление проектов (каскадное удаление всех грантов, кодов, текстов, музыки)

## [1.14.0] - 2024-03-24
- Ручка изменения уровня доступа пользователя (READ_WRITE -> READ_ONLY, READ_ONLY -> READ_WRITE)

## [1.13.1] - 2024-03-24
- При активации нового кода по проекту где уже есть права происходит перезапись

## [1.13.0] - 2024-03-24
- Ручка деактивации кода доступа (блок новых подключений)

## [1.12.0] - 2024-03-24
- Ручка для получения списка кодов доступа к проекту

## [1.11.0] - 2024-03-24
- Ручка /tiptap/token/{text_id}, которая учитывает наличие прав у пользователя на проект и выдает токен с READ_ONLY / READ_WRITE доступом
- Старая ручка помечена deprecated и будет вскоре удалена

## [1.10.9] - 2024-03-24
- Отзыв доступа (с точки зрения API, все еще не TipTap)

## [1.10.8] - 2024-03-24
- Запрет повторной активации кода тем же пользователем
- Запрет активации кода владельцем проекта

## [1.10.7] - 2024-03-24
- Запрет изменения чужого проекта
- Запрет получения информации о проекте, к которому нет доступа

## [1.10.6] - 2024-03-24
- Запрет выдачи кода доступа к чужому проекту
- Запрет получения списка пользователей с доступом к проекту для чужих проектов
- Запрет отзыва прав на проект для чужих проектов

## [1.10.5] - 2024-03-24
- Ручка отзыва доступа, удален грант типа owner (нельзя выдать права владельца, только read_write или read_only)

## [1.9.2] - 2024-03-23
- Выставлен operation_id для списка пользователей с доступом к проекту

## [1.9.1] - 2024-03-23
- Исправлена работа с бд, приводящая к ошибкам 500

## [1.9.0] - 2024-03-23
- Ручка для получения списка пользователей с доступом к проекту

## [1.8.0] - 2024-03-17
- Эндпоинты /grants/* для создания кода доступа к проекту и его активации

## [1.7.0] - 2024-03-17
- GET /projects/ выдает только те проекты, что пользователь создал через POST /projects/

## [1.6.0] - 2024-03-17
- Мок поиска рифм заменен на обращение к gpt3,5

## [1.5.0] - 2024-03-17
- Liveness и readyness пробы, включен rollingUpdate

## [1.4.0] - 2024-03-16
- Дата создания и последнего изменения текста (created_at, updated_at)

## [1.3.0] - 2024-03-16
- Дата последнего изменения проекта (updated_at)

## [1.2.0] - 2024-03-16
- Дата создания проекта (created_at)

## [1.1.5] - 2024-03-16
- Миграции бд в CI/CD

## [1.1.4] - 2024-03-16
- Обновление версий зависимостей github actions

## [1.1.3] - 2024-03-16
- Разделен build и deploy

## [1.1.2] - 2024-03-16
- Автоматическое создание первого варианта текста вместе с созданием проекта

## [1.1.1] - 2024-03-16
- Запрет удаления единственного текста из проекта

## [1.1.0] - 2024-03-16
- Дополнение с помощью gpt3,5-turbo от openai

## [1.0.4] - 2024-03-15
- Автоматический редеплой подов бэкенда

## [1.0.3] - 2024-03-15
- Отображение списка текстов при удалении музыки из проекта

## [1.0.0] - 2024-03-09
- mongodb теперь хранит варианты текста в виде произвольного JSON
- Деплой бэкенда по пушу в main ветку
- CORS настройки для бакета с музыкой (разрешение доступа с http://localhost:5173)

- Релиз без простоя, поддержка 2 реплик API

## [0.5.0] - 2024-01-28
- Получение синонимов слова через [API Яндекс.Словарь](https://api.yandex.ru/dictionary)

## [0.4.0] - 2024-01-27
- Определение значения слова по словарю Ожегова
- [WIP] Нормализация слов

## [0.3.0] - 2024-01-27
- Определение длительности трека

## [0.2.2] - 2024-01-27
- Определение bpm стало быстрее и точнее

## [0.2.0] - 2024-01-27
- bpm теперь может быть null
- Ручка загрузки музыки из-за анализа bpm стала медленнее

## [0.1.0] - 2024-01-26
- Загрузка музыки
- Получение музыки
- Удаление музыки
- Музыка отдается через presigned url на 3600 секунд

## [Неопределённая версия] - 2024-01-21 до 2024-01-22
- Аутентификация по почте
- CRUD проектов теперь сохраняет данные в базе данных (исключая музыку и тексты)
- Токен теперь живет 30 дней
- Добавлена загрузка музыки в проект
- Реализовано получение музыки проекта
- Установка пользовательского BPM
- Удаление музыки из проекта
- Создание / изменение / удаление вариантов текста

## [1.0.2] - 2024-03-14
- Ручка изменения проекта: PATCH projects/<uuid>

## [1.0.1] - 2024-03-14
- Ручка получения TipTap JWT: /tiptap/token

## [1.0.0] - 2024-03-09
- mongodb теперь хранит варианты текста в виде произвольного JSON
- Деплой бэкенда по пушу в main ветку
- CORS настройки для бакета с музыкой (разрешение доступа с http://localhost:5173)

- Релиз без простоя, поддержка 2 реплик API

## [0.5.0] - 2024-01-28
- Получение синонимов слова через [API Яндекс.Словарь](https://api.yandex.ru/dictionary)

## [0.4.0] - 2024-01-27
- Определение значения слова по словарю Ожегова
- [WIP] Нормализация слов

## [0.3.0] - 2024-01-27
- Определение длительности трека

## [0.2.2] - 2024-01-27
- Определение bpm стало быстрее и точнее

## [0.2.0] - 2024-01-27
- bpm теперь может быть null
- Ручка загрузки музыки из-за анализа bpm стала медленнее

## [0.1.0] - 2024-01-26
- Загрузка музыки
- Получение музыки
- Удаление музыки
- Музыка отдается через presigned url на 3600 секунд

## [0.0.1] - 2024-01-22
- Аутентификация по почте
- CRUD проектов теперь сохраняет данные в базе данных (исключая музыку и тексты)
- Токен теперь живет 30 дней
- Добавлена загрузка музыки в проект
- Реализовано получение музыки проекта
- Установка пользовательского BPM
- Удаление музыки из проекта
- Создание / изменение / удаление вариантов текста