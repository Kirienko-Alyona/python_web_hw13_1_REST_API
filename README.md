# python_web_hw13_1_REST_API
poetry add python-multipart
poetry add python-jose["cryptography"]
poetry add passlib["bcrypt"]
poetry add fastapi
poetry add uvicorn[standard] 
poetry add alembic 
poetry add sqlalchemy 
poetry add psycopg2 
poetry add sphinx -G dev 
poetry add pytest-cov --dev
poetry add pytest-mock --dev
poetry add redis
poetry add cloudinary
poetry add libgravatar
poetry add fastapi-limiter
poetry add fastapi-mail

Облегчить написание строк документации может помочь плагин Trelent - AI Docstrings on Demand. 

 pip install -U sphinx

 poetry add sphinx -G dev

sphinx-quickstart docs

cd docs

docker-compose!!!
docker-compose up
docker-compose up -d - запуск з існуючою базою даних


alembic revision --autogenerate -m 'Init'
alembic upgrade head
#--- запустити серевер
uvicorn main:app --host localhost --port 8000 --reload
uvicorn main:app --reload

--> this text must be added to pyproject.toml
[tool.pytest.ini_options]
pythonpath = ["."]

#---- запустити створення файла тестового покриття
poetry add pytest-cov --dev
pytest --cov=. --cov-report html tests/  


Для запуска тестов в Pytest надо вызвать команду pytest с необходимыми параметрами из терминала. Вот самые необходимые параметры, которые можно использовать в командной строке Pytest:

-v или --verbose - показывает дополнительную информацию о тестах, например, имена тестов, которые были пройдены.
-s - отключает перехват вывода, чтобы вывод тестовых функций был направлен в консоль.
-x - останавливает выполнение тестов при первой ошибке или неудачном тесте.
-q или --quiet - уменьшает количество выводимых сообщений о прогрессе выполнения тестов.
-h или --help - выводит справочную информацию по использованию команды.

 Основные команды Sphinx:

sphinx-quickstart - это команда для создания нового проекта документации. Она задает ряд вопросов пользователю, таких как название проекта, автор, язык и т.д., а затем генерирует структуру каталогов и файлов, которые могут быть использованы для начала работы над документацией.
sphinx-build - это команда для сборки документации. Она принимает входной файл или директорию с исходными файлами документации и генерирует HTML, PDF, LaTeX или другой формат документации.
sphinx-apidoc - это команда для автоматической генерации документации из модулей Python. Она принимает имя модуля Python и генерирует документацию для всех его функций, классов и методов.
sphinx-autogen - это команда, которую следует использовать для генерации документации на основе шаблонов. Она позволяет определить структуру документации и заполнить ее автоматически на основе шаблонов.




