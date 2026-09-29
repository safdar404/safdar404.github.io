# Customer Purchase Intelligence

[Open interactive dashboard](https://safdar404.github.io/customer-purchase-intelligence/). The supplied `AnalystAssistantHiringProcess_Assessment_V01.csv` contains customer purchase fields, despite its filename. The published dashboard uses aggregated data and contains no customer names or IDs.

## Cleaning and reconciliation

The source has 100 rows. Remove one exact duplicate, trim Country (`Nepal ` → `Nepal`), and parse mixed slash/hyphen date strings with a day-first convention. The resulting 99 purchases span 5 January 2016 to 5 July 2019 and total 34,400 **source currency units**. The source does not specify a currency. Ambiguous slash dates are interpreted day-first and should be checked against the data provider before operational use. Year selection updates the KPI, product, country and age-band views; the full-period annual chart and year-country heatmap stay as context.

## Power BI Desktop implementation

Import the original CSV locally with Power Query. Trim header whitespace and Country; remove exact duplicate rows; parse `Year` as a Date using a day-first locale and validate the ambiguous slash dates. Rename it `Purchase Date`. Set Age and Amount to whole numbers. Create an Age Band column (`Under 25`, `25–34`, `35–44`, `45+`), and a Date table related one-to-many to Purchases on Purchase Date. Keep customer names/IDs out of public exports. Build a year slicer, annual trend, country and product comparisons, age-band mix and a year-by-country matrix.

```DAX
Date = CALENDAR(MIN(Purchases[Purchase Date]), MAX(Purchases[Purchase Date]))
Purchase Amount = SUM(Purchases[Amount])
Transactions = COUNTROWS(Purchases)
Average Basket = DIVIDE([Purchase Amount], [Transactions])
Customers = DISTINCTCOUNT(Purchases[CustomerCode])
```

Create the Date table before making Year = YEAR('Date'[Date]) as a calculated column; mark it as a date table and relate it to Purchases. Use source currency units as the format label until the currency is confirmed. A native `.pbix` is not included.
