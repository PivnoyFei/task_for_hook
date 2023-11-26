from copy import copy
from random import choices

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from application.auth.permissions import IsAuthenticated, PermissionsDependency
from application.exceptions import BadRequestException
from application.settings import NUMBERS_WEIGHT
from application.users.managers import RoundManager, UserManager
from application.users.schemas import InfoOut, UserCreate, UserOut

router = APIRouter()


@router.post(
    "/",
    response_model=UserOut,
    status_code=HTTP_201_CREATED,
    response_description="Пользователь успешно создан",
)
async def create_user(user_in: UserCreate) -> UserOut:
    """Регистрация пользователя."""
    if await UserManager().is_username(user_in.username):
        raise BadRequestException("Имя пользователя уже занято")
    return await UserManager().create(user_in)


@router.get(
    "/me/",
    response_model=UserOut,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=HTTP_200_OK,
)
async def me(request: Request) -> JSONResponse:
    """Текущий пользователь."""
    return await UserManager().by_username(request.user.username)


@router.get("/info_roulette/", response_model=InfoOut, status_code=HTTP_200_OK)
async def info_roulette() -> JSONResponse:
    return await RoundManager().get_info()


@router.post(
    "/spin_roulette/",
    response_model=dict,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=HTTP_200_OK,
)
async def spin_roulette(request: Request) -> JSONResponse:
    round = await RoundManager().get()

    if numbers_weight := copy(round.numbers_weight):
        result = choices(list(numbers_weight.keys()), weights=list(numbers_weight.values()))[0]
        del numbers_weight[result]
        update_items = {
            "numbers_weight": numbers_weight,
        }
    else:
        result = "джекпот"
        update_items = {
            "number_rounds": round.number_rounds + 1,
            "numbers_weight": NUMBERS_WEIGHT,
        }

    info_items = {"number_rounds": round.number_rounds, "user_id": request.user.id, "cell": result}
    if await RoundManager().update(round.id, update_items, info_items):
        return {"numbers_weight": result}
    raise BadRequestException("Произошла ошибка!")
