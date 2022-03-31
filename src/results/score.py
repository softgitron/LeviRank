class Score:
    query_id: int
    score: float
    relevance_score: float
    coverage_score: float

    def __init__(self, query_id, score, relevance_score, coverage_score) -> None:
        self.query_id = query_id
        self.score = score
        self.relevance_score = relevance_score
        self.coverage_score = coverage_score
