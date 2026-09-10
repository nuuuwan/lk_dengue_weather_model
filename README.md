# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 10 September 2026 · 333 regions with model results._

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
| Dehiovita | LK-92 | 2.48 | 145.3 | 29.7 | 23.4 |
| Rathmalana | LK-11 | 2.03 | 83.8 | 30.1 | 26.1 |
| Pitakotte | LK-11 | 2.03 | 83.8 | 30.1 | 26.1 |
| Maharagama | LK-11 | 2.03 | 83.8 | 30.1 | 26.1 |
| Boralesgamuwa | LK-11 | 2.03 | 83.8 | 30.1 | 26.1 |
| Kaduwela | LK-11 | 2.02 | 96.0 | 30.4 | 24.9 |
| Piliyandala | LK-11 | 2.00 | 81.6 | 30.1 | 26.1 |
| Moratuwa | LK-11 | 2.00 | 81.6 | 30.1 | 26.1 |
| Dehiwala | LK-11 | 1.91 | 83.8 | 30.0 | 25.9 |
| Lahugala | LK-52 | 1.87 | 8.7 | 34.6 | 26.6 |
| Biyagama | LK-12 | 1.87 | 89.9 | 30.5 | 24.9 |
| Kelaniya | LK-12 | 1.84 | 79.6 | 30.1 | 25.9 |
| Pottuvil | LK-52 | 1.81 | 9.5 | 34.4 | 26.6 |
| Kolonnawa | LK-11 | 1.80 | 77.0 | 30.0 | 26.1 |
| Battaramulla | LK-11 | 1.80 | 77.0 | 30.0 | 26.1 |
| Nugegoda | LK-11 | 1.80 | 77.0 | 30.0 | 26.1 |
| Dompe | LK-12 | 1.79 | 114.2 | 29.8 | 23.8 |
| CMC | LK-11 | 1.78 | 77.0 | 30.0 | 26.0 |
| Kuruwita | LK-91 | 1.77 | 114.9 | 29.7 | 23.8 |
| Ottamavadi | LK-51 | 1.76 | 6.1 | 34.2 | 26.9 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.0829 |
| Spearman ρ | 0.1261 |
| *p*-value (Pearson) | 0.131 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Dehiovita | Kegalle | 2.48 | 0.0 |
| Rathmalana | Colombo | 2.03 | 0.0 |
| Moratuwa | Colombo | 2.00 | 0.0 |
| Dehiwala | Colombo | 1.91 | 0.0 |
| Lahugala | Ampara | 1.87 | 0.0 |
| Biyagama | Gampaha | 1.87 | 0.0 |
| Kelaniya | Gampaha | 1.84 | 0.0 |
| Pottuvil | Ampara | 1.81 | 0.0 |
| Kolonnawa | Colombo | 1.80 | 6.1 |
| Dompe | Gampaha | 1.79 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ruwanwella | Kegalle | -0.44 | 27.4 |
| Yatiyanthota | Kegalle | -0.26 | 24.1 |
| Wennappuwa | Puttalam | 0.48 | 21.6 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.89 | 21.0 |
| Pasbage Korale | Kandy | -1.39 | 16.8 |
| Galle Four Gravets | Galle | 0.58 | 13.8 |
| Kundasale | Kandy | -1.61 | 13.6 |
| Yatinuwara | Kandy | -0.85 | 12.3 |
| Harispattuwa | Kandy | -1.55 | 10.4 |
| Udapalatha | Kandy | -3.02 | 10.1 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6076.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (21 September 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (5 October 2026)

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
