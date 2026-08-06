# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 6 August 2026 · 333 regions with model results._

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
| Ratnapura-Mc | LK-91 | 3.32 | 102.8 | 34.1 | 24.0 |
| Elapatha | LK-91 | 3.12 | 109.7 | 33.7 | 23.6 |
| Ayagama | LK-91 | 3.12 | 109.7 | 33.7 | 23.6 |
| Mathugama | LK-13 | 2.84 | 122.5 | 31.9 | 23.6 |
| Agalawatta | LK-13 | 2.81 | 119.2 | 32.3 | 23.5 |
| Kuruwita | LK-91 | 2.76 | 91.3 | 33.8 | 23.9 |
| Kiriella | LK-91 | 2.55 | 91.3 | 33.6 | 23.7 |
| Panadura | LK-13 | 2.51 | 96.6 | 31.3 | 25.3 |
| Kalutara | LK-13 | 2.41 | 105.5 | 31.3 | 24.5 |
| Palindanuwara | LK-13 | 2.37 | 115.7 | 31.6 | 23.4 |
| Eheliyagoda | LK-91 | 2.36 | 79.3 | 33.9 | 23.9 |
| Pelmadulla | LK-91 | 2.31 | 88.4 | 33.4 | 23.6 |
| Dehiovita | LK-92 | 2.27 | 82.2 | 33.9 | 23.4 |
| Walallawita | LK-13 | 2.24 | 99.3 | 32.2 | 23.7 |
| Bandaragama | LK-13 | 2.20 | 95.4 | 31.8 | 24.3 |
| Madurawala | LK-13 | 2.17 | 102.1 | 31.9 | 23.7 |
| Beruwala | LK-13 | 2.17 | 106.1 | 30.8 | 24.3 |
| Piliyandala | LK-11 | 2.10 | 87.4 | 31.1 | 25.2 |
| Moratuwa | LK-11 | 2.10 | 87.4 | 31.1 | 25.2 |
| Nugegoda | LK-11 | 2.03 | 79.1 | 31.5 | 25.3 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.1772 |
| Spearman ρ | 0.217 |
| *p*-value (Pearson) | 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Elapatha | Ratnapura | 3.12 | 0.0 |
| Ayagama | Ratnapura | 3.12 | 0.0 |
| Panadura | Kalutara | 2.51 | 0.0 |
| Kalutara | Kalutara | 2.41 | 0.0 |
| Palindanuwara | Kalutara | 2.37 | 0.0 |
| Walallawita | Kalutara | 2.24 | 0.0 |
| Beruwala | Kalutara | 2.17 | 0.0 |
| Madurawala | Kalutara | 2.17 | 0.0 |
| Hikkaduwa | Galle | 1.85 | 0.0 |
| Gonapinuwala | Galle | 1.82 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -3.05 | 160.0 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.88 | 69.6 |
| Ipalogama | Anuradhapura | 0.38 | 62.0 |
| Pasbage Korale | Kandy | -2.92 | 56.4 |
| Udunuwara | Kandy | -2.14 | 53.7 |
| Harispattuwa | Kandy | -1.42 | 53.3 |
| Kalawana | Ratnapura | -1.57 | 53.2 |
| Yatinuwara | Kandy | -1.48 | 50.1 |
| Akkaraipattu | Ampara | -0.05 | 45.7 |
| Badulla | Badulla | -4.76 | 42.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.5978.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (17 August 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (31 August 2026)

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
