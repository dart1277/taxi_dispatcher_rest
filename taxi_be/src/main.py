from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from infrastructure.api.routers.routers_config import add_routers
from infrastructure.config.cors import add_middleware
from infrastructure.config.exceptions import main_exception_handler
from infrastructure.config.lifespan import app_lifespan
from infrastructure.config.settings import settings

app = FastAPI(
    lifespan=app_lifespan
)


@app.get("/")
def version():
    return {"message": f'{settings.hostname}'}


add_middleware(app)
add_routers(app)


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request: Request, exc: RequestValidationError):
    return await main_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await main_exception_handler(request, exc)


@app.exception_handler(Exception)
async def app_exception_handler(request: Request, exc: Exception):
    return await main_exception_handler(request, exc)

# fastapi dev --reload src/main.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
