# Info about submission notebooks here

1)levirank_initial_retrieval_bm25- This notebook can be used to build the index for Initial BM25 retreival and for Intial Retrieval using Bm25. It takes the queries and documents as inputs and outputs the initial ranking for each query. 

2)levirank_mono_reranker.ipynb - This notebook can be used to the second stage reranking using Mono T5. It takes the intially ranked documents as inputs and outputs the a new ranking for each query. 
Note: The documents used for Mono T5 reranking are preprocessed on a different way than for Initial Bm25 ranking.

3)levirank_duo_reranker.ipynb - This notebook can be used for the final stage reranking. It takes the  second stage reranked documents as inputs and outputs the a new ranking for each query. 
Note: Only top K documents for each query are reranked and the other documents are just appended in the same order as ranked using Mono T5.

4)levirank_stance_prediction_and_qrels_file_generation.ipynb -  This notebook can be used for stance prediction and the final output generation. It takes the third stage reranked documents as inputs and outputs the final submission file.

5)levirank_psuedo_relevance_feedback.ipynb - This notebook can be used for new query generation using psuedo relevance feedback. It takes the reranked documents as inputs and outputs a new query based on these documents.

For replicating the submission levirank_psuedo_relevance_feedback_run_2022 - Run the notebooks in the order - 1--2--5--1--2--3--4. In this submission one iteration of psuedo relevance is done by running the notebooks 1--2--5 first and getting a new query.  The new query is the combination of the old query and the most frequent word from the top 20 Mono T5 reranked documents for each query. Once the new query is generated the whole process is run and the submission file is generated.

