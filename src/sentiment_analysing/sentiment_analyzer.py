from abc import ABC, abstractmethod
from indexing.queries import Queries


class SentimentAnalyzer:
    @abstractmethod
    def analyze(self, queries: Queries, passage: str) -> str:
        pass