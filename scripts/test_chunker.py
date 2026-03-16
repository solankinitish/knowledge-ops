from app.extraction.page_extractor import PageExtractor
from app.processing.chunker import TextChunker

url = "https://en.wikipedia.org/wiki/FastAPI"

page_extractor = PageExtractor()
text = page_extractor.extract(url=url)
text_chunker = TextChunker()

texts = text_chunker.chunk(text)

print(texts[0])
print(len(texts))
