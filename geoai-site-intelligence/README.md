# GeoAI Site Intelligence Suite

**Three interactive spatial decision-support prototypes** by Muhammad Safdar.

[Open the suite](https://safdar404.github.io/geoai-site-intelligence/) · [Portfolio](https://safdar404.github.io/) · [GitHub profile case study](https://github.com/safdar404#-featured-project--geoai-site-intelligence-suite)

## Applications

| Workspace | Decision question | Five adjustable factors |
|---|---|---|
| [MERIDIAN PRO](https://safdar404.github.io/geoai-site-intelligence/meridian-pro.html) | Which candidate areas are most suitable? | Terrain, flood avoidance, road access, utility access, demand |
| [GEOSENTINEL PRO](https://safdar404.github.io/geoai-site-intelligence/geosentinel-pro.html) | Where might flood mitigation be prioritized? | Storage capacity, floodplain interception, outfall access, drainage proximity, impervious load |
| [SOLARIS PRO](https://safdar404.github.io/geoai-site-intelligence/solaris-pro.html) | Which areas merit solar feasibility review? | Terrain buildability, transmission proximity, road access, interconnection, grid demand |

Each workspace provides a Leaflet map, study grid, adjustable weights, a relative suitability surface, candidate ranking, factor contributions, coordinates and CSV export. The applications are standalone static HTML/CSS/JavaScript pages served by GitHub Pages.

## Reproduce the demonstration

1. Open an application and set the study area.
2. Generate the study grid and run the siting analysis.
3. Change the factor sliders to explore how rankings change.
4. Inspect the map and ranked candidate cards; export a CSV for review.

The weighted composite is conceptually `score(cell) = Σ(normalized_weight_i × normalized_factor_i(cell))`. It is a relative ranking within the chosen scenario. A percentage displayed in the interface is a normalized suitability score, **not** a measured probability of project success.

## Evidence and limitations

The published pages implement the scoring and map interaction in client-side JavaScript. References to Python, remote sensing and AI/ML describe the broader analytical context; these pages do not provide a trained model, a documented satellite-data processing pipeline or a Power BI `.pbix` report. Treat their generated study surfaces and candidate positions as demonstration outputs, not verified parcels or engineering recommendations.

Before operational decisions, replace demonstration inputs with licensed authoritative local layers. Document CRS, resolution, data dates, source lineage, exclusions and normalization. Test sensitivity to weights and input uncertainty; check site access, land rights, grid or drainage capacity, environmental rules and engineering feasibility with qualified reviewers.

## Project structure

- `index.html` — suite overview and navigation
- `meridian-pro.html` — general suitability workspace
- `geosentinel-pro.html` — flood-mitigation workspace
- `solaris-pro.html` — solar-screening workspace

The [profile visual](https://github.com/safdar404/safdar404/blob/main/geoai-site-intelligence.svg) depicts the workflow and the three applications. It is a schematic, not a measured results chart.

© 2026 Muhammad Safdar
