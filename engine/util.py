import os
import pickle

def get_child(base_path):
    base_path = base_path.replace("\\", "/")
    child_dirs = set()  # Utilisation d'un set pour éviter les doublons

    try:
        with open('engine/file_index.pkl', 'rb') as f:
            file_index = pickle.load(f)
        print("Index loaded!")
    except FileNotFoundError:
        print("Error: The file 'engine/file_index.pkl' was not found.")
        return []
    except pickle.UnpicklingError:
        print("Error: The file 'engine/file_index.pkl' could not be unpickled.")
        return []
    
    for paths, dirs, files in file_index:
        normalized_path = paths.replace("\\", "/")
        if normalized_path.startswith(base_path):
            relative_path = normalized_path[len(base_path):].strip("/")
            if "/" not in relative_path:
                child_dirs.add(normalized_path)
    
    return list(child_dirs)

def path_to_dict(paths):
    path_dict = {}
    for path in paths:
        key = os.path.basename(path)  # Le dernier segment du chemin
        path_dict[key] = path
    return path_dict

# Serve client list
def get_client_list():
    client_base_path = r"//192.168.130.231/adv$/GED/CLIENTS"
    client_paths = get_child(client_base_path)
    return path_to_dict(sorted(client_paths))

def get_file_list(base_path, level=[1]):
    return []

# Serve station list
def get_station_list():
    return []

if __name__ == "__main__":
    clients = get_client_list()
    for client, path in clients.items():
        print(f"Client: {client}, Path: {path}")

'''
    filter : station/client, 
    base_path, level, folder, file, file_type

    result : full_path, folder, name

'''
