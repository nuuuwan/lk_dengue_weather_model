import datetime
import json
import os

from utils_future import Log

log = Log("ReadMe")

README_PATH = "README.md"
RISK_MAP_IMAGE = os.path.join("images", "risk_map.png")


class ReadMe:
    @staticmethod
    def _load_summary_rows(moh_list) -> list[dict]:
        from moh.MOH import MOH
        from moh.RiskMap import RiskMap

        latest = RiskMap._load_latest_features()
        density = (
            {m.region_id: m.population_density for m in moh_list}
            if MOH.DENSITY_WEIGHT
            else None
        )
        scores = RiskMap._composite_scores(latest, density, MOH.DENSITY_WEIGHT)
        name_map = {m.region_id: m for m in moh_list}
        rows = []
        for rid, score in scores.items():
            moh = name_map.get(rid)
            feat = latest[rid]
            rows.append(
                {
                    "region": moh.region_name if moh else rid,
                    "district": moh.district_id if moh else "",
                    "risk_score": round(score, 2),
                    "R_lag10": feat.get("R_lag10"),
                    "MT_lag16": feat.get("MT_lag16"),
                    "mT_lag13": feat.get("mT_lag13"),
                }
            )
        rows.sort(key=lambda r: r["risk_score"], reverse=True)
        return rows

    @staticmethod
    def _fmt(val, decimals=1):
        if val is None:
            return "—"
        return f"{val:.{decimals}f}"

    @classmethod
    def _table_md(cls, rows: list[dict], n: int = 20) -> str:
        header = (
            "| Region | District | Risk Score | "
            "Rainfall mm (−10w) | Max Temp °C (−16w)"
            " | Min Temp °C (−13w) |\n"
            "|---|---|---:|---:|---:|---:|"
        )
        lines = [header]
        for r in rows[:n]:
            cols = [
                r["region"],
                r["district"],
                cls._fmt(r["risk_score"], 2),
                cls._fmt(r["R_lag10"]),
                cls._fmt(r["MT_lag16"]),
                cls._fmt(r["mT_lag13"]),
            ]
            lines.append("| " + " | ".join(cols) + " |")
        return "\n".join(lines)

    @classmethod
    def _risk_map_section(cls) -> str:
        desc = (
            "The choropleth below shows a composite weather-risk score"
            " for each MOH\nregion, derived from the three lagged"
            " predictors in Erandi et al. (2021):\nweekly rainfall"
            " (lag 10 w), mean max temperature (lag 16 w), and mean\n"
            "min temperature (lag 13 w). Higher scores (red) indicate"
            " conditions\nassociated with higher dengue risk."
        )
        return "\n".join(
            [
                "## Risk Map",
                "",
                desc,
                "",
                f"![Dengue Weather Risk Map]({RISK_MAP_IMAGE})",
            ]
        )

    @classmethod
    def _table_section(cls, table_md) -> str:
        note = (
            "> **Note:** Risk scores are weather-only"
            " (composite z-score of lagged\n"
            "> meteorological predictors). Full GLM-based dengue\n"
            "> incidence prediction requires historical case data"
            " (not yet integrated)."
        )
        return "\n".join(
            [
                "## Top 20 High-Risk Regions",
                "",
                "Sorted by composite weather-risk score (descending).",
                "",
                table_md,
                "",
                note,
            ]
        )

    @classmethod
    def _correlation_section(cls, stats) -> str:
        img = os.path.join("images", "correlation.png")
        if not stats:
            return "\n".join(
                [
                    "## Model Validation",
                    "",
                    "_No case data available for correlation._",
                ]
            )
        r = stats["pearson_r"]
        rho = stats["spearman_rho"]
        p = stats["pearson_p"]
        n = stats["n"]
        p_str = f"{p:.3f}" if p >= 0.001 else "< 0.001"
        table = (
            "| Metric | Value |\n"
            "|---|---:|\n"
            f"| Pearson *r* | {r} |\n"
            f"| Spearman \u03c1 | {rho} |\n"
            f"| *p*-value (Pearson) | {p_str} |\n"
            f"| Regions (*n*) | {n} |"
        )
        return "\n".join(
            [
                "## Model Validation",
                "",
                "Composite weather-risk score vs reported cases/100k"
                f" ({n} regions with available case data).",
                "",
                table,
                "",
                f"![Predicted vs Actual Cases]({img})",
                "",
                "![Confusion Matrix](images/confusion_matrix.png)",
                "",
                "![Confusion Map](images/confusion_map.png)",
                "",
                cls._fp_fn_md(stats),
            ]
        )

    @staticmethod
    def _fp_fn_md(stats) -> str:
        def _tbl(rows, title):
            hdr = (
                f"### {title}\n\n"
                "| Region | District | Risk Score | Cases/100k |\n"
                "|---|---|---:|---:|"
            )
            lines = [hdr]
            for p in rows:
                lines.append(
                    f"| {p['region']} | {p['district']}"
                    f" | {p['score']:.2f} | {p['actual']:.1f} |"
                )
            return "\n".join(lines)

        fp_md = _tbl(
            stats.get("top_fp", []),
            "Top 10 False Positives"
            " (high predicted risk, low actual cases)",
        )
        fn_md = _tbl(
            stats.get("top_fn", []),
            "Top 10 False Negatives"
            " (low predicted risk, high actual cases)",
        )
        return fp_md + "\n\n" + fn_md

    @classmethod
    def _precision_curve_section(cls, stats) -> str:
        if not stats:
            return ""
        cutoff = stats.get("cutoff", 20)
        return "\n".join(
            [
                "## Score Threshold Analysis",
                "",
                f"Proportion of MOH regions with \u2265 {cutoff} actual"
                " cases/100k among all regions with predicted risk"
                " score above a given threshold.",
                "",
                "![Score Threshold vs High-Risk Proportion]"
                "(images/precision_curve.png)",
                "",
                f"False positive rate (FPR) and false negative rate (FNR)"
                f" for classifying regions as high-risk"
                f" (\u2265 {cutoff} cases/100k) at each threshold.",
                "",
                "![FPR and FNR vs Threshold](images/fpr_fnr_curve.png)",
                "",
                "ROC curve with AUC = " f"{stats.get('auc', '—')}.",
                "",
                "![ROC Curve](images/roc_curve.png)",
            ]
        )

    @staticmethod
    def _latest_data_week() -> datetime.date | None:
        """Return the most recent week date found across all model results."""
        results_dir = os.path.join("data", "model_results")
        latest = None
        if not os.path.isdir(results_dir):
            return None
        for fname in os.listdir(results_dir):
            if not fname.endswith(".json"):
                continue
            data = json.load(open(os.path.join(results_dir, fname)))
            features = data.get("weekly_features") or []
            if features:
                week = datetime.date.fromisoformat(features[-1]["week"])
                if latest is None or week > latest:
                    latest = week
        return latest

    @classmethod
    def _forecast_section(cls) -> str:
        latest = cls._latest_data_week()
        if latest:
            date_2w = (latest + datetime.timedelta(weeks=2)).strftime(
                "%-d %B %Y"
            )
            date_4w = (latest + datetime.timedelta(weeks=4)).strftime(
                "%-d %B %Y"
            )
        else:
            date_2w = "2 weeks ahead"
            date_4w = "4 weeks ahead"
        return "\n".join(
            [
                "## Forward-Looking Forecasts",
                "",
                "Dengue weather-risk scores projected 2 and 4 weeks ahead,"
                " using the same lagged meteorological predictors applied"
                " to already-recorded historical weather.  All three maps"
                " (current + forecasts) share an identical colour scale so"
                " regional risk levels are directly comparable.",
                "",
                f"### 2-Week Forecast ({date_2w})",
                "",
                "![2-Week Forecast Risk Map](images/forecast_map_2w.png)",
                "",
                f"### 4-Week Forecast ({date_4w})",
                "",
                "![4-Week Forecast Risk Map](images/forecast_map_4w.png)",
                "",
                "### Change from Current \u2014 2-Week Delta",
                "",
                "Blue regions show a projected **decrease** in risk;"
                " red regions show a projected **increase**.",
                "",
                "![2-Week Delta Map](images/forecast_delta_2w.png)",
                "",
                "### Change from Current \u2014 4-Week Delta",
                "",
                "![4-Week Delta Map](images/forecast_delta_4w.png)",
            ]
        )

    @classmethod
    def _data_sources_section(cls) -> str:
        api_url = "https://open-meteo.com/en/docs/historical-weather-api"
        ref = (
            "Erandi et al. (2021), "
            "*Int. J. Dynamical Systems and Differential Equations*,"
            " Vol. 11, Nos. 5/6, pp. 462–472."
        )
        return "\n".join(
            [
                "## Data Sources",
                "",
                "- **Weather:** [Open-Meteo Historical Weather API]"
                f"({api_url})",
                "  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)",
                "- **Region boundaries:** Ministry of Health Sri Lanka"
                " (333 MOH regions)",
                f"- **Model:** {ref}",
            ]
        )

    @classmethod
    def _make_content(cls, today, n_regions, table_md, stats) -> str:
        sections = [
            "# lk_dengue_weather_model",
            "",
            "Dengue outbreak weather-risk model for Sri Lanka MOH regions.",
            "",
            "> \U0001f4d6 **Methodology:**"
            " [README.methodology.md](README.methodology.md)",
            "",
            f"_Last updated: {today} ·"
            f" {n_regions} regions with model results._",
            "",
            "---",
            "",
            cls._risk_map_section(),
            "",
            "---",
            "",
            cls._table_section(table_md),
            "",
            "---",
            "",
            cls._correlation_section(stats),
            "",
            "---",
            "",
            cls._precision_curve_section(stats),
            "",
            "---",
            "",
            cls._forecast_section(),
            "",
            "---",
            "",
            cls._data_sources_section(),
            "",
        ]
        return "\n".join(sections)

    @classmethod
    def build(cls, moh_list) -> None:
        from moh.Correlation import Correlation

        today = datetime.date.today().strftime("%-d %B %Y")
        rows = cls._load_summary_rows(moh_list)
        stats = Correlation.build(moh_list)
        table_md = cls._table_md(rows) if rows else "_No model results yet._"
        content = cls._make_content(today, len(rows), table_md, stats)
        with open(README_PATH, "w") as f:
            f.write(content)
        log.info(f"Wrote {README_PATH}")
