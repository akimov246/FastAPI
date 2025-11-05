from typing import Annotated, Literal

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: Annotated[int, Field(gt=0, le=100)] = 100
    offset: Annotated[int, Field(ge=0)] = 0
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query