from fastapi import FastAPI

from .routers import pets

app = FastAPI()

app.include_router(pets.router)

@app.get('/health-check')
async def health_check():
  return {"message": 'OK'}