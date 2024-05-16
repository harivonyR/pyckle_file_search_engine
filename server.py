# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:41:35 2024

@author: harivonyratefiarison
"""

"""

    CONFIGURATION    

"""
# API
from typing import Optional

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ENGINE
from engine.pickle_search import SearchEngine
from util.spliter import path_parse_dict, print_dict_tree,dict_to_html_list
s = SearchEngine()
s.load_existing_index()

# FILE SYSTEM
import aiofiles
import os

# EXTENSION HANDLER
from util.extension import get_extension, get_media_type

"""
    
    ROUTE

"""

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/restatic", response_class=HTMLResponse)
async def read_restatic(request: Request):
    return templates.TemplateResponse("restatic.html", {"request": request})

@app.get("/refresh_index/{id}", response_class=HTMLResponse)
async def refresh_index(request: Request):
    print(f"> refresh triggered on :{id}")
    #s.create_new_index()
    return RedirectResponse(url="/")

@app.post("/search", response_class=HTMLResponse)
async def search_result(request: Request, search_string: str = Form(...), filter: Optional[str] = Form(None)):
    query = search_string
    res,matches,records = s.search_file(query) #FOLDER SEARCH#s.search_dir(query)
    
    # FORMATING RESULT
    res_dict = path_parse_dict(res)
    tree_html  = dict_to_html_list(res_dict,base_path="/view_file/")
    
    return templates.TemplateResponse("result.html", 
                                      {"request": request, 
                                       "search_string": search_string, 
                                       "filter": filter,
                                       "response": tree_html
                                      })

@app.get("/view_file/{file_path:path}", response_class=HTMLResponse)
async def serve_file(request: Request, file_path: str):
    print(f"A file is trigere {file_path}")
    file_path = os.path.join("//", file_path)  # Adjust the base directory accordingly
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    async with aiofiles.open(file_path, 'r') as file:
        #content = await file.read()

        extension = get_extension(file_path)
        media_type = get_media_type(extension)
        
        return FileResponse(file_path, media_type=media_type)
    
    return templates.TemplateResponse("view_file.html", {"request": request, "content": content, "file_path": file_path})
