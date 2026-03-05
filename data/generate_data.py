import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ensure data folder exists
os.makedirs("data", exist_ok=True)

start_date = datetime(2023,1,1)
days = 365

warehouses = ["WH1","WH2","WH3","WH4"]
products = ["P1","P2","P3","P4","P5"]

data = []

# initial inventory
inventory = {
    (w,p): np.random.randint(400,600)
    for w in warehouses
    for p in products
}

for day in range(days):

    date = start_date + timedelta(days=day)

    for warehouse in warehouses:
        for product in products:

            base_demand = np.random.randint(20,50)

            # weekend demand spike
            if date.weekday() >= 5:
                base_demand *= 1.2

            # promotions
            promotion = np.random.choice([0,1], p=[0.9,0.1])
            if promotion:
                base_demand *= 1.5

            # holiday spike
            holiday = np.random.choice([0,1], p=[0.97,0.03])
            if holiday:
                base_demand *= 1.3

            demand = int(base_demand + np.random.normal(0,4))
            demand = max(demand,0)

            current_inventory = inventory[(warehouse,product)]

            sales = min(demand,current_inventory)

            inventory[(warehouse,product)] -= sales

            # supplier lead time
            lead_time = np.random.randint(3,7)

            # restock if inventory low
            if inventory[(warehouse,product)] < 100:

                restock = np.random.randint(300,500)

                inventory[(warehouse,product)] += restock

            data.append([
                date,
                warehouse,
                product,
                sales,
                inventory[(warehouse,product)],
                lead_time,
                promotion,
                holiday
            ])

df = pd.DataFrame(data,columns=[
    "date",
    "warehouse_id",
    "product_id",
    "sales",
    "inventory_level",
    "lead_time",
    "promotion",
    "holiday"
])

df.to_csv("data/supply_chain_sales.csv", index=False)

print("Dataset created successfully")
print("Rows:", len(df))
print("Saved to: data/supply_chain_sales.csv")