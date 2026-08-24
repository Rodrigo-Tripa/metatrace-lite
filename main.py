# Name: MetaTrace Lite
# Author: Rodrigo-Tripa (GitHub)
# Description: Lightweight forensic tool for extracting and analyzing image metadata (EXIF)
# Version: 0.4.2 (Updated with bug fixes)

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
    """Generates a human-readable summary of the metadata and analysis.
    
    Extracts key forensic indicators:
    - Device information (make, model)
    - Capture timestamp
    - Geographic coordinates (if present)
    - Notable analysis findings
    """
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
        accuracy = analysis.get("gps_accuracy", "unknown")
        highlights.append(f"Contains GPS data ({accuracy} accuracy)")
    if analysis.get("device_type") == "phone":
        highlights.append("Captured on mobile device")
    elif analysis.get("device_type") == "camera":
        highlights.append("Captured on dedicated camera")
    
    summary["highlights"] = "; ".join(highlights) if highlights else "No notable findings"

    return summary

def main():
    """Main entry point for the MetaTrace Lite application.
    
    Parses command-line arguments, processes input files, extracts and analyzes metadata,
    and outputs results in JSON format.
    
    Workflow:
    1. Validate input path (file or directory)
    2. Collect all supported image files
    3. Extract metadata from each file
    4. Perform forensic analysis
    5. Generate human-readable summary
    6. Export results to JSON and stdout
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
        logger.debug("Debug logging enabled")

    path = args.path

    try:
        # Validate the input path and determine whether it is a file or directory
        logger.debug(f"Validating input path: {path}")
        validated_path = validate_input_path(path)
        input_paths = collect_input_paths(validated_path)
        
        logger.info(f"Found {len(input_paths)} image(s) to process")

        # Process files sequentially and aggregate results
        results: List[Dict[str, Any]] = []
        failed_files: List[Dict[str, Any]] = []
        
        for idx, file_path in enumerate(input_paths, 1):
            logger.info(f"[{idx}/{len(input_paths)}] Processing file: {file_path}")
            
            try:
                result = extract_metadata(file_path)
                analysis = analyze_metadata(result["metadata"])
                result["analysis"] = analysis
                result["summary"] = _generate_summary(result["metadata"], analysis)

                export_metadata_to_file(result, file_path, args.output_dir)
                logger.info(f"Report successfully exported to: {args.output_dir}/{file_path.stem}_report.json")
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                failed_files.append({
                    "filename": str(file_path),
                    "error": str(e)
                })

        # Print summary of processing
        if failed_files:
            logger.warning(f"{len(failed_files)} file(s) failed to process")
        
        # Output results
        # 5. Print a single object for one file or a list for batch mode
        if len(results) == 1:
            print(json.dumps(results[0], indent=4))
        elif len(results) > 1:
            output = {
                "summary": {
                    "total_processed": len(results),
                    "total_failed": len(failed_files)
                },
                "results": results
            }
            if failed_files:
                output["failed"] = failed_files
            print(json.dumps(output, indent=4))
        else:
            logger.error("No files were successfully processed")
            sys.exit(1)

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
