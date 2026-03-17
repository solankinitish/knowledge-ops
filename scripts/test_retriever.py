from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.vector_retrieval import VectorRetriever

url = "https://en.wikipedia.org/wiki/FastAPI"

extractor = PageExtractor()
chunker = TextChunker()
embedder = EmbeddingService()
store = VectorStore()

# Build index
text = extractor.extract(url)
chunks = chunker.chunk(text)
embeddings = embedder.embed(chunks)
store.add(chunks, embeddings)

# Retriever
retriever = VectorRetriever(store, embedder)

query = "What is FastAPI?"

results = retriever.retrieve(query)

print(results)
