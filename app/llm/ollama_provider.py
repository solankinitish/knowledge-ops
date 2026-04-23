import requests

class OLLAMA:
    def __init__(self, model_name="mistral"):
        self.model = model_name
    
    def generate(self, prompt):
        url = "http://localhost:11434/api/generate"

        body = {"model": self.model, "prompt": prompt, "stream": False}

        response = requests.post(url, json=body)

        return response.json()["response"]
