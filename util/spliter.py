def path_parse_dict(input_paths):
    data = {}
    for path in input_paths:
        parts = path.split("/")
        current_level = data

        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        file_name = parts[-1]
        current_level[file_name] = None

    return data


# PRINT PATH TREE
def print_dict_tree(data_tree, indent=0):
    for key, value in data_tree.items():
        print("  " * indent + "- " + key)
        if isinstance(value, dict):
            print_dict_tree(value, indent + 1)
