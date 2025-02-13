import os
from dotenv import load_dotenv
import requests
from ai_backends.prompt_generator import generate_prompt
import json

load_dotenv()

class LmStudioAI:
    def __init__(self, api_key=None):
        self.base_url = "http://localhost:1234"

    def generate_query(self, prompt, schema):
        prompt_content = generate_prompt(schema, prompt)
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
            return query.replace("```sql", "").replace("```", "").strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with LM Studio API: {e}"
        except (KeyError, IndexError) as e:
            return f"Error parsing LM Studio API response: {e}. Response: {response.text}"
        except Exception as e:
            return f"Error generating SQL query: {str(e)}"
