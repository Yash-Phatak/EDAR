from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_load_dotenv


class MongoDBService:
    def __init__(self):
        """Initialize MongoDB connection using environment variables."""
        load_dotenv()  # Load environment variables from .env file

        # Get MongoDB connection string from environment variable
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            raise ValueError("MongoDB URI not found in environment variables")

        # Initialize MongoDB client
        self.client = MongoClient(mongodb_uri)

        # Get database and collection
        self.db = self.client['news_db']
        self.articles_collection = self.db['articles']

        # Create indexes for better query performance
        self.setup_indexes()

    def setup_indexes(self):
        """Set up necessary indexes for the articles collection."""
        # Create indexes for commonly queried fields
        self.articles_collection.create_index('id')
        self.articles_collection.create_index('fetch_timestamp')
        self.articles_collection.create_index(
            [('title', 'text'), ('content', 'text')])

    def save_articles(self, articles: List[Dict]) -> List[str]:
        """
        Save multiple articles to MongoDB.
        Returns list of inserted article IDs.
        """
        if not articles:
            return []

        # Prepare articles for insertion
        processed_articles = []
        for idx, article in enumerate(articles, 1):
            processed_article = {
                'id': f'article_{idx}',
                'title': article.get('title', ''),
                'content': article.get('content', ''),
                'source': article.get('source', ''),
                'time': article.get('time', ''),
                'link': article.get('link', ''),
                'fetch_timestamp': article.get('fetch_timestamp', datetime.now().isoformat()),
                'created_at': datetime.now()
            }
            processed_articles.append(processed_article)

        # Insert articles
        result = self.articles_collection.insert_many(processed_articles)
        return result.inserted_ids

    def get_latest_articles(self, limit: int = 5) -> List[Dict]:
        """Retrieve the most recent articles."""
        return list(self.articles_collection
                    .find({})
                    .sort('fetch_timestamp', -1)
                    .limit(limit))

    def search_articles(self, keyword: str) -> List[Dict]:
        """Search articles using text search."""
        return list(self.articles_collection.find(
            {'$text': {'$search': keyword}},
            {'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})]))

    def get_article_by_id(self, article_id: str) -> Optional[Dict]:
        """Retrieve a specific article by its ID."""
        return self.articles_collection.find_one({'id': article_id})

    def update_article(self, article_id: str, updates: Dict) -> bool:
        """Update an article's information."""
        result = self.articles_collection.update_one(
            {'id': article_id},
            {'$set': updates}
        )
        return result.modified_count > 0

    def delete_article(self, article_id: str) -> bool:
        """Delete an article by its ID."""
        result = self.articles_collection.delete_one({'id': article_id})
        return result.deleted_count > 0

    def delete_old_articles(self, days: int = 30) -> int:
        """Delete articles older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        result = self.articles_collection.delete_many(
            {'created_at': {'$lt': cutoff_date}}
        )
        return result.deleted_count

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()

# Updated main script to use MongoDB


def main():
    try:
        # Initialize MongoDB service
        mongo_service = MongoDBService()

        print("Starting news scraping process for top 5 articles...")
        news_articles = scrape_top_5_news()

        if news_articles:
            # Save articles to MongoDB
            inserted_ids = mongo_service.save_articles(news_articles)
            print(f"\nSaved {len(inserted_ids)} articles to MongoDB")

            # Display the scraped articles
            display_articles(news_articles)

            # Example of retrieving latest articles
            print("\nRetrieving latest articles from MongoDB...")
            latest_news = mongo_service.get_latest_articles()
            if latest_news:
                print(f"Retrieved {len(latest_news)} latest articles!")

            # Example of searching articles
            print("\nSearching for articles containing 'technology'...")
            search_results = mongo_service.search_articles("technology")
            print(f"Found {len(search_results)} articles about technology")

        else:
            print("No articles were scraped successfully.")

        # Close MongoDB connection
        mongo_service.close_connection()

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
