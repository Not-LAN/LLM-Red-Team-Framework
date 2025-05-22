import os
import openai

class OpenAIInterface:
    def __init__(self):
        # Fetch the OpenAI API key from an environment variable
          # Optional fallback (not recommended for prod)

        # Instantiate the OpenAI client as required in openai >= 1.0.0
        self.client = openai.OpenAI()

    def ask(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenAI chat model and returns the assistant's response.
        """
        try:
            # Call the chat completion endpoint
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" if your key supports it
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Return error message to help debug in CLI
            return f"[ERROR] Failed to query OpenAI model: {str(e)}"
