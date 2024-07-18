import re
import sys
from argparse import ArgumentParser
from pathlib import Path

import intake_esgf
from intake_esgf import ESGFCatalog
from intake_esgf.exceptions import NoSearchResults

parser = ArgumentParser(
    prog="get_ilamb_records",
    description="Print paths to data in the NERSC ESG data lake",
)
parser.add_argument("-s", "--source_id", required=True)
parser.add_argument("-e", "--experiment_id", default="historical")
args = parser.parse_args()

intake_esgf.conf.set(all_indices=True)
#    indices={"ornl-dev": False, "anl-dev": False, "esgf-node.llnl.gov": True}
#)
intake_esgf.conf.set(additional_df_cols=[])

search = {
    "experiment_id": args.experiment_id,
    "source_id": args.source_id,
    "frequency": "mon",
    "variable_id": [
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
        "netAtmosLandCO2Flux",
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
        "areacella",
        "sftlf",
    ],
}

cat = ESGFCatalog()
msr = True
try:
    cat.search(**search)
except NoSearchResults:
    msr = False
    search["project"] = "CMIP5"
    for cmip5, cmip6 in zip(
        ["experiment", "model", "time_frequency", "variable"],
        ["experiment_id", "source_id", "frequency", "variable_id"],
    ):
        search[cmip5] = search.pop(cmip6)
    cat.search(**search)
cat.remove_ensembles()
ds = cat.to_dataset_dict(add_measures=msr)
files = re.findall(r"accessed\s(.*)\n", cat.session_log())
files = list(set([Path(f).parent for f in files]))
files = "\n".join([f"    - {f}" for f in sorted(files,key=lambda f: str(f).split("/")[-3])])
print(
    f"""
{args.source_id}:
  modelname: {args.source_id}
  path: None
  paths:
{files}"""
)
