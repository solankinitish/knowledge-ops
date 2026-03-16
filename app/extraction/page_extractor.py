import requests
from bs4 import BeautifulSoup
import re
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PageExtractor:

    def extract(self, url: str) -> str:

        logger.info(f"Extracting page: {url}")

        try:
            # Download Page
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove Garbage
            for tag in soup(["script", "style", "nav", "footer", "noscript"]):
                tag.decompose()
            
            # Extract Text
            content = soup.find("div", {"id": "mw-content-text"})
            
            if content:
                text = content.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)

            # Return Clean String
            return re.sub(r"\n{3,}", "\n\n", text).strip()
        
        except Exception as e:

            logger.error(f"Failed to extract {url}: {e}")
            return ""
