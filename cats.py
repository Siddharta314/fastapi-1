from pydantic import BaseModel
from typing import Optional

cats = [
    {"id": 1, "name": "Rodrigo", "age": 2, "gender": "male"},
    {"id": 2, "name": "Pepa", "age": 7, "gender": "female"},
    {"id": 3, "name": "Eustass", "age": 1, "gender": "male"},
    {"id": 4, "name": "Alexandra", "age": 5, "gender": "female"},
]


class Cat(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str
