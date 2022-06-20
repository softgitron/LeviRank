# About this repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains all the necessary code for running the retrieval pipeline. However unfortunately the codebase is not fully homogenous and instead consists of multiple parts. Main runner is available in the src folder while more complex index builders and advanced methods are available in the `submission_notebooks` folder.

Main program is able to do following things:
- Read the corpus
- Preprocess the corpus
- Build BM25 indexes
- Search documents using
    - BM25 indexes
    - Pyserini based dense indexes
    - Wordnet based expanded indexes
- Do reranking using
    - MonoT5
    - DuoT5
    - Spelling errors
- Do sentiment analysis using two step process
- Batch process queries
- Evaluate search results nDCG and custom methods

Main program is not able to do following things:
- Build dense indexes
- Build sentiment analysis models
- Use more advanced methods

Results, prebuild Docker images and evaluations can be found from this [OneDrive folder](https://lut-my.sharepoint.com/:f:/g/personal/roni_juntunen_student_lut_fi/EqRd-8I_zpRNmRLuo_ZunpABeMxjpftEWbM1qfOrDZqCZA).

## Preparing to build the program
Before program can be build certain steps must executed:
1. Pipenv, pyenv and (Docker) should be installed.
2. If using premade indexes and models, those must be loaded from the [OneDrive](https://lut-my.sharepoint.com/:f:/g/personal/roni_juntunen_student_lut_fi/EqRd-8I_zpRNmRLuo_ZunpABeMxjpftEWbM1qfOrDZqCZA) from the data folder to the data folder in the root directory.
3. Selecting which version of the program to build. Due to library incompatibility only either pyterrier or pyserini indexers can be build in. Selection can be made by commenting / uncommenting respective libraries in the `Pipfile` and by running `pipenv install` to update the `Pipfile.lock` correspondingly.
4. If program is used in batch mode, batch mode must be chosen by altering `src/constants.py` and changing `METHOD_NAME` variable. As seen in the `main.py` following methods are available:
    - BM25
    - BM25_with_mono_t5
    - BM25_with_duo_t5_and_advanced_expander
    - levirank_baseline_large_duo_t5
    - levirank_dense_vote_initial_retrieval
    - levirank_dense_initial_retrieval

## Building Docker image
If index data is available building Docker image should be simple. You can build the image by running `docker build ./ -t touche-2022`. Alternatively you can build the image by running `build_docker.sh` script, which produces the Docker image and packs it into tar.gz file.

## Running the Docker image
Now the Docker image can be run in the batch mode by running `./run_docker.sh -i $inputDataset -o $outputDir`. Non batch mode can be run by using Dockers conventional running commands, but then you also have to take care of proper directory mounting. You may use contents of the `run_docker.sh` file as your reference.

## Running the program locally
Program can be also run locally. Before the program is able to start locally, some Python libraries must be installed. This can be done by running `./install_local.sh`. After that the program can be simply run by running `./run_local.sh`. If you want to program in the batch mode locally, this can be done using command `./run_local.sh -i $inputDataset -o $outputDir`

## About the architecture
Program is separated into several modules that are visible in the src folder. Bellow quick overview of different modules:
- Main module
    - `main.py` provides menu functionality and hosts setup for different batch modes
    - `constants.py` provides main configuration file for programs most important hardcoded values
    - `test.py` provides example how to manually run different parts of the program
- Batch processing module
    - Functionality for reading queries file
    - Functionality for batch processing multiple queries with different configurations
- Corpus module
    - Provide methods for reading and writing corpus files
- Indexing module
    - Provides different indexers
    - Is capable of indexing and queueing
- Preprocessing module
    - Hosts different preprocessors that can preprocess the corpus
    - Can also count spelling mistakes
- Query expansion module
    - Hosts query expanders that can expand queries and produce string results
- Reranking module
    - Hosts different rerankers that can rerank initial retrieval results
- Results module
    - Can read and write final results file
    - Can evaluate results based on the prior relevance judgements
- Sentiment analysing module
    - Can produce sentiment analysis for textual content and categorize it into different stances
- Special environments
    - Hosts special python scripts that can't be directly run under the main environment
    - Hosts real implementation of MonoT5 and DuoT5
    - Pyserini indexer is not moved to special environments due to lack of time
