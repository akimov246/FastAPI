from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
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


data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield 'Rick'
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item


class InternalErrorWithoutRaise(Exception):
    pass


def get_username_without_raise():
    try:
        yield 'Rick'
    except InternalErrorWithoutRaise:
        print("Oops, we didn't raise again, Britney")


@app.get("/items/without_raise/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username_without_raise)]):
    if item_id == 'portal-gun':
        raise InternalErrorWithoutRaise(f"The portal gun is too dangerous to be owned by {username}")
    if item_id != 'plumbus':
        raise HTTPException(status_code=404, detail="Item not found, there's only a plumbus here")
    return item_id


class InternalErrorWithRaise(Exception):
    pass


def get_username_with_raise():
    try:
        yield 'Rick'
    except InternalErrorWithRaise:
        print("We don't swallow the internal error here, we raise again")
        raise


@app.get("/items/with_raise/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username_with_raise)]):
    if item_id == 'portal-gun':
        raise InternalErrorWithRaise(f"The portal gun is too dangerous to be owned by {username}")
    if item_id != 'plumbus':
        raise HTTPException(status_code=404, detail="Item not found, there's only a plumbus here")
    return item_id