from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.vector_retrieval import VectorRetriever
from app.prompts.prompt_builder import PromptBuilder
from app.llm.llm_client import LLMClient


class ResearchService:

    def __init__(self):

        self.extractor = PageExtractor()
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self.retriever = VectorRetriever(self.vector_store, self.embedder)
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient()

    def process(self, url: str, query: str):

        # Step 1: Extract
        text = self.extractor.extract(url)

        # Step 2: Chunk
        chunks = self.chunker.chunk(text)

        # Step 3: Embed
        embeddings = self.embedder.embed(chunks)

        # Step 4: Store
        self.vector_store.add(chunks, embeddings)

        # Step 5: Retrieve
        retrieved_chunks = self.retriever.retrieve(query)

        # Step 6: Build Prompt
        prompt = self.prompt_builder.build(query, retrieved_chunks)

        # Step 7: Generate Answer
        response = self.llm.generate(prompt)

        return response
