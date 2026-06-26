import datetime
import os
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
    population: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            region_id=data["region_id"],
            region_name=data["region_name"],
            district_id=data["district_id"],
            centroid_lat=data["centroid_lat"],
            centroid_lng=data["centroid_lng"],
            population=data["population"],
        )

    MOH_FILE = JSONFile(os.path.join("moh_data", "ent", "moh.json"))

    @classmethod
    @cache
    def list(cls):
        d_list = cls.MOH_FILE.read()
        log.debug(
            f"Loaded {len(d_list)} MOH regions from {cls.MOH_FILE.path}"
        )
        return [cls.from_dict(d) for d in d_list]

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
    def weather_history_file(self):
        return JSONFile(
            os.path.join(self.DIR_WEATHER_HISTORY, f"{self.region_id}.json")
        )

    def build_weather_history(self, force=False) -> dict:
        if self.weather_history_file.exists and not force:
            return self.weather_history_file.read()

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(
            weeks=self.WEATHER_HISTORY_WEEKS
        )
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
        response = requests.get(
            self.WEATHER_HISTORY_URL, params=params, timeout=60
        )
        response.raise_for_status()
        data = response.json()

        os.makedirs(self.DIR_WEATHER_HISTORY, exist_ok=True)
        self.weather_history_file.write(data)
        log.info(f"Wrote {self.weather_history_file}")
        return data

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
