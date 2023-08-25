from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession) -> None:
        """
        Сохранить модель в базу данных.
        :param db_session: Сессия базы данных
        :return: None
        """

        try:
            db_session.add(self)

            await db_session.commit()
        except IntegrityError:
            raise Exception("Entity with assigned data already exists")
        except SQLAlchemyError:
            raise Exception("Cant create model")

    async def delete(self, db_session: AsyncSession) -> None:
        """
        Сохранить изменения в модели.
        :param db_session: Сессия базы данных
        :return: None
        """

        try:
            await db_session.delete(self)

            await db_session.commit()
        except SQLAlchemyError:
            raise Exception("Cant delete model")

    async def update(self, db_session: AsyncSession, **kwargs) -> None:
        """
        Обновить модель в базе данных.
        :param db_session: Сессия базы данных
        :param kwargs: Поля модели для обновления
        :return: None
        """

        try:
            for k, v in kwargs.items():
                setattr(self, k, v)

            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError:
            raise Exception("Cant update model")
