from datetime import datetime
from io import TextIOWrapper
import json
import re
import constants
from corpus_entry import CorpusEntry
from corpus_premise import CorpusPremise
from corpus_context import CorpusContext

class Corpus:
    _corpus_file: TextIOWrapper

    def __init__(self, corpus_file_path: str = constants.CORPUS_FILE_LOCATION):
        self.open_corpus_file(corpus_file_path)

    def open_corpus_file(self, corpus_file_path: str) -> None:
        try:
            self._corpus_file = open(corpus_file_path, "r")
            
            # Read title line away
            self._corpus_file.readline()
        except OSError as error:
            print(error)
            print("Couldn't open corpus file, is the file path correct?")
            exit(1)

    def __iter__(self):
        return self

    def __next__(self):
        corpus_entry = CorpusEntry()

        line = self._corpus_file.readline()

        # Check, have we reached the end
        if line == "":
            raise StopIteration

        # Remove line change
        line = line[:-1]

        # Clean bad JSON quotes
        
        try:
        
            # Parse id
            line_index = 0
            while line[line_index] != ",":
                line_index += 1
            corpus_entry.id = line[0:line_index]

            # Parse conclusion
            line_index += 1
            conclusion_start_index = line_index
            mark = ","
            if line[line_index] == '"':
                mark = '"'
                line_index += 1
            while line[line_index] != mark:
                line_index += 1
            corpus_entry.conclusion = line[conclusion_start_index:line_index].strip("\"")

            line_split = line[line_index + 1:].lstrip(",")
            json_split_1 = re.findall(r"\[{'text'.*?}\]", line_split)[0]
            json_split_2 = re.findall(r",\"{.*?}\",", line_split)[0].strip(",")
            json_split_3 = re.findall(r"\[{'sent_id'.*?}\]", line_split)[0]

            # Parse premises
            premises_json = json_split_1
            premises_json = self._clean_json(premises_json)
            premises_json_list = json.loads(premises_json)
            premises_list = []
            for premise_json_entry in premises_json_list:
                premise = CorpusPremise()
                premise.text = premise_json_entry["text"]
                premise.stance = premise_json_entry["stance"]
                premises_list.append(premise)
            corpus_entry.premises = premises_list

            # Parse context
            context_text = json_split_2
            context_text = self._clean_json(context_text)
            context_json = json.loads(context_text)
            context = CorpusContext()
            context.acquisition_time = datetime.strptime(context_json["acquisitionTime"], "%Y-%m-%dT%H:%M:%S%z")
            context.discussion_title = context_json["discussionTitle"]
            context.mode = context_json["mode"]
            context.source_domain = context_json["sourceDomain"]
            context.source_text = context_json["sourceText"]
            context.source_text_conclusion_start = context_json["sourceTextConclusionStart"]
            context.source_text_conclusion_end = context_json["sourceTextConclusionEnd"]
            context.source_text_premise_start = context_json["sourceTextPremiseStart"]
            context.source_text_premise_end= context_json["sourceTextPremiseEnd"]
            context.source_title = context_json["sourceTitle"]
            context.source_url = context_json["sourceUrl"]
            corpus_entry.context = context

            # Parse sentences
            sentences_json = json_split_3
            sentences_json = self._clean_json(sentences_json)
            sentences_json_list = json.loads(sentences_json)
            sentences_list = []
            for sentence_json_entry in sentences_json_list:
                sentence = sentence_json_entry["sent_text"]
                sentences_list.append(sentence)
            corpus_entry.sentences = sentences_list

        except Exception:
            corpus_entry = None

        return corpus_entry

    def _clean_json(self, json_string: str) -> str:
        # Convert double quotion marks to single quotion marks
        cleaned_json_string = re.sub(r": \"", ": '", json_string)
        cleaned_json_string = re.sub(r"\", ", "', ", cleaned_json_string)
        cleaned_json_string = re.sub(r"\"\"}", "'}", cleaned_json_string)
        # Remove all double quotion marks
        cleaned_json_string = cleaned_json_string.replace("\"", "")
        # Remove escaped space
        cleaned_json_string = cleaned_json_string.replace("\\xa0", " ")
        # Remove escape characters
        cleaned_json_string = cleaned_json_string.replace("\\", "")
        # Convert single quotes to double quotes, for JSON parsing
        cleaned_json_string = re.sub(r"([{:,][{:\s]?)'", "\\1\"", cleaned_json_string)
        cleaned_json_string = re.sub(r"'([^0-9a-zA-Z\s\(\)])", "\"\\1", cleaned_json_string)
        # Fix leak caused by quote at the end
        cleaned_json_string = re.sub(r"([a-z]{3,6})\"([^\"\[{0-9]{4})", "\\1\\2", cleaned_json_string)
        return cleaned_json_string

if __name__ == '__main__':
    corpus = Corpus()
    iteration = 0
    errors = 0
    for entry in corpus:
        if entry == None:
            errors += 1
        iteration += 1
        if iteration % 1000 == 0:
            print(f"Iteration: {iteration}, errors: {errors}")