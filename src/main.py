#!/bin/python3
from corpus import Corpus
import constants
from indexing.bm25_indexer import BM25Indexer
from indexing.index import Index
from preprocessing.general_preprocessor import GeneralPreprocessor
from preprocessing.preprocessor import Preprocessor


class Main:
    corpus: Corpus = None
    preprocessor: Preprocessor = None
    indexer_type = None
    index: Index = None

    def __init__(self) -> None:
        self.main()

    def main(self) -> None:
        while True:
            print("""
Main menu:
1. Corpus options
2. Preprocessing options
3. Indexing options
4. Query options
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
                self.corpus = self.corpus.write_corpus_pickle(
                    constants.CORPUS_PICKLE_FILE_LOCATION)
                print("Saved.")
            elif option == "2":
                file_path = input("Enter file path: ")
                self.corpus = self.corpus.write_corpus_pickle(
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
2. Preprocess corpus
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                self.preprocessor = GeneralPreprocessor(verbose=True)
                print("Preprocessor set to generic preprocessor.")
            elif option == "2":
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
                    self.indexer_type, self.corpus, index_file_path)
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
                    self.indexer_type, self.corpus, index_file_path)
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
1. Query using text
2. Query using id
0. Go back""")
            option = input("Select the operation: ")
            if option == "1":
                if not self.corpus:
                    print("Corpus must be loaded, before query can be issued")
                    continue
                elif not self.index:
                    print("Index must be loaded, before query can be made")
                    continue
                if self.preprocessor:
                    query_input = input("Enter text query: ")
                    query_input = self.preprocessor.process(query_input)
                    self.index.query(query_input, verbose=True)
                else:
                    print(
                        "Note, it is recommended that preprocessor is set before textual queries")
                    query_input = input("Enter text query: ")
                    self.index.query(query_input, verbose=True)
            elif option == "2":
                if not self.corpus:
                    print("Corpus must be loaded, before query can be issued")
                    continue
                query_input = input("Enter id query: ")
                print(self.corpus.entries_by_id.get(query_input))
            elif option == "0":
                break
            else:
                print("Unknown option")


Main()
