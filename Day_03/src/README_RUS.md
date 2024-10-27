``` bash
docker build .
```
или лучше
``` bash
docker build -t day03_image . 
```

Потом запускать командой
``` bash   
docker run -d --name day03_cont day03_image
```
Далее
``` bash
docker exec -it day03_cont bash
```
Внутри сделать redis-cli и проверить

Чтобы ВСЁ почистить:
``` bash
docker stop $(docker ps -aq) 
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
```