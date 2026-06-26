import datetime
import os

from utils_future import Log

log = Log("ReadMe")

README_PATH = "README.md"
RISK_MAP_IMAGE = os.path.join("images", "risk_map.png")


class ReadMe:
    @staticmethod
    def _load_summary_rows(moh_list) -> list[dict]:
        from moh.RiskMap import RiskMap

        latest = RiskMap._load_latest_features()
        scores = RiskMap._composite_scores(latest)
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
    def _make_content(cls, today, n_regions, table_md) -> str:
        sections = [
            "# lk_dengue_weather_model",
            "",
            "Dengue outbreak weather-risk model for Sri Lanka MOH regions.",
            "See [README.methodology.md](README.methodology.md)"
            " for full methodology.",
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
            cls._data_sources_section(),
            "",
        ]
        return "\n".join(sections)

    @classmethod
    def build(cls, moh_list) -> None:
        today = datetime.date.today().strftime("%-d %B %Y")
        rows = cls._load_summary_rows(moh_list)
        table_md = cls._table_md(rows) if rows else "_No model results yet._"
        content = cls._make_content(today, len(rows), table_md)
        with open(README_PATH, "w") as f:
            f.write(content)
        log.info(f"Wrote {README_PATH}")


README_PATH = "README.md"
RISK_MAP_IMAGE = os.path.join("images", "risk_map.png")
DIR_MODEL_RESULTS = os.path.join("data", "model_results")


class ReadMe:
    @staticmethod
    def _load_summary_rows(moh_list) -> list[dict]:
        """Return one row per region that has a model result, sorted by
        descending composite risk score."""
        from moh.RiskMap import RiskMap

        latest = RiskMap._load_latest_features()
        scores = RiskMap._composite_scores(latest)

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
                    "week": feat.get("week", ""),
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
            "Rainfall mm (−10w) | Max Temp °C (−16w) | Min Temp °C (−13w) |\n"
            "|---|---|---:|---:|---:|---:|"
        )
        lines = [header]
        for r in rows[:n]:
            lines.append(
                f"| {
                    r['region']} | {
                    r['district']} | {
                    cls._fmt(
                        r['risk_score'],
                        2)} "
                f"| {cls._fmt(r['R_lag10'])} "
                f"| {cls._fmt(r['MT_lag16'])} "
                f"| {cls._fmt(r['mT_lag13'])} |"
            )
        return "\n".join(lines)

    @classmethod
    def build(cls, moh_list) -> None:
        today = datetime.date.today().strftime("%-d %B %Y")
        rows = cls._load_summary_rows(moh_list)
        n_regions = len(rows)

        table_md = cls._table_md(rows) if rows else "_No model results yet._"

        # Relative path from README to the image
        img_rel = RISK_MAP_IMAGE

        content = f"""# lk_dengue_weather_model

Dengue outbreak weather-risk model for Sri Lanka MOH regions.
See [README.methodology.md](README.methodology.md) for full methodology.

_Last updated: {today} · {n_regions} regions with model results._

---

## Risk Map

The choropleth below shows a composite weather-risk score for each MOH region,
derived from the three lagged meteorological predictors in the Erandi et al. (2021) GLM:
weekly rainfall (lag 10 weeks), mean maximum temperature (lag 16 weeks), and
mean minimum temperature (lag 13 weeks).
Higher scores (red) indicate conditions historically associated with higher dengue risk.

![Dengue Weather Risk Map]({img_rel})

---

## Top 20 High-Risk Regions

Sorted by composite weather-risk score (descending). Data as of the most recent
available prediction week.

{table_md}

> **Note:** Risk scores are weather-only (composite z-score of lagged meteorological
> predictors). Full GLM-based dengue incidence prediction requires historical
> case data (not yet integrated).

---

## Data Sources

- **Weather:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
  (ERA5 / ERA5-Land reanalysis, 0.1°–0.25° resolution)
- **Region boundaries:** Ministry of Health Sri Lanka (333 MOH regions)
- **Model:** Erandi, K.K.W.H., Perera, S.S.N. and Mahasinghe, A.C. (2021),
  *Int. J. Dynamical Systems and Differential Equations*, Vol. 11, Nos. 5/6, pp. 462–472.
"""

        with open(README_PATH, "w") as f:
            f.write(content)
        log.info(f"Wrote {README_PATH}")
