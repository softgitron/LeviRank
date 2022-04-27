from indexing.index import Index
from sentiment_analysing.sentiment_analyzer import SentimentAnalyzer
from preprocessing.preprocessor import Preprocessor
from batch_processing.topics import Topics
from results.result import Result
from results.results import Results


class BatchQueryProcess:
    index: Index = None
    sentiment_analyzer: SentimentAnalyzer = None

    def __init__(self, index: Index, sentiment_analyzer: SentimentAnalyzer):
        self.index = index
        self.sentiment_analyzer = sentiment_analyzer

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

                # Analyze sentiments
                queries = self.index.expand_query(query_input)
                if self.sentiment_analyzer:
                    sentiment = self.sentiment_analyzer.analyze(queries, hit.corpus_entry.contents)
                else:
                    sentiment = "Q0"

                # Create and add result to results
                result = Result(topic.number, sentiment, hit.id,
                                rank + 1, hit.score)
                results.append(result)

            print(f"Analyzed topic {topic_number + 1}/{topic_amount}")

        # Save results
        results.write_results_csv(output_path)
