from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, instance_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == instance_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, page: int, size: int):
        async with async_session_maker() as session:
            query = select(cls.model).order_by(cls.model.id).limit(size).offset((page - 1) * size)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_in_db(cls, data: dict):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            new_instance = result.scalar_one()
            await session.refresh(new_instance)
            return new_instance

    @classmethod
    async def update_one(cls, instance_id: int, data: dict):
        async with async_session_maker() as session:
            existing_instance = await session.execute(
                select(cls.model).where(cls.model.id == instance_id)
            )
            existing_instance = existing_instance.scalar_one_or_none()

            if not existing_instance:
                raise HTTPException(status_code=404, detail="User not found")

            if 'email' in data:
                email_to_check = data['email']
                email_exists = await session.execute(
                    select(cls.model).where(cls.model.email == email_to_check, cls.model.id != instance_id)
                )
                if email_exists.scalar_one_or_none():
                    raise HTTPException(status_code=400, detail="Email already registered.")

            if 'username' in data:
                username_to_check = data['username']
                username_exists = await session.execute(
                    select(cls.model).where(cls.model.username == username_to_check, cls.model.id != instance_id)
                )
                if username_exists.scalar_one_or_none():
                    raise HTTPException(status_code=400, detail="Username already taken.")

            query = update(cls.model).where(cls.model.id == instance_id).values(**data).returning(cls.model)

            try:
                await session.execute(query)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Failed to update user due to integrity error.")

            updated_instance = await session.execute(select(cls.model).where(cls.model.id == instance_id))
            return updated_instance.scalar_one()

    @classmethod
    async def delete_by_id(cls, instance_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == instance_id)
            await session.execute(query)
            await session.commit()
