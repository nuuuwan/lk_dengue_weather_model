# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 16 October 2026 · 333 regions with model results._

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
| Kuruwita | LK-91 | 2.49 | 291.3 | 29.3 | 23.6 |
| Kiriella | LK-91 | 2.34 | 291.3 | 29.1 | 23.4 |
| Ratnapura-Mc | LK-91 | 2.30 | 257.5 | 29.8 | 23.9 |
| Dehiovita | LK-92 | 2.27 | 286.8 | 29.0 | 23.4 |
| Mullaitivu | LK-44 | 2.02 | 33.6 | 35.7 | 26.8 |
| Uppuveli | LK-53 | 1.91 | 61.9 | 34.3 | 26.6 |
| Vakarai | LK-51 | 1.91 | 39.6 | 34.8 | 27.1 |
| Pelmadulla | LK-91 | 1.89 | 258.5 | 29.3 | 23.3 |
| Trincomalee | LK-53 | 1.87 | 52.1 | 34.5 | 26.8 |
| Kiran | LK-51 | 1.82 | 38.1 | 34.9 | 26.8 |
| Kandawalai | LK-45 | 1.80 | 16.9 | 35.4 | 27.1 |
| Puthukkudiyiruppu | LK-44 | 1.80 | 21.0 | 35.7 | 26.7 |
| Lahugala | LK-52 | 1.80 | 42.1 | 35.0 | 26.5 |
| Kinniya | LK-53 | 1.78 | 66.6 | 33.6 | 26.7 |
| Welioya | LK-43 | 1.78 | 45.1 | 34.6 | 26.7 |
| Eachchilampatru | LK-53 | 1.73 | 47.4 | 34.4 | 26.6 |
| Kuchchaveli | LK-53 | 1.72 | 39.3 | 34.5 | 26.9 |
| Vavunathivu | LK-51 | 1.70 | 57.5 | 34.4 | 26.1 |
| Muthur | LK-53 | 1.66 | 56.1 | 33.8 | 26.7 |
| Valaichenai | LK-51 | 1.64 | 37.7 | 34.7 | 26.5 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0399 |
| Spearman ρ | -0.1431 |
| *p*-value (Pearson) | 0.468 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kuruwita | Ratnapura | 2.49 | 0.0 |
| Kiriella | Ratnapura | 2.34 | 0.0 |
| Ratnapura-Mc | Ratnapura | 2.30 | 0.0 |
| Dehiovita | Kegalle | 2.27 | 0.0 |
| Mullaitivu | Mullaitivu | 2.02 | 0.0 |
| Vakarai | Batticaloa | 1.91 | 0.0 |
| Uppuveli | Trincomalee | 1.91 | 0.0 |
| Pelmadulla | Ratnapura | 1.89 | 0.0 |
| Trincomalee | Trincomalee | 1.87 | 0.0 |
| Kiran | Batticaloa | 1.82 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ambanpola | Kurunegala | -0.64 | 78.4 |
| Ukuwela | Matale | -1.00 | 22.1 |
| Kundasale | Kandy | -1.62 | 20.4 |
| Yatinuwara | Kandy | -1.04 | 19.3 |
| Pathadumbara | Kandy | -1.00 | 17.5 |
| Ja-Ela | Gampaha | -0.29 | 17.4 |
| Dehiwala | Colombo | 0.12 | 17.1 |
| Harispattuwa | Kandy | -0.96 | 16.7 |
| Menikhinna | Kandy | -1.80 | 14.8 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.67 | 11.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.3542.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (26 October 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (9 November 2026)

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
