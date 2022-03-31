from abc import ABC, abstractmethod


class QueryExpander:
    @abstractmethod
    def expand(self, query) -> str:
        pass
