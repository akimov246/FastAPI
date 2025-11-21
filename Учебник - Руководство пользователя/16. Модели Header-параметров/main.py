from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


class CommonHeadersExtraForbid(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers


@app.get("/items/extra_forbid")
async def read_items(headers: Annotated[CommonHeadersExtraForbid, Header()]):
    return headers


@app.get("/items/underscored")
async def read_items(headers: Annotated[CommonHeaders, Header(convert_underscores=False)]):
    return headers