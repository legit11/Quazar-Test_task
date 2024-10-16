import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserFromDB(UserCreate):
    id: int
    registration_date: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserCreate):
    pass


class UserStatistics(BaseModel):
    recent_7days_users_count: int
    top_5_users: list
    domain_share: float
