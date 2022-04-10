from reranking.reranker import Reranker
from indexing.hit import Hit


class MultiReranker(Reranker):
    rerankers = list[Reranker]

    def __init__(self, rerankers: list[Reranker]) -> None:
        self.rerankers = rerankers

    def rerank(self, query: str, hit_list: list[Hit]) -> list[Hit]:
        latest_reranked_hit_list = hit_list
        for reranker in self.rerankers:
            latest_reranked_hit_list = reranker.rerank(
                query, latest_reranked_hit_list)

        return latest_reranked_hit_list
