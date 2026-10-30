# COD Risk Decision System – Decision Log

## 1. Machine Learning Model

* **Decision:** Used Random Forest Classifier.
* **Alternatives considered:** Logistic Regression and Decision Tree.
* **Reason:** Random Forest can capture non-linear relationships and work with a combination of numerical and categorical features.

## 2. Risk Thresholds

* **Decision:** Used four risk levels: Low, Medium, High and Very High.
* **Alternatives considered:** A simple binary classification of risky and safe orders.
* **Reason:** Four levels allow different interventions instead of treating every risky order equally.
* **Implementation:** Thresholds are configurable through `config/risk_config.json`.

## 3. Order Actions

* **Decision:** Implemented Ship As-Is, WhatsApp Confirmation, Prepaid Nudge and Hold for Review.
* **Alternatives considered:** Automatically cancelling all high-risk orders.
* **Reason:** Automatic cancellation could reject genuine customers and waste customer acquisition costs.

## 4. First-Time Customer Protection

* **Decision:** First-time customers flagged for hold are moved to WhatsApp confirmation.
* **Alternative considered:** Applying the same hold rule to every customer.
* **Reason:** Protects potential genuine customers and supports business growth.

## 5. WhatsApp Automation

* **Decision:** Built a simulated WhatsApp workflow with YES, NO, PREPAID, unclear-response and 24-hour timeout handling.
* **Alternative considered:** Connecting a live WhatsApp Business API.
* **Reason:** A simulation demonstrates the workflow without requiring external API credentials or additional setup.

## 6. Prepaid Discount

* **Decision:** Used a configurable 5% prepaid discount.
* **Alternative considered:** A larger discount or no discount.
* **Reason:** A modest incentive encourages prepaid conversion while limiting the discount cost.

## 7. Model Evaluation

* **Decision:** Used a time-based backtest, training on April–August data and testing on September data.
* **Alternative considered:** Relying only on a random train-test split.
* **Reason:** Time-based evaluation better represents how the system would perform on future orders.

## 8. Dashboard

* **Decision:** Used Streamlit and Plotly.
* **Alternatives considered:** Building a separate frontend using React or Angular.
* **Reason:** Streamlit enabled faster development of an interactive dashboard for business users.

## 9. High-Risk Order Handling

* **Decision:** High-risk orders receive a prepaid nudge, while very-high-risk orders are held for manual review.
* **Alternative considered:** Automatic cancellation.
* **Reason:** The model's prediction performance does not justify automatic cancellation without further validation.

## 10. Financial Impact

* **Decision:** Built an adjustable financial impact calculator.
* **Alternative considered:** Presenting estimated savings as guaranteed results.
* **Reason:** Intervention success and prepaid conversion rates are assumptions that need validation through a real pilot.

## Final Approach

The system prioritizes reducing avoidable RTO losses while protecting genuine customers. Machine learning predictions support business decisions, but manual review and customer confirmation remain important.
