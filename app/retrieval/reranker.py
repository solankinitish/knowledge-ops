import numpy as np


class Reranker:

    def __init__(self, embedding_service, threshold=0.3):
        self.embedding_service = embedding_service
        self.threshold = threshold

    def rerank(self, query, documents, top_k=3):

        if not documents:
            return []
        
        # Embed query + docs
        query_embedding = self.embedding_service.embed([query])[0]
        doc_embeddings = self.embedding_service.embed(documents)

        # Similarity (dot product)
        scores = np.dot(doc_embeddings, query_embedding)

        # Sort by relevance
        ranked_indices = np.argsort(scores)[::-1]

        results = []

        for i in ranked_indices:
            if scores[i] < self.threshold:
                continue

            results.append(documents[i])

            if len(results) == top_k:
                break

        return results
