import constants
import numpy as np
import torch
from transformers import RobertaTokenizer, TFRobertaModel
from sentiment_analysing.sentiment_analyzer import SentimentAnalyzer
from indexing.queries import Queries
from transformers import AutoConfig, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm


class GeneralSentimentAnalyzer(SentimentAnalyzer):
    device = None
    tokenizer_n = None
    config_n = None
    model_n = None
    tokenizer_s = None
    config_s = None
    model_s = None

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.tokenizer_n = AutoTokenizer.from_pretrained(constants.STANCE_MODEL_N_PATH)
        self.config_n = AutoConfig.from_pretrained(constants.STANCE_MODEL_N_PATH, num_labels=3)
        self.model_n = AutoModelForSequenceClassification.from_pretrained(constants.STANCE_MODEL_N_PATH, config=self.config_n).to(self.device)

        self.tokenizer_s = AutoTokenizer.from_pretrained(constants.STANCE_MODEL_S_PATH)
        self.config_s = AutoConfig.from_pretrained(constants.STANCE_MODEL_S_PATH, num_labels=3)
        self.model_s = AutoModelForSequenceClassification.from_pretrained(constants.STANCE_MODEL_S_PATH, config=self.config_s).to(self.device)

    def analyze(self, queries: Queries, passage: str) -> str:
        label_index = self.detect(passage, queries.original_query)
        return constants.LABELS[label_index]

    # this function has the logic for converting prediction numbers to labels.
    # please, take time and try to understand it.
    # also, feel free to call if required for understanding.
    def detect(self, evidence, claim):
        # first step
        # predicting neutral or not
        first = self.object_predictor(evidence, claim, self.tokenizer_n, self.model_n)
        final = 1
        if first == 1:
            final = 1
        elif first == 0:
            final = 0
        else:
            #predicting support or not
            second = self.object_predictor(evidence, claim, self.tokenizer_s, self.model_s)
            if second == 0:
                final = 2
            elif second == 1:
                final = 3
        return final

    def object_predictor(self, evidence, claim, tokenizer, model):
        model.eval()
        def encode(claim, rationale):
            encoding = tokenizer(claim, rationale, padding=True, truncation=True, max_length=512, return_tensors="pt")
            input_ids = encoding['input_ids']
            attention_mask = encoding['attention_mask']
            return input_ids, attention_mask

        def predict(model, evidence, claim):
            with torch.no_grad():
                input_ids, attention_mask = encode(claim, evidence)
                logits = model(input_ids.to(self.device)).logits
                output = logits.argmax(dim=1).tolist()[0]
            return output

        return predict(model, evidence, claim)
