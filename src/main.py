#!/bin/python3
import sys
import os
import argparse
from batch_processing.batch_query_process import BatchQueryProcess
import constants
from corpus.corpus import Corpus
from indexing.bm25_indexer import BM25Indexer
from indexing.index import Index
from preprocessing.general_preprocessor import GeneralPreprocessor
from preprocessing.preprocessor import Preprocessor
from reranking.distilbert_reranker import DistilbertReranker
from reranking.mono_t5_reranker import MonoT5Reranker
from reranking.duo_t5_reranker import DuoT5Reranker
from reranking.multi_reranker import MultiReranker
from query_expansion.query_expander import QueryExpander
from query_expansion.wordnet_expander import WordnetExpander
from query_expansion.advanced_wordnet_expander import AdvancedWordnetExpander
from results.evaluate_results import EvaluateResults
from reranking.spelling_error_reranker import SpellingErrorReranker
from sentiment_analysing.general_sentiment_analyzer import GeneralSentimentAnalyzer
from preprocessing.baseline_preprocessor import BaselinePreprocessor


class Main:
    corpus: Corpus = None
    preprocessor: Preprocessor = None
    indexer_type = None
    index: Index = None
    results_file_path: str = None

    def __init__(self) -> None:
        # Set standard environment flags
        os.environ["TOKENIZERS_PARALLELISM"] = "true"

        if len(sys.argv) > 1:
            # If there are arguments, proceed to batch processing
            self.process_with_arguments()
        else:
            # If there are no arguments, proceed to main menu
            self.main_menu()

    def process_with_arguments(self) -> None:
        parser = argparse.ArgumentParser(description="Process search queries.")
        parser.add_argument("-i", dest="input_directory", required=True,
                            help="Input directory of the queries.")
        parser.add_argument("-o", dest="output_directory", required=True,
                            help="Output directory, where results will be stored.")

        args = parser.parse_args()
        input_path = os.path.join(
            args.input_directory, constants.INPUT_FILE_NAME)
        output_path = os.path.join(
            args.output_directory, constants.OUTPUT_FILE_NAME)

        # Load default corpus
        corpus = Corpus()
        sentiment_analyzer = GeneralSentimentAnalyzer()
        if constants.METHOD_NAME == "BM25":
            mono_t5_reranker = MonoT5Reranker()
            index = Index(BM25Indexer, corpus=corpus, preprocessor=GeneralPreprocessor(),)
            process = BatchQueryProcess(index, sentiment_analyzer)
            process.execute(input_path, output_path, constants.METHOD_NAME)
        elif constants.METHOD_NAME == "BM25_with_mono_t5":
            # advanced_wordnet_expander = AdvancedWordnetExpander()
            mono_t5_reranker = MonoT5Reranker()
            index = Index(BM25Indexer, corpus=corpus, preprocessor=GeneralPreprocessor(),
                        reranker=mono_t5_reranker)
            process = BatchQueryProcess(index, sentiment_analyzer)
            process.execute(input_path, output_path, constants.METHOD_NAME)
        elif constants.METHOD_NAME == "BM25_with_duo_t5":
            duo_t5_reranker = DuoT5Reranker()
            distilbert_reranker = DistilbertReranker()
            multi_reranker = MultiReranker([duo_t5_reranker, distilbert_reranker])
            index = Index(BM25Indexer, corpus=corpus, preprocessor=GeneralPreprocessor(),
                        reranker=multi_reranker)
            process = BatchQueryProcess(index, sentiment_analyzer)
            process.execute(input_path, output_path, constants.METHOD_NAME)
        elif constants.METHOD_NAME == "BM25_with_duo_t5_and_advanced_expander":
            advanced_wordnet_expander = AdvancedWordnetExpander()
            spelling_error_reranker = SpellingErrorReranker()
            mono_t5_reranker = MonoT5Reranker()
            duo_t5_reranker = DuoT5Reranker()
            multi_reranker = MultiReranker([spelling_error_reranker, mono_t5_reranker, duo_t5_reranker])
            index = Index(BM25Indexer, corpus=corpus, preprocessor=GeneralPreprocessor(),
                        reranker=multi_reranker)
            process = BatchQueryProcess(index, sentiment_analyzer)
            process.execute(input_path, output_path, constants.METHOD_NAME)
        elif constants.METHOD_NAME == "levirank_baseline":
            mono_t5_reranker = MonoT5Reranker()
            duo_t5_reranker = DuoT5Reranker()
            multi_reranker = MultiReranker([mono_t5_reranker, duo_t5_reranker])
            preprocessor = BaselinePreprocessor()
            index = Index(BM25Indexer, corpus=corpus, preprocessor=preprocessor,
                        reranker=multi_reranker)
            process = BatchQueryProcess(index, sentiment_analyzer)
            process.execute(input_path, output_path, constants.METHOD_NAME)

    def main_menu(self) -> None:
        while True:
            print("""
Main menu:
1. Corpus options
2. Preprocessing options
3. Indexing options
4. Query options
5. Batch process queries
6. Evaluate batch processing results
0. Quit the program""")
            option = input("Select the operation: ")
            if option == "1":
                self.corpus_options_menu()
            elif option == "2":
                self.preprocessing_options_menu()
            elif option == "3":
                self.indexing_options_menu()
            elif option == "4":
                self.query_options()
            elif option == "5":
                self.batch_process()
            elif option == "6":
                self.evaluate_results()
            elif option == "0":
                break
            else:
                print("Unknown option")

    def corpus_options_menu(self):
        while True:
            print("""
Corpus options:
1. Load corpus from the file options
2. Save corpus to the file options
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.corpus_load_options_menu()
            elif option == "2":
                self.corpus_save_options_menu()
            elif option == "0":
                break
            else:
                print("Unknown option")

    def corpus_load_options_menu(self):
        while True:
            print("""
Corpus options:
1. Load corpus from default jsonl file
2. Load corpus from default pickle file
3. Load file from user defined file
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.corpus = Corpus(
                    corpus_file_path=constants.CORPUS_JSONL_FILE_LOCATION)
                print("Loaded.")
            elif option == "2":
                self.corpus = Corpus(
                    corpus_file_path=constants.CORPUS_PICKLE_FILE_LOCATION)
                print("Loaded.")
            elif option == "3":
                file_path = input("Enter file path: ")
                self.corpus = Corpus(corpus_file_path=file_path)
                print("Loaded.")
            elif option == "0":
                break
            else:
                print("Unknown option")

    def corpus_save_options_menu(self):
        while True:
            print("""
Corpus options:
1. Save corpus to default pickle file
2. Save corpus to user defined file
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.corpus.write_corpus_pickle(
                    constants.CORPUS_PICKLE_FILE_LOCATION)
                print("Saved.")
            elif option == "2":
                file_path = input("Enter file path: ")
                self.corpus.write_corpus_pickle(
                    file_path)
                print("Saved.")
            elif option == "0":
                break
            else:
                print("Unknown option")

    def preprocessing_options_menu(self):
        while True:
            print("""
Preprocessing options:
1. Set preprocessor to general preprocessor
2. Set preprocessor to general parallel preprocessor
3. Preprocess corpus
0. Go back""")
            # Update index preprocessor, if index is defined
            if self.index:
                self.index.preprocessor = self.preprocessor
            option = input("Select the operation: ")
            if option == "1":
                self.preprocessor = GeneralPreprocessor(verbose=True)
                print("Preprocessor set to generic preprocessor.")
            elif option == "2":
                self.preprocessor = GeneralPreprocessor(
                    verbose=True, parallel=True)
                print("Preprocessor set to generic parallel preprocessor.")
            elif option == "3":
                if not self.preprocessor:
                    print(
                        "Can't start preprocessing, because preprocessor is not selected.")
                    continue
                elif not self.corpus:
                    print("Can't start preprocessing, because corpus is not loaded.")
                    continue
                print("Starting preprocessing, this may take a while...")
                self.corpus = self.preprocessor.process_corpus(self.corpus)
                print("Preprocessed.")
            elif option == "0":
                break
            else:
                print("Unknown option")

    def indexing_options_menu(self):
        while True:
            print("""
Indexing options:
1. Set indexer type
2. Start indexing
3. Load index from the file
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.indexer_type_menu()
            elif option == "2":
                if not self.corpus:
                    print("Corpus must be loaded before indexing.")
                    continue
                elif not self.indexer_type:
                    print("Indexer type must be set, before indexing can be started.")
                    continue
                index_file_path = input(
                    "Enter path for the index file or leave empty for the default: ")
                if not index_file_path:
                    index_file_path = constants.INDEX_FILE_LOCATION
                self.index = Index(
                    self.indexer_type, self.corpus, preprocessor=self.preprocessor, index_file_path=index_file_path)
                self.index.update()
                print("Indexing has been completed.")
            elif option == "3":
                if not self.indexer_type:
                    print(
                        "indexer must be selected, before index can be loaded from the file")
                    continue
                index_file_path = input(
                    "Enter path for the index file or leave empty for the default: ")
                if not index_file_path:
                    index_file_path = constants.INDEX_FILE_LOCATION
                self.index = Index(
                    self.indexer_type, self.corpus, preprocessor=self.preprocessor, index_file_path=index_file_path)
            elif option == "0":
                break
            else:
                print("Unknown option")

    def indexer_type_menu(self):
        while True:
            print("""
Corpus options:
1. Set indexer type as BM25
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.indexer_type = BM25Indexer
                print("Indexer type set as BM25")
            elif option == "0":
                break
            else:
                print("Unknown option")

    def query_options(self):
        while True:
            print("""
Corpus options:
1. Set query expander type
2. Query using text
3. Query using id
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.query_expander_type_menu()
            elif option == "2":
                if not self.corpus:
                    print("Corpus must be loaded, before query can be issued")
                    continue
                elif not self.index:
                    print("Index must be loaded, before query can be made")
                    continue
                if not self.index.preprocessor:
                    print(
                        "Note, it is recommended that preprocessor is set before textual queries")
                if not self.index.query_expander:
                    print(
                        "Note, it is recommended that query expander is set before textual queries")
                query_input = input("Enter text query: ")
                self.index.query(query_input, verbose=True)
            elif option == "3":
                if not self.corpus:
                    print("Corpus must be loaded, before query can be issued")
                    continue
                query_input = input("Enter id query: ")
                print(self.corpus.entries_by_id.get(query_input))
            elif option == "0":
                break
            else:
                print("Unknown option")

    def query_expander_type_menu(self):
        if not self.index:
            print("Index must be loaded, before query expander can be set")
            return
        while True:
            print("""
Corpus options:
1. Set query expander type to Wordnet
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.index.query_expander = WordnetExpander()
                print("Query expander type set to Wordnet")
            elif option == "0":
                break
            else:
                print("Unknown option")

    def batch_process(self):
        if not self.index:
            print("Index must be loaded before batch processing")
            return
        if not self.index.preprocessor:
            print("Preprocessor is recommended to be defined before batch processing")
        if not self.index.query_expander:
            print("Query expander is recommended to be defined before batch processing")
        input_file_path = input("Please provide path for the topics file: ")
        self.results_file_path = input(
            "Please provide path for the results file: ")
        method = input("Please provide some name for the used method: ")

        process = BatchQueryProcess(self.index)
        process.execute(input_file_path, self.results_file_path, method)

    def evaluate_results(self):
        if not self.corpus:
            print(
                "Corpus must be loaded before evaluation in order to remove unfair entries")
            return
        if not self.results_file_path:
            self.results_file_path = input(
                "Results file path is not known, please provide the path: ")
        evaluation_file_path = input(
            "Please provide the path for the evaluation file: ")

        evaluate_results = EvaluateResults()
        evaluate_results.evaluate(
            self.results_file_path, evaluation_file_path, self.corpus)

        save_results = input("Would you like to save results (y/n): ").lower()
        if save_results == "y":
            evaluation_results_file = input(
                "Please input path for the evaluation results: ")
            evaluate_results.save_results_to_file(evaluation_results_file)


Main()
