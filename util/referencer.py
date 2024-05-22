import pandas as pd
import os
from datetime import datetime

def parse_path(file_path: str) -> dict:
    # Ignorer le premier partie de la path
    base_path = "\\\\192.168.130.231\\adv$\\"
    relative_path = file_path.replace(base_path, "")
    
    parts = relative_path.split("\\")
    
    if len(parts) < 5:
        raise ValueError("Path does not conform to the expected structure")

    # Extraire les éléments
    ged = parts[0]
    clients = parts[1]
    dossier = parts[2]
    file_name = parts[-1]
    file_type = file_name.split('.')[-1].upper()
    
    # Extraire la date du nom de fichier
    date_str = file_name.split('.')[0].split(' ')[-1]
    try:
        date = datetime.strptime(date_str, "%d%m%y").strftime("%d/%m/%Y")
    except ValueError:
        date = None
    
    return {
        "GED": ged,
        "CLIENTS": clients,
        "DOSSIER": dossier,
        "FILE_TYPE": file_type,
        "DATE": date
    }

def create_reference_df(file_paths: list) -> pd.DataFrame:
    data = [parse_path(path) for path in file_paths]
    df = pd.DataFrame(data)
    return df

def apply_filter(path_list: list, path_ref_df: pd.DataFrame, filters: dict) -> list:
    df_filtered = path_ref_df.copy()
    
    if "GED" in filters:
        df_filtered = df_filtered[df_filtered['GED'].isin(filters['GED'])]
    
    if "CLIENTS" in filters:
        df_filtered = df_filtered[df_filtered['CLIENTS'].isin(filters['CLIENTS'])]
    
    if "DOSSIER" in filters:
        df_filtered = df_filtered[df_filtered['DOSSIER'].isin(filters['DOSSIER'])]
    
    if "FILE_TYPE" in filters:
        df_filtered = df_filtered[df_filtered['FILE_TYPE'].isin(filters['FILE_TYPE'])]
    
    if "DATE_MIN" in filters:
        date_min = filters["DATE_MIN"]
        if date_min:
            df_filtered = df_filtered[pd.to_datetime(df_filtered['DATE'], format='%d/%m/%Y') >= pd.to_datetime(date_min, format='%d/%m/%Y')]
    
    if "DATE_MAX" in filters:
        date_max = filters["DATE_MAX"]
        if date_max:
            df_filtered = df_filtered[pd.to_datetime(df_filtered['DATE'], format='%d/%m/%Y') <= pd.to_datetime(date_max, format='%d/%m/%Y')]
    
    # Récupérer la liste des chemins filtrés
    filtered_paths = []
    for index, row in df_filtered.iterrows():
        ged = row['GED']
        clients = row['CLIENTS']
        dossier = row['DOSSIER']
        file_type = row['FILE_TYPE']
        date = row['DATE']
        
        for path in path_list:
            if (ged in path and clients in path and dossier in path and file_type in path and (date in path if date else True)):
                filtered_paths.append(path)
    
    return filtered_paths