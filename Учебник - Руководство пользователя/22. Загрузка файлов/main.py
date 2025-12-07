from typing import Annotated

from fastapi import FastAPI, File, UploadFile
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


@app.post("/file")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile")
async def create_upload_file(file: Annotated[UploadFile | None, File(description="A file read as UploadFile")] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@app.post("/files")
async def create_files(files: Annotated[list[bytes], File(description="Multiple files as bytes")]):
    return {"size_files": [len(file) for file in files]}


@app.post("/uploadfiles")
async def create_upload_files(files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]):
    return {"filenames": [file.filename for file in files]}