from typing import Dict, Any

from fastapi import HTTPException

from src.users.dao import UserDao
from src.users.schemas import UserFromDB


class UserService:
    @staticmethod
    async def get_user_statistics(domain: str) -> Dict[str, Any]:
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

        return {
            "recent_users_count": recent_users_count,
            "top_5_users": [UserFromDB.from_orm(user) for user in top_5_users],
            "domain_share": domain_share
        }
