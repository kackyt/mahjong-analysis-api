import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

import sentry_sdk
from dotenv import load_dotenv

from api.routers import game, kyoku, statistics, dataset

load_dotenv()

app = FastAPI(
    title="Mahjong Analysis API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ALLOW_ORIGINS"].split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    debug=False,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(dataset.router, prefix="/datasets", tags=["datasets"])
app.include_router(game.router, prefix="/games", tags=["games"])
app.include_router(kyoku.router, prefix="/kyokus", tags=["kyokus"])
app.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
