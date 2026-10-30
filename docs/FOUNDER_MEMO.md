# Founder Memo: Reducing COD Returns to Origin (RTO)

**Project:** COD Risk Decision System
**Prepared for:** D2C Haircare Brand
**Date:** October 2026

## 1. Executive Summary

The objective of this system is to reduce Cash on Delivery (COD) Return to Origin (RTO) losses while avoiding unnecessary cancellations of genuine customers.

The proposed solution uses a machine learning model to estimate RTO probability and a configurable decision engine to recommend one of four actions:

* Ship as-is
* WhatsApp confirmation
* Prepaid payment nudge
* Hold for manual review

The recommendation is to use AI predictions to prioritize customer interventions rather than automatically cancel orders. This balances operational risk with customer experience and business growth.

## 2. Key Findings from Historical Data

The analysis covered 2,018 historical COD orders.

**Finding 1: Overall RTO rate**

* 2,017 orders had a final status of Delivered or RTO.
* 573 orders resulted in RTO.
* Historical RTO rate: 28.41%.

**Finding 2: Previous customer RTO history is an important signal**

| Previous RTOs | Orders | RTO Rate |
| ------------- | -----: | -------: |
| 0             |  1,872 |   27.19% |
| 1             |    111 |   34.23% |
| 2             |     34 |   76.47% |

Customers with two previous RTOs showed a substantially higher historical RTO rate. This supports additional verification for repeat-risk customers.

**Finding 3: Incomplete addresses are a warning signal**

* 41 orders had an address recorded as ".".
* 30 of these resulted in RTO.
* RTO rate for this group: 73.17%.

Address completeness should therefore be checked before fulfilment.

**Finding 4: RTO rates differ across cities**

| City      | Orders | RTO Rate |
| --------- | -----: | -------: |
| Gorakhpur |     46 |   63.04% |
| Bareilly  |     33 |   60.61% |
| Darbhanga |     62 |   58.06% |
| Mumbai    |    219 |   17.81% |
| Pune      |    171 |   18.13% |

City-level patterns can help prioritize verification. However, small sample sizes and changing delivery conditions mean that city alone should not determine cancellation.

## 3. Model Backtest: September 2026

The model was trained on April–August 2026 data and evaluated on September 2026 data.

* Training orders: 1,658
* Test orders: 329
* Actual September RTO orders: 86
* Actual September RTO rate: 26.14%

| Metric    | Result |
| --------- | -----: |
| Accuracy  | 69.60% |
| Precision | 44.07% |
| Recall    | 60.47% |
| F1 Score  | 50.98% |
| ROC AUC   | 0.7094 |

The model identified 52 of the 86 actual RTO orders but incorrectly flagged 66 delivered orders as potential RTOs.

**Interpretation:** The model provides useful predictive signals, but its precision is not sufficient for automatic cancellation. Human review and customer confirmation should remain part of the process.

## 4. Recommended Business Rules

The current configurable thresholds are provisional and should be validated through a controlled pilot.

| Predicted RTO Risk | Recommended Action     |
| ------------------ | ---------------------- |
| Below 15%          | Ship as-is             |
| 15%–29.99%         | WhatsApp confirmation  |
| 30%–49.99%         | Offer prepaid discount |
| 50% or above       | Hold for manual review |

Additional safeguards:

* Do not automatically cancel first-time customers solely because of a high model score.
* Verify incomplete addresses and missing pincodes.
* Use customer confirmation before proceeding with uncertain orders.
* Review high-risk pincodes using sufficient historical delivery data.
* Treat no response within 24 hours as a manual-review case, not an automatic cancellation.

## 5. Financial Trade-offs

The assignment's business assumptions are:

| Cost Component               |      Amount |
| ---------------------------- | ----------: |
| Forward shipping             |         ₹65 |
| Return shipping              |         ₹65 |
| Packaging and handling       |         ₹25 |
| Expected product damage cost |      ₹14.40 |
| **Expected cost per RTO**    | **₹169.40** |

A 5% prepaid discount on an average order value of ₹649 equals ₹32.45.

The resulting prepaid amount is ₹616.55.

If one prepaid conversion genuinely prevents one RTO, the ₹169.40 expected RTO cost avoided exceeds the ₹32.45 discount. However, not every prepaid conversion prevents an RTO, so actual savings must be measured.

The scenario also estimates 62% gross margin on a delivered order, equivalent to approximately ₹402.38 at a ₹649 order value. This makes unnecessary cancellation of genuine customers commercially risky.

The dashboard therefore displays estimated savings and discount costs using adjustable assumptions. These are scenario estimates, not proven financial results.

## 6. Risks and Monitoring

Key risks include:

* False positives causing genuine orders to be delayed or lost.
* Changes in courier performance and city-level delivery patterns.
* Incorrect or incomplete customer information.
* Customers ignoring WhatsApp messages.
* Discount expenses exceeding the benefit from prevented RTOs.
* Model performance changing over time.

Recommended monitoring:

* Weekly precision, recall and RTO rate.
* Orders flagged versus actual RTO outcomes.
* WhatsApp confirmation and prepaid conversion rates.
* Genuine delivered orders flagged for intervention.
* Discount expense versus estimated RTO savings.
* Performance by city, courier and acquisition source.

## 7. Next Two Weeks

**Week 1**

* Pilot the system on a limited group of COD orders.
* Use WhatsApp confirmation and prepaid nudges.
* Keep high-risk orders under manual review.
* Record customer responses and fulfilment outcomes.

**Week 2**

* Compare pilot outcomes with historical RTO performance.
* Measure confirmation rates and prepaid conversions.
* Review false positives and customer complaints.
* Adjust thresholds based on observed results.
* Prepare a recommendation for wider rollout.

## Final Recommendation

Deploy the system initially as a decision-support tool, not an automatic cancellation system.

The strongest business opportunity is to identify risky orders early, verify customer intent and encourage prepaid conversion while protecting genuine customers from unnecessary rejection.

The model should be improved continuously using new order outcomes and real intervention results.
