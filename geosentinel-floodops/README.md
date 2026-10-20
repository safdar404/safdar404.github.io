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

Cloud >20% or valid coverage <70% flags a measurement for review and excludes it from comparisons. These are portal screening defaults, not universal agronomic thresholds. Values should be calculated from reviewed field boundaries and atmospherically corrected, cloud/shadow-masked imagery. Live Satellite Check now supports opt-in public scene search and browser-side COG analysis; continuous background ingestion is not connected.

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

## Live Sentinel-2 field connection

1. Register a crop field with coordinates, area and sowing dates. Optional consent on the registration form opens and runs the scene lookup after save.
2. The provider-specific consent transmits only the field bounding box to Element 84 Earth Search. Farm names, finances and passwords are not transmitted. Consent resets on manual field selection. No client secret is stored on GitHub Pages.
3. Import a reviewed WGS84 Polygon/MultiPolygon for field pixel analysis. A point/acreage alone permits nearby scene discovery only.
4. Choose dates and maximum tile-cloud percentage. Public search uses `sentinel-2-c1-l2a`, returns up to 12 newest scenes, and is separate from the actual field mask.
5. Analyse a scene inside the registered crop cycle. Whole field windows must lie inside the tile, be on a supported WGS84 UTM grid, and contain no more than 65,536 20 m analysis cells.
6. Browser COG reads use GeoTIFF.js 2.1.3 and Proj4.js 2.11.0. Red/NIR 10 m cells are block-averaged to the aligned 20 m SCL/SWIR grid. Reflectance uses per-asset scale/offset, including nodata handling. Accept SCL classes 4/5/6, exclude centres within 10 m of polygon edges, then calculate median NDVI and NDMI.
7. Saving requires at least 10 accepted cells, ≥70% of polygon area represented by accepted cells, ≤20% field cloud, and entered/polygon areas within a 25% screening tolerance. These are portal screening defaults, not agronomic action thresholds or legal boundary verification.
8. Quality-screened records enter the existing index ledger with acquisition date, source, boundary/stage and valid-cell metadata. The last detailed analysis JSON can be downloaded; the displayed raster remains in tab memory.
9. A matching non-synthetic crop/stage yield model can receive the measured NDVI through the explicit handoff. Model training and independent validation are still required; no universal pretrained yield model is supplied.

Scene search, field location suitability, crop identity and disease diagnosis are different checks. The app flags low canopy/low moisture and comparable-stage declines as scouting cues; it does not diagnose a particular pathogen/pest, establish pesticide causality/residue safety or verify land ownership. A scene before sowing or after recorded actual harvest cannot be used to assess the registered crop.

The public service diagnostic fetches a provider-listed public sample and one public raster pixel without sending any field location. Catalog availability has no service guarantee. CORS/network failures, missing assets, grid misalignment, inadequate resolution and low clear-pixel coverage produce explicit withheld/error results rather than fabricated values.

### Satellite QA

Synthetic raster assertions cover polygon masking, edge distances, reflectance scale/offset, NDVI/NDMI, cloud rejection, valid coverage and an allowlist for public C1 assets. A provider-listed public COG supports HTTP 206 range reads with CORS. This is not evidence that a farmer's private field has been successfully analysed; that still requires provider-specific sharing consent, a reviewed boundary and suitable imagery.
