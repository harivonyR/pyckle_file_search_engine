# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:41:35 2024

@author: harivonyratefiarison
"""

# CONFIGURATION

# API
from typing import Optional, List

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import quote
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ENGINE
from engine.pickle_search import SearchEngine
from util.spliter import path_parse_dict, print_dict_tree, dict_to_html_list

s = SearchEngine()
s.load_existing_index()

# FILE SYSTEM
import aiofiles
import os

# EXTENSION HANDLER
from util.extension import get_extension, get_media_type

# ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@app.get("/restatic", response_class=HTMLResponse)
async def read_restatic(request: Request):
    return templates.TemplateResponse("restatic.html", {"request": request})

@app.get("/refresh_index", response_class=HTMLResponse)
async def refresh_index(request: Request):
    print(f"> refresh triggered ")
    s.create_new_index(r"//192.168.130.231/adv$/GED")
    s.load_existing_index()
    print(f"> refresh done ")
    return RedirectResponse(url="/")

@app.get("/search")
async def read_home(request: Request):
    s.load_existing_index()
    return templates.TemplateResponse("result.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_result(request: Request, search_string: str = Form(...), filter: Optional[str] = Form(None)):
    query = search_string
    # PERFORM SEARCH
    res, matches, records = s.search_file(query)  # FOLDER SEARCH#s.search_dir(query)
    
    # FILTERING
    
    # FORMATTING RESULT
    res_dict = path_parse_dict(res)
    tree_html = dict_to_html_list(res_dict, base_path="/view_file/")
    
    return templates.TemplateResponse("result.html", 
                                      {"request": request, 
                                       "search_string": search_string, 
                                       "filter": filter,
                                       "response": tree_html
                                      })

@app.post("/search_async", response_class=HTMLResponse)
async def search_result_async(
    request: Request, 
    search_string: str = Form(...), 
    filter_type: List[str] = Form([]), 
    stations_dropdown: Optional[str] = Form(None), 
    clients_dropdown: Optional[str] = Form(None)
):
    query = search_string

    # Perform search
    res, matches, records = s.search_file(query)

    # Apply filters if any
    # Format result
    res_dict = path_parse_dict(res)
    tree_html = dict_to_html_list(res_dict, base_path="/view_file/")

    return tree_html

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
'''
# to implement
@app.get("/client/{client_name:str}", response_class=HTMLResponse)
async def get_client(request: Request, client_name:str):
    base_path = get_client_path(client_name)
    res = get_file(base_path)

@app.get("/station/{station_name:str}", response_class=HTMLResponse)
'''