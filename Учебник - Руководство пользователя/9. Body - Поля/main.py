from typing import Annotated

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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


class Item(BaseModel):
    name: str
    description: Annotated[str | None, Field(title="The description of the item", max_length=300)] = None
    price: Annotated[float, Field(gt=0, description="The price must be greater than zero")]
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results