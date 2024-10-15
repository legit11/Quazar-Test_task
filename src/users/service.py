from typing import Dict, Any

from fastapi import HTTPException

from src.users.dao import UserDao
from src.users.schemas import UserFromDB, UserStatistics


class UserService:
    @classmethod
    async def get_user_statistics(cls, domain: str) -> UserStatistics:
        try:
            recent_users_count = await UserDao.count_recent_users()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Error counting recent users: {str(e)}")

        try:
            top_5_users = await UserDao.top_5_longest_usernames()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Error retrieving top 5 users: {str(e)}")

        try:
            domain_share = await UserDao.get_domain_share(domain)
            if domain_share is None:
                raise HTTPException(status_code=404, detail="Domain share not found.")
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Error retrieving domain share: {str(e)}")

        return UserStatistics(
            recent_users_count=recent_users_count,
            top_5_users=[UserFromDB.from_orm(user) for user in top_5_users],
            domain_share=domain_share
        )

    @classmethod
    async def create_user(cls, user_data: Dict[str, Any]) -> UserFromDB:
        existing_user_by_email = await UserDao.find_by_email(user_data['email'])
        if existing_user_by_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        existing_user_by_username = await UserDao.find_by_username(user_data['username'])
        if existing_user_by_username:
            raise HTTPException(status_code=400, detail="Username already taken")

        try:
            new_user = await UserDao.add_in_db(user_data)
            return UserFromDB.from_orm(new_user)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
