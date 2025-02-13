import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

class DeepSeekAI:
    def __init__(self, api_key=None):
        if api_key is None:
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
        else:
            self.api_key = api_key
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    def generate_query(self, prompt, schema):
        prompt_content = f"""
        **IMPORTANT and CRITICAL INSTRUCTION**: Generate a valid SQL query with comments to answer the question based **EXCLUSIVELY** on the provided database schema.
        Your SQL query **MUST ONLY** use tables and columns that are **explicitly defined** in the provided schema.
        **ABSOLUTELY DO NOT** use any tables or columns that are **NOT** present in the schema.
        Ensure that all information is retrieved from the **correct tables** as defined in the schema. Use JOINs and aggregetions when necessary.
        It is **ABSOLUTELY CRITICAL** to pay meticulous attention to the schema and column names. 
        **Column names are case-sensitive**. Your generated SQL query **MUST ALSO BE case-sensitive** and accurately reflect the schema's case.
        To reiterate, **UNDER NO CIRCUMSTANCES** should you invent or assume the existence of tables or columns that are not in the provided schema.
        Return **ONLY** the raw SQL query, without any markdown wrappers, as plain text.

        Database Schema:
        {schema}

        Question:
        {prompt}

        SQL Query:
        """
        print("Using DeepSeek AI Backend")
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": "You are a database admin. Generate SQL queries strictly adhering to the schema provided."},
                          {"role": "user", "content": prompt_content}],
                stream=False
            )
            query = response.choices[0].message.content
            return query.replace("```sql", "").replace("```", "").strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with DeepSeek API: {e}\n {response.text}"
        except (KeyError, IndexError) as e:
            return f"Error parsing DeepSeek API response: {e}"
