from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import validate_token


class Cat(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=8)
    age: int = Field(gt=0)
    gender: str = Field(min_length=4, max_length=6)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "name",
                    "age": 1,
                    "gender": "unkown",
                }
            ]
        }
    }


class User(BaseModel):
    email: str
    password: str


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data["email"] != "admin@admin.com":
            raise HTTPException(status_code=403, detail="invalid credentials")
