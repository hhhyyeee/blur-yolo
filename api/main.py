from typing import Optional
from fastapi import FastAPI, File, UploadFile
import sys
from darkflow.cli import cliHandler_api

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/yolo")
def read_root(): # 파라미터 핸들링 어케하냐
    cliHandler_api(sys.argv)