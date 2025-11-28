from typing import Any

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://localhost:8080",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


@app.post("/items/with_response_model", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/with_response_model", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/in")
async def create_user(user: UserIn) -> UserIn:
    return user


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/out", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class BaseUserIn(BaseUser):
    password: str


@app.post("/user")
async def create_user(user: BaseUserIn) -> BaseUser:
    return user


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="http://127.0.0.1:8000/docs")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="http://127.0.0.1:8000/docs")


@app.get("/portal/response_model_none", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="http://127.0.0.1:8000/docs")
    return {"message": "Here's your interdimensional portal."}


class ItemWithDefaultTax(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=ItemWithDefaultTax, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


class ItemWithoutTags(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items_without_tags = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get("/items/{item_id}/name", response_model=ItemWithoutTags, response_model_include={"name", "description"})
async def read_item_name(item_id: str):
    return items_without_tags[item_id]


@app.get("/items/{item_id}/public", response_model=ItemWithoutTags, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items_without_tags[item_id]