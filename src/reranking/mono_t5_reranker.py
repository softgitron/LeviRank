from reranking.reranker import Reranker
from reranking.special_environment_helper import SpecialEnvironmentHelper
from indexing.hit import Hit


class MonoT5Reranker(Reranker):
    t5_special_environment: SpecialEnvironmentHelper

    def __init__(self):
        self.t5_special_environment = SpecialEnvironmentHelper("./src/special_environments/t5_reranker", "./mono_t5_reranker.py")

    def rerank(self, query: str, hit_list: list[Hit]) -> list[Hit]:
        return self.t5_special_environment.rerank(query, hit_list)
