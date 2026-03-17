class PromptBuilder:

    def build(self, query: str, context_chunks):

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a helpful assistant.

Answer the question using ONLY the provided context.

If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""
        
        return prompt.strip()
