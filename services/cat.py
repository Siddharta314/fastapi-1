""""
Implementation of the cat services class
"""
from typing import List
from models.cat import Cat as CatModel
from schemas.cat import Cat


class CatService:
    """
    CatService provides the connection with the database by query
    """

    def __init__(self, db) -> None:
        self.db = db

    def get_cats(self) -> List[Cat]:
        return self.db.query(CatModel).all()

    def get_cat(self, id: int) -> Cat:
        return self.db.query(CatModel).filter(CatModel.id == id).first()

    def get_cat_by_gender(self, gender: str) -> List[Cat]:
        return self.db.query(CatModel).filter(CatModel.gender == gender).all()

    def create_cat(self, cat: Cat) -> None:
        new_cat = CatModel(**vars(cat))
        self.db.add(new_cat)
        self.db.commit()
        return None

    def update_cat(self, id: int, cat_update: Cat) -> None:
        cat = self.get_cat(id)
        cat.name = cat_update.name
        cat.age = cat_update.age
        cat.gender = cat_update.gender
        self.db.commit()
        return None

    def delete_cat(self, id) -> None:
        cat = self.get_cat(id)
        self.db.delete(cat)  # or cat.delete()
        self.db.commit()
        return
