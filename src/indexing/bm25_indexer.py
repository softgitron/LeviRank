import constants
from corpus.corpus import Corpus
from indexing.hit import Hit
from indexing.index import Indexer


class BM25Indexer(Indexer):
    corpus: Corpus
    index_file_path: str
    indexer = None
    num_results = constants.INITIAL_RETRIEVAL_AMOUNT
    pt = None

    def __init__(self, corpus: Corpus, index_file_path: str):
        # Initialize python terrier
        try:
            import pyterrier as pt
            self.pt = pt
            if not pt.started():
                pt.init(version = 5.5, helper_version = "0.0.6")
        except:
            print("PYTHON-TERRIER NOT SUPPORTED IN THIS BUILD")

        self.corpus = corpus
        self.index_file_path = index_file_path
        self.indexer = pt.IterDictIndexer(self.index_file_path, meta=["id"], meta_reverse=["id"], fields=[
                                          "contents_preprocessed"], controls={"wmodel":"BM25", "k_1":"1.2d", "b":"0.68d"}, threads=1)

    def index(self):
        self.indexer.index(self.corpus, meta=["id"], fields=["contents_preprocessed"])

    def query(self, query: str) -> list[type[Hit]]:
        raw_results = self.pt.BatchRetrieve(
            self.indexer, metadata=["id"], num_results=self.num_results).search(query)
        results = [0] * len(raw_results)
        for i in range(len(results)):
            results[i] = Hit(raw_results["id"][i], raw_results["score"][i])
        return results
