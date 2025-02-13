import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiAI:
    def __init__(self, api_key=None):
        if api_key is None:
            self.api_key = os.getenv("GEMINI_API_KEY")
        else:
            self.api_key = api_key
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_query(self, prompt, schema):
        prompt_content = f"""
        **IMPORTANT and CRITICAL INSTRUCTION**: Generate a valid SQL query with comments to answer the question based **EXCLUSIVELY** on the provided database schema.
        Your SQL query **MUST ONLY** use tables and columns that are **explicitly defined** in the provided schema.
        **ABSOLUTELY DO NOT** use any tables or columns that are **NOT** present in the schema.
        Ensure that all information is retrieved from the **correct tables** as defined in the schema. Use JOINs when necessary and explicitly indicated by relationships within the schema.
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

        response = self.model.generate_content(prompt_content)
        # Strip markdown formatting
        sql_query = response.text
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query
