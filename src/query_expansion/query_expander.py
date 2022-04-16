from abc import ABC, abstractmethod
from indexing.queries import Queries


class QueryExpander:
    @abstractmethod
    def expand(self, queries: Queries) -> str:
        pass
