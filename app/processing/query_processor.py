class QueryProcessor:

    def process(self, query: str):

        query = self.normalize(query)

        queries = set()

        # Original
        queries.add(query)

        # Rewritten version
        rewritten = self.rewrite(query)
        queries.add(rewritten)

        # Variations
        variations = self.generate_variations(query)
        queries.update(variations)

        return list(queries)

    def normalize(self, qeury: str) -> str:
        return qeury.lower().strip()
    
    def rewrite(self, query: str) -> str:

        if query.startswith("what is"):
            return query.replace("what is", "definition of", 1)
        
        if query.startswith("who created"):
            return query.replace("who created", "creator of", 1)
        
        if query.startswith("how to"):
            return query.replace("how to", "guide to", 1)
        
        if query.startswith("why"):
            return f"reason for {query}"
        
        return query
    
    def generate_variations(self, query: str):

        variations = [
            f"{query} explanation",
            f"{query} details",
            f"{query} overview",
        ]

        return variations
