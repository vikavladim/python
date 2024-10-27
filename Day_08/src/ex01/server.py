from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import asyncio
import aiohttp
from fastapi.responses import JSONResponse

app = FastAPI()

class Task(BaseModel):
    id: str
    status: str
    results: dict

class UrlsStruct(BaseModel):
    urls: List[str]

tasks = {}


@app.post("/api/v1/tasks/")
async def create_task(urls_struct: UrlsStruct):
    try:
        urls = urls_struct.urls
        print(urls)
        task_id = str(uuid4())
        tasks[task_id] = Task(id=str(task_id), status='running', results={})
        await asyncio.create_task(process_task(task_id, urls))
        return JSONResponse(content={'task': tasks[task_id].dict()}, status_code=201)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

async def process_task(task_id, urls):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                tasks[task_id].results[url] = response.status
            print(f'{response.status}\t{url}')
    tasks[task_id].status = 'ready'

@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id in tasks:
        return tasks[task_id]
    else:
        raise HTTPException(status_code=404, detail="Task not found")
