from indexing.hit import Hit
from sentence_transformers import SentenceTransformer, util


class DistilbertReranker:
    model: any

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            'sentence-transformers/msmarco-distilbert-base-tas-b')

    def rerank(self, query: str, hit_list: list[Hit]) -> list[Hit]:
        # Receive original preprocessed texts
        query_texts = []
        for hit in hit_list:
            corpus_entry_content = hit.corpus_entry.contents
            query_texts.append(corpus_entry_content)

        # Form document text collection object
        docs_object = self.model.encode(query_texts)

        # Form query object
        query_object = self.model.encode(query)

        # Form new score rankings
        new_scores = util.dot_score(query_object, docs_object)[
            0].cpu().tolist()

        # Combine hit list with new scores and order
        new_scores_and_hit_list = list(zip(hit_list, new_scores))
        new_scores_and_hit_list = sorted(
            new_scores_and_hit_list, key=lambda tupple: tupple[1], reverse=True)

        # Form new hit list based on the new scores
        reranked_hit_list = []
        for id, new_score_and_old_hit in enumerate(new_scores_and_hit_list):
            hit = Hit(id, new_score_and_old_hit[1])
            hit.corpus_entry = new_score_and_old_hit[0].corpus_entry
            reranked_hit_list.append(hit)

        return reranked_hit_list
