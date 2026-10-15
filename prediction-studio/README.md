# Prediction Studio 2.0

[Open the live application](https://safdar404.github.io/prediction-studio/)

A browser-local analytics workbench by Muhammad Safdar. Upload a CSV, inspect validated results, compare assumptions and export the evidence. Synthetic examples are explicitly labelled. No uploaded records are sent to a server by this application.

## Workflows

| Workflow | Inputs | Outputs |
| --- | --- | --- |
| Classifier audit | actual, predicted, probability | Confusion counts, accuracy, recall, precision, F1, specificity, balanced accuracy, exact ROC AUC with tied scores, Brier score and threshold comparisons |
| Regression lab | x, y | One-feature ordinary least squares, ordered or seeded holdout, test MAE/RMSE/R²/bias, training-mean baseline, residuals and a selected-x prediction |
| Hospital capacity | date, occupied, capacity, admissions, discharges | Observed utilization and a configurable net-flow planning scenario with bed shortfall |
| Healthcare stock | sku, on_hand, daily_use, lead_days, safety_days | Demand scenarios, days of coverage, reorder points, whole-unit suggested orders and pre-delivery coverage risks |
| Device event trends | date, device, severity | Report counts by observed month, severity and device; no incidence inference |

Dates use YYYY-MM-DD. Severity is low, moderate or high. Classifier labels are 0/1 and probabilities are in [0,1]. Operational quantities are nonnegative; capacity is positive. Regression accepts finite signed values within the documented input range. Files are limited to 4 MB / 20,000 rows; regression requires at least eight rows. Capacity accepts a single daily facility series with unique dates; inventory requires unique SKUs. Aggregate duplicate keys before upload.

## Evaluation and assumptions

Regression fits the training partition only. Ordered splitting holds out the final rows; seed-42 shuffled splitting is repeatable and is inappropriate for time-dependent data when it would mix past and future. No hyperparameter tuning or automatic model selection is performed. Test-set baseline predictions use the training mean. R² is unavailable for constant test targets. Predictions outside the training x range are marked as extrapolation. Confidence or prediction intervals are not estimated.

Classifier audit can use supplied predictions or a probability threshold. ROC AUC uses probability ranking and grouped ties, independent of the active classification cutoff. Both outcome classes are required for AUC. Undefined ratio metrics show N/A. Threshold comparisons are exploratory: choosing a threshold and evaluating it on the same data does not provide an independent final test.

Capacity scenarios use the last seven available observations' mean net flow plus the user's daily adjustment; capacity is held at the latest value. Date gaps are flagged. The ≥85% indicator from the original implementation is not a universal clinical operating standard. Inventory demand is multiplied by the selected factor; order quantity covers lead time + safety days + review coverage and rounds up to whole units. Zero-demand rows have no suggested order. Device months without records are omitted rather than presumed to have zero events.

Exact duplicate rows are counted and retained for review. Schema validation rejects incomplete or invalid required values. Extra input columns are not included in analyzed rows. Tables show 50 rows per page and support text search; CSV exports include all analyzed rows. Spreadsheet formula-like text is escaped. JSON reports include provenance, quality checks, controls, metrics and limitations. Print/PDF includes the rendered results and current table page; use CSV for the complete record set.

## Run and verify

No build, Python service, API keys or external JavaScript dependencies are required. Serve index.html with any static web server.

Run the mathematical and workflow checks with:

```sh
node prediction-studio/test.cjs
```

Tests cover ROC ties, undefined metrics, OLS coefficients, deterministic non-overlapping partitions, CSV validation and escaping, all five sample workflows, perfect-line holdout evaluation, duplicate capacity dates and zero-demand stock.

This is an exploratory workbench, not a clinical diagnostic tool, causal model or regulatory forecasting system. Model performance depends on representative data and an appropriate independent evaluation design.
