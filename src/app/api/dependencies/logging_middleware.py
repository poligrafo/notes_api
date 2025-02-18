import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.app.core.logging_config import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования всех HTTP-запросов"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        user = request.state.user if hasattr(request.state, "user") else "Anonymous"

        log_message = (f"User: {user} | Method: {request.method} | Path: {request.url.path} | "
                       f"Status: {response.status_code}")
        logger.info(log_message)

        return response
