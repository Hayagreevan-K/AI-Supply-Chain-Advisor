import pandas as pd


def generate_insight(question, df):

    question = question.lower()

    # stockout question
    if "stockout" in question:

        warehouse = None

        for w in df["warehouse_id"].unique():
            if w.lower() in question:
                warehouse = w

        if warehouse:

            warehouse_df = df[df["warehouse_id"] == warehouse]

            avg_demand = warehouse_df["predicted_demand"].mean()
            inventory = warehouse_df["inventory_level"].iloc[-1]

            days_left = inventory / avg_demand

            return f"{warehouse} will run out of stock in approximately {round(days_left,2)} days."

        return "Please specify a warehouse."



    # restocking insight
    if "restock" in question:

        grouped = df.groupby("product_id")["predicted_demand"].mean()

        highest = grouped.idxmax()

        return f"Product {highest} has the highest demand and should be prioritized for restocking."



    # reorder recommendation
    if "reorder" in question:

        avg_demand = df["predicted_demand"].mean()

        reorder_point = avg_demand * 5

        return f"A recommended reorder point is approximately {round(reorder_point,2)} units."



    return "I couldn't understand the question. Try asking about stockout, restocking, or reorder levels."