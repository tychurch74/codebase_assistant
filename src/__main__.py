from code_parser import parser_main
from semantic_search import query_codebase
from gpt_funcs import code_helper


def main():
    db_path = parser_main()
    query = input("Query: ")
    context = query_codebase(db_path, query)
    response = code_helper(query, context)
    
    return response


if __name__ == "__main__":
    print(main())


    
    