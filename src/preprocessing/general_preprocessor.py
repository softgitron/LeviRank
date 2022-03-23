import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from constants import PRINT_STATUS_UPDATE_SPEED

from corpus import Corpus
from preprocessing.preprocessor import Preprocessor

WORDNET_TAG_CONVERSION_DICT = {
    "J": wordnet.ADJ,
    "N": wordnet.NOUN,
    "V": wordnet.VERB,
    "R": wordnet.ADV
}


class GeneralPreprocessor(Preprocessor):
    verbose: bool

    _language: str = "english"
    _stop_words: set[str]

    def __init__(self, verbose=False) -> None:
        super().__init__()
        self.verbose = verbose
        # Load stop words
        self._stop_words = set(stopwords.words(self._language))

    def process_corpus(self, corpus: Corpus) -> Corpus:
        # Preprocess all entries in the corpus
        for i, entry in enumerate(corpus):
            if i % PRINT_STATUS_UPDATE_SPEED == 0:
                print(f"{i}/{corpus.length()} preprocessed")
            entry.contents = self.process(entry.contents)

        # Remove empty entries from the corpus
        filter(lambda entry: entry.contents == "", corpus.entries)
        corpus.update_id_dictionary()

        return corpus

    # https://medium.com/almabetter/data-preprocessing-techniques-6b04d820fda2
    # Took ideas from this article, what could be preprocessed
    def process(self, document: str) -> str:
        document += " 2006"

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
