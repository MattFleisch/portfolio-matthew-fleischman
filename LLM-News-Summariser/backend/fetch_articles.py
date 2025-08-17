import requests
from datetime import datetime, timedelta

def fetch_articles(topic : str, api_key, max_results = 10) -> list[dict]:
    """
    Fetches articles related to a given topic using the NewsData.io API.
    Args:
        topic (str): The topic to search for in news articles.
        api_key (str): API key for NewsData.io.
        max_results (int): Maximum number of articles to fetch. Default is 10.
    Returns:
        list[dict]: A list of articles, each represented as a dictionary with keys:
            - "title": Title of the article
            - "url": URL of the article
            - "published": Publication date of the article
            - "text": Full description or excerpt of the article
    """
    # Sort out time frames of news articles
    today = datetime.today() # use UTC to match API format
    one_week_ago = today - timedelta(days=7)

    from_date = one_week_ago.date().isoformat()
    to_date = today.date().isoformat()

    url = (
        f"https://newsdata.io/api/1/news"
        f"?apikey={api_key}"
        f"&q={topic}"
        f"&language=en"
        #f"&from_date={from_date}"
        #f"&to_date={to_date}"
    )

    res = requests.get(url, verify=False)
    res.raise_for_status()
    data = res.json()

    articles = []
    for item in data.get("results", [])[:max_results]:
        articles.append({
            "title": item["title"],
            "url": item["link"],
            "published": item.get("pubDate", ""),
            "text": item.get("full_description", "") or item.get("description", ""),
        })

    return articles

