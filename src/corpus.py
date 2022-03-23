import pickle
import json
import constants
from corpus_entry import CorpusEntry


class Corpus:
    entries: list[CorpusEntry]
    entries_by_id: dict[CorpusEntry]

    def __init__(self, corpus_file_path: str = constants.CORPUS_PICKLE_FILE_LOCATION):
        # Read file according to extension.
        if corpus_file_path.endswith(".jsonl"):
            self._read_corpus_jsonl(corpus_file_path)
        else:
            self._read_corpus_pickle(corpus_file_path)
        self.update_id_dictionary()

    def _read_corpus_jsonl(self, corpus_file_path: str) -> None:
        try:
            corpus_file = open(corpus_file_path, "r")
        except OSError as error:
            print(error)
            print("Couldn't open corpus file in jsonl format, is the file path correct?")
            exit(1)

        entries = []
        for line in corpus_file:
            # Remove line change
            line = line[:-1]

            # Parse corpus entry
            corpus_entry = CorpusEntry()
            corpus_entry_json = json.loads(line)
            corpus_entry.id = corpus_entry_json["id"]
            corpus_entry.contents = corpus_entry_json["contents"]
            corpus_entry.chat_noir_url = corpus_entry_json["chatNoirUrl"]

            # If no contents, skip the entry
            if not corpus_entry.contents:
                continue
            entries.append(corpus_entry)

        self.entries = entries
        corpus_file.close()

    def _read_corpus_pickle(self, corpus_file_path: str) -> None:
        try:
            corpus_file = open(corpus_file_path, "rb")
        except OSError as error:
            print(error)
            print("Couldn't open corpus file in pickle format, is the file path correct?")
            exit(1)

        self.entries = pickle.load(corpus_file)
        corpus_file.close()

    def update_id_dictionary(self):
        self.entries_by_id = {}
        for entry in self.entries:
            self.entries_by_id[entry.id] = entry

    def write_corpus_pickle(self, corpus_file_path: str) -> None:
        try:
            corpus_file = open(corpus_file_path, "wb")
        except OSError as error:
            print(error)
            print("Couldn't open corpus file, is the file path correct?")
            exit(1)

        pickle.dump(self.entries, corpus_file)
        corpus_file.close()

    def __iter__(self):
        return iter(self.entries)

    def length(self) -> int:
        return len(self.entries)


if __name__ == '__main__':
    if True == False:
        # Load default jsonl
        corpus = Corpus(constants.CORPUS_JSONL_FILE_LOCATION)
        # Write loaded data to pickle file
        corpus.write_corpus_pickle(constants.CORPUS_PICKLE_FILE_LOCATION)
        # Load just created pickle to verify functionality
        corpus._read_corpus_pickle(constants.CORPUS_PICKLE_FILE_LOCATION)
    else:
        # Load corpus using pickle
        corpus = Corpus(corpus_file_path=constants.CORPUS_PICKLE_FILE_LOCATION)
