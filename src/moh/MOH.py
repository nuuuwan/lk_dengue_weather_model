import datetime
import os
import shutil
import time
from dataclasses import dataclass
from functools import cache

import numpy as np
import pandas as pd
import requests

from utils_future import JSONFile, Log

log = Log("MOH")


@dataclass
class MOH:
    region_id: str
    region_name: str
    district_id: str
    centroid_lat: float
    centroid_lng: float
    area_sqkm: float
    population: int
    population_density: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            region_id=data["region_id"],
            region_name=data["region_name"],
            district_id=data["district_id"],
            centroid_lat=data["centroid_lat"],
            centroid_lng=data["centroid_lng"],
            area_sqkm=data["area_sqkm"],
            population=data["population"],
            population_density=data["population_density"],
        )

    MOH_FILE = JSONFile(os.path.join("static_data", "ent", "moh.json"))

    DENSITY_WEIGHT = 0

    @classmethod
    @cache
    def list(cls):
        d_list = cls.MOH_FILE.read()
        log.debug(f"Loaded {len(d_list)} MOH regions from {cls.MOH_FILE.path}")
        return [cls.from_dict(d) for d in d_list]

    @classmethod
    @cache
    def idx(cls):
        return {m.region_id: m for m in cls.list()}

    @classmethod
    @cache
    def from_id(cls, region_id: str):
        return cls.idx().get(region_id)

    WEATHER_HISTORY_URL = "https://archive-api.open-meteo.com/v1/archive"
    WEATHER_HISTORY_DAILY_VARS = [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "rain_sum",
        "wind_speed_10m_max",
        "et0_fao_evapotranspiration",
    ]
    WEATHER_HISTORY_WEEKS = 52
    DIR_WEATHER_HISTORY = os.path.join("data", "weather_history")

    @property
    def weather_history_dir(self):
        return os.path.join(self.DIR_WEATHER_HISTORY, self.region_id)

    def _existing_daily_dates(self) -> set:
        """Return set of date strings (YYYY-MM-DD) for which per-day files exist."""
        d = self.weather_history_dir
        if not os.path.isdir(d):
            return set()
        return {
            f[:-5]
            for f in os.listdir(d)
            if f.endswith(".json") and len(f) == 15  # yyyy-mm-dd.json
        }

    def _fetch_and_store(
        self, start_date: datetime.date, end_date: datetime.date
    ):
        """Fetch weather for [start_date, end_date] and write one file per day."""
        params = {
            "latitude": self.centroid_lat,
            "longitude": self.centroid_lng,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": ",".join(self.WEATHER_HISTORY_DAILY_VARS),
            "timezone": "Asia/Colombo",
        }
        log.debug(
            f"Fetching weather history for {self.region_id}"
            f" ({start_date} → {end_date})"
        )
        max_retries = 5
        t_sleep = 5
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.WEATHER_HISTORY_URL, params=params, timeout=120
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt + 1 == max_retries:
                    log.error(
                        f"[{attempt + 1}/{max_retries}] {self.region_id}: {e}."
                        " Max retries reached. Aborting."
                    )
                    raise
                log.warning(
                    f"[{attempt + 1}/{max_retries}] {self.region_id}: {e}."
                    f" Retrying in {t_sleep}s..."
                )
                time.sleep(t_sleep)
                t_sleep *= 2
        daily = response.json()["daily"]
        os.makedirs(self.weather_history_dir, exist_ok=True)
        for i, date_str in enumerate(daily["time"]):
            day_data = {
                var: daily[var][i] for var in self.WEATHER_HISTORY_DAILY_VARS
            }
            JSONFile(
                os.path.join(self.weather_history_dir, f"{date_str}.json")
            ).write(day_data)
        log.info(
            f"Wrote {len(daily['time'])} daily files for {self.region_id}"
        )

    def _assemble_daily_data(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> dict:
        """Assemble per-day files into the dict format expected by _make_daily_df."""
        d = self.weather_history_dir
        times = []
        var_lists = {var: [] for var in self.WEATHER_HISTORY_DAILY_VARS}
        date = start_date
        while date <= end_date:
            date_str = date.isoformat()
            fp = os.path.join(d, f"{date_str}.json")
            if os.path.exists(fp):
                day = JSONFile(fp).read()
                times.append(date_str)
                for var in self.WEATHER_HISTORY_DAILY_VARS:
                    var_lists[var].append(day.get(var))
            date += datetime.timedelta(days=1)
        return {"daily": {"time": times, **var_lists}}

    def build_weather_history(self, force=False) -> dict:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(
            weeks=self.WEATHER_HISTORY_WEEKS
        )
        if force:
            if os.path.isdir(self.weather_history_dir):
                shutil.rmtree(self.weather_history_dir)
            self._fetch_and_store(start_date, end_date)
        else:
            existing = self._existing_daily_dates()
            if existing:
                latest_date = datetime.date.fromisoformat(max(existing))
                if latest_date < end_date:
                    fetch_start = latest_date + datetime.timedelta(days=1)
                    self._fetch_and_store(fetch_start, end_date)
            else:
                self._fetch_and_store(start_date, end_date)
        return self._assemble_daily_data(start_date, end_date)

    @property
    def model_result_file(self):
        return JSONFile(
            os.path.join("data", "model_results", f"{self.region_id}.json")
        )

    @staticmethod
    def _make_daily_df(daily: dict) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "rainfall": daily["precipitation_sum"],
                "max_temp": daily["temperature_2m_max"],
                "min_temp": daily["temperature_2m_min"],
            },
            index=pd.to_datetime(daily["time"]),
        )

    @staticmethod
    def _add_lags(df: pd.DataFrame) -> pd.DataFrame:
        weekly = df.resample("W-MON", label="left", closed="left").agg(
            {"rainfall": "sum", "max_temp": "mean", "min_temp": "mean"}
        )
        weekly["R_lag10"] = weekly["rainfall"].shift(10)
        weekly["MT_lag16"] = weekly["max_temp"].shift(16)
        weekly["mT_lag13"] = weekly["min_temp"].shift(13)
        return weekly.dropna(subset=["R_lag10", "MT_lag16", "mT_lag13"])

    @staticmethod
    def _weekly_records(weekly: pd.DataFrame) -> list:
        return [
            {
                "week": idx.strftime("%Y-%m-%d"),
                **{
                    k: (None if np.isnan(v) else round(float(v), 4))
                    for k, v in row.items()
                },
            }
            for idx, row in weekly.iterrows()
        ]

    def build_model_result(self, force=False) -> dict:
        if self.model_result_file.exists and not force:
            return self.model_result_file.read()

        raw = self.build_weather_history()
        weekly = self._add_lags(self._make_daily_df(raw["daily"]))
        result = {
            "region_id": self.region_id,
            "generated_date": datetime.date.today().isoformat(),
            "weekly_features": self._weekly_records(weekly),
        }
        os.makedirs(
            os.path.dirname(self.model_result_file.path), exist_ok=True
        )
        self.model_result_file.write(result)
        log.info(f"Wrote {self.model_result_file}")
        return result

    def build_all(self, force=False) -> dict:
        self.build_weather_history(force=force)
        return self.build_model_result(force=force)
