import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
from ai_backends.prompt_generator import generate_prompt
import uuid

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
        self.threads = {}

    def generate_query(self, prompt, schema, thread_id=None):
        if not thread_id:
            thread_id = str(uuid.uuid4())
            self.threads[thread_id] = []

        history = self.threads.get(thread_id, [])
        prompt_content = generate_prompt(schema, prompt, history)
        print("Using DeepSeek AI Backend")
        try:
            model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "You are a database admin. Generate SQL queries strictly adhering to the schema provided."},
                          {"role": "user", "content": prompt_content}],
                stream=False
            )
            query = response.choices[0].message.content
            query = query.replace("```sql", "").replace("```", "").strip()

            self.threads[thread_id].append((prompt, query))
            return query
        except requests.exceptions.RequestException as e:
            return f"Error communicating with DeepSeek API: {e}\n {response.text}"
        except (KeyError, IndexError) as e:
            return f"Error parsing DeepSeek API response: {e}"

    def stop_thread(self, thread_id):
        if thread_id in self.threads:
            del self.threads[thread_id]
        else:
            return f"Thread ID {thread_id} not found."
