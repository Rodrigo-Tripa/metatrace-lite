# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

def analyze_metadata(metadata):
    analysis = {}

    mapping = {
        "gps_present": _check_gps_presence,
        "editing_software_detected": _check_editing_software,
        "exif_missing": _check_exif_missing
    }

    for key, function in mapping.items():
        analysis[key] = function(metadata)

    return analysis


def _check_gps_presence(metadata):
    return 'GPS GPSLatitude' in metadata and 'GPS GPSLongitude' in metadata

def _check_editing_software(metadata):
    image_software = metadata.get("Image Software", "")
    softwares = ["Photoshop", "GIMP", "Lightroom", "Canva", "Snapseed"]
    for software in softwares:
        if software in image_software:
            return True
    return False


def _check_exif_missing(metadata):
    return not bool(metadata)