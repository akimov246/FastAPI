from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:63342',
        'http://localhost:8000',
        'http://127.0.0.1:8000'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItemList(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


@app.put("/items/list/{item_id}")
async def update_item(item_id: int, item: ItemList):
    results = {"item_id": item_id, "item": item}
    return results


class ItemListStr(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.put("/items/list_str/{item_id}")
async def update_item(item_id: int, item: ItemListStr):
    results = {"item_id": item_id, "item": item}
    return results


class ItemSetStr(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.put("/items/set_str/{item_id}")
async def update_item(item_id: int, item: ItemSetStr):
    results = {"item_id": item_id, "item": item}
    return results


class Image(BaseModel):
    url: HttpUrl
    name: str


class ItemWithImage(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/item_with_image/{item_id}")
async def update_item(item_id: int, item: ItemWithImage):
    results = {"item_id": item_id, "item": item}
    return results


class ItemWithImages(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


@app.put("/items/item_with_images/{item_id}")
async def update_item(item_id: int, item: ItemWithImages):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/index-weights")
async def create_index_weights(weights: dict[int, float]):
    return weights