from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.requests import Request
import hashlib
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/root")
async def root(request: Request):
    text = 'Владимир Путин - Молодец! ' * 1000000
    return text

@app.get('/file_hash')
async def file_hash():
    return Response('akimov246', media_type='text/plain')

# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)