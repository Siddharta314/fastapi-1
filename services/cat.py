from models.cat import Cat as CatModel


class CatService:
    def __init__(self, db) -> None:
        self.db = db

    def get_cats(self):
        return self.db.query(CatModel).all()

    def get_cat(self, id):
        return self.db.query(CatModel).filter(CatModel.id == id).first()

    def get_cat_by_gender(self, gender):
        return self.db.query(CatModel).filter(CatModel.gender == gender).all()
