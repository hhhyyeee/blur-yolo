from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shortuuid
import os
import sys
import shutil
from darkflow.apicli import cliHandlerApi

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/yolo")
async def create_upload_file(file: UploadFile = File(...)):
    # 받은 파일을 새이름의 파일로 저장
    filename = shortuuid.uuid() + ".png"
    saveFile = open('./api/' + filename, 'wb+')
    shutil.copyfileobj(file.file, saveFile)
    saveFile.close()

    cliHandlerApi()
    os.remove('./api/' + filename)

    return FileResponse('./api/blur/' + filename)
