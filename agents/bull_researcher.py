def bull_argue(client, ticker, context, bear_argument):
    """Make the bull case, rebutting the bear's last argument."""
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a Bull Analyst making the case FOR investing in {ticker}. "
                "Use the provided context (news + sentiment) as evidence. "
                "Directly rebut the bear's argument with specific points. "
                "Be concise — 3-4 paragraphs."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Bear's argument:\n{bear_argument or '(no argument yet — open with your bull thesis)'}\n\n"
                "Make your bull case."
            ),
        },
    ]
    response = client.chat.completions.create(model="deepseek-chat", messages=messages)
    return response.choices[0].message.content.strip()
