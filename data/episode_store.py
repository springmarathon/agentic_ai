import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

EPISODES_FILE = Path(__file__).parent.parent / "episodes.json"


def save_episode(
    ticker: str,
    price: float | None,
    sentiment_results: list[dict],
    sentiment_score: float | None,
    debate_rounds: list[dict],
    verdict: str,
) -> str:
    episode = {
        "id": str(uuid.uuid4()),
        "ticker": ticker,
        "analysed_at": datetime.now(timezone.utc).isoformat(),
        "price_at_analysis": price,
        "sentiment_results": sentiment_results,
        "sentiment_score": sentiment_score,
        "debate_rounds": debate_rounds,
        "verdict": verdict,
        "outcome": None,
    }

    if EPISODES_FILE.exists():
        data = json.loads(EPISODES_FILE.read_text())
    else:
        data = {"episodes": []}

    data["episodes"].append(episode)
    EPISODES_FILE.write_text(json.dumps(data, indent=2))
    return episode["id"]
