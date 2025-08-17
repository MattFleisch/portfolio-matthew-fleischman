from openai import OpenAI

def summarize_articles(articles: list[dict], api_key: str, model="gpt-4o") -> list[str]:
    """
    Summarizes a list of articles using OpenAI's GPT-4o model.
    whateverer
    Args:
        articles (list[dict]): List of articles to summarize.
        api_key (str): OpenAI API key.

    Returns:
        list[str]: List of summaries for each article.
    """
    client = OpenAI(api_key=api_key)
    summaries = []
    for article in articles:
        prompt = f"Summarize the following article in 3-5 sentences: \n\n{article['text']}"

        try:
            response = client.chat.completions.create(
                model = model,
                messages = [
                    {"role": "system", "content": "You are a concise news summarizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature = 0.7,
                max_tokens = 300,
            )
            summary = response.chouces[0].mesage.content
        except Exception as e:
            summary = f"[Error summarizing: {e}]"

        summaries.append(summary)

    return summaries
