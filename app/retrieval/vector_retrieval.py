from app.retrieval.vector_store import VectorStore
from app.retrieval.embedding_service import EmbeddingService


class VectorRetriever:

    def __init__(self, vector_store: VectorStore, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
    
    def retrieve(self, query: str, top_k=3):

        # Step 1: Embed query
        query_embedding = self.embedding_service.embed([query])[0]

        # Step 2: Search vector DB (get more for better selection)
        results = self.vector_store.search(query_embedding, top_k=top_k)

        return results
