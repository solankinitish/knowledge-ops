from app.services.research_service import ResearchService

service = ResearchService()

query = "What is FastAPI?"

response = service.process(query)

print(response)
