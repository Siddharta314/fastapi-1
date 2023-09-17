from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from model import Cat
from db import cats

app = FastAPI(
    title="first Catapplication fastAPI",
    description="Searching for cats",
    version="0.0.1",
)


@app.get("/", tags=["home"])
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


@app.get("/cats", tags=["cats"], response_model=List[Cat])
def get_cats():
    return JSONResponse(content=cats)


@app.get("/cats/{id}", tags=["cats"], response_model=Cat)
def get_cat(id: int = Path(ge=1)):
    for cat in cats:
        if cat["id"] == id:
            return cat
    raise HTTPException(status_code=404, detail="Cat missing")


@app.get("/cats/", tags=["cats"], response_model=List[Cat])  # male/female
def get_cat_by_gender(
    gender: str = Query(min_length=4, max_length=6)
):  # detect parameter query
    cat_by_gender = [cat for cat in cats if cat["gender"] == gender]
    return JSONResponse(content=cat_by_gender)


@app.post("/cats/", tags=["cats"])
def create_cat(cat: Cat):
    cats.append(cat)
    return cats


@app.put("/cats/{id}", tags=["cats"])
def update_cat(id: int, cat_update: Cat):
    for cat in cats:
        if cat["id"] == id:
            cat["name"] = cat_update.name
            cat["age"] = cat_update.age
            cat["gender"] = cat_update.gender
            return cats


@app.delete("/cats/{id}", tags=["cats"])
def delete_cat(id: int):
    for cat in cats:
        if cat["id"] == id:
            cats.remove(cat)
    return cats


"""
to run terminal: uvicorn main:app
option --reload --port 8080
Another Way
app = FastAPI(
    title= 'First application fastAPI',
    description= 'Exploring fastAPI',
    version= '0.0.1',
)

"""
