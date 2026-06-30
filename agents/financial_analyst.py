def score_content(client, content):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial analyst. Given a news headline or article, "
                    "classify its likely impact on the stock price with one of: "
                    "STRONGLY POSITIVE, POSITIVE, NEUTRAL, NEGATIVE, STRONGLY NEGATIVE. "
                    "Respond with only that label, nothing else."
                )
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message.content.strip()