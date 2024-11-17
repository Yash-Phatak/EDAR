import spacy
import warnings
import pandas as pd
from transformers import pipeline,AutoTokenizer , AutoModelForSequenceClassification
import torch
import json
import re
import requests


warnings.filterwarnings('ignore')

nlp = spacy.load('data/ner_amazon_embeddings_1\model-best')
ner_pipeline = spacy.load("en_core_web_lg")
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def extract_entities(paragraph):
    
    # Process the input paragraph
    doc = nlp(paragraph)
    
    entities = {
        "brands": [],
        "products": [],
        "locations": [],
        "events": [],
        "dates": []
    }
    
    for ent in doc.ents:
        # Extract specific entity types
        if ent.label_ == "PRODUCT":
            entities["products"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["brands"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)
        elif ent.label_ == "EVENT":
            entities["events"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
    
    # Normalize and deduplicate entity values
    for key, values in entities.items():
        entities[key] = list(set([re.sub(r'\W+', ' ', item).strip() for item in values]))
    
    return entities



def sentiment_score(paragraph):
    inputs = tokenizer(paragraph, return_tensors="pt")
    outputs = model(**inputs)
    scores = outputs.logits

    # Apply softmax to convert logits to probabilities
    probs = torch.nn.functional.softmax(scores, dim=1)
    predicted_class = torch.argmax(probs, dim=1).item()  # Get the class with the highest probability

    # Convert the class to a human-readable sentiment score (e.g., 1-5 stars)
    sentiment_score = predicted_class + 1  # Add 1 because classes are 0-indexed
    confidence = probs[0][predicted_class].item()  # Confidence score for the predicted class

    return sentiment_score,confidence

