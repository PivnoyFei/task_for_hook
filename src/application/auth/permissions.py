from abc import ABC, abstractmethod
from typing import Optional

from starlette.authentication import AuthenticationBackend
from starlette.requests import HTTPConnection, Request

from application.auth.managers import AuthTokenManager
from application.auth.schemas import CurrentUser
from application.exceptions import BadRequestException, CustomException, UnauthorizedException
from application.users.models import User


class AuthBackend(AuthenticationBackend):
    """Авторизация по токену.
    Все запросы от имени пользователя должны выполняться с заголовком
    "Authorization: Token TOKENVALUE"
    Отдает `CurrentUser` для дальнейшей работы с неавторизованными пользователями.
    Для авторизованных пользователей отдает `User`."""

    async def authenticate(self, request: HTTPConnection) -> tuple[bool, Optional[User]]:
        current_user = CurrentUser()
        authorization: str = request.headers.get("Authorization", None)
        if authorization:
            scheme, credentials = authorization.split()
            if scheme.lower() == "token":
                if user := await self.get_current_user(credentials):
                    return True, user

        return False, current_user

    async def get_current_user(self, token: str) -> User | None:
        user: User = await AuthTokenManager().check(token)
        if user and not user.is_active:
            raise BadRequestException("Неактивный пользователь")
        return user


class BasePermission(ABC):
    """
    Абстрактный класс, от которого должны быть унаследованы все остальные разрешения.
    При инициализации вызывает абстрактный метод `has_permission`
    который будет специфичен для конкретной реализации класса разрешений.

    .. code-block:: python

        class YourIsAuthenticated(BasePermission):
            exception = YourException

            def has_permission(self, request: Request) -> bool:
                return request.user.id is not None
    """

    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        raise NotImplementedError("Метод должен быть переопределен.")


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class PermissionsDependency:
    """
    Зависимость от разрешений, которая используется для определения и проверки всех разрешений
    классов, из одного места внутри определения маршрута.
    Используйте в качестве аргумента `Depends` следующим образом:

    .. code-block:: python

        @app.get("/your/", dependencies=[Depends(PermissionsDependency([YourPermission]))])
    """

    def __init__(self, permissions_classes: list[type[BasePermission]]) -> None:
        self.permissions_classes = permissions_classes

    async def __call__(self, request: Request) -> None:
        for permission_class in self.permissions_classes:
            cls = permission_class()
            if not await cls.has_permission(request=request):
                raise cls.exception
