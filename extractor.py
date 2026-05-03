# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

import exifread
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_metadata(path: Path) -> Dict[str, Any]:
    """
    Extracts EXIF metadata from an image file and structures it into categories.

    Args:
        path: A pathlib.Path object pointing to the image file.

    Returns:
        A dictionary containing the filename and structured metadata.
        Returns an empty metadata dictionary if extraction fails or no EXIF data is found.
    """
    logger.info(f"Attempting to extract metadata from: {path.name}")
    
    try:
        # Open the image file in binary mode and process EXIF tags
        with path.open('rb') as file:
            exif_data = exifread.process_file(file)

            if not exif_data:
                logger.warning(f"No EXIF data found in: {path.name}")
                return {"filename": str(path), "metadata": {}}

            # Structure metadata into categories
            structured_metadata = _structure_metadata(exif_data)

    except Exception as e:
        logger.error(f"Failed to extract metadata from {path.name}: {e}")
        return {"filename": str(path), "metadata": {}}

    logger.debug(f"Successfully extracted structured metadata from {path.name}.")

    # Structure the final result including the source filename
    result = {
        "filename": str(path),
        "metadata": structured_metadata
    }

    return result

def _structure_metadata(exif_data: Dict[str, Any]) -> Dict[str, Any]:
    """Structures raw EXIF data into categorized, human-readable metadata."""
    structured = {
        "camera": {},
        "datetime": {},
        "gps": {},
        "image": {},
        "other": {}
    }

    for key, value in exif_data.items():
        key_str = str(key)
        value_str = str(value)

        # Filter out noise
        if "Thumbnail" in key_str or "Padding" in key_str:
            continue

        # Categorize
        if key_str.startswith("Image "):
            subkey = key_str[6:].lower().replace(" ", "_")
            structured["camera"][subkey] = value_str
        elif key_str.startswith("EXIF "):
            subkey = key_str[5:].lower().replace(" ", "_")
            if "datetime" in subkey:
                structured["datetime"][subkey] = _parse_datetime(value_str)
            else:
                structured["image"][subkey] = value_str
        elif key_str.startswith("GPS "):
            subkey = key_str[4:].lower().replace(" ", "_")
            structured["gps"][subkey] = value_str
        else:
            structured["other"][key_str.lower().replace(" ", "_")] = value_str

    # Special handling for GPS coordinates
    if "gpslatitude" in structured["gps"] and "gpslongitude" in structured["gps"]:
        lat = _parse_gps_coord(structured["gps"]["gpslatitude"], structured["gps"].get("gpslatituderef", "N"))
        lon = _parse_gps_coord(structured["gps"]["gpslongitude"], structured["gps"].get("gpslongituderef", "E"))
        structured["gps"]["decimal_latitude"] = lat
        structured["gps"]["decimal_longitude"] = lon

    # Remove empty categories
    structured = {k: v for k, v in structured.items() if v}

    return structured

def _parse_datetime(dt_str: str) -> str:
    """Parses EXIF datetime string to a more readable format."""
    try:
        # EXIF datetime is YYYY:MM:DD HH:MM:SS
        dt = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
        return dt.isoformat()
    except ValueError:
        return dt_str

def _parse_gps_coord(coord_str: str, ref: str) -> Optional[float]:
    """Parses GPS coordinate string to decimal degrees safely."""
    try:
        # coord_str example: "[37, 47, 1234/100]"
        parts = coord_str.strip("[]").split(", ")

        degrees = float(parts[0])
        minutes = float(parts[1])

        # Safe parsing instead of eval()
        seconds_raw = parts[2]

        if "/" in seconds_raw:
            numerator, denominator = seconds_raw.split("/")
            seconds = float(numerator) / float(denominator)
        else:
            seconds = float(seconds_raw)

        decimal = degrees + (minutes / 60) + (seconds / 3600)

        if ref in ["S", "W"]:
            decimal = -decimal

        return round(decimal, 6)

    except (ValueError, IndexError, ZeroDivisionError):
        return None