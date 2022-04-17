### Touche 2022: Comparative Argument Retrieval

Refer to [current working directory](https://drive.google.com/drive/folders/1RHJvnsI22y48zITfO5vhyqV_N56JAETA?usp=sharing) for touche merged datasets, BM25 indexes, missed document analysis and working jupyter notebooks of this branch. Refer to the [stance prediction working directory]() for touche stance prediction module jupyter notebooks and base datasets used.

* __[stance_classification_object_detector_touche_22.ipynb](stance_classification_object_detector_touche_22.ipynb) and [stance-classification-two-step-touche-22.ipynb](stance-classification-two-step-touche-22.ipynb)__: Predicts stance labels under 3-step and 2-step stance prediction model designs. But, these are trained only till 5 epochs but might be required to train upto 20 epochs, from practical experience w/ these models. Additionally, any of these can be working we can't guarantee results for any specific design.

* __[query_expansion_merging_and_retrieval_coverage_analysis.ipynb](query_expansion_merging_and_retrieval_coverage_analysis.ipynb)__: Query expansion based retrieval and average coverage for BM25 retrieval.

* __[initial_retrieval_prototyping_and_analysis.ipynb](initial_retrieval_prototyping_and_analysis.ipynb)__: Intitial BM25 based retrieval analysis and code, dense retrieval failure analysis, query expansion document usage.
