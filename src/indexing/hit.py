from corpus.corpus import CorpusEntry


class Hit:
    id: str
    score: float
    corpus_entry: CorpusEntry

    def __init__(self, id, score) -> None:
        self.id = id
        self.score = score
