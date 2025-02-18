from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.include_router(auth.router)
