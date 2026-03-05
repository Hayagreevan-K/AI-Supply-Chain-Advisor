import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("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"))


def ask_supply_chain_ai(question, metrics, stockout_days):

    context = f"""
    Supply Chain Metrics:

    Average Demand: {metrics['average_demand']}
    Safety Stock: {metrics['safety_stock']}
    Reorder Point: {metrics['reorder_point']}
    Estimated Stockout Days: {stockout_days}

    The user is asking a supply chain planning question.
    Answer clearly like a supply chain analyst.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a supply chain planning assistant."},
            {"role": "user", "content": context + "\n\nQuestion: " + question}
        ]
    )

    return response.choices[0].message.content