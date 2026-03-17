from app.llm.dummy_provider import DummyLLM


class LLMClient:

    def __init__(self):
        self.provider = DummyLLM()
    
    def generate(self, prompt: str):
        return self.provider.generate(prompt)
