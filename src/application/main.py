from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.sql.schema import MetaData
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request

from application.auth.permissions import AuthBackend
from application.auth.views import router as auth_router
from application.database import Base
from application.exceptions import CustomException
from application.settings import settings
from application.users.views import router as user_router


def init_routers(app_: FastAPI) -> None:
    router = APIRouter()
    router.include_router(auth_router, prefix="/auth", tags=["auth"])
    router.include_router(user_router, prefix="/users", tags=["users"])
    app_.include_router(router, prefix=settings.API_V1_STR)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception) -> JSONResponse:
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        debug=False,
        title="HOOK",
        description="Тестовое задание для Hook",
        version="1.0",
        redoc_url=f"{settings.API_V1_STR}/docs",
        middleware=make_middleware(),
        contact={
            "name": "Смелов Илья",
            "url": "https://github.com/PivnoyFei",
        },
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app: FastAPI = create_app()


@app.get("/")
async def main(request: Request) -> dict[str, str]:
    return {
        "app": app.title,
        "doc_path": f"{request.base_url}docs",
    }


metadata: MetaData = Base.metadata
