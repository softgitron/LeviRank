#!/bin/bash
echo "This script installs locally required python versions automatically"
cd src
pipenv install -v
cd special_environments/t5_reranker
pipenv install -v