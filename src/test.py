#!/bin/python3
import constants
from corpus import Corpus
from corpus_entry import CorpusEntry
from indexing.index import Index
from indexing.bm25_indexer import BM25Indexer
from preprocessing.general_preprocessor import GeneralPreprocessor
from batch_processing.batch_query_process import BatchQueryProcess
from query_expansion.wordnet_expander import WordnetExpander
from results.evaluate_results import EvaluateResults
from results.evaluations import Evaluations
from results.results import Results

TEST = 10

if (TEST == 0):
    # Indexing test
    # Load corpus via default fashion.
    corpus = Corpus(corpus_file_path=constants.CORPUS_JSONL_FILE_LOCATION)
    # Create new index
    index = Index(BM25Indexer, corpus)
    index.update()
elif(TEST == 1):
    # Index building test
    index = Index(BM25Indexer)
elif(TEST == 2):
    # Preprocessing test
    corpus = Corpus(corpus_file_path=constants.CORPUS_JSONL_FILE_LOCATION)
    # Execute generall preprocessing
    general_preprocessing = GeneralPreprocessor()
    corpus = general_preprocessing.process_corpus(corpus)
elif(TEST == 3):
    # Test queyring
    corpus = Corpus(corpus_file_path="./data/corpus/pp.dat")
    index = Index(BM25Indexer, corpus, "./data/index/preprocessed_index")
    index.query("car", verbose=True)
elif(TEST == 4):
    # Test processing pipeline
    index = Index(
        BM25Indexer, preprocessor=GeneralPreprocessor(), index_file_path="./data/index/preprocessed_index")
    process = BatchQueryProcess(index)
    process.execute("./data/topics_21.xml",
                    "./data/results_21.txt", "testing")
elif(TEST == 5):
    # Test loading of the results file
    results = Results()
    results.load_results_csv("./data/results.txt")
    print(results.entries[0])
elif(TEST == 6):
    # Test calculating corpus coverage based on the relevance judgments
    corpus = Corpus(corpus_file_path="./data/pp_22.dat")
    evaluations = Evaluations("./data/relevance_judgments_21.qrels")
    evaluations.compare_similarity_with_corpus(corpus)
elif(TEST == 7):
    # Test evaluate results class
    corpus = Corpus(corpus_file_path="./data/pp_22.dat")
    evaluate_results = EvaluateResults()
    evaluate_results.evaluate("./data/results_21.txt",
                              "./data/relevance_judgments_21.qrels", corpus)
    evaluate_results.save_results_to_file("./data/evaluation_results_21.txt")
elif(TEST == 8):
    # Test parallel processing pipeline
    corpus = Corpus(corpus_file_path=constants.CORPUS_JSONL_FILE_LOCATION)
    # Execute generall preprocessing parallel
    general_preprocessing = GeneralPreprocessor(verbose=True, parallel=True)
    corpus = general_preprocessing.process_corpus(corpus)
    input("Waiting any key...")
elif(TEST == 9):
    # Test corpus entry generation
    corpus_entry = CorpusEntry()
    corpus_entry.id = "doc 123"
    corpus_entry.contents = "Test contents"
    corpus_entry.chat_noir_url = "https://test.com"
    corpus_entry.spelling_errors_count = 2
    print(corpus_entry)
    print(corpus_entry.get("id"))
elif(TEST == 10):
    # Test queyring with preprocessing and query expansion
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    index = Index(BM25Indexer, corpus, preprocessor=GeneralPreprocessor(
    ), query_expander=WordnetExpander(), index_file_path="./data/index")
    index.query("Should I buy steel or ceramic knives?", verbose=True)
