from app.llm.llm_client import LLMClient
import json


class QueryPlanner:
    def __init__(self):
        self.llm = LLMClient()
    def plan(self, query: str) -> list[str]:
        prompt = f"""
        Take this query: {query} and using just the info provided in the query itself,
        frame each element into one independent sub-question that is independently
        answerable without reference to other part of the query,
        extracted from the query,
        no extra text before or after. Output only a json array of strings.
        """
        try:
            response = self.llm.generate(prompt)
            sub_ques = json.loads(response)
            return sub_ques
        except:
            return [query]
