from app.services.research_service import ResearchService

service = ResearchService()

query = input("Enter your query: ")

response = service.process(query)

print(response)
