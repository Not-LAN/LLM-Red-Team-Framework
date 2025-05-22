# Model Configuration for Mistral-7B-Instruct-v0.2
# -----------------------------------------------
# model: Mistral-7B-Instruct-v0.2
# https://gitlab.cee.redhat.com/models-corp/user-documentation/-/blob/main/models/mistral-7b-instruct-v0-2.md?ref_type=heads
# model-string: mistralai/Mistral-7B-Instruct-v0.2
# api: https://mistral-7b-instruct-v0-2--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com/v1
# huggingface: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
# internal-repository: https://simple-llm-cache.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com/llm-cache/Mistral-7B-Instruct-v0.2/
# context-length: deployed with 16384 of model theoretical max 32768
# tool-calling: No
# tool-calling-template: na
# supported-criticality: C4
# availability-slo: 95%
# redundant-deployment: false
# disaster-recovery: false
# cost-per-million-inferences: $0.0  <- cost model not implemented yet


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
