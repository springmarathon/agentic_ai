from datetime import datetime

from data.yahoo_finance import get_current_price, get_news, get_article_text
from data.episode_store import save_episode
from agents.sentiment_analyst import score_content
from agents.bull_researcher import bull_argue
from agents.bear_researcher import bear_argue
from agents.research_manager import summarize_debate
from llm.factory import create_llm_client

SCORE = {
    "STRONGLY POSITIVE": 2,
    "POSITIVE": 1,
    "NEUTRAL": 0,
    "NEGATIVE": -1,
    "STRONGLY NEGATIVE": -2,
    "UNKNOWN": None,
}

DEBATE_ROUNDS = 2


def analyse(ticker):
    ticker = ticker.upper()
    client = create_llm_client()
    print(f"\n{'='*60}")
    print(f"Sentiment Analysis: {ticker}")
    print(f"{'='*60}\n")

    price = get_current_price(ticker)
    if price:
        print(f"Current Price: ${price:.2f}\n")

    news = get_news(ticker)
    if not news:
        return

    print(f"Analysing {len(news)} articles...\n")

    results = []
    for item in news:
        headline = item["content"]["title"]
        url = item["content"].get("canonicalUrl", {}).get("url", "")
        published = item["content"].get("pubDate", "")

        if published:
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                published = dt.strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                pass

        # try full article, fall back to headline
        article_text = get_article_text(url) if url else None
        content_to_score = article_text if article_text else headline
        source = "article" if article_text else "headline"

        sentiment = score_content(client, content_to_score)
        results.append({
            "headline": headline,
            "sentiment": sentiment,
            "published": published,
            "source": source
        })

        print(f"[{sentiment:<18}] {headline}")
        print(f"{'':22}Source: {source}")
        if published:
            print(f"{'':22}{published}\n")

    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    counts = {}
    for r in results:
        counts[r["sentiment"]] = counts.get(r["sentiment"], 0) + 1
    for sentiment, count in sorted(counts.items()):
        print(f"  {sentiment:<22} {count}")

    article_count = sum(1 for r in results if r["source"] == "article")
    headline_count = len(results) - article_count
    print(f"\n  Scored from full article: {article_count}")
    print(f"  Scored from headline only: {headline_count}")

    scores = [SCORE[r["sentiment"]] for r in results if SCORE.get(r["sentiment"]) is not None]
    if scores:
        final_score = sum(scores) / len(scores)
        print(f"\n  Final Score: {final_score:+.2f}  (avg over {len(scores)} articles, range -2 to +2)")

    # --- Bull / Bear Debate ---
    # Build context from the news headlines and their sentiment scores
    context_lines = [f"Ticker: {ticker}", f"Current price: ${price:.2f}" if price else ""]
    for r in results:
        context_lines.append(f"- [{r['sentiment']}] {r['headline']} ({r['published']})")
    context = "\n".join(context_lines)

    print(f"\n{'='*60}")
    print("Bull vs Bear Debate")
    print(f"{'='*60}\n")

    history = ""
    last_bull = ""
    last_bear = ""
    debate_rounds = []

    for round_num in range(1, DEBATE_ROUNDS + 1):
        print(f"--- Round {round_num} ---\n")

        last_bull = bull_argue(client, ticker, context, last_bear)
        history += f"\nBull: {last_bull}\n"
        print(f"Bull:\n{last_bull}\n")

        last_bear = bear_argue(client, ticker, context, last_bull)
        history += f"\nBear: {last_bear}\n"
        print(f"Bear:\n{last_bear}\n")

        debate_rounds.append({"round": round_num, "bull": last_bull, "bear": last_bear})

    print(f"{'='*60}")
    print("Research Manager Verdict")
    print(f"{'='*60}\n")
    verdict = summarize_debate(client, ticker, history)
    print(verdict)

    episode_id = save_episode(
        ticker=ticker,
        price=price,
        sentiment_results=results,
        sentiment_score=final_score if scores else None,
        debate_rounds=debate_rounds,
        verdict=verdict,
    )
    print(f"\n[Episode saved: {episode_id}]")


if __name__ == "__main__":
    analyse("MU")