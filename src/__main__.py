import os
from code_parser import parse_codebase
from semantic_search import query_codebase

def main():
    db_path = parse_codebase()
    query = input("Query: ")
    response = query_codebase(db_path, query)
    
    return response

if __name__ == "__main__":
    print(main())

'''
similarities = [0.715,  0.674, 0.739, 0.705, 0.761, 0.773,
 0.661, 0.671, 0.770, 0.727, 0.734, 0.738,
 0.671, 0.647, 0.690, 0.690, 0.659,  0.713,
 0.695, 0.707, 0.722, 0.679] 
'''  
    
    