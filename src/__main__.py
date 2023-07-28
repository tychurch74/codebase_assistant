from code_parser import parse_codebase
from semantic_search import query_codebase

def main():
    db_path = parse_codebase()
    query = input("Query: ")
    response = query_codebase(db_path, query)
    
    return response

if __name__ == "__main__":
    print(main())
    
    
    