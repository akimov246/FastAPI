from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
import fastapi

app = FastAPI()


@app.get('/')
async def root(request: fastapi.requests.Request):
    print(request)

    return JSONResponse({'message': 'Hello World!'})
    #return RedirectResponse('https://vk.com', status_code=301)
    # return HTMLResponse('''
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <b>Пошел нахуй</b>
    #     </body>
    # </html>''')

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}
