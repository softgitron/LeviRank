from abc import ABC, abstractmethod
from indexing.hit import Hit
from indexing.queries import Queries


class SpellingErrorReranker:
    def rerank(self, queries: Queries, hit_list: list[Hit]) -> list[Hit]:
        # Sort hit list based on the spelling errors amount and return first 1000 entries
        spelling_error_ordered_hit_list = sorted(hit_list, key=lambda hit: hit.corpus_entry.spelling_errors_count)
        new_hit_list = spelling_error_ordered_hit_list[:1000]
        new_hit_list = sorted(new_hit_list, reverse=True, key=lambda hit: hit.score)
        return new_hit_list
