# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 6 July 2026 · 333 regions with model results._

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
| Welivitiya-Divithura | LK-31 | 3.04 | 92.1 | 32.7 | 24.0 |
| Bulathsinhala | LK-13 | 3.04 | 90.6 | 33.3 | 23.5 |
| Madurawala | LK-13 | 3.01 | 85.6 | 33.5 | 23.9 |
| Pitabeddara | LK-32 | 2.88 | 82.9 | 33.3 | 24.1 |
| Akuressa | LK-32 | 2.69 | 82.1 | 33.0 | 24.1 |
| Karandeniya | LK-31 | 2.63 | 80.4 | 32.8 | 24.4 |
| Godakawela | LK-91 | 2.49 | 92.5 | 32.1 | 23.2 |
| Elpitiya | LK-31 | 2.48 | 75.1 | 33.2 | 24.2 |
| Mahara | LK-12 | 2.42 | 66.0 | 34.0 | 24.4 |
| Niyagama | LK-31 | 2.42 | 72.5 | 33.4 | 24.2 |
| Beliatta | LK-33 | 2.38 | 79.0 | 32.2 | 24.6 |
| Hakmana | LK-32 | 2.38 | 79.0 | 32.2 | 24.6 |
| Galle Four Gravets | LK-31 | 2.37 | 77.5 | 31.6 | 25.3 |
| Bope-Poddala | LK-31 | 2.37 | 77.5 | 31.6 | 25.3 |
| Ayagama | LK-91 | 2.30 | 67.0 | 34.6 | 23.4 |
| Elapatha | LK-91 | 2.30 | 67.0 | 34.6 | 23.4 |
| Dompe | LK-12 | 2.28 | 70.5 | 33.5 | 24.0 |
| Sooriyawewa | LK-33 | 2.25 | 65.2 | 33.4 | 24.7 |
| Athuraliya | LK-32 | 2.23 | 73.5 | 32.8 | 24.3 |
| Thamankaduwa | LK-72 | 2.19 | 70.5 | 32.5 | 24.9 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.1675 |
| Spearman ρ | 0.2569 |
| *p*-value (Pearson) | 0.002 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Welivitiya-Divithura | Galle | 3.04 | 0.0 |
| Niyagama | Galle | 2.42 | 0.0 |
| Ayagama | Ratnapura | 2.30 | 0.0 |
| Elapatha | Ratnapura | 2.30 | 0.0 |
| Sooriyawewa | Hambantota | 2.25 | 0.0 |
| Okewela | Hambantota | 2.11 | 0.0 |
| Mahawa | Kurunegala | 2.09 | 0.0 |
| Gonapinuwala | Galle | 1.99 | 0.0 |
| Wariyapola | Kurunegala | 1.98 | 0.0 |
| Rathgama | Galle | 1.93 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kelaniya | Gampaha | 0.25 | 162.2 |
| Seeduwa | Gampaha | -0.45 | 130.2 |
| Negambo | Gampaha | -0.14 | 130.2 |
| Ja-Ela | Gampaha | 0.29 | 112.4 |
| Wennappuwa | Puttalam | -0.31 | 88.0 |
| Wattala | Gampaha | 0.29 | 85.3 |
| Ragama | Gampaha | 0.29 | 78.4 |
| Ganga Ihala Korale | Kandy | -1.67 | 75.3 |
| Yatinuwara | Kandy | -1.14 | 71.2 |
| Battaramulla | Colombo | 0.28 | 68.6 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6589.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (20 July 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (3 August 2026)

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
