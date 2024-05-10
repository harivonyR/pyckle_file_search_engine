# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:07:31 2024

@author: harivonyratefiarison
"""

from engine.pickle_search import SearchEngine
from util.spliter import path_parse_dict, print_dict_tree

# INIT
s = SearchEngine()
# only create index once
#s.create_new_index(r"C:\Users\harivonyratefiarison\0_dev_eurodata")
s.load_existing_index()
status = "Y"

while(status=="Y"):
    # SEARCH
    query = input("> Enter your query :")
    s.search_file(query)
    #s.print_result(result_type="file")
    
        #FOLDER SEARCH
    #s.search_dir(query)
    
    # FORMATING RESULT
    res_dict = path_parse_dict(s.results_file)
    print_dict_tree(res_dict)
    print()
    print("------------------------------------------")
    status = input("Continue ? (Y/N) :")
    
    

