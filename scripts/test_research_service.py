from app.services.research_service import ResearchService

service = ResearchService()

query = "What is the role of Subhash Chandra Bose in Independence?"

response = service.process(query)

print(response)
