import asyncio
from fastapi import FastAPI
import httpx
from routes import scoreRoute
app = FastAPI()
app.include_router(scoreRoute.score)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

async def periodic_health_check():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get("https://pythonbackend-searchkeywords.onrender.com/health")
                print(f"Health check status: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"Health check failed: {e}")
            await asyncio.sleep(120)  

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_health_check())

