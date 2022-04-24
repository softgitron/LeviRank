import pyterrier as pt
import constants
from corpus.corpus import Corpus
from indexing.hit import Hit
from indexing.index import Indexer


class BM25Indexer(Indexer):
    corpus: Corpus
    index_file_path: str
    indexer = None
    num_results = constants.INITIAL_RETRIEVAL_AMOUNT

    def __init__(self, corpus: Corpus, index_file_path: str):
        self.corpus = corpus
        self.index_file_path = index_file_path
        self.indexer = pt.IterDictIndexer(self.index_file_path, meta=["id"], meta_reverse=["id"], fields=[
                                          "contents_preprocessed"], controls={"wmodel":"BM25", "k_1":"1.2d", "b":"0.68d"}, threads=1)

    def index(self):
        self.indexer.index(self.corpus, meta=["id"], fields=["contents_preprocessed"])

    def query(self, query: str) -> list[type[Hit]]:
        raw_results = pt.BatchRetrieve(
            self.indexer, metadata=["id"], num_results=self.num_results).search(query)
        results = [0] * len(raw_results)
        for i in range(len(results)):
            results[i] = Hit(raw_results["id"][i], raw_results["score"][i])
        return results
