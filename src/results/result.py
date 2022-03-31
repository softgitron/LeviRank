class Result:
    topic_number: int
    stance: str = "Q0"
    document_id: str
    rank: int
    score: float

    def __init__(self, topic_number, stance, document_id, rank, score):
        self.topic_number = topic_number
        self.stance = stance
        self.document_id = document_id
        self.rank = rank
        self.score = score

    def __repr__(self) -> str:
        return f"qid: {self.topic_number}, stance: {self.stance}, doc: {self.document_id}, rank: {self.rank}, score: {self.score}"
