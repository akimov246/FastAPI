from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*']
)


@app.get('/xmlhttprequest/example/load')
async def load():
    return FileResponse('../3. Fetch. Ход загрузки/video/Polina.mp4', status_code=200)