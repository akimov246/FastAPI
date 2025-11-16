from typing import Annotated

from fastapi import FastAPI, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Cookies(BaseModel):
    model_config = {'extra': 'forbid'}

    session_id: str | None = None
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()], response: Response):
    response.set_cookie(
        key="session_id",
        value="session_id_value",
        max_age=5,
        samesite="none",
        secure=True
    )
    response.set_cookie(
        key="fatebook_tracker",
        value="fatebook_tracker_value",
        max_age=5,
        samesite="none",
        secure=True
    )
    response.set_cookie(
        key="googall_tracker",
        value="googall_tracker_value",
        max_age=5,
        samesite="none",
        secure=True
    )
    response.set_cookie(
        key="santa_tracker",
        value="good-list-please",
        max_age=2,
        samesite="none",
        secure=True
    )
    return cookies