import asyncio
from fastapi import FastAPI
import httpx
from routes import scoreRoute
app = FastAPI()
app.include_router(scoreRoute.score)

@app.get("/health")
async def health_check():
    return 200

