from enum import Enum

from fastapi import FastAPI, status
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


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create an item",
    response_description="The created item"
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


class Tags(Enum):
    items = 'items'
    users = 'users'


@app.get("/items_with_enum_tag", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users_with_enum_tag", tags=[Tags.users])
async def get_users():
    return ["Rick", "Morty"]


@app.get("/elements", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]