from fastapi import FastAPI, Form, File, UploadFile, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.requests import Request
from pathlib import Path
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_headers = ['*'],
    allow_methods=["*"]
)

@app.get('/article/xmlhttprequest/example/load')
async def article_xmlhttprequest_example_load():
    return FileResponse('video/Polina.mp4', status_code=200)

@app.get('/article/xmlhttprequest/example/json')
async def article_xmlhttprequest_example_json():
    return {"message": 'Привет, мир!'}

@app.get('/article/xmlhttprequest/{filename}')
async def article_xmlhttprequest_hello_txt(filename: str):
    return FileResponse(f'data/{filename}')

@app.post('/article/xmlhttprequest/post/user')
async def article_xmlhttprequest_post_user(name: str = Form(...), surname: str = Form(...), middle: str = Form(...)):
    return {
        'message': f'Ответ от сервера\nПользователь: "{surname} {name} {middle}" сохранен'
    }

@app.post('/article/xmlhttprequest/post/json')
async def article_xmlhttprequest_post_json(request: Request):
    json = await request.json()
    print(json.get('name'))
    return {
        'message': f'Ответ от сервера\nПользователь: "{json.get("surname")} {json.get("name")}" сохранен'
    }

@app.post('/article/xmlhttprequest/post/upload')
async def article_xmlhttprequest_post_upload(file: UploadFile = File(...)):
    content = await file.read()
    return {
        'filename': file.filename
    }

UPLOAD_DIR = Path('upload')
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get('/article/resume-upload/status')
async def article_resume_upload_status(x_file_id: str = Header(..., alias='X-File-Id')):
    print(x_file_id)
    save_path = UPLOAD_DIR/f'{x_file_id}'
    if save_path.exists():
        return os.path.getsize(save_path)
    else:
        return 0

@app.post('/article/resume-upload/upload')
async def article_resume_upload_upload(
        request: Request,
        x_file_id: str = Header(..., alias='X-File-Id')
):

    save_path = UPLOAD_DIR/f'{x_file_id}'

    mode = 'ab' if save_path.exists() else 'wb'

    try:
        with open(save_path, mode) as f:
            async for chunk in request.stream():
                f.write(chunk)
    except:
        print(f'Something went wrong!\nЗагружено: {os.path.getsize(save_path)}')
        return {
            "status": "aborted",
            "size": os.path.getsize(save_path)
        }

    return {
        "status": "OK",
        "size": os.path.getsize(save_path)
    }
