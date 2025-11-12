import random

from typing import Annotated
from string import ascii_uppercase

from fastapi import FastAPI, Cookie, Response, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:63342',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(r: Request, response: Response, ads_id: Annotated[str | None, Cookie()] = None):
    if not ads_id:
        response.set_cookie(
            key="ads_id",
            value=str(random.randint(1, 9)) + random.choice(ascii_uppercase),
            max_age=5,
            samesite='none',
            secure=True
        )
    return {"ads_id": ads_id}