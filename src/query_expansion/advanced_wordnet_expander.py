import spacy
from nltk.corpus import wordnet
import gensim.downloader as gensim_api
from query_expansion.query_expander import QueryExpander


class AdvancedWordnetExpander(QueryExpander):
    spacy_object = None
    model_glove = None

    def __init__(self):
        self.spacy_object = spacy.load("en_core_web_sm")
        self.model_glove = gensim_api.load("glove-wiki-gigaword-300")

    def expand(self, query: str) -> str:
        query_object = self.spacy_object(query)

        # Get tokens for the query
        new_query_candidates = []
        for token in query_object:
            synonyms, antonyms = self.synonym_antonym_extractor(token.text)
            synonyms, antonyms = self.best_words_extractor(token.text, synonyms, antonyms)
            new_query_candidates.append(token.text)
            new_query_candidates += synonyms + antonyms
        
        # Remove duplicates
        new_query_terms = list(dict.fromkeys(new_query_candidates))
        new_query = " ".join(new_query_terms)

        return new_query

    def synonym_antonym_extractor(self, word: str) -> tuple[str, str]:
        synonyms = []
        antonyms = []

        for alternatives in wordnet.synsets(word):
            for alternative in alternatives.lemmas():
                synonyms.append(str(alternative.name()).replace("_", " "))
                if alternative.antonyms():
                    antonyms.append(str(alternative.antonyms()[0].name()).replace("_", " "))

        return list(set(synonyms)), list(set(antonyms))

    def best_words_extractor(self, word: str, synonyms: list[str], antonyms: list[str]) -> tuple[str, str]:
        glove_synonyms = []
        glove_antonyms = []

        for synonym in synonyms:
            try:
                if self.model_glove.get_vector(synonym) is not None and synonym != word:
                    glove_synonyms.append(synonym)
            except:
                pass
        for antonym in antonyms:
            try:
                if self.model_glove.get_vector(antonym) is not None and antonym != word:
                    glove_antonyms.append(antonym)
            except:
                pass

        synonym_score_dictionary = {}
        antonym_score_dictionary = {}
        for glove_synonym in glove_synonyms:
            synonym_score_dictionary[glove_synonym] = self.model_glove.distance(word, glove_synonym)
        for glove_antonym in glove_antonyms:
            antonym_score_dictionary[glove_antonym] = self.model_glove.distance(word, glove_antonym)



        # getting only the top-3 most similar synonyms and most dissimilar antonyms
        # values from the dictionaries
        synonym_score_dictionary = {k: v for k, v in sorted(synonym_score_dictionary.items(), key=lambda item: item[1])}
        synonym_score_dictionary = {k: synonym_score_dictionary[k] for k in list(synonym_score_dictionary)[:20]}
        antonym_score_dictionary = {k: v for k, v in sorted(antonym_score_dictionary.items(), reverse=True, key=lambda item: item[1])}
        antonym_score_dictionary = {k: antonym_score_dictionary[k] for k in list(antonym_score_dictionary)[:20]}

        if len(synonym_score_dictionary) > 3:
            synonym_results = list(synonym_score_dictionary.keys())[:3]
        else:
            synonym_results = list(synonym_score_dictionary.keys())

        if len(antonym_score_dictionary) > 3:
            antonym_results = list(antonym_score_dictionary.keys())[:3]
        else:
            antonym_results = list(antonym_score_dictionary.keys())

        return synonym_results, antonym_results
