import os
import ast
import json
import astunparse
from concurrent.futures import ThreadPoolExecutor
from gpt_funcs import code_to_nl
from db_gen import db_gen as create_db
import asyncio

executor = ThreadPoolExecutor()

async def extract_info(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        docstring = ast.get_docstring(node)
        ast_output = ast.dump(node)
        source_code = astunparse.unparse(node)

        loop = asyncio.get_event_loop()
        nl_description = await loop.run_in_executor(executor, code_to_nl, source_code)

        return {
            "name": node.name,
            "nl_description": nl_description,
            "docstring": docstring,
            "ast_output": ast_output,
            "source_code": source_code,
        }

async def parse_file(file_path):
    with open(file_path, "r") as file:
        source_code = file.read()

    module = ast.parse(source_code)
    module_docstring = ast.get_docstring(module)

    tasks = [
        extract_info(node) for node in module.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    ]

    results = await asyncio.gather(*tasks)

    functions_and_classes = {
        result["name"]: result for result in results
    }

    return {
        "full_path": file_path,
        "docstring": module_docstring,
        "functions_and_classes": functions_and_classes,
    }

async def parse_directory(directory_path):
    tasks = [
        parse_file(os.path.join(directory_path, filename))
        for filename in os.listdir(directory_path)
        if filename.endswith(".py")
    ]

    results = await asyncio.gather(*tasks)

    return {os.path.splitext(filename)[0]: result for filename, result in zip(os.listdir(directory_path), results)}

async def parse_codebase():
    workspace = "gpt_workspace"
    if not os.path.exists(workspace):
        os.mkdir(workspace)

    project_folder_name = input("Codebase Name: ")
    directory_location = input("Full Directory Location: ")
    json_filename = f"{workspace}/{project_folder_name}-{directory_location}_info.json"
    db_filename = f"{workspace}/{project_folder_name}-{directory_location}_info.db"

    if not os.path.exists(json_filename):
        modules = await parse_directory(directory_location)
        data = {project_folder_name: {directory_location: modules}}
        with open(json_filename, "w") as file:
            json.dump(data, file, indent=2)

    if not os.path.exists(db_filename):
        create_db(json_filename, db_filename)

    return db_filename


def parser_main():
    db_filename = asyncio.run(parse_codebase())
    executor.shutdown()
    return db_filename


if __name__ == "__main__":
    parser_main()

