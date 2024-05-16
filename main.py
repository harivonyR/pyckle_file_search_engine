# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:07:31 2024

@author: harivonyratefiarison
"""

from engine.pickle_search import SearchEngine
from util.spliter import path_parse_dict, print_dict_tree,dict_to_html_list

# INIT
s = SearchEngine()
# only create index once
#s.create_new_index(r"C:\Users\harivonyratefiarison\3_script traitement\pickle_engine\engine\file_index.pkl")
s.load_existing_index()
status = "Y"

while(status=="Y"):
    # SEARCH
    query = input("> Enter your query :")
    
    res,matches,records = s.search_file(query) #FOLDER SEARCH#s.search_dir(query)
    
    # FORMATING RESULT
    res_dict = path_parse_dict(res)
    print_dict_tree(res_dict)
    tmp_html = dict_to_html_list(res_dict)
    
    print()
    print("------------------------------------------")
    status = input("Continue ? (Y/N) :")
    
    

