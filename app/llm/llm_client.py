from app.llm.ollama_provider import OLLAMA


class LLMClient:

    def __init__(self):
        self.provider = OLLAMA()
    
    def generate(self, prompt: str):
        return self.provider.generate(prompt)
