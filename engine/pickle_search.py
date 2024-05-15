# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:13:58 2024

@author: harivonyratefiarison
@credit: israel-dryer

File SEARCH ENGINE USING pickle

"""

import os 
import pickle

class SearchEngine:
    def __init__(self):
        self.file_index = [] 
        self.results_file = []
        self.results_folder = []
        self.matches = 0
        self.records = 0
        
    def create_new_index(self, root_path):
        ''' create a new index and save to file '''
        self.file_index = [(root,dirs,files) for root, dirs, files in os.walk (root_path) if files]
       
        # save to file
        with open('engine/file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)
    
    def load_existing_index(self):
        ''' load existing index '''
        try:
            with open('engine/file_index.pkl', 'rb') as f: self.file_index = pickle.load(f)
            print("index loaded !")
        except:
            self.file_index = []
            print("index file not found")
            
    def search_file(self, term, search_type = 'contains'): 
        ''' search for term based on search type '''
        # reset variables
        self.results_file.clear()
        res = []
        matches = 0
        records = 0
        
        for path, dirs, files in self.file_index:
            for file in files:
                records += 1
                if (
                    search_type == "contains"
                    and term.lower() in file.lower()
                    or search_type == "startswith"
                    and file.lower().startswith(term.lower())
                    or search_type == "endswith"
                    and file.lower().endswith(term.lower())
                ):
                    result = path.replace("\\", "/") + "/" + file
                    #self.results_file.append(result)
                    res.append(result)
                    matches+=1
                else:
                    continue

        return res,matches,records
    

    # todo : match method with search_file            
    def search_dir(self, term, search_type = 'contains'): 
        ''' search for term based on search type '''
        # reset variables
        self.results_folder.clear()
        self.matches = 0
        self.records = 0
        
        for path, dirs, files in self.file_index:
            for folder in dirs:
                self.records += 1
                if (
                    search_type == "contains"
                    and term.lower() in folder.lower()
                    or search_type == "startswith"
                    and folder.lower().startswith(term.lower())
                    or search_type == "endswith"
                    and folder.lower().endswith(term.lower())
                ):
                    result = path.replace("\\", "/") + "/" + folder
                    self.results_folder.append(result)
                    self.matches+=1
                else:
                    continue

        # save search results
        with open('folder_results.tx','w') as f:
            for row in self.results_folder:
                f.write(row + '\n')
'''
    def print_result(self,result_type="file"):
        if result_type == "file" :
            print()
            print('>> RESULTS FILE : \n')
            for match in self.results_file:
                print(match)
                
        if result_type=="folder" :
            print()
            print('>> RESULTS FILE : \n')
            for match in self.results_folder:
                print(match)
                
    def print_result_stat(self) :
        print()
        print(
            '>> {:,d} match ou of  {:,d} reccrds'.format(
                self.matches, self.records
            )
        )


# OPTIMIZATION
# rechercher aussi dans path
# 
'''