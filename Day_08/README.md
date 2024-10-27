# Содержание

- [Задание 00: Я знаю Кунг-Фу](#упражнение-00-я-знаю-кунг-фу)
- [Упражнение 01: Кальмар на палочке](#упражнение-01-кальмар-на-палочке)
- [Упражнение 02: Дежа Вю](#упражнение-02-дежа-вю)

### Упражнение 00: Я знаю Кунг-Фу

Напишите скрипт "fight.py", который будет включать в себя следующий код:

```python
import asyncio

from enum import Enum, auto
from random import choice


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)
```

Для простоты, в этом учебном сеансе доступны только четыре действия для обоих агента и Нео.
Рецепт победы в бою прост: для каждого удара Нео должен защитить ту часть тела (высокая/низкая),
куда направлен агент, а для каждого блока он должен целиться в незащищенную часть тела.

Вам необходимо написать скрипт под названием "fight.py", который будет включать неизмененный код
из вышеуказанного, а также асинхронную функцию 'fight()', которая будет реализовывать логику,
описанную выше.

Выход скрипта может выглядеть так (поскольку действия рандомизированы, фактический результат будет
отличаться на каждом запуске):

``` bash
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 4
Agent: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 3
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 3
Agent: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent Health: 3
Agent: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 2
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 2
Agent: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent Health: 2
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 2
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 1
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 0
Neo wins!
```

БОНУС: за дополнительные очки вы можете написать еще одну функцию под названием 'fightmany(n)',
где вместо одного агента Нео будет сражаться с несколькими агентами (списком), поэтому первая строка
может быть:

``` python
agents = [Agent() for _ in range(n)]
```

Попробуйте найти способ рандомизировать входящие действия от агентов и реагировать на них
соответственно. Лог боя с тремя агентами может выглядеть так:

``` bash
Agent 1: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 1 Health: 4
Agent 2: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 2 Health: 5
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 4
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 4
Agent 1: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 1 Health: 4
Agent 2: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 2 Health: 4
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 1: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 1 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 2
Agent 2: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 1
Agent 1: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 1 Health: 2
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 1
Agent 2: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 0
Agent 2: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 2 Health: 1
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 0
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 0
Neo wins!
```

### Упражнение 01: Кальмар на палочке

Поэтому давайте создадим кальмара.

Для этого задания рекомендуется быть минималистичным. Программа должна состоять из двух файлов - `crawl.py` и
`server.py`. Рекомендуется использовать [aiohttp](https://docs.aiohttp.org/en/stable/)
или [httpx](https://www.python-httpx.org/) для клиентской стороны и [FastAPI](https://fastapi.tiangolo.com/) для
серверной стороны. Все ввод-вывод должен быть асинхронным.

Поток работы следующий:

- сервер запускается и прослушивает порт 8888
- клиент (`crawl.py`) получает один или несколько запросимых URL в качестве аргумента
- клиент отправляет все URL через HTTP POST запрос в формате JSON списка на конечную точку сервера `/api/v1/tasks/`
- сервер отвечает с HTTP 201 созданным и объектом задачи (рекомендуется
  использовать [PyDantic](https://pydantic-docs.helpmanual.io/))
- объект задачи включает статус "запущен" и ID, который
  является [UUID4](https://docs.python.org/3/library/uuid.html#uuid.uuid4)
- сервер затем асинхронно (не используйте потоки или multiprocessing) отправляет HTTP GET запросы на отправленные URL и
  собирает коды ответов HTTP, либо 200, либо 404 или другой
- клиент периодически запрашивает конечную точку `/api/v1/tasks/{полученный_ID_задачи}` до тех пор, пока сервер не
  закончит обрабатывать все URL. Затем статус задачи должен измениться на "готов" и поле "результат" задачи должно
  содержать список кодов ответов для отправленных URL
- клиент выводит табулированный код ответа HTTP и соответствующий URL для каждого элемента

В синхронном мире люди часто реализуют это с помощью модулей, таких
как [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html), но в этой задаче не требуются
внешние рабочие процессы, поэтому весь сервер должен быть в одном Python-файле, и весь код должен
использовать [парадигму async/await](https://docs.python.org/3/library/asyncio-task.html).

### Упражнение 02: Дежа Вю

Одна из функций, которой наш кроллер еще не обладает, - это кэширование. Если сервер недавно видел один из отправленных
URL, он может просто взять закэшированное значение для кода HTTP.

Другое дело - собрать некоторые метрики по входным данным. Независимо от того, попал ли URL в кэш или нет, давайте также
посчитаем на сервере, сколько запросов мы сделали до сих пор для определенного домена (например,
для "https://www.google.com/search?q=there+is+no+spoon" домен будет "www.google.com").

Для кэширования и счетчика доменов следует использовать Redis. Все код должен быть асинхронным и использовать парадигму
async/await. Для этого можно использовать библиотеку [aioredis](https://aioredis.readthedocs.io/en/latest/).

Поскольку клиентский код не изменен, следует предоставить только один файл с измененным серверным кодом EX01,
названным "server_cached.py".

БОНУС: Обновите код и добавьте еще одну корутину, которая будет очищать записи в кэше после некоторого конфигурируемого
таймаута.
