# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:41:35 2024

@author: harivonyratefiarison
"""

from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

from engine.pickle_search import SearchEngine
from util.spliter import path_parse_dict, print_dict_tree,dict_to_html_list

# INIT
s = SearchEngine()
s.load_existing_index()

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/restatic", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("restatic.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_result(request: Request, search_string: str = Form(...), filter: Optional[str] = Form(None)):
    query = search_string
    res,matches,records = s.search_file(query) #FOLDER SEARCH#s.search_dir(query)
    
    # FORMATING RESULT
    res_dict = path_parse_dict(res)
    print_dict_tree(res_dict)
    tree_html  = dict_to_html_list(res_dict)
    
    return templates.TemplateResponse("result.html", 
                                      {"request": request, 
                                       "search_string": search_string, 
                                       "filter": filter,
                                       "response": tree_html
                                      })

