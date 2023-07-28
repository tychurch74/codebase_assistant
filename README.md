# Codebase_Assistant
python program that parses entire codebases and provides assistance via GPT

## Example output
```
Project folder name: codebase_assistant
Directory location: ex_codebase
Query: what does the extract_info function do?
The `extract_info` function takes an Abstract Syntax Tree (AST) node as an input and checks if the node is an instance of either `ast.FunctionDef` or `ast.ClassDef`. If it is, the function extracts the following information:

1. Docstring: The documentation string associated with the function or class.
2. AST output: A string representation of the AST node.
3. Source code: The source code of the function or class, reconstructed from the AST node.
4. Natural language description: A human-readable description of the source code.

The function then returns a dictionary containing these values. If the input node is not an instance of `ast.FunctionDef` or `ast.ClassDef`, the function returns `None`.
```

## Setup
