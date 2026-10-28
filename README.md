# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 28 October 2026 · 333 regions with model results._

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
| Ottamavadi | LK-51 | 2.63 | 24.4 | 36.5 | 27.8 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 2.63 | 24.4 | 36.5 | 27.8 |
| Kiran | LK-51 | 2.39 | 19.3 | 36.5 | 27.7 |
| Mullaitivu | LK-44 | 2.22 | 17.1 | 36.4 | 27.6 |
| Irakkamam | LK-52 | 2.02 | 26.8 | 35.6 | 26.7 |
| Ampara | LK-52 | 2.00 | 28.9 | 35.3 | 26.8 |
| Sammanthurai | LK-52 | 1.99 | 21.3 | 36.9 | 26.2 |
| Padiyathalawa | LK-52 | 1.97 | 19.7 | 36.3 | 26.8 |
| Vavunathivu | LK-51 | 1.94 | 17.1 | 36.7 | 26.6 |
| Mahaoya | LK-52 | 1.90 | 13.1 | 36.6 | 27.1 |
| Puthukkudiyiruppu | LK-44 | 1.90 | 11.3 | 36.3 | 27.5 |
| Chenkalady | LK-51 | 1.90 | 20.0 | 36.5 | 26.4 |
| Kuchchaveli | LK-53 | 1.86 | 8.7 | 36.4 | 27.6 |
| Vakarai | LK-51 | 1.85 | 12.9 | 35.9 | 27.5 |
| Vavuniya | LK-43 | 1.82 | 19.4 | 35.6 | 27.0 |
| Padavi Sri Pura | LK-53 | 1.80 | 8.8 | 36.3 | 27.5 |
| Valaichenai | LK-51 | 1.79 | 11.9 | 36.5 | 27.0 |
| Lunugamvehera | LK-33 | 1.76 | 14.4 | 36.8 | 26.4 |
| Agalawatta | LK-13 | 1.72 | 92.7 | 30.0 | 23.7 |
| Tissamaharama | LK-33 | 1.71 | 11.1 | 36.6 | 26.8 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0429 |
| Spearman ρ | -0.0752 |
| *p*-value (Pearson) | 0.436 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ottamavadi | Batticaloa | 2.63 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 2.63 | 0.0 |
| Kiran | Batticaloa | 2.39 | 0.0 |
| Mullaitivu | Mullaitivu | 2.22 | 0.0 |
| Irakkamam | Ampara | 2.02 | 0.0 |
| Ampara | Ampara | 2.00 | 0.0 |
| Sammanthurai | Ampara | 1.99 | 0.0 |
| Padiyathalawa | Ampara | 1.97 | 0.0 |
| Vavunathivu | Batticaloa | 1.94 | 0.0 |
| Mahaoya | Ampara | 1.90 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ambanpola | Kurunegala | -0.55 | 78.4 |
| Ukuwela | Matale | -1.55 | 22.1 |
| Kundasale | Kandy | -2.42 | 20.4 |
| Yatinuwara | Kandy | -2.07 | 19.3 |
| Pathadumbara | Kandy | -2.22 | 17.5 |
| Ja-Ela | Gampaha | 0.32 | 17.4 |
| Dompe | Gampaha | 0.37 | 17.1 |
| Harispattuwa | Kandy | -2.16 | 16.7 |
| Menikhinna | Kandy | -2.60 | 14.8 |
| Hanwella | Colombo | 0.30 | 13.1 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.38.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (9 November 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (23 November 2026)

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
