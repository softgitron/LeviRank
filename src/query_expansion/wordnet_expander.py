from nltk.corpus import wordnet
from query_expansion.query_expander import QueryExpander


class WordnetExpander(QueryExpander):
    def expand(self, query) -> str:
        query_words = query.split(" ")

        all_entries = query_words.copy()
        # Find synonyms for every words in the query and append them to new query
        for query_word in query_words:
            for synonyms in wordnet.synsets(query_word):
                for synonym in synonyms.lemmas():
                    all_entries.append(synonym.name())

        # Remove duplicates from the list
        new_query_word_list = list(dict.fromkeys(all_entries))

        # Form new search query
        new_query = " ".join(new_query_word_list)

        return new_query
