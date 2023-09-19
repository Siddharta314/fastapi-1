"""
Defining the endpoints of the application
"""

from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi import Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from schemas.cat import Cat
from services.cat import CatService

cat_router = APIRouter()


@cat_router.get(
    "/cats",
    tags=["cats"],
    response_model=List[Cat],
    status_code=status.HTTP_200_OK,
)
def get_cats():
    """Get all the cats in the database"""
    db = Session()
    res = CatService(db).get_cats()
    return JSONResponse(status_code=200, content=jsonable_encoder(res))


@cat_router.get("/cats/{id}", tags=["cats"], response_model=Cat)
def get_cat_by_id(id: int = Path(ge=1)):
    """
    Get a cata by id from the database.
    The id must be >= 1
    """
    db = Session()
    res = CatService(db).get_cat(id)
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    raise HTTPException(status_code=404, detail="Cat not found")


@cat_router.get("/cats/", tags=["cats"], response_model=List[Cat])  # male/female
def get_cat_by_gender(
    gender: str = Query(min_length=4, max_length=6)
):  # detect parameter query
    """
    Get a cata by gender from the database.
    The gender must be male or female.
    """
    db = Session()
    res = CatService(db).get_cat_by_gender(gender)
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    return JSONResponse(
        status_code=404, content={"message": "There are no cats of this gender"}
    )


@cat_router.post("/cats/", tags=["cats"])
def create_cat(cat: Cat):
    """Create a cat in the database."""
    db = Session()
    CatService(db).create_cat(cat)
    return JSONResponse(status_code=200, content={"message": "New cat added to db"})


@cat_router.put("/cats/{id}", tags=["cats"], dependencies=[Depends(JWTBearer())])
def update_cat(id: int, cat_update: Cat):
    """
    Update information of a cat by id
    JWT authentication token required
    """
    db = Session()
    res = CatService(db).get_cat(id)
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    CatService(db).update_cat(id, cat_update)

    return JSONResponse(
        status_code=200,
        content={"message": "The cat info has been updated successfully"},
    )


@cat_router.delete("/cats/{id}", tags=["cats"], dependencies=[Depends(JWTBearer())])
def delete_cat(id: int):
    """
    Delete a cat by id from the database
    JWT authentication token required
    """
    db = Session()
    res = CatService(db).get_cat(id)
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    CatService(db).delete_cat(id)
    return JSONResponse(
        status_code=200,
        content={"message": "The cat has been deleted forever"},
    )
