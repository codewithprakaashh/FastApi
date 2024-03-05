import asyncio
from asyncio import create_task
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, users

from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount('/static',StaticFiles(directory='static'), name='static')




@app.get('/')
async def root():
    return RedirectResponse(url="/todos",status_code = status.HTTP_302_FOUND)


async def keep_alive_task():
  # Simulate keeping the server alive (replace with your actual logic)
  print("Background Task: Keeping server alive...")
  await asyncio.sleep(600)  

async def startup():
  # Schedule background task here
  task = create_task(keep_alive_task())

app.add_event_handler("startup", startup)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)




