from datetime import datetime, timedelta

from sqlalchemy import select, func

from src.dao.base import BaseDAO
from src.users.models import User
from src.database import async_session_maker


class UserDao(BaseDAO):
    model = User

    @classmethod
    async def find_by_email(cls, email: str):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.email == email))
            return result.scalars().first()

    @classmethod
    async def find_by_username(cls, identifier: str):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(
                (cls.model.email == identifier) | (cls.model.username == identifier)
            ))
            return result.scalars().first()

    @classmethod
    async def count_recent_users(cls):
        async with async_session_maker() as session:
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            query = select(func.count(cls.model.id)).where(cls.model.registration_date >= seven_days_ago)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def top_5_longest_usernames(cls):
        async with async_session_maker() as session:
            query = select(cls.model).order_by(func.length(cls.model.username).desc()).limit(5)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_domain_share(cls, domain: str):
        async with async_session_maker() as session:
            total_users_query = select(func.count(cls.model.id))
            domain_users_query = select(func.count(cls.model.id)).where(cls.model.email.like(f'%@{domain}'))

            total_users = await session.execute(total_users_query)
            total_users_count = total_users.scalar()

            domain_users = await session.execute(domain_users_query)
            domain_users_count = domain_users.scalar()

            if total_users_count == 0:
                return 0

            return domain_users_count / total_users_count
