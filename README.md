# FarPostBooks - Telegram
Телеграм бот для корпоративной библиотеки FarPost, написанный с использованием
асинхронного фреймворка aiogram.

## Запуск
Бот объединён в общий volume и network с основным [REST API](https://github.com/FarPostBooks/farpostbooks_backend),
поэтому перед запуском требуется поднять [основную платформу](https://github.com/FarPostBooks/farpostbooks_backend).

Запуск проекта, используя Docker:
```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```


## Конфигурация
Все переменные окружения должны начинаться с префикса `FARPOSTBOOKS_TELEGRAM_`.

Настройки переменных окружения находятся в `farpostbooks_telegram.settings.Settings`.


## Структура проекта
```bash
$ tree "farpostbooks_telegram"
farpostbooks_telegram
├── filters  # Фильтры для хендлеров
│   └── guest.py  # Основной фильтр для проверки регистрации пользователя
├── handlers  # Хендлеры для обработки апдейтов от телеграма
│   ├── guest  # Хендлеры для несуществующих пользователей
│   └── user  # Хендлеры для существующих пользователей
├── keyboards
│   └── reply.py  # Reply клавиатуры
├── misc  # Дополнительные возможности
│   └── states.py  # Машина состояний (FSM)
├── models  # Модели и конфигурация для Базы Данных
│   └── config.py  # Конфигурация Базы Данных
├── __main__.py  # Запуск бота в поллинге и его конфигурация.
└── settings.py  # Основные параметры конфигурации проекта.
```

