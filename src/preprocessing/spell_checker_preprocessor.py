from language_tool_python import LanguageTool

from corpus.corpus_entry import CorpusEntry


class SpellCheckerPreprocessor:
    spell_checker: LanguageTool

    def __init__(self, language_tool_address=None) -> None:
        if not language_tool_address:
            # Start new language server
            self.spell_checker = LanguageTool(
                "en-US", config={'cacheSize': 1000, 'pipelineCaching': True})
        else:
            self.spell_checker = LanguageTool(
                "en-US", remote_server=language_tool_address)

    def get_server_url(self):
        return self.spell_checker._url[:-3]

    def score_corpus_entry(self, corpus_entry: CorpusEntry):
        # Try again 3 times
        for attempt in range(3):
            try:
                spelling_errors = self.spell_checker.check(corpus_entry.contents)
                corpus_entry.spelling_errors_count = len(spelling_errors)
                break
            except Exception as error:
                print("Error occurred while trying to evaluate corpus entry.")
                print(f"Trying again {attempt + 1}/3")
                print(error)
                corpus_entry.spelling_errors_count = 999