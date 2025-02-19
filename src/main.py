from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.logging_middleware import LoggingMiddleware
from app.core.config import settings
from app.api.routes import auth, notes, admin
from app.core.logging_config import logger

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "The application is working successfully!"}


app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)
