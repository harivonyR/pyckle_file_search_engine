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


def dict_to_html_list(data_tree, base_path="", level=0):
    html = f'<ul class="level-{level}">'
    for key, value in data_tree.items():
        full_path = f"{base_path}/{key}".strip("/")
        if value is None:
            html += f'<li class="level-{level} file"><a href="{full_path}">{key}</a></li>'
        else:
            html += f'<li class="level-{level} folder">{key}{dict_to_html_list(value, full_path, level + 1)}</li>'
    html += "</ul>"
    return html