import asyncio
from fastapi import FastAPI
import httpx
from routes import scoreRoute
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(scoreRoute.score)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return 200


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
