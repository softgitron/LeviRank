from abc import ABC, abstractmethod
from indexing.hit import Hit
from indexing.queries import Queries


class Reranker:  
    @abstractmethod
    def rerank(self, queries: Queries, hit_list: list[Hit]) -> list[Hit]:
        pass
