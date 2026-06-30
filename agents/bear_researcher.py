def bear_argue(client, ticker, context, bull_argument):
    """Make the bear case, rebutting the bull's last argument."""
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a Bear Analyst making the case AGAINST investing in {ticker}. "
                "Use the provided context (news + sentiment) as evidence. "
                "Directly rebut the bull's argument with specific points. "
                "Be concise — 3-4 paragraphs."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Bull's argument:\n{bull_argument}\n\n"
                "Make your bear case."
            ),
        },
    ]
    response = client.chat.completions.create(model="deepseek-chat", messages=messages)
    return response.choices[0].message.content.strip()
