from app.prompts.prompt_builder import PromptBuilder

builder = PromptBuilder()

query = "What is FastAPI?"

chunks = [
    "FastAPI is a web framework for building APIs in Python.",
    "It uses Pydantic for validation."
]

prompt = builder.build(query, chunks)

print(prompt)
