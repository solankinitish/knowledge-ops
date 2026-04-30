from app.llm.llm_client import LLMClient
import json


class QueryPlanner:
    def __init__(self):
        self.llm = LLMClient()
    def plan(self, query: str) -> list[str]:
        # prompt = f"""
        # Take this query: {query} and using just the info provided in the query itself,
        # frame each element into one independent sub-question that is independently
        # answerable without reference to other part of the query,
        # extracted from the query,
        # no extra text before or after. Output only a json array of strings or just with
        # one entry if the query is a one simple question.
        # """
        prompt = f"""
        Analyze this query: {query}

        A query contains multiple sub-questions only if it explicitly asks about more than one distinct topic.

        Example of multiple sub-questions: "What is FastAPI and who created it?" -> ["What is FastAPI?", "Who created FastAPI?"]
        Example of single question: "Who created FastAPI?" -> ["Who created FastAPI?"]

        Return a JSON array of complete, meaningful questions extracted from the query.
        Each question must be a full sentence, not a fragment.
        Output only the JSON array, no extra text.
        """
        try:
            response = self.llm.generate(prompt)
            sub_ques = json.loads(response)
            return sub_ques
        except:
            return [query]
