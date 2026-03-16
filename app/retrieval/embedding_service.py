from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    def embed(self, texts):

        embeddings = self.model.encode(texts)

        return embeddings
