from typing import Union
import pyterrier as pt

import constants
from corpus import Corpus
from indexing.hit import Hit
from indexing.indexer import Indexer


class Index:
    corpus: Corpus
    indexer: Indexer
    index_file_path: str

    def __init__(self, indexer, corpus: Union[Corpus, None] = None, index_file_path: str = constants.INDEX_FILE_LOCATION):
        self.threads = constants.THREADS

        # Initialize python terrier
        if not pt.started():
            pt.init()

        self.corpus = corpus
        self.index_file_path = index_file_path
        self.indexer = indexer(self.corpus, self.index_file_path)

    def update(self):
        self.indexer.index()

    def query(self, query: str, verbose=False) -> list[Hit]:
        results = self.indexer.query(query)

        # Link corpus to the hit objects if available
        if not self.corpus:
            return results

        for result in results:
            result.corpus = self.corpus.entries_by_id.get(result.id)

        if verbose:
            for i in range(10):
                contents = results[i].corpus.contents if len(
                    results[i].corpus.contents) < 80 else results[i].corpus.contents[:80] + "..."
                print(f"Id: {results[i].corpus.id} | Contents: {contents}")

        return results
