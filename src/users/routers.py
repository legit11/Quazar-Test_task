from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from src.users.dao import UserDao
from src.users.schemas import UserCreate, UserFromDB, UserUpdate, UserStatistics
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users_main_functional"],
)


@router.get("/statistics", response_model=UserStatistics)
async def get_user_statistics(domain: str):
    return await UserService.get_user_statistics(domain)


@router.post("", response_model=UserFromDB)
async def create_user(user: UserCreate):
    user_data = user.dict()
    return await UserService.create_user(user_data)


@router.get("", response_model=list[UserFromDB])
async def read_users(
        page:int = Query(default=1,
        description="Номер страницы",
        gt=0,
    ),
    size: int = Query(
        default=10,
        description="Размер страницы",
        gt=0,
    )
):
    users = await UserDao.find_all(page, size)
    return users


@router.get("/{user_id}", response_model=UserFromDB)
async def read_user(user_id: int):
    user = await UserDao.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserFromDB)
async def update_user(user_id: int, user: UserUpdate):
    existing_user = await UserDao.find_by_id(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await UserDao.update_one(user_id, user.dict())
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    existing_user = await UserDao.find_by_id(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await UserDao.delete_by_id(user_id)
