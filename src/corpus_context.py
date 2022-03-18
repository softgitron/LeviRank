from datetime import datetime


class CorpusContext:
    acquisition_time: datetime
    discussion_title: str
    mode: str
    source_domain: str
    source_text: str
    source_text_conclusion_start: int
    source_text_conclusion_end: int
    source_text_premise_start: int
    source_text_premise_end: int
    source_title: str
    source_url: str