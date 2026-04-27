from app.services.research_service import ResearchService

service = ResearchService()

query = "What is FastAPI and who created it?"

response = service.process(query)

print(response)
