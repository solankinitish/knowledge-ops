from app.search.search_engine import SearchEngine

engine = SearchEngine()

results = engine.search("What is FastAPI")

print(results)
