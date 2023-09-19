from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token


class User(BaseModel):
    email: str
    password: str


user_router = APIRouter()


@user_router.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(vars(user))
        return JSONResponse(status_code=200, content=token)
