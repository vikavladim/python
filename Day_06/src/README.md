Написать 
``` bash 
docker-compose run -it day06_cont bash
``` 
Потом внутри контейнера
``` bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/ship.proto
```
Остальное не внутри контейнера
Сгенерируются файлы (3 pb2). Нужно написать сервер и клиент и запустить их.

``` bash
python reporting_server.py
```

``` bash
python reporting_client.py
```

Затем в третьей части:

```bash
alembic init migrations
```

```bash
alembic revision --autogenerate
```

```bash
alembic upgrade head
```