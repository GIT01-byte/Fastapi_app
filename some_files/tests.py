import asyncio
import time
from fastapi import FastAPI, BackgroundTasks
import uvicorn


app = FastAPI()

def sync_task():
    time.sleep(3)
    print('Отправлен email')
    
async def async_task():
    await asyncio.sleep(3)
    print('Запрос в сторонний API сделан')

@app.post('/')
async def some_route(bg_tasks: BackgroundTasks):
    ...
    bg_tasks.add_task(async_task)
    bg_tasks.add_task(sync_task)
    return {'succces': True}

if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', reload=True)
    