from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import pets
from .db.db import create_db_and_tables, delete_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
  print('🚀🚀🚀🚀 starting app')
  create_db_and_tables()
  yield
  print('🔚🔚🔚🔚 shutting down app')
  # delete_db_and_tables()

app = FastAPI(lifespan=lifespan)

app.include_router(pets.router)

@app.get('/health-check')
async def health_check():
  return {"message": 'OK'}