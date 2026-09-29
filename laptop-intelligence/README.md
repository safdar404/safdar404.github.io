# Laptop Sales & Pricing Intelligence

[Open interactive dashboard](https://safdar404.github.io/laptop-intelligence/). This is an independent analysis of the supplied `amazon_laptop_prices_v01 (1).csv`. The archive also contains a Power BI report and documentation credited to Sridhar Kamali; those files have not been republished or represented as Muhammad Safdar's work.

## Scope and reconciliation

4,446 listings; reported Total Sales of $205,069,552.04 across 4,445 numeric values; 171,678 reported units. The data has no date column. One sales value is missing, 537 lines differ from Price × Sale Product Count by more than $1, 2,272 ratings are missing and 542 stock values are missing. The dashboard sums supplied Total Sales without inventing a time series or replacing inconsistencies with calculated sales. Public `data.js` groups listings by normalized brand, CPU family, graphics type and price band; no model or individual listing identifiers are published.

## Power BI Desktop implementation

Import the original CSV locally. In Power Query, trim and uppercase Brand, parse Price by removing `$` and commas, parse Total Sales as a decimal number, and set Sale Product Count and Available Stock to whole numbers. Keep nulls, document them, and create CPU Group, Graphics Group and Price Band columns with the categories shown in the interactive dashboard. Do not create a calendar or sales trend without transaction dates. Add brand, CPU, graphics and price-band slicers; present brand sales, product mix, price distribution, price-versus-sales scatter, rating coverage and stock coverage.

```DAX
Reported Sales = SUM(Laptops[Total Sales])
Units Sold = SUM(Laptops[Sale Product Count])
Listings = COUNTROWS(Laptops)
Average Listing Price = AVERAGE(Laptops[Price])
Average Rating = AVERAGE(Laptops[rating])
Rated Listings = COUNT(Laptops[rating])
Rating Coverage = DIVIDE([Rated Listings], [Listings])
Stocked Listings = COUNT(Laptops[Available Stock])
Stock Coverage = DIVIDE([Stocked Listings], [Listings])
Sales Formula Mismatch Rows = COUNTROWS(FILTER(Laptops, NOT ISBLANK(Laptops[Total Sales]) && ABS(Laptops[Price] * Laptops[Sale Product Count] - Laptops[Total Sales]) > 1))
```

Use `Reported Sales` as supplied, not `Price × Units`. Measure results depend on the applied filters. A native `.pbix` for this independent implementation is not included.
