from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
    x_token: Annotated[str | None, Header()] = None
):
    if x_token:
        x_token = x_token.split(', ')
    return {"User-Agent": user_agent, "strange_header": strange_header, "x_token values": x_token}