from pydantic import BaseModel, Field, StringConstraints, field_validator
from typing_extensions import Annotated

from application.schemas import BaseSchema, name_en_str
from application.users.utils import hash_password


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(pattern=name_en_str, min_length=1, max_length=150)]
    password: str | bytes = Field(min_length=7, max_length=150)

    class ConfigDict:
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "username": "vasyapupkin",
                "password": "Qwerty123",
            }
        }

    @field_validator("password")
    @classmethod
    def hash(cls, v: str) -> bytes:
        return hash_password(v)


class UserOut(BaseSchema):
    username: str


class CountUsers(BaseModel):
    number_rounds: int = Field(..., description="Номер раунда рулетки")
    count_users: int = Field(..., description="Количество пользователей")


class MostActiveUsers(BaseModel):
    user_id: int = Field(..., description="Айди пользователя")
    count_rounds: int = Field(..., description="Количество раундов рулетке в которые он участвовал")
    avg_number_moves: int = Field(
        ..., description="Среднее количество прокручиваний рулетки за раунд"
    )


class InfoOut(BaseModel):
    count_users: list[CountUsers]
    most_active: list[MostActiveUsers]
