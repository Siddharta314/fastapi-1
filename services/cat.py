from models.cat import Cat as CatModel
from schemas.cat import Cat


class CatService:
    def __init__(self, db) -> None:
        self.db = db

    def get_cats(self):
        return self.db.query(CatModel).all()

    def get_cat(self, id: int):
        return self.db.query(CatModel).filter(CatModel.id == id).first()

    def get_cat_by_gender(self, gender: str):
        return self.db.query(CatModel).filter(CatModel.gender == gender).all()

    def create_cat(self, cat: Cat):
        new_cat = CatModel(**vars(cat))
        self.db.add(new_cat)
        self.db.commit()
        return

    def update_cat(self, id: int, cat_update: Cat):
        cat = self.get_cat(id)
        cat.name = cat_update.name
        cat.age = cat_update.age
        cat.gender = cat_update.gender
        self.db.commit()
        return

    def delete_cat(self, id):
        cat = self.get_cat(id)
        self.db.delete(cat)  # or cat.delete()
        self.db.commit()
        return
