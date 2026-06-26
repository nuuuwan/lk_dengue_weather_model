import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr

from moh.RiskMap import RiskMap
from utils_future import Log

log = Log("DensityModel")


class DensityModel:
    @staticmethod
    def optimal_density_params(moh_list) -> tuple[float, float]:
        """
        Returns (exponent, weight) maximising Spearman ρ between
        the composite risk score and actual cases/100k.

        Score = z(R_lag10) + z(MT_lag16) + z(mT_lag13)
                + weight * z(raw_density ** exponent)

        Raw density is taken directly from the MOH JSON (not the
        pre-transformed value stored on the MOH dataclass).
        """
        from moh.Correlation import Correlation
        from moh.MOH import MOH as MOHClass

        raw_data = {
            d["region_id"]: d["population_density"]
            for d in MOHClass.MOH_FILE.read()
        }

        latest = RiskMap._load_latest_features()
        weather_scores = RiskMap._composite_scores(latest, None, 0.0)
        actual_map = Correlation._load_actual()

        rids = list(weather_scores.keys())
        ws = np.array([weather_scores[r] for r in rids])
        actual = np.array([actual_map.get(r, 0.0) for r in rids])
        raw_d = np.array([raw_data.get(r, 0.0) for r in rids])

        def neg_rho(params):
            exp, w = params[0], params[1]
            d = np.power(np.maximum(raw_d, 1e-9), max(exp, 1e-9))
            std = d.std()
            d_z = (d - d.mean()) / std if std > 0 else np.zeros_like(d)
            rho, _ = spearmanr(ws + w * d_z, actual)
            return -float(rho) if np.isfinite(rho) else 0.0

        best, best_val = [0.25, 1.0], float("inf")
        for e in np.linspace(0.1, 2.0, 20):
            for w in [0, 0.5, 1, 2, 3, 5]:
                v = neg_rho([e, w])
                if v < best_val:
                    best_val, best = v, [e, w]

        result = minimize(
            neg_rho,
            x0=best,
            method="Nelder-Mead",
            options={"xatol": 0.005, "fatol": 1e-5, "maxiter": 1000},
        )
        e_opt, w_opt = result.x
        rho_opt = -neg_rho(result.x)
        log.info(
            f"Optimal: exponent={e_opt:.3f},"
            f" weight={w_opt:.3f}, rho={rho_opt:.4f}"
        )
        return round(float(e_opt), 3), round(float(w_opt), 3)
