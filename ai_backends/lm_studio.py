import os
from dotenv import load_dotenv
import requests
from ai_backends.prompt_generator import generate_prompt
import json
import uuid

load_dotenv()

class LmStudioAI:
    def __init__(self, api_key=None):
        self.base_url = "http://localhost:1234"
        self.threads = {}

    def generate_query(self, prompt, schema, thread_id=None):
        if not thread_id:
            thread_id = str(uuid.uuid4())
            self.threads[thread_id] = []

        history = self.threads.get(thread_id, [])
        prompt_content = generate_prompt(schema, prompt, history)
        headers = {
            "Content-Type": "application/json"
        }
        model = os.getenv("LM_STUDIO_MODEL", "lm-chat")
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a database admin. Generate SQL queries strictly adhering to the schema provided."},
                {"role": "user", "content": prompt_content}
            ],
            "stream": False
        }
        try:
            response = requests.post(f"{self.base_url}/v1/chat/completions", headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            query = response.json()["choices"][0]["message"]["content"]
            query = query.replace("```sql", "").replace("```", "").strip()

            self.threads[thread_id].append((prompt, query))
            return query
        except requests.exceptions.RequestException as e:
            return f"Error communicating with LM Studio API: {e}"
        except (KeyError, IndexError) as e:
            return f"Error parsing LM Studio API response: {e}. Response: {response.text}"
        except Exception as e:
            return f"Error generating SQL query: {str(e)}"

    def stop_thread(self, thread_id):
        if thread_id in self.threads:
            del self.threads[thread_id]
        else:
            return f"Thread ID {thread_id} not found."
