class PromptBuilder:

    def detect_query_type(self, query):
        if query.lower().startswith(("who", "when", "where")):
            mode = "extract"
        else:
            mode = "explain"
        return mode

    def build(self, context: str, query: str):
        mode = self.detect_query_type(query)

        extraction_prompt = f"""
You are a precise question-answering assistant.

You must follow these steps strictly:

1. Read all the provided context carefully.
2. Identify the parts of the context that are relevant to the question.
3. Look for answer signals:
    - keywords related to the question
    - entities matching the expected answer type (example, person for "who", date for "when")
    - relationships (example, "created by", "developed by", "is defined as")
4. From the relevant parts, extract the exact answer.
5. Do NOT summarize the entire context.
6. If no clear answer is found, say "I don't know".

Context:
{context}

Question:
{query}

Answer (concise and direct):
"""
        
        explanation_prompt = f"""
You are a precise question-answering assistant.

You must follow these steps strictly:

1. Read all the provided context carefully.
2. Identify the parts of the context that are relevant to the question.
3. Understand the expected scope of the answer:
    - "what" -> definition or description
    - "why" -> reasons or causes
    - "how" -> process or steps
4. From the relevant parts, construct a clear and concise answer.
5. Do NOT include unnecessary information beyond the question scope.
6. If no clear answer is found, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

        if mode == "extract":
            return extraction_prompt.strip()
        
        else:
            return explanation_prompt.strip()
