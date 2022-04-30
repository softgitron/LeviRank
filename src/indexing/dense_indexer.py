import transformers
# Force faiss to be available, because it should be
transformers.utils.import_utils._faiss_available = True

import constants
from indexing.hit import Hit
from corpus.corpus import Corpus

class DenseIndexer:
    sp = None
    model_glove = None
    index_file_path = None
    searcher = None

    def __init__(self, corpus: Corpus, index_file_path: str):
        try:
            from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder
        except:
            print("PYSERINI NOT SUPPORTED IN THIS BUILD")
        self.index_file_path = index_file_path


        # Initialize indexer
        self.searcher = FaissSearcher(
            self.index_file_path,
            'castorini/tct_colbert-msmarco'
        )

    def index(self):
        # Indexing is not directly supported in the program
        pass

    def query(self, query: str) -> list[type[Hit]]:
        hits = self.searcher.search(query, k=constants.INITIAL_RETRIEVAL_AMOUNT)

        # Convert to proper hit list
        hit_list = []
        for hit in hits:
            # Create hit object
            hit_object = Hit(hit.docid, hit.score)

            # Append to final hit list
            hit_list.append(hit_object)
        
        # Sort hit list based on the scores
        hit_list = sorted(hit_list, key=lambda hit: hit.score, reverse=True)

        # Finally return hit list
        return hit_list