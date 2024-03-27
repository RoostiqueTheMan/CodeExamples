"""Module with Services table operations."""

from typing import Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from authorization_app import models
from authorization_app.dbase import orm
from authorization_app.dbase.dal.base import BaseDAL

__all__ = [
    'ServiceDAL'
]


class ServiceDAL(BaseDAL):
    """Class with Services table methods."""

    def __init__(self, session: AsyncSession):
        """Initializing method.

        Args:
            session: AsyncSession
        """
        super().__init__(session=session)

    async def get_by_name(self, name: str) -> Union[models.Service, None]:
        """Get service by name.

        Args:
            name: service name

        Returns: Service or None
        """
        query = select(orm.Service).where(
            func.lower(orm.Service.name) == name.lower()
        )
        service = (await self.session.execute(query)).scalar()

        if not service:
            return

        return models.Service(id_=service.id_, name=service.name)