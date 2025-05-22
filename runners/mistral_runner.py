import os
import requests

class MistralInterface:
    def __init__(self):
        self.api_url = "https://mistral.foo.com”
        self.model_id = "mistralai/Mistral"
        self.api_key = os.getenv("USER_KEY")

        if not self.api_key:
            raise ValueError("USER_KEY environment variable not set")

    def ask(self, prompt: str) -> str:
        """
        Sends a prompt to the Mistral REST API and returns the response.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model_id,
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.7
            }

            response = requests.post(
                f"{self.api_url}/v1/completions",
                headers=headers,
                json=payload,
                timeout=30,
                verify=False  # Allow self-signed or unverified certs if needed
            )

            response.raise_for_status()
            data = response.json()

            return data.get("choices", [{}])[0].get("text", "").strip()

        except Exception as e:
            return f"[ERROR] Failed to query Mistral API: {str(e)}"
