from datetime import date
from enum import Enum
from typing import Optional, Self

from sqlalchemy import select, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class UserStage(Enum):
    WELCOME = "welcome"
    WAITING_FOR_MATERIAL = "waiting_for_material"
    IDLE = "idle"


class User(Base):
    user_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    current_stage: Mapped[UserStage] = mapped_column(default=UserStage.WELCOME)
    created_at: Mapped[date] = mapped_column(Date(), default=date.today())

    @classmethod
    async def find_by_user_id(
        cls, db_session: AsyncSession, user_id: str
    ) -> Self | None:
        """
        Поиск пользователя по UserID.
        :param db_session: Сессия базы данных
        :param user_id: Telegram UserID пользователя
        :return: self | None
        """

        stmt = select(cls).where(cls.user_id == user_id)
        result = await db_session.execute(stmt)

        return result.scalars().first()
