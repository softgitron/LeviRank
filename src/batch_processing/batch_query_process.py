from indexing.index import Index
from preprocessing.preprocessor import Preprocessor
from batch_processing.topics import Topics
from results.result import Result
from results.results import Results


class BatchQueryProcess:
    index: Index = None

    def __init__(self, index):
        self.index = index

    def execute(self, input_path: str, output_path: str, method: str):
        # Load topics
        topics = Topics(title_file_path=input_path)

        # Prepare results objects
        results = Results()
        results.method = method

        print("Starting batch processing")
        topic_amount = len(topics.topic_list)
        for topic_number, topic in enumerate(topics):
            query_input = topic.title

            # Search using the query
            hit_list = self.index.query(query_input)

            # Write results to the string
            for rank, hit in enumerate(hit_list):
                # Add at maximum 1000 results
                if rank >= 1000:
                    break

                # Create and add result to results
                result = Result(topic.number, "Q0", hit.id,
                                rank + 1, hit.score)
                results.append(result)

            print(f"Analyzed topic {topic_number + 1}/{topic_amount}")

        # Save results
        results.write_results_csv(output_path)
