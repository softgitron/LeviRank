from typing import Union
import pyterrier as pt

import constants
from corpus.corpus import Corpus
from indexing.hit import Hit
from indexing.indexer import Indexer
from preprocessing.preprocessor import Preprocessor
from query_expansion.query_expander import QueryExpander
from reranking.reranker import Reranker
from indexing.queries import Queries


class Index:
    corpus: Corpus
    indexer: Indexer
    preprocessor: Preprocessor
    query_expander: QueryExpander
    reranker: Reranker
    index_file_path: str

    def __init__(self, indexer, corpus: Union[Corpus, None] = None, preprocessor: Preprocessor = None,
                 query_expander: QueryExpander = None, reranker: Reranker = None,
                 index_file_path: str = constants.INDEX_FILE_LOCATION):
        # Initialize python terrier
        if not pt.started():
            pt.init(version = 5.5, helper_version = "0.0.6")

        self.corpus = corpus
        self.index_file_path = index_file_path
        self.preprocessor = preprocessor
        self.query_expander = query_expander
        self.reranker = reranker
        self.indexer = indexer(self.corpus, self.index_file_path)

    def update(self):
        self.indexer.index()

    def query(self, query: str, verbose=False) -> list[Hit]:
        # Expand query
        queries = self.expand_query(query)

        # Get query results from the indexer
        results = self.indexer.query(queries.preprocessed_query)

        # Link corpus to the hit objects if available
        if not self.corpus:
            return results

        for result in results:
            result.corpus_entry = self.corpus.entries_by_id.get(result.id)

        # If reranker is available, rerank the results
        if self.reranker:
            results = self.reranker.rerank(queries, results)

        if verbose:
            for i in range(10):
                contents = results[i].corpus_entry.contents if len(
                    results[i].corpus_entry.contents) < 80 else results[i].corpus_entry.contents[:80] + "..."
                print(
                    f"Id: {results[i].corpus_entry.id} | Contents: {contents}")

        return results

    def expand_query(self, query):
        # Save original query
        queries = Queries(query, query)

        # Preprocess query, if there is preprocessor available
        if self.preprocessor:
            queries.preprocessed_query = self.preprocessor.process(queries.preprocessed_query)

        # Expand query, if there is query expander available
        if self.query_expander:
            queries.expanded_without_post_processing = self.query_expander.expand(queries.preprocessed_query)
            # Preprocess again after expansion to avoid problems with special signs
            if self.preprocessor:
                queries.preprocessed_query = self.preprocessor.process(queries.preprocessed_query)

            # Remove duplicates
            queries.preprocessed_query = list(dict.fromkeys(queries.preprocessed_query))

        return queries