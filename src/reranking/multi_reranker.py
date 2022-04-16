from reranking.reranker import Reranker
from indexing.hit import Hit
from indexing.queries import Queries


class MultiReranker(Reranker):
    rerankers = list[Reranker]

    def __init__(self, rerankers: list[Reranker]) -> None:
        self.rerankers = rerankers

    def rerank(self, queries: Queries, hit_list: list[Hit]) -> list[Hit]:
        latest_reranked_hit_list = hit_list
        for reranker in self.rerankers:
            latest_reranked_hit_list = reranker.rerank(
                queries, latest_reranked_hit_list)

        return latest_reranked_hit_list
