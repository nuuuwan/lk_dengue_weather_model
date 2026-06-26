import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from moh.RiskMap import RiskMap
from utils_future import Log

log = Log("Correlation")


class Correlation:
    TSV_PATH = os.path.join("data", "high_risk_moh_areas.tsv")
    OUTPUT_PATH = os.path.join("images", "correlation.png")
    CONFUSION_PATH = os.path.join("images", "confusion_matrix.png")
    PRECISION_PATH = os.path.join("images", "precision_curve.png")
    FPR_FNR_PATH = os.path.join("images", "fpr_fnr_curve.png")
    ROC_PATH = os.path.join("images", "roc_curve.png")
    DISTRICTS_TSV = os.path.join("data", "districts.tsv")

    PRECISION_CUTOFF = 5

    @classmethod
    def _load_actual(cls) -> dict:
        if not os.path.isfile(cls.TSV_PATH):
            return {}
        df = pd.read_csv(cls.TSV_PATH, sep="\t")
        return dict(zip(df["moh_id"], df["n_cases_this_week_per_100k"]))

    @classmethod
    def _build_pairs(cls, moh_list) -> list[dict]:

        actual = cls._load_actual()
        latest = RiskMap._load_latest_features()
        scores = RiskMap._composite_scores(latest)
        name_map = {m.region_id: m.region_name for m in moh_list}
        dist_map = {m.region_id: m.district_id for m in moh_list}
        dist_names = cls._load_district_names()
        pairs = [
            {
                "region_id": rid,
                "region": name_map.get(rid, rid),
                "district_id": dist_map.get(rid, ""),
                "district": dist_names.get(dist_map.get(rid, ""), ""),
                "score": score,
                "actual": actual.get(rid, 0.0),
            }
            for rid, score in scores.items()
        ]
        return pairs

    @classmethod
    def _compute_stats(cls, pairs) -> dict:
        xs = np.array([p["score"] for p in pairs])
        ys = np.array([p["actual"] for p in pairs])
        r, p_r = pearsonr(xs, ys)
        rho, p_rho = spearmanr(xs, ys)
        return {
            "n": len(pairs),
            "pearson_r": round(float(r), 4),
            "pearson_p": round(float(p_r), 4),
            "spearman_rho": round(float(rho), 4),
            "spearman_p": round(float(p_rho), 4),
        }

    @staticmethod
    def _precision_values(pairs, thresholds, cutoff):
        precision, n_above = [], []
        for t in thresholds:
            above = [p for p in pairs if p["score"] > t]
            n_above.append(len(above))
            if above:
                n_hi = sum(1 for p in above if p["actual"] >= cutoff)
                precision.append(n_hi / len(above))
            else:
                precision.append(float("nan"))
        return precision, n_above

    @classmethod
    def _plot_precision_curve(cls, pairs, cutoff) -> str:
        scores = np.array([p["score"] for p in pairs])
        thresholds = np.linspace(scores.min(), scores.max(), 200)
        precision, n_above = cls._precision_values(pairs, thresholds, cutoff)
        total = len(pairs)
        prop_above = [n / total for n in n_above]
        base = sum(1 for p in pairs if p["actual"] >= cutoff) / total
        fig, ax1 = plt.subplots(figsize=(9, 5))
        ax1.plot(
            thresholds,
            precision,
            color="steelblue",
            linewidth=2,
            label=f"Precision (\u2265 {cutoff} cases/100k)",
        )
        ax1.axhline(
            base,
            color="gray",
            linestyle="--",
            linewidth=1,
            label=f"Base rate ({base:.1%})",
        )
        ax1.set_xlabel("Predicted Risk Score Threshold")
        ax1.set_ylabel(
            f"Proportion with \u2265 {cutoff} cases/100k", color="steelblue"
        )
        ax1.tick_params(axis="y", labelcolor="steelblue")
        ax1.set_ylim(0, 1)
        ax2 = ax1.twinx()
        ax2.plot(
            thresholds,
            prop_above,
            color="coral",
            linewidth=1.5,
            linestyle=":",
            label="Proportion above threshold",
        )
        ax2.set_ylabel("Proportion above threshold", color="coral")
        ax2.set_ylim(0, 1)
        ax2.tick_params(axis="y", labelcolor="coral")
        l1, lb1 = ax1.get_legend_handles_labels()
        l2, lb2 = ax2.get_legend_handles_labels()
        ax1.legend(l1 + l2, lb1 + lb2, fontsize=8, loc="upper right")
        ax1.set_title(
            f"Score Threshold vs % Regions with \u2265 {cutoff} Cases/100k",
            fontsize=11,
        )
        ax1.grid(True, alpha=0.3)
        os.makedirs(os.path.dirname(cls.PRECISION_PATH), exist_ok=True)
        plt.tight_layout()
        plt.savefig(cls.PRECISION_PATH, dpi=150, bbox_inches="tight")
        plt.close()
        return cls.PRECISION_PATH

    @staticmethod
    def _fpr_fnr_values(pairs, thresholds, cutoff):
        positives = [p for p in pairs if p["actual"] >= cutoff]
        negatives = [p for p in pairs if p["actual"] < cutoff]
        n_pos, n_neg = len(positives), len(negatives)
        fpr_list, fnr_list = [], []
        for t in thresholds:
            tp = sum(1 for p in positives if p["score"] > t)
            fp = sum(1 for p in negatives if p["score"] > t)
            fpr_list.append(fp / n_neg if n_neg else float("nan"))
            fnr_list.append((n_pos - tp) / n_pos if n_pos else float("nan"))
        return fpr_list, fnr_list

    @classmethod
    def _plot_fpr_fnr(cls, pairs) -> str:
        scores = np.array([p["score"] for p in pairs])
        thresholds = np.linspace(scores.min(), scores.max(), 200)
        fpr, fnr = cls._fpr_fnr_values(
            pairs, thresholds, cls.PRECISION_CUTOFF
        )
        fpr_arr, fnr_arr = np.array(fpr), np.array(fnr)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(
            thresholds,
            fpr_arr,
            color="crimson",
            linewidth=2,
            label="FPR",
        )
        ax.plot(
            thresholds,
            fnr_arr,
            color="steelblue",
            linewidth=2,
            label="FNR",
        )
        idx = int(np.nanargmin(np.abs(fpr_arr - fnr_arr)))
        ax.axvline(
            thresholds[idx],
            color="gray",
            linestyle="--",
            linewidth=1,
            label=f"Crossover (t\u2248{thresholds[idx]:.2f})",
        )
        ax.set_xlabel("Predicted Risk Score Threshold")
        ax.set_ylabel("Rate")
        ax.set_ylim(0, 1)
        ax.set_title(
            f"FPR & FNR vs Threshold"
            f" (cutoff = {cls.PRECISION_CUTOFF} cases/100k)",
            fontsize=11,
        )
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        os.makedirs(os.path.dirname(cls.FPR_FNR_PATH), exist_ok=True)
        plt.tight_layout()
        plt.savefig(cls.FPR_FNR_PATH, dpi=150, bbox_inches="tight")
        plt.close()
        return cls.FPR_FNR_PATH

    @classmethod
    def _plot_roc(cls, pairs) -> float:
        scores = np.array([p["score"] for p in pairs])
        thresholds = np.concatenate(
            [
                [scores.min() - 1],
                np.linspace(scores.min(), scores.max(), 200),
                [scores.max() + 1],
            ]
        )
        fpr, fnr = cls._fpr_fnr_values(
            pairs, thresholds, cls.PRECISION_CUTOFF
        )
        tpr = [1.0 - f for f in fnr]
        pts = sorted(zip(fpr, tpr))
        fpr_s = np.array([x for x, _ in pts])
        tpr_s = np.array([y for _, y in pts])
        auc = float(np.trapezoid(tpr_s, fpr_s))
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(
            fpr_s,
            tpr_s,
            color="steelblue",
            linewidth=2,
            label=f"ROC (AUC\u202f=\u202f{auc:.3f})",
        )
        ax.plot(
            [0, 1],
            [0, 1],
            color="gray",
            linestyle="--",
            linewidth=1,
            label="Random",
        )
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(
            f"ROC Curve (cutoff = {cls.PRECISION_CUTOFF} cases/100k)",
            fontsize=11,
        )
        ax.legend(fontsize=9)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        os.makedirs(os.path.dirname(cls.ROC_PATH), exist_ok=True)
        plt.tight_layout()
        plt.savefig(cls.ROC_PATH, dpi=150, bbox_inches="tight")
        plt.close()
        return auc

    @classmethod
    def _classify_pairs(cls, pairs) -> dict:
        scores = np.array([p["score"] for p in pairs])
        actuals = np.array([p["actual"] for p in pairs])
        s_med = float(np.median(scores))
        a_med = float(np.median(actuals))

        def zn(arr):
            s = arr.std()
            return (arr - arr.mean()) / s if s else np.zeros_like(arr)

        zs, za = zn(scores), zn(actuals)
        buckets: dict = {"TP": [], "FP": [], "FN": [], "TN": []}
        for i, p in enumerate(pairs):
            hi_s = scores[i] >= s_med
            hi_a = actuals[i] > a_med  # strict: zeros stay "low actual"
            key = (
                ("TP" if hi_s else "FN") if hi_a else ("FP" if hi_s else "TN")
            )
            buckets[key].append({**p, "zdiff": float(zs[i] - za[i])})
        return buckets

    @classmethod
    def _plot_confusion(cls, buckets, top_fp, top_fn) -> str:
        cm = np.array(
            [
                [len(buckets["FN"]), len(buckets["TP"])],
                [len(buckets["TN"]), len(buckets["FP"])],
            ]
        )
        fig, ax = plt.subplots(figsize=(6, 7))
        im = ax.imshow(cm, cmap="Blues")
        cell_labels = [["FN", "TP"], ["TN", "FP"]]
        names_map = {(0, 0): top_fn, (1, 1): top_fp}
        for i in range(2):
            for j in range(2):
                offset = -0.18 if (i, j) in names_map else 0
                ax.text(
                    j,
                    i + offset,
                    f"{cell_labels[i][j]}\n{cm[i, j]}",
                    ha="center",
                    va="center",
                    fontsize=14,
                    fontweight="bold",
                )
        for (i, j), items in names_map.items():
            names = "\n".join(p["region"] for p in items)
            ax.text(
                j,
                i + 0.27,
                names,
                ha="center",
                va="center",
                fontsize=4,
                color="#222222",
                family="monospace",
            )
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Predicted Low", "Predicted High"], fontsize=9)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Actual High", "Actual Low"], fontsize=9)
        ax.set_title("Confusion Matrix (median threshold)", fontsize=11)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        os.makedirs(os.path.dirname(cls.CONFUSION_PATH), exist_ok=True)
        plt.tight_layout()
        plt.savefig(cls.CONFUSION_PATH, dpi=150, bbox_inches="tight")
        plt.close()
        return cls.CONFUSION_PATH

    @classmethod
    def _load_district_names(cls) -> dict:
        if not os.path.isfile(cls.DISTRICTS_TSV):
            return {}
        df = pd.read_csv(cls.DISTRICTS_TSV, sep="\t")
        return dict(zip(df["id"], df["name"]))

    @classmethod
    def _scatter_by_district(cls, ax, pairs):
        dist_names = cls._load_district_names()
        districts = sorted({p["district_id"] for p in pairs})
        cmap = plt.cm.get_cmap("nipy_spectral", len(districts))
        color_map = {d: cmap(i) for i, d in enumerate(districts)}
        for dist in districts:
            pts = [p for p in pairs if p["district_id"] == dist]
            label = dist_names.get(dist, dist)
            ax.scatter(
                [pt["score"] for pt in pts],
                [pt["actual"] for pt in pts],
                color=color_map[dist],
                alpha=0.7,
                s=50,
                label=label,
                zorder=3,
            )

    @staticmethod
    def _annotate_top(ax, pairs, n=5):
        for pt in pairs:
            ax.annotate(
                pt["region"],
                (pt["score"], pt["actual"]),
                fontsize=3,
                ha="left",
                xytext=(2, 2),
                textcoords="offset points",
                color="#444444",
            )

    @classmethod
    def _plot(cls, pairs, stats) -> str:
        xs = np.array([p["score"] for p in pairs])
        ys = np.array([p["actual"] for p in pairs])
        fig, ax = plt.subplots(figsize=(12, 7))
        cls._scatter_by_district(ax, pairs)
        m, b = np.polyfit(xs, ys, 1)
        xl = np.linspace(xs.min(), xs.max(), 100)
        ax.plot(xl, m * xl + b, color="crimson", linewidth=1.5, zorder=2)
        r = stats["pearson_r"]
        p = stats["pearson_p"]
        rho = stats["spearman_rho"]
        p_str = f"{p:.3f}" if p >= 0.001 else "< 0.001"
        ax.set_title(
            f"Predicted Risk vs Actual Cases/100k\n"
            f"Pearson r={r:.3f} (p={p_str}),"
            f" Spearman rho={rho:.3f}, n={stats['n']}",
            fontsize=11,
        )
        ax.set_xlabel("Composite Weather-Risk Score (predicted)")
        ax.set_ylabel("Cases per 100k this week (actual)")
        ax.grid(True, alpha=0.3)
        ax.legend(
            fontsize=6,
            ncol=2,
            loc="upper left",
            title="District",
            title_fontsize=7,
        )
        cls._annotate_top(ax, pairs)
        os.makedirs(os.path.dirname(cls.OUTPUT_PATH), exist_ok=True)
        plt.tight_layout()
        plt.savefig(cls.OUTPUT_PATH, dpi=600, bbox_inches="tight")
        plt.close()
        return cls.OUTPUT_PATH

    @classmethod
    def build(cls, moh_list) -> dict:
        pairs = cls._build_pairs(moh_list)
        if len(pairs) < 3:
            log.info("Insufficient overlap for correlation")
            return {}
        stats = cls._compute_stats(pairs)
        cls._plot(pairs, stats)
        cls._plot_precision_curve(pairs, cutoff=cls.PRECISION_CUTOFF)
        cls._plot_fpr_fnr(pairs)
        auc = cls._plot_roc(pairs)
        buckets = cls._classify_pairs(pairs)
        top_fp = sorted(
            buckets["FP"], key=lambda p: p["score"], reverse=True
        )[:10]
        top_fn = sorted(
            buckets["FN"], key=lambda p: p["actual"], reverse=True
        )[:10]
        cls._plot_confusion(buckets, top_fp, top_fn)
        log.info(
            f"Correlation: r={stats['pearson_r']},"
            f" rho={stats['spearman_rho']}, n={stats['n']}"
        )
        return {
            **stats,
            "top_fp": top_fp,
            "top_fn": top_fn,
            "cutoff": cls.PRECISION_CUTOFF,
            "auc": round(auc, 4),
        }
