from app.llm.llm_client import LLMClient
import json


class QueryPlanner:
    def __init__(self):
        self.llm = LLMClient()
    def plan(self, query: str) -> list[str]:
        prompt = f"""
Analyze this query: {query}

A query contains multiple sub-questions only if it explicitly asks about more than one distinct topic.

Rules:
1. Each sub-question must be a complete, standalone sentence.
2. Never use pronouns like "he", "she", "it", "they" — always use the explicit entity name from the original query.
3. Output only the JSON array, no extra text.

Return a JSON array of complete, meaningful questions extracted from the query.
"""
        try:
            response = self.llm.generate(prompt)
            sub_ques = json.loads(response)
            return sub_ques
        except:
            return [query]
