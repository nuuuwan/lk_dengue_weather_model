# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 3 October 2026 · 333 regions with model results._

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
| Lahugala | LK-52 | 2.67 | 16.9 | 35.4 | 26.0 |
| Kiran | LK-51 | 2.28 | 7.4 | 34.6 | 27.9 |
| Paddipalai | LK-51 | 2.27 | 12.2 | 34.6 | 26.8 |
| Habaraduwa | LK-31 | 2.13 | 31.0 | 29.9 | 26.0 |
| Walallawita | LK-13 | 2.12 | 39.3 | 30.0 | 23.9 |
| Kataragama | LK-82 | 2.12 | 13.0 | 34.2 | 26.6 |
| Ratnapura-Mc | LK-91 | 2.10 | 41.8 | 29.5 | 23.6 |
| Mullaitivu | LK-44 | 2.10 | 8.3 | 34.2 | 27.7 |
| Valaichenai | LK-51 | 2.07 | 7.1 | 34.5 | 27.6 |
| Ottamavadi | LK-51 | 2.06 | 4.9 | 34.6 | 28.0 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 2.06 | 4.9 | 34.6 | 28.0 |
| Buttala | LK-82 | 2.03 | 13.7 | 34.3 | 26.0 |
| Bentota | LK-31 | 1.97 | 32.0 | 29.5 | 25.8 |
| Vellaveli | LK-51 | 1.94 | 12.2 | 34.3 | 26.2 |
| Sammanthurai | LK-52 | 1.92 | 14.3 | 34.5 | 25.4 |
| Siyambalanduwa | LK-82 | 1.91 | 17.8 | 34.2 | 24.8 |
| Tissamaharama | LK-33 | 1.91 | 8.1 | 34.6 | 26.8 |
| Wellawaya | LK-82 | 1.91 | 15.4 | 34.0 | 25.5 |
| Gonapinuwala | LK-31 | 1.89 | 29.1 | 29.8 | 26.0 |
| Hikkaduwa | LK-31 | 1.89 | 29.1 | 29.8 | 26.0 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.096 |
| Spearman ρ | -0.0616 |
| *p*-value (Pearson) | 0.080 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Lahugala | Ampara | 2.67 | 0.0 |
| Kiran | Batticaloa | 2.28 | 0.0 |
| Paddipalai | Batticaloa | 2.27 | 0.0 |
| Habaraduwa | Galle | 2.13 | 0.0 |
| Walallawita | Kalutara | 2.12 | 0.0 |
| Kataragama | Monaragala | 2.12 | 0.0 |
| Ratnapura-Mc | Ratnapura | 2.10 | 0.0 |
| Mullaitivu | Mullaitivu | 2.10 | 0.0 |
| Valaichenai | Batticaloa | 2.07 | 0.0 |
| Ottamavadi | Batticaloa | 2.06 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Pasbage Korale | Kandy | -2.30 | 21.4 |
| Udunuwara | Kandy | -2.53 | 19.8 |
| Kundasale | Kandy | -2.40 | 17.7 |
| Ruwanwella | Kegalle | -1.37 | 16.7 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.68 | 16.4 |
| Harispattuwa | Kandy | -2.47 | 15.7 |
| Pathadumbara | Kandy | -2.48 | 15.5 |
| Yatinuwara | Kandy | -2.02 | 14.1 |
| Hanwella | Colombo | 0.03 | 11.5 |
| Warakapola | Kegalle | -0.90 | 10.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.3661.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (12 October 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (26 October 2026)

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
