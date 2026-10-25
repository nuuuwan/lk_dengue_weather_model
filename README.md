# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 25 October 2026 · 333 regions with model results._

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
| Eravur | LK-51 | 2.35 | 23.6 | 36.2 | 26.8 |
| Sammanthurai | LK-52 | 2.23 | 27.1 | 36.9 | 25.4 |
| Navithanveli | LK-52 | 2.22 | 29.1 | 36.4 | 25.6 |
| Vavunathivu | LK-51 | 2.17 | 19.3 | 36.8 | 26.3 |
| Batticaloa | LK-51 | 2.12 | 23.2 | 35.5 | 26.8 |
| Paddipalai | LK-51 | 2.07 | 27.8 | 35.5 | 26.0 |
| Mullaitivu | LK-44 | 2.03 | 18.7 | 35.7 | 26.9 |
| Ottamavadi | LK-51 | 1.98 | 15.9 | 35.9 | 27.0 |
| Koralaipattu ( Oddmavadi Central ) | LK-51 | 1.98 | 15.9 | 35.9 | 27.0 |
| Neluwa | LK-31 | 1.97 | 81.3 | 29.0 | 24.1 |
| Pelmadulla | LK-91 | 1.97 | 87.2 | 29.0 | 23.4 |
| Puthukkudiyiruppu | LK-44 | 1.87 | 16.0 | 35.6 | 26.9 |
| Alayadivembu | LK-52 | 1.86 | 30.5 | 34.3 | 26.1 |
| Siyambalanduwa | LK-82 | 1.86 | 38.1 | 34.0 | 25.4 |
| Akkaraipattu | LK-52 | 1.86 | 30.5 | 34.3 | 26.1 |
| Thirukkovil | LK-52 | 1.86 | 41.8 | 32.7 | 25.9 |
| Hambantota | LK-33 | 1.85 | 25.1 | 35.1 | 26.1 |
| Karaithivu | LK-52 | 1.84 | 22.8 | 35.4 | 26.1 |
| Ninthavur | LK-52 | 1.84 | 22.8 | 35.4 | 26.1 |
| Ampara | LK-52 | 1.79 | 25.8 | 34.7 | 26.2 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | -0.0281 |
| Spearman ρ | -0.037 |
| *p*-value (Pearson) | 0.610 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Eravur | Batticaloa | 2.35 | 0.0 |
| Sammanthurai | Ampara | 2.23 | 0.0 |
| Navithanveli | Ampara | 2.22 | 0.0 |
| Vavunathivu | Batticaloa | 2.17 | 0.0 |
| Batticaloa | Batticaloa | 2.12 | 0.0 |
| Paddipalai | Batticaloa | 2.07 | 0.0 |
| Mullaitivu | Mullaitivu | 2.03 | 0.0 |
| Ottamavadi | Batticaloa | 1.98 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 1.98 | 0.0 |
| Pelmadulla | Ratnapura | 1.97 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ambanpola | Kurunegala | -0.76 | 78.4 |
| Ukuwela | Matale | -1.56 | 22.1 |
| Kundasale | Kandy | -2.70 | 20.4 |
| Yatinuwara | Kandy | -2.36 | 19.3 |
| Pathadumbara | Kandy | -2.37 | 17.5 |
| Ja-Ela | Gampaha | 0.47 | 17.4 |
| Harispattuwa | Kandy | -2.34 | 16.7 |
| Menikhinna | Kandy | -2.88 | 14.8 |
| Biyagama | Gampaha | 0.56 | 14.5 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -3.86 | 11.2 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.4519.

![ROC Curve](images/roc_curve.png)

---

## Forward-Looking Forecasts

Dengue weather-risk scores projected 2 and 4 weeks ahead, using the same lagged meteorological predictors applied to already-recorded historical weather.  All three maps (current + forecasts) share an identical colour scale so regional risk levels are directly comparable.

### 2-Week Forecast (2 November 2026)

![2-Week Forecast Risk Map](images/forecast_map_2w.png)

### 4-Week Forecast (16 November 2026)

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
