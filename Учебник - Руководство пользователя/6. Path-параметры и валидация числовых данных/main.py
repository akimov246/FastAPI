from typing import Annotated

from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items/ge/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/gtle/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/float/{item_id}")
async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
        q: str,
        size: Annotated[float, Query(gt=0, lt=10.5)]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None
 ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results