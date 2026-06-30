def summarize_debate(client, ticker, debate_history):
    """Read the full bull/bear debate and give a final investment verdict."""
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a neutral Research Manager judging a debate about {ticker}. "
                "Read the full bull/bear exchange and give a final verdict: "
                "BUY, HOLD, or SELL — with a brief rationale citing the strongest points from each side."
            ),
        },
        {
            "role": "user",
            "content": f"Full debate:\n\n{debate_history}\n\nYour verdict:",
        },
    ]
    response = client.chat.completions.create(model="deepseek-chat", messages=messages)
    return response.choices[0].message.content.strip()
