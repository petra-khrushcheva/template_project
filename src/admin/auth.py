from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from database.db_config import async_session
from services import admin_service
from utils import verify_password


class UsernameAndPasswordProvider(AuthProvider):

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        async with async_session() as session:
            admin = await admin_service.get(session=session, username=username)
            if not admin:
                raise LoginFailed("Invalid username or password")

            if not verify_password(password, admin.password):
                raise LoginFailed("Invalid username or password")

            request.session.update({"username": username})
            return response

    async def is_authenticated(self, request) -> bool:

        if request.session.get("username", None):
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            async with async_session() as session:
                request.state.user = await admin_service.get(
                    session=session, username=request.session.get("username")
                )
                return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        custom_app_title = "Hello, " + user.username + "!"
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
