import chromadb


class VectorStore:

    def __init__(self):

        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="knowledge_ops"
        )
    
    def add(self, chunks, embeddings):

        ids = [str(i) for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    def clear(self):
        all_items = self.collection.get()

        if all_items and "ids" in all_items and len(all_items["ids"]) > 0:
            self.collection.delete(ids=all_items["ids"])
    
    def search(self, query_embedding, top_k=3):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0]
