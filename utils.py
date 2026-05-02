# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

from pathlib import Path
import json
from typing import Any, Dict, List

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

def validate_input_path(path_str: str) -> Path:
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if path.is_dir():
        return path

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    return path


def collect_input_paths(path: Path) -> List[Path]:
    """Collects supported image file paths from a directory for batch processing."""
    if path.is_file():
        return [path]

    images = sorted(
        [item for item in path.rglob("*") if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS]
    )

    if not images:
        raise ValueError(f"No supported image files found in directory: {path}")

    return images


def export_metadata_to_file(data: Dict[str, Any], input_path: Path, folder_name: str = "reports") -> Path:
    # Create the folder automatically if it doesn't exist
    output_dir = Path(folder_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate report name based on the original file using .stem (filename without extension)
    report_path = output_dir / f"{input_path.stem}_report.json"

    with report_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return report_path