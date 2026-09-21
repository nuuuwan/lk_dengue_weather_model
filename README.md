# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 21 September 2026 · 333 regions with model results._

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
| Vakarai | LK-51 | 2.32 | 5.5 | 35.3 | 27.3 |
| Ottamavadi | LK-51 | 2.31 | 7.3 | 35.2 | 27.0 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 2.31 | 7.3 | 35.2 | 27.0 |
| Neluwa | LK-31 | 2.23 | 42.9 | 30.4 | 23.8 |
| Pelmadulla | LK-91 | 2.02 | 45.4 | 30.1 | 23.1 |
| Mullaitivu | LK-44 | 1.97 | 3.3 | 35.2 | 27.0 |
| Eravur | LK-51 | 1.94 | 5.1 | 34.8 | 26.9 |
| Eachchilampatru | LK-53 | 1.89 | 3.2 | 35.0 | 27.0 |
| Chenkalady | LK-51 | 1.87 | 7.0 | 35.0 | 26.2 |
| Kiran | LK-51 | 1.81 | 3.2 | 35.0 | 26.8 |
| Batticaloa | LK-51 | 1.80 | 3.8 | 34.6 | 27.0 |
| Sammanthurai | LK-52 | 1.79 | 13.7 | 34.3 | 25.2 |
| Kuruwita | LK-91 | 1.76 | 38.2 | 30.5 | 23.5 |
| Valaichenai | LK-51 | 1.74 | 2.9 | 35.2 | 26.5 |
| Vavunathivu | LK-51 | 1.73 | 4.2 | 35.1 | 26.3 |
| Thamankaduwa | LK-72 | 1.67 | 0.3 | 34.5 | 27.5 |
| Paddipalai | LK-51 | 1.65 | 4.3 | 35.0 | 26.2 |
| Puthukkudiyiruppu | LK-44 | 1.63 | 1.9 | 34.5 | 27.1 |
| Kuchchaveli | LK-53 | 1.59 | 1.4 | 34.9 | 26.8 |
| Trincomalee | LK-53 | 1.59 | 1.5 | 34.7 | 26.8 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0237 |
| Spearman ρ | -0.0161 |
| *p*-value (Pearson) | 0.666 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Vakarai | Batticaloa | 2.32 | 0.0 |
| Ottamavadi | Batticaloa | 2.31 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 2.31 | 0.0 |
| Neluwa | Galle | 2.23 | 0.0 |
| Pelmadulla | Ratnapura | 2.02 | 0.0 |
| Mullaitivu | Mullaitivu | 1.97 | 0.0 |
| Eravur | Batticaloa | 1.94 | 0.0 |
| Eachchilampatru | Trincomalee | 1.89 | 0.0 |
| Chenkalady | Batticaloa | 1.87 | 0.0 |
| Kiran | Batticaloa | 1.81 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Pasbage Korale | Kandy | -0.77 | 32.0 |
| Thalawa | Anuradhapura | -0.13 | 23.2 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.47 | 21.0 |
| Yatiyanthota | Kegalle | -0.50 | 17.7 |
| Pathadumbara | Kandy | -1.53 | 16.5 |
| Yatinuwara | Kandy | -1.93 | 15.8 |
| Kundasale | Kandy | -1.81 | 14.9 |
| Udunuwara | Kandy | -2.63 | 14.1 |
| Homagama | Colombo | 0.35 | 12.8 |
| Attanagalla | Gampaha | 0.26 | 12.1 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.4545.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (5 October 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (19 October 2026)

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
