PROJECTIONS = {
    "EQUIRECTANGULAR": "equirectangular",
    "MERCATOR": "mercator",
    "GALL_STEREOGRAPHIC": "gall-stereo",
}
STATUS_TYPES = {
    "ERROR": "error",
    "SUCCESS": "success",
    "WAIT": "wait",
}
PRINT_SIZES = {"A4": "a4", "US_LETTER": "us-letter"}

from .utils import format_output_filename
from .get_stripes import get_stripes
from .write_pdf import write_pdf
from .main import PaperGlobe
