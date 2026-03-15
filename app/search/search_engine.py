from ddgs import DDGS
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SearchEngine:

    def __init__(self):
        pass

    def search(self, query: str, max_results: int = 5):

        results = []

        logger.info(f"Searching web for: {query}")

        with DDGS() as ddgs:

            searches = [r for r in ddgs.text(query, max_results=max_results)]

            for search in searches:
                if "href" in search:
                    results.append(search['href'])

        return results
