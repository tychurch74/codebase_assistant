# Codebase_Assistant
Collection of Python scripts that parses entire codebases, creates highly detailed descriptions of every class or function along with a high level overview of the structure and purpose of the codebase, and uses that information to provide specific, tailored assistance via GPT without the need for copy and pasting the code in question, simply just state the name of the function, class or script you want assistance with.

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
1. Clone the repository
2. Install the requirements.txt file
3. Make sure you have a valid OpenAI API key and set it as an environment variable, instructions can be found here: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
4. Run the src/__main.py__ file
5. Follow the instructions in the terminal, make sure to specify the correct full directory location of the codebase you want assistance with.

## Optional setup
1. You can change the default GPT-3.5-Turbo model that is used to generate the descriptions by changing the model name in the src/gpt_funcs.py file.You can also change the default GPT-4 model that is used to generate the system messages by changing the model name within the same file.

## How it works
1. The program parses the entire codebase and creates a dictionary of every function and class in the codebase (see codebase_info_template.json to see the basic structure).
2. Using GPT-3.5-Turbo the program generates a natural language description along with potential improvements of each and every class or function in the codebase.
3. This data is then saved to a JSON file and a SQL database.
4. Using OpenAI's embeddings API the program generates a vector representation of the user's query and compares it to the vector representations of the descriptions, names and source code of each function and class in the codebase. The most contextually relevant functions or classes that fit within GPT-4's context window are then returned and used as context in a GPT-4 system message.

## Future improvements
1. Add support for parsing other languages such as Java, C++, C#, JavaScript, etc.
2. Add functionality inspired by gpt_engineer to allow for the generation of full script files.
3. Add functionality to allow for the parsing of github reposistories not locally cloned.
4. Add functionality to allow for the code interpreting and debugging of scripts.



