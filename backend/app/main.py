
from fastapi import FastAPI
from app.api.v1.router import router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Bitaxe Monitor API", version="1.0.0")
app.include_router(router, prefix="/api/v1")
