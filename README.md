# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 10 August 2026 · 333 regions with model results._

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
| Ratnapura-Mc | LK-91 | 3.02 | 108.5 | 33.8 | 24.0 |
| Elapatha | LK-91 | 2.81 | 111.2 | 33.7 | 23.5 |
| Ayagama | LK-91 | 2.81 | 111.2 | 33.7 | 23.5 |
| Kuruwita | LK-91 | 2.73 | 111.0 | 33.1 | 23.9 |
| Eheliyagoda | LK-91 | 2.60 | 103.4 | 33.7 | 23.6 |
| Agalawatta | LK-13 | 2.58 | 118.5 | 32.9 | 23.3 |
| Dehiovita | LK-92 | 2.57 | 108.5 | 33.8 | 23.2 |
| Pelmadulla | LK-91 | 2.55 | 114.8 | 33.0 | 23.4 |
| Kiriella | LK-91 | 2.51 | 111.0 | 32.9 | 23.6 |
| Walallawita | LK-13 | 2.43 | 113.7 | 32.7 | 23.5 |
| Bulathkohupitiya | LK-92 | 2.35 | 101.9 | 33.2 | 23.6 |
| Neluwa | LK-31 | 2.33 | 102.5 | 32.6 | 24.0 |
| Bulathsinhala | LK-13 | 2.27 | 114.6 | 32.5 | 23.3 |
| Palindanuwara | LK-13 | 2.25 | 121.0 | 32.2 | 23.2 |
| Hanwella | LK-11 | 2.21 | 91.5 | 33.6 | 23.6 |
| Mathugama | LK-13 | 2.10 | 97.0 | 32.8 | 23.7 |
| Mahara | LK-12 | 2.06 | 86.4 | 33.7 | 23.5 |
| Thawalama | LK-31 | 2.04 | 97.0 | 32.7 | 23.7 |
| Dompe | LK-12 | 2.01 | 84.2 | 33.5 | 23.6 |
| Ingiriya | LK-13 | 2.00 | 104.0 | 32.6 | 23.3 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.1844 |
| Spearman ρ | 0.2543 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Elapatha | Ratnapura | 2.81 | 0.0 |
| Ayagama | Ratnapura | 2.81 | 0.0 |
| Walallawita | Kalutara | 2.43 | 0.0 |
| Neluwa | Galle | 2.33 | 0.0 |
| Palindanuwara | Kalutara | 2.25 | 0.0 |
| Thawalama | Galle | 2.04 | 0.0 |
| Beruwala | Kalutara | 1.93 | 0.0 |
| Kalutara | Kalutara | 1.79 | 0.0 |
| Madurawala | Kalutara | 1.79 | 0.0 |
| Niyagama | Galle | 1.70 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -2.61 | 160.0 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.21 | 69.6 |
| Ipalogama | Anuradhapura | -0.02 | 62.0 |
| Pasbage Korale | Kandy | -1.29 | 56.4 |
| Udunuwara | Kandy | -1.95 | 53.7 |
| Harispattuwa | Kandy | -1.39 | 53.3 |
| Kalawana | Ratnapura | -0.78 | 53.2 |
| Yatinuwara | Kandy | -1.06 | 50.1 |
| Akkaraipattu | Ampara | -0.34 | 45.7 |
| Badulla | Badulla | -5.27 | 42.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6271.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (24 August 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (7 September 2026)

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
