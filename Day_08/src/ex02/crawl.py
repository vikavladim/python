import asyncio
import random
import sys

import aiohttp
import json

urls = [
    "https://ru.wikipedia.org/wiki/%D0%AE%D0%BD%D1%83%D1%81-%D0%91%D0%B5%D0%BA_%D0%95%D0%B2%D0%BA%D1%83%D1%80%D0%BE%D0%B2",
    "https://www.kommersant.ru/doc/425444",
    "https://www.gazeta.ru/politics/2019/09/26_a_12655161.shtml",
    "https://www.kommersant.ru/doc/425444",
    # "https://www.rbc.ru/politics/26/09/2019/5d8d4c7a9a794700c4749c5a", "https://tass.ru/politika/6841111",
    # "https://ria.ru/20190926/1559066091.html", "https://www.interfax.ru/russia/6841111",
    # "https://www.vedomosti.ru/politics/articles/2019/09/26/8101111", "https://regnum.ru/news/polit/2651111",
    # "https://www.mk.ru/incident/2019/09/26/v-ingushetii-zaderzhali-aktivistov-za-organizatsiyu-mitinga.html"
    # 'http://localhost:8888/api/v1/tasks/a',
    # 'http://localhost:8888/api/v1/task',
]


async def send_tasks(urls):
    data = {'urls': urls}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8888/api/v1/tasks/', json=data) as response:
            if response.status == 201:
                task_id = (await response.json())['task']['id']
                return task_id
            else:
                print(f"Error: {response.text}")
                return None


async def get_task(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/api/v1/tasks/{task_id}') as response:
            if response.status == 200:
                task = await response.json()
                return task
            else:
                print(f"Error: {response.status}")
                return None


async def main():
    # urls = sys.argv[1:]
    task_id = await send_tasks(urls)
    while True:
        task = await get_task(task_id)
        print(task)
        task_status = task['status']
        if task_status == 'ready':
            results = task['results']
            for url, status_code in results.items():
                print(f"{status_code}\t{url}")
            break
        await asyncio.sleep(1)


asyncio.run(main())
