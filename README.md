## Running the program in a local environment

1. Download competition data and extract it into: `data/touche-task2-passages-version-002.jsonl`
2. Then execute:

```# Install required Python environment
pipenv install

# Load additional required packages
pipenv run python ./src/prepare_libraries.py

# Run the actual program
pipenv run python ./src/main.py
```

## Running program in competition mode

After you have constructed the index using menu program, you can run the program in competition mode by running `pipenv run python ./src/main.py -i $inputDataset -o $outputDir` where `$inputDataset` points to directory with _topics.xml_ and `$outputDir` points to directory, where you want _results.txt_ to be saved. For example you can run `pipenv run python ./src/main.py -i ./data -o ./data`
