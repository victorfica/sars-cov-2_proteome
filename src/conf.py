from pathlib import Path
import pkg_resources


# Data folders
_DATA_DIR = Path(pkg_resources.resource_filename(__name__, "../data")).resolve()
DATA_PROCESSED = _DATA_DIR/'processed'
DATA_INTERIM = _DATA_DIR/'interim'
DATA_RAW = _DATA_DIR/'raw'

# Resources
protein_names = ["NSP1","NSP2","NSP3","NSP4","NSP5","NSP6","NSP7","NSP8","NSP9","NSP10","NSP11","NSP12",
                 "NSP13","NSP14","NSP15","NSP16","Spike","NS3","E","M","NS6","NS7a","NS7b","NS8","N"]

# reference seq
reference_seq = 'EPI_ISL_402124'