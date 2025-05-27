# main.py
from fastapi import FastAPI
from routes import scoreRoute  # importa tu archivo de rutas

app = FastAPI()

app.include_router(scoreRoute.score)
