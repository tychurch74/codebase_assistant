import openai

def code_to_nl(
    input_content, model_temperature=0.1, model="gpt-3.5-turbo"
):
    system_message = {"role": "system", "content": "You are an AI trained by openai to read code and translate what the code does into natural language as well make suggestions on potential improvements to the code. For example the python code `def hello_world(): print('Hello World!')` your response would be `A Python function called hello_world is defined. When the function is called, it prints 'Hello World!' to the console.`. Code may contain newline characters, represented with a backslash followed by the letter n, you can ignore these as they are not a part of the actual code. Keep your responses as short and concise as possible."}
    
    user_message = {"role": "user", "content": input_content}

    response = openai.ChatCompletion.create(
        model=model,
        messages=[system_message, user_message],
        temperature=model_temperature,
    )

    return response["choices"][0]["message"]["content"]


def relevant_context(
    input_content, context, model_temperature=0.1, model="gpt-3.5-turbo-16k"
):
    system_message = {"role": "system", "content": "You are an AI trained by openai to read through a user's query regarding a codebase as well as various pieces of contextual information retrieved from said codebase and return only the pieces of context that could aid in responding to the user's query. This context will include the names of specific functions or classes, a natural language explanation of said functions or classes and the actual source code of said functions or classes. Do not attempt to actually answer the user's query with the context provided, that is the job of the code_helper AI, your response should only include the pieces of context you deem most beneficial to the code_helper AI. Keep your responses as short and concise as possible and include the related full source code for the code_helper AI to see."}
    
    user_message = {"role": "user", "content": f"user query: {input_content}. Which pieces of the following context would be most beneficial to the code_helper AI when answering the user's query?: {context}" }

    response = openai.ChatCompletion.create(
        model=model,
        messages=[system_message, user_message],
        temperature=model_temperature,
    )

    return response["choices"][0]["message"]["content"]


def code_helper(
    input_content, context, model_temperature=0.2, model="gpt-4-0314"
):
    system_message = {"role": "system", "content": f"You are an AI trained by openai to assist users with their codebases. To help inform your responses you will be given relevant context retrieved from the user's codebase. This context will include the name of a specific function or class, a natural language explanation of said function or class and the actual source code of said function or class. If you are unable to answer the user's query with the following context provided you may ask the user for more information. Context: {context}"}
    
    user_message = {"role": "user", "content": input_content}

    response = openai.ChatCompletion.create(
        model=model,
        messages=[system_message, user_message],
        temperature=model_temperature,
    )

    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    
    input_content = "\n\ndef my_function(arg1, arg2):\n    'This is an example function.\\n    \\n    Args:\\n        arg1: The first argument.\\n        arg2: The second argument.\\n    \\n    Returns:\\n        The sum of arg1 and arg2.\\n    '\n    return (arg1 + arg2)\n"

    print(code_to_nl(input_content))


