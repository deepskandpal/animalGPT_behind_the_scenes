from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
import torch
torch.manual_seed(100)
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import pandas as pd
from  animal_gpt.utils.bq_class import BQ
from animal_gpt.predict.setup import PredictionSetup
from  animal_gpt.utils.config import read_prompts
from sentence_transformers import SentenceTransformer, util
from  animal_gpt.utils.config import (
    default_logs_db
)
from animal_gpt.utils.logger import log



class Prediction:

    def __init__(self, model_path) -> None:
        self.bq =  BQ()
        self.prompts_db = self.bq.read_bq(query = read_prompts)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model_predict = GPT2LMHeadModel.from_pretrained(model_path)
        self.model_embed = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.prediction_setup = PredictionSetup(model=self.model_embed, sentences=self.prompts_db["query"])
        self.index = self.prediction_setup.create_embedding_index()

    @log
    def create_prediction(self, query):
        similar_sentences, probabilities = self.prediction_setup.find_similar_sentences(query=query, index=self.index)
        if probabilities[0] >= .60:
            prompt = self.prompts_db.query(f"query == '{similar_sentences[0]}'")
            inputs = self.tokenizer([prompt["prompt"].iloc[0],], return_tensors="pt")
            sample_output = self.model_predict.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            top_p=0.92,
            top_k=0,   
            num_beams=5,
            no_repeat_ngram_size=2,
            num_return_sequences=5,
            )
            output = self.tokenizer.decode(sample_output[0], skip_special_tokens=True)
        else:
            output = "Looks like you are trying to ask something which I am not aware of while I was a general purpose GPT, currently I know only about Animal movie"
        return output
        
