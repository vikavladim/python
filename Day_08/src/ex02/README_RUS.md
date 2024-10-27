Написать 

``` bash 
docker-compose run -it day08_cont bash
``` 

Запуск сервера:

```bash
nohup uvicorn server_cached:app --port 8888 --limit-max-requests 1
```

А дальше всё может быть. Неспособность проверить работоспособность. И непонятно, когда они хотят чистить БД? И всю ли?