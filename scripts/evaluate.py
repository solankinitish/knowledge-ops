from app.services.research_service import ResearchService
from app.utils.logger import get_logger

logger = get_logger(__name__)

service = ResearchService()

queries = ["Who is the owner of Virgin Group and when was he born?",
            "What is the 2nd Amendment of the USA constitution?",
            "When did first person reach Mars and who was he?",
            "How to fractionionally distillate crude oil to extract petrol and diesel?",
            "Why did Subash Chandra Bose resigned from Congress Presidency?"]

answers = ["Richard Brandon, 18 July 1950",
           "The Second Amendment to the U.S. Constitution, ratified in 1791 as part of the Bill of Rights, protects the right of the people to keep and bear arms.",
           "I don't know",
           "Fractional distillation separates crude oil into useful components (fractions) by heating it to vaporize the mixture, then passing it into a tower that is hot at the bottom and cool at the top. Components condense at different heights based on their boiling points: long-chain hydrocarbons (high boiling points) collect lower down, while short-chain hydrocarbons (low boiling points) rise higher.",
           """
           Key reasons for his resignation included:
                    Ideological Divide: Bose advocated for a mass movement and a direct ultimatum to the British, opposing the moderate, non-violent approach favored by Gandhi.
                    1939 Election Controversy: Despite Gandhi supporting Pattabhi Sitaramayya, Bose won re-election. Gandhi called Sitaramayya's defeat "my own failure," leading to pressure on Bose.
                    Internal Opposition: Thirteen members of the Congress Working Committee resigned, and others withdrew support, making it impossible for Bose to form a working cabinet.
                    Foreign Policy Views: Bose was proactive about seeking aid from nations hostile to the British (like Nazi Germany) to secure Indian independence, a stance not supported by the Congress leadership.
                    """
            ]

for i, q in enumerate(queries):
    response = service.process(q)
    logger.info(f"Query: {q}")
    logger.info(f"Expected: {answers[i]}")
    logger.info(f"Actual: {response}")
    logger.info("---")
