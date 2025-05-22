
import os
import google.generativeai as genai

class GeminiInterface:
    def __init__(self):
        # Load the Gemini API key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Configure the Gemini API client
        genai.configure(api_key=self.api_key)

        # Initialize the generative model (using direct prompt-response)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")

    def ask(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns the single-shot response.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"[ERROR] Failed to query Gemini model: {str(e)}"