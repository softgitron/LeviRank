from corpus import Corpus


class Hit:
    id: str
    score: float
    corpus: Corpus

    def __init__(self, id, score) -> None:
        self.id = id
        self.score = score
