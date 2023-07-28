import os
import ast
import json
import astunparse
from gpt_funcs import code_to_nl
from db_gen import db_gen as create_db


def extract_info(node):
    """
    Extract docstrings and AST dumps for functions and classes.

    Args:
        node (ast.AST): An AST node.

    Returns:
        dict: A dictionary containing natural language description, docstring, AST output, and source code
              if the node is an instance of ast.FunctionDef or ast.ClassDef; None otherwise.
    """
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        docstring = ast.get_docstring(node)
        ast_output = ast.dump(node)
        source_code = astunparse.unparse(node)
        nl_description = code_to_nl(source_code)

        return {
            "nl_description": nl_description,
            "docstring": docstring,
            "ast_output": ast_output,
            "source_code": source_code,
        }


def parse_file(file_path):
    """
    Parse a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing the module docstring and a dictionary of the functions and classes.
    """
    with open(file_path, "r") as file:
        source_code = file.read()

    module = ast.parse(source_code)
    module_docstring = ast.get_docstring(module)

    functions_and_classes = {
        node.name: extract_info(node)
        for node in module.body
        if extract_info(node) is not None
    }

    return {
        "docstring": module_docstring,
        "functions_and_classes": functions_and_classes,
    }


def parse_directory(directory_path):
    """
    Parse a directory.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        dict: A dictionary of the modules parsed from the directory.
    """
    modules = {
        os.path.splitext(filename)[0]: parse_file(
            os.path.join(directory_path, filename)
        )
        for filename in os.listdir(directory_path)
        if filename.endswith(".py")
    }

    return modules


def parse_codebase():
    """
    Parse a codebase.

    This function checks if a workspace exists, prompts the user for the project folder name and
    directory location, creates a JSON file with this information, and creates a SQLite database from
    the JSON file.

    Returns:
        str: The path to the database file.
    """
    workspace = "gpt_workspace"
    if not os.path.exists(workspace):
        os.mkdir(workspace)

    project_folder_name = input("Project folder name: ")
    directory_location = input("Directory location: ")
    json_filename = f"{workspace}/{project_folder_name}-{directory_location}_info.json"
    db_filename = f"{workspace}/{project_folder_name}-{directory_location}_info.db"

    if not os.path.exists(json_filename):
        modules = parse_directory(directory_location)
        data = {project_folder_name: {directory_location: modules}}
        with open(json_filename, "w") as file:
            json.dump(data, file, indent=2)

    if not os.path.exists(db_filename):
        create_db(json_filename, db_filename)

    return db_filename


if __name__ == "__main__":
    parse_codebase()
