import mysql.connector
import mysql.connector
import os
from dotenv import load_dotenv

from ai_backends.lm_studio import LmStudioAI
from ai_backends.gemini_ai import GeminiAI
from ai_backends.deepseek_ai import DeepSeekAI

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
                sql_schema += "\n)"
            sql_schema += ";\n\n"
        return sql_schema
    except mysql.connector.Error as e:
        print(f"Error reading database schema: {e}")
        return None
    finally:
        cursor.close()

def generate_sql_query(prompt, schema, ai_backend_name):
    if ai_backend_name == "gemini":
        ai_backend = GeminiAI()
    elif ai_backend_name == "deepseek":
        ai_backend = DeepSeekAI()
    elif ai_backend_name == "lm-studio":
        ai_backend = LmStudioAI()
    else:
        raise ValueError(f"Unsupported AI backend: {ai_backend_name}")
    return ai_backend.generate_query(prompt, schema)

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

    ai_backend_name = os.getenv("AI_BACKEND")
    if not ai_backend_name:
        ai_backend_name = "gemini" # Default to gemini if not set in env

    while True:
        user_prompt = input("Ask me anything about the database (or type 'exit' to quit): ")
        if user_prompt.lower() == 'exit':
            break

        sql_query = generate_sql_query(user_prompt, schema, ai_backend_name)
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
