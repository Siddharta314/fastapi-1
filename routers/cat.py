from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi import Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from models.cat import Cat as CatModel
from schemas.cat import Cat
from services.cat import CatService

cat_router = APIRouter()


@cat_router.get(
    "/cats",
    tags=["cats"],
    response_model=List[Cat],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_cats():
    db = Session()
    res = CatService(db).get_cats()
    return JSONResponse(status_code=200, content=jsonable_encoder(res))


@cat_router.get("/cats/{id}", tags=["cats"], response_model=Cat)
def get_cat_by_id(id: int = Path(ge=1)):
    db = Session()
    res = CatService(db).get_cat(id)
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    raise HTTPException(status_code=404, detail="Cat not found")


@cat_router.get("/cats/", tags=["cats"], response_model=List[Cat])  # male/female
def get_cat_by_gender(
    gender: str = Query(min_length=4, max_length=6)
):  # detect parameter query
    db = Session()
    res = CatService(db).get_cat_by_gender(gender)
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    return JSONResponse(
        status_code=404, content={"message": "There are no cats of this gender"}
    )


@cat_router.post("/cats/", tags=["cats"])
def create_cat(cat: Cat):
    db = Session()
    CatService(db).create_cat(cat)
    return JSONResponse(status_code=200, content={"message": "New cat added to db"})


@cat_router.put("/cats/{id}", tags=["cats"])
def update_cat(id: int, cat_update: Cat):
    db = Session()
    res = CatService(db).get_cat(id)
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    CatService(db).update_cat(id, cat_update)

    return JSONResponse(
        status_code=200,
        content={"message": "The cat info has been updated successfully"},
    )


@cat_router.delete("/cats/{id}", tags=["cats"])
def delete_cat(id: int):
    db = Session()
    res = CatService(db).get_cat(id)
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    CatService(db).delete_cat(id)
    return JSONResponse(
        status_code=200,
        content={"message": "The cat has been deleted forever"},
    )
