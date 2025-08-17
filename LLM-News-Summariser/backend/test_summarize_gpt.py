import sys
import os
sys.path.append(os.path.abspath(""))
from fetch_articles import fetch_articles
from summarize_gpt import summarize_articles

NEWS_KEY = "your API key"
OPENAI_KEY = "you GPT API key"

articles = fetch_articles("Pizza", NEWS_KEY, max_results=1)
summaries = summarize_articles(articles, OPENAI_KEY, model="gpt-4o")

for i, summary in enumerate(summaries):
    print(f"Article {i+1} Summary:")
    print(summary)
    print("-" * 80)  # Separator for readability