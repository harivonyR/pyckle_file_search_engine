# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:41:35 2024

@author: harivonyratefiarison
"""


from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_result(request: Request, search_string: str = Form(...), filter: str = Form(...)):
    
    response = "Hi, this is the response"
    return templates.TemplateResponse("result.html", 
                                      {"request": request, 
                                       "search_string": search_string, 
                                       "filter": filter,
                                       "response":response
                                       })
