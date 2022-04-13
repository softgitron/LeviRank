from abc import ABC, abstractmethod
from corpus.corpus import Corpus
from indexing.hit import Hit


class Indexer:
    @abstractmethod
    def __init__(self, corpus: Corpus, index_file_path: str):
        pass

    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def query(self, query: str) -> list[Hit]:
        pass
