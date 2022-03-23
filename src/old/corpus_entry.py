from corpus_premise import CorpusPremise
from corpus_context import CorpusContext

class CorpusEntry:
    id: str
    conclusion: str
    premises: list[CorpusPremise]
    context: CorpusContext
    sentences: list[str]