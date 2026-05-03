# Name: MetaTrace Lite
# Author: Rodrigo-Tripa (GitHub)
# Description: Lightweight forensic tool for extracting and analyzing image metadata (EXIF)
# Version: 0.4.1

from utils import validate_input_path, collect_input_paths, export_metadata_to_file
from extractor import extract_metadata
from analyzer import analyze_metadata
import argparse
import json
import sys
import logging
from typing import Dict, Any, List

# Configure logging: levels and format
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def _generate_summary(metadata: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, str]:
    """Generates a human-readable summary of the metadata and analysis."""
    summary = {}

    # Camera info
    camera = metadata.get("camera", {})
    if camera.get("make") or camera.get("model"):
        summary["device"] = f"{camera.get('make', 'Unknown')} {camera.get('model', '')}".strip()

    # Date
    dt = metadata.get("datetime", {})
    if dt.get("datetime_original"):
        summary["capture_date"] = dt["datetime_original"]

    # GPS
    gps = metadata.get("gps", {})
    if analysis.get("gps_present"):
        lat = gps.get("decimal_latitude")
        lon = gps.get("decimal_longitude")
        summary["location"] = f"Lat: {lat}, Lon: {lon}"

    # Analysis highlights
    highlights = []
    if analysis.get("editing_software_detected"):
        highlights.append("Edited with software")
    if analysis.get("gps_present"):
        highlights.append("Contains GPS data")
    if analysis.get("device_type") == "phone":
        highlights.append("Captured on mobile device")
    summary["highlights"] = "; ".join(highlights) if highlights else "No notable findings"

    return summary

def main():
    """Main entry point for the MetaTrace Lite application.
    
    Parses command-line arguments, processes input files, extracts and analyzes metadata,
    and outputs results in JSON format.
    """
    parser = argparse.ArgumentParser(
        description="MetaTrace Lite: Lightweight forensic tool for image metadata analysis."
    )
    parser.add_argument("path", help="Path to an image file or a directory containing images to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument("-o", "--output-dir", default="reports", help="Directory to save the report file(s).")
    
    args = parser.parse_args()
    
    # Adjust log level based on verbosity flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    path = args.path

    try:
        # 3. Validate the input path and determine whether it is a file or directory
        validated_path = validate_input_path(path)
        input_paths = collect_input_paths(validated_path)

        # 4. Process files sequentially and aggregate results
        results: List[Dict[str, Any]] = []
        for file_path in input_paths:
            logger.info(f"Processing file: {file_path}")
            result = extract_metadata(file_path)
            analysis = analyze_metadata(result["metadata"])
            result["analysis"] = analysis
            result["summary"] = _generate_summary(result["metadata"], analysis)

            export_metadata_to_file(result, file_path, args.output_dir)
            logger.info(f"Report successfully exported to: {args.output_dir}/{file_path.stem}_report.json")
            results.append(result)

        # 5. Print a single object for one file or a list for batch mode
        if len(results) == 1:
            print(json.dumps(results[0], indent=4))
        else:
            print(json.dumps(results, indent=4))

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        sys.exit(1)
    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
        sys.exit(1)
    except (IOError, EOFError) as e:
        logger.error(f"Failed to process image file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()