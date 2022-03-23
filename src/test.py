#!/bin/python3
import constants
from corpus import Corpus
from indexing.index import Index
from indexing.bm25_indexer import BM25Indexer
from preprocessing.general_preprocessor import GeneralPreprocessor
from processing.batch_query_process import BatchQueryProcess

TEST = 4

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
        BM25Indexer, index_file_path="./data/index/preprocessed_index")
    preprocessor = GeneralPreprocessor()
    process = BatchQueryProcess(index, preprocessor)
    process.execute("./data/titles/topics.xml",
                    "./data/output/results.txt", "testing")
