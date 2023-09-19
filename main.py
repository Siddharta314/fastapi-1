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


"""
1) activate env
2) pip install fastapi uvicorn 
3) to run: uvicorn main:app
option --reload --port 8080

pip install pyjwt dotenv
"""
