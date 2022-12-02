from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil
import keras
import keras.models
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image

app = FastAPI()

templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/json", StaticFiles(directory="json"), name="json")

model_file_name='..\IA\models\\type_fire-water_finder.h5'
model = keras.models.load_model(model_file_name)
# recuper la page index dans le dossier templates
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

#recuper variable mis dans le formulaire : 
@app.post("/submitform")
async def handle_form(user_image: UploadFile = File(...)):
    with open("buffer", "wb") as buffer:
        shutil.copyfileobj(user_image.file, buffer)
        img=Image.open(user_image.file)
        img.save(user_image.filename)
        img.show(user_image.filename)
        try:
            class_probabilities = model.predict(img) # ERROR here
            predictions = np.argmax(class_probabilities, axis=1)
            print(predictions)
        except IndexError as e:
            # return {"error":e}
            return {"filename" : user_image.filename, "Content_type": user_image.content_type, "file":user_image.file}
    # return {"predi": predictions}
  


# @app.post("/submitform", response_class=HTMLResponse)
# async def read_item(request: Request,  ):
#     return templates.TemplateResponse("index.html",{"request": request})

if __name__ == '__main__':
    uvicorn.run(app) 
   
#port='8080',host='0.0.0.0'