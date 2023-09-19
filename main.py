"""
FastAPI application with sqlAlchemy
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.cat import cat_router
from routers.user import user_router


app = FastAPI(
    title="first Catapplication fastAPI",
    description="Searching for cats",
    version="0.0.1",
)
app.add_middleware(ErrorHandler)
app.include_router(cat_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["index"])
def message():
    """Webpage for the URL http://127.0.0.1:8000 if running locally."""
    return HTMLResponse(
        """<h1>Cats API</h1>
                        <ul>
                        <li>/docs</li> 
                        <li>/cats/1</li> 
                        <li>/cats/?gender=female</li> 
                        </ul>"""
    )
