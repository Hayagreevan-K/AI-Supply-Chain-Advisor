def calculate_inventory_metrics(predicted_demand, lead_time=5, safety_factor=0.2):

    avg_demand = predicted_demand.mean()

    safety_stock = avg_demand * safety_factor

    reorder_point = avg_demand * lead_time + safety_stock

    return {
        "average_demand": avg_demand,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point
    }


def estimate_stockout_days(current_inventory, avg_demand):

    if avg_demand == 0:
        return float("inf")

    return current_inventory / avg_demand