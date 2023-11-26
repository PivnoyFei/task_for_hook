from sqlalchemy import Integer, cast, func, insert, select, update

from application.database import scoped_session
from application.users.models import Round, RoundsInfo, User
from application.users.schemas import UserCreate


class UserManager:
    async def is_username(self, username: str) -> int | None:
        async with scoped_session() as session:
            return await session.scalar(select(User.id).where(User.username == username))

    async def by_username(self, username: str) -> User | None:
        async with scoped_session() as session:
            return await session.scalar(select(User).where(User.username == username))

    async def create(self, user_in: UserCreate) -> User:
        async with scoped_session() as session:
            query = await session.execute(
                insert(User).values(**user_in.model_dump()).returning(User)
            )
            await session.commit()
            return query.scalar()


class RoundManager:
    async def get(self) -> Round:
        async with scoped_session() as session:
            query = await session.execute(select(Round))
            if result := query.scalar_one_or_none():
                return result

            query = await session.execute(insert(Round).values(number_rounds=1).returning(Round))
            await session.commit()
            return query.scalar()

    async def get_info(self):
        async with scoped_session() as session:
            count_users = await session.execute(
                select(
                    RoundsInfo.number_rounds,
                    func.count(func.distinct(RoundsInfo.user_id)).label("count_users"),
                ).group_by(RoundsInfo.number_rounds)
            )
            count_rounds = func.count(func.distinct(RoundsInfo.number_rounds))
            most_active = await session.execute(
                select(
                    RoundsInfo.user_id,
                    count_rounds.label("count_rounds"),
                    cast(
                        func.count(RoundsInfo.number_rounds) / count_rounds,
                        Integer,
                    ).label("avg_number_moves"),
                ).group_by(RoundsInfo.user_id)
            )
            return {"count_users": count_users.all(), "most_active": most_active.all()}

    async def update(self, round_id: int, items: dict, info_items: dict) -> int | None:
        async with scoped_session() as session:
            try:
                await session.execute(insert(RoundsInfo).values(**info_items))
                user = await session.execute(
                    update(Round).where(Round.id == round_id).values(**items).returning(Round)
                )
                await session.commit()
                return user.scalar()

            except Exception:
                await session.rollback()
                return None
