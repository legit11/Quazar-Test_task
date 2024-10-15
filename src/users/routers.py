from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from src.users.dao import UserDao
from src.users.schemas import UserCreate, UserFromDB, UserUpdate
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users_main_functional"],
)


@router.get("/statistics", response_model=Dict[str, Any])
async def get_user_statistics(domain: str):
    return await UserService.get_user_statistics(domain)


@router.post("/users", response_model=UserFromDB)
async def create_user(user: UserCreate):
    user_data = user.dict()

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


@router.get("/users", response_model=list[UserFromDB])
async def read_users(page: int = 1, size: int = 10):
    users = await UserDao.find_all(page, size)
    return users


@router.get("/users/{user_id}", response_model=UserFromDB)
async def read_user(user_id: int):
    user = await UserDao.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserFromDB)
async def update_user(user_id: int, user: UserUpdate):
    existing_user = await UserDao.find_by_id(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await UserDao.update_one(user_id, user.dict())
    return updated_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    existing_user = await UserDao.find_by_id(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await UserDao.delete_by_id(user_id)
    return("User deleted")
