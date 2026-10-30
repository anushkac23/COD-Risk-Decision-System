# September 2026 – Time-Based Model Backtest

## Dataset Split

* Training period: April–August 2026
* Training orders: 1,658
* Testing period: September 2026
* Testing orders: 329
* Delivered orders: 243
* RTO orders: 86
* Actual September RTO rate: 26.14%

## Model Performance

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 69.60% |
| Precision | 44.07% |
| Recall    | 60.47% |
| F1 Score  | 50.98% |
| ROC AUC   | 0.7094 |

## Confusion Matrix

| Actual / Predicted | Delivered | RTO |
| ------------------ | --------: | --: |
| Delivered          |       177 |  66 |
| RTO                |        34 |  52 |

## Key Observations

1. The model correctly identified 52 of 86 actual RTO orders.
2. It missed 34 actual RTO orders.
3. It incorrectly flagged 66 delivered orders as potential RTOs.
4. The model demonstrates useful predictive signal, but its precision is insufficient for automatic order cancellation.

## Business Recommendation

Use predictions to prioritize interventions rather than automatically reject COD orders.

Recommended actions include WhatsApp confirmation, prepaid conversion offers and manual review for high-risk orders.
