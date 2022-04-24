#!/bin/python3
import os
import constants
from corpus.corpus import Corpus
from corpus.corpus_entry import CorpusEntry
from indexing.index import Index
from indexing.bm25_indexer import BM25Indexer
from preprocessing.general_preprocessor import GeneralPreprocessor
from batch_processing.batch_query_process import BatchQueryProcess
from query_expansion.wordnet_expander import WordnetExpander
from query_expansion.advanced_wordnet_expander import AdvancedWordnetExpander
from reranking.distilbert_reranker import DistilbertReranker
from reranking.mono_t5_reranker import MonoT5Reranker
from reranking.multi_reranker import MultiReranker
from results.evaluate_results import EvaluateResults
from results.evaluations import Evaluations
from results.results import Results
from batch_processing.topics import Topics
from indexing.queries import Queries
from indexing.hit import Hit
from reranking.spelling_error_reranker import SpellingErrorReranker
from sentiment_analysing.general_sentiment_analyzer import GeneralSentimentAnalyzer
from preprocessing.baseline_preprocessor import BaselinePreprocessor

TEST = 16

if (TEST == 0):
    # Indexing test
    # Load corpus via default fashion.
    corpus = Corpus()
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
    corpus = Corpus(corpus_file_path="./data/corpus.dat")
    index = Index(BM25Indexer, corpus)
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
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    evaluations = Evaluations("./data/relevance_judgments_21.qrels")
    evaluations.compare_similarity_with_corpus(corpus)
elif(TEST == 7):
    # Test evaluate results class
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    evaluate_results = EvaluateResults()
    evaluate_results.evaluate("./data/results_21.txt",
                              "./data/relevance_judgments_21.qrels", corpus)
    evaluate_results.save_results_to_file("./data/evaluation_results_21.txt")
elif(TEST == 8):
    # Test parallel preprocessing pipeline
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
elif(TEST == 11):
    print(os.getcwd())
    # Test T5 reranker
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    preprocessor = GeneralPreprocessor()
    index = Index(BM25Indexer, corpus, preprocessor=preprocessor,
                  index_file_path="./data/index")
    query = "What is better at reducing fever in children, Ibuprofen or Aspirin?"
    hit_list = index.query(
        query, verbose=True)
    reranker = MonoT5Reranker()
    reranked_hit_list = reranker.rerank(preprocessor.process(query), hit_list)
elif(TEST == 12):
    # Test distilbert reranker
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    preprocessor = GeneralPreprocessor()
    index = Index(BM25Indexer, corpus, preprocessor=preprocessor,
                  index_file_path="./data/index")
    query = "What is better at reducing fever in children, Ibuprofen or Aspirin?"
    hit_list = index.query(query, verbose=True)
    reranker = DistilbertReranker()
    reranked_hit_list = reranker.rerank(preprocessor.process(query), hit_list)
elif(TEST == 13):
    # Test whole pipeline with reranking support
    corpus = Corpus(corpus_file_path="./data/pp_22_old.dat")
    preprocessor = GeneralPreprocessor()
    mono_t5_reranker = MonoT5Reranker()
    distilbert_reranker = DistilbertReranker()
    multi_reranker = MultiReranker([mono_t5_reranker, distilbert_reranker])
    index = Index(BM25Indexer, corpus=corpus, preprocessor=GeneralPreprocessor(),
                  reranker=multi_reranker)
    process = BatchQueryProcess(index)
    process.execute("./data/topics_21.xml",
                    "./data/results_with_rerank_21.txt", "Reranking_test")
    evaluate_results = EvaluateResults()
    evaluate_results.evaluate(
        "./data/results_with_rerank_21.txt", "./relevance_judgments_21.qrels", corpus)
    evaluate_results.save_results_to_file(
        "evaluation_results_21_with_reranking.txt")
elif(TEST == 14):
    # Test advanced wordnet expander
    preprocessor = GeneralPreprocessor()
    query_expander = AdvancedWordnetExpander()

    topics = Topics("./data/topics.xml")

    for topic in topics:
        queries = Queries(topic.title, topic.title)
        queries.preprocessed_query = preprocessor.process(queries.original_query)
        queries.preprocessed_query = query_expander.expand(queries)
        print(f"{queries.original_query} -> {queries.preprocessed_query}")

elif(TEST == 15):
    # Test that spelling error reranker works
    corpus_entry1 = CorpusEntry()
    corpus_entry1.spelling_errors_count = 100
    corpus_entry2 = CorpusEntry()
    corpus_entry2.spelling_errors_count = 50
    hit1 = Hit("1", 1)
    hit1.corpus_entry = corpus_entry1
    hit2 = Hit("2", 2)
    hit2.corpus_entry = corpus_entry2
    hit_list = [hit1, hit2]
    spelling_error_reranker = SpellingErrorReranker()
    spelling_error_reranker.rerank(Queries("", ""), hit_list)
elif(TEST == 16):
    corpus = Corpus(corpus_file_path="./data/corpus.pkl")
    sentiment_analyzer = GeneralSentimentAnalyzer()
    queries = Queries("What is better at reducing fever in children, Ibuprofen or Aspirin?", "What is better at reducing fever in children, Ibuprofen or Aspirin?")
    sentiment = sentiment_analyzer.analyze(queries, corpus.entries[0].contents)
    print(sentiment)
elif(TEST == 17):
    preprocessor = GeneralPreprocessor()
    print(preprocessor.process("What is better at reducing fever in children, Ibuprofen or Aspirin?"))
elif(TEST == 18):
    # Baseline preprocessing with saving
    corpus = Corpus(corpus_file_path="./test_data/passages.jsonl")
    baseline_preprocessor = BaselinePreprocessor(verbose=True, parallel=True)
    baseline_preprocessor.process_corpus(corpus)
    corpus.write_corpus_pickle("./data/corpus.pkl")