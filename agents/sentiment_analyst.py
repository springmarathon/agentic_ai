def score_content(client, content):
    # Lopez-Lira & Tang, Can ChatGPT Forecast Stock Price Movements? (2023)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial analyst. Given a news headline or article, "
                    "classify its likely impact on the stock price using exactly one "
                    "of these labels:\n"
                    "- STRONGLY POSITIVE\n"
                    "- POSITIVE\n"
                    "- NEUTRAL  (clearly not material to the stock price)\n"
                    "- NEGATIVE\n"
                    "- STRONGLY NEGATIVE\n"
                    "- UNKNOWN  (direction cannot be determined from the information "
                    "given, or the headline is too ambiguous to call)\n"
                    "Use NEUTRAL only when the news is genuinely immaterial; use "
                    "UNKNOWN when you cannot tell the direction. "
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