"""Extract text from URLs using newspaper3k."""

from newspaper import Article


def extract_article_text(url: str) -> dict:
    """Extract text and metadata from URL."""
    article = Article(url)
    article.download()
    article.parse()
    return {'title': article.title, 'text': article.text}