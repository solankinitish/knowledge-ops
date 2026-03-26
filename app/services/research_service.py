from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.vector_retrieval import VectorRetriever
from app.prompts.prompt_builder import PromptBuilder
from app.llm.llm_client import LLMClient
from app.utils.logger import get_logger
from app.search.search_engine import SearchEngine




class ResearchService:

    def __init__(self):

        self.logger = get_logger(__name__)

        self.extractor = PageExtractor()
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self.retriever = VectorRetriever(self.vector_store, self.embedder)
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient()
        self.search_engine = SearchEngine()

    def process(self, query: str):

        self.logger.info("Starting research pipeline")

        self.logger.info(f"Query: {query}")

        # Step 1: Searching URLs
        urls = self.search_engine.search(query)
        self.logger.info(f"URLs found: {len(urls)}")

        urls = urls[:3]

        # Step 2: Extracting text and forming chunks
        all_chunks = []

        for url in urls:
            try:
                self.logger.info(f"Processing URL: {url}")

                text = self.extractor.extract(url)
                chunks = self.chunker.chunk(text)

                all_chunks.extend(chunks)
            except Exception as e:
                self.logger.info(f"Failed Url: {url} | Error: {e}")
                continue
    
        if not all_chunks:
            return "I don't know."
        self.logger.info(f"Number of chunks created: {len(all_chunks)}")

        # Step 3: Embed
        embeddings = self.embedder.embed(all_chunks)

        # Step 4: Store
        self.vector_store.add(all_chunks, embeddings)

        # Step 5: Retrieve
        retrieved_chunks = self.retriever.retrieve(query)
        if len(retrieved_chunks) == 0:
            self.logger.info("No relevant context found.")
            return "I don't know"
        self.logger.info(f"Retrieved chunks: {len(retrieved_chunks)}")

        # Step 6: Build Prompt
        context = "\n\n".join(retrieved_chunks[:3])
        prompt = self.prompt_builder.build(context, query)

        # Step 7: Generate Answer
        self.logger.info("Sending prompt to LLM")
        response = self.llm.generate(prompt)
        self.logger.info("Received response from LLM")

        return response
