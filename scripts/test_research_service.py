from app.services.research_service import ResearchService

service = ResearchService()

query = "Who created FastAPI?"

response = service.process(query)

print(response)
