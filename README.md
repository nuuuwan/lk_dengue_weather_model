# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 7 November 2026 · 333 regions with model results._

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
| Kiran | LK-51 | 2.25 | 16.3 | 36.9 | 26.5 |
| Irakkamam | LK-52 | 2.23 | 34.2 | 36.1 | 25.5 |
| Valaichenai | LK-51 | 2.08 | 11.2 | 36.9 | 26.4 |
| Lahugala | LK-52 | 2.08 | 21.0 | 37.5 | 25.2 |
| Uhana | LK-52 | 2.07 | 22.7 | 36.6 | 25.8 |
| Vellaveli | LK-51 | 2.02 | 37.2 | 35.0 | 25.7 |
| Ottamavadi | LK-51 | 2.01 | 19.1 | 35.5 | 26.7 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 2.01 | 19.1 | 35.5 | 26.7 |
| Pottuvil | LK-52 | 1.98 | 26.6 | 36.2 | 25.5 |
| Paddipalai | LK-51 | 1.90 | 29.2 | 35.0 | 26.1 |
| Akkaraipattu | LK-52 | 1.90 | 31.4 | 35.5 | 25.5 |
| Vavunathivu | LK-51 | 1.90 | 18.4 | 36.2 | 26.0 |
| Alayadivembu | LK-52 | 1.90 | 31.4 | 35.5 | 25.5 |
| Lunugamvehera | LK-33 | 1.87 | 20.7 | 36.3 | 25.6 |
| Damana | LK-52 | 1.82 | 34.0 | 35.6 | 25.0 |
| Navithanveli | LK-52 | 1.77 | 27.6 | 35.6 | 25.4 |
| Kataragama | LK-82 | 1.76 | 12.6 | 36.9 | 25.5 |
| Mahaoya | LK-52 | 1.76 | 9.3 | 36.8 | 25.9 |
| Sammanthurai | LK-52 | 1.73 | 19.6 | 36.5 | 25.3 |
| Ampara | LK-52 | 1.71 | 17.8 | 36.0 | 25.7 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0537 |
| Spearman ρ | -0.0789 |
| *p*-value (Pearson) | 0.328 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kiran | Batticaloa | 2.25 | 0.0 |
| Irakkamam | Ampara | 2.23 | 0.0 |
| Valaichenai | Batticaloa | 2.08 | 0.0 |
| Lahugala | Ampara | 2.08 | 0.0 |
| Uhana | Ampara | 2.07 | 0.0 |
| Vellaveli | Batticaloa | 2.02 | 0.0 |
| Ottamavadi | Batticaloa | 2.01 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 2.01 | 0.0 |
| Pottuvil | Ampara | 1.98 | 0.0 |
| Akkaraipattu | Ampara | 1.90 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kundasale | Kandy | -2.03 | 34.0 |
| Udunuwara | Kandy | -2.51 | 21.2 |
| Menikhinna | Kandy | -2.21 | 20.8 |
| Pathadumbara | Kandy | -2.19 | 20.6 |
| Yatinuwara | Kandy | -1.80 | 20.2 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.43 | 19.7 |
| Ukuwela | Matale | -1.75 | 19.4 |
| Dompe | Gampaha | 0.14 | 18.9 |
| Harispattuwa | Kandy | -2.17 | 15.7 |
| Badulla | Badulla | -2.54 | 13.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.3999.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (16 November 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (30 November 2026)

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
