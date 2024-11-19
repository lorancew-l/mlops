# mlops

## Установка окружения

### Создание виртуального окружения

```bash
python -m venv venv
```

### Активация окружения

`source ./venv/bin/activate`

### Установка зависимостей и pre-commit hooks:

```bash
make requirements
```

### Создание .env

```sh
cp ./.env.example ./.env
```

### Запуск minio

```sh
docker-compose --env-file .env up -d
```

### Загрузка датасета ("сида") в minio

```sh
make seed_s3 BUCKET=dataset OBJECT=titanic.csv
```

## Команды

Запуск линтера:

```sh
make lint
```

Проверка типов:

```sh
make typecheck
```

ETL - скрипт:

```sh
make process BUCKET=dataset IN_OBJECT=titanic.csv OUT_OBJECT=titanic_processed.csv
```

## Запуск экспериментов

Подготовка образа:

```sh
chmod +X setup_experiments.sh && ./setup_experiments.sh
```

Загрузка датасета ("сида") в s3 (если еще не сделано)

```sh
make seed_s3 BUCKET=dataset OBJECT=titanic.csv
```

Подготовка данных:

```sh
make process BUCKET=dataset IN_OBJECT=titanic.csv OUT_OBJECT=titanic_processed.csv
```

Запуск экспериментов:

```sh
make run_experiments DATASET=dataset/titanic_processed.csv CONFIG="./mlops/models/titanic_classifier/config.yaml"
```
