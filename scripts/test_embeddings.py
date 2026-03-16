from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService

url = "https://en.wikipedia.org/wiki/FastAPI"

extractor = PageExtractor()
chunker = TextChunker()
embedder = EmbeddingService()

text = extractor.extract(url)

chunks = chunker.chunk(text)

embeddings = embedder.embed(chunks)

print("Number of chunks:", len(chunks))
print("Embedding shape:", len(embeddings), len(embeddings[0]))
