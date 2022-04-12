#!/bin/bash
echo "This script installs locally required python versions automatically"
cd src
pipenv install -v
pipenv run python ./prepare_libraries.py

cd special_environments/t5_reranker
pipenv install -v
pipenv run python ./prepare_libraries.py