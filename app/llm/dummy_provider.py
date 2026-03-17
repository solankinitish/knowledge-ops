class DummyLLM:

    def generate(self, prompt: str):

        return f"LLM Response:\n{prompt.upper()}"
    