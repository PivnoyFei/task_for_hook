<h1 align="center">task_for_hook</h1>
<p align="center">Тестовое задание для компании "ХУК"</p>


### Стек:
![Python](https://img.shields.io/badge/Python-171515?style=flat-square&logo=Python)![3.12](https://img.shields.io/badge/3.12-blue?style=flat-square&logo=3.12)
![FastAPI](https://img.shields.io/badge/FastAPI-171515?style=flat-square&logo=FastAPI)![0.100](https://img.shields.io/badge/0.100-blue?style=flat-square&logo=0.100)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-171515?style=flat-square&logo=PostgreSQL)![13.0](https://img.shields.io/badge/13.0-blue?style=flat-square&logo=13.0)

![Pydantic](https://img.shields.io/badge/Pydantic-171515?style=flat-square&logo=Pydantic)![2.1.1](https://img.shields.io/badge/2.1.1-blue?style=flat-square&logo=2.1.1)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-171515?style=flat-square&logo=SQLAlchemy)![2](https://img.shields.io/badge/2-blue?style=flat-square&logo=2)

![Alembic](https://img.shields.io/badge/Alembic-171515?style=flat-square&logo=Alembic)
![Docker-compose](https://img.shields.io/badge/Docker--compose-171515?style=flat-square&logo=Docker)

### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/task_for_hook.git
cd task_for_hook
```

### Перед запуском сервера, в папке hook-docker необходимо создать `.env` на основе `.env.template` файл со своими данными.
#### Переходим в папку с файлом docker-compose.yaml:
```bash
cd hook-docker
```

### Запуск проекта
```bash
docker-compose up -d --build
```

#### Миграции базы данных:
```bash
# docker-compose exec hook-backend alembic revision --message="Initial" --autogenerate
docker-compose exec hook-backend alembic upgrade head
```

#### Проект доступен по:
```bash
http://localhost:9993
```

#### Останавливаем контейнеры:
```bash
docker-compose down -v
```

#### Автор
[Смелов Илья](https://github.com/PivnoyFei)

