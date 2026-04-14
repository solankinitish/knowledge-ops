import numpy as np
import spacy


class Reranker:
    def __init__(self, embedding_service, threshold=0.3):
        self.embedding_service = embedding_service
        self.threshold = threshold
        self.nlp = spacy.load("en_core_web_sm")
    
    def rerank(self, query, documents, top_k=3):
        nlp = self.nlp

        if not documents:
            return []
        
        # Question Type
        words = query.lower().split()
        question_words = ["who", "what", "why", "when", "how", "where"]
        q_type = next((w for w in words if w in question_words), None)

        # Evaluating Similarity Scores
        query_embedding = self.embedding_service.embed([query])[0]
        doc_embeddings = self.embedding_service.embed(documents)
        s_scores = np.dot(doc_embeddings, query_embedding)


        results = {}

        # Evaluating h_scores
        h_scores = []
        for docu in documents:
            score = 0
            doc = nlp(docu)

            if q_type=="who":
                proper_noun = any(token.pos_ == "PROPN" for token in doc)
                if proper_noun:
                    score += 1

            if q_type=="when":

                for ent in doc.ents:
                    if ent.label_ in ["TIME", "DATE"]:
                        score += 1

            if q_type=="how":

                has_to_verb = any(token.text.lower() == "to" and token.head.pos_ == "VERB" for token in doc)

                modals = ["can", "should", "must", "need"]
                has_modal = any(token.text.lower() in modals for token in doc)

                step_words = ["first", "then", "next", "finally"]
                has_steps = any(token.text.lower() in step_words for token in doc)

                method_preps = ["by", "using", "through", "with"]
                has_method_prep = any(token.text.lower() in method_preps for token in doc)

                if has_to_verb or has_modal or has_steps or has_method_prep:
                    score += 1

            if q_type=="where":

                has_location = any(ent.label_ in ["GPE", "LOC", "FAC"] for ent in doc.ents)

                prepositions = ["in", "at", "on"]
                has_prep = any(token.text.lower() in prepositions for token in doc)

                if has_location and has_prep:
                    score += 1

            if q_type=="what":

                definites = ["is", "means", "refers to", "explained by"]
                has_definites = any(token.text.lower() in definites for token in doc)

                if has_definites:
                    score += 1

            if q_type=="why":

                causals = ["because", "since", "due to", "as a result"]
                has_causals = any(token.text.lower() in causals for token in doc)

                if has_causals:
                    score += 1
            
            if q_type==None:
                score = 0

            h_scores.append(score)

        
        # Evaluating Final Scores
        i = 0
        for docu in documents:
            f_score = 0
            if q_type in ["who", "where", "when"]:
                f_score = 0.4 * s_scores[i] + 0.6 * h_scores[i]
            elif q_type in ["what", "how", "why"]:
                f_score = 0.6 * s_scores[i] + 0.4 * h_scores[i]
            else:
                f_score = s_scores[i]
            results[docu] = f_score
            i += 1

        sorted_results = [k for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True)[:top_k]]

        return sorted_results
