from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from cats import cats


app = FastAPI()
# Making changes to the docs
app.title = "first application fastAPI"
app.version = "0.0.1"


"""
Another Way
app = FastAPI(
    title= 'first application fastAPI',
    description= 'Una API solo por diversión',
    version= '0.0.1',
)
"""


@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Title</h1>")


@app.get("/cats", tags=["cats"])
def get_cats():
    return cats


# to run terminal: uvicorn main:app
# option --reload --port 5000
