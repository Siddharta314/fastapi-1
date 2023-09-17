from pydantic import BaseModel, Field
from typing import Optional

cats = [
    {"id": 1, "name": "Rodrigo", "age": 2, "gender": "male"},
    {"id": 2, "name": "Pepa", "age": 7, "gender": "female"},
    {"id": 3, "name": "Eustass", "age": 1, "gender": "male"},
    {"id": 4, "name": "Alexandra", "age": 5, "gender": "female"},
]


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
                    "category": "unko",
                }
            ]
        }
    }
