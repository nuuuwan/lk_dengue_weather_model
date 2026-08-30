# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 30 August 2026 · 333 regions with model results._

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
| Battaramulla | LK-11 | 3.23 | 92.9 | 31.6 | 25.9 |
| Kolonnawa | LK-11 | 3.23 | 92.9 | 31.6 | 25.9 |
| Nugegoda | LK-11 | 3.23 | 92.9 | 31.6 | 25.9 |
| CMC | LK-11 | 3.21 | 92.9 | 31.5 | 25.9 |
| Boralesgamuwa | LK-11 | 3.07 | 92.7 | 31.3 | 25.8 |
| Maharagama | LK-11 | 3.07 | 92.7 | 31.3 | 25.8 |
| Pitakotte | LK-11 | 3.07 | 92.7 | 31.3 | 25.8 |
| Rathmalana | LK-11 | 3.07 | 92.7 | 31.3 | 25.8 |
| Dehiwala | LK-11 | 2.98 | 92.7 | 31.2 | 25.7 |
| Ratnapura-Mc | LK-91 | 2.97 | 94.2 | 32.5 | 24.2 |
| Panadura | LK-13 | 2.93 | 92.2 | 31.2 | 25.7 |
| Kelaniya | LK-12 | 2.88 | 85.0 | 31.6 | 25.8 |
| Kaduwela | LK-11 | 2.61 | 88.9 | 31.9 | 24.4 |
| Kahathuduwa | LK-11 | 2.55 | 83.6 | 32.1 | 24.6 |
| Biyagama | LK-12 | 2.52 | 83.4 | 32.2 | 24.4 |
| Piliyandala | LK-11 | 2.50 | 81.3 | 31.1 | 25.8 |
| Moratuwa | LK-11 | 2.50 | 81.3 | 31.1 | 25.8 |
| Dehiovita | LK-92 | 2.39 | 86.8 | 32.5 | 23.5 |
| Ayagama | LK-91 | 2.34 | 88.9 | 32.1 | 23.6 |
| Ragama | LK-12 | 2.34 | 75.4 | 31.5 | 25.5 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.1311 |
| Spearman ρ | 0.18 |
| *p*-value (Pearson) | 0.017 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| CMC | Colombo | 3.21 | 2.2 |
| Rathmalana | Colombo | 3.07 | 0.0 |
| Ratnapura-Mc | Ratnapura | 2.97 | 0.0 |
| Kelaniya | Gampaha | 2.88 | 0.0 |
| Kahathuduwa | Colombo | 2.55 | 9.8 |
| Biyagama | Gampaha | 2.52 | 0.0 |
| Moratuwa | Colombo | 2.50 | 9.4 |
| Dehiovita | Kegalle | 2.39 | 0.0 |
| Eheliyagoda | Ratnapura | 2.34 | 0.0 |
| Ayagama | Ratnapura | 2.34 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Yatiyanthota | Kegalle | -1.43 | 40.2 |
| Pasbage Korale | Kandy | -2.80 | 27.5 |
| Bambaradeniya | Kandy | -2.33 | 25.1 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.62 | 20.3 |
| Katuwana | Hambantota | -0.49 | 19.2 |
| Kundasale | Kandy | -2.14 | 17.7 |
| Yatinuwara | Kandy | -1.24 | 16.7 |
| Harispattuwa | Kandy | -1.88 | 15.7 |
| Udunuwara | Kandy | -2.33 | 15.5 |
| Tangalle | Hambantota | -0.29 | 13.8 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6224.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (7 September 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (21 September 2026)

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
