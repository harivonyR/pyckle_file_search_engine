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
        self.file_index = [(root, dirs, files) for root, dirs, files in os.walk(root_path) if files]

        # save to file
        with open('engine/file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        ''' load existing index '''
        try:
            with open('engine/file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
            print("Index loaded!")
        except:
            self.file_index = []
            print("Index file not found")

    def search_file(self, term, search_type='contains'):
        ''' search for term based on search type '''
        # reset variables
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
                    res.append(result)
                    matches += 1
                else:
                    continue

        return res, matches, records

    def search_dir(self, term, search_type='contains'):
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
                    self.matches += 1
                else:
                    continue

        # save search results
        with open('folder_results.txt', 'w') as f:
            for row in self.results_folder:
                f.write(row + '\n')

    def search_in_path(self, term, search_type='startswith'):
        ''' search for files where the path matches the term based on search type '''
        res = []
        matches = 0
        records = 0

        for path, dirs, files in self.file_index:
            normalized_path = path.replace("\\", "/")
            records += 1
            if (
                search_type == "contains"
                and term.lower() in normalized_path.lower()
                or search_type == "startswith"
                and normalized_path.lower().startswith(term.lower())
                or search_type == "endswith"
                and normalized_path.lower().endswith(term.lower())
            ):
                for file in files:
                    result = normalized_path + "/" + file
                    res.append(result)
                    matches += 1
            else:
                continue
        
        return res, matches, records

if __name__ == "__main__":
    engine = SearchEngine()
    engine.load_existing_index()
    search_term = "//192.168.130.231/adv$/GED/CLIENTS/SMTP"
    results, matches, records = engine.search_in_path(search_term)
    for result in results:
        print(result)
    print(f"Matches: {matches}, Records: {records}")
