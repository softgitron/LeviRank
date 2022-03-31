from corpus import Corpus


class Evaluations:
    entries: dict[dict[int]]

    def __init__(self, csv_path: str):
        self._load_evaluations_csv(csv_path)

    def _load_evaluations_csv(self, csv_path: str):
        # Open results file for reading
        try:
            results_file = open(csv_path, "r")
        except OSError as error:
            print(error)
            print("Couldn't open evaluations file for reading, is the file path correct?")
            exit(1)

        # Empty current results
        self.entries = {}

        for line in results_file:
            # Split lines to tokens
            tokens = line[:-1].split(" ")
            topic_number = int(tokens[0])
            # Second field is always unused
            document_id = tokens[2]
            relevance_judgement = int(tokens[3])

            # First by topics
            if not self.entries.get(topic_number):
                self.entries[topic_number] = {}

            # Then by document ids
            if not self.entries.get(topic_number).get(document_id):
                self.entries[topic_number][document_id] = {}

            # Append new judgement
            self.entries[topic_number][document_id] = relevance_judgement

        # Finally close the file
        results_file.close()

    def clean_non_essential_evaluations_using_corpus(self, corpus: Corpus) -> float:
        # Create list of document ids in the corpus without section id
        document_ids = []
        for id in corpus.entries_by_id.keys():
            id_without_section_id = id.split("_")[0]
            document_ids.append(id_without_section_id)

        # Calculate how many judgments can be found from the given corpus
        overall_document_amount = 0
        corpus_document_amount = 0
        for document_dictionary in self.entries.values():
            documents_to_delete = []
            for document_id in document_dictionary.keys():
                overall_document_amount += 1
                if document_id in document_ids:
                    corpus_document_amount += 1
                else:
                    documents_to_delete.append(document_id)
            # Delete entries that are not part of the corpus
            for document_to_delete in documents_to_delete:
                del document_dictionary[document_to_delete]

        percentage_float = corpus_document_amount / overall_document_amount
        percentage = round(percentage_float * 100, 2)
        print(
            f"{percentage}% of the evaluations were available in the corpus")
        print("Extra evaluations have now been deleted")

        return percentage_float
