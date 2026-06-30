# Methodology: Dengue Outbreak Prediction Model for Sri Lanka MOH Regions

## Overview

This repository implements the dengue outbreak prediction model for all 300+ Ministry of Health (MOH) regions across Sri Lanka, extending the approach described by Erandi, Perera, and Mahasinghe (2021) in _International Journal of Dynamical Systems and Differential Equations_, Vol. 11, Nos. 5/6, pp. 462–472 ([Paper](<research_papers/[2021 Erandi et al] Dengue outbreak prediction model for urban Colombo using meteorological data.pdf>)).

The original study developed a generalised linear regression model (GLM) that incorporates lagged meteorological variables — weekly rainfall, maximum temperature, and minimum temperature — to predict weekly dengue incidence approximately one month in advance. This implementation reproduces that model in Python and applies it independently to each MOH region, producing one prediction per region per week. Meteorological data for each region is sourced from the Open-Meteo API using the geographic centroid of that region as the representative point.

## Background and Motivation

Dengue fever is a vector-borne viral disease transmitted by _Aedes aegypti_ and _Aedes albopictus_ mosquitoes. Sri Lanka has experienced dengue as an endemic disease since 1962, with the CMC area — the most densely populated urban zone in the country, home to approximately 555,000 residents within 37 km² — consistently reporting the highest case counts nationally, accounting for roughly 25% of annual dengue cases. The city is subject to two monsoon seasons (Northeast: December–February; Southwest: May–September), and temperatures range from 22°C to 33°C, creating conditions highly favourable for mosquito breeding and viral replication.

Classical time-series models fail to capture the impact of external climatic drivers, and simple moving-average thresholds used by the Epidemiology Unit, Department of Health, do not adequately signal outbreak onset. A climate-driven predictive model that can anticipate outbreak magnitude several weeks ahead gives public health authorities actionable lead time to deploy vector control resources.

## Model Selection: Generalised Linear Regression

The model adopts a generalised linear regression framework (GLM), as proposed by McCullagh and Nelder (1989), treating weekly dengue incidence as the dependent variable and meteorological series as predictors. A key biological motivation for using GLM over simple time-series models is that the relationship between climate factors and dengue is non-linear: extreme rainfall or high temperatures can suppress mosquito vector abundance, so a linear combination of log-transformed dengue incidence with meteorological covariates captures the underlying dynamics more faithfully.

Because the weekly dengue incidence data contains zeros, one is added before taking the natural logarithm. Distribution fitting (validated using a histogram against a normal distribution) confirms that log(D + 1) follows an approximately normal distribution, satisfying the multivariate normality assumption of the GLM.

## Cross-Correlation Analysis and Lag Determination

A critical modelling step is establishing the time delay between each meteorological variable and observed dengue incidence. Erandi et al. computed Pearson cross-correlation coefficients between weekly dengue counts and each climate variable across lags of 0 to 20 weeks, using data from the CMC area for 2009–2015.

The results established three empirical lags:

| Meteorological Variable | Optimal Lag (weeks) |
|||
| Rainfall | 10 |
| Maximum temperature | 16 |
| Minimum temperature | 13 |

The 10-week lag for rainfall reflects the combined duration of the _Aedes_ mosquito lifecycle (approximately 1–2 weeks from egg to adult depending on temperature and nutrient availability) and the human incubation period for dengue (3–14 days). The longer temperature lags (13–16 weeks) are consistent with the biology: temperature modulates both the speed of larval development and the extrinsic incubation period of the virus within the mosquito, and these indirect effects propagate on a longer timescale than direct rainfall-driven breeding.

## Final Model Equation

To account for the autoregressive dynamics of dengue transmission — specifically, that current mosquito density depends on the infected human population approximately four weeks prior (one _Aedes_ generation cycle of ~2 weeks plus a 3–14 day incubation period) — the moderated regression equation incorporates a lagged dengue term alongside the climate predictors. The final model (Equation 3 in the paper) is:

$$\log(D_t + 1) = \beta_0 + \beta_1 R_{t-10} + \beta_2 MT_{t-16} + \beta_3 mT_{t-13} + \beta_4 D_{t-4}$$

where:

- $D_t$ is the reported weekly dengue incidence at week $t$
- $R_{t-10}$ is weekly rainfall 10 weeks prior
- $MT_{t-16}$ is weekly maximum temperature 16 weeks prior
- $mT_{t-13}$ is weekly minimum temperature 13 weeks prior
- $D_{t-4}$ is reported dengue incidence 4 weeks prior
- $\beta_0, \beta_1, \beta_2, \beta_3, \beta_4$ are the regression coefficients estimated by distribution fitting

Model parameters are estimated using the `glmfit` function in the original MATLAB implementation. In this Python implementation, the equivalent is provided by `statsmodels.GLM` with a Gaussian family and identity link on the log-transformed response.

## Outbreak Threshold

An epidemic threshold is defined as the mean weekly dengue incidence over the calibration period (2009–2015). When the model's predicted incidence exceeds this threshold, an outbreak state is flagged. This threshold is static in the current formulation; the authors note that a time-varying (moving) threshold would better reflect the secular increase in outbreak magnitude and is a direction for future work.

## Python Implementation

### Data Acquisition via Open-Meteo

The original study used data from the Meteorological Department of Sri Lanka. This implementation replaces that source with the [Open-Meteo](https://open-meteo.com/) historical weather API, which provides free, high-resolution (hourly and daily) meteorological records globally.

For each of the 300+ MOH regions, the geographic centroid of the region boundary is used as the representative coordinate for the Open-Meteo query. Weather conditions at the centroid are taken as representative of the region as a whole. This approach enables the same pipeline to run uniformly across all regions without requiring a dedicated weather station within each one.

Open-Meteo is queried for three variables at daily resolution:

- `precipitation_sum` — aggregated to weekly totals to represent $R_t$
- `temperature_2m_max` — averaged to weekly means to represent $MT_t$
- `temperature_2m_min` — averaged to weekly means to represent $mT_t$

Weekly aggregation aligns with the weekly epidemiological reporting cadence used in the original study and by the Sri Lanka Epidemiology Unit.

### Pipeline Structure

The Python pipeline in `workflows/pipeline.py` executes the following stages for **each MOH region independently**:

1. **Region enumeration**: Load the list of 300+ MOH regions and compute or retrieve the centroid coordinates for each.
2. **Fetch**: Query the Open-Meteo historical weather API for the centroid of the current region and the target date range; aggregate daily values to ISO calendar weeks.
3. **Lag construction**: For each predictor, shift the weekly time series by its empirical lag (10, 16, or 13 weeks) using `pandas.DataFrame.shift()`.
4. **Log transform**: Compute $\log(D_{t-4} + 1)$ for the autoregressive dengue term, sourced from Ministry of Health (MOH) weekly case data stored under `static_data/`.
5. **Model fitting**: Fit the GLM using `statsmodels.api.GLM` on the training period, recovering $\hat{\beta}_0$ through $\hat{\beta}_4$.
6. **Prediction**: Apply the fitted coefficients to the lagged feature matrix for the forecast period, then back-transform via $\hat{D}_t = \exp(\hat{y}_t) - 1$.
7. **Threshold comparison**: Compare $\hat{D}_t$ against the calibration-period mean. Weeks where the prediction exceeds the threshold are classified as outbreak weeks.

The pipeline produces one prediction series per MOH region, yielding 300+ independent regional forecasts per run.

### Dependencies

The implementation relies on the following Python packages:

- `pandas` — time series construction, weekly resampling, lag shifting
- `numpy` — numerical operations and log/exp transforms
- `statsmodels` — GLM fitting with Gaussian family
- `requests` or `openmeteo-requests` — Open-Meteo API client
- `utils-nuuuwan` — project utility functions

## Limitations and Adaptations

The original model was calibrated on 2009–2015 CMC data. This implementation uses Open-Meteo data, which derives from ERA5 reanalysis and station interpolation; minor discrepancies from Meteorological Department station records may affect coefficient estimates. Additionally, the original paper reports fitted $\beta$ coefficients derived from 2009–2015 data, and re-calibration on a longer or more recent time window is advisable. The autoregressive dengue term $D_{t-4}$ requires contemporaneous MOH case reporting, which is subject to the notification lag inherent in Sri Lanka's epidemiological surveillance system.

## Reference

Erandi, K.K.W.H., Perera, S.S.N. and Mahasinghe, A.C. (2021) 'Dengue outbreak prediction model for urban Colombo using meteorological data', _Int. J. Dynamical Systems and Differential Equations_, Vol. 11, Nos. 5/6, pp. 462–472.
