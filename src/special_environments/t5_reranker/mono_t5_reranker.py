import pickle
import sys
from indexing.hit import Hit
from pygaggle.rerank.base import Query, Text
from pygaggle.rerank.transformer import MonoT5

# Load parameters from the stdin
parameters_tuple = pickle.load(sys.stdin.buffer)
query, hit_list = parameters_tuple

# Create reranker
reranker = MonoT5()

# Receive original preprocessed texts
query_texts = []
for hit in hit_list:
    corpus_entry_content = hit.corpus_entry.contents
    text = Text(corpus_entry_content, {
                "corpus_entry": hit.corpus_entry}, 0)
    query_texts.append(text)

# Form query object
query_object = Query(query)
reranks = reranker.rerank(query_object, query_texts)

# Form new hit list based on the reranked results
reranked_hit_list = []
for id, rerank in enumerate(reranks):
    hit = Hit(id, rerank.score)
    hit.corpus_entry = rerank.metadata["corpus_entry"]
    reranked_hit_list.append(hit)

# Dump generated output into stdout
pickle.dump(reranked_hit_list, sys.stdout.buffer)
