from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil

app = FastAPI()

templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/json", StaticFiles(directory="json"), name="json")

# recuper la page index dans le dossier templates
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

#recuper variable mis dans le formulaire : 
@app.post("/submitform")
async def handle_form(user_image: UploadFile = File(...)):
    with open("test", "wb") as buffer:
        shutil.copyfileobj(user_image.file, buffer)
    return {"filename" : user_image.filename, "Content_type": user_image.content_type, "file":user_image.file}
  


# @app.post("/submitform", response_class=HTMLResponse)
# async def read_item(request: Request,  ):
#     return templates.TemplateResponse("index.html",{"request": request})

if __name__ == '__main__':
    uvicorn.run(app) 
   
#port='8080',host='0.0.0.0'