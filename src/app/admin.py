# from starlette_admin.contrib.sqla import ModelView, Admin
# from starlette_admin.auth import AuthProvider
# from starlette.requests import Request
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.db.session import async_session_maker, engine
# from app.db.base import Base  # ✅ Используем `Base.metadata`, чтобы избежать дублирования
# from app.db.models import User, Note
# from app.core.security import verify_password
#
#
# class CustomAuthProvider(AuthProvider):
#     """Аутентификация в админке"""
#
#     async def login(self, request: Request) -> bool:
#         """Авторизация в админке (через форму входа)"""
#         form = await request.form()
#         username = form.get("username")
#         password = form.get("password")
#
#         async with async_session_maker() as session:
#             result = await session.execute(select(User).where(User.username == username))
#             user = result.scalars().first()
#
#             if user and verify_password(password, user.password_hash) and user.role == "Admin":
#                 request.session["user"] = {"username": user.username}
#                 return True
#
#         return False
#
#     async def is_authenticated(self, request: Request) -> bool:
#         """Проверка аутентификации"""
#         return "user" in request.session
#
#
# # ✅ Используем `Base.metadata`, чтобы избежать дублирования таблиц
# admin = Admin(
#     engine,
#     title="Notes Admin Panel",
#     auth_provider=CustomAuthProvider(),
# )
#
#
# class AsyncModelView(ModelView):
#     """Обеспечиваем правильное подключение `async_session_maker`"""
#     async def scaffold_session(self) -> AsyncSession:
#         return async_session_maker()
#
#
# # ✅ Теперь передаем асинхронную сессию
# admin.add_view(AsyncModelView(User))
# admin.add_view(AsyncModelView(Note))
