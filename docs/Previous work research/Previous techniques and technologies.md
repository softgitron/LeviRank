### Asterix

1. Preprocessing:
   - Duplicate document removal
   - Removal of too short documents
2. Indexing: BM25
3. Data: Webis-ArgQuality-20
4. Learning: Linear regression model
5. Query expansion WordNet
6. Ranking:
   - BM25 index
   - Regression model results

### Athos

1. Preprocessing
   - Lower-casing
   - Stop words removal
   - urls
   - emails
2. Indexing:
   - DirichletLM with u = 2,000
   - conclusion and premise indexed separately
3. Ranking:
   - 0.1 conclusion
   - 0.9 premise

### Blade

2. Indexing: DirichletLM

### Deadpool

2. Indexing: DirichletLM with u = 4,000
3. Ranking:
   - 0.1 conclusion
   - 0.9 premise

### Dread Pirate Roberts

2. Indexing:
   - Dirichlet-smoothed language-model with low-quality argument removal
   - LambdaMART
3. Ranking: Combination of Dirichlet and LambdaMART

### Elrond

1. Preprocessing:
   - Krovetz stemming
   - Custom stopword list
   - Speech tag filtering
   - WordNet synonyms
2. Indexing: DirichletLM

### Goemon Ishikawa

1. Preprocessing:
   - Tokenizer (Lucene)
   - Tokenizer (OpenNLP)
   - Stop word list (Lucene, Atire, Terrier and Smart)
   - Lemmatizers (OpenNLP)
   - Synonyms (WordNet)
2. Indexing:
   - BM25
   - DirichletLM

### Heimdall

1. Preprocessing: Universal sentence encoder
2. Indexing: DirichletLM
3. Data: Webis-ArgQuality-20
4. Learning:
   - KMS k = 300
   - Support vector regression model
5. Ranking:
   - Cluster centroids
   - Cosine similarity

### Hua Mulan

5. Query expansion:
   - Transformer-based query prediction
   - GPT-2
   - TF-IDF

### Jean-Pierre Polnareff

2. Indexing:
   - BM25
   - DirichletLM
3. Query expansion: WordNet
4. Ranking:
   - Combination of different indexer results

### Little Foot

1. Preprocessing:
   - Lemmatization
   - Removal of stop words
2. Indexing: Okapi BM25

### Luke Skywalker

2. Indexing: TF-IDF

### Macbeth

1. Preprocessing:
   - SBERT sentence embeddings
2. Learning: RoBERTa model

### Pippin Took

1. Preprocessing:
   - Krovetz Stemmer
   - Custom stop word list (combination of stop word list from various libraries)
2. Query expansion: WordNet

### Robin Hood

1. Preprocessing:
   - Universal Sentence Encoder
2. Query expansion: RM3 (Pyserini toolkit)
3. Ranking:
   - Cosine similarity
   - Document length bias

### Shanks

1. Preprocessing:
   - Custom stop word list based on the Smart and Lucene lists and frequent word from the document collection
2. Indexing:
   - BM25
   - DirichletLM
3. Ranking: Combination of multiple scores

### Skeletor

2. Indexing
   - BM25 retrieval
   - Ranking arguments based on their semantic
   - Pseudo relevance feedback with the sematic similarity of passages

### Yeagerists

2. Indexing: DirichletLM
3. Query expansion: Pretrained BERT model
