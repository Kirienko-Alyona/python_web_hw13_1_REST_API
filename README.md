# python_web_hw13_1_REST_API

Вот наиболее распространенные команды для работы с файлом docker-compose.yml:

docker-compose up - запуск служб, определенных в файле docker-compose.yml. Эта команда создаст и запустит контейнеры для каждого сервиса, а также создаст сеть для взаимодействия контейнеров.
docker-compose down - остановить и удалить контейнеры, сети и тома, созданные командой docker-compose up.
docker-compose ps - выведет список контейнеров, созданных docker-compose up, а также их статус и другую информацию.
docker-compose logs - просмотр логов контейнеров, созданных docker-compose up.
docker-compose exec <имя службы> <команда> - выполнить команду в запущенном контейнере, созданном docker-compose up. Например, docker-compose exec redis redis-cli запустит команду redis-cli в контейнере redis.
docker-compose build - перестроить образы, определенные в файле docker-compose.yml. Это может быть полезно, если вы внесли изменения в свои сервисы и хотите убедиться, что образы актуальны.
Это лишь несколько наиболее часто используемых команд, полный набор команд docker-compose можно найти в официальной документации Docker Compose.

docker-compose up -d - запустити наступного разу, щоб стару базу підгрузити

 alembic revision --autogenerate -m 'Init'