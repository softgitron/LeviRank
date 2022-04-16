class Queries:
    original_query: str
    preprocessed_query: str
    expanded_without_post_processing: str = None
    
    def __init__(self, original_query: str, preprocessed_query: str):
        self.original_query = original_query
        self.preprocessed_query = preprocessed_query