import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nersentiment import extract_entities, sentiment_score
import json

flipkart_db = pd.read_csv('data/flipkart_com-ecommerce_sample.csv')

# class ProductRecommender:
#     def __init__(self, flipkart_db):
#         self.flipkart_db = flipkart_db
#         self.vectorizer = TfidfVectorizer(stop_words='english')
        
#         # Create a combined text field for TF-IDF
#         self.flipkart_db['combined_text'] = self.flipkart_db.apply(
#             lambda row: ' '.join(filter(None, [
#                 str(row['product_name']),
#                 str(row['description']),
#                 str(row['brand'])
#             ])), axis=1
#         )
        
#         self.product_vectors = self.vectorizer.fit_transform(self.flipkart_db['combined_text'])

#     def get_product_recommendations(self, news_text):
#         entities = extract_entities(news_text)
#         products, brands, locations = entities.get('products', []), entities.get('brands', []), entities.get('locations', [])

#         # Combine all entities into a single query text
#         query_text = ' '.join(products + brands + locations)
#         query_vector = self.vectorizer.transform([query_text])

#         # Calculate cosine similarity
#         content_similarities = cosine_similarity(query_vector, self.product_vectors).flatten()
#         top_indices = content_similarities.argsort()[-5:][::-1]

#         # Adjust scores based on sentiment
#         sentiment_value, _ = sentiment_score(news_text)
#         normalized_sentiment = (sentiment_value - 1) / 4

#         recommendations = []
#         for idx in top_indices:
#             product = self.flipkart_db.iloc[idx]
#             final_score = (content_similarities[idx] * 0.7) + (normalized_sentiment * 0.3)
#             recommendations.append({
#                 'unique_id': product['uniq_id'],
#                 'product_name': product['product_name'],
#                 'brand': product['brand'],
#                 'similarity_score': content_similarities[idx],
#                 'sentiment_score': normalized_sentiment,
#                 'final_score': final_score
#             })

#         return sorted(recommendations, key=lambda x: x['final_score'], reverse=True)

#     def final_list(self):
#         with open("data/summarized_data.json","r") as file:
#             data = json.load(file)
#         final_recommendations = []
#         for item in data:
#             _id = item.get("_id")
#             text = item.get("text")
#             rec = self.get_product_recommendations(text)
#             for r in rec:
#                 final_recommendations.append(r['unique_id'])
#         return final_recommendations



class ProductRecommender:
    def __init__(self, flipkart_db):
        self.flipkart_db = flipkart_db
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Create a combined text field for TF-IDF
        self.flipkart_db['combined_text'] = self.flipkart_db.apply(
            lambda row: ' '.join(filter(None, [
                str(row['product_name']),
                str(row['description']),
                str(row['brand'])
            ])), axis=1
        )
        
        self.product_vectors = self.vectorizer.fit_transform(self.flipkart_db['combined_text'])

    def get_product_recommendations(self, news_text):
        entities = extract_entities(news_text)
        products, brands, locations = entities.get('products', []), entities.get('brands', []), entities.get('locations', [])

        # Combine all entities into a single query text
        query_text = ' '.join(products + brands + locations) or news_text  # Use news_text if entities are sparse
        query_vector = self.vectorizer.transform([query_text])

        # Calculate cosine similarity
        content_similarities = cosine_similarity(query_vector, self.product_vectors).flatten()
        
        # Filter for a minimum similarity threshold
        min_similarity_threshold = 0.1
        top_indices = [i for i in content_similarities.argsort()[-5:][::-1] if content_similarities[i] > min_similarity_threshold]

        # Adjust scores based on sentiment
        sentiment_value, _ = sentiment_score(news_text)
        normalized_sentiment = (sentiment_value - 1) / 4

        recommendations = []
        for idx in top_indices:
            product = self.flipkart_db.iloc[idx]
            final_score = (content_similarities[idx] * 0.7) + (normalized_sentiment * 0.3)
            recommendations.append({
                'unique_id': product['uniq_id'],
                'product_name': product['product_name'],
                'brand': product['brand'],
                'similarity_score': content_similarities[idx],
                'sentiment_score': normalized_sentiment,
                'final_score': final_score
            })

        return sorted(recommendations, key=lambda x: x['final_score'], reverse=True)

    def final_list(self):
        with open("data/summarized_data.json","r") as file:
            data = json.load(file)
        
        final_recommendations = set()  # Use set to avoid duplicate unique IDs
        for item in data:
            _id = item.get("_id")
            text = item.get("text")
            rec = self.get_product_recommendations(text)
            final_recommendations.update([r['unique_id'] for r in rec])  # Add unique IDs to the set

        return list(final_recommendations)
