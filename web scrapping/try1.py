# # from playwright.sync_api import sync_playwright
# # import time
# # import json
# # from datetime import datetime
# # import os
# # from typing import List, Dict, Optional


# # class NewsStorage:
# #     def __init__(self, storage_dir: str = "news_archives"):
# #         """Initialize NewsStorage with a storage directory."""
# #         self.storage_dir = storage_dir
# #         if not os.path.exists(storage_dir):
# #             os.makedirs(storage_dir)

# #     def save_articles(self, articles: List[Dict]) -> str:
# #         """Save news articles to a JSON file."""
# #         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# #         filename = f'top_news_{timestamp}.json'
# #         filepath = os.path.join(self.storage_dir, filename)

# #         json_data = {
# #             'metadata': {
# #                 'scrape_timestamp': datetime.now().isoformat(),
# #                 'total_articles': len(articles),
# #                 'version': '1.0'
# #             },
# #             'articles': []
# #         }

# #         for idx, article in enumerate(articles, 1):
# #             processed_article = {
# #                 'id': f'article_{idx}',
# #                 'title': article.get('title', ''),
# #                 'content': article.get('content', ''),
# #                 'source': article.get('source', ''),
# #                 'time': article.get('time', ''),
# #                 'link': article.get('link', ''),
# #                 'fetch_timestamp': article.get('fetch_timestamp', datetime.now().isoformat())
# #             }
# #             json_data['articles'].append(processed_article)

# #         with open(filepath, 'w', encoding='utf-8') as f:
# #             json.dump(json_data, f, ensure_ascii=False, indent=4)

# #         return filepath

# #     def get_latest_articles(self) -> Optional[Dict]:
# #         """Retrieve the most recently saved articles."""
# #         try:
# #             json_files = [f for f in os.listdir(self.storage_dir)
# #                           if f.endswith('.json')]

# #             if not json_files:
# #                 return None

# #             latest_file = max(json_files,
# #                               key=lambda x: os.path.getctime(
# #                                   os.path.join(self.storage_dir, x)))

# #             with open(os.path.join(self.storage_dir, latest_file),
# #                       'r', encoding='utf-8') as f:
# #                 return json.load(f)

# #         except Exception as e:
# #             print(f"Error reading latest articles: {e}")
# #             return None

# #     def search_articles(self, keyword: str) -> List[Dict]:
# #         """Search for articles containing a specific keyword."""
# #         results = []
# #         keyword = keyword.lower()

# #         try:
# #             for file in os.listdir(self.storage_dir):
# #                 if file.endswith('.json'):
# #                     with open(os.path.join(self.storage_dir, file),
# #                               'r', encoding='utf-8') as f:
# #                         data = json.load(f)

# #                         for article in data['articles']:
# #                             if (keyword in article['title'].lower() or
# #                                     keyword in article['content'].lower()):
# #                                 results.append(article)

# #         except Exception as e:
# #             print(f"Error searching articles: {e}")

# #         return results


# # def get_article_content(page, url):
# #     """Extract content from an article page."""
# #     try:
# #         page.goto(url, timeout=30000)
# #         time.sleep(3)

# #         content = page.evaluate("""
# #             () => {
# #                 const selectors = [
# #                     'article',
# #                     '.article-content',
# #                     '.article-body',
# #                     '.story-content',
# #                     'main',
# #                     '[itemprop="articleBody"]',
# #                     '.content-body'
# #                 ];

# #                 for (let selector of selectors) {
# #                     const element = document.querySelector(selector);
# #                     if (element) {
# #                         return element.textContent
# #                             .replace(/\\n+/g, '\\n')
# #                             .replace(/\\s+/g, ' ')
# #                             .trim();
# #                     }
# #                 }

# #                 const paragraphs = Array.from(document.querySelectorAll('p'));
# #                 return paragraphs
# #                     .map(p => p.textContent.trim())
# #                     .filter(text => text.length > 0)
# #                     .join('\\n\\n');
# #             }
# #         """)

# #         return content if content else "No content found"
# #     except Exception as e:
# #         print(f"Error fetching {url}: {str(e)}")
# #         return f"Error fetching content: {str(e)}"


# # def scrape_top_5_news():
# #     """Scrape top 5 news articles from Google News."""
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(headless=True)
# #         context = browser.new_context(
# #             viewport={'width': 1920, 'height': 1080},
# #             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
# #         )

# #         page = context.new_page()

# #         try:
# #             print("Navigating to Google News...")
# #             page.goto(
# #                 'https://news.google.com/home?hl=en-GB&gl=GB&ceid=GB:en', timeout=30000)

# #             print("Waiting for content to load...")
# #             selectors = [
# #                 'article a.JtKRv',
# #                 'article h3 a',
# #                 'article h4 a',
# #                 '[jscontroller="d0DtYd"]',
# #                 '[jsmodel="hT8rr"]'
# #             ]

# #             for selector in selectors:
# #                 try:
# #                     page.wait_for_selector(selector, timeout=20000)
# #                     print(f"Found content with selector: {selector}")
# #                     break
# #                 except:
# #                     continue

# #             time.sleep(5)

# #             print("\nExtracting top 5 articles...")
# #             articles_data = page.evaluate("""
# #                 () => {
# #                     const articles = [];
# #                     const selectors = [
# #                         'article a.JtKRv',
# #                         'article h3 a',
# #                         'article h4 a',
# #                         '[jscontroller="d0DtYd"] a'
# #                     ];

# #                     let articleElements = [];
# #                     for (const selector of selectors) {
# #                         const elements = document.querySelectorAll(selector);
# #                         if (elements.length > 0) {
# #                             articleElements = elements;
# #                             break;
# #                         }
# #                     }

# #                     for (let i = 0; i < Math.min(5, articleElements.length); i++) {
# #                         const article = articleElements[i];
# #                         const container = article.closest('article') || article.closest('[jscontroller="d0DtYd"]');

# #                         let link = article.href;
# #                         if (link.startsWith('./')) {
# #                             link = 'https://news.google.com' + link.substring(1);
# #                         }

# #                         articles.push({
# #                             title: article.textContent.trim(),
# #                             link: link,
# #                             time: container?.querySelector('time')?.textContent.trim() ||
# #                                   container?.querySelector('[datetime]')?.textContent.trim() || null,
# #                             source: container?.querySelector('a[data-n-tid]')?.textContent.trim() ||
# #                                    container?.querySelector('.UwMQC')?.textContent.trim() || null
# #                         });
# #                     }

# #                     return articles;
# #                 }
# #             """)

# #             if not articles_data:
# #                 print("No articles found. The page structure might have changed.")
# #                 browser.close()
# #                 return []

# #             content_page = context.new_page()

# #             for idx, article in enumerate(articles_data):
# #                 article['id'] = f"article_{idx+1}"
# #                 if article['link']:
# #                     print(
# #                         f"\nFetching content for article {idx+1}/5: {article['title'][:100]}...")
# #                     article['content'] = get_article_content(
# #                         content_page, article['link'])
# #                     article['fetch_timestamp'] = datetime.now().isoformat()
# #                     print(
# #                         "✓ Content fetched successfully" if "Error" not in article['content'] else "✗ Error fetching content")
# #                     time.sleep(2)

# #             browser.close()
# #             return articles_data

# #         except Exception as e:
# #             print(f"Error during scraping: {e}")
# #             if 'page' in locals():
# #                 try:
# #                     page.screenshot(path='error_screenshot.png')
# #                     print("Error screenshot saved as 'error_screenshot.png'")
# #                 except:
# #                     pass
# #             browser.close()
# #             return []


# # def display_articles(articles):
# #     """Display article information in a readable format."""
# #     print("\nAll articles:")
# #     print("=" * 80)
# #     for article in articles:
# #         print(f"\nArticle ID: {article['id']}")
# #         print(f"Title: {article['title']}")
# #         print(f"Source: {article['source']}")
# #         print(f"Time: {article['time']}")
# #         print("\nContent Preview:")
# #         content_preview = article['content'][:300] + "..." if len(
# #             article['content']) > 300 else article['content']
# #         print(content_preview)
# #         print("-" * 80)


# # if __name__ == "__main__":
# #     try:
# #         # Initialize storage
# #         storage = NewsStorage()

# #         print("Starting news scraping process for top 5 articles...")
# #         news_articles = scrape_top_5_news()

# #         if news_articles:
# #             # Save articles
# #             json_file = storage.save_articles(news_articles)
# #             print(f"\nSaved {len(news_articles)} articles to: {json_file}")

# #             # Display the scraped articles
# #             display_articles(news_articles)

# #             # Example of retrieving latest articles
# #             print("\nRetrieving latest articles from storage...")
# #             latest_news = storage.get_latest_articles()
# #             if latest_news:
# #                 print("Latest articles retrieved successfully!")

# #             # Example of searching articles
# #             print("\nSearching for articles containing 'technology'...")
# #             search_results = storage.search_articles("technology")
# #             print(f"Found {len(search_results)} articles about technology")

# #         else:
# #             print("No articles were scraped successfully.")

# #     except Exception as e:
# #         print(f"\nAn error occurred: {e}")
# #         import traceback
# #         print(traceback.format_exc())


# # main.py

# from playwright.sync_api import sync_playwright
# import time
# from datetime import datetime
# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv
# from typing import List, Dict


# class MongoDBService:
#     def __init__(self):
#         """Initialize MongoDB connection using environment variables."""
#         load_dotenv()  # Load environment variables from .env file

#         # Get MongoDB connection string from environment variable
#         mongodb_uri = os.getenv('MONGODB_URI')
#         if not mongodb_uri:
#             raise ValueError("MongoDB URI not found in environment variables")

#         # Initialize MongoDB client
#         self.client = MongoClient(mongodb_uri)

#         # Get database and collection
#         self.db = self.client['news_db']
#         self.articles_collection = self.db['articles']

#         # Create indexes for better query performance
#         self.setup_indexes()

#     def setup_indexes(self):
#         """Set up necessary indexes for the articles collection."""
#         self.articles_collection.create_index('id')
#         self.articles_collection.create_index('fetch_timestamp')
#         self.articles_collection.create_index(
#             [('title', 'text'), ('content', 'text')])

#     def save_articles(self, articles: List[Dict]) -> List[str]:
#         """Save multiple articles to MongoDB."""
#         if not articles:
#             return []

#         # Prepare articles for insertion
#         processed_articles = []
#         for idx, article in enumerate(articles, 1):
#             processed_article = {
#                 'id': f'article_{idx}',
#                 'title': article.get('title', ''),
#                 'content': article.get('content', ''),
#                 'source': article.get('source', ''),
#                 'time': article.get('time', ''),
#                 'link': article.get('link', ''),
#                 'fetch_timestamp': article.get('fetch_timestamp', datetime.now().isoformat()),
#                 'created_at': datetime.now()
#             }
#             processed_articles.append(processed_article)

#         # Insert articles
#         result = self.articles_collection.insert_many(processed_articles)
#         return result.inserted_ids

#     def close_connection(self):
#         """Close the MongoDB connection."""
#         self.client.close()


# def get_article_content(page, url):
#     """Extract content from an article page."""
#     try:
#         page.goto(url, timeout=30000)
#         time.sleep(3)

#         content = page.evaluate("""
#             () => {
#                 const selectors = [
#                     'article',
#                     '.article-content',
#                     '.article-body',
#                     '.story-content',
#                     'main',
#                     '[itemprop="articleBody"]',
#                     '.content-body'
#                 ];

#                 for (let selector of selectors) {
#                     const element = document.querySelector(selector);
#                     if (element) {
#                         return element.textContent
#                             .replace(/\\n+/g, '\\n')
#                             .replace(/\\s+/g, ' ')
#                             .trim();
#                     }
#                 }

#                 const paragraphs = Array.from(document.querySelectorAll('p'));
#                 return paragraphs
#                     .map(p => p.textContent.trim())
#                     .filter(text => text.length > 0)
#                     .join('\\n\\n');
#             }
#         """)

#         return content if content else "No content found"
#     except Exception as e:
#         print(f"Error fetching {url}: {str(e)}")
#         return f"Error fetching content: {str(e)}"


# def scrape_top_5_news():
#     """Scrape top 5 news articles from Google News."""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context(
#             viewport={'width': 1920, 'height': 1080},
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
#         )

#         page = context.new_page()

#         try:
#             print("Navigating to Google News...")
#             page.goto(
#                 'https://news.google.com/home?hl=en-GB&gl=GB&ceid=GB:en', timeout=30000)

#             print("Waiting for content to load...")
#             selectors = [
#                 'article a.JtKRv',
#                 'article h3 a',
#                 'article h4 a',
#                 '[jscontroller="d0DtYd"]',
#                 '[jsmodel="hT8rr"]'
#             ]

#             for selector in selectors:
#                 try:
#                     page.wait_for_selector(selector, timeout=20000)
#                     print(f"Found content with selector: {selector}")
#                     break
#                 except:
#                     continue

#             time.sleep(5)

#             print("\nExtracting top 5 articles...")
#             articles_data = page.evaluate("""
#                 () => {
#                     const articles = [];
#                     const selectors = [
#                         'article a.JtKRv',
#                         'article h3 a',
#                         'article h4 a',
#                         '[jscontroller="d0DtYd"] a'
#                     ];

#                     let articleElements = [];
#                     for (const selector of selectors) {
#                         const elements = document.querySelectorAll(selector);
#                         if (elements.length > 0) {
#                             articleElements = elements;
#                             break;
#                         }
#                     }

#                     for (let i = 0; i < Math.min(5, articleElements.length); i++) {
#                         const article = articleElements[i];
#                         const container = article.closest('article') || article.closest('[jscontroller="d0DtYd"]');

#                         let link = article.href;
#                         if (link.startsWith('./')) {
#                             link = 'https://news.google.com' + link.substring(1);
#                         }

#                         articles.push({
#                             title: article.textContent.trim(),
#                             link: link,
#                             time: container?.querySelector('time')?.textContent.trim() ||
#                                   container?.querySelector('[datetime]')?.textContent.trim() || null,
#                             source: container?.querySelector('a[data-n-tid]')?.textContent.trim() ||
#                                    container?.querySelector('.UwMQC')?.textContent.trim() || null
#                         });
#                     }

#                     return articles;
#                 }
#             """)

#             if not articles_data:
#                 print("No articles found. The page structure might have changed.")
#                 browser.close()
#                 return []

#             content_page = context.new_page()

#             for idx, article in enumerate(articles_data):
#                 article['id'] = f"article_{idx+1}"
#                 if article['link']:
#                     print(
#                         f"\nFetching content for article {idx+1}/5: {article['title'][:100]}...")
#                     article['content'] = get_article_content(
#                         content_page, article['link'])
#                     article['fetch_timestamp'] = datetime.now().isoformat()
#                     print(
#                         "✓ Content fetched successfully" if "Error" not in article['content'] else "✗ Error fetching content")
#                     time.sleep(2)

#             browser.close()
#             return articles_data

#         except Exception as e:
#             print(f"Error during scraping: {e}")
#             if 'page' in locals():
#                 try:
#                     page.screenshot(path='error_screenshot.png')
#                     print("Error screenshot saved as 'error_screenshot.png'")
#                 except:
#                     pass
#             browser.close()
#             return []


# def display_articles(articles):
#     """Display article information in a readable format."""
#     print("\nAll articles:")
#     print("=" * 80)
#     for article in articles:
#         print(f"\nArticle ID: {article['id']}")
#         print(f"Title: {article['title']}")
#         print(f"Source: {article['source']}")
#         print(f"Time: {article['time']}")
#         print("\nContent Preview:")
#         content_preview = article['content'][:300] + \
#             "..." if len(article['content']) > 300 else article['content']
#         print(content_preview)
#         print("-" * 80)


# def main():
#     try:
#         # Initialize MongoDB service
#         mongo_service = MongoDBService()
#         print("MongoDB connection established successfully!")

#         print("\nStarting news scraping process for top 5 articles...")
#         news_articles = scrape_top_5_news()

#         if news_articles:
#             # Save articles to MongoDB
#             inserted_ids = mongo_service.save_articles(news_articles)
#             print(
#                 f"\nSuccessfully saved {len(inserted_ids)} articles to MongoDB!")

#             # Display the scraped articles
#             display_articles(news_articles)

#         else:
#             print("No articles were scraped successfully.")

#         # Close MongoDB connection
#         mongo_service.close_connection()
#         print("\nMongoDB connection closed.")

#     except Exception as e:
#         print(f"\nAn error occurred: {e}")
#         import traceback
#         print(traceback.format_exc())


# if __name__ == "__main__":
#     main()


from playwright.sync_api import sync_playwright
import schedule
import time
from datetime import datetime
import logging
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
from typing import List, Dict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_fetcher.log'),
        logging.StreamHandler()
    ]
)


class NewsScraperService:
    def __init__(self):
        """Initialize the news scraper service with MongoDB connection."""
        load_dotenv()

        # MongoDB setup
        self.mongodb_uri = os.getenv('MONGODB_URI')
        if not self.mongodb_uri:
            raise ValueError("MongoDB URI not found in environment variables")

        self.client = None
        self.db = None
        self.articles_collection = None

        # Connect to MongoDB
        self._connect_to_mongodb()

    def _connect_to_mongodb(self):
        """Establish MongoDB connection and set up indexes."""
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client['news_db']
            self.articles_collection = self.db['articles']

            # Set up indexes
            self.articles_collection.create_index('id')
            self.articles_collection.create_index('fetch_timestamp')
            self.articles_collection.create_index(
                [('title', 'text'), ('content', 'text')])

            logging.info("Successfully connected to MongoDB")
        except errors.ConnectionError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise

    def clear_database(self):
        """Clear all existing articles from the database."""
        try:
            result = self.articles_collection.delete_many({})
            logging.info(
                f"Cleared {result.deleted_count} articles from database")
        except Exception as e:
            logging.error(f"Error clearing database: {e}")

    def get_article_content(self, page, url: str) -> str:
        """Extract content from an article page."""
        try:
            page.goto(url, timeout=30000)
            time.sleep(3)

            content = page.evaluate("""
                () => {
                    const selectors = [
                        'article',
                        '.article-content',
                        '.article-body',
                        '.story-content',
                        'main',
                        '[itemprop="articleBody"]',
                        '.content-body'
                    ];

                    for (let selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            return element.textContent
                                .replace(/\\n+/g, '\\n')
                                .replace(/\\s+/g, ' ')
                                .trim();
                        }
                    }

                    const paragraphs = Array.from(document.querySelectorAll('p'));
                    return paragraphs
                        .map(p => p.textContent.trim())
                        .filter(text => text.length > 0)
                        .join('\\n\\n');
                }
            """)

            return content if content else "No content found"
        except Exception as e:
            logging.error(f"Error fetching content from {url}: {e}")
            return f"Error fetching content: {str(e)}"

    def fetch_and_store_news(self):
        """Fetch news articles and store them in MongoDB."""
        try:
            logging.info("Starting news fetch cycle")

            # Clear existing articles before fetching new ones
            self.clear_database()

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                )

                page = context.new_page()

                # Navigate to Google News
                logging.info("Navigating to Google News...")
                page.goto(
                    'https://news.google.com/home?hl=en-GB&gl=GB&ceid=GB:en', timeout=30000)

                # Wait for content
                selectors = [
                    'article a.JtKRv',
                    'article h3 a',
                    'article h4 a',
                    '[jscontroller="d0DtYd"]'
                ]

                for selector in selectors:
                    try:
                        page.wait_for_selector(selector, timeout=20000)
                        logging.info(
                            f"Found content with selector: {selector}")
                        break
                    except Exception:
                        continue

                time.sleep(5)

                # Extract articles
                articles_data = page.evaluate("""
                    () => {
                        const articles = [];
                        const selectors = [
                            'article a.JtKRv',
                            'article h3 a',
                            'article h4 a',
                            '[jscontroller="d0DtYd"] a'
                        ];

                        let articleElements = [];
                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            if (elements.length > 0) {
                                articleElements = elements;
                                break;
                            }
                        }

                        for (let i = 0; i < Math.min(5, articleElements.length); i++) {
                            const article = articleElements[i];
                            const container = article.closest('article') || article.closest('[jscontroller="d0DtYd"]');

                            let link = article.href;
                            if (link.startsWith('./')) {
                                link = 'https://news.google.com' + link.substring(1);
                            }

                            articles.push({
                                title: article.textContent.trim(),
                                link: link,
                                time: container?.querySelector('time')?.textContent.trim() ||
                                      container?.querySelector('[datetime]')?.textContent.trim() || null,
                                source: container?.querySelector('a[data-n-tid]')?.textContent.trim() ||
                                       container?.querySelector('.UwMQC')?.textContent.trim() || null
                            });
                        }

                        return articles;
                    }
                """)

                if not articles_data:
                    logging.warning(
                        "No articles found. The page structure might have changed.")
                    browser.close()
                    return

                # Fetch content for each article
                content_page = context.new_page()
                for idx, article in enumerate(articles_data):
                    article['id'] = f"article_{idx+1}"
                    if article['link']:
                        logging.info(
                            f"Fetching content for article {idx+1}/5: {article['title'][:100]}")
                        article['content'] = self.get_article_content(
                            content_page, article['link'])
                        article['fetch_timestamp'] = datetime.now().isoformat()
                        article['created_at'] = datetime.now()

                browser.close()

                # Store articles in MongoDB
                if articles_data:
                    try:
                        result = self.articles_collection.insert_many(
                            articles_data)
                        logging.info(
                            f"Successfully saved {len(result.inserted_ids)} fresh articles to MongoDB")
                    except errors.PyMongoError as e:
                        logging.error(f"Error saving articles to MongoDB: {e}")

        except Exception as e:
            logging.error(f"Error during news fetch cycle: {e}")

    def run_scheduler(self):
        """Run the news fetcher scheduler."""
        logging.info(
            "Starting news fetcher scheduler - Running every 2 minutes with database refresh")

        # Schedule the job to run every 2 minutes
        schedule.every(2).minutes.do(self.fetch_and_store_news)

        # Run the first fetch immediately
        self.fetch_and_store_news()

        # Keep the scheduler running
        while True:
            try:
                schedule.run_pending()
                time.sleep(10)  # Check every 10 seconds for pending tasks
            except Exception as e:
                logging.error(f"Error in scheduler loop: {e}")
                # Wait 1 minute before retrying if there's an error
                time.sleep(60)

    def cleanup(self):
        """Clean up resources."""
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed")


def main():
    news_service = None
    try:
        news_service = NewsScraperService()
        news_service.run_scheduler()
    except Exception as e:
        logging.error(f"Fatal error in news fetcher: {e}")
    finally:
        if news_service:
            news_service.cleanup()


if __name__ == "__main__":
    main()
