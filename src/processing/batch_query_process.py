import os
from indexing.index import Index
from preprocessing.preprocessor import Preprocessor
from processing.topics import Topics


class BatchQueryProcess:
    index: Index = None
    preprocessor: Preprocessor = None

    def __init__(self, index, preprocessor=None):
        self.index = index
        self.preprocessor = preprocessor

    def execute(self, input_path: str, output_path: str, method: str):
        # Load topics
        topics = Topics(title_file_path=input_path)

        # Preparing results
        results_string = ""

        topic_amount = len(topics.topic_list)
        for topic_number, topic in enumerate(topics):
            query_input = topic.title

            # Do preprocessing for the query, if preprocessor is available
            if self.preprocessor:
                query_input = self.preprocessor.process(query_input)

            # Search using the query
            hit_list = self.index.query(query_input)

            # Write results to the string
            for rank, hit in enumerate(hit_list):
                results_string += f"{topic.number} Q0 {hit.id} {rank + 1} {hit.score} {method}\n"

            print(f"Analyzed topic {topic_number + 1}/{topic_amount}")

        # Remove final line ending
        results_string = results_string[:-1]

        # Open results file for writing
        try:
            results_file = open(output_path, "w")
        except OSError as error:
            print(error)
            print("Couldn't open results file for writing, is the file path correct?")
            exit(1)

        # Write results
        results_file.write(results_string)
        results_file.close()

        print(f'Results saved to the "{output_path}"')
