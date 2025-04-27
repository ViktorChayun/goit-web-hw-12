cd %pyenv%  
python -m venv %pyenv%\home_work_12
%pyenv%\home_work_12\Scripts\activate.bat
%pyenv%\home_work_12\Scripts\deactivate.bat
pip install poetry

1. ініціалізація поетрі проекту в існуючій папці
```cmd
cd %github%\goit-web-hw-12
poetry init
```
2. install  packages
```cmd
poetry add fastapi
poetry add uvicorn[standard]
poetry add sqlalchemy
poetry add psycopg2
poetry add alembic
poetry add pydantic[email]
poetry add python-jose[cryptography]
poetry add passlib
poetry add python-multipart
poetry add bcrypt
poetry add pycryptodome
```

3. create docker container with postgress
```cmd
docker run --name postgres-goit-hw11 -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
```

4. ініціалізація створення оточення alembic
```cmd
    cd <root fodler of project>
    cd C:\GitHub\pytraining-1\2 - Web\Module 11 - FastAPI + REST API\home-work
    alembic init migrations
```

5. створеюємо міграційний скрпит для створення схеми БД
```cmd
alembic revision --autogenerate -m 'Init'
```

6. накатуємо цей міграційни скорпит в саму БД
```cmd
alembic upgrade head
```

7. run api server
```cmd
uvicorn main:app --host localhost --port 8000 --reload
```
