import google.generativeai as genai
import os
from dotenv import load_dotenv
from ai_backends.prompt_generator import generate_prompt
import uuid

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
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.model = genai.GenerativeModel(model_name)
        self.threads = {}

    def generate_query(self, prompt, schema, thread_id=None):
        if not thread_id:
            thread_id = str(uuid.uuid4())
            self.threads[thread_id] = []

        history = self.threads.get(thread_id, [])
        prompt_content = generate_prompt(schema, prompt, history)

        response = self.model.generate_content(prompt_content)
        # Strip markdown formatting
        sql_query = response.text
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        self.threads[thread_id].append((prompt, sql_query))
        return sql_query

    def stop_thread(self, thread_id):
        if thread_id in self.threads:
            del self.threads[thread_id]
        else:
            return f"Thread ID {thread_id} not found."
