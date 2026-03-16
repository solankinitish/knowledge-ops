from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore

url = "https://en.wikipedia.org/wiki/FastAPI"

extractor = PageExtractor()
chunker = TextChunker()
embedder = EmbeddingService()
store = VectorStore()

text = extractor.extract(url)

chunks = chunker.chunk(text)

embeddings = embedder.embed(chunks)

store.add(chunks, embeddings)

query = "What is FastAPI?"

query_embedding = embedder.embed([query])[0]

results = store.search(query_embedding)

print(results)
