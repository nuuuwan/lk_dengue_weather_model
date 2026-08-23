# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 23 August 2026 · 333 regions with model results._

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
| Pannala | LK-61 | 2.55 | 125.0 | 34.3 | 23.8 |
| Divulapitiya | LK-12 | 2.53 | 130.8 | 33.9 | 23.7 |
| Dankotuwa | LK-62 | 2.51 | 124.8 | 33.9 | 24.1 |
| Nattandiya | LK-62 | 2.36 | 126.5 | 32.5 | 24.9 |
| Wennappuwa | LK-62 | 2.26 | 126.5 | 32.4 | 24.8 |
| Thamankaduwa | LK-72 | 2.16 | 26.0 | 36.2 | 27.2 |
| Arachchikattuwa | LK-62 | 2.13 | 104.7 | 32.2 | 26.1 |
| Mahawewa | LK-62 | 2.11 | 113.6 | 32.5 | 25.2 |
| Kuliyapitiya | LK-61 | 2.04 | 104.5 | 33.8 | 24.3 |
| Chilaw | LK-62 | 2.02 | 108.3 | 32.4 | 25.4 |
| Panduwasnuwara | LK-61 | 1.98 | 98.8 | 33.8 | 24.6 |
| Udubaddawa | LK-61 | 1.96 | 116.4 | 32.9 | 24.3 |
| Kandawalai | LK-45 | 1.86 | 5.2 | 36.2 | 27.8 |
| Katupotha | LK-61 | 1.85 | 97.8 | 33.6 | 24.5 |
| Minuwangoda | LK-12 | 1.79 | 105.4 | 33.5 | 24.0 |
| Kuruwita | LK-91 | 1.79 | 120.4 | 32.5 | 24.0 |
| Katana | LK-12 | 1.77 | 110.4 | 32.5 | 24.6 |
| Kopay | LK-41 | 1.77 | 21.9 | 34.0 | 28.7 |
| Negambo | LK-12 | 1.77 | 110.4 | 32.5 | 24.6 |
| Karaveddy | LK-41 | 1.76 | 8.9 | 34.9 | 28.6 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.1214 |
| Spearman ρ | 0.1322 |
| *p*-value (Pearson) | 0.027 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Thamankaduwa | Polonnaruwa | 2.16 | 0.0 |
| Arachchikattuwa | Puttalam | 2.13 | 0.0 |
| Mahawewa | Puttalam | 2.11 | 0.0 |
| Kuliyapitiya | Kurunegala | 2.04 | 0.0 |
| Chilaw | Puttalam | 2.02 | 9.8 |
| Panduwasnuwara | Kurunegala | 1.98 | 0.0 |
| Udubaddawa | Kurunegala | 1.96 | 0.0 |
| Kandawalai | Kilinochchi | 1.86 | 0.0 |
| Katupotha | Kurunegala | 1.85 | 0.0 |
| Kopay | Jaffna | 1.77 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.99 | 44.6 |
| Yakkalamulla | Galle | -0.57 | 38.6 |
| Hatharaliyadda | Kandy | 0.23 | 38.5 |
| Ruwanwella | Kegalle | 0.16 | 38.0 |
| Ganga Ihala Korale | Kandy | -2.66 | 37.6 |
| Tangalle | Hambantota | -0.77 | 36.5 |
| Udapalatha | Kandy | -2.76 | 35.7 |
| Yatinuwara | Kandy | -0.79 | 33.4 |
| Mawanella | Kegalle | 0.50 | 32.5 |
| Harispattuwa | Kandy | -1.27 | 32.4 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.5711.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (31 August 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (14 September 2026)

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
