from abc import ABC, abstractmethod
from indexing.hit import Hit


class Reranker:
    @abstractmethod
    def rerank(self, query: str, hit_list: list[Hit]) -> list[Hit]:
        pass
