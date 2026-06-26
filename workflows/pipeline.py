from moh import MOH, ReadMe, RiskMap


def main():
    moh_list = MOH.list()
    for moh in moh_list:
        moh.build_all()
    RiskMap.build(moh_list)
    ReadMe.build(moh_list)


if __name__ == "__main__":
    main()
