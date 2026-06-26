"""
Generate forward-looking dengue weather risk maps for:
  - 2 weeks from the most recent complete data week
  - 4 weeks from the most recent complete data week

All required lagged inputs (R_lag10, MT_lag16, mT_lag13) are already
available in historical weather data, so no weather forecasting is needed.

Lag logic:
  R_lag10(W)  = rainfall    at week W-10
  MT_lag16(W) = max_temp    at week W-16
  mT_lag13(W) = min_temp    at week W-13

For week W+k (forecast horizon k weeks ahead):
  R_lag10  = weekly_features[-(10-k)].rainfall   → index offset from latest
  MT_lag16 = weekly_features[-(16-k)].max_temp
  mT_lag13 = weekly_features[-(13-k)].min_temp
"""

import datetime
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import topojson as tp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

DIR_MODEL_RESULTS = os.path.join("data", "model_results")
TOPOJSON_PATH = os.path.join("moh_data", "geo", "moh.topojson")
MOH_JSON = os.path.join("moh_data", "ent", "moh.json")
DENSITY_WEIGHT = 2
DENSITY_EXPONENT = 0.05


def load_all_weekly_features() -> dict:
    """Returns {region_id: [weekly_feature_dicts...]} for all regions."""
    result = {}
    for fname in os.listdir(DIR_MODEL_RESULTS):
        if not fname.endswith(".json"):
            continue
        data = json.load(open(os.path.join(DIR_MODEL_RESULTS, fname)))
        features = data.get("weekly_features") or []
        if len(features) >= 17:  # need at least 17 entries to cover lag-16
            result[data["region_id"]] = features
    return result


def extract_forecast_features(all_features: dict, horizon_weeks: int) -> dict:
    """
    For each region, compute the lagged feature values for a forecast
    horizon of `horizon_weeks` weeks beyond the most recent data week.

    Returns {region_id: {"R_lag10": ..., "MT_lag16": ..., "mT_lag13": ...,
                          "forecast_week": "YYYY-MM-DD"}}
    """
    result = {}
    for region_id, features in all_features.items():
        n = len(features)
        # Indices into features list (from the end):
        #   latest week = features[-1] = features[n-1]
        #
        # For horizon h (weeks ahead of latest):
        #   R_lag10(latest+h)  = rainfall at (latest+h-10) = latest-(10-h)
        #   MT_lag16(latest+h) = max_temp at (latest+h-16) = latest-(16-h)
        #   mT_lag13(latest+h) = min_temp at (latest+h-13) = latest-(13-h)
        #
        # In list indices from current tail:
        #   r_idx  = n - 1 - (10 - horizon_weeks)
        #   mt_idx = n - 1 - (16 - horizon_weeks)
        #   mt2_idx= n - 1 - (13 - horizon_weeks)

        r_offset = 10 - horizon_weeks  # how many weeks back from latest
        mt_offset = 16 - horizon_weeks
        mt2_offset = 13 - horizon_weeks

        r_idx = n - 1 - r_offset
        mt_idx = n - 1 - mt_offset
        mt2_idx = n - 1 - mt2_offset

        if r_idx < 0 or mt_idx < 0 or mt2_idx < 0:
            continue  # not enough history

        r_lag10 = features[r_idx].get("rainfall")
        mt_lag16 = features[mt_idx].get("max_temp")
        mt_lag13 = features[mt2_idx].get("min_temp")

        if any(v is None for v in [r_lag10, mt_lag16, mt_lag13]):
            continue

        # Compute forecast week date
        latest_week_str = features[-1]["week"]
        latest_week = datetime.date.fromisoformat(latest_week_str)
        forecast_week = latest_week + datetime.timedelta(weeks=horizon_weeks)

        result[region_id] = {
            "R_lag10": r_lag10,
            "MT_lag16": mt_lag16,
            "mT_lag13": mt_lag13,
            "forecast_week": forecast_week.isoformat(),
        }
    return result


def zscore(arr: np.ndarray) -> np.ndarray:
    std = arr.std()
    return (arr - arr.mean()) / std if std > 0 else np.zeros_like(arr)


def composite_scores(forecast_features: dict, density: dict) -> dict:
    rids = list(forecast_features.keys())
    vals = {
        k: np.array([float(forecast_features[r].get(k) or 0.0) for r in rids])
        for k in ("R_lag10", "MT_lag16", "mT_lag13")
    }
    composite = sum(zscore(v) for v in vals.values())
    if density and DENSITY_WEIGHT:
        d_arr = np.array([float(density.get(r) or 0.0) for r in rids])
        composite = composite + DENSITY_WEIGHT * zscore(d_arr)
    return dict(zip(rids, composite.tolist()))


def load_density() -> dict:
    moh_data = json.load(open(MOH_JSON))
    return {
        d["region_id"]: d["population_density"] ** DENSITY_EXPONENT
        for d in moh_data
    }


def load_region_names() -> dict:
    moh_data = json.load(open(MOH_JSON))
    return {d["region_id"]: d["region_name"] for d in moh_data}


def label_fontsize(ax, geom, label):
    b = geom.bounds
    p0 = ax.transData.transform((b[0], b[1]))
    p1 = ax.transData.transform((b[2], b[3]))
    w_px = abs(p1[0] - p0[0])
    h_px = abs(p1[1] - p0[1])
    dpi = ax.figure.dpi
    n = max(len(label), 1)
    fs_w = w_px * 72 / (dpi * 0.6 * n)
    fs_h = h_px * 72 / (dpi * 1.2)
    return max(1.5, min(fs_w, fs_h, 7)) * 0.5


def render_delta_map(
    delta_scores: dict,
    forecast_date: str,
    horizon_label: str,
    output_path: str,
    vmax: float = None,
):
    with open(TOPOJSON_PATH) as f:
        gdf = tp.Topology(json.load(f)).to_gdf()

    region_names = load_region_names()
    name_to_score = {}
    for region_id, score in delta_scores.items():
        rname = region_names.get(region_id, "")
        name_to_score[rname.upper()] = score

    gdf["delta_score"] = gdf["MOH_N"].str.upper().map(name_to_score)

    if vmax is None:
        if gdf["delta_score"].notna().any():
            vmax = float(gdf["delta_score"].abs().quantile(0.97))
            vmax = max(vmax, 0.1)
        else:
            vmax = 1.0

    fig, ax = plt.subplots(figsize=(10, 14))
    fig.patch.set_facecolor("#f8f8f8")
    ax.set_facecolor("#cce6ff")

    gdf[gdf["delta_score"].isna()].plot(
        ax=ax, color="#d0d0d0", edgecolor="white", linewidth=0.3
    )
    if gdf["delta_score"].notna().any():
        gdf[gdf["delta_score"].notna()].plot(
            ax=ax,
            column="delta_score",
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
            edgecolor="white",
            linewidth=0.3,
            legend=True,
            legend_kwds={
                "label": "Change in Risk Score (Δ composite z-score)",
                "shrink": 0.55,
                "orientation": "vertical",
            },
        )

    for _, row in gdf.iterrows():
        c = row.geometry.centroid
        label = row["MOH_N"].title()
        ax.annotate(
            label,
            xy=(c.x, c.y),
            ha="center",
            va="center",
            fontsize=label_fontsize(ax, row.geometry, label),
            color="#ffffff",
            clip_on=True,
        )

    formatted_date = datetime.date.fromisoformat(forecast_date).strftime(
        "%-d %B %Y"
    )
    ax.set_title(
        f"Sri Lanka — MOH Dengue Risk Change\n"
        f"Forecast: {formatted_date}  ({horizon_label} vs. current)",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.axis("off")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout(pad=0.5)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {output_path}")


def render_forecast_map(
    scores: dict,
    forecast_date: str,
    horizon_label: str,
    output_path: str,
    vmin: float = None,
    vmax: float = None,
):
    with open(TOPOJSON_PATH) as f:
        gdf = tp.Topology(json.load(f)).to_gdf()

    # Map region names to scores (same logic as RiskMap._build_gdf)
    region_names = load_region_names()
    name_to_score = {}
    for region_id, score in scores.items():
        rname = region_names.get(region_id, "")
        name_to_score[rname.upper()] = score

    gdf["risk_score"] = gdf["MOH_N"].str.upper().map(name_to_score)

    fig, ax = plt.subplots(figsize=(10, 14))
    fig.patch.set_facecolor("#f8f8f8")
    ax.set_facecolor("#cce6ff")

    gdf[gdf["risk_score"].isna()].plot(
        ax=ax, color="#d0d0d0", edgecolor="white", linewidth=0.3
    )
    if gdf["risk_score"].notna().any():
        plot_kwargs = dict(
            ax=ax,
            column="risk_score",
            cmap="RdBu_r",
            edgecolor="white",
            linewidth=0.3,
            legend=True,
            legend_kwds={
                "label": "Weather Risk Score (composite z-score)",
                "shrink": 0.55,
                "orientation": "vertical",
            },
        )
        if vmin is not None:
            plot_kwargs["vmin"] = vmin
        if vmax is not None:
            plot_kwargs["vmax"] = vmax
        gdf[gdf["risk_score"].notna()].plot(**plot_kwargs)

    # Labels
    for _, row in gdf.iterrows():
        c = row.geometry.centroid
        label = row["MOH_N"].title()
        ax.annotate(
            label,
            xy=(c.x, c.y),
            ha="center",
            va="center",
            fontsize=label_fontsize(ax, row.geometry, label),
            color="#ffffff",
            clip_on=True,
        )

    formatted_date = datetime.date.fromisoformat(forecast_date).strftime(
        "%-d %B %Y"
    )
    ax.set_title(
        f"Sri Lanka — MOH Dengue Weather Risk\n"
        f"Forecast: {formatted_date}  ({horizon_label})",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.axis("off")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout(pad=0.5)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {output_path}")


def main():
    print("Loading weekly features from model results...")
    all_features = load_all_weekly_features()
    print(f"  Loaded {len(all_features)} regions")

    density = load_density()

    # Compute scores for current + both forecast horizons
    current_features = extract_forecast_features(all_features, 0)
    current_scores = composite_scores(current_features, density)

    all_horizon_scores = {}
    forecast_dates = {}
    for horizon_weeks in (2, 4):
        feats = extract_forecast_features(all_features, horizon_weeks)
        if feats:
            all_horizon_scores[horizon_weeks] = composite_scores(
                feats, density
            )
            forecast_dates[horizon_weeks] = next(iter(feats.values()))[
                "forecast_week"
            ]

    # Global colour scale: shared vmin/vmax across current + all forecast maps
    all_score_values = list(current_scores.values())
    for s in all_horizon_scores.values():
        all_score_values.extend(s.values())
    global_vmin = float(np.min(all_score_values))
    global_vmax = float(np.max(all_score_values))
    print(
        f"\nGlobal risk score range: [{global_vmin:.2f}, {global_vmax:.2f}]"
    )

    # Shared delta colour scale: symmetric, based on max absolute delta
    all_deltas = []
    for horizon_weeks, scores in all_horizon_scores.items():
        shared_rids = set(scores) & set(current_scores)
        all_deltas.extend(scores[r] - current_scores[r] for r in shared_rids)
    delta_vmax = float(np.max(np.abs(all_deltas))) if all_deltas else 1.0
    delta_vmax = max(delta_vmax, 0.1)
    print(f"Global delta range: [±{delta_vmax:.2f}]")

    # Re-render the current risk map with the shared colour scale
    print("\nRe-rendering current risk map with shared colour scale...")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from moh.MOH import MOH
    from moh.RiskMap import RiskMap

    moh_list = MOH.list()
    RiskMap.build(moh_list, vmin=global_vmin, vmax=global_vmax)

    # Render forecast maps and delta maps
    for horizon_weeks, label in [
        (2, "2-Week Forecast"),
        (4, "4-Week Forecast"),
    ]:
        print(f"\nGenerating {label}...")
        scores = all_horizon_scores.get(horizon_weeks)
        if not scores:
            print("  No data — skipping")
            continue

        forecast_date = forecast_dates[horizon_weeks]
        print(f"  Forecast week: {forecast_date}  ({len(scores)} regions)")

        output_path = os.path.join(
            "images", f"forecast_map_{horizon_weeks}w.png"
        )
        render_forecast_map(
            scores,
            forecast_date,
            label,
            output_path,
            vmin=global_vmin,
            vmax=global_vmax,
        )

        # Delta map
        shared_rids = set(scores) & set(current_scores)
        delta_scores = {
            rid: scores[rid] - current_scores[rid] for rid in shared_rids
        }
        delta_path = os.path.join(
            "images", f"forecast_delta_{horizon_weeks}w.png"
        )
        render_delta_map(
            delta_scores, forecast_date, label, delta_path, vmax=delta_vmax
        )


if __name__ == "__main__":
    main()
