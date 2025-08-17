from fetch_articles import fetch_articles
from summarize_bart import summarize_articles

NEWSDATA_KEY = "your API key"

if __name__ == "__main__":
    arts = fetch_articles("artificial intelligence", NEWSDATA_KEY, max_results=3)
    sums = summarize_articles(arts)
    for i, s in enumerate(sums, 1):
        print("\nText:")
        print(arts[i].get("text"))
        print(f"\n--- Summary {i} ---\n{s}\n")