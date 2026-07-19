# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 19 July 2026 · 333 regions with model results._

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
| Galenbidunuwawe | LK-71 | 3.05 | 125.7 | 34.1 | 24.2 |
| Cheddikulam | LK-43 | 2.75 | 90.8 | 36.9 | 24.7 |
| Kekirawa | LK-71 | 2.73 | 132.1 | 33.0 | 23.8 |
| Nuwaragam Palatha East | LK-71 | 2.70 | 108.7 | 34.9 | 24.5 |
| Karuwalagaswewa | LK-62 | 2.67 | 98.6 | 36.0 | 24.4 |
| Puttalam | LK-62 | 2.55 | 104.3 | 35.2 | 24.4 |
| Kobeigane | LK-61 | 2.46 | 89.7 | 36.5 | 24.5 |
| Mihintale | LK-71 | 2.46 | 104.7 | 34.8 | 24.4 |
| Nochchiyagama | LK-71 | 2.41 | 89.3 | 36.4 | 24.5 |
| Mallawapitiya | LK-61 | 2.41 | 88.9 | 37.0 | 24.0 |
| Kurunegala | LK-61 | 2.41 | 88.9 | 37.0 | 24.0 |
| Lankapura | LK-72 | 2.31 | 108.9 | 33.5 | 24.8 |
| Lunugamvehera | LK-33 | 2.30 | 97.1 | 35.2 | 24.5 |
| Nikaweratiya | LK-61 | 2.30 | 86.2 | 36.4 | 24.5 |
| Okewela | LK-33 | 2.28 | 115.3 | 34.4 | 23.2 |
| Rajanganaya | LK-71 | 2.24 | 88.3 | 35.8 | 24.8 |
| Madhu | LK-42 | 2.24 | 84.2 | 36.4 | 24.6 |
| Giribawa | LK-61 | 2.19 | 84.3 | 36.0 | 24.8 |
| Ambanpola | LK-61 | 2.19 | 92.1 | 35.8 | 24.2 |
| Thalawa | LK-71 | 2.14 | 91.9 | 35.3 | 24.5 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.1992 |
| Spearman ρ | -0.2919 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Galenbidunuwawe | Anuradhapura | 3.05 | 0.0 |
| Cheddikulam | Vavuniya | 2.75 | 0.0 |
| Kekirawa | Anuradhapura | 2.73 | 0.0 |
| Nuwaragam Palatha East | Anuradhapura | 2.70 | 0.0 |
| Karuwalagaswewa | Puttalam | 2.67 | 0.0 |
| Puttalam | Puttalam | 2.55 | 0.0 |
| Mihintale | Anuradhapura | 2.46 | 0.0 |
| Kobeigane | Kurunegala | 2.46 | 0.0 |
| Nochchiyagama | Anuradhapura | 2.41 | 0.0 |
| Mallawapitiya | Kurunegala | 2.41 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kelaniya | Gampaha | -1.61 | 191.4 |
| Biyagama | Gampaha | -0.00 | 154.5 |
| Boralesgamuwa | Colombo | -1.22 | 145.2 |
| Battaramulla | Colombo | -1.24 | 138.3 |
| Ganga Ihala Korale | Kandy | -2.27 | 133.6 |
| Maharagama | Colombo | -1.22 | 125.0 |
| Ja-Ela | Gampaha | -1.52 | 122.6 |
| Wennappuwa | Puttalam | -0.81 | 98.8 |
| Wattala | Gampaha | -1.52 | 91.9 |
| Nugegoda | Colombo | -1.24 | 87.7 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.3393.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (27 July 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (10 August 2026)

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
