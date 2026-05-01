# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.
from typing import Any, Dict

def analyze_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Performs forensic analysis on the provided structured metadata dictionary."""
    analysis = {}

    mapping = {
        "gps_present": _check_gps_presence,
        "editing_software_detected": _check_editing_software,
        "exif_missing": _check_exif_missing,
        "device_type": _check_device_type,
        "datetime_valid": _check_datetime_valid,
        "gps_accuracy": _check_gps_accuracy
    }

    for key, function in mapping.items():
        analysis[key] = function(metadata)

    return analysis


def _check_gps_presence(metadata: Dict[str, Any]) -> bool:
    """Checks if geolocation data is present in the metadata."""
    gps = metadata.get("gps", {})
    return "decimal_latitude" in gps and "decimal_longitude" in gps

def _check_editing_software(metadata: Dict[str, Any]) -> bool:
    """Detects signatures of known image editing software."""
    software = ""
    if "camera" in metadata and "software" in metadata["camera"]:
        software = metadata["camera"]["software"].lower()
    elif "image" in metadata and "software" in metadata["image"]:
        software = metadata["image"]["software"].lower()
    
    known_signatures = ["photoshop", "gimp", "lightroom", "canva", "snapseed", "affinity", "picsart", "adobe"]
    return any(signature in software for signature in known_signatures)

def _check_exif_missing(metadata: Dict[str, Any]) -> bool:
    """Returns True if no metadata was extracted."""
    return not bool(metadata)

def _check_datetime_valid(metadata: Dict[str, Any]) -> bool:
    """Checks if datetime information is present and valid."""
    dt = metadata.get("datetime", {})
    return bool(dt.get("datetimeoriginal") or dt.get("datetimedigitized"))
def _check_gps_accuracy(metadata: Dict[str, Any]) -> str:
    """Assesses GPS accuracy based on available data."""
    gps = metadata.get("gps", {})
    if "decimal_latitude" not in gps:
        return "no_gps"
    if "gpsdop" in gps:
        dop = float(gps["gpsdop"]) if gps["gpsdop"].replace(".", "").isdigit() else 10
        if dop < 2:
            return "high"
        elif dop < 5:
            return "medium"
        else:
            return "low"
    return "unknown"

def _check_device_type(metadata: Dict[str, Any]) -> str:
    """Determines the likely device type based on the camera make."""
    make = metadata.get("camera", {}).get("make", "").lower()
    if any(brand in make for brand in ["apple", "samsung", "huawei", "xiaomi", "google", "oneplus"]):
        return "phone"
    elif make:
        return "camera"
    else:
        return "unknown"