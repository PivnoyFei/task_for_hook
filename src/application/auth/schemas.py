from pydantic import BaseModel, Field

from application.schemas import BaseSchema


class UserLogin(BaseModel):
    username: str
    password: str


class TokenBase(BaseModel):
    auth_token: str


class CurrentUser(BaseSchema):
    id: int = Field(None, description="Id")
    username: str = Field(None, description="Username")
    is_active: bool = Field(False, description="Is active")

    class ConfigDict:
        validate_assignment = True
