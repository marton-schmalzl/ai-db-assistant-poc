import mysql.connector
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(debug=False):
    db_host = input("Enter MySQL Host (default: localhost): ") or "localhost"
    db_user = input("Enter MySQL User (default: root): ") or "root"
    db_password = input("Enter MySQL Password (default: root): ") or "root"
    db_name = input("Enter MySQL Database Name (default: mydb): ") or "mydb"

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            if debug:
                schema = get_db_schema(conn)
                if schema:
                    print("\nDatabase Schema (Debug Mode):")
                    print(schema)
            return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_db_schema(conn):
    cursor = conn.cursor()
    sql_schema = ""
    try:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        sql_schema += f"-- MySQL Version: {version}\n\n"

        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        for table_name in tables:
            sql_schema += f"-- Table: {table_name}\n"
            sql_schema += f"CREATE TABLE {table_name} (\n"
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            column_definitions = []
            for col in columns:
                column_name = col[0]
                column_type = col[1]
                column_definitions.append(f"    {column_name} {column_type}")
            sql_schema += ",\n".join(column_definitions)
            sql_schema += "\n)";

            # Fetch foreign keys for the current table
            cursor.execute(f"""
                SELECT
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME,
                    COLUMN_NAME,
                    CONSTRAINT_NAME
                FROM
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE
                    TABLE_NAME = '{table_name}'
                    AND REFERENCED_TABLE_NAME IS NOT NULL;
            """)
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                sql_schema += " ADD CONSTRAINT"
                for fk in foreign_keys:
                    ref_table_name, ref_column_name, column_name, constraint_name = fk
                    sql_schema += f"""\n    CONSTRAINT {constraint_name}
    FOREIGN KEY ({column_name}) REFERENCES {ref_table_name}({ref_column_name}),"""
                sql_schema = sql_schema.rstrip(',') + "\n)"; # Remove trailing comma and add closing parenthesis
            else:
                sql_schema += "\n)";
            sql_schema += ";\n\n"
        return sql_schema
    except mysql.connector.Error as e:
        print(f"Error reading database schema: {e}")
        return None
    finally:
        cursor.close()

def generate_sql_query(prompt, schema, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt_content = f"""
    **IMPORTANT and CRITICAL INSTRUCTION**: Generate a valid SQL query with comments to answer the question based **EXCLUSIVELY** on the provided database schema.
    Your SQL query **MUST ONLY** use tables and columns that are **explicitly defined** in the provided schema.
    **ABSOLUTELY DO NOT** use any tables or columns that are **NOT** present in the schema.
    If the schema does not contain the necessary tables or columns to answer the question, then return a comment saying "Schema does not contain necessary columns or tables to answer question."
    Ensure that all information is retrieved from the **correct tables** as defined in the schema. Use JOINs only when necessary and explicitly indicated by relationships within the schema.
    It is **ABSOLUTELY CRUCIAL** to pay meticulous attention to the schema and column names. 
    **Column names are case-sensitive**. Your generated SQL query **MUST ALSO BE case-sensitive** and accurately reflect the schema's case.
    To reiterate, **UNDER NO CIRCUMSTANCES** should you invent or assume the existence of tables or columns that are not in the provided schema.
    Return **ONLY** the raw SQL query, without any markdown wrappers, as plain text.

    Database Schema:
    {schema}

    Question:
    {prompt}

    SQL Query:
    """

    response = model.generate_content(prompt_content)
    # Strip markdown formatting
    sql_query = response.text
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query

def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return results, column_names
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None, None
    finally:
        cursor.close()

def ask_yes_no_question(question, default_answer=True):
    valid_answers = {'yes': True, 'y': True, 'no': False, 'n': False}
    default_str = 'Y' if default_answer else 'N'
    prompt_options = f"([{default_str.upper()}]/{'n'.lower()})" if default_answer else f"([{default_str.lower()}]/{'y'.lower()})"

    while True:
        answer = input(f"{question} {prompt_options}: ")
        if not answer:
            return default_answer
        if answer.lower() in valid_answers:
            return valid_answers[answer.lower()]
        else:
            print("Please answer 'yes' or 'no'.")

def main():
    conn = get_db_connection(debug=True)
    if not conn:
        return

    schema = get_db_schema(conn)
    if not schema:
        conn.close()
        return

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        conn.close()
        return

    while True:
        user_prompt = input("Ask me anything about the database (or type 'exit' to quit): ")
        if user_prompt.lower() == 'exit':
            break

        sql_query = generate_sql_query(user_prompt, schema, gemini_api_key)
        print("\nGenerated SQL Query:")
        print(sql_query)

        confirm_run = ask_yes_no_question("Run this query?")
        if confirm_run:
            results, column_names = execute_query(conn, sql_query)
            if results is not None:
                print("\nQuery Results:")
                if column_names:
                    print(column_names)
                for row in results:
                    print(row)
        else:
            print("Query not executed.")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
