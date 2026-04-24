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

            if not content:
                content = soup.find("article")
            if not content:
                content = soup.find("main")
            
            if content:
                text = content.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)

            text = self.clean_text(text)

            # Return Clean String
            text = re.sub(r"\n{3,}", "\n\n", text).strip()

            if len(text) < 200:
                return ""
            if "sign in" in text.lower():
                return ""
            
            return text
        
        except Exception as e:

            logger.error(f"Failed to extract {url}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:

        lines = text.split("\n")

        cleaned = []

        for line in lines:
            line = line.strip()

            if len(line) < 50:
                continue

            if "learn how and when to remove" in line.lower():
                continue

            if "[" in line and "]" in line:
                continue

            cleaned.append(line)
        
        return "\n".join(cleaned)
