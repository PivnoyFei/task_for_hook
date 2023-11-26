from pydantic import BaseModel

name_en_str = "^[A-Za-z]+$"


class BaseSchema(BaseModel):
    id: int

    class ConfigDict:
        from_attributes = True
