import transformers
# Force faiss to be available, because it should be
transformers.utils.import_utils._faiss_available = True

import nltk
from nltk.corpus import wordnet
import string
import spacy
import gensim.downloader as api
from spacy.lang.en.stop_words import STOP_WORDS
from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder
import constants
from indexing.hit import Hit
from corpus.corpus import Corpus

class DenseVoteIndexer:
    sp = None
    model_glove = None
    index_file_path = None
    searcher = None

    def __init__(self, corpus: Corpus, index_file_path: str):
        self.index_file_path = index_file_path
        self.sp = spacy.load("en_core_web_sm")
        self.model_glove = api.load("glove-wiki-gigaword-300")


        # Initialize indexer
        self.searcher = FaissSearcher(
            self.index_file_path,
            'castorini/tct_colbert-msmarco'
        )

    # important function, required to be implemented in the query expansion script.
    # extracts list of synonyms and antonyms from the wordnet.
    def synonym_antonym_extractor(self, w_):
        # extracting relevant synonyms and antonym pairs.
        from nltk.corpus import wordnet
        synonyms = []
        antonyms = []

        for syn in wordnet.synsets(w_):
            for l in syn.lemmas():
                synonyms.append(str(l.name()).replace('_',' '))
                if l.antonyms():
                        antonyms.append(str(l.antonyms()[0].name()).replace('_',' '))
        return list(set(synonyms)), list(set(antonyms))

    # Important function required for the script you are making, for extract best
    # synonym and antonym words. Second, it also calls synonym_antonym_extractor function in it.
    # Also, it requires above loading of the module for its working.

    # Getting 3 best synonyms and 2 best antonym pairs for a given 'ADJ'
    def best_words_extractor(self, w_, syn_list, ann_list):
        # prepare dictionaries for scores of syn_list & ann_list with w_
        syns = []
        anns = []
        for s_ in syn_list:
            try:
                if self.model_glove.get_vector(s_) is not None and s_ != w_:
                    syns.append(s_)
            except:
                pass
        # print(syns)
        for a_ in ann_list:
            try:
                if self.model_glove.get_vector(a_) is not None and a_ != w_:
                    anns.append(a_)
            except:
                pass
        # print(anns)
        syn_score_dict = {}
        ann_score_dict = {}
        for s_ in syns:
            syn_score_dict[s_] = self.model_glove.distance(w_, s_)
        for a_ in anns:
            ann_score_dict[a_] = self.model_glove.distance(w_, a_)
        # getting only the top-k most similar synonyms and most dissimilar antonyms
        # values from the dictionaries and creating score permutations for them.
        syn_score_dict = {k: v for k, v in sorted(syn_score_dict.items(), key=lambda item: item[1])}
        # print(syn_score_dict)
        syn_score_dict = {k: syn_score_dict[k] for k in list(syn_score_dict)[:20]}
        # print(syn_score_dict)
        ann_score_dict = {k: v for k, v in sorted(ann_score_dict.items(), key=lambda item: item[1])}
        # print(ann_score_dict)
        ann_score_dict = {k: ann_score_dict[k] for k in list(ann_score_dict)[:20]}
        # print(ann_score_dict)
        syn_data = []
        ann_data = []
        c_ = 0
        for i, j in syn_score_dict.items():
            c_ = c_ + 1
            syn_data.append(i)
            if c_ >=3:
                break
        if len(syn_data) < 3:
            syn_data = ['good','well', 'best']
        c_ = 0
        for i, j in ann_score_dict.items():
            c_ = c_ + 1
            ann_data.append(i)
            if c_ >=1:
                break
        if len(ann_data) < 2:
            if len(ann_data) == 0:
                ann_data = ['worse','badly']
            if len(ann_data) == 1 and ann_data[0] != 'worse':
                ann_data.append('worse')
            if len(ann_data) == 1 and ann_data[0] == 'worse':
                ann_data.append('different')
        return syn_data, ann_data

    # IMPORTANT: This function combined with above two synonym and antonym
    # finding and generating function is required to generate the expanded queries.
    # return two expanded query versions.
    # nouns only, top-3 synonyms and antonyms queries.
    # Note: this is the final function that given an input query generates out
    # series of various expanded queries as output.
    def get_comparation_superlation_nouns(self, query):
        nouns_as_string = []
        nouns_only_string = []
        restricted_nouns_as_string = []
        doc = self.sp(query)
        annotations = ["CC", "CD", "JJ", "JJR", "JJS",
                "RB", "RBR", "RBS", "NN", "NNS", "NNP",
                "NNPS", "VB"]
        annotations_except_nouns = ["CC", "CD", "JJ", "JJR", "JJS",
                "RB", "RBR", "RBS", "VB"]
        annotations_nouns = ["NN", "NNS", "NNP", "NNPS", "VB"]
        adj_flg = 0
        adj_val = 'better' # default value, query objectives.
        # appending data into nouns as string
        for token in doc:
            if token.tag_ in annotations:
                nouns_as_string.append(token.text)
                if token.tag_ in annotations_except_nouns and adj_flg == 0:
                    adj_val = token.text
                    adj_flg = 1
                if token.tag_ not in annotations_except_nouns:
                    restricted_nouns_as_string.append(token.text)
                if token.tag_ in annotations_nouns:
                    nouns_only_string.append(token.text)

        # appending top-3 syns and anons to the query
        adj_val= adj_val.lower()
        syns, anons = self.synonym_antonym_extractor(adj_val)
        # print(syns, anons)
        if len(syns) == 0:
            syns, _ = self.synonym_antonym_extractor('different')
        if len(anons) == 0:
            _, anons = self.synonym_antonym_extractor('better')
        
        syns_fin, anons_fin = self.best_words_extractor(adj_val,syns, anons)
        
        # queries preprepartion
        base_query = " ".join(nouns_as_string)
        noun_query = " ".join(nouns_only_string)
        temp_query = " ".join(restricted_nouns_as_string)
        syn1_query = "".join(syns_fin[0]).strip() + " " + temp_query
        syn2_query = "".join(syns_fin[1]).strip() + " " + temp_query
        syn3_query = "".join(syns_fin[2]).strip() + " " + temp_query
        ant1_query = "".join(anons_fin[0]).strip() + " " + temp_query
        ant2_query = "".join(anons_fin[1]).strip() + " " + temp_query

        return base_query.strip(), noun_query.strip(), syn1_query.strip(), syn2_query.strip(), syn3_query.strip(), \
        ant1_query.strip(), ant2_query.strip()

    def index(self):
        # Indexing is not directly supported in the program
        pass

    def query(self, query: str) -> list[type[Hit]]:
        # Get expanded query variations
        queries = self.get_comparation_superlation_nouns(query)

        all_hits = []
        for query in queries:
            hits = self.searcher.search(query, k=constants.INITIAL_RETRIEVAL_AMOUNT)
            all_hits += hits
        
        # Group hits by document id
        hits_by_id = {}
        for hit in all_hits:
            if hit.docid in hits_by_id:
                hits_by_id[hit.docid].append(hit)
            else:
                hits_by_id[hit.docid] = [hit]
        
        # Sort dictionary to list based on the hit amount
        hits_sorted = sorted(hits_by_id.values(), key=lambda item: len(item), reverse=True)

        # Return at maximum twice the amount of initial search
        if len(hits_sorted) > constants.INITIAL_RETRIEVAL_AMOUNT * 2:
            hits_sorted = hits_sorted[:constants.INITIAL_RETRIEVAL_AMOUNT]

        # Convert to proper hit list
        hit_list = []
        for hits in hits_sorted:
            # Calculate average of scores
            score = sum((hit.score for hit in hits)) / len(hits)

            # Create hit object
            hit = Hit(hits[0].docid, score)

            # Append to final hit list
            hit_list.append(hit)
        
        # Sort hit list based on the scores
        hit_list = sorted(hit_list, key=lambda hit: hit.score, reverse=True)

        # Finally return hit list
        return hit_list