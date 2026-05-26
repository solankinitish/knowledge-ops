from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.vector_retrieval import VectorRetriever
from app.prompts.prompt_builder import PromptBuilder
from app.llm.llm_client import LLMClient
from app.utils.logger import get_logger
from app.search.search_engine import SearchEngine
from app.processing.query_processor import QueryProcessor
from app.processing.query_planner import QueryPlanner
import time
import numpy as np


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
        self.query_processor = QueryProcessor()
        self.query_planner = QueryPlanner()
    
    def cos_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    def is_grounded(self, answer: str, retrieved_chunks: list, threshold: float = 0.7) -> bool:
        combined_context = " ".join(retrieved_chunks[:3])
        answer_embedding = self.embedder.embed([answer])[0]
        context_embedding = self.embedder.embed([combined_context])[0]
        similarity = self.cos_sim(answer_embedding, context_embedding)
        self.logger.info(f"Grounding score: {similarity:.3f} (threshold: {threshold})")
        return similarity >= threshold


    def process(self, query: str):

        self.logger.info("Starting research pipeline")

        self.logger.info(f"Query: {query}")

        # Step 1: Searching URLs
        sub_ques = self.query_planner.plan(query)
        self.logger.info(f"Sub-questions: {sub_ques}")

        if not sub_ques:
            self.logger.error("No questions framed from the query.")

        all_urls = []
        for sub_q in sub_ques:
            queries = self.query_processor.process(sub_q)[:2]
            
            for q in queries:
                try:
                    urls = self.search_engine.search(q)[:2]
                    all_urls.extend(urls)
                except Exception as e:
                    self.logger.error(f"Search failed for query: {q} | Error: {e}")
                    continue
            time.sleep(1)
        
        urls = list(set(all_urls))[:5]
        self.logger.info(f"URLs to process: {urls}")

        if not urls:
            self.logger.error("No URLs found.")

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

        all_chunks = all_chunks[:50]
    
        if not all_chunks:
            return "I don't know."
        self.logger.info(f"Number of chunks created: {len(all_chunks)}")

        # Step 3: Embed
        embeddings = self.embedder.embed(all_chunks)
        self.logger.info("Chunks embedded.")

        # Step 4: Clear and Store
        self.vector_store.clear()
        self.vector_store.add(all_chunks, embeddings)

        # Step 5: Retrieve
        retrieved_chunks = self.retriever.retrieve(query)
        self.logger.info(f"Retrieved chunks: {len(retrieved_chunks)}")

        for i, chunk in enumerate(retrieved_chunks):
            self.logger.info(f"Retrieved chunk {i}: {chunk[:150]}")
        if len(retrieved_chunks) == 0:
            self.logger.info("No relevant context found.")
            return "I don't know"

        # Step 6: Build Prompt
        context = "\n\n".join(retrieved_chunks[:3])
        prompt = self.prompt_builder.build(context, query)
        self.logger.info(f"Prompt:\n{prompt}")

        # Step 7: Generate Answer
        self.logger.info("Sending prompt to LLM")
        response = self.llm.generate(prompt)
        self.logger.info("Received response from LLM")

        # Step 8: Grounding Verification
        self.logger.info("Verifying grounding...")
        if not self.is_grounded(response, retrieved_chunks):
            self.logger.info("Answer failed grounding check")
            return "I don't know - answer couldn't be retrieved from chunks."


        return response
