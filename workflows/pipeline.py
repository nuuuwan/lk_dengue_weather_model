import os
import shutil

from moh import MOH, ReadMe, RiskMap
from utils_future import WWW, File, Log

log = Log("pipeline")


def load_data():
    shutil.rmtree("data", ignore_errors=True)
    os.makedirs("data", exist_ok=True)
    content = WWW(
        "https://raw.githubusercontent.com"
        + "/nuuuwan/lk_dengue/refs/heads/main"
        + "/data/NDCUWeekly/latest/custom_data/high_risk_moh_areas.tsv"
    ).read_static()

    File(os.path.join("data", "high_risk_moh_areas.tsv")).write(content)
    log.info("Loaded high_risk_moh_areas.tsv")


def main():
    load_data()
    moh_list = MOH.list()
    for moh in moh_list:
        moh.build_all()
    RiskMap.build(moh_list)
    ReadMe.build(moh_list)


if __name__ == "__main__":
    main()
