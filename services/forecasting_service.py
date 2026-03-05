import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "best_demand_forecast_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_demand(X):

    predictions = model.predict(X)

    return predictions