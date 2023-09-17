from pydantic import BaseModel, Field
from typing import Optional


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
