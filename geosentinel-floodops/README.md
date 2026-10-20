# AgriSentinel Pakistan — فصل نگہبان

Pakistan-focused crop and farmer decision-support portal by Muhammad Safdar. Replaces the former GeoSentinel FloodOps page at the existing URL:

https://safdar404.github.io/geosentinel-floodops/

## Implemented workflows

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

Node syntax check and a DOM-mock smoke test covering initialization, all nine screen renders, example data, reports, comparison values, CSV formula escaping and JSON backup round-trip. Core assertions cover dates, index ranges, quality flags, quoted CSV, geometry closure/bounds, matching scouting visits, Pakistan-time label intervals, backup references and HTML escaping. Visual browser layout and real map tile delivery were not tested in the build environment.

## Production integrations still required

For continuous farm monitoring: authenticated shared storage, reviewed region/variety calendars, a server-side satellite ingestion and zonal statistics pipeline, scheduled jobs and alerts, and validated crop/pest image models with measured performance and human review. Do not describe the current application as an autonomous national monitoring service.
