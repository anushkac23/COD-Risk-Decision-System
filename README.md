# COD Risk Decision System

An AI-powered decision support system designed to help D2C businesses reduce Cash on Delivery (COD) Return to Origin (RTO) losses while protecting genuine customers.

## Project Overview

This project uses machine learning to predict the probability of COD orders resulting in RTO and recommends appropriate business actions.

The system provides four possible recommendations:

* Ship as-is
* WhatsApp confirmation
* Prepaid payment nudge
* Hold for manual review

It also includes a Streamlit dashboard, a mock WhatsApp automation flow and an illustrative financial impact calculator.

## Key Features

* COD RTO prediction using Random Forest.
* Configurable risk thresholds using JSON.
* Plain-English decision explanations.
* WhatsApp confirmation and prepaid message simulation.
* YES, NO, PREPAID and unclear-response handling.
* 24-hour no-response timeout simulation.
* Daily order action summaries.
* Interactive risk analysis dashboard.
* Downloadable order decision log.
* Financial impact scenario calculator.

## Technology Stack

| Category             | Technologies                |
| -------------------- | --------------------------- |
| Programming Language | Python                      |
| Data Processing      | Pandas, NumPy               |
| Machine Learning     | Scikit-learn, Random Forest |
| Dashboard            | Streamlit                   |
| Visualization        | Plotly                      |
| Model Storage        | Joblib                      |
| Configuration        | JSON                        |

## Project Structure

```text
COD-Risk-Decision-System/
│
├── app/
│   ├── services/
│   │   ├── decision_engine.py
│   │   ├── prediction_service.py
│   │   └── whatsapp_service.py
│   ├── analyze_data.py
│   ├── train_model.py
│   ├── backtest_model.py
│   └── dashboard.py
│
├── config/
│   └── risk_config.json
│
├── data/
│   └── orders_sample.csv
│
├── models/
│   ├── cod_risk_model.pkl
│   └── cod_risk_model_time_based.pkl
│
├── docs/
│   ├── AI_USAGE_LOG.md
│   ├── FOUNDER_MEMO.md
│   └── backtest_results.md
│
├── logs/
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd COD-Risk-Decision-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment (Windows)

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Train the model (optional)

```bash
python app/train_model.py
```

### 6. Run the dashboard

```bash
streamlit run app/dashboard.py
```

Open `http://localhost:8501` in your browser.

## Model Evaluation

The September 2026 time-based backtest produced:

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 69.60% |
| Precision | 44.07% |
| Recall    | 60.47% |
| F1 Score  | 50.98% |
| ROC AUC   | 0.7094 |

The model is intended for decision support. Its predictions should not be used for automatic order cancellation without further validation.

## Important Notes

* WhatsApp functionality is simulated; no live WhatsApp API is connected.
* Financial savings are illustrative estimates based on adjustable assumptions.
* Risk thresholds are configurable and require pilot validation.
* The sample dataset contains historical COD orders.

## Documentation

Additional project documentation is available in the `docs/` folder:

* `FOUNDER_MEMO.md` – Business findings and recommendations.
* `backtest_results.md` – Model evaluation and September backtest.
* `AI_USAGE_LOG.md` – AI assistance and validation record.
