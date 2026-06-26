import datetime
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import topojson as tp

from utils_future import Log

log = Log("RiskMap")


class RiskMap:
    TOPOJSON_PATH = os.path.join("moh_data", "geo", "moh.topojson")
    OUTPUT_PATH = os.path.join("images", "risk_map.png")
    DIR_MODEL_RESULTS = os.path.join("data", "model_results")

    @classmethod
    def _load_latest_features(cls) -> dict:
        result = {}
        if not os.path.isdir(cls.DIR_MODEL_RESULTS):
            return result
        for fname in os.listdir(cls.DIR_MODEL_RESULTS):
            if not fname.endswith(".json"):
                continue
            data = json.load(open(os.path.join(cls.DIR_MODEL_RESULTS, fname)))
            features = data.get("weekly_features") or []
            if features:
                result[data["region_id"]] = features[-1]
        return result

    @staticmethod
    def _zscore(arr: np.ndarray) -> np.ndarray:
        std = arr.std()
        return (arr - arr.mean()) / std if std > 0 else np.zeros_like(arr)

    @classmethod
    def _composite_scores(cls, latest: dict) -> dict:
        if not latest:
            return {}
        rids = list(latest.keys())
        vals = {
            k: np.array([float(latest[r].get(k) or 0.0) for r in rids])
            for k in ("R_lag10", "MT_lag16", "mT_lag13")
        }
        composite = sum(cls._zscore(v) for v in vals.values())
        return dict(zip(rids, composite.tolist()))

    @classmethod
    def _build_gdf(cls, moh_list, scores):
        name_to_score = {
            moh.region_name.upper(): scores[moh.region_id]
            for moh in moh_list
            if moh.region_id in scores
        }
        with open(cls.TOPOJSON_PATH) as f:
            gdf = tp.Topology(json.load(f)).to_gdf()
        gdf["risk_score"] = gdf["MOH_N"].map(name_to_score)
        return gdf

    @classmethod
    def _add_labels(cls, ax, gdf):
        for _, row in gdf.iterrows():
            c = row.geometry.centroid
            ax.annotate(
                row["MOH_N"].title(),
                xy=(c.x, c.y),
                ha="center",
                va="center",
                fontsize=4,
                color="#111111",
                clip_on=True,
            )

    @classmethod
    def _render_map(cls, gdf):
        fig, ax = plt.subplots(figsize=(10, 14))
        fig.patch.set_facecolor("#f8f8f8")
        ax.set_facecolor("#cce6ff")
        gdf[gdf["risk_score"].isna()].plot(
            ax=ax, color="#d0d0d0", edgecolor="white", linewidth=0.3
        )
        if gdf["risk_score"].notna().any():
            gdf[gdf["risk_score"].notna()].plot(
                ax=ax,
                column="risk_score",
                cmap="RdYlGn_r",
                edgecolor="white",
                linewidth=0.3,
                legend=True,
                legend_kwds={
                    "label": "Weather Risk Score (composite z-score)",
                    "shrink": 0.55,
                    "orientation": "vertical",
                },
            )
        cls._add_labels(ax, gdf)
        today = datetime.date.today().strftime("%-d %B %Y")
        ax.set_title(
            f"Sri Lanka — MOH Dengue Weather Risk\n{today}",
            fontsize=15,
            fontweight="bold",
            pad=14,
        )
        ax.axis("off")

    @classmethod
    def build(cls, moh_list) -> str:
        latest = cls._load_latest_features()
        scores = cls._composite_scores(latest)
        gdf = cls._build_gdf(moh_list, scores)
        cls._render_map(gdf)
        os.makedirs(os.path.dirname(cls.OUTPUT_PATH), exist_ok=True)
        plt.tight_layout(pad=0.5)
        plt.savefig(cls.OUTPUT_PATH, dpi=150, bbox_inches="tight")
        plt.close()
        log.info(f"Saved {cls.OUTPUT_PATH}")
        return cls.OUTPUT_PATH
