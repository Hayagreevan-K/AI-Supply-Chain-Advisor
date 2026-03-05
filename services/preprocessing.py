import pandas as pd


def preprocess_data(df):

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["warehouse_id", "product_id", "date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    df["lag_1"] = df.groupby(["warehouse_id", "product_id"])["sales"].shift(1)

    df["lag_7"] = df.groupby(["warehouse_id", "product_id"])["sales"].shift(7)

    df["rolling_mean_7"] = df.groupby(
        ["warehouse_id", "product_id"]
    )["sales"].transform(lambda x: x.shift(1).rolling(7).mean())

    df["rolling_std_7"] = df.groupby(
        ["warehouse_id", "product_id"]
    )["sales"].transform(lambda x: x.shift(1).rolling(7).std())

    df = df.dropna()

    return df