# mlops

## Установка окружения

Создание виртуального окружения:

```bash
python -m venv venv
```

Активация окружения:

- На Mac/Linux: `source ./venv/bin/activate`
- На Windows: `bash ./venv/Scripts/activate`

Установка зависимостей и pre-commit hooks:

```bash
make requirements
```

## Команды

Запуск линтера: `make lint`

Проверка типов: `make typecheck`
