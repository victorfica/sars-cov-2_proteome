from pathlib import Path
import pkg_resources


# Data folders
_DATA_DIR = Path(pkg_resources.resource_filename(__name__, "../data")).resolve()
DATA_PROCESSED = _DATA_DIR/'processed'
DATA_INTERIM = _DATA_DIR/'interim'
DATA_RAW = _DATA_DIR/'raw'

# Resources
protein_names = ["NSP1","NSP2","NSP3","NSP4","NSP5","NSP6","NSP7","NSP8","NSP9","NSP10","NSP11","NSP12",
                 "NSP13","NSP14","NSP15","NSP16","Spike","NS3","E","M","NS6","NS7a","NS7b","NS8","N", "NS9b", "NS9c"]

prot_len = {"NSP1":180, "NSP2":638, "NSP3":1945, "NSP4":500,
            "NSP5":306, "NSP6":290, "NSP7":83, "NSP8":198,
            "NSP9":113, "NSP10":139, "NSP11":13, "NSP12":932,
            "NSP13":601, "NSP14":527, "NSP15":346, "NSP16":298,
            "Spike":1273, "NS3":275, "E":75, "M":222, "NS6":61,
            "NS7a":121, "NS7b":43, "NS8":121, "N":419}

# reference seq
reference_seq = 'EPI_ISL_402124'