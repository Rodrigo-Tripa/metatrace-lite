# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

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
    
    # Expanded list of known editing software signatures
    known_signatures = [
        "photoshop", "gimp", "lightroom", "canva", "snapseed", 
        "affinity", "picsart", "adobe", "paint.net", "krita", 
        "inkscape", "darktable", "capture one", "luminar", "rawtherapee"
    ]
    return any(signature in software for signature in known_signatures)

def _check_exif_missing(metadata: Dict[str, Any]) -> bool:
    """Returns True if no metadata was extracted."""
    return not bool(metadata)

def _check_datetime_valid(metadata: Dict[str, Any]) -> bool:
    """Checks if datetime information is present and valid.
    
    FIXED: Corrected key names from 'datetimeoriginal' to 'datetime_original'
    to match the actual keys used in extractor.py
    """
    dt = metadata.get("datetime", {})
    return bool(dt.get("datetime_original") or dt.get("datetime_digitized"))

def _check_gps_accuracy(metadata: Dict[str, Any]) -> str:
    """Assesses GPS accuracy based on available data (Dilution of Precision).
    
    FIXED: Improved DOP parsing with proper exception handling instead of fragile
    .isdigit() check. Now handles scientific notation, spacing, and malformed values.
    """
    gps = metadata.get("gps", {})
    
    if "decimal_latitude" not in gps:
        return "no_gps"
    
    if "gpsdop" in gps:
        try:
            # Safe conversion: try to parse as float directly
            dop = float(gps["gpsdop"])
            
            # Validate DOP is positive (negative values indicate error)
            if dop < 0:
                logger.warning(f"Invalid GPS DOP value (negative): {dop}")
                return "unknown"
            
            # Classify accuracy by DOP value
            if dop < 2:
                return "high"
            elif dop < 5:
                return "medium"
            else:
                return "low"
        except (ValueError, TypeError) as e:
            logger.debug(f"Failed to parse GPS DOP value '{gps['gpsdop']}': {e}")
            return "unknown"
    
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
