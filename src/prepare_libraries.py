#!/bin/python3
import nltk
import pyterrier as pt
from language_tool_python import LanguageTool
from sentence_transformers import SentenceTransformer, util

"""This file is used mainly by the Docker to make sure all the files
Needed by the libraries are properly downloaded."""
nltk.download("punkt")
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
LanguageTool('en-US')
if not pt.started():
    pt.init()
SentenceTransformer(
    'sentence-transformers/msmarco-distilbert-base-tas-b')
