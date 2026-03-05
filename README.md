# AI Supply Chain Advisor

An AI-driven supply chain analytics system that forecasts product demand and provides intelligent inventory recommendations across warehouses.

The system uses machine learning forecasting, inventory optimization logic, and an interactive dashboard to help businesses make better supply chain decisions.

---

## Live Dashboard

Run locally using Streamlit:

```
streamlit run app/streamlit_app.py
```

---

## Features

• Demand forecasting using Machine Learning (XGBoost / LSTM)

• Synthetic supply chain dataset generation

• Inventory optimization using safety stock and reorder point calculations

• Stockout prediction based on demand patterns

• Interactive analytics dashboard built with Streamlit

• Optional AI assistant for supply chain insights using ChatGPT

---

## Project Architecture

```
Dataset
   ↓
Feature Engineering
   ↓
Demand Forecasting Model
   ↓
Inventory Optimization Engine
   ↓
Stockout Prediction
   ↓
Interactive Dashboard (Streamlit)
   ↓
Optional AI Assistant (ChatGPT)
```

---

## Project Structure

```
ai_supply_chain_advisor
│
├── app
│   └── streamlit_app.py
│
├── services
│   ├── preprocessing.py
│   ├── forecasting_service.py
│   ├── inventory_service.py
│   └── llm_service.py
│
├── data
│   └── synthetic_supply_chain.csv
│
├── models
│   └── best_model.pkl
│
├── notebooks
│   └── forecasting_training.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/AI-Supply-Chain-Advisor.git
cd AI-Supply-Chain-Advisor
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the dashboard:

```
streamlit run app/streamlit_app.py
```

---

## Using Your Own Dataset

You can upload your own supply chain dataset directly through the dashboard.

Required columns:

```
date
warehouse_id
product_id
sales
inventory_level
lead_time
promotion
holiday
```

The system will automatically:

• preprocess the data
• generate forecasting features
• run the demand prediction model
• generate inventory recommendations

---

## Optional: Enable ChatGPT Supply Chain Assistant

This project includes optional integration with OpenAI ChatGPT to allow natural language queries about supply chain insights.

Example questions:

```
When will WH1 run out of stock?
Which product should be restocked first?
What reorder point should warehouse WH2 maintain?
```

### Step 1 — Install OpenAI library

```
pip install openai
```

---

### Step 2 — Generate an API Key

Create an API key here:

https://platform.openai.com/api-keys

---

### Step 3 — Set Environment Variable

Mac / Linux:

```
export OPENAI_API_KEY="your_api_key"
```

Windows:

```
setx OPENAI_API_KEY "your_api_key"
```

---

### Step 4 — Add ChatGPT Service

Create file:

```
services/llm_service.py
```

Add the following code:

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_supply_chain_ai(question, metrics, stockout_days):

    context = f"""
    Supply Chain Metrics:

    Average Demand: {metrics['average_demand']}
    Safety Stock: {metrics['safety_stock']}
    Reorder Point: {metrics['reorder_point']}
    Estimated Stockout Days: {stockout_days}

    Answer the user's question like a supply chain analyst.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a supply chain planning assistant."},
            {"role": "user", "content": context + "\n\nQuestion: " + question}
        ]
    )

    return response.choices[0].message.content
```

---

### Step 5 — Add Chat Interface to Dashboard

Inside `streamlit_app.py`:

```python
from services.llm_service import ask_supply_chain_ai
```

Then add:

```python
st.subheader("AI Supply Chain Assistant")

question = st.text_input(
    "Ask a supply chain question",
    placeholder="Example: When will WH1 run out of stock?"
)

if question:

    answer = ask_supply_chain_ai(
        question,
        metrics,
        days_left
    )

    st.success(answer)
```

---

## Technologies Used

Python
Pandas
NumPy
XGBoost
TensorFlow / LSTM
Streamlit
OpenAI API (optional)

---

## Example Dashboard

The dashboard provides:

• dataset preview
• demand forecast visualization
• inventory recommendations
• stockout prediction

---

## Future Improvements

• Digital Twin Supply Chain Simulator

• Multi-warehouse optimization

• Supplier delay simulation

• Distributed backend using FastAPI + Redis

• Docker deployment

---

## License

MIT License
