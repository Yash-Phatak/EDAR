from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime
import os


def get_article_content(page, url):
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
        print(f"Error fetching {url}: {str(e)}")
        return f"Error fetching content: {str(e)}"


def scrape_top_5_news():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )

        page = context.new_page()

        try:
            print("Navigating to Google News...")
            page.goto(
                'https://news.google.com/home?hl=en-GB&gl=GB&ceid=GB:en', timeout=30000)

            # Wait for any of these selectors to appear
            print("Waiting for content to load...")
            selectors = [
                'article a.JtKRv',  # Main article links
                'article h3 a',     # Article headlines
                'article h4 a',     # Smaller headlines
                '[jscontroller="d0DtYd"]',  # Article containers
                '[jsmodel="hT8rr"]'  # News content wrapper
            ]

            # Try each selector with a longer timeout
            for selector in selectors:
                try:
                    page.wait_for_selector(selector, timeout=20000)
                    print(f"Found content with selector: {selector}")
                    break
                except:
                    continue

            # Additional wait to ensure dynamic content loads
            time.sleep(5)

            print("\nExtracting top 5 articles...")
            articles_data = page.evaluate("""
                () => {
                    const articles = [];
                    // Try multiple possible selectors for articles
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
                        
                        // Get the full URL by checking if it's a relative path
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
                print("No articles found. The page structure might have changed.")
                browser.close()
                return []

            content_page = context.new_page()

            for idx, article in enumerate(articles_data):
                article['id'] = f"article_{idx+1}"
                if article['link']:
                    print(
                        f"\nFetching content for article {idx+1}/5: {article['title'][:100]}...")
                    article['content'] = get_article_content(
                        content_page, article['link'])
                    article['fetch_timestamp'] = datetime.now().isoformat()
                    print(
                        "✓ Content fetched successfully" if "Error" not in article['content'] else "✗ Error fetching content")
                    time.sleep(2)

            browser.close()
            return articles_data

        except Exception as e:
            print(f"Error during scraping: {e}")
            if 'page' in locals():
                # Take a screenshot for debugging
                try:
                    page.screenshot(path='error_screenshot.png')
                    print("Error screenshot saved as 'error_screenshot.png'")
                except:
                    pass
            browser.close()
            return []


def save_to_json(articles_data):
    if not os.path.exists('news_archives'):
        os.makedirs('news_archives')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'news_archives/top_5_news_{timestamp}.json'

    json_data = {
        'scrape_timestamp': datetime.now().isoformat(),
        'total_articles': len(articles_data),
        'articles': articles_data
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return filename


if __name__ == "__main__":
    try:
        print("Starting news scraping process for top 5 articles...")
        news_articles = scrape_top_5_news()

        if news_articles:
            json_file = save_to_json(news_articles)
            print(f"\nSaved {len(news_articles)} articles to: {json_file}")

            print("\nAll saved articles:")
            print("=" * 80)
            for article in news_articles:
                print(f"\nArticle ID: {article['id']}")
                print(f"Title: {article['title']}")
                print(f"Source: {article['source']}")
                print(f"Time: {article['time']}")
                print("\nContent Preview:")
                content_preview = article['content'][:300] + "..." if len(
                    article['content']) > 300 else article['content']
                print(content_preview)
                print("-" * 80)
        else:
            print("No articles were scraped successfully.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        print(traceback.format_exc())
