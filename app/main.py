from typing import Union

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import os

class Result(BaseModel):
    url: str

file_path = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=file_path+ "/static"), name="static")

@app.get("/", response_class=FileResponse)
def read_root():
    html_path = Path(file_path + "/static/index.html")
    return html_path


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/process_job_data")
async def process_job_data(
    request: Request,
    jobtitle: str = Query(...),
    job_function: str = Query(...),
    business_unit: str = Query(...),
    division_department: str = Query(...),
    
) -> Result:
    
    html_path = str(request.url).split("/", 3)[-2] + "/?jobtitle=" + jobtitle + "&job_function=" + job_function  + "&business_unit=" + business_unit + "&division_department=" + division_department
    result = Result(url=html_path)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
