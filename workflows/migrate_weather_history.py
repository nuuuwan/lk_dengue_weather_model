"""
Migrate weather history from the old single-file-per-region format:
  data/weather_history/<region_id>.json

to the new per-day format:
  data/weather_history/<region_id>/YYYY-MM-DD.json

Run once from the project root:
  python workflows/migrate_weather_history.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils_future import Log

log = Log("migrate_weather_history")

DIR_WEATHER_HISTORY = os.path.join("data", "weather_history")
DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "rain_sum",
    "wind_speed_10m_max",
    "et0_fao_evapotranspiration",
]


def migrate():
    if not os.path.isdir(DIR_WEATHER_HISTORY):
        log.info("No weather history directory found. Nothing to migrate.")
        return

    old_files = [
        f
        for f in os.listdir(DIR_WEATHER_HISTORY)
        if f.endswith(".json")
        and os.path.isfile(os.path.join(DIR_WEATHER_HISTORY, f))
    ]

    if not old_files:
        log.info("No legacy region files found. Nothing to migrate.")
        return

    log.info(f"Found {len(old_files)} region file(s) to migrate.")

    for fname in sorted(old_files):
        region_id = fname[:-5]  # strip .json
        old_path = os.path.join(DIR_WEATHER_HISTORY, fname)

        try:
            with open(old_path) as f:
                data = json.load(f)
        except Exception as e:
            log.warning(f"Skipping {fname}: {e}")
            continue

        daily = data.get("daily", {})
        times = daily.get("time", [])
        if not times:
            log.warning(f"No daily data in {fname}, skipping.")
            continue

        region_dir = os.path.join(DIR_WEATHER_HISTORY, region_id)
        os.makedirs(region_dir, exist_ok=True)

        written = 0
        for i, date_str in enumerate(times):
            day_path = os.path.join(region_dir, f"{date_str}.json")
            if os.path.exists(day_path):
                continue  # don't overwrite already-migrated days
            day_data = {
                var: (daily[var][i] if i < len(daily.get(var, [])) else None)
                for var in DAILY_VARS
            }
            with open(day_path, "w") as f:
                json.dump(day_data, f)
            written += 1

        log.info(f"Migrated {region_id}: {written} day(s) → {region_dir}/")
        os.remove(old_path)
        log.info(f"Removed old file: {old_path}")

    log.info("Migration complete.")


if __name__ == "__main__":
    migrate()
