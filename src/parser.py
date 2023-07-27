
import ast
import astunparse
import json
import os
from gpt_funcs import code_to_nl
from db_gen import main as create_db

# Define a function to extract docstrings and AST dumps for functions and classes.
def extract_info(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        docstring = ast.get_docstring(node)
        ast_output = ast.dump(node)
        source_code = astunparse.unparse(node)
        nl_desription = code_to_nl(source_code)
        return {"nl_description": nl_desription, "docstring": docstring, "ast_output": ast_output, "source_code": source_code}
    else:
        return None

# Define a function to parse a Python file.
def parse_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    module = ast.parse(source_code)
    module_docstring = ast.get_docstring(module)

    functions_and_classes = {}
    for node in module.body:
        info = extract_info(node)
        if info is not None:
            functions_and_classes[node.name] = info

    return {"docstring": module_docstring, "functions_and_classes": functions_and_classes}

# Define a function to parse a directory.
def parse_directory(directory_path):
    modules = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.py'):
            file_path = os.path.join(directory_path, filename)
            module_name = os.path.splitext(filename)[0]
            modules[module_name] = parse_file(file_path)
    return modules

if __name__ == '__main__':
    # Parse the directory and write the result to a .json file.
    if not os.path.exists('gpt_workspace'):
        os.mkdir('gpt_workspace')

    project_folder_name = "codebase_assistant"
    directory_location = "src"
    modules = parse_directory(directory_location)

    data = {project_folder_name: {directory_location: modules}}

    with open(f'gpt_workspace/{project_folder_name}-{directory_location}_info.json', 'w') as file:
        json.dump(data, file, indent=2)

    # Create a database from the .json file.
    create_db(f'gpt_workspace/{project_folder_name}-{directory_location}_info.json', f'gpt_workspace/{project_folder_name}-{directory_location}_info.db')

    
