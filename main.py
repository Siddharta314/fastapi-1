from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from jwt_manager import create_token
from config.database import Session, engine, Base
from models.cat import Cat as CatModel
from model import Cat, User
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI(
    title="first Catapplication fastAPI",
    description="Searching for cats",
    version="0.0.1",
)
app.add_middleware(ErrorHandler)


Base.metadata.create_all(bind=engine)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInBhc3N3b3JkIjoiYWRtaW4ifQ.PqCLn5WclTsjQvky6Ywh_nkj0o2qPVsCWaZ0_RRP_6s


@app.get("/", tags=["index"])
def message():
    return HTMLResponse(
        """<h1>Cats API</h1>
                        <ul>
                         <li>/cats</li> 
                         <li>/cats/1</li> 
                         <li>/cats/?gender=female</li> 
                         <li>/cats/Cat</li> 
                        </ul>"""
    )


@app.get(
    "/cats",
    tags=["cats"],
    response_model=List[Cat],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
def get_cats():
    db = Session()
    res = db.query(CatModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(res))


@app.get("/cats/{id}", tags=["cats"], response_model=Cat)
def get_cat_by_id(id: int = Path(ge=1)):
    db = Session()
    res = db.query(CatModel).filter(CatModel.id == id).first()
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    raise HTTPException(status_code=404, detail="Cat not found")


@app.get("/cats/", tags=["cats"], response_model=List[Cat])  # male/female
def get_cat_by_gender(
    gender: str = Query(min_length=4, max_length=6)
):  # detect parameter query
    db = Session()
    res = db.query(CatModel).filter(CatModel.gender == gender).all()
    if res:
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    return JSONResponse(
        status_code=404, content={"message": "There are no cats of this gender"}
    )


@app.post("/cats/", tags=["cats"])
def create_cat(cat: Cat):
    db = Session()
    new_cat = CatModel(**vars(cat))
    db.add(new_cat)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "New cat added to db"})


@app.put("/cats/{id}", tags=["cats"])
def update_cat(id: int, cat_update: Cat):
    db = Session()
    res = db.query(CatModel).filter(CatModel.id == id).first()
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    res.name = cat_update.name
    res.age = cat_update.age
    res.gender = cat_update.gender
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "The cat info has been updated successfully"},
    )


@app.delete("/cats/{id}", tags=["cats"])
def delete_cat(id: int):
    db = Session()
    res = db.query(CatModel).filter(CatModel.id == id).first()
    if not res:
        return JSONResponse(status_code=404, content={"message": "Cat not found by ID"})
    db.delete(res)
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "The cat has been deleted forever"},
    )


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(vars(user))
        return JSONResponse(status_code=200, content=token)


"""
1) activate env
2) pip install fastapi uvicorn 
3) to run: uvicorn main:app
option --reload --port 8080

pip install pyjwt dotenv
"""
