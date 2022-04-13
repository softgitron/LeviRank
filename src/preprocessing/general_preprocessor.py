import os
import math
import re
import nltk
import constants
import multiprocessing
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from corpus.corpus import Corpus
from preprocessing.preprocessor import Preprocessor
from preprocessing.spell_checker_preprocessor import SpellCheckerPreprocessor

WORDNET_TAG_CONVERSION_DICT = {
    "J": wordnet.ADJ,
    "N": wordnet.NOUN,
    "V": wordnet.VERB,
    "R": wordnet.ADV
}


class GeneralPreprocessor(Preprocessor):
    verbose: bool
    parallel: bool

    _language: str = "english"
    _stop_words: set[str]
    _spell_checker_server_url: str

    def __init__(self, verbose=False, parallel=False) -> None:
        self.verbose = verbose
        self.parallel = parallel
        # Load stop words
        self._stop_words = set(stopwords.words(self._language))

    def process_corpus(self, corpus: Corpus) -> Corpus:
        # Create new spell checking server
        spell_checker = SpellCheckerPreprocessor()
        self._spell_checker_server_url = spell_checker.get_server_url()
        if self.parallel:
            corpus = self._process_corpus_parallel(corpus)
        else:
            corpus = self._process_corpus(corpus)
        return corpus

    def _process_corpus_parallel(self, corpus: Corpus) -> Corpus:
        # Divide corpus into list of corpuses based on the core amount
        core_amount = os.cpu_count()
        entries_per_core = math.floor(len(corpus.entries) / core_amount)
        corpuses = []
        for starting_index in range(0, entries_per_core * core_amount, entries_per_core):
            new_corpus = Corpus(None)
            new_corpus.entries = corpus.entries[starting_index:
                                                starting_index + entries_per_core]
            corpuses.append(new_corpus)

        # Add leftover entries to last corpus
        corpuses[-1].entries += corpus.entries[entries_per_core * core_amount:]

        # Run preprocess parallel
        with Pool() as pool:
            corpuses = pool.map(self._process_corpus, corpuses)

        # Join seperated corpuses back into main corpus
        corpus.entries = []
        for parallel_corpus in corpuses:
            corpus.entries += parallel_corpus.entries

        # Update corpus id dictionary
        corpus.update_id_dictionary()

        # Return joined corpus
        return corpus

    def _process_corpus(self, corpus: Corpus) -> Corpus:
        # Initialize spell checker client
        spell_checker = SpellCheckerPreprocessor(
            self._spell_checker_server_url)
        # Preprocess all entries in the corpus
        for i, entry in enumerate(corpus):
            if i % constants.PRINT_STATUS_UPDATE_SPEED == 0 and self.verbose:
                print(
                    f"{i}/{corpus.length()} preprocessed @ {multiprocessing.current_process()}")
            # Score language
            spell_checker.score_corpus_entry(entry)
            # Preprocess
            entry.contents_preprocessed = self.process(entry.contents)

        # Remove empty entries from the corpus
        filter(lambda entry: entry.contents_preprocessed == "", corpus.entries)
        corpus.update_id_dictionary()

        return corpus

    # https://medium.com/almabetter/data-preprocessing-techniques-6b04d820fda2
    # Took ideas from this article, what could be preprocessed
    def process(self, document: str) -> str:
        # Lowercase all
        document = document.lower()

        # Remove punctuation and numbers
        document = re.sub(r"[^A-Za-z\s]+", "", document)

        # Remove extra white spaces
        document = re.sub(r"[\s]{2,}", "", document)

        # Tokenize string
        word_tokens = word_tokenize(document)

        # Remove stop words
        word_tokens = [
            token for token in word_tokens if token not in self._stop_words]

        # Lemmatize words

        # Get pos tags for the word tokens
        tags = nltk.pos_tag(word_tokens)

        # Convert tags to Wordnet tags
        wordnet_tags = [0] * len(tags)
        for i, tag in enumerate(tags):
            wordnet_tag = WORDNET_TAG_CONVERSION_DICT.get(tag[1][0])
            if wordnet_tag:
                wordnet_tags[i] = wordnet_tag
            else:
                wordnet_tags[i] = wordnet.NOUN

        # Do lemmatization using wordnet lemmatizer
        lemmatizer = WordNetLemmatizer()
        word_tokens = [lemmatizer.lemmatize(
            word, wordnet_tags[i]) for i, word in enumerate(word_tokens)]

        # Combining word tokens for results.
        results = " ".join(word_tokens)
        return results
