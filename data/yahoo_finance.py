import requests
import yfinance as yf
from bs4 import BeautifulSoup


def get_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    if not news:
        print(f"No news found for {ticker}")
        return []
    return news


def get_article_text(url):
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs[:20])
        return text if len(text) > 200 else None  # discard near-empty fetches
    except Exception:
        return None

    
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if hist.empty:
        return None
    return hist["Close"].iloc[-1]