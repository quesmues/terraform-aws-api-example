from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as v1_router
from app.config.settings import settings

app = FastAPI(debug=settings.debug)

app.include_router(v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_allow_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
