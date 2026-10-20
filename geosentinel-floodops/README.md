# AgriSentinel Pakistan — فصل نگہبان

Pakistan-focused crop and farmer decision-support portal by Muhammad Safdar. Replaces the former GeoSentinel FloodOps page at the existing URL:

https://safdar404.github.io/geosentinel-floodops/

## Implemented workflows

- Explicit empty-state dropdown messages and setup actions; province-linked searchable district options (including a custom-district fallback); combined province/district/crop and text filters with result counts, reset actions and matching map markers.
- Field registration, editing and deletion; province, district, variety, acres, irrigation, sowing, planned/actual harvest and yield records.
- Leaflet/OpenStreetMap field markers and imported WGS84 Polygon/MultiPolygon boundaries.
- Dated scouting visits with repeatable sampling methods, affected/checked plant counts, symptoms and pest counts.
- Rule-based symptom assessment and ground-check guidance (not an automated diagnosis).
- Imported NDVI/NDMI measurements, quality screening, charts, provenance and measurement ledger.
- Pesticide application logs with product, active ingredient, target, recorded rate, mode-of-action group, label reference, weather, pre-harvest and re-entry intervals.
- Descriptive before/after scouting and NDVI comparisons. Scouting method text must match; comparison visits are 1–14 days before/after application and exclude the application date.
- Illustrative Punjab lowland crop calendar; other region selections explicitly identify missing reviewed regional calendars.
- Crop-specific farmer guides, Urdu introductory guidance and official extension links.
- Printable reports, CSV exports, GeoJSON exports and validated JSON backup/restore.
- Explicitly labelled synthetic example workspace. Real workspaces start empty.

## Operation and deployment

`index.html` is a buildless static application. GitHub Pages publishes this folder as part of the portfolio. There is no package installation or server build step. Leaflet and map tiles need internet access. The page remains usable for records if Leaflet does not load.

Data uses this browser's localStorage key `agrisentinel-pk-v1`. There is no authentication, shared database, account sync, remote alert service or background processing. Export JSON backups regularly. Clearing browser storage removes local records. The former FloodOps data is not migrated.

## Import contracts

Vegetation CSV columns:

```csv
field,date,ndvi,ndmi,cloud,coverage,source
YOUR_EXISTING_FIELD_ID,2026-10-01,0.6,0.2,5,95,ACTUAL_SCENE_ID_AND_PROCESSING_METHOD
```

Dates use YYYY-MM-DD. NDVI/NDMI must lie in [-1,1]; NDMI can be blank. Cloud and valid coverage are percentages in [0,100]. Field IDs must already exist and source provenance is mandatory. Future acquisition dates are rejected. Invalid CSV rows reject the entire import; existing field/date/source duplicates are skipped.

Cloud >20% or valid coverage <70% flags a measurement for review and excludes it from comparisons. These are portal screening defaults, not universal agronomic thresholds. Values should be calculated from reviewed field boundaries and atmospherically corrected, cloud/shadow-masked imagery. No live satellite feed is connected.

Boundary imports accept one Polygon/MultiPolygon feature, with closed rings and coordinates within a broad Pakistan bounding extent (60–78 longitude, 23–38 latitude). Bounding-box checks do not establish national jurisdiction or polygon topology. Self-intersections, holes, overlap, alignment and cadastral validity require GIS review. Registered area remains farmer-entered; it is not calculated from imported geometry.

## Interpretation limits

Vegetation indices indicate canopy conditions, not a particular disease or pesticide residue. Before/after changes do not establish causal pesticide efficacy; untreated-control adjustment is not implemented. Sampling effort and crop stage must be comparable. Residue clearance requires appropriate laboratory testing.

Pre-harvest and re-entry timestamps are arithmetic based on the user-entered product-label intervals and Pakistan Standard Time (UTC+05:00). They do not certify residue safety or legal compliance. Follow the actual registered product label and local agricultural extension advice. No pesticide dose is recommended by this application.

Regional calendars beyond the illustrative Punjab lowland reference still need local agronomist review. Urdu content is introductory guidance, not full interface translation.

## Validation completed

Node syntax check and a DOM-mock smoke test covering initialization, all nine screen renders, example data, reports, comparison values, CSV formula escaping and JSON backup round-trip. Core assertions cover dates, index ranges, quality flags, quoted CSV, geometry closure/bounds, matching scouting visits, Pakistan-time label intervals, backup references and HTML escaping. Live Chromium QA on 21 October 2026 additionally verified province-linked district search (Punjab/Lahore and Sindh/Hyderabad), field registration, dropdown propagation, combined filters, no-result/reset behaviour, edit preservation, scouting validation, persistence after reload, measurement/application saves, guide selection, map controls, and JSON backup download/restore. Map controls loaded; third-party tile availability can vary.

Run the automated regression suite from the repository root:

```bash
node geosentinel-floodops/tests/qa.cjs
```

The suite parses the actual application JavaScript and exercises rendering through a minimal DOM mock. It does not replace live browser testing. Printable layout, all external links, all mobile devices, and every possible import were not exhaustively tested.

## Production integrations still required

For continuous farm monitoring: authenticated shared storage, reviewed region/variety calendars, a server-side satellite ingestion and zonal statistics pipeline, scheduled jobs and alerts, and validated crop/pest image models with measured performance and human review. Do not describe the current application as an autonomous national monitoring service.

## Regional intelligence, yield lab and crop issue atlas

- Published reference dashboard: Wheat and Rice, seasons 2022–23 through 2024–25, four provinces. Area, production and yield come from [Space4Climate's historical crop-estimation tables](https://space4climate.gov.pk/historical-data-on-crop-estimation/), retrieved 21 October 2026. The publisher attributes these to satellite estimation and states they were not field-validated. Values are a reference snapshot, not a live statistics service.
- Proportional-symbol maps at approximate province centres; bar charts, seasonal comparisons, production shares, area–yield scatter and downloadable evidence tables. No fabricated province boundaries.
- Separate province/district/crop aggregation of registered fields; actual production includes only fields with actual harvest date and actual yield. These holdings are not a representative provincial sample.
- Illustrated symptom cards, ground-check explanations, observed symptom distributions, field points and imported polygon boundaries coloured by observed incidence. Display bands are not pest-action thresholds.
- Descriptive empirical semivariograms using great-circle distance, one crop, and latest observation per field in a 7-day window. At least five distinct observed locations required; no kriging, significance test or prediction surface is claimed.
- Crop-cut estimator using total sample mass/area and an explicit measured-to-target moisture adjustment. Sample min/max are descriptive, not confidence bounds.
- Trainable ordinary-least-squares yield baseline from labelled NDVI/yield CSV. At least 15 rows and 3 districts, one crop and one stage protocol; validation leaves each district out. RMSE, MAE, R² and held-out mean-baseline RMSE are reported. Prediction outside the training NDVI range is blocked. No independent-season validation or calibrated prediction interval is provided.
- Synthetic training demonstration is explicitly labelled; its scores do not demonstrate real-world model skill. Uploaded training rows remain in tab memory and are not included in farm backups. Download the model/validation JSON to retain its parameters and model card.
- Power BI handoff provides field facts CSV, coordinates, DAX measures and setup instructions. There is no native .pbix, embedded live Power BI report or server connection.

Training CSV header:

```csv
crop,district,season,stage,ndvi,yield_kg_ha,source
```

Use independently measured harvest labels, stage-consistent cloud-screened NDVI, traceable source identifiers and meaningful spatial/seasonal coverage. Avoid duplicate or leaked records. A single-index linear model is an exploratory baseline and omits major agronomic drivers.

QA now also checks reference-unit conversions, source separation, crop-cut moisture correction, leave-one-district-out fitting, geographic distance and empirical semivariogram pair counts. Run the same Node regression command above.

## Farm operations extension

- Farm activities: field-linked tasks, due dates, priorities, open/completed status, overdue filtering and all-day iCalendar (.ics) export. Calendar text is escaped and folded; the visitor must import it in a calendar application. No cloud reminders are created.
- Irrigation planner: locally sourced ET₀, Kc, period, effective rainfall, usable root-zone water and application efficiency calculate simplified net/gross depth, volume and optional pump duration. Saved plans retain the original field-area snapshot and can be marked applied after their date. This is not metered irrigation or a complete paddy/salinity/event-scheduling model. [FAO crop coefficient guidance](https://www.fao.org/4/X0490E/x0490e0b.htm) informs the ETc relationship; input values still need local verification.
- Costs and returns: PKR expenses and sales with field filters, category charts, cash-ledger balances and CSV export. The balance is not full economic profit.
- Yield/price scenarios: user-entered assumptions produce revenue, cost balance, break-even price/yield and a ±20% sensitivity matrix. No live market prices or guaranteed yields.
- Action centre: record-based scouting/data freshness checks, harvest/label interval conflicts, outstanding follow-up, overdue activities and planned irrigation. Rules run on page rendering or explicit refresh, not as background notifications.
- Optional `operations` data extends the existing v1 backup. Older backups without it remain valid; new task/cost/water references and numeric/date fields are validated. Deleting a field also removes its linked operations. Full JSON backups include these records.

Regression checks cover water depths/area-volume conversion, zero-deficit and invalid-efficiency cases, scenario arithmetic, ledger totals, operation references in backups, overdue-task rules and iCalendar date/text handling.
