# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

import exifread
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

def extract_metadata(path: Path) -> Dict[str, Any]:
    """
    Extracts EXIF metadata from an image file.

    Args:
        path: A pathlib.Path object pointing to the image file.

    Returns:
        A dictionary containing the filename and extracted metadata.
        Returns an empty metadata dictionary if extraction fails or no EXIF data is found.
    """
    logger.info(f"Attempting to extract metadata from: {path.name}")
    
    metadata: Dict[str, str] = {}
    try:
        # Open the image file in binary mode and process EXIF tags
        with path.open('rb') as file:
            exif_data = exifread.process_file(file)

            if not exif_data:
                logger.warning(f"No EXIF data found in: {path.name}")
                return {"filename": str(path), "metadata": {}}

            for key, value in exif_data.items():
                # Filter out noise tags like Thumbnails or Padding to keep data clean
                if "Thumbnail" in str(key) or "Padding" in str(key): # Ensure key is string for 'in' operator
                    continue

                # Convert tags and values to strings to ensure JSON serializability
                metadata[str(key)] = str(value)

    except Exception as e:
        logger.error(f"Failed to extract metadata from {path.name}: {e}")
        return {"filename": str(path), "metadata": {}}

    logger.debug(f"Successfully extracted {len(metadata)} tags from {path.name}.")

    # Structure the final result including the source filename
    result = {
        "filename": str(path), # Convert Path object to string for output consistency
        "metadata": metadata
    }

    return result