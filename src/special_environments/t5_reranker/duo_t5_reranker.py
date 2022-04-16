import pickle
import sys
from indexing.hit import Hit
from pygaggle.rerank.base import Query, Text
from pygaggle.rerank.transformer import DuoT5

# Load parameters from the stdin
parameters_tuple = pickle.load(sys.stdin.buffer)
queries, hit_list = parameters_tuple

# Create reranker
reranker = DuoT5()

# Receive original preprocessed texts
# Take only first 100 entries
query_texts = []
for hit in hit_list[:100]:
    corpus_entry_content = hit.corpus_entry.contents
    text = Text(corpus_entry_content, {"docid": hit.id,
                "corpus_entry": hit.corpus_entry}, hit.score)
    query_texts.append(text)

# Form query object
query_object = Query(queries.original_query)
reranks = reranker.rerank(query_object, query_texts)

# Form new hit list based on the reranked results
reranked_hit_list = []
for rerank in reranks:
    hit = Hit(rerank.metadata["docid"], rerank.score)
    hit.corpus_entry = rerank.metadata["corpus_entry"]
    reranked_hit_list.append(hit)

# Merge rest of the original list to the new list
reranked_hit_list += hit_list[100:]

# Dump generated output into stdout
pickle.dump(reranked_hit_list, sys.stdout.buffer)
