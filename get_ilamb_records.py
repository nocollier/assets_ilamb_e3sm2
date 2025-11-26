from argparse import ArgumentParser
from pathlib import Path

from intake_esgf import ESGFCatalog

parser = ArgumentParser(
    prog="get_ilamb_records",
    description="Print paths to data in the NERSC ESG data lake",
)
parser.add_argument("-s", "--source_id", required=True)
parser.add_argument("-m", "--member_id", default="r1i1p1f1")
parser.add_argument("-e", "--experiment_id", default="historical")
args = parser.parse_args()


cat = ESGFCatalog().search(
    experiment_id=args.experiment_id,
    source_id=args.source_id,
    member_id=args.member_id,
    frequency=["mon", "fx"],
    variable_id=[
        "burntFractionAll",
        "cSoilAbove1m",
        "cSoil",
        "cVeg",
        "evspsbl",
        "fBNF",
        "gpp",
        "hfls",
        "hfss",
        "lai",
        "mrro",
        "mrsos",
        "nbp",
        "pr",
        "ra",
        "rh",
        "hurs",
        "rlds",
        "rlus",
        "rsds",
        "rsus",
        "snw",
        "tas",
        "tasmax",
        "tasmin",
        "tsl",
    ],
)
pd = cat.to_path_dict()

# cell measures
for v in ["areacella", "sftlf"]:
    try:
        tmp = ESGFCatalog().search(
            source_id=args.source_id,
            grid_label=list(cat.df.grid_label.unique()),
            variable_id=v,
        )
    except:
        continue
    tmp.df = tmp.df.iloc[slice(0, 1)]
    pd.update(tmp.to_path_dict())


files = [f"    - {str(Path(f).parent)}" for _, files in pd.items() for f in files]
files = sorted(list(set(files)))
files = "\n".join(files)
print(
    f"""
{args.source_id}:
  modelname: {args.source_id}
  path: None
  paths:
{files}"""
)
