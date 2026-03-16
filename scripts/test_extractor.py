from app.extraction.page_extractor import PageExtractor

page_extractor = PageExtractor()

url = "https://en.wikipedia.org/wiki/FastAPI"

text = page_extractor.extract(url=url)

print(text[:1000])
print(len(text))
