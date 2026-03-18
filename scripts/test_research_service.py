from app.services.research_service import ResearchService

service = ResearchService()

url = "https://en.wikipedia.org/wiki/FastAPI"
query = "Who created FastAPI?"

response = service.process(url, query)

print(response)
