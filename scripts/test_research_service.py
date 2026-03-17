from app.services.research_service import ResearchService

service = ResearchService()

url = "https://en.wikipedia.org/wiki/FastAPI"
query = "What is FastAPI?"

response = service.process(url, query)

print(response)
