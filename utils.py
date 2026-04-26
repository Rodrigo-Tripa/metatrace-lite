# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

from pathlib import Path
import json
from typing import Any, Dict

def validate_input_path(path_str: str) -> Path:
    # Define the list of supported image file extensions
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    path = Path(path_str)

    # Check if the provided path exists on the system
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    # Ensure the path points to a file and not a directory
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    # Verify that the file extension is supported
    if path.suffix.lower() not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    return path

def export_metadata_to_file(data: Dict[str, Any], input_path: Path, folder_name: str = "reports") -> Path:
    # Create the folder automatically if it doesn't exist
    output_dir = Path(folder_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate report name based on the original file using .stem (filename without extension)
    report_path = output_dir / f"{input_path.stem}_report.json"

    with report_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return report_path