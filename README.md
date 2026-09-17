# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 17 September 2026 · 333 regions with model results._

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
| Kiran | LK-51 | 2.63 | 12.4 | 35.6 | 26.5 |
| Valaichenai | LK-51 | 2.43 | 11.5 | 35.6 | 26.2 |
| Ottamavadi | LK-51 | 2.35 | 9.0 | 35.4 | 26.8 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 2.35 | 9.0 | 35.4 | 26.8 |
| Vakarai | LK-51 | 1.94 | 3.6 | 35.0 | 27.2 |
| Mathugama | LK-13 | 1.93 | 42.6 | 29.8 | 24.0 |
| Eachchilampatru | LK-53 | 1.92 | 6.3 | 34.8 | 26.9 |
| Vavunathivu | LK-51 | 1.89 | 6.8 | 35.2 | 26.3 |
| Paddipalai | LK-51 | 1.88 | 10.9 | 34.5 | 26.0 |
| Mullaitivu | LK-44 | 1.88 | 5.6 | 35.2 | 26.6 |
| Lahugala | LK-52 | 1.82 | 5.8 | 35.2 | 26.3 |
| Madurawala | LK-13 | 1.81 | 44.1 | 29.4 | 23.7 |
| Kandawalai | LK-45 | 1.81 | 7.2 | 34.0 | 27.2 |
| Batticaloa | LK-51 | 1.76 | 8.0 | 33.9 | 27.0 |
| Chenkalady | LK-51 | 1.70 | 4.8 | 35.0 | 26.4 |
| Thamankaduwa | LK-72 | 1.68 | 0.8 | 34.8 | 27.4 |
| Welikanda | LK-72 | 1.66 | 2.9 | 34.6 | 27.1 |
| Kalutara | LK-13 | 1.64 | 36.2 | 29.6 | 24.8 |
| Kuruwita | LK-91 | 1.64 | 39.4 | 30.1 | 23.7 |
| Beruwala | LK-13 | 1.62 | 36.4 | 29.4 | 24.9 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0305 |
| Spearman ρ | -0.0391 |
| *p*-value (Pearson) | 0.579 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kiran | Batticaloa | 2.63 | 0.0 |
| Valaichenai | Batticaloa | 2.43 | 0.0 |
| Ottamavadi | Batticaloa | 2.35 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 2.35 | 0.0 |
| Vakarai | Batticaloa | 1.94 | 0.0 |
| Mathugama | Kalutara | 1.93 | 0.0 |
| Eachchilampatru | Trincomalee | 1.92 | 0.0 |
| Vavunathivu | Batticaloa | 1.89 | 0.0 |
| Mullaitivu | Mullaitivu | 1.88 | 0.0 |
| Paddipalai | Batticaloa | 1.88 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Pasbage Korale | Kandy | -0.96 | 32.0 |
| Thalawa | Anuradhapura | -0.04 | 23.2 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.20 | 21.0 |
| Yatiyanthota | Kegalle | -0.52 | 17.7 |
| Pathadumbara | Kandy | -1.21 | 16.5 |
| Yatinuwara | Kandy | -1.51 | 15.8 |
| Wennappuwa | Puttalam | 0.15 | 15.4 |
| Kundasale | Kandy | -1.85 | 14.9 |
| Weligama | Matara | 0.22 | 14.4 |
| Udunuwara | Kandy | -2.35 | 14.1 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.4413.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (28 September 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (12 October 2026)

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
