## Running the program in a local environment

1. Download competition data and extract it into: `data/corpus/touche-task2-passages-version-002.jsonl`
2. Then execute:

```# Install required Python environment
pipenv install

# Load additional required packages
pipenv run python ./src/prepare_libraries.py

# Run the actual program
pipenv run python ./src/main.py
```
