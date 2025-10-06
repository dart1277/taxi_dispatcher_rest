from fastapi.middleware.cors import CORSMiddleware

# TODO load from base settings
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",

]


def add_middleware(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
    )
