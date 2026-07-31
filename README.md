# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 31 July 2026 · 333 regions with model results._

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
| Rathmalana | LK-11 | 2.99 | 138.3 | 32.4 | 25.5 |
| Boralesgamuwa | LK-11 | 2.99 | 138.3 | 32.4 | 25.5 |
| Pitakotte | LK-11 | 2.99 | 138.3 | 32.4 | 25.5 |
| Maharagama | LK-11 | 2.99 | 138.3 | 32.4 | 25.5 |
| Kelaniya | LK-12 | 2.95 | 140.6 | 32.3 | 25.4 |
| Nugegoda | LK-11 | 2.94 | 132.1 | 32.5 | 25.6 |
| Kolonnawa | LK-11 | 2.94 | 132.1 | 32.5 | 25.6 |
| Battaramulla | LK-11 | 2.94 | 132.1 | 32.5 | 25.6 |
| CMC | LK-11 | 2.92 | 132.1 | 32.5 | 25.6 |
| Dehiwala | LK-11 | 2.89 | 138.3 | 32.3 | 25.4 |
| Kuruwita | LK-91 | 2.86 | 137.8 | 33.4 | 24.1 |
| Kahathuduwa | LK-11 | 2.82 | 145.3 | 32.9 | 24.2 |
| Mahara | LK-12 | 2.77 | 121.5 | 33.7 | 24.4 |
| Attanagalla | LK-12 | 2.72 | 119.7 | 33.8 | 24.3 |
| Kiriella | LK-91 | 2.66 | 137.8 | 33.2 | 23.9 |
| Gampaha | LK-12 | 2.64 | 116.2 | 33.6 | 24.5 |
| Kaduwela | LK-11 | 2.64 | 131.1 | 32.8 | 24.6 |
| Biyagama | LK-12 | 2.63 | 125.1 | 33.1 | 24.6 |
| Dehiovita | LK-92 | 2.58 | 135.2 | 33.6 | 23.4 |
| Panadura | LK-13 | 2.55 | 121.8 | 32.4 | 25.4 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.2808 |
| Spearman ρ | 0.3033 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Panadura | Kalutara | 2.55 | 0.0 |
| Kalutara | Kalutara | 2.07 | 0.0 |
| Madurawala | Kalutara | 1.93 | 0.0 |
| Elapatha | Ratnapura | 1.91 | 0.0 |
| Ayagama | Ratnapura | 1.91 | 0.0 |
| Chavakachcheri | Jaffna | 1.37 | 0.0 |
| Kopay | Jaffna | 1.35 | 0.0 |
| Manthai East | Mullaitivu | 1.33 | 0.0 |
| Uduvil | Jaffna | 1.33 | 0.0 |
| Kilinochchi | Kilinochchi | 1.32 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -3.10 | 160.0 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -2.86 | 69.6 |
| Ipalogama | Anuradhapura | 0.26 | 62.0 |
| Pasbage Korale | Kandy | -2.90 | 56.4 |
| Udunuwara | Kandy | -2.09 | 53.7 |
| Harispattuwa | Kandy | -1.47 | 53.3 |
| Kalawana | Ratnapura | -2.00 | 53.2 |
| Yatinuwara | Kandy | -1.16 | 50.1 |
| Akkaraipattu | Ampara | 0.22 | 45.7 |
| Badulla | Badulla | -4.53 | 42.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.6483.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (10 August 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (24 August 2026)

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
