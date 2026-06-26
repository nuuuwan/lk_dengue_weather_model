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
| CMC | LK-11 | 19.42 | 23.5 | 31.8 | 25.0 |
| Dehiwala | LK-11 | 18.12 | 25.8 | 31.4 | 24.8 |
| Kattankudy | LK-51 | 16.50 | 13.7 | 29.1 | 25.7 |
| Kolonnawa | LK-11 | 15.93 | 23.5 | 31.8 | 25.0 |
| Moratuwa | LK-11 | 15.43 | 25.3 | 30.5 | 24.7 |
| Rathmalana | LK-11 | 14.57 | 25.8 | 31.5 | 24.9 |
| Kelaniya | LK-12 | 14.29 | 30.5 | 32.0 | 24.8 |
| Sainthamaruthu | LK-52 | 14.26 | 16.9 | 29.1 | 25.4 |
| Nugegoda | LK-11 | 13.91 | 23.5 | 31.8 | 25.0 |
| Pitakotte | LK-11 | 13.80 | 25.8 | 31.5 | 24.9 |
| Boralesgamuwa | LK-11 | 13.01 | 25.8 | 31.5 | 24.9 |
| Biyagama | LK-12 | 12.32 | 43.3 | 34.5 | 24.0 |
| Maharagama | LK-11 | 12.26 | 25.8 | 31.5 | 24.9 |
| Galle Four Gravets | LK-31 | 12.12 | 36.4 | 30.3 | 23.6 |
| Negambo | LK-12 | 11.44 | 18.9 | 31.9 | 24.2 |
| Battaramulla | LK-11 | 11.37 | 23.5 | 31.8 | 25.0 |
| Kaduwela | LK-11 | 11.15 | 46.3 | 33.6 | 23.8 |
| Ragama | LK-12 | 10.89 | 26.9 | 31.7 | 24.3 |
| Kalmunai South ( Muslim Div ) | LK-52 | 10.68 | 16.9 | 29.1 | 25.4 |
| Matara Mc | LK-32 | 10.56 | 34.4 | 30.2 | 23.9 |

> **Note:** Risk scores are weather-only (composite z-score of lagged
> meteorological predictors). Full GLM-based dengue
> incidence prediction requires historical case data (not yet integrated).

---

## Model Validation

Composite weather-risk score vs reported cases/100k (333 regions with available case data).

| Metric | Value |
|---|---:|
| Pearson *r* | 0.548 |
| Spearman ρ | 0.5652 |
| *p*-value (Pearson) | < 0.001 |
| Regions (*n*) | 333 |

![Predicted vs Actual Cases](images/correlation.png)

![Confusion Matrix](images/confusion_matrix.png)

![Confusion Map](images/confusion_map.png)

### Top 10 False Positives (high predicted risk, low actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Kattankudy | Batticaloa | 16.50 | 0.0 |
| Sainthamaruthu | Ampara | 14.26 | 0.0 |
| Kalmunai South ( Muslim Div ) | Ampara | 10.68 | 0.0 |
| Jaffna | Jaffna | 10.24 | 0.0 |
| Kalnumai North ( Tamil Div ) | Ampara | 9.40 | 0.0 |
| Gampaha | Gampaha | 9.30 | 16.8 |
| Trincomalee | Trincomalee | 9.16 | 0.0 |
| Koralaipattu ( Oddmavadi Central ) | Batticaloa | 8.51 | 0.0 |
| Beruwala | Kalutara | 8.38 | 0.0 |
| Eravur | Batticaloa | 7.88 | 0.0 |

### Top 10 False Negatives (low predicted risk, high actual cases)

| Region | District | Risk Score | Cases/100k |
|---|---|---:|---:|
| Ganga Ihala Korale | Kandy | -2.43 | 92.2 |
| Akuressa | Matara | 0.15 | 74.1 |
| Athuraliya | Matara | 1.42 | 57.9 |
| Thawalama | Galle | -2.79 | 54.9 |
| Palagala | Anuradhapura | -4.33 | 54.6 |
| Ayagama | Ratnapura | -2.05 | 47.6 |
| Pitabeddara | Matara | -0.25 | 45.0 |
| Nivithigala | Ratnapura | -0.22 | 43.7 |
| Kalawana | Ratnapura | -6.12 | 39.4 |
| Chilaw | Puttalam | 0.89 | 36.4 |

---

## Score Threshold Analysis

Proportion of MOH regions with ≥ 20 actual cases/100k among all regions with predicted risk score above a given threshold.

![Score Threshold vs High-Risk Proportion](images/precision_curve.png)

False positive rate (FPR) and false negative rate (FNR) for classifying regions as high-risk (≥ 20 cases/100k) at each threshold.

![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)

ROC curve with AUC = 0.8444.

![ROC Curve](images/roc_curve.png)

---

## Data Sources

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)
- **Region boundaries:** Ministry of Health Sri Lanka (333 MOH regions)
- **Model:** Erandi et al. (2021), *Int. J. Dynamical Systems and Differential Equations*, Vol. 11, Nos. 5/6, pp. 462–472.
