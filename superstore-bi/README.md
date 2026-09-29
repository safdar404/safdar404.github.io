# Superstore Sales Intelligence

Interactive portfolio dashboard and Power BI build specification based on the supplied Superstore workbook. The live page is [safdar404.github.io/superstore-bi/](https://safdar404.github.io/superstore-bi/).

## Data

- The source workbook contains 5,899 order lines dated 2019-01-02 through 2020-12-30. It is not published in this repository.
- The Returns sheet has 296 distinct returned order IDs. No IDs match the Orders sheet. Do not calculate a return rate or relate this table to Orders until the correct matching extract is supplied.
- Source: uploaded `Superstore Dataset.xlsx`, Orders and Returns sheets. The unusual first header `Row ID+O6G3A1:R6` has been normalized to `Row ID`.
- The live dashboard uses `data.js`, grouped by month, region, category, subcategory and segment, with no order or customer identifiers. Its numbers are displayed rounded but aggregated from the original amounts.

## Power BI Desktop build

1. Import the supplied `Superstore Dataset.xlsx` using **Get data → Excel workbook** and select Orders. Rename the first column to `Row ID`. In Power Query set Order Date and Ship Date to Date, Sales and Profit to Decimal Number, Quantity and Row ID to Whole Number, and IDs to Text. Name the query `Orders`.
2. Create a Date table with the DAX below and mark it as a date table on `[Date]`. Link `Date[Date]` (one) to `Orders[Order Date]` (many), single filter direction.
3. Create the measures below. Use a 16:9 report canvas with overview, product and geography pages. Add Year, Region, Category and Segment slicers. Use sales and profit trend lines, category bars, subcategory matrix and state bars. Enable drill-through from category to subcategory and state to orders.
4. Set amounts to USD and margins to percentages. In the order-level detail visual, show Order ID, Order Date, State, Category, Sub-Category, Sales and Profit.
5. Keep the workbook Returns sheet as a separate quality-control query. It has zero matching IDs and must not be presented as a related Returns table.

```DAX
Date = CALENDAR(MIN(Orders[Order Date]), MAX(Orders[Order Date]))
Year = YEAR('Date'[Date])
Month Number = MONTH('Date'[Date])
Month = FORMAT('Date'[Date], "MMM")
Year Month = FORMAT('Date'[Date], "YYYY-MM")
Sales = SUM(Orders[Sales])
Profit = SUM(Orders[Profit])
Profit Margin = DIVIDE([Profit], [Sales])
Orders Count = DISTINCTCOUNT(Orders[Order ID])
Units = SUM(Orders[Quantity])
Average Order Value = DIVIDE([Sales], [Orders Count])
Loss Orders = COUNTROWS(FILTER(VALUES(Orders[Order ID]), CALCULATE([Profit]) < 0))
```

Create the Date table first, then calculated columns Year, Month Number, Month and Year Month on that table; create measures on Orders or a dedicated measures table. Sort Month by Month Number. `Loss Orders` is evaluated in the current filter context, so an order can be loss-making within a slice even if its full-order profit is positive.

## Reconciliation

| Metric | Full dataset |
| --- | ---: |
| Order lines | 5,899 |
| Distinct orders | 3,002 |
| Sales | $1,342,420.8532 |
| Profit | $175,234.4439 |
| Units | 22,313 |
| Profit margin | 13.0536% |

This repository contains a Power BI build specification and the published interactive web dashboard based on grouped data. Import the original workbook locally to create the full semantic model. A native `.pbix` was not generated in this environment; complete the steps in Power BI Desktop to produce and publish one.
