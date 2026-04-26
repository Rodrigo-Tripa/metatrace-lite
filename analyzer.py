# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.
from typing import Any, Dict

def analyze_metadata(metadata: Dict[str, str]) -> Dict[str, Any]:
    """Performs forensic analysis on the provided metadata dictionary."""
    analysis = {}

    mapping = {
        "gps_present": _check_gps_presence,
        "editing_software_detected": _check_editing_software,
        "exif_missing": _check_exif_missing
    }

    for key, function in mapping.items():
        analysis[key] = function(metadata)

    return analysis


def _check_gps_presence(metadata: Dict[str, str]) -> bool:
    """Checks if geolocation tags are present in the metadata."""
    return "GPS GPSLatitude" in metadata and "GPS GPSLongitude" in metadata

def _check_editing_software(metadata: Dict[str, str]) -> bool:
    """Detects signatures of known image editing software (case-insensitive)."""
    # Normalize the tag value to lowercase for robust matching
    software_tag = metadata.get("Image Software", "").lower()
    
    # List of common forensic markers for editing tools
    known_signatures = ["photoshop", "gimp", "lightroom", "canva", "snapseed", "affinity", "picsart", "adobe"]
    
    return any(signature in software_tag for signature in known_signatures)

def _check_exif_missing(metadata: Dict[str, str]) -> bool:
    """Returns True if no metadata tags were extracted."""
    return not bool(metadata)