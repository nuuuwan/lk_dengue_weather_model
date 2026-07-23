# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 23 July 2026 · 333 regions with model results._

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
| Manthai East | LK-44 | 3.47 | 127.4 | 35.4 | 24.5 |
| Mahara | LK-12 | 2.85 | 129.3 | 34.3 | 23.9 |
| Pitakotte | LK-11 | 2.75 | 130.7 | 32.9 | 25.0 |
| Maharagama | LK-11 | 2.75 | 130.7 | 32.9 | 25.0 |
| Rathmalana | LK-11 | 2.75 | 130.7 | 32.9 | 25.0 |
| Boralesgamuwa | LK-11 | 2.75 | 130.7 | 32.9 | 25.0 |
| Alawwa | LK-61 | 2.74 | 113.9 | 35.7 | 23.7 |
| Kuruwita | LK-91 | 2.69 | 125.7 | 34.3 | 23.9 |
| Dehiwala | LK-11 | 2.63 | 130.7 | 32.8 | 24.8 |
| Battaramulla | LK-11 | 2.59 | 127.7 | 32.7 | 25.1 |
| Nugegoda | LK-11 | 2.59 | 127.7 | 32.7 | 25.1 |
| Kolonnawa | LK-11 | 2.59 | 127.7 | 32.7 | 25.1 |
| CMC | LK-11 | 2.57 | 127.7 | 32.7 | 25.0 |
| Kiriella | LK-91 | 2.50 | 125.7 | 34.1 | 23.7 |
| Mathugama | LK-13 | 2.48 | 138.6 | 33.2 | 23.4 |
| Katupotha | LK-61 | 2.48 | 108.6 | 35.3 | 24.0 |
| Attanagalla | LK-12 | 2.47 | 118.5 | 34.5 | 23.8 |
| Nallur | LK-41 | 2.46 | 88.0 | 33.5 | 27.5 |
| Jaffna | LK-41 | 2.46 | 88.0 | 33.5 | 27.5 |
| Warakapola | LK-92 | 2.46 | 115.7 | 34.9 | 23.6 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.2174 |
| Spearman ρ | 0.2544 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Manthai East | Mullaitivu | 3.47 | 0.0 |
| Katupotha | Kurunegala | 2.48 | 0.0 |
| Nallur | Jaffna | 2.46 | 0.0 |
| Jaffna | Jaffna | 2.46 | 0.0 |
| Vavuniya North | Vavuniya | 2.40 | 0.0 |
| Kandawalai | Kilinochchi | 2.34 | 0.0 |
| Panadura | Kalutara | 2.33 | 0.0 |
| Uduvil | Jaffna | 2.25 | 0.0 |
| Beruwala | Kalutara | 2.20 | 0.0 |
| Narammala | Kurunegala | 2.18 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -2.91 | 160.0 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.71 | 69.6 |
| Pasbage Korale | Kandy | -2.60 | 56.4 |
| Udunuwara | Kandy | -1.80 | 53.7 |
| Harispattuwa | Kandy | -1.15 | 53.3 |
| Kalawana | Ratnapura | -2.61 | 53.2 |
| Yatinuwara | Kandy | -0.63 | 50.1 |
| Kahawaththa | Ratnapura | 0.37 | 49.0 |
| Akkaraipattu | Ampara | 0.02 | 45.7 |
| Badulla | Badulla | -5.14 | 42.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6251.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (3 August 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (17 August 2026)

![4-Week Forecast Risk Map](images/forecast_map_4w.png)

### Change from Current — 2-Week Delta

Blue regions show a projected **decrease** in risk; red regions show a projected **increase**.

![2-Week Delta Map](images/forecast_delta_2w.png)

### Change from Current — 4-Week Delta

![4-Week Delta Map](images/forecast_delta_4w.png)

---

## Data Sources

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)
- **Region boundaries:** Ministry of Health Sri Lanka (333 MOH regions)
- **Model:** Erandi et al. (2021), *Int. J. Dynamical Systems and Differential Equations*, Vol. 11, Nos. 5/6, pp. 462–472.
