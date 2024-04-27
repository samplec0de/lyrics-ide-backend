<p align="center">
  <img src="lyrics-ide-backend.png" width="60%" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">LYRICS-IDE-BACKEND</h1>
</p>
<p align="center">
    <em>Веб-приложение для разработки текстов песен. Серверная часть.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/samplec0de/lyrics-ide-backend?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/samplec0de/lyrics-ide-backend?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/samplec0de/lyrics-ide-backend?style=flat&color=0080ff" alt="repo-top-language">
<p>
<p align="center">
		<em>Разработано с использованием технологий</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=flat&logo=Pydantic&logoColor=white" alt="Pydantic">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white" alt="OpenAI">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?style=flat&logo=AIOHTTP&logoColor=white" alt="AIOHTTP">
	<br>
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
	<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI">
</p>

# 📖 Содержание
- [📍 Описание](#-описание)
- [🧩 Ключевые особенности](#-ключевые-особенности)
- [🗂️ Структура репозитория](#-структура-репозитория)
- [🚀 Начало работы](#-начало-работы)
  - [⚙️ Установка](#-установка)
  - [🤖 Запуск](#-запуск)
  - [🧪 Тесты](#-тесты)
- [🎗 Лицензия](#-лицензия)
- [🔗 Сторонние зависимости](#-сторонние-зависимости)
<hr>

## 📍 Описание

Репозиторий содержит серверную часть веб-приложения (API), разработанную для платформы разработки текстов песен.

Основные функции
- Аутентификация и авторизация пользователей
- Управление проектами и текстами
- Загрузка музыкальных файлов и определение BPM (beats per minute)
- Автодополнение текстов песен с использованием искусственного интеллекта
- Определение значения слов, получение синонимов, поиск рифм

Ключевым принципом бэкенда является интеграция передовых веб-платформ 
и технологий для обеспечения высокой производительности и надежности.
В проекте используется Docker для инкапсуляции среды, что делает развертывание последовательным и эффективным.
Kubernetes используется для управления контейнерами и обеспечения масштабируемости.

Качество кода имеет первостепенное значение, оно обеспечивается с помощью различных корректировок и проверок стиля, 
с помощью библиотек указанных в `requirements.linters.txt`.
Тестирование - еще один важный аспект. Используются библиотеки для асинхронного тестирования, мокирования и составления 
отчетов о покрытии - `requirements.tests.txt`.
Благодаря тестам и статическому анализу кода обеспечивается соответствие серверной части стандартам качества.

Проект предлагает мощную платформу для творчества - написания текстов, дополненную технологической строгостью, 
что делает ее ценным инструментом для артистов, стремящихся использовать современные технологии для оптимизации своей работы.

---

## 🧩 Ключевые особенности

|    | Особенность            | Описание                                                                                                                     |
|----|------------------------|------------------------------------------------------------------------------------------------------------------------------|
| ⚙️  | **Архитектура**        | stateless модульный монолит на основе FastAPI, использует Docker для контейнеризации                                         |
| 🔩 | **Качество кода**      | Применяются линтеры6 форматтеры для проверки стиля                                                                           |
| 📄 | **Документация**       | Обширная документация в файлах и комментариях в модулях, описывающих функциональность. Swagger UI, ReDoc поставляются с API. |
| 🔌 | **Интеграции**         | Интеграция с AI-сервисом - OpenAI, библиотека мультимедиа -  aubio, технологии Яндекса (Яндекс Словарь).                     |
| 🧩 | **Модульность**        | Высокая модульность с четким разделением функциональности.                                                                   |
| 🧪 | **Тесты**              | Быстрые асинхронные модульные и интеграционные тесты в CI/CD.                                                                |
| ⚡️  | **Производительность** | Используется асинхронное программирование для повышения производительности.                                                  |
| 🛡️ | **Безопасность**       | Используется `python-jose` для обработки JWT, обеспечивая безопасную обработку данных.                                       |
| 🚀 | **Масштабируемость**   | Используется kubernetes для управления масштабированием.                                                                     |

---

## 🗂️ Структура репозитория

```sh
└── lyrics-ide-backend/
    ├── .github
    │   └── workflows
    │       └── deploy-prod.yml
    ├── CHANGELOG.md
    ├── Dockerfile
    ├── README.md
    ├── app
    │   ├── alembic
    │   │   └── versions
    │   ├── api
    │   │   ├── routers
    │   ├── main.py
    │   ├── models
    ├── docs
    ├── k8s
    ├── requirements.linters.txt
    ├── requirements.tests.txt
    ├── requirements.txt
    └── tests
        ├── integration_tests
        └── unit_tests
```

---

## 🚀 Начало работы

**Требования:**

* TODO

### ⚙️ Установка

<h4>From <code>source</code></h4>

> 1. Склонируйте репозиторий lyrics-ide-backend:
>
> ```console
> $ git clone https://github.com/samplec0de/lyrics-ide-backend
> ```
>
> 2. Перейдите в директорию проекта:
> ```console
> $ cd lyrics-ide-backend
> ```
>
> 3. Установите зависимости:
> ```console
> $ pip install -r requirements.txt
> ```
> 
>TODO

### 🤖 Запуск

<h4>From <code>source</code></h4>

> Запустите приложение:
> ```console
> $ python main.py
> ```

### 🧪 Тесты

> Запустите тесты:
> ```console
> $ pytest tests/integration_tests
> $ pytest tests/unit_tests
> ```

---

## 🎗 Лицензия

Проект защищен [SELECT-A-LICENSE](https://choosealicense.com/licenses). Подробности смотрите на [LICENSE](https://choosealicense.com/licenses/).

---

## 🔗 Сторонние зависимости

- TODO

---
