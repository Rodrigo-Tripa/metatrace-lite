# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

from pathlib import Path
import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Centralized configuration for supported image formats
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}

def validate_input_path(path_str: str) -> Path:
    """Validates and normalizes input path.
    
    Args:
        path_str: String representation of file or directory path
        
    Returns:
        pathlib.Path object pointing to validated file or directory
        
    Raises:
        FileNotFoundError: If path does not exist
        ValueError: If path is unsupported file type or invalid
    """
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if path.is_dir():
        logger.debug(f"Validated directory path: {path}")
        return path

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}")

    logger.debug(f"Validated file path: {path}")
    return path


def collect_input_paths(path: Path) -> List[Path]:
    """Collects supported image file paths from a directory for batch processing.
    
    Args:
        path: pathlib.Path object (file or directory)
        
    Returns:
        List of pathlib.Path objects for all supported image files (sorted)
        
    Raises:
        ValueError: If directory contains no supported image files
    """
    if path.is_file():
        return [path]

    # Recursive glob to find images in subdirectories
    images = sorted(
        [item for item in path.rglob("*") if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS]
    )

    if not images:
        raise ValueError(f"No supported image files found in directory: {path}")

    logger.debug(f"Found {len(images)} image file(s) in {path}")
    return images


def export_metadata_to_file(data: Dict[str, Any], input_path: Path, folder_name: str = "reports") -> Path:
    """Exports structured metadata and analysis to JSON file.
    
    Creates output directory if it doesn't exist. Report filename is derived from
    the original image name (e.g., "photo_report.json").
    
    Args:
        data: Dictionary containing metadata, analysis, and summary
        input_path: pathlib.Path object of the original image file
        folder_name: Name of output directory (default: "reports")
        
    Returns:
        pathlib.Path object pointing to the generated report file
        
    Raises:
        IOError: If file cannot be written
    """
    # Create the folder automatically if it doesn't exist
    output_dir = Path(folder_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate report name based on the original file using .stem (filename without extension)
    report_path = output_dir / f"{input_path.stem}_report.json"

    try:
        with report_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.debug(f"Successfully exported report to: {report_path}")
    except IOError as e:
        logger.error(f"Failed to write report file {report_path}: {e}")
        raise

    return report_path
