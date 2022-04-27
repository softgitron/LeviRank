#!/bin/python3
import os
import nltk
import gensim.downloader as gensim_api
from language_tool_python import LanguageTool
from sentence_transformers import SentenceTransformer, util

"""This file is used mainly by the Docker to make sure all the files
Needed by the libraries are properly downloaded."""
nltk.download("punkt")
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# Hack for downloading spacy model
os.system("python -m spacy download en_core_web_sm")

gensim_api.load("glove-wiki-gigaword-300")
LanguageTool('en-US')
try:
    import pyterrier as pt
    if not pt.started():
        pt.init(version = 5.5, helper_version = "0.0.6")
except:
    print("PYTHON-TERRIER NOT SUPPORTED IN THIS BUILD")
SentenceTransformer(
    'sentence-transformers/msmarco-distilbert-base-tas-b')

try:
    from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder
    TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
except:
    print("PYSERINI NOT SUPPORTED IN THIS BUILD")