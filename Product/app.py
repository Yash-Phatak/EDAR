from fastapi import FastAPI
from pydantic import BaseModel
from main import ProductRecommender
from retrieve import retrieve_recent_data,preprocess_scraped_data
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

# Load the Flipkart database
flipkart_db = pd.read_csv('data/flipkart_com-ecommerce_sample.csv')
recommender = ProductRecommender(flipkart_db)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def main():
    return {'message':'EDAR'}

@app.get("/recommend")
def send_recommendations():
    retrieve_recent_data()
    preprocess_scraped_data()
    recommendations = set(recommender.final_list())
    print(recommendations)
    return {"recommended_ids": recommendations}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)