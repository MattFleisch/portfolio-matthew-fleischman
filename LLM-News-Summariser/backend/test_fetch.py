import sys
import os
sys.path.append(os.path.abspath(""))
from fetch_articles import fetch_articles

API_KEY = "your API key"

if __name__ == "__main__":
    topic = "pizza"
    articles = fetch_articles(topic, API_KEY, max_results=20)

    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Published: {article['published']}")
        print(f"URL: {article['url']}")
        try:
            print(f"Excerpt: {article['text'][:200]}...\n")
        except Exception as e:
            print(f"Article has no text\n")