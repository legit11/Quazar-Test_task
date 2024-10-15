from fastapi import FastAPI
from src.users.routers import router as user_router


app = FastAPI(
    title="Quazar-test API",
    version="1.0.0",
    root_path="/api"
)

app.include_router(user_router)
