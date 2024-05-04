from fastapi import FastAPI
from api import token_apis
from database import Base, engine


def start_app():

    fastapi_app = FastAPI(
        title="JWT demo",
        description="This app is to learn on how resouce access using JWT token",
        summary="Token services like JWT token creation, validation etc.",
        version="0.0.1",
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        contact={
            "name": "Rishabh Kumar",
            "email": "rishabh.kumar94@outlook.com",
        },
    )
    return fastapi_app


Base.metadata.create_all(bind=engine)
app = start_app()


app.include_router(token_apis.router)
