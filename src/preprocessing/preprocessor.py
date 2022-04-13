from abc import ABC, abstractmethod
from corpus.corpus import Corpus


class Preprocessor:
    @abstractmethod
    def process_corpus(self, corpus: Corpus) -> Corpus:
        pass

    @abstractmethod
    def process(self, document: str) -> str:
        pass
