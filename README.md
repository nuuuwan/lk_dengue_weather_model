# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.
See [README.methodology.md](README.methodology.md) for full methodology.

_Last updated: 26 June 2026 · 17 regions with model results._

---

## Risk Map

The choropleth below shows a composite weather-risk score for each MOH
region, derived from the three lagged predictors in Erandi et al. (2021):
weekly rainfall (lag 10 w), mean max temperature (lag 16 w), and mean
min temperature (lag 13 w). Higher scores (red) indicate conditions
associated with higher dengue risk.

![Dengue Weather Risk Map](images/risk_map.png)

---

## Top 20 High-Risk Regions

Sorted by composite weather-risk score (descending).

| Region | District | Risk Score | Rainfall mm (−10w) | Max Temp °C (−16w) | Min Temp °C (−13w) |
|---|---|---:|---:|---:|---:|
| Attanagalla | LK-12 | 1.87 | 35.0 | 36.0 | 23.5 |
| Homagama | LK-11 | 1.77 | 55.2 | 33.5 | 23.1 |
| Kaduwela | LK-11 | 1.76 | 46.3 | 33.6 | 23.8 |
| Padukka | LK-11 | 0.57 | 44.0 | 33.8 | 22.9 |
| Kahathuduwa | LK-11 | 0.26 | 44.9 | 32.0 | 23.6 |
| Hanwella | LK-11 | 0.07 | 34.7 | 34.5 | 22.9 |
| Nugegoda | LK-11 | -0.25 | 23.5 | 31.8 | 25.0 |
| Kolonnawa | LK-11 | -0.25 | 23.5 | 31.8 | 25.0 |
| Battaramulla | LK-11 | -0.25 | 23.5 | 31.8 | 25.0 |
| CMC | LK-11 | -0.28 | 23.5 | 31.8 | 25.0 |
| Maharagama | LK-11 | -0.42 | 25.8 | 31.5 | 24.9 |
| Rathmalana | LK-11 | -0.42 | 25.8 | 31.5 | 24.9 |
| Pitakotte | LK-11 | -0.42 | 25.8 | 31.5 | 24.9 |
| Boralesgamuwa | LK-11 | -0.42 | 25.8 | 31.5 | 24.9 |
| Dehiwala | LK-11 | -0.68 | 25.8 | 31.4 | 24.8 |
| Moratuwa | LK-11 | -1.44 | 25.3 | 30.5 | 24.7 |
| Piliyandala | LK-11 | -1.44 | 25.3 | 30.5 | 24.7 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Data Sources

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)
- **Region boundaries:** Ministry of Health Sri Lanka (333 MOH regions)
- **Model:** Erandi et al. (2021), *Int. J. Dynamical Systems and Differential Equations*, Vol. 11, Nos. 5/6, pp. 462–472.
