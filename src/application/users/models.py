import bcrypt
from sqlalchemy import JSON, Boolean, Column, Integer, LargeBinary, String

from application.database import Base
from application.settings import NUMBERS_WEIGHT


class User(Base):
    id = Column(Integer, primary_key=True)
    password = Column(LargeBinary, nullable=False)
    username = Column(String(150), nullable=False, unique=True, index=True)

    is_active = Column(Boolean, nullable=False, default=True)

    async def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password)


class RoundsInfo(Base):
    id = Column(Integer, primary_key=True)
    number_rounds = Column(Integer)
    user_id = Column(Integer)
    cell = Column(String(10))


class Round(Base):
    id = Column(Integer, primary_key=True)
    number_rounds = Column(Integer, default=1)
    numbers_weight = Column(JSON, default=NUMBERS_WEIGHT)
