# Muhammad Safdar — Professional Portfolio

Live portfolio: https://safdar404.github.io/

A responsive showcase of GIS, GeoAI, Python, applied AI, engineering tools and business intelligence. The GitHub profile repository is managed independently.

## Features

- 26 distinct project entries, with a compact six-project initial view.
- Category filters, keyword search, full project details and live/source links.
- Six professional map case studies with full-resolution viewing.
- Career timeline, credentials, professional resume and direct contact links.
- Persistent light/dark themes, mobile navigation, keyboard-accessible dialogs, reduced-motion support and print styling.
- Local project preview graphics that do not depend on profile-repository history.

## Editing

The homepage is static HTML with embedded project and case data, styled by `portfolio.css` and enhanced by `portfolio.js`. Update the visible cards and corresponding embedded JSON together. `projects.json` and `cases.json` are reference copies of that data.

All displayed figures and screenshots keep the source projects' demonstration, data-quality and validation limitations. Building footprints are reference geometry, not legal property boundaries. Healthcare and forecasting projects are educational demonstrations.

## Deployment

GitHub Pages serves the default branch. Existing application folders and their individual assets remain available at their original paths.


<!-- ML-DASHBOARDS-START -->
## Eight applied AI/ML dashboards

[Explore the full dashboard collection](https://safdar404.github.io/applied-ml-analysis/). Each preview links to the original PNG for full-size viewing.

### Sonar Signal Classification

Scaled SVC classification of rock and mine sonar signals; signal profiles, confusion matrix, ROC, precision–recall and decision-score analysis.

[![Sonar Signal Classification — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/sonar.png)](https://safdar404.github.io/assets/ml-dashboards/sonar.png)

**Accuracy 81.0% · ROC AUC 0.939 · Average precision 0.950**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#sonar) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/sonar/README.md)

### Breast Cancer Classification

StandardScaler → PCA → SVC evaluation with malignant recall, specificity, confusion matrix and precision–recall analysis.

[![Breast Cancer Classification — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/cancer.png)](https://safdar404.github.io/assets/ml-dashboards/cancer.png)

**Accuracy 96.5% · Malignant recall 92.9% · ROC AUC 0.990**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#cancer) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/cancer/README.md)

### Credit Card Fraud Detection

Rare-event classification at threshold 0.25: 82 detected frauds, 16 missed frauds and 11 false alarms.

[![Credit Card Fraud Detection — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/fraud.png)](https://safdar404.github.io/assets/ml-dashboards/fraud.png)

**Fraud recall 83.7% · Precision 88.2% · Average precision 0.861**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#fraud) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/fraud/README.md)

### House Price Prediction

California housing regression with residuals, geographic errors, price-range analysis and feature relationships.

[![House Price Prediction — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/house-price.png)](https://safdar404.github.io/assets/ml-dashboards/house-price.png)

**MAE $30,846 · RMSE $46,504 · R² 0.835**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#house-price) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/house-price/README.md)

### Medical Insurance Cost Prediction

Log-target random-forest regression with subgroup errors and feature importance.

[![Medical Insurance Cost Prediction — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/insurance-cost.png)](https://safdar404.github.io/assets/ml-dashboards/insurance-cost.png)

**MAE 1,959.91 · RMSE 4,284.29 · R² 0.900**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#insurance-cost) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/insurance-cost/README.md)

### Customer Segmentation

K-Means customer profiles, cluster sizes, elbow and silhouette analysis; cluster IDs are arbitrary.

[![Customer Segmentation — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/customer-segmentation.png)](https://safdar404.github.io/assets/ml-dashboards/customer-segmentation.png)

**200 customers · 5 clusters · Silhouette 0.555**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#customer-segmentation) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/customer-segmentation/README.md)

### Fake News Text Classification

TF-IDF and LinearSVC evaluation with term weights and errors by text length; numeric class labels are retained.

[![Fake News Text Classification — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/fake-news.png)](https://safdar404.github.io/assets/ml-dashboards/fake-news.png)

**Accuracy 95.4% · Macro F1 0.954 · ROC AUC 0.991**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#fake-news) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/fake-news/README.md)

### Airline Passenger Forecasting

Historical passenger forecasts with chronological validation, residuals and 1961 forecast uncertainty.

[![Airline Passenger Forecasting — original collective dashboard](https://raw.githubusercontent.com/safdar404/safdar404.github.io/main/assets/ml-dashboards/airline-forecast.png)](https://safdar404.github.io/assets/ml-dashboards/airline-forecast.png)

**Log-SARIMAX RMSE 18.83 · Seasonal-naive RMSE 50.71 · ARIMA RMSE 86.81**

[View collective analysis](https://safdar404.github.io/applied-ml-analysis/#airline-forecast) · [Project README](https://github.com/safdar404/safdar404.github.io/blob/main/applied-ml-analysis/airline-forecast/README.md)

Figures are transcribed from the supplied notebook-dashboard screenshots. Sonar and fraud results refer to these displayed runs and differ from earlier comparison experiments. These are educational evaluations; clinical and operational validation are not established. Text classification does not establish factual truth. Streamlit hosting is pending.
<!-- ML-DASHBOARDS-END -->
