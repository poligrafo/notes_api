from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.dependencies.logging_middleware import LoggingMiddleware
from app.core.config import settings
from app.api.routes import auth, notes, admin
from app.core.logging_config import logger
# from app.admin import admin as admin_panel

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(LoggingMiddleware)

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "The application is working successfully!"}

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)


# admin_panel.mount_to(app)