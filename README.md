# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.

> 📖 **Methodology:** [README.methodology.md](README.methodology.md)

_Last updated: 26 June 2026 · 333 regions with model results._

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
| CMC | LK-11 | 6.82 | 23.5 | 31.8 | 25.0 |
| Biyagama | LK-12 | 6.78 | 43.3 | 34.5 | 24.0 |
| Dehiwala | LK-11 | 6.46 | 25.8 | 31.4 | 24.8 |
| Homagama | LK-11 | 6.36 | 55.2 | 33.5 | 23.1 |
| Kaduwela | LK-11 | 6.30 | 46.3 | 33.6 | 23.8 |
| Mahara | LK-12 | 6.10 | 37.5 | 35.8 | 23.6 |
| Kolonnawa | LK-11 | 6.03 | 23.5 | 31.8 | 25.0 |
| Kelaniya | LK-12 | 6.02 | 30.5 | 32.0 | 24.8 |
| Rathmalana | LK-11 | 5.69 | 25.8 | 31.5 | 24.9 |
| Horana | LK-13 | 5.58 | 64.2 | 32.6 | 23.1 |
| Nugegoda | LK-11 | 5.53 | 23.5 | 31.8 | 25.0 |
| Moratuwa | LK-11 | 5.50 | 25.3 | 30.5 | 24.7 |
| Pitakotte | LK-11 | 5.50 | 25.8 | 31.5 | 24.9 |
| Gampaha | LK-12 | 5.41 | 35.4 | 34.6 | 23.7 |
| Boralesgamuwa | LK-11 | 5.29 | 25.8 | 31.5 | 24.9 |
| Maharagama | LK-11 | 5.10 | 25.8 | 31.5 | 24.9 |
| Kahathuduwa | LK-11 | 5.10 | 44.9 | 32.0 | 23.6 |
| Galle Four Gravets | LK-31 | 4.98 | 36.4 | 30.3 | 23.6 |
| Attanagalla | LK-12 | 4.93 | 35.0 | 36.0 | 23.5 |
| Kattankudy | LK-51 | 4.88 | 13.7 | 29.1 | 25.7 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.4853 |
| Spearman ρ | 0.5447 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kattankudy | Batticaloa | 4.88 | 0.0 |
| Sainthamaruthu | Ampara | 4.45 | 0.0 |
| Beruwala | Kalutara | 4.14 | 0.0 |
| Dankotuwa | Puttalam | 3.81 | 0.0 |
| Kalmunai South ( Muslim Div ) | Ampara | 3.54 | 0.0 |
| Jaffna | Jaffna | 3.53 | 0.0 |
| Trincomalee | Trincomalee | 3.29 | 0.0 |
| Kalnumai North ( Tamil Div ) | Ampara | 3.19 | 0.0 |
| Hakmana | Matara | 3.13 | 0.0 |
| Kiriella | Ratnapura | 3.00 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -2.45 | 92.2 |
| Thawalama | Galle | -0.60 | 54.9 |
| Palagala | Anuradhapura | -2.08 | 54.6 |
| Ayagama | Ratnapura | 0.10 | 47.6 |
| Kandy Four Gravets & Gangawata Korale | Kandy | -0.73 | 46.6 |
| Pitabeddara | Matara | 0.83 | 45.0 |
| Nivithigala | Ratnapura | 0.70 | 43.7 |
| Yatinuwara | Kandy | 0.61 | 39.6 |
| Kalawana | Ratnapura | -3.55 | 39.4 |
| Udunuwara | Kandy | 1.03 | 36.7 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 10 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 10 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.8338.

![ROC Curve](images/roc_curve.png)

---

## Data Sources

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)
- **Region boundaries:** Ministry of Health Sri Lanka (333 MOH regions)
- **Model:** Erandi et al. (2021), *Int. J. Dynamical Systems and Differential Equations*, Vol. 11, Nos. 5/6, pp. 462–472.
