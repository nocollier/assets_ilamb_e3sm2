from intake_esgf import ESGFCatalog
import sys
import re
from pathlib import Path
from intake_esgf.exceptions import NoSearchResults
import intake_esgf

intake_esgf.conf.set(indices={'ornl-dev':False,'anl-dev':False,'esgf-node.llnl.gov':True})

if len(sys.argv) != 2:
    print(f"Usage: python {__file__.split('/')[-1]} source_id")
    sys.exit(1)

search = {
    "experiment_id": "historical",
    "source_id": sys.argv[1],
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
    search['project'] = 'CMIP5'
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
files = "\n".join([f"    - {f}" for f in sorted(files)])
print(
    f"""
{sys.argv[1]}:
  modelname: {sys.argv[1]}
  path: None
  paths:
{files}"""
)
