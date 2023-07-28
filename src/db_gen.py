import json
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Create a database connection to a SQLite database.

    Args:
        db_file (str): Path to the database file.

    Returns:
        Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None


def create_tables(conn):
    """
    Create tables in the SQLite database.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
    """
    try:
        cursor = conn.cursor()

        tables = [
            """
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE folders (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                project_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            );
            """,
            """
            CREATE TABLE files (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                docstring TEXT,
                folder_id INTEGER,
                FOREIGN KEY(folder_id) REFERENCES folders(id)
            );
            """,
            """
            CREATE TABLE functions_classes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                nl_description TEXT,
                docstring TEXT,
                ast_output TEXT,
                source_code TEXT,
                file_id INTEGER,
                FOREIGN KEY(file_id) REFERENCES files(id)
            );
            """,
        ]

        for table in tables:
            cursor.execute(table)
    except Error as e:
        print(e)


def parse_json_insert_data(conn, json_file_path):
    """
    Parse JSON data and insert it into the SQLite database.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        json_file_path (str): Path to the JSON file containing the data.
    """
    with open(json_file_path, "r") as f:
        data = json.load(f)

    cursor = conn.cursor()

    for project_name, folders in data.items():
        cursor.execute("INSERT INTO projects(name) VALUES(?)", (project_name,))
        project_id = cursor.lastrowid

        for folder_name, files in folders.items():
            cursor.execute(
                "INSERT INTO folders(name, project_id) VALUES(?, ?)",
                (folder_name, project_id),
            )
            folder_id = cursor.lastrowid

            for file_name, file_contents in files.items():
                docstring = file_contents.get("docstring")
                cursor.execute(
                    "INSERT INTO files(name, docstring, folder_id) VALUES(?, ?, ?)",
                    (file_name, docstring, folder_id),
                )
                file_id = cursor.lastrowid

                for function_name, function_contents in file_contents.get(
                    "functions_and_classes", {}
                ).items():
                    nl_description = function_contents.get("nl_description")
                    docstring = function_contents.get("docstring")
                    ast_output = function_contents.get("ast_output")
                    source_code = function_contents.get("source_code")

                    cursor.execute(
                        """
                        INSERT INTO functions_classes(name, nl_description, docstring, ast_output, source_code, file_id) 
                        VALUES(?, ?, ?, ?, ?, ?)
                        """,
                        (
                            function_name,
                            nl_description,
                            docstring,
                            ast_output,
                            source_code,
                            file_id,
                        ),
                    )

    conn.commit()


def query_function_class(
    conn, project_name, folder_name, file_name, function_class_name
):
    """
    Query a function or class from the SQLite database.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        project_name (str): Name of the project.
        folder_name (str): Name of the folder.
        file_name (str): Name of the file.
        function_class_name (str): Name of the function or class.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            f_c.name, 
            f_c.nl_description, 
            f_c.docstring, 
            f_c.ast_output, 
            f_c.source_code 
        FROM functions_classes f_c
        JOIN files f ON f_c.file_id = f.id
        JOIN folders fo ON f.folder_id = fo.id
        JOIN projects p ON fo.project_id = p.id
        WHERE 
            f_c.name = ? AND
            f.name = ? AND
            fo.name = ? AND
            p.name = ?
        """,
        (function_class_name, file_name, folder_name, project_name),
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)


def db_gen(json_file_path, db_file_path):
    """
    Generate a SQLite database from a JSON file.

    Args:
        json_file_path (str): Path to the JSON file.
        db_file_path (str): Path to the SQLite database file.
    """
    conn = create_connection(db_file_path)
    if conn is not None:
        create_tables(conn)
        parse_json_insert_data(conn, json_file_path)


def test_db_gen(json_file_path, db_file_path):
    """
    Test the generation of a SQLite database from a JSON file.

    Args:
        json_file_path (str): Path to the JSON file.
        db_file_path (str): Path to the SQLite database file.
    """
    conn = create_connection(db_file_path)
    if conn is not None:
        create_tables(conn)
        parse_json_insert_data(conn, json_file_path)
        query_function_class(
            conn, "codebase_assistant", "src", "parser", "extract_info"
        )


if __name__ == "__main__":
    db_gen("codebase_info.json", "codebase_info.db")
