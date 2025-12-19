from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
        q: Annotated[str | None, Depends(query_extractor)] = None,
        last_query: Annotated[str | None, Cookie()] = None
):
    if not q:
        return last_query
    return q


@app.get("/items")
async def read_query(
        response: Response,
        query_or_default: Annotated[str | None, Depends(query_or_cookie_extractor)] = None
):
    response.set_cookie(
        key='last_query',
        value='Last Query from Cookies',
        max_age=5,
        samesite='none',
        secure=True
    )
    return {"q_or_cookie": query_or_default}