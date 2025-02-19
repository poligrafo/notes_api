from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.app.core.logging_config import logger
from src.app.core.security import decode_access_token


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования всех HTTP-запросов"""

    async def dispatch(self, request: Request, call_next) -> Response:
        user = "Anonymous"  # По умолчанию анонимный пользователь
        token = request.headers.get("Authorization")

        if token and token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
            try:
                payload = decode_access_token(token)
                if payload and "sub" in payload and "role" in payload:
                    role = payload["role"]
                    user_id = payload["sub"]
                    if role == "Admin":
                        user = f"Admin ID {user_id}"
                    else:
                        user = f"User ID {user_id}"
            except Exception as e:
                logger.warning(f"Failed to decode token: {e}")

        response = await call_next(request)

        log_message = (f"User: {user} | Method: {request.method} | Path: {request.url.path} | "
                       f"Status: {response.status_code}")
        logger.info(log_message)

        return response

