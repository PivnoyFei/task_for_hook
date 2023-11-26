from datetime import datetime
from uuid import uuid4

from sqlalchemy import and_, delete, insert, select

from application.auth.models import AuthToken, generate_uuid
from application.database import scoped_session
from application.settings import settings
from application.users.models import User


def generate_uuid() -> str:
    return str(uuid4().hex)


class AuthTokenManager:
    async def create(self, user_id: int) -> AuthToken | None:
        async with scoped_session() as session:
            query = await session.execute(
                insert(AuthToken)
                .values(
                    key=generate_uuid(),
                    created=datetime.now() + settings.TOKEN_EXP,
                    user_id=user_id,
                )
                .returning(AuthToken.key)
            )
            await session.commit()
            return query.scalar()

    async def check(self, token: str) -> User | None:
        """Возвращает информацию о владельце указанного токена."""
        async with scoped_session() as session:
            query = await session.execute(
                select(User)
                .join(AuthToken, AuthToken.user_id == User.id)
                .where(and_(AuthToken.key == token, AuthToken.created > datetime.now()))
            )
            if user := query.scalar_one_or_none():
                return user
            return None

    async def delete(self, user_id: int) -> None:
        """Удаляет токен при выходе владельца."""
        async with scoped_session() as session:
            await session.execute(delete(AuthToken).where(AuthToken.user_id == user_id))
            await session.commit()
            return True
